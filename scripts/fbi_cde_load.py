#!/usr/bin/env python3
"""Deterministic loader for the FBI Crime Data Explorer (CDE) estimates API.

Rebuilds dead fed_fbi_cde from the 2026-08-09 triage (Chris: Option 1). The old
loader hit the API with no key and landed the error/help payload as data. The
real API needs a free api.data.gov key -- BLOCKED until Chris's 2-minute signup
at https://api.data.gov/signup lands the key in library-onboarding/.env as:

    FBI_CDE_API_KEY=...

We pull state x year estimated offense counts (the estimates endpoints -- the
consistent long-run series; incident-level NIBRS bulk is a separate, larger
project if ever needed). ~50 states+DC x offenses, one request per state.

    python scripts/fbi_cde_load.py           # preview: probe 1 state, show sample
    python scripts/fbi_cde_load.py --run     # land all states + gate + register
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
import time
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
for p in (str(_REPO), str(_LIB)):
    if p not in sys.path:
        sys.path.insert(0, p)
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest        # noqa: E402
import register      # noqa: E402
import snow          # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402
from config import settings  # noqa: E402

SID = "fed_fbi_cde"
TABLE = SID.upper()
BASE = "https://api.usa.gov/crime/fbi/cde"
STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO",
    "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA",
    "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
]
FROM_YEAR, TO_YEAR = 1985, 2023


def _key() -> str:
    k = os.getenv("FBI_CDE_API_KEY", "").strip()
    if not k:
        raise SystemExit(
            "FBI_CDE_API_KEY missing from library-onboarding/.env -- Chris's free "
            "signup at https://api.data.gov/signup is the only blocker.")
    return k


def _fetch_state(key: str, state: str, tries: int = 4) -> list[dict]:
    """State estimates: one row per year x offense category."""
    url = f"{BASE}/estimate/state/{state}"
    for i in range(tries):
        try:
            r = requests.get(url, params={
                "from": FROM_YEAR, "to": TO_YEAR, "API_KEY": key}, timeout=120)
            r.raise_for_status()
            j = r.json()
            rows = []
            # response shape: {"results": [{"year":..., offense keys...}, ...]}
            # (older deployments used {"data": [...]}) -- accept either.
            for rec in j.get("results", j.get("data", [])) or []:
                rec = dict(rec)
                rec["STATE"] = state
                rows.append(rec)
            return rows
        except Exception as e:  # noqa: BLE001
            wait = 10 * (i + 1)
            print(f"    {state} retry {i + 1}/{tries} ({str(e)[:80]}); wait {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"CDE fetch failed for {state}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="FBI CDE state estimates loader")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)
    key = _key()

    if not args.run:
        rows = _fetch_state(key, "OH")
        print(f"OH: {len(rows)} rows; sample:")
        for r in rows[:3]:
            print("  ", {k: r[k] for k in list(r)[:8]})
        print("\nPREVIEW only -- add --run to land all states.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    all_rows = []
    for st in STATES:
        rows = _fetch_state(key, st)
        all_rows.extend(rows)
        print(f"    {st}: +{len(rows)} (total {len(all_rows):,})", flush=True)
        time.sleep(1)  # api.data.gov default limit is 1,000/hr -- 51 calls is fine

    df = pd.DataFrame(all_rows)
    conn = snow.connect()
    try:
        out = ingest._stringify(df)
        out.columns = [ingest._sf_col(c) for c in out.columns]
        out = out.loc[:, ~out.columns.duplicated()]
        out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = hashlib.sha256(
            df.to_csv(index=False).encode("utf-8")).hexdigest()
        from snowflake.connector.pandas_tools import write_pandas
        ok, _c, _r, _ = write_pandas(
            conn, out, table_name=TABLE, database=settings.raw_database,
            schema=settings.raw_schema, auto_create_table=True,
            overwrite=True, quote_identifiers=False)
        if not ok:
            raise RuntimeError("write_pandas failed")
        # 51 jurisdictions x ~39 years -- under 1,000 rows total means most states failed
        passed, report = bulk.run_quality_gate(
            conn, SID, TABLE, run_id, row_count=len(out),
            source_url=BASE, expected_min_rows=1_000)
        if not passed:
            print(f"QUALITY GATE FAILED {TABLE}: {report}")
            return 1
        cfg = {
            "source_id": SID,
            "name": "FBI Crime Data Explorer -- State Crime Estimates",
            "publisher": "FBI -- Criminal Justice Information Services",
            "url": "https://cde.ucr.cjis.gov/",
            "description": "Estimated offense counts by state and year (violent/property "
                           "categories) from the FBI Crime Data Explorer estimates API.",
            "jurisdiction": "US", "category": "Crime", "subcategory": "Offense Estimates",
            "unit_of_observation": "one row = one state x year of estimated offense counts",
            "geographic_scope": "United States", "access_method": "api", "format": "json",
            "auth": {"type": "api_key"}, "cost": "free", "update_cadence": "annual",
            "volume": f"{len(out):,} rows", "license_terms": "Public domain (US Gov)",
            "join_keys": "STATE, YEAR",
            "accountability_relevance": "Victim-side crime volume by state/year -- the "
                                        "baseline any local harm or enforcement pattern is read against.",
            "priority_tier": "1", "landing_table": TABLE,
            "notes": "Loaded by scripts/fbi_cde_load.py (2026-08-09 rebuild of the dead "
                     "keyless scrape; needs FBI_CDE_API_KEY).",
        }
        snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))
        print(f"\nLOADED {len(out):,} rows -> LIBRARY_RAW.LANDING.{TABLE}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
