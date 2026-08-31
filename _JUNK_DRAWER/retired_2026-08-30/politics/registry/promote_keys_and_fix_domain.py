"""Phase 2 Step 2 -- the two authorized precursor fixes.

FIX A (append-only INSERT into FACET_VOCAB): promote the political join keys to
the governed JOIN_KEY vocab as STEEL (clean, unique, government-issued IDs), so
the money-spine joins register against governed keys:
    BIOGUIDE, ICPSR, FEC_CAND_ID, FEC_CMTE_ID

FIX B (the ONE authorized non-additive change -- a single one-row UPDATE):
correct fed_fec_bulk (the FEC committee master) which is registered UNCLASSIFIED.
Sets DOMAIN_PRIMARY='money_in_politics' and, on the SAME row, populates the now-
governed FEC keys it actually carries (FEC_CMTE_ID, FEC_CAND_ID columns verified
present). Touches NO other row.

Usage:
  python politics/registry/promote_keys_and_fix_domain.py            # PREVIEW
  python politics/registry/promote_keys_and_fix_domain.py --apply    # execute
"""
from __future__ import annotations
import sys
from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
import snow  # noqa: E402

VOCAB = '"LIBRARY_META"."REGISTRY"."FACET_VOCAB"'
REG = '"LIBRARY_META"."REGISTRY"."SOURCE_REGISTRY"'

# Fix A: new governed JOIN_KEY values (TIER STEEL). SORT_ORD continues after 21.
NEW_KEYS = [
    ("JOIN_KEY", "BIOGUIDE",    "STEEL", "Bioguide (member PK)",  22),
    ("JOIN_KEY", "ICPSR",       "STEEL", "ICPSR (Voteview key)",  23),
    ("JOIN_KEY", "FEC_CAND_ID", "STEEL", "FEC Candidate ID",      24),
    ("JOIN_KEY", "FEC_CMTE_ID", "STEEL", "FEC Committee ID",      25),
]

INSERT = (
    f"INSERT INTO {VOCAB} (FACET, VALUE, TIER, LABEL, SORT_ORD) "
    f"SELECT %s, %s, %s, %s, %s FROM (SELECT 1) "
    f"WHERE NOT EXISTS (SELECT 1 FROM {VOCAB} WHERE FACET=%s AND VALUE=%s)"
)

# Fix B: the single one-row correction. Append a marker to NOTES so the change is
# self-documenting and trivially reversible.
FIXB = f"""
UPDATE {REG}
SET DOMAIN_PRIMARY = 'money_in_politics',
    JOIN_KEYS_STD = PARSE_JSON('["FEC_CMTE_ID","FEC_CAND_ID"]'),
    JOIN_KEY_TIER = 'STEEL',
    JOIN_KEY_TIER_PROVISIONAL = FALSE,
    NOTES = COALESCE(NOTES,'') || ' [Phase2 FixB 2026-06-29: domain UNCLASSIFIED->money_in_politics; JOIN_KEYS_STD []->[FEC_CMTE_ID,FEC_CAND_ID] (governed). Authorized one-row correction.]'
WHERE SOURCE_ID = 'fed_fec_bulk'
  AND DOMAIN_PRIMARY = 'UNCLASSIFIED'
"""


def main(apply: bool):
    conn = snow.connect()
    cur = conn.cursor()
    print("=" * 70)
    print(f"STEP 2 FIXES -- {'APPLY' if apply else 'PREVIEW'}")
    print("=" * 70)

    # --- Fix A preview ---
    cur.execute(f"SELECT VALUE FROM {VOCAB} WHERE FACET='JOIN_KEY'")
    have = {r[0] for r in cur.fetchall()}
    print("\nFIX A -- FACET_VOCAB JOIN_KEY additions (append-only):")
    for facet, val, tier, label, srt in NEW_KEYS:
        print(f"  {'EXISTS (skip)' if val in have else 'WILL ADD   '}  {val:<12} tier={tier}")

    # --- Fix B preview ---
    cur.execute(f"SELECT SOURCE_ID, DOMAIN_PRIMARY, JOIN_KEYS_STD FROM {REG} WHERE SOURCE_ID='fed_fec_bulk'")
    before = cur.fetchall()
    print("\nFIX B -- one-row correction of fed_fec_bulk (the authorized exception):")
    print(f"  BEFORE: {before}")

    if not apply:
        print("\n(preview only -- re-run with --apply)")
        cur.close(); conn.close(); return

    # --- Fix A apply ---
    added = 0
    for facet, val, tier, label, srt in NEW_KEYS:
        cur.execute(INSERT, (facet, val, tier, label, srt, facet, val))
        added += cur.rowcount or 0
    # --- Fix B apply ---
    cur.execute(FIXB)
    fixb_rows = cur.rowcount or 0
    conn.commit()

    cur.execute(f"SELECT SOURCE_ID, DOMAIN_PRIMARY, JOIN_KEYS_STD, JOIN_KEY_TIER FROM {REG} WHERE SOURCE_ID='fed_fec_bulk'")
    after = cur.fetchall()
    cur.execute(f"SELECT VALUE, TIER FROM {VOCAB} WHERE FACET='JOIN_KEY' AND VALUE IN ('BIOGUIDE','ICPSR','FEC_CAND_ID','FEC_CMTE_ID') ORDER BY VALUE")
    print(f"\nAPPLIED. Fix A rows inserted: {added}. Fix B rows updated: {fixb_rows} (must be 0 or 1).")
    print(f"  vocab now: {cur.fetchall()}")
    print(f"  fed_fec_bulk AFTER: {after}")
    cur.close(); conn.close()


if __name__ == "__main__":
    main(apply="--apply" in sys.argv)
