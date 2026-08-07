#!/usr/bin/env python3
"""Deterministic loader for IRS Political Organization Filing & Disclosure (POFD)
data — Forms 8871 (initial notice) and 8872 (periodic report) for 527 political
organizations. NOT the same as fed_irs_eo_pr (Puerto Rico exempt orgs) -- verified
distinct IRS program.

Source: https://forms.irs.gov/app/pod/dataDownload/dataDownload -- one big
pipe-delimited multi-record-type flat file (H=header, 1=8871 org, D=director/officer,
R=related entity, E=EAIN, 2=8872 report, A=Schedule A contributions, B=Schedule B
expenditures, F=footer). Field layout confirmed from the IRS's own
PolOrgsFileLayout.doc (extracted via raw text scrape -- the .doc is legacy binary,
no docx/antiword available in this env, so this is a best-effort parse of the field
list, not a rendered read of the doc).

SCOPE NOTE: this loader lands record types 1 / D / R / E / 2 (the organization
registry + directors/officers + related entities + EAINs + periodic reports --
~405K rows total). Schedule A (itemized contributions, 9.7M rows) and Schedule B
(itemized expenditures, 8.2M rows) are DEFERRED -- 17.9M additional pipe-delimited
rows is a multi-hour parse+land effort disproportionate to this pass; add a second
loader pass for those if/when a story needs itemized contribution/expenditure data.

    python scripts/irs527_load.py          # preview (parse + sample, no write)
    python scripts/irs527_load.py --run     # land it
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import uuid
import zipfile
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

URL = "https://forms.irs.gov/app/pod/dataDownload/fullData"
ZIP_PATH = _LIB / "raw_downloads" / "irs527_full.zip"
TXT_PATH = _LIB / "raw_downloads" / "irs527" / "var" / "IRS" / "data" / "scripts" / "pofd" / "download" / "FullDataFile.txt"

# record type -> (source_id, table, description, field names in pipe order after the record-type field)
SCHEMAS = {
    "1": ("irs527_8871_orgs", "IRS527_8871_ORGS", "Form 8871 initial/amended/final notice (organization registry)", [
        "FORM_TYPE", "FORM_ID_NUMBER", "INITIAL_REPORT_IND", "AMENDED_REPORT_IND", "FINAL_REPORT_IND",
        "EIN", "ORGANIZATION_NAME", "MAILING_ADDR1", "MAILING_ADDR2", "MAILING_CITY", "MAILING_STATE",
        "MAILING_ZIP", "MAILING_ZIP_EXT", "EMAIL_ADDRESS", "ESTABLISHED_DATE", "CUSTODIAN_NAME",
        "CUSTODIAN_ADDR1", "CUSTODIAN_ADDR2", "CUSTODIAN_CITY", "CUSTODIAN_STATE", "CUSTODIAN_ZIP",
        "CUSTODIAN_ZIP_EXT", "CONTACT_NAME", "CONTACT_ADDR1", "CONTACT_ADDR2", "CONTACT_CITY",
        "CONTACT_STATE", "CONTACT_ZIP", "CONTACT_ZIP_EXT", "BUSINESS_ADDR1", "BUSINESS_ADDR2",
        "BUSINESS_CITY", "BUSINESS_STATE", "BUSINESS_ZIP", "BUSINESS_ZIP_EXT", "EXEMPT_8872_IND",
        "EXEMPT_STATE", "EXEMPT_990_IND", "PURPOSE", "MATERIAL_CHANGE_DATE", "INSERT_DATETIME",
        "RELATED_ENTITY_BYPASS", "EAIN_BYPASS",
    ]),
    "D": ("irs527_directors_officers", "IRS527_DIRECTORS_OFFICERS", "Directors/Officers attached to a Form 8871", [
        "FORM_ID_NUMBER", "DIRECTOR_ID", "ORG_NAME", "EIN", "ENTITY_NAME", "ENTITY_TITLE",
        "ENTITY_ADDR1", "ENTITY_ADDR2", "ENTITY_CITY", "ENTITY_STATE", "ENTITY_ZIP", "ENTITY_ZIP_EXT",
    ]),
    "R": ("irs527_related_entities", "IRS527_RELATED_ENTITIES", "Related entities attached to a Form 8871", [
        "FORM_ID_NUMBER", "ENTITY_ID", "ORG_NAME", "EIN", "ENTITY_NAME", "ENTITY_RELATIONSHIP",
        "ENTITY_ADDR1", "ENTITY_ADDR2", "ENTITY_CITY", "ENTITY_STATE", "ENTITY_ZIP", "ENTITY_ZIP_EXT",
    ]),
    "E": ("irs527_eain", "IRS527_EAIN", "Election Authority ID Numbers attached to a Form 8871", [
        "FORM_ID_NUMBER", "EAIN_ID", "ELECTION_AUTHORITY_ID_NUMBER", "STATE_ISSUED",
    ]),
    "2": ("irs527_8872_reports", "IRS527_8872_REPORTS", "Form 8872 periodic report (organization report registry)", [
        "FORM_TYPE", "FORM_ID_NUMBER", "PERIOD_BEGIN_DATE", "PERIOD_END_DATE", "INITIAL_REPORT_IND",
        "AMENDED_REPORT_IND", "FINAL_REPORT_IND", "CHANGE_OF_ADDRESS_IND", "ORGANIZATION_NAME", "EIN",
        "MAILING_ADDR1", "MAILING_ADDR2", "MAILING_CITY", "MAILING_STATE", "MAILING_ZIP", "MAILING_ZIP_EXT",
        "EMAIL_ADDRESS", "ORG_FORMATION_DATE", "CUSTODIAN_NAME", "CUSTODIAN_ADDR1", "CUSTODIAN_ADDR2",
        "CUSTODIAN_CITY", "CUSTODIAN_STATE", "CUSTODIAN_ZIP", "CUSTODIAN_ZIP_EXT", "CONTACT_NAME",
        "CONTACT_ADDR1", "CONTACT_ADDR2", "CONTACT_CITY", "CONTACT_STATE", "CONTACT_ZIP", "CONTACT_ZIP_EXT",
        "BUSINESS_ADDR1", "BUSINESS_ADDR2", "BUSINESS_CITY", "BUSINESS_STATE", "BUSINESS_ZIP", "BUSINESS_ZIP_EXT",
        "QTR_INDICATOR", "MONTHLY_RPT_MONTH", "PRE_ELECT_TYPE", "PRE_OR_POST_ELECT_DATE",
        "PRE_OR_POST_ELECT_STATE", "SCHED_A_IND", "TOTAL_SCHED_A", "SCHED_B_IND", "TOTAL_SCHED_B",
        "INSERT_DATETIME",
    ]),
}


def _register(conn, sid: str, table: str, desc: str, rows: int) -> None:
    cfg = {
        "source_id": sid,
        "name": f"IRS Political Organization Filing & Disclosure — {desc}",
        "publisher": "Internal Revenue Service",
        "url": "https://www.irs.gov/charities-non-profits/political-organizations/political-organization-filing-and-disclosure",
        "description": f"{desc}. Part of the IRS POFD bulk flat-file export (electronically filed forms only). "
                       "NOT fed_irs_eo_pr (Puerto Rico exempt orgs) -- separate program, verified distinct.",
        "jurisdiction": "federal", "category": "Politics", "subcategory": "527 political organizations",
        "unit_of_observation": f"one row = one {desc.lower()}",
        "geographic_scope": "United States", "access_method": "bulk_download", "format": "pipe-delimited flat file",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "weekly (Sundays 1AM)",
        "volume": f"{rows:,} rows", "license_terms": "Public record (IRS)",
        "join_keys": "FORM_ID_NUMBER, EIN",
        "accountability_relevance": "527 political organization registry, officers, related entities, and reports "
                                    "-- who funds/runs which political fund.",
        "priority_tier": "2", "landing_table": table,
        "notes": "Loaded by scripts/irs527_load.py (LLM-free, split from IRS POFD full pipe-delimited data file, "
                 "snapshot-replace). Schedule A/B (itemized contributions/expenditures, 17.9M rows) deferred -- see script docstring.",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def _parse() -> dict[str, pd.DataFrame]:
    rows_by_type: dict[str, list[list[str]]] = {k: [] for k in SCHEMAS}
    with open(TXT_PATH, encoding="latin-1") as f:
        for line in f:
            line = line.rstrip("\n").rstrip("\r")
            if not line:
                continue
            rt, _, rest = line.partition("|")
            if rt not in SCHEMAS:
                continue
            rows_by_type[rt].append(rest.split("|"))

    dfs = {}
    for rt, (sid, table, desc, cols) in SCHEMAS.items():
        raw_rows = rows_by_type[rt]
        # tolerate ragged rows (pad/truncate) rather than dropping -- a handful of
        # rows have trailing pipes that under/over-count vs. the documented layout
        fixed = [r[:len(cols)] + [""] * (len(cols) - len(r)) for r in raw_rows]
        dfs[rt] = pd.DataFrame(fixed, columns=cols)
    return dfs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for IRS 527 POFD data (record types 1/D/R/E/2)")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== IRS 527 Political Organization Filing & Disclosure (POFD) ===", flush=True)
    TXT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not TXT_PATH.exists():
        ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not ZIP_PATH.exists():
            r = requests.get(URL, timeout=300)
            r.raise_for_status()
            ZIP_PATH.write_bytes(r.content)
        with zipfile.ZipFile(ZIP_PATH) as z:
            z.extractall(TXT_PATH.parents[4])

    dfs = _parse()
    for rt, (sid, table, desc, cols) in SCHEMAS.items():
        print(f"  record type {rt:3} {len(dfs[rt]):>9,} rows  -> {table}  ({desc})", flush=True)

    if not args.run:
        orgs = dfs["1"]
        print("\nSAMPLE (Form 8871 orgs, first 3):")
        for _, row in orgs.head(3).iterrows():
            print(f"  FORM_ID={row['FORM_ID_NUMBER']}  EIN={row['EIN']}  NAME={row['ORGANIZATION_NAME'][:50]}")
        print(f"\ndistinct EIN in 8871 orgs: {orgs['EIN'].nunique():,} of {len(orgs):,} rows")
        print(f"distinct FORM_ID_NUMBER: {orgs['FORM_ID_NUMBER'].nunique():,}")
        print("\nDEFERRED: Schedule A (contributions, 9.7M rows) and Schedule B (expenditures, 8.2M rows) "
              "-- not landed this pass, see script docstring.")
        print("\nPREVIEW only — add --run to land.")
        return 0

    conn = snow.connect()
    gate_failed = []
    try:
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        from snowflake.connector.pandas_tools import write_pandas
        for rt, (sid, table, desc, cols) in SCHEMAS.items():
            df = dfs[rt]
            started = ingest._utcnow()
            run_id = str(uuid.uuid4())
            sha = hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()
            if settings.skip_if_unchanged:
                last_sha = ingest._latest_success_sha(conn, sid)
                if last_sha == sha:
                    print(f"skip {table} (sha unchanged)", flush=True)
                    continue
            out = ingest._stringify(df)
            out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
            out[ingest.META_SOURCE_RUN_ID] = run_id
            out[ingest.META_SRC_SHA256] = sha
            out.columns = [ingest._sf_col(c) for c in out.columns]
            ok, _c, nrows, _ = write_pandas(conn, out, table_name=table,
                                            database=settings.raw_database, schema=settings.raw_schema,
                                            auto_create_table=True, overwrite=True, quote_identifiers=False)
            if not ok:
                raise RuntimeError(f"write_pandas failed for {table}")
            ended = ingest._utcnow()
            dens = ingest.assess_density(df)
            status = "success" if dens.get("populated_fraction", 0) >= 0.01 else "empty"
            if status != "success":
                print(f"  QUALITY GATE FAILED for {table}: {dens}")
                gate_failed.append(table)
            ingest._log_run(conn, sid, run_id, status, len(df), None, sha, URL, started, ended,
                            f"IRS 527 POFD {desc}; {len(df):,} rows; density {dens.get('populated_fraction')}")
            _register(conn, sid, table, desc, len(df))
            print(f"LOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{table} "
                  f"(status={status})", flush=True)
    finally:
        conn.close()
    if gate_failed:
        raise RuntimeError(f"QUALITY GATE FAILED for: {', '.join(gate_failed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
