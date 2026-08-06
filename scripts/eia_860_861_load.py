"""EIA-860 (generator/plant/utility) + EIA-861 (utility sales/service territory)
bulk Excel loader. Files pre-downloaded to outputs/_eia860.zip / _eia861.zip
(eia.gov works fine with a browser User-Agent header -- the bare
requests-default UA on the first attempt returned an HTML redirect page
instead of the zip; noting as a fetch trap).

Each workbook's row 0 is a title caption ("2024 Form EIA-860 Data -
Schedule 2, 'Plant Data'"), real headers are row 1 -> header=1.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import io
import re
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

SKIP_SUBSTR = ("instructions", "Form.xlsx", "Layout")


def clean_name(fname: str, prefix: str) -> str:
    stem = Path(fname).stem
    stem = re.sub(r"_Y?20\d\d$", "", stem)  # strip trailing year
    stem = re.sub(r"[^a-zA-Z0-9]+", "_", stem).strip("_").upper()
    tbl = f"{prefix}_{stem}"
    return tbl[:80]


def load_workbook(conn, data: bytes, zip_name: str, fname: str, prefix: str, source_id_base: str, url: str):
    from snowflake.connector.pandas_tools import write_pandas
    # try header=1 first (EIA convention); fall back to header=0 if that fails to find real columns
    try:
        df = pd.read_excel(io.BytesIO(data), header=1, dtype=str, engine="openpyxl")
    except Exception as e:
        print(f"    SKIP {fname}: read error {str(e)[:150]}")
        return None
    if df.shape[1] < 2 or df.shape[0] == 0:
        # maybe header=0 is right (some files like Balancing_Authority have no title row)
        try:
            df2 = pd.read_excel(io.BytesIO(data), header=0, dtype=str, engine="openpyxl")
            if df2.shape[1] > df.shape[1]:
                df = df2
        except Exception:
            pass
    if df.shape[0] == 0:
        print(f"    SKIP {fname}: 0 rows")
        return None

    # Quality gate (audit 2026-08-05/06 finding: none here at all -- and this
    # function DROPs the old table before writing, so an empty/degenerate parse
    # would destroy the existing good table with nothing left to fall back to).
    density = ingest.assess_density(df)
    if density["empty"]:
        print(f"    SKIP {fname}: parsed frame looks empty/degenerate -- {density['reason']} "
              f"(populated_fraction={density['populated_fraction']:.3f})")
        return None

    df.columns = [ingest._sf_col(str(c)) for c in df.columns]
    tbl = clean_name(fname, prefix)
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    sha = hashlib.sha256(data).hexdigest()
    df["_INGESTED_AT"] = started.isoformat()
    df["_SOURCE_RUN_ID"] = run_id
    df["_SRC_FILE"] = fname

    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS LIBRARY_RAW.LANDING."{tbl}"')
    cur.close()
    ok, _c, n, _ = write_pandas(
        conn, df, table_name=tbl,
        database="LIBRARY_RAW", schema="LANDING",
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    ended = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    source_id = f"{source_id_base}_{tbl.split('_', 2)[-1].lower()}"
    ingest._log_run(conn, source_id=source_id, run_id=run_id,
                     status="success" if ok else "failed", row_count=n, file_bytes=len(data),
                     sha=sha, url=url, started=started, ended=ended,
                     message=f"source file {fname}")
    print(f"    {tbl}: {n:,} rows")
    return tbl, n


def process_zip(conn, zip_path: str, prefix: str, source_id_base: str, url: str):
    results = []
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if not name.lower().endswith((".xlsx", ".xls")):
                continue
            if any(s.lower() in name.lower() for s in SKIP_SUBSTR):
                print(f"  skip (form/instructions/layout): {name}")
                continue
            print(f"  loading {name}...")
            with zf.open(name) as f:
                data = f.read()
            r = load_workbook(conn, data, zip_path, name, prefix, source_id_base, url)
            if r:
                results.append(r)
    return results


def main():
    conn = snow.connect()
    print("=== EIA-860 ===")
    r860 = process_zip(conn, str(_REPO / "outputs" / "_eia860.zip"), "FED_EIA860",
                        "fed_eia860", "https://www.eia.gov/electricity/data/eia860/")
    print("=== EIA-861 ===")
    r861 = process_zip(conn, str(_REPO / "outputs" / "_eia861.zip"), "FED_EIA861",
                        "fed_eia861", "https://www.eia.gov/electricity/data/eia861/")
    print("\nSummary:")
    for tbl, n in r860 + r861:
        print(f"  {tbl}: {n:,}")


if __name__ == "__main__":
    main()
