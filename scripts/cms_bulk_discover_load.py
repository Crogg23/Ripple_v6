"""Auto-discover and bulk-load CMS datasets from the data.cms.gov catalog.

Parses the CMS DCAT catalog (data.json), finds datasets with direct CSV
download URLs that carry healthcare join keys (NPI/CCN/EIN), skips what's
already loaded, and bulk-loads the rest.

    python scripts/cms_bulk_discover_load.py             # preview (show what WOULD load)
    python scripts/cms_bulk_discover_load.py --run       # actually load them all
    python scripts/cms_bulk_discover_load.py --run --limit 10  # load first 10
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import time
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

CATALOG_URL = "https://data.cms.gov/data.json"
LANDING_SCHEMA = "LIBRARY_RAW.LANDING"
# Keys that indicate a dataset connects to the entity graph
ENTITY_KEYS = {"NPI", "CCN", "EIN", "PROVIDER_NPI", "FAC_CCN", "PRVDR_NPI",
               "RNDRNG_NPI", "PRSCRBR_NPI", "ORGNZTN_NPI", "PROVIDER_CCN",
               "FACILITY_CCN", "ENROLLMENT_ID"}
# Skip datasets we already have or that are too large / known-problematic
SKIP_PATTERNS = {"NPPES", "OPEN_PAYMENTS", "PART_D_PRESCRIB", "MEDICARE_PROVIDER",
                 "FACILITY_AFFILIATION", "PARTD_PRESCRIBER_DRUG", "HCRIS",
                 "TRANSPARENCY_IN_COVERAGE", "MRF", "MACHINE_READABLE"}


def _table_name(title: str) -> str:
    """Convert dataset title to a Snowflake table name."""
    name = re.sub(r'[^a-zA-Z0-9]+', '_', title).strip('_').upper()
    name = re.sub(r'_+', '_', name)
    if len(name) > 60:
        name = name[:60].rstrip('_')
    return f"FED_CMS_{name}"


def _should_skip(title: str, table_name: str, loaded_tables: set) -> str | None:
    """Return skip reason or None if loadable."""
    if table_name in loaded_tables:
        return "already loaded"
    for pat in SKIP_PATTERNS:
        if pat in table_name:
            return f"skip pattern: {pat}"
    return None


def _check_header(url: str) -> list[str] | None:
    """Fetch just the first 4KB to read column headers. Returns column names or None."""
    try:
        resp = requests.get(url, stream=True, timeout=20,
                           headers={"Range": "bytes=0-4096"})
        if resp.status_code not in (200, 206):
            return None
        chunk = resp.content.decode("utf-8", errors="ignore")
        first_line = chunk.split("\n")[0].strip()
        if not first_line or len(first_line) < 5:
            return None
        cols = [c.strip().strip('"').upper() for c in first_line.split(",")]
        return cols
    except Exception:
        return None


def _has_entity_key(cols: list[str]) -> list[str]:
    """Return which entity keys are present in the column list."""
    return [c for c in cols if c in ENTITY_KEYS or any(c.endswith(f"_{k}") for k in ENTITY_KEYS)]


def discover_catalog() -> list[dict]:
    """Parse the CMS DCAT catalog and find loadable datasets with entity keys."""
    print("Fetching CMS catalog (data.cms.gov/data.json)...")
    resp = requests.get(CATALOG_URL, timeout=60)
    resp.raise_for_status()
    catalog = resp.json()
    datasets = catalog.get("dataset", [])
    print(f"  {len(datasets)} datasets in catalog")

    candidates = []
    for ds in datasets:
        title = ds.get("title", "")
        distributions = ds.get("distribution", [])
        # Find the most recent CSV distribution
        csv_dists = [d for d in distributions
                     if d.get("mediaType") == "text/csv" and d.get("downloadURL")]
        if not csv_dists:
            continue
        # Take the most recently modified CSV
        csv_dists.sort(key=lambda d: d.get("modified", ""), reverse=True)
        best = csv_dists[0]
        candidates.append({
            "title": title,
            "url": best["downloadURL"],
            "modified": best.get("modified", ""),
            "description": ds.get("description", "")[:200],
        })

    print(f"  {len(candidates)} datasets have CSV download URLs")
    return candidates


def load_dataset(conn, url: str, table_name: str, max_rows: int = 5_000_000) -> int:
    """Download CSV and load to Snowflake via staging + SWAP."""
    from snowflake.connector.pandas_tools import write_pandas

    print(f"    downloading {url[:80]}...")
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text), dtype=str, nrows=max_rows + 1, low_memory=False)
    if len(df) > max_rows:
        raise RuntimeError(
            f"{table_name}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    # Normalize column names for Snowflake
    df.columns = [re.sub(r'[^A-Z0-9_]', '_', c.upper()).strip('_') for c in df.columns]
    df.columns = [re.sub(r'_+', '_', c) for c in df.columns]

    staging = f"{table_name}__STAGING"
    cur = conn.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {LANDING_SCHEMA}.{staging}")
    write_pandas(conn, df, staging, database="LIBRARY_RAW", schema="LANDING",
                 auto_create_table=True, overwrite=True)
    # Provenance
    cur.execute(f"ALTER TABLE {LANDING_SCHEMA}.{staging} ADD COLUMN IF NOT EXISTS _INGESTED_AT TIMESTAMP_NTZ")
    cur.execute(f"ALTER TABLE {LANDING_SCHEMA}.{staging} ADD COLUMN IF NOT EXISTS _SOURCE_RUN_ID STRING")
    cur.execute(f"UPDATE {LANDING_SCHEMA}.{staging} SET _INGESTED_AT=CURRENT_TIMESTAMP(), _SOURCE_RUN_ID=UUID_STRING()")
    # Swap
    cur.execute(f"CREATE TABLE IF NOT EXISTS {LANDING_SCHEMA}.{table_name} LIKE {LANDING_SCHEMA}.{staging}")
    cur.execute(f"ALTER TABLE {LANDING_SCHEMA}.{staging} SWAP WITH {LANDING_SCHEMA}.{table_name}")
    cur.execute(f"DROP TABLE IF EXISTS {LANDING_SCHEMA}.{staging}")
    return len(df)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--limit", type=int, default=50, help="max datasets to load this run")
    ap.add_argument("--max-rows", type=int, default=5_000_000, help="row cap per dataset")
    args = ap.parse_args()

    # Get what's already loaded
    conn = snow.connect()
    cur = conn.cursor()
    cur.execute("SELECT TABLE_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='LANDING'")
    loaded = {r[0] for r in cur.fetchall()}
    print(f"Already loaded: {len(loaded)} tables")

    # Discover catalog
    candidates = discover_catalog()

    # Check headers for entity keys
    print("Checking headers for entity keys (NPI/CCN/EIN)...")
    loadable = []
    checked = 0
    for cand in candidates:
        table_name = _table_name(cand["title"])
        skip = _should_skip(cand["title"], table_name, loaded)
        if skip:
            continue
        cols = _check_header(cand["url"])
        if not cols:
            continue
        checked += 1
        keys_found = _has_entity_key(cols)
        if keys_found:
            cand["table_name"] = table_name
            cand["cols"] = cols
            cand["entity_keys"] = keys_found
            loadable.append(cand)
            print(f"  [{len(loadable)}] {table_name} — keys: {keys_found}")
        if checked % 20 == 0:
            time.sleep(0.5)  # polite pacing
        if len(loadable) >= args.limit:
            break

    print(f"\n{len(loadable)} datasets ready to load (have entity keys, not yet in warehouse)")

    if not args.run:
        print("\n(preview only — add --run to actually load)")
        for i, d in enumerate(loadable[:20], 1):
            print(f"  {i:2d}. {d['table_name']:50s} keys={d['entity_keys']}")
        return 0

    # Load them
    loaded_count = 0
    total_rows = 0
    failed = 0
    for d in loadable:
        try:
            n = load_dataset(conn, d["url"], d["table_name"], max_rows=args.max_rows)
            if n > 0:
                # Quality gate + INGEST_RUNS row (audit 2026-08-05 finding #3:
                # this loader bypassed the gate)
                passed, report = bulk.run_quality_gate(
                    conn, d["table_name"], d["table_name"], str(uuid.uuid4()),
                    source_url=d["url"])
                if not passed:
                    print(f"    QUALITY GATE FAILED {d['table_name']}: {report}")
                    failed += 1
                    continue
                loaded_count += 1
                total_rows += n
                print(f"    -> {d['table_name']}: {n:,} rows loaded")
        except Exception as e:
            print(f"    FAILED {d['table_name']}: {str(e)[:100]}")
            failed += 1
            continue

    print(f"\nDone: {loaded_count} datasets loaded, {total_rows:,} total rows, {failed} failed")
    conn.close()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
