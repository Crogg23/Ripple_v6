#!/usr/bin/env python3
"""DOL OLMS union financial reports (LM-2/3/4 core filing table), full history.

The OLPDR download servlet uses per-session rotating tokens: POST
GetYearlyDownlaodFilenamesServlet -> {filenames: [years], encriptedFilenames:
[tokens]}, then GET GetYearlyFileServlet?report=<token> per year. The host
TLS-fingerprint-blocks python-requests (connection refused) but serves curl,
so all transport shells out to curl.

Each yearly zip holds ~25 pipe-delimited headerless files; we load only the
lm_data core filing table, appending YEAR per row. Year-checkpointed like
scripts/nih_reporter_load.py — rerun resumes at the next undone year.

    python scripts/dol_olms_load.py          # full run (checkpointed)
"""
from __future__ import annotations
import datetime as dt
import hashlib
import io
import json
import subprocess
import sys
import uuid
import zipfile
from pathlib import Path

import pandas as pd

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import ingest  # noqa: E402

BASE = "https://olmsapps.dol.gov/olpdr"
TABLE = "FED_DOL_OLMS"
SID = "fed_dol_olms"
CKPT = _REPO / "outputs" / "_dol_olms_checkpoint.json"
LOG = _REPO / "outputs" / "_dol_olms_progress.log"

# NOTE: the lm_data_data_<year>.txt member is pipe-delimited WITH a header row
# (the sprint-b spec's headerless 21-column assumption was wrong — that matched
# the meta/dictionary file). Columns come from the file itself; the table is
# created from the first landed year and later years must fit inside it.


def log(msg):
    line = f"{dt.datetime.now().isoformat()} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


COOKIES = _REPO / "outputs" / "_dol_olms_cookies.txt"


def curl(args: list[str]) -> bytes:
    r = subprocess.run(["curl", "-s", "--max-time", "600", *args],
                       capture_output=True, check=True)
    return r.stdout


def year_tokens() -> dict[str, str]:
    # Tokens are SESSION-BOUND: without the JSESSIONID cookie from this POST,
    # the file servlet 404s ("no such file") — carry the cookie jar everywhere.
    raw = curl(["-c", str(COOKIES), "-X", "POST",
                "-H", "Content-Type: application/json",
                "-d", "{}", f"{BASE}/GetYearlyDownlaodFilenamesServlet"])
    d = json.loads(raw)
    return dict(zip(d["filenames"], d["encriptedFilenames"]))


def main():
    conn = snow.connect()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    done: list[str] = []
    total = 0
    if CKPT.exists():
        ck = json.loads(CKPT.read_text())
        done, total = ck["done_years"], ck["total_loaded"]
        log(f"resuming: {len(done)} years done, total={total}")

    tokens = year_tokens()
    years = sorted(tokens.keys())

    from snowflake.connector.pandas_tools import write_pandas

    table_cols: list[str] | None = None
    for y in years:
        if y in done:
            continue
        blob = curl(["-b", str(COOKIES), f"{BASE}/GetYearlyFileServlet?report={tokens[y]}"])
        if not blob.startswith(b"PK"):
            log(f"year={y}: not a zip ({blob[:60]!r}) -- skipping as failed year")
            continue
        zf = zipfile.ZipFile(io.BytesIO(blob))
        member = next((n for n in zf.namelist() if n.lower().startswith("lm_data_data")), None)
        if not member:
            log(f"year={y}: no lm_data_data member in {zf.namelist()[:5]} -- skipping")
            continue
        df = pd.read_csv(io.BytesIO(zf.read(member)), sep="|", header=0,
                         dtype=str, keep_default_na=False,
                         na_values=[], encoding="latin-1", engine="python",
                         on_bad_lines="warn")
        df.columns = [ingest._sf_col(c) for c in df.columns]

        if table_cols is None and not done:
            cur = conn.cursor()
            cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{TABLE}")
            table_cols = list(df.columns)
            ddl = ", ".join(f'"{c}" VARCHAR' for c in table_cols)
            ddl += ', "REPORT_YEAR" VARCHAR, "_INGESTED_AT" VARCHAR, "_SOURCE_RUN_ID" VARCHAR, "_SRC_SHA256" VARCHAR'
            cur.execute(f'CREATE TABLE LIBRARY_RAW.LANDING.{TABLE} ({ddl})')
            cur.close()
            log(f"created {TABLE} with {len(table_cols)} columns from year {y}")
        elif table_cols is None:
            cur = conn.cursor()
            cur.execute(f"select column_name from LIBRARY_RAW.information_schema.columns "
                        f"where table_schema='LANDING' and table_name='{TABLE}' order by ordinal_position")
            table_cols = [r[0] for r in cur.fetchall()
                          if r[0] not in ("REPORT_YEAR", "_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256")]
            cur.close()

        extra = [c for c in df.columns if c not in table_cols]
        if extra:
            raise RuntimeError(f"year={y} has columns not in the table: {extra} -- schema drift, refusing")
        for c in table_cols:
            if c not in df.columns:
                df[c] = None
        df = df[table_cols]
        sha = hashlib.sha256(blob).hexdigest()[:16]
        df["REPORT_YEAR"] = y
        df["_INGESTED_AT"] = started.isoformat()
        df["_SOURCE_RUN_ID"] = run_id
        df["_SRC_SHA256"] = sha
        ok, _c, n, _ = write_pandas(conn, df, table_name=TABLE,
                                    database="LIBRARY_RAW", schema="LANDING",
                                    quote_identifiers=False)
        if not ok:
            raise RuntimeError(f"write failed year={y}")
        total += len(df)
        done.append(y)
        CKPT.write_text(json.dumps({"done_years": done, "total_loaded": total}))
        log(f"year={y} rows={len(df)} total={total}")

    ended = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    ingest._log_run(conn, SID, run_id, "success", total, None, run_id[:16], BASE,
                    started, ended, f"{SID}; OLMS LM core filings all years; {total:,} rows")
    log(f"DONE total={total}")
    CKPT.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
