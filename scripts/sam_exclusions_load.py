#!/usr/bin/env python3
"""Deterministic loader for the SAM.gov Exclusions list (the federal "banned from
doing business" list — the bad-list side of the money + health detectors).

SAM's Entity Management API (api.sam.gov) returns exclusions as nested JSON,
paginated. Each record carries UEI, CAGE, AND NPI in exclusionIdentification, so
a debarred party hard-joins to USASpending (UEI -> 'debarred-but-funded') and to
NPPES/LEIE (NPI -> health). We paginate at a large page size (well under the
1,000 req/day key limit), flatten the key fields, and land a flat TEXT mirror
through the shared ingest pipeline. Needs SAM_API_KEY in library-onboarding/.env.

Run detached (the API is slow per call):
    python scripts/sam_exclusions_load.py --run
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

SID = "fed_sam_exclusions"
TABLE = SID.upper()
API = "https://api.sam.gov/entity-information/v4/exclusions"
PAGE_SIZE = 1000


def _g(d, *path):
    """Safe nested get -> '' if any hop missing."""
    cur = d
    for p in path:
        if isinstance(cur, list):
            cur = cur[0] if cur else {}
        if not isinstance(cur, dict):
            return ""
        cur = cur.get(p)
        if cur is None:
            return ""
    if isinstance(cur, (dict, list)):
        return ""
    return cur


def _flatten(e: dict) -> dict:
    idn, det = e.get("exclusionIdentification", {}) or {}, e.get("exclusionDetails", {}) or {}
    return {
        "UEI": _g(idn, "ueiSAM"),
        "CAGE": _g(idn, "cageCode"),
        "NPI": _g(idn, "npi"),
        "ENTITY_NAME": _g(idn, "entityName"),
        "FIRST_NAME": _g(idn, "firstName"),
        "MIDDLE_NAME": _g(idn, "middleName"),
        "LAST_NAME": _g(idn, "lastName"),
        "PREFIX": _g(idn, "prefix"),
        "SUFFIX": _g(idn, "suffix"),
        "DNB_OPEN_DATA": _g(idn, "dnbOpenData"),
        "CLASSIFICATION": _g(det, "classificationType"),
        "EXCLUSION_TYPE": _g(det, "exclusionType"),
        "EXCLUSION_PROGRAM": _g(det, "exclusionProgram"),
        "EXCLUDING_AGENCY": _g(det, "excludingAgencyName"),
        "ACTIVATION_DATE": _g(e, "exclusionActions", "activationDate"),
        "TERMINATION_DATE": _g(e, "exclusionActions", "terminationDate"),
        "RECORD_STATUS": _g(e, "exclusionActions", "recordStatus"),
        "CITY": _g(e, "exclusionPrimaryAddress", "city"),
        "STATE": _g(e, "exclusionPrimaryAddress", "stateOrProvinceCode"),
        "ZIP": _g(e, "exclusionPrimaryAddress", "zipCode"),
        "COUNTRY": _g(e, "exclusionPrimaryAddress", "countryCode"),
    }


def _fetch_page(key: str, page: int):
    """One page, up to 6 tries with exponential backoff. Returns json or None (give up)."""
    for attempt in range(6):
        try:
            r = requests.get(API, params={"api_key": key, "page": page, "size": PAGE_SIZE}, timeout=120)
            r.raise_for_status()
            return r.json()
        except Exception as ex:  # noqa: BLE001
            wait = min(60, 5 * (2 ** attempt))
            print(f"    page {page} retry {attempt + 1}/6 ({str(ex)[:60]}); wait {wait}s", flush=True)
            time.sleep(wait)
    return None


def _land(conn, rows: list[dict], overwrite: bool, run_id: str, started) -> None:
    from snowflake.connector.pandas_tools import write_pandas
    df = pd.DataFrame(rows)
    out = ingest._stringify(df)
    out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
    out[ingest.META_SOURCE_RUN_ID] = run_id
    out[ingest.META_SRC_SHA256] = hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()
    ok, _c, _r, _ = write_pandas(conn, out, table_name=TABLE, database=settings.raw_database,
                                 schema=settings.raw_schema, auto_create_table=True,
                                 overwrite=overwrite, quote_identifiers=False)
    if not ok:
        raise RuntimeError("write_pandas failed")


def _register(conn, rows: int) -> None:
    cfg = {
        "source_id": SID,
        "name": "SAM.gov Exclusions (Federal Debarment List)",
        "publisher": "U.S. GSA — System for Award Management",
        "url": "https://sam.gov/content/exclusions",
        "description": "Parties excluded/debarred from federal contracts & assistance. Carries "
                       "UEI, CAGE and NPI per record (bridges to USASpending and to NPPES/LEIE).",
        "jurisdiction": "US", "category": "Sanctions", "subcategory": "Federal Debarment",
        "unit_of_observation": "one row = one exclusion record (party x program)",
        "geographic_scope": "United States", "access_method": "api", "format": "json",
        "auth": {"type": "api_key"}, "cost": "free", "update_cadence": "daily",
        "volume": f"{rows:,} rows", "license_terms": "US Gov; contains D&B Open Data (attribute D&B, no bulk resale)",
        "join_keys": "UEI, CAGE, NPI",
        "accountability_relevance": "The federal banned list. UEI -> debarred-but-funded (USASpending); "
                                    "NPI -> excluded provider cross-checks (health).",
        "priority_tier": "1", "landing_table": TABLE,
        "notes": "Loaded by scripts/sam_exclusions_load.py (LLM-free, SAM Entity API paginated + flattened).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for SAM exclusions")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--flush-pages", type=int, default=10, help="land every N pages (durable progress)")
    args = ap.parse_args(argv)

    key = os.getenv("SAM_API_KEY", "").strip()
    if not key:
        raise SystemExit("SAM_API_KEY missing from library-onboarding/.env")

    print("=== SAM exclusions (incremental, fault-tolerant) ===")
    if not args.run:
        j = _fetch_page(key, 0)
        ents = (j or {}).get("excludedEntity", []) or []
        print(f"page 0: {len(ents)} records of {(j or {}).get('totalRecords')}; sample:")
        for e in ents[:3]:
            f = _flatten(e)
            print(f"  [{f['CLASSIFICATION']}] {f['ENTITY_NAME'] or f['LAST_NAME']}  UEI={f['UEI']} NPI={f['NPI']}")
        print("\nPREVIEW only — add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    conn = snow.connect()
    snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
    buf, total, skipped, page, tot, first, consec = [], 0, [], 0, None, True, 0
    try:
        while True:
            j = _fetch_page(key, page)
            if j is None:                       # gave up on this page after retries
                skipped.append(page)
                consec += 1
                if consec >= 5:                 # sustained throttle/quota — stop, keep what we have
                    print(f"    {consec} consecutive failures — SAM throttled; landing what we have", flush=True)
                    break
                page += 1
                if tot and page * PAGE_SIZE >= tot:
                    break
                continue
            consec = 0
            if tot is None:
                tot = j.get("totalRecords")
                print(f"    total exclusions: {tot:,}", flush=True)
            ents = j.get("excludedEntity", []) or []
            if not ents:
                break
            buf.extend(_flatten(e) for e in ents)
            print(f"    page {page}: +{len(ents)} (buffered {len(buf):,}, landed {total:,}/{tot})", flush=True)
            page += 1
            if len(buf) >= args.flush_pages * PAGE_SIZE:
                _land(conn, buf, overwrite=first, run_id=run_id, started=started)
                total += len(buf); first = False; buf = []
                print(f"    -> flushed (landed {total:,})", flush=True)
            if tot and page * PAGE_SIZE >= tot:
                break
            time.sleep(3)                        # gentle pace — stay under SAM's throttle
        if buf:
            _land(conn, buf, overwrite=first, run_id=run_id, started=started)
            total += len(buf)
        ended = ingest._utcnow()
        ingest._log_run(conn, SID, run_id, "success", total, None, "",
                        API, started, ended,
                        f"SAM exclusions. {total:,} rows landed"
                        + (f"; {len(skipped)} pages skipped ({skipped[:10]})" if skipped else "."))
        _register(conn, total)
        print(f"\nLOADED {total:,} rows -> LIBRARY_RAW.LANDING.{TABLE}; "
              f"{len(skipped)} pages skipped; registered INCLUDE=Y")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
