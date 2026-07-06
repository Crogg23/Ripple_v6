#!/usr/bin/env python3
"""Preview (and optionally apply) the spine-taxonomy columns on SOURCE_REGISTRY.

Additive only -- adds three columns, touches nothing else:
    GRAIN          VARCHAR   human-readable "one row = one what" (e.g. "one NPI provider")
    NATURAL_KEY    ARRAY     ordered landing column name(s) that uniquely identify a row
    SPINE_ENTITY   VARCHAR   single value from FACET_VOCAB facet 'SPINE_ENTITY'
                             (see connect/spine_entity.py -- reconciles connect/spine.py's
                             key-driven entity types with the registry's existing
                             ENTITY_TYPES facet, per Chris's 2026-07-05 taxonomy sign-off)

Also seeds FACET_VOCAB with the new 'SPINE_ENTITY' facet (11 values) -- idempotent,
MERGE-based, safe to re-run.

This script ONLY adds columns and vocab rows. It does NOT populate GRAIN/NATURAL_KEY/
SPINE_ENTITY for any source -- that's scripts/profile_spine_backfill.py, run after
this lands.

    python3 scripts/add_spine_columns.py            # preview only
    python3 scripts/add_spine_columns.py --apply    # Chris runs this

NB: the three columns are added to the base table only. To surface them in the
CATALOG view, add them to that view's SELECT (its DDL lives only in Snowflake --
GET_DDL first, per the V_LEADS_PUBLISHED lesson: never redefine a view here on a
guess at its current text).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "connect"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402
from spine_entity import SPINE_ENTITY_VOCAB  # noqa: E402

REGISTRY = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"
FACET_VOCAB = "LIBRARY_META.REGISTRY.FACET_VOCAB"
BACKUP = "LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_SPINECOLS_20260705"

# label + sort order for the new facet's FACET_VOCAB rows.
_LABELS = {
    "person": "Person", "organization": "Organization", "provider": "Provider",
    "facility": "Facility", "vessel": "Vessel", "place": "Place",
    "payment": "Payment", "filing": "Filing", "case": "Case", "asset": "Asset",
    "event": "Event", "aircraft": "Aircraft",
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Add GRAIN/NATURAL_KEY/SPINE_ENTITY to SOURCE_REGISTRY.")
    ap.add_argument("--apply", action="store_true", help="write the columns + vocab (default previews)")
    args = ap.parse_args()

    conn = snow.connect()
    try:
        cur = conn.cursor()
        cur.execute(
            f"SELECT column_name FROM LIBRARY_META.INFORMATION_SCHEMA.COLUMNS "
            f"WHERE table_schema='REGISTRY' AND table_name='SOURCE_REGISTRY' "
            f"AND column_name IN ('GRAIN','NATURAL_KEY','SPINE_ENTITY')"
        )
        existing = {r[0] for r in cur.fetchall()}
        cur.execute(f"SELECT value FROM {FACET_VOCAB} WHERE facet='SPINE_ENTITY'")
        existing_vocab = {r[0] for r in cur.fetchall()}
        cur.close()

        mode = "APPLY" if args.apply else "PREVIEW (reads only)"
        print("=" * 78)
        print(f"Spine taxonomy columns on SOURCE_REGISTRY  --  {mode}")
        print("=" * 78)
        for col in ("GRAIN", "NATURAL_KEY", "SPINE_ENTITY"):
            state = "already present" if col in existing else "would ADD"
            print(f"  {col:<14} {state}")
        missing_vocab = [v for v in SPINE_ENTITY_VOCAB if v not in existing_vocab]
        print(f"\n  FACET_VOCAB facet 'SPINE_ENTITY': {len(existing_vocab)}/{len(SPINE_ENTITY_VOCAB)} "
              f"present, {len(missing_vocab)} to add: {missing_vocab or '(none)'}")

        if not args.apply:
            print("\nPREVIEW only. Re-run with --apply to write "
                  f"(rollback snapshot -> {BACKUP}).")
            return 0

        cur = conn.cursor()
        cur.execute(f"CREATE OR REPLACE TABLE {BACKUP} AS SELECT * FROM {REGISTRY}")
        print(f"\n  rollback snapshot -> {BACKUP}")
        cur.execute(f"ALTER TABLE {REGISTRY} ADD COLUMN IF NOT EXISTS GRAIN VARCHAR")
        cur.execute(f"ALTER TABLE {REGISTRY} ADD COLUMN IF NOT EXISTS NATURAL_KEY ARRAY")
        cur.execute(f"ALTER TABLE {REGISTRY} ADD COLUMN IF NOT EXISTS SPINE_ENTITY VARCHAR")
        print("  added GRAIN, NATURAL_KEY, SPINE_ENTITY (IF NOT EXISTS -- idempotent)")

        n = 0
        for i, val in enumerate(SPINE_ENTITY_VOCAB, start=1):
            cur.execute(
                f"MERGE INTO {FACET_VOCAB} t USING (SELECT 'SPINE_ENTITY' AS facet, "
                "%s AS value, %s AS label, %s AS sort_ord) s "
                "ON t.facet=s.facet AND t.value=s.value "
                "WHEN NOT MATCHED THEN INSERT (facet, value, label, sort_ord) "
                "VALUES (s.facet, s.value, s.label, s.sort_ord)",
                (val, _LABELS.get(val, val.title()), i),
            )
            n += cur.rowcount or 0
        conn.commit()
        cur.close()
        print(f"  seeded {n} new FACET_VOCAB row(s) for facet 'SPINE_ENTITY' "
              f"({len(SPINE_ENTITY_VOCAB)} total in vocab)")
        print("\n  Next: scripts/profile_spine_backfill.py to populate these columns.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
