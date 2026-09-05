"""Load CFPB HMDA Historic LAR (pre-2018) data — first-lien owner-occupied 1-4
family records, nationwide, with plain-language labels.

Source: https://www.consumerfinance.gov/data-research/hmda/historic-data/
Record layout: https://files.consumerfinance.gov/hmda-historic-data-dictionaries/lar_record_format.pdf
  Comma-separated, 41 fields, "Respondent ID" (Legacy Respondent ID, 10-char
  alphanumeric) is the join key for this era — NOT the LEI used by modern HMDA
  (fed_cfpb_hmda, 2022-era, already landed separately).

This loads a 3-year slice (2015-2017). Two file families exist:
  first-lien  "first-lien-owner-occupied-1-4-family" -- ORIGINATED loans only,
              every row is ACTION_TAKEN=1. Loaded 2026-08-05, 19.1M rows.
              Any denial-rate query on it returns 0.0%. (trap, 2026-09-05)
  all         "all-records" -- every application, all 8 action codes, ~45M rows.
              Loaded 2026-09-05 to replace the first-lien slice.
Zips must already be downloaded to scripts/hmda_historic_scratch/
  hmda_<year>.zip       (first-lien)      hmda_<year>_all.zip   (all)

    python scripts/hmda_historic_lar_load.py --family all          # preview
    python scripts/hmda_historic_lar_load.py --family all --run    # actual load
"""
from __future__ import annotations

import argparse
import sys
import uuid
import zipfile
from pathlib import Path

import pandas as pd

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))

try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

TABLE = "FED_CFPB_HMDA_HISTORIC"  # must match dbt source name in stg_fed_cfpb_hmda_historic__records.sql
SCRATCH = Path(__file__).parent / "hmda_historic_scratch"
YEARS = [2015, 2016, 2017]
CHUNK = 200_000  # rows per write_pandas batch
FAMILY = "all"   # set by --family; "all" or "first-lien"


def _zip_path(year: int) -> Path:
    suffix = "_all" if FAMILY == "all" else ""
    return SCRATCH / f"hmda_{year}{suffix}.zip"


def _find_csv_in_zip(zf: zipfile.ZipFile) -> str:
    names = [n for n in zf.namelist() if n.lower().endswith(".csv") or n.lower().endswith(".txt")]
    if not names:
        raise RuntimeError(f"no csv/txt found in zip: {zf.namelist()}")
    return names[0]


def preview():
    for y in YEARS:
        zpath = _zip_path(y)
        if not zpath.exists():
            print(f"  {y}: MISSING {zpath}")
            continue
        with zipfile.ZipFile(zpath) as zf:
            inner = _find_csv_in_zip(zf)
            with zf.open(inner) as f:
                header = f.readline().decode("utf-8", errors="replace").strip()
                first_row = f.readline().decode("utf-8", errors="replace").strip()
        cols = header.split(",")
        print(f"  {y}: inner={inner!r}  n_cols={len(cols)}")
        print(f"       header: {cols}")
        print(f"       row1  : {first_row.split(',')}")


def load_year(conn, year: int, staging: str, first: bool) -> int:
    zpath = _zip_path(year)
    with zipfile.ZipFile(zpath) as zf:
        inner = _find_csv_in_zip(zf)
        total = 0
        with zf.open(inner) as f:
            reader = pd.read_csv(f, dtype=str, chunksize=CHUNK, low_memory=False)
            for i, chunk in enumerate(reader):
                chunk.columns = [c.strip().upper().replace(" ", "_") for c in chunk.columns]
                if "AS_OF_YEAR" not in chunk.columns:
                    chunk.insert(0, "AS_OF_YEAR", str(year))
                if "SOURCE_YEAR" not in chunk.columns:
                    chunk.insert(1, "SOURCE_YEAR", str(year))
                from snowflake.connector.pandas_tools import write_pandas
                write_pandas(
                    conn, chunk, staging, database="LIBRARY_RAW", schema="LANDING",
                    auto_create_table=first and i == 0, overwrite=False,
                )
                total += len(chunk)
                print(f"    {year}: wrote {total:,} rows so far...", end="\r")
    print(f"    {year}: {total:,} rows total.                    ")
    return total


def load(conn) -> int:
    staging = f"{TABLE}__STAGING"
    cur = conn.cursor()
    cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{staging}")

    grand_total = 0
    first = True
    for y in YEARS:
        n = load_year(conn, y, staging, first)
        grand_total += n
        first = False

    cur.execute(f"ALTER TABLE LIBRARY_RAW.LANDING.{staging} ADD COLUMN IF NOT EXISTS "
                f"_INGESTED_AT TIMESTAMP_NTZ")
    cur.execute(f"ALTER TABLE LIBRARY_RAW.LANDING.{staging} ADD COLUMN IF NOT EXISTS "
                f"_SOURCE_RUN_ID STRING")
    cur.execute(f"UPDATE LIBRARY_RAW.LANDING.{staging} SET "
                f"_INGESTED_AT = CURRENT_TIMESTAMP(), _SOURCE_RUN_ID = UUID_STRING() "
                f"WHERE _INGESTED_AT IS NULL")

    cur.execute(f"SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.{staging}")
    n = cur.fetchone()[0]
    if n == 0:
        cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{staging}")
        print("  EMPTY — staging dropped, no swap.")
        return 0

    if FAMILY == "first-lien":
        # 2026-09-05: the live table is all-records (45M rows, 8 action codes).
        # Swapping the originated-only slice back in is a downgrade; make it deliberate.
        ans = input(f"  {TABLE} is all-records; replace it with the first-lien slice? [yes/NO] ")
        if ans.strip().lower() != "yes":
            cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{staging}")
            print("  aborted, staging dropped, live table untouched.")
            return 0
    cur.execute(f"CREATE TABLE IF NOT EXISTS LIBRARY_RAW.LANDING.{TABLE} "
                f"LIKE LIBRARY_RAW.LANDING.{staging}")
    cur.execute(f"ALTER TABLE LIBRARY_RAW.LANDING.{staging} "
                f"SWAP WITH LIBRARY_RAW.LANDING.{TABLE}")
    cur.execute(f"DROP TABLE IF EXISTS LIBRARY_RAW.LANDING.{staging}")
    print(f"  loaded {n:,} rows -> LIBRARY_RAW.LANDING.{TABLE}")
    return n


