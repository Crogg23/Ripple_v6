"""Full-national re-ingest of the IRS Exempt Organizations Business Master File.

WHY THIS EXISTS (2026-08-09): the 2026-08-07 tier-1 bulk sweep landed only
eo1.csv (region 1 of 4 -- the Northeast, 280,922 rows across 8 states) but the
catalog recorded the source as fully landed. The real national extract is the
union of eo1.csv..eo4.csv (~1.9M orgs). This loader pulls all four region
files, unions them, and atomically replaces LIBRARY_RAW.LANDING.FED_IRS_EO_BMF.

Same conventions as scripts/recon_bulk_load_tier1_remaining_2026-08-07.py:
one run_id for the load, sha256 provenance (manifest sha over the four file
shas), quality gate via _bulk_load_utils, overwrite via write_pandas with a
staging SWAP so a crash never leaves the live table half-written.

    python scripts/irs_eo_bmf_full_load.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import sys
import uuid
from pathlib import Path

import pandas as pd
import requests

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

TABLE = "FED_IRS_EO_BMF"
STAGING = TABLE + "__STAGING"
URLS = [f"https://www.irs.gov/pub/irs-soi/eo{i}.csv" for i in (1, 2, 3, 4)]
USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}


def main():
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc)
    frames = []
    file_shas = []
    for url in URLS:
        r = requests.get(url, headers=USER_AGENT, timeout=600)
        r.raise_for_status()
        file_shas.append(hashlib.sha256(r.content).hexdigest())
        df = pd.read_csv(io.BytesIO(r.content), dtype=str, low_memory=False,
                         encoding_errors="replace")
        print(f"{url}: {len(df):,} rows, {len(df.columns)} cols")
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    print(f"union: {len(df):,} rows")

    manifest_sha = hashlib.sha256("".join(file_shas).encode()).hexdigest()
    df[bulk.META_INGESTED_AT] = started.replace(tzinfo=None)
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = manifest_sha

    conn = snow.connect()
    from snowflake.connector.pandas_tools import write_pandas
    # Same sanitizer the 2026-08-07 sweep used (it's what produced the existing
    # table's C_GROUP / C_ORGANIZATION names for the reserved-word columns).
    df.columns = [bulk.sf_col(c) for c in df.columns]
    ok, _c, nrows, _ = write_pandas(
        conn, df, table_name=STAGING,
        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError("write_pandas failed for staging table")
    fq = lambda t: f'"{bulk.LANDING_DB}"."{bulk.LANDING_SCHEMA}"."{t}"'
    cur = conn.cursor()
    cur.execute(f"ALTER TABLE {fq(STAGING)} SWAP WITH {fq(TABLE)}")
    cur.execute(f"DROP TABLE IF EXISTS {fq(STAGING)}")

    passed, report = bulk.run_quality_gate(
        conn, "fed_irs_eo_bmf", TABLE, run_id,
        sha256=manifest_sha, row_count=len(df),
        source_url="https://www.irs.gov/pub/irs-soi/eo1.csv (regions 1-4 unioned)")
    print(f"quality gate: passed={passed} {report}")

    cur.execute(f"SELECT COUNT(*), COUNT(DISTINCT EIN), COUNT(DISTINCT STATE) FROM {fq(TABLE)}")
    print("final:", cur.fetchone())
    conn.close()
    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
