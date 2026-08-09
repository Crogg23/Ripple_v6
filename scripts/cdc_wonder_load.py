#!/usr/bin/env python3
"""Deterministic (LLM-free) loader for CDC WONDER Detailed Mortality (D76).

Rebuilds dead fed_cdc_wonder from the 2026-08-09 triage (Chris: Option 1). The old
loader scraped the API *help page* as data (1 HTML row). The real API takes an XML
request POSTed to https://wonder.cdc.gov/controller/datarequest/D76 with
accept_datause_restrictions=true, and returns an XML data table.

D76 = Underlying Cause of Death, 1999-2020 (final, stable). CDC policy limits the
web service to NATIONAL data only (any state/county/region group-by or filter is
rejected — verified live 2026-08-09), so this lands the national YEAR x ICD-10
CHAPTER x SEX grid (~840 rows) in one request. State-level geography comes from
the companion Socrata source fed_cdc_leading_causes_state instead
(sprint_rebuild_20260809_specs.py).

    python scripts/cdc_wonder_load.py                 # preview: fetch + show sample
    python scripts/cdc_wonder_load.py --run           # land + gate + register
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import time
import uuid
import xml.etree.ElementTree as ET
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

SID = "fed_cdc_wonder"
TABLE = SID.upper()
API = "https://wonder.cdc.gov/controller/datarequest/D76"
YEARS = list(range(1999, 2021))
# NO browser User-Agent: CDC's edge 403-blocks fake-browser UAs from non-browser
# clients but accepts python-requests' honest default (verified live 2026-08-09).
UA: dict[str, str] = {}


def _param(name: str, *values: str) -> str:
    vals = "".join(f"<value>{v}</value>" for v in values)
    return f"<parameter><name>{name}</name>{vals}</parameter>"


def _request_xml(year: int) -> str:
    """State x ICD-chapter grid for one year. Parameter names follow the public
    D76 form field names (B_=group-by, M_=measures, F_/I_=finder selections,
    V_=variable filters, O_=options) — the same set the WONDER web form posts."""
    p = [
        _param("B_1", "D76.V1-level1"),   # group by year
        _param("B_2", "D76.V2-level1"),   # group by ICD-10 chapter
        _param("B_3", "D76.V7"),          # group by sex
        _param("B_4", "*None*"),
        _param("B_5", "*None*"),
        # (year param is unused now — the whole 1999-2020 grid comes in one request)
        _param("M_1", "D76.M1"),          # deaths
        _param("M_2", "D76.M2"),          # population
        _param("M_3", "D76.M3"),          # crude rate
        _param("F_D76.V1", "*All*"),      # all years — year is a group-by axis now
        _param("F_D76.V2", "*All*"),      # cause finder
        _param("F_D76.V9", "*All*"),      # state finder
        _param("F_D76.V10", "*All*"),
        _param("F_D76.V27", "*All*"),
        _param("I_D76.V1", "*All* (All Dates)"),
        _param("I_D76.V2", "*All* (All Causes of Death)"),
        _param("I_D76.V9", "*All* (The United States)"),
        _param("I_D76.V10", "*All* (The United States)"),
        _param("I_D76.V27", "*All* (The United States)"),
        _param("V_D76.V1", ""),           # year filtering happens via the finder above
        _param("V_D76.V2", ""),
        _param("V_D76.V4", "*All*"),      # month
        _param("V_D76.V5", "*All*"),      # age
        _param("V_D76.V6", "00"),         # infant age groups: all
        _param("V_D76.V7", "*All*"),      # gender
        _param("V_D76.V8", "*All*"),      # race
        _param("V_D76.V9", ""),
        _param("V_D76.V10", ""),
        _param("V_D76.V11", "*All*"),     # 2013 urbanization
        _param("V_D76.V12", "*All*"),     # ICD-10 130 infant causes
        _param("V_D76.V17", "*All*"),     # hispanic origin
        _param("V_D76.V19", "*All*"),     # weekday
        _param("V_D76.V20", "*All*"),     # autopsy
        _param("V_D76.V21", "*All*"),     # place of death
        _param("V_D76.V22", "*All*"),     # injury intent
        _param("V_D76.V23", "*All*"),     # injury mechanism
        _param("V_D76.V24", "*All*"),     # weekday/month sub
        _param("V_D76.V25", "*All*"),     # drug/alcohol
        _param("V_D76.V27", ""),
        _param("O_V1_fmode", "freg"), _param("O_V2_fmode", "freg"),
        _param("O_V9_fmode", "freg"), _param("O_V10_fmode", "freg"),
        _param("O_V27_fmode", "freg"),
        _param("O_aar", "aar_none"),      # no age-adjusted rates (keeps it simple)
        _param("O_aar_pop", "0000"),      # std population for AAR (required even when off)
        _param("O_age", "D76.V5"),
        _param("O_javascript", "on"),
        _param("O_location", "D76.V9"),
        _param("O_precision", "1"),
        _param("O_rate_per", "100000"),
        _param("O_show_totals", "false"),
        _param("O_show_zeros", "true"),
        _param("O_show_suppressed", "true"),
        _param("O_timeout", "300"),
        _param("O_title", f"Ripple state x chapter {year}"),
        _param("O_ucd", "D76.V2"),        # cause axis: ICD chapter
        _param("O_urban", "D76.V11"),
        _param("action-Send", "Send"),
        _param("finder-stage-D76.V1", "codeset"),
        _param("finder-stage-D76.V2", "codeset"),
        _param("finder-stage-D76.V9", "codeset"),
        _param("finder-stage-D76.V10", "codeset"),
        _param("finder-stage-D76.V27", "codeset"),
        _param("stage", "request"),
    ]
    return f"<request-parameters>{''.join(p)}</request-parameters>"


def _fetch_all(tries: int = 4) -> str:
    """One request returns the whole 1999-2020 year x chapter x sex grid."""
    for i in range(tries):
        try:
            r = requests.post(API, data={
                "request_xml": _request_xml(0),
                "accept_datause_restrictions": "true"}, headers=UA, timeout=300)
            r.raise_for_status()
            if "<data-table" not in r.text:
                raise RuntimeError(f"no data-table in response: {r.text[:300]}")
            return r.text
        except Exception as e:  # noqa: BLE001
            wait = 15 * (i + 1)
            print(f"    retry {i + 1}/{tries} ({str(e)[:80]}); wait {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError("WONDER fetch failed")


def _parse(xml_text: str) -> list[dict]:
    """WONDER's data-table rows use rowspan-style carry-down for group columns."""
    root = ET.fromstring(xml_text)
    table = root.find(".//data-table")
    rows, carry = [], {}
    for r in table.findall("r"):
        cells = r.findall("c")
        # label cells carry 'l' (label) or 'v'; measure cells carry 'v' (value)
        labels = [c for c in cells if c.get("l") is not None]
        values = [c.get("v") for c in cells if c.get("l") is None]
        if labels:
            # first label cell(s) update the carry-down keys in order
            keys = ["YEAR", "ICD_CHAPTER", "SEX"]
            # leading group columns carry down (rowspan): a row may omit YEAR
            # and/or ICD_CHAPTER and deliver only the trailing label(s)
            offset = len(keys) - len(labels)
            for j, c in enumerate(labels):
                carry[keys[offset + j]] = c.get("l")
        m = dict(carry)
        for name, v in zip(["DEATHS", "POPULATION", "CRUDE_RATE"], values):
            m[name] = v
        rows.append(m)
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="CDC WONDER D76 state x chapter loader")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    all_rows = _parse(_fetch_all())
    print(f"fetched {len(all_rows):,} rows (year x chapter x sex, 1999-2020)")
    if not args.run:
        for r in all_rows[:5]:
            print("  ", r)
        print("\nPREVIEW only — add --run to land.")
        return 0

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    df = pd.DataFrame(all_rows)
    conn = snow.connect()
    try:
        out = ingest._stringify(df)
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
        # 22 years x ~19 chapters x 2 sexes ≈ 840; well below that = something broke
        passed, report = bulk.run_quality_gate(
            conn, SID, TABLE, run_id, row_count=len(out),
            source_url=API, expected_min_rows=500)
        if not passed:
            print(f"QUALITY GATE FAILED {TABLE}: {report}")
            return 1
        cfg = {
            "source_id": SID,
            "name": "CDC WONDER — Underlying Cause of Death (state x ICD chapter, 1999-2020)",
            "publisher": "CDC — National Center for Health Statistics",
            "url": "https://wonder.cdc.gov/ucd-icd10.html",
            "description": "Deaths, population and crude rate by state, year and ICD-10 "
                           "chapter from CDC WONDER D76 (final multiple-cause files).",
            "jurisdiction": "US", "category": "Health", "subcategory": "Mortality",
            "unit_of_observation": "one row = one state x year x ICD-10 chapter",
            "geographic_scope": "United States", "access_method": "api", "format": "xml",
            "auth": {"type": "none"}, "cost": "free", "update_cadence": "static (1999-2020 final)",
            "volume": f"{len(out):,} rows", "license_terms": "Public domain (US Gov); WONDER data-use restrictions accepted",
            "join_keys": "STATE, YEAR",
            "accountability_relevance": "The canonical who-dies-of-what-where grid — baseline "
                                        "mortality any harm pattern gets checked against.",
            "priority_tier": "1", "landing_table": TABLE,
            "notes": "Loaded by scripts/cdc_wonder_load.py (XML API, one request/year; "
                     "2026-08-09 rebuild of the dead help-page scrape). County detail is "
                     "API-suppressed by CDC policy; state is the floor.",
        }
        snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))
        print(f"\nLOADED {len(out):,} rows -> LIBRARY_RAW.LANDING.{TABLE}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