def register(conn, n_rows: int):
    cur = conn.cursor()
    cur.execute(f"""
        MERGE INTO LIBRARY_META.REGISTRY.SOURCE_REGISTRY t
        USING (SELECT 'FED_CFPB_HMDA_HISTORIC' AS SOURCE_ID) s ON t.SOURCE_ID = s.SOURCE_ID
        WHEN NOT MATCHED THEN INSERT (SOURCE_ID, NAME, PUBLISHER, DESCRIPTION,
            JURISDICTION, CATEGORY, JOIN_KEYS, PRIORITY_TIER, ACCESS_METHOD, URL,
            UNIT_OF_OBSERVATION, UPDATE_CADENCE, DOMAIN_PRIMARY)
        VALUES ('FED_CFPB_HMDA_HISTORIC',
            'HMDA Historic LAR (pre-2018), first-lien owner-occupied 1-4 family, nationwide',
            'CFPB / FFIEC',
            'Historic (pre-2018) HMDA Loan Application Register, 2015-2017 slice landed. ' ||
            'Legacy Respondent ID (not LEI) is the join key for this era -- distinct from ' ||
            'the modern LEI-keyed fed_cfpb_hmda (2022-era) table.',
            'US', 'consumer_finance', 'RESPONDENT_ID, AGENCY_CODE, AS_OF_YEAR', '1',
            'bulk flat file',
            'https://www.consumerfinance.gov/data-research/hmda/historic-data/',
            'one row = one loan application (first-lien owner-occupied 1-4 family)',
            'annual', 'consumer_finance')
    """)
    cur.execute(f"SELECT COUNT(DISTINCT ACTION_TAKEN), "
                f"SUM(IFF(ACTION_TAKEN = '3', 1, 0)) FROM LIBRARY_RAW.LANDING.{TABLE}")
    n_actions, n_denied = cur.fetchone()
    if FAMILY == "all" and (n_actions < 2 or not n_denied):
        raise RuntimeError(f"--family all but the table holds {n_actions} ACTION_TAKEN codes "
                           f"and {n_denied} denials; refusing to label the registry all-records")
    if FAMILY == "all":
        cur.execute("""
            UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY SET
              NAME = 'HMDA Historic LAR (pre-2018), all records, nationwide',
              DESCRIPTION = 'Historic (pre-2018) HMDA Loan Application Register, 2015-2017, ' ||
                'all-records file family: every application, all 8 ACTION_TAKEN codes. ' ||
                'Replaced the originated-only first-lien slice on 2026-09-05. ' ||
                'Legacy Respondent ID (not LEI) is the join key for this era.',
              UNIT_OF_OBSERVATION = 'one row = one loan application, any action taken'
            WHERE SOURCE_ID = 'FED_CFPB_HMDA_HISTORIC'
        """)
    else:
        cur.execute("""
            UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY SET
              NAME = 'HMDA Historic LAR (pre-2018), first-lien owner-occupied 1-4 family, nationwide',
              DESCRIPTION = 'Historic (pre-2018) HMDA Loan Application Register, 2015-2017, ' ||
                'first-lien-owner-occupied file family: ORIGINATED loans only, ACTION_TAKEN=1. ' ||
                'Legacy Respondent ID (not LEI) is the join key for this era.',
              UNIT_OF_OBSERVATION = 'one row = one originated loan (first-lien owner-occupied 1-4 family)'
            WHERE SOURCE_ID = 'FED_CFPB_HMDA_HISTORIC'
        """)
    print(f"  registered {TABLE} in SOURCE_REGISTRY (family={FAMILY}, {n_actions} action codes)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--family", choices=["all", "first-lien"], default="all")
    ap.add_argument("--register-only", action="store_true",
                    help="skip the load; run registry update + quality gate on the live table")
    args = ap.parse_args()
    global FAMILY
    FAMILY = args.family

    print(f"HMDA Historic LAR Loader (years {YEARS}, family {FAMILY})")
    print(f"  Table: LIBRARY_RAW.LANDING.{TABLE}")

    if not args.run:
        preview()
        print("\n  (preview only — add --run to actually load)")
        return 0

    conn = snow.connect()
    try:
        n = load(conn) if not args.register_only else 1
        if n > 0:
            register(conn, n)
            # Quality gate + INGEST_RUNS row (audit 2026-08-05 finding #3:
            # this loader bypassed the gate — failure must reach exit code)
            passed, report = bulk.run_quality_gate(
                conn, TABLE, TABLE, str(uuid.uuid4()))
            if not passed:
                print(f"  QUALITY GATE FAILED: {report}")
                return 1
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
