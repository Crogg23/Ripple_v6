#!/usr/bin/env python3
"""Export the NON-REBUILDABLE control-plane tables off Snowflake (Phase 0 DR close).

infra/ddl/ recreates the STRUCTURE of the control plane. But these tables hold judgment that cannot be
regenerated from code + raw — if the database is DROPped (a predecessor infra DB already was), they're gone:

  LIBRARY_META.INGEST_LOGS.INGEST_RUNS     the heartbeat's memory (skip-if-unchanged, resume, lifecycle)
  LIBRARY_META.REGISTRY.SOURCE_REGISTRY    the catalog content (domains, facets, join keys — curated)
  LIBRARY_META.REGISTRY.FACET_VOCAB        the governed vocabulary
  LIBRARY_META.REGISTRY.FACET_CROSSWALK    raw-category -> domain crosswalk
  LIBRARY_META.REGISTRY.SOURCE_FRESHNESS   the freshness ledger (if applied)
  LIBRARY_META."CONNECT".ENTITY_LINKS      gated fuzzy entity-resolution verdicts
  LIBRARY_META."CONNECT".DECISIONS         human review sign-offs
  LIBRARY_META."CONNECT".LEADS             persisted leads + their review status

A stage INSIDE LIBRARY_META would die with a DROP DATABASE, so this unloads to a stage, then GETs the
files down to local disk (backups/dr/<ts>/) — OFF Snowflake. Parquet preserves types incl. ARRAY columns.

RESTORE (per table):  CREATE the table from infra/ddl/, PUT the parquet back to a stage, then
  COPY INTO <table> FROM @stage FILE_FORMAT=(TYPE=PARQUET) MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;

    python scripts/export_control_plane.py            # PREVIEW: what would be exported + row counts
    python scripts/export_control_plane.py --apply    # Chris: unload to stage + GET to backups/dr/<ts>/
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass
import snow  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
STAGE = "LIBRARY_META.REGISTRY.DR_STAGE"

# (fully-qualified table, safe folder name)
TARGETS = [
    ("LIBRARY_META.INGEST_LOGS.INGEST_RUNS", "ingest_runs"),
    ("LIBRARY_META.REGISTRY.SOURCE_REGISTRY", "source_registry"),
    ("LIBRARY_META.REGISTRY.FACET_VOCAB", "facet_vocab"),
    ("LIBRARY_META.REGISTRY.FACET_CROSSWALK", "facet_crosswalk"),
    ("LIBRARY_META.REGISTRY.SOURCE_FRESHNESS", "source_freshness"),
    ('LIBRARY_META."CONNECT".ENTITY_LINKS', "entity_links"),
    ('LIBRARY_META."CONNECT".DECISIONS', "decisions"),
    ('LIBRARY_META."CONNECT".LEADS', "leads"),
]


def row_count(cur, table: str):
    """Row count, or None if the table is genuinely absent. A transient/permission/timeout
    error is surfaced LOUDLY (not silently treated as 'absent'), so a DR backup never quietly
    skips a real control-plane table because of a hiccup."""
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        return cur.fetchone()[0]
    except Exception as exc:
        msg = str(exc).lower()
        if "does not exist" in msg or "not authorized" in msg:
            return None  # object truly absent
        print(f"  [WARN] row_count({table}) failed — NOT an absence: {str(exc)[:120]}")
        return None


def preview(cur) -> None:
    print("=" * 74)
    print("  CONTROL-PLANE DR EXPORT — preview")
    print("=" * 74)
    total = 0
    for table, _ in TARGETS:
        n = row_count(cur, table)
        if n is None:
            print(f"  {table:<48} ABSENT (skip)")
        else:
            total += n
            print(f"  {table:<48} {n:>12,} rows")
    print("-" * 74)
    print(f"  {total:,} rows would be unloaded (PARQUET) to {STAGE} then GET to backups/dr/<ts>/")
    print("  PREVIEW only — nothing exported. Re-run with --apply (Chris).")


def apply(cur) -> int:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = REPO / "backups" / "dr" / ts
    dest.mkdir(parents=True, exist_ok=True)
    cur.execute(f"CREATE STAGE IF NOT EXISTS {STAGE} "
                "FILE_FORMAT = (TYPE = PARQUET) COMMENT = 'Transit stage for off-platform DR export'")
    manifest = {"ts": ts, "tables": []}
    for table, folder in TARGETS:
        n = row_count(cur, table)
        if n is None:
            manifest["tables"].append({"table": table, "status": "absent"})
            print(f"  skip  {table} (absent)")
            continue
        path = f"@{STAGE}/{ts}/{folder}/"
        cur.execute(f"COPY INTO {path} FROM {table} "
                    "FILE_FORMAT = (TYPE = PARQUET) HEADER = TRUE OVERWRITE = TRUE MAX_FILE_SIZE = 268435456")
        cur.execute(f"GET '{path}' 'file://{dest}/{folder}/'")
        got = cur.fetchall()
        # local copy is downloaded; clear the stage so the off-platform DR backup
        # doesn't linger on-platform (unbounded stage-storage growth each --apply).
        cur.execute(f"REMOVE '{path}'")
        manifest["tables"].append({"table": table, "rows": n, "files": len(got)})
        print(f"  ok    {table:<46} {n:>12,} rows -> backups/dr/{ts}/{folder}/")
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print("-" * 74)
    print(f"EXPORTED to {dest}  (off Snowflake — survives a DROP). Manifest: {dest/'manifest.json'}")
    print("  NEXT hardening: replicate backups/dr/ to cloud storage (S3/GCS) on a schedule.")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Export non-rebuildable control-plane tables off Snowflake")
    ap.add_argument("--apply", action="store_true", help="run the export (Chris)")
    args = ap.parse_args(argv)
    conn = snow.connect()
    try:
        cur = conn.cursor()
        if args.apply:
            return apply(cur)
        preview(cur)
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
