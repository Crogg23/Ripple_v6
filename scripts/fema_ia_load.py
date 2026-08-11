"""FEMA OpenFEMA IndividualsAndHouseholdsProgramValidRegistrations loader.

~26.2M rows (per API metadata count). Paginates via $skip/$top=10000,
appends to Snowflake in batches, checkpoints skip offset to disk so a
kill/restart resumes instead of re-downloading from zero.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import sys
import time
import uuid
from pathlib import Path

import pandas as pd
import requests

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
import _bulk_load_utils as bulk  # noqa: E402


def _as_text(v):
    """Stringify for an all-VARCHAR landing table WITHOUT inventing the text 'nan'.

    THE BUG THIS FIXES (2026-08-11). Every loader here did
    `None if v is None else str(v)`. pandas does not keep a JSON null as None --
    it becomes float NaN as soon as the column is built -- so `v is None` was
    False and str(NaN) wrote the four characters n-a-n into the warehouse. The
    column then reads as populated: FDIC's LEI showed 6,260 non-null values, of
    which 4,008 were the string 'nan'. That is exactly the sentinel-masked-blank
    trap that has already fooled this platform on two other join keys, and it is
    worse for a KEY column, because 'nan' joins to 'nan'.

    Also catches pandas' NA/NaT and the whitespace-only strings that some of
    these APIs return in place of a null.
    """
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass  # arrays/lists raise here; they are real values, fall through
    s = str(v)
    return None if s.strip() == "" else s


BASE = "https://www.fema.gov/api/open/v2/IndividualsAndHouseholdsProgramValidRegistrations"
TABLE = "FED_FEMA_IA_HOUSING_REGISTRATIONS"
TOP = 10000
ATTEMPTS = 10
CKPT = _REPO / "outputs" / "_fema_ia_checkpoint.json"
LOG = _REPO / "outputs" / "_fema_ia_progress.log"


def log(msg):
    line = f"{dt.datetime.now().isoformat()} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def fetch_page(skip: int) -> list[dict]:
    """One page, retried hard.

    WHY THE RETRY BUDGET IS THIS BIG (2026-08-11): the run died at
    skip=19,520,000 after six straight failures. The page itself is fine --
    re-requesting the exact same offset later returned 200 with data. OpenFEMA
    just degrades badly at deep offsets, because $skip forces it to walk the
    whole ordered set every call, so single requests routinely blow past two
    minutes near the 25.9M-row tail. The old budget (120s timeout, 6 tries,
    3-18s linear backoff) was tuned on shallow pages and could not ride out a
    slow patch. Timeout and backoff now scale with attempt number: a page gets
    ~25 minutes of wall clock before we call it dead.
    """
    params = {"$top": TOP, "$skip": skip, "$orderby": "id"}
    last = None
    for attempt in range(ATTEMPTS):
        try:
            r = requests.get(BASE, params=params, timeout=min(120 + 60 * attempt, 420))
            if r.status_code == 200:
                d = r.json()
                return d.get("IndividualsAndHouseholdsProgramValidRegistrations", [])
            last = f"HTTP {r.status_code}"
        except Exception as e:
            last = repr(e)[:120]
        wait = min(10 * (2 ** attempt), 180)
        log(f"  retry skip={skip} attempt={attempt + 1}/{ATTEMPTS} ({last}) -- sleeping {wait}s")
        time.sleep(wait)
    raise RuntimeError(f"failed page skip={skip} after {ATTEMPTS} attempts ({last})")


def main():
    conn = snow.connect()
    skip = 0
    first_batch = True
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    total_loaded = 0

    if CKPT.exists():
        ck = json.loads(CKPT.read_text())
        skip = ck["skip"]
        total_loaded = ck["total_loaded"]
        first_batch = False
        log(f"resuming at skip={skip}, total_loaded={total_loaded}")
    else:
        # fresh run -- pre-create with an explicit all-VARCHAR schema so a page
        # with an all-null column (e.g. rentalAssistanceEndDate) never gets
        # auto_create_table-inferred as NUMBER and breaks a later text batch.
        sample = fetch_page(0)
        if not sample:
            log("no data returned on probe page -- aborting")
            sys.exit(1)
        cols = sorted({k for rec in sample for k in rec.keys()})
        sf_cols = [ingest._sf_col(c) for c in cols]
        cur = conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{TABLE}")
        ddl_cols = ", ".join(f'"{c}" VARCHAR' for c in sf_cols)
        ddl_cols += ', "_INGESTED_AT" VARCHAR, "_SOURCE_RUN_ID" VARCHAR, "_SRC_SHA256" VARCHAR'
        cur.execute(f'CREATE TABLE LIBRARY_RAW.LANDING.{TABLE} ({ddl_cols})')
        cur.close()
        log(f"created {TABLE} with {len(sf_cols)} VARCHAR columns")

    from snowflake.connector.pandas_tools import write_pandas

    while True:
        batch = fetch_page(skip)
        if not batch:
            log(f"empty page at skip={skip} -- done")
            break
        df = pd.DataFrame(batch)
        df.columns = [ingest._sf_col(c) for c in df.columns]
        # force everything to string so auto_create_table always picks VARCHAR --
        # mixed None/bool/number/date columns across pages otherwise cause
        # Snowflake type-inference conflicts on later COPY INTO batches.
        for c in df.columns:
            df[c] = df[c].apply(_as_text)
        sha = hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()[:16]
        df["_INGESTED_AT"] = started.isoformat()
        df["_SOURCE_RUN_ID"] = run_id
        df["_SRC_SHA256"] = sha

        ok, _c, n, _ = write_pandas(
            conn, df, table_name=TABLE,
            database="LIBRARY_RAW", schema="LANDING",
            auto_create_table=False, overwrite=False, quote_identifiers=False,
        )
        total_loaded += n
        skip += TOP
        first_batch = False
        CKPT.write_text(json.dumps({"skip": skip, "total_loaded": total_loaded}))
        if (skip // TOP) % 10 == 0:
            log(f"skip={skip} total_loaded={total_loaded}")
        if len(batch) < TOP:
            log(f"final short page ({len(batch)}) -- done, total_loaded={total_loaded}")
            break

    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*), COUNT(DISTINCT ID) FROM LIBRARY_RAW.LANDING.{TABLE}")
    total, distinct_id = cur.fetchone()
    log(f"FINAL VERIFY: {total} rows, {distinct_id} distinct ID")

    ended = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    # Quality gate (audit 2026-08-05/06 finding: this paginated loader had NO gate at
    # all -- not even the ad-hoc ingest.assess_density pattern other loaders use. Can't
    # check density before writing since pages stream in and append; check the live
    # landed table right after, like fracfocus_load.py's fix for the same shape of
    # loader last session.
    prev_rows = ingest._latest_success_rows(conn, "fed_fema_ia_housing_registrations")
    passed, report = bulk.assess_bulk_load(conn, TABLE, prev_row_count=prev_rows)
    status = "success" if passed else "partial"
    if not passed:
        log(f"QUALITY GATE FAILED for {TABLE}: {report}")
    ingest._log_run(conn, source_id="fed_fema_ia_housing_registrations", run_id=run_id,
                     status=status, row_count=total, file_bytes=None,
                     sha="paginated", url=BASE, started=started, ended=ended,
                     message=f"paginated load, {skip} skip offset reached. DQ: {report}")
    if CKPT.exists():
        CKPT.unlink()
    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
