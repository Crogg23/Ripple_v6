#!/usr/bin/env python3
"""Deterministic loader for the NAAG / attorneysgeneral.org multistate AG settlements database.

The canonical, fully-searchable listing of multistate settlements concluded by state
Attorneys General from 1980 to the present (issue #69 accountability). NAAG points to the
"State Litigation and AG Activity Database" at attorneysgeneral.org, whose searchable table
is powered by the Ninja Tables WordPress plugin. That plugin exposes a public "get-all-data"
JSON feed (admin-ajax.php, table_id=1166) returning every settlement row as structured JSON --
NOT page chrome. Each row = one multistate settlement with defendants, date resolved, total
settlement amount, lead/participating AGs, industry, enforcement campaign, NAICS codes, etc.

The original landing for this SID was 26 rows of naag.org website menu chrome (a dead scrape).
This loader replaces it with the real machine-readable data feed behind the searchable table.

Snapshot-replace (overwrite=True) -> idempotent; rerun never duplicates.

    python scripts/naag_multistate_settlements_load.py          # preview (fetch + sample, no write)
    python scripts/naag_multistate_settlements_load.py --run     # land it
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest        # noqa: E402
import register      # noqa: E402
import snow          # noqa: E402
from config import settings  # noqa: E402

SID = "fed_naag_multistate_settlements"
TABLE = SID.upper()

# Human-facing page (what we register as URL):
PAGE_URL = ("https://attorneysgeneral.org/settlements-and-enforcement-actions/"
            "searchable-list-of-settlements-1980-present/")
# Machine-readable feed behind the searchable Ninja Tables table (the real data):
DATA_URL = ("https://attorneysgeneral.org/wp-admin/admin-ajax.php"
            "?action=wp_ajax_ninja_tables_public_action"
            "&table_id=1166&target_action=get-all-data&default_sorting=new_first")

# A real browser header set -- the site's ModSecurity returns 406 to bare clients.
_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": PAGE_URL,
}

# Order the columns so the analytically-useful ones come first; the loader keeps ALL fields.
_PREFERRED_ORDER = [
    "case", "year", "dateresolved", "defendants", "additionaldefendants",
    "totalsettlementamount", "totalstateshare", "total_federal_share",
    "leadags", "participatingags", "demleadstates", "gopleadstates",
    "demparticipatingstate", "gopparticipatingstate",
    "industrytype", "issueareageneral", "issueareaspecific",
    "enforcementcampaign", "product_involved", "description",
]


def _fetch() -> list[dict]:
    r = requests.get(DATA_URL, headers=_HEADERS, timeout=120)
    r.raise_for_status()
    payload = r.json()
    if not isinstance(payload, list):
        raise RuntimeError(f"unexpected payload type: {type(payload).__name__}")
    return payload


def _flatten(payload: list[dict]) -> pd.DataFrame:
    """Each item is {'options': {...}, 'value': {<the real settlement fields>}}.

    We keep only the 'value' dict -- that's the actual data row. Column UPPER-cased.
    """
    rows = []
    for item in payload:
        v = item.get("value") or {}
        rows.append({k: ("" if val is None else str(val)) for k, val in v.items()})
    df = pd.DataFrame(rows).fillna("")

    # Stable, useful-first column ordering; preserve every remaining field.
    cols = [c for c in _PREFERRED_ORDER if c in df.columns]
    cols += [c for c in df.columns if c not in cols]
    df = df[cols]
    df.columns = [c.upper() for c in df.columns]
    return df


def _register(conn, rows: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "NAAG Multistate AG Settlements (1980-present)",
        "publisher": "National Association of Attorneys General (NAAG) / State Litigation and AG Activity Database",
        "url": PAGE_URL,
        "description": "Canonical searchable listing of multistate settlements concluded by state "
                       "Attorneys General from 1980 to the present. Each row carries defendants, date "
                       "resolved, total settlement amount, state/federal shares, lead and participating "
                       "AGs (with party breakdown), industry/NAICS, issue area, and enforcement campaign. "
                       "Sourced from the Ninja Tables get-all-data JSON feed behind the searchable table "
                       "(table_id=1166), NOT page chrome.",
        "jurisdiction": "federal", "category": "Accountability", "subcategory": "AG Settlements",
        "unit_of_observation": "one row = one multistate AG settlement",
        "geographic_scope": "United States (all states + DC)", "access_method": "api", "format": "json",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "irregular (as settlements concluded)",
        "volume": f"{rows:,} rows", "license_terms": "NAAG / attorneysgeneral.org public research database",
        "join_keys": "NAICS, state postal codes (participating/lead AGs)",
        "accountability_relevance": "Which AGs sued whom, for how much, over what -- the public record of "
                                    "state-level corporate accountability. Defendants join to corporate "
                                    "registries; NAICS to industry; state codes to FIPS. Issue #69.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/naag_multistate_settlements_load.py. Real data feed: "
                 "admin-ajax.php?action=wp_ajax_ninja_tables_public_action&table_id=1166"
                 "&target_action=get-all-data (Ninja Tables). Site ModSecurity 406s bare clients -- "
                 "loader sends a full browser header set. Replaces a prior dead scrape (26 rows of "
                 "naag.org menu chrome). Amounts stored as raw '$xxx,xxx' TEXT; cast in staging.",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for NAAG multistate AG settlements")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== NAAG Multistate AG Settlements ===", flush=True)
    payload = _fetch()
    df = _flatten(payload)
    print(f"{len(df):,} settlements, {len(df.columns)} cols", flush=True)

    if not args.run:
        print("\nSAMPLE (first 3):")
        for _, row in df.head(3).iterrows():
            amt = row.get("TOTALSETTLEMENTAMOUNT", "")
            print(f"  case {row.get('CASE',''):>5} | {row.get('DATERESOLVED',''):>10} | "
                  f"{amt:>14} | {str(row.get('DEFENDANTS',''))[:60]}")
        dens = ingest.assess_density(df)
        print(f"\ndensity: {dens}")
        # quick distinctness proof that this is real data, not chrome
        for col in ("CASE", "DEFENDANTS", "DATERESOLVED", "TOTALSETTLEMENTAMOUNT"):
            if col in df.columns:
                ne = df[col][df[col].astype(str).str.strip() != ""]
                print(f"  {col:22} present={len(ne):4} distinct={ne.nunique():4}")
        print("\nPREVIEW only — add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    sha = hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()
    conn = snow.connect()
    try:
        from snowflake.connector.pandas_tools import write_pandas
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        out = ingest._stringify(df)
        out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = sha
        out.columns = [ingest._sf_col(c) for c in out.columns]
        ok, _c, nrows, _ = write_pandas(conn, out, table_name=TABLE,
                                        database=settings.raw_database, schema=settings.raw_schema,
                                        auto_create_table=True, overwrite=True, quote_identifiers=False)
        if not ok:
            raise RuntimeError("write_pandas failed")
        ended = ingest._utcnow()
        dens = ingest.assess_density(df)
        status = "success" if dens.get("populated_fraction", 0) >= 0.01 else "empty"
        ingest._log_run(conn, SID, run_id, status, len(df), None, sha, DATA_URL, started, ended,
                        f"NAAG multistate settlements; {len(df):,} rows; "
                        f"density {dens.get('populated_fraction')}")
        _register(conn, len(df))
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{TABLE} "
              f"(status={status}); registered INCLUDE=Y", flush=True)
        # show what landed
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        dd = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT DEFENDANTS) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        print(f"verify: {n:,} rows in landing; {dd:,} distinct defendants", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
