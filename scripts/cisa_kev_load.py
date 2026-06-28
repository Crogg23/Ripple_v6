#!/usr/bin/env python3
"""Deterministic loader for the CISA Known Exploited Vulnerabilities (KEV) Catalog.

The authoritative "vulnerabilities attackers are ACTUALLY exploiting in the wild"
list (issue #35 cybersecurity). One flat public-domain (CC0) JSON file, no key,
refreshed on US weekdays. Each row = one exploited CVE with vendor/product, the
date CISA added it, the federal remediation due date, and a known-ransomware flag.

Snapshot-replace (overwrite=True) -> idempotent; rerun never duplicates.

    python scripts/cisa_kev_load.py          # preview (fetch + sample, no write)
    python scripts/cisa_kev_load.py --run     # land it
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

SID = "fed_cisa_kev"
TABLE = SID.upper()
URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


def _flatten(v: dict) -> dict:
    return {
        "CVE_ID": v.get("cveID", ""),
        "VENDOR_PROJECT": v.get("vendorProject", ""),
        "PRODUCT": v.get("product", ""),
        "VULNERABILITY_NAME": v.get("vulnerabilityName", ""),
        "DATE_ADDED": v.get("dateAdded", ""),
        "SHORT_DESCRIPTION": v.get("shortDescription", ""),
        "REQUIRED_ACTION": v.get("requiredAction", ""),
        "DUE_DATE": v.get("dueDate", ""),
        "KNOWN_RANSOMWARE_CAMPAIGN_USE": v.get("knownRansomwareCampaignUse", ""),
        "NOTES": v.get("notes", ""),
        "CWES": "; ".join(v.get("cwes", []) or []),
    }


def _register(conn, rows: int, catalog_version: str) -> None:
    cfg = {
        "source_id": SID,
        "name": "CISA Known Exploited Vulnerabilities (KEV) Catalog",
        "publisher": "Cybersecurity and Infrastructure Security Agency (CISA)",
        "url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        "description": "Authoritative list of CVEs with reliable evidence of active in-the-wild "
                       "exploitation. Carries a known-ransomware-campaign flag and federal due dates. "
                       f"Catalog version {catalog_version}.",
        "jurisdiction": "federal", "category": "Cybersecurity", "subcategory": "Vulnerabilities",
        "unit_of_observation": "one row = one known-exploited vulnerability (CVE)",
        "geographic_scope": "Global", "access_method": "bulk_download", "format": "json",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "US weekdays",
        "volume": f"{rows:,} rows", "license_terms": "Public domain (CC0) — CISA / U.S. Gov work",
        "join_keys": "CVE, CWE",
        "accountability_relevance": "Critical-infrastructure cyber exposure: which vulnerabilities are "
                                    "actively exploited and ransomware-linked. Issue #35.",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/cisa_kev_load.py (LLM-free, single CC0 JSON, snapshot-replace).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for CISA KEV")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== CISA KEV ===", flush=True)
    r = requests.get(URL, timeout=120)
    r.raise_for_status()
    payload = r.json()
    vulns = payload.get("vulnerabilities", []) or []
    cver = str(payload.get("catalogVersion", ""))
    rows = [_flatten(v) for v in vulns]
    df = pd.DataFrame(rows)
    print(f"catalog {cver}: {len(df):,} vulnerabilities, {len(df.columns)} cols", flush=True)

    if not args.run:
        print("\nSAMPLE (first 3):")
        for _, row in df.head(3).iterrows():
            print(f"  {row['CVE_ID']:18} {row['VENDOR_PROJECT']}/{row['PRODUCT']} "
                  f"(added {row['DATE_ADDED']}, ransomware={row['KNOWN_RANSOMWARE_CAMPAIGN_USE']})")
        dens = ingest.assess_density(df)
        print(f"\ndensity: {dens}")
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
        ingest._log_run(conn, SID, run_id, status, len(df), None, sha, URL, started, ended,
                        f"CISA KEV catalog {cver}; {len(df):,} rows; density {dens.get('populated_fraction')}")
        _register(conn, len(df), cver)
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{TABLE} "
              f"(status={status}); registered INCLUDE=Y", flush=True)
        # show what landed
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}"')
        ransom = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{TABLE}" WHERE KNOWN_RANSOMWARE_CAMPAIGN_USE = \'Known\'')
        print(f"verify: {n:,} rows in landing; {ransom:,} flagged known-ransomware", flush=True)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
