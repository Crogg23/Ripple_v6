#!/usr/bin/env python3
"""Deterministic loader for ICIJ Offshore Leaks (nodes + edges).

Public data behind Panama Papers / Paradise Papers / Pandora Papers etc:
offshoreleaks.icij.org, packaged as one zip at
offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip.
Six files land as six RAW tables: entities, officers, addresses,
intermediaries, others (all "nodes") plus relationships (the edges,
node_id_start -> node_id_end). node_id is the join key across all of them.

Snapshot-replace per table (overwrite=True) -> idempotent; rerun never duplicates.

    python scripts/icij_offshoreleaks_load.py          # preview (fetch + sample, no write)
    python scripts/icij_offshoreleaks_load.py --run     # land all six tables
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

URL = "https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip"
ZIP_PATH = _LIB / "icij_extract" / "..-download.zip"
EXTRACT_DIR = _LIB / "icij_extract"

FILES = {
    "fed_icij_offshoreleaks_entities": "nodes-entities.csv",
    "fed_icij_offshoreleaks_officers": "nodes-officers.csv",
    "fed_icij_offshoreleaks_addresses": "nodes-addresses.csv",
    "fed_icij_offshoreleaks_intermediaries": "nodes-intermediaries.csv",
    "fed_icij_offshoreleaks_others": "nodes-others.csv",
    "fed_icij_offshoreleaks_relationships": "relationships.csv",
}

DESCRIPTIONS = {
    "fed_icij_offshoreleaks_entities": "Offshore companies/trusts/funds named in ICIJ's leaks "
        "(Panama Papers, Paradise Papers, Pandora Papers, Offshore Leaks, Bahamas Leaks). name, "
        "jurisdiction, incorporation/struck-off dates, status.",
    "fed_icij_offshoreleaks_officers": "People and companies acting as directors/shareholders/etc. "
        "of the offshore entities above.",
    "fed_icij_offshoreleaks_addresses": "Address nodes tied to entities/officers/intermediaries.",
    "fed_icij_offshoreleaks_intermediaries": "Law firms and corporate-service providers that set up "
        "the offshore entities (e.g. Mossack Fonseca, Appleby).",
    "fed_icij_offshoreleaks_others": "Miscellaneous entity nodes not fitting the other categories.",
    "fed_icij_offshoreleaks_relationships": "The edge list: node_id_start -> node_id_end with a "
        "rel_type (officer_of, registered_agent, similar, etc). This IS the offshore ownership graph.",
}


def _register(conn, sid: str, table: str, rows: int) -> None:
    cfg = {
        "source_id": sid,
        "name": f"ICIJ Offshore Leaks -- {sid.replace('fed_icij_offshoreleaks_', '')}",
        "publisher": "International Consortium of Investigative Journalists (ICIJ)",
        "url": "https://offshoreleaks.icij.org/pages/database",
        "description": DESCRIPTIONS[sid],
        "jurisdiction": "global", "category": "Corporate/Offshore", "subcategory": "Offshore Leaks",
        "unit_of_observation": "one row = one node or one edge in the offshore ownership graph",
        "geographic_scope": "Global", "access_method": "bulk_download", "format": "csv",
        "auth": {"type": "none"}, "cost": "free", "update_cadence": "irregular (leak-driven)",
        "volume": f"{rows:,} rows", "license_terms": "ICIJ Offshore Leaks data use terms (non-commercial "
                                                       "investigative use)",
        "join_keys": "node_id (entities/officers/addresses/intermediaries/others); "
                     "node_id_start/node_id_end (relationships)",
        "accountability_relevance": "Entity spine block (Phase 5): the canonical offshore-ownership "
                                    "graph. Names here are the anchor for beneficial-ownership tracing.",
        "priority_tier": "1", "landing_table": table.upper(),
        "notes": "Loaded by scripts/icij_offshoreleaks_load.py from ICIJ's full-oldb.LATEST.zip "
                 "(nodes + edges, six files, snapshot-replace each).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))


def _fetch_and_extract() -> Path:
    EXTRACT_DIR.mkdir(exist_ok=True)
    already = all((EXTRACT_DIR / f).exists() for f in FILES.values())
    if already:
        print("zip already extracted locally, reusing", flush=True)
        return EXTRACT_DIR
    print(f"downloading {URL} ...", flush=True)
    r = requests.get(URL, timeout=600)
    r.raise_for_status()
    zpath = EXTRACT_DIR.parent / "scratch_icij.zip"
    zpath.write_bytes(r.content)
    print(f"downloaded {len(r.content):,} bytes, extracting...", flush=True)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(EXTRACT_DIR)
    return EXTRACT_DIR


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="LLM-free loader for ICIJ Offshore Leaks")
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args(argv)

    print("=== ICIJ Offshore Leaks ===", flush=True)
    extract_dir = _fetch_and_extract()

    conn = snow.connect() if args.run else None
    gate_failed = []
    try:
        for sid, fname in FILES.items():
            table = sid.upper()
            path = extract_dir / fname
            print(f"\n-- {fname} -> {table} --", flush=True)
            df = pd.read_csv(path, dtype=str, low_memory=False)
            print(f"{len(df):,} rows, {len(df.columns)} cols: {list(df.columns)}", flush=True)
            if not args.run:
                print(df.head(3).to_string())
                dens = ingest.assess_density(df)
                print(f"density: {dens}")
                continue

            started = ingest._utcnow()
            run_id = str(uuid.uuid4())
            sha = hashlib.sha256(pd.util.hash_pandas_object(df).values.tobytes()).hexdigest()
            if settings.skip_if_unchanged:
                last_sha = ingest._latest_success_sha(conn, sid)
                if last_sha == sha:
                    print(f"skip (sha unchanged) -- {sid}", flush=True)
                    continue
            from snowflake.connector.pandas_tools import write_pandas
            snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
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
                            f"ICIJ Offshore Leaks {fname}; {len(df):,} rows; density {dens.get('populated_fraction')}")
            _register(conn, sid, table, len(df))
            n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{table}"')
            d = snow.fetch_scalar(conn, f'SELECT COUNT(DISTINCT NODE_ID) FROM "{settings.raw_database}"."{settings.raw_schema}"."{table}"') \
                if "node_id" in df.columns else None
            print(f"LOADED {n:,} rows -> {table} (status={status})" + (f"; distinct NODE_ID={d:,}" if d is not None else ""), flush=True)
    finally:
        if conn:
            conn.close()

    if not args.run:
        print("\nPREVIEW only -- add --run to land all six tables.")
    elif gate_failed:
        raise RuntimeError(f"QUALITY GATE FAILED for: {', '.join(gate_failed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
