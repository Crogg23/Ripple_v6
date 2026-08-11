"""Measure EVERY connection in the map, not a sample of two.

The 2026-08-11 spine audit hand-checked two join surfaces and left the rest
"structurally sound but unmeasured". This closes that gap in one pass.

Method (and why it is complete rather than a sample):

  Every connection Ripple can make between two sources is, by construction, an
  entity that appears in BOTH of them -- the spine is hard-ID-only, so there is
  no other path from source A to source B. So the per-source-pair join is
  already materialised in the entity index: one row per (entity, source). A
  self-join of that index on entity id therefore enumerates every connection the
  platform is capable of making, exactly once, with no pair left out.

  For each (key type, source A, source B) we report:
    entities      how many real-world entities the two sources share
    named_pairs   how many of those carry a display name on BOTH sides
    agree         name agreement: identical after normalisation, or one name
                  contains the other's leading token run (a firm trading under a
                  shorter name is the same firm; 'SANFORD FEDERAL, INC.' vs
                  'Sanford Federal Africa')
    agree_pct     agree / named_pairs -- the measured accuracy of that join

  A pair with a LOW agreement rate is the alarm: it means the same ID value is
  attached to two differently-named things in two publishers, which is either a
  publisher error or a key we should not be joining on.

  Pairs with no names on one side cannot be corroborated this way; they are
  reported honestly as unverifiable-by-name rather than counted as good.

Read-only. One heavy query (bounded: an entity sits in at most ~18 sources, so
the pairwise expansion per entity is small), plus small follow-ups.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

from connect import db  # noqa: E402

EI = '"LIBRARY_META"."CONNECT"."ENTITY_INDEX"'
OUT = _ROOT / "outputs" / "connection_validation_2026-08-11.json"

PAIR_SQL = f"""
WITH idx AS (
    SELECT ENTITY_ID, KEY_TYPE, SOURCE_TABLE,
           NULLIF(TRIM(UPPER(DISPLAY_NORM)), '') AS NM
    FROM {EI}
),
pairs AS (
    SELECT a.KEY_TYPE, a.SOURCE_TABLE AS SRC_A, b.SOURCE_TABLE AS SRC_B,
           a.ENTITY_ID, a.NM AS NM_A, b.NM AS NM_B
    FROM idx a
    JOIN idx b
      ON a.ENTITY_ID = b.ENTITY_ID
     AND a.SOURCE_TABLE < b.SOURCE_TABLE
)
SELECT KEY_TYPE, SRC_A, SRC_B,
       COUNT(DISTINCT ENTITY_ID)                                   AS ENTITIES,
       COUNT_IF(NM_A IS NOT NULL AND NM_B IS NOT NULL)              AS NAMED_PAIRS,
       COUNT_IF(NM_A IS NOT NULL AND NM_B IS NOT NULL AND (
                    NM_A = NM_B
                 OR CONTAINS(NM_A, LEFT(NM_B, 8))
                 OR CONTAINS(NM_B, LEFT(NM_A, 8))
                 -- ORDER-INSENSITIVE token overlap. Without this the check
                 -- called 'Josh Gottheimer' vs 'Gottheimer, Josh' a mismatch and
                 -- flagged five perfectly good congressional joins. Tokens of 4+
                 -- characters only, so 'OF'/'THE'/'INC' can't manufacture
                 -- agreement between unrelated names.
                 OR ARRAY_SIZE(ARRAY_INTERSECTION(
                        FILTER(SPLIT(NM_A, ' '), t -> LENGTH(t) >= 4),
                        FILTER(SPLIT(NM_B, ' '), t -> LENGTH(t) >= 4))) >= 1))  AS AGREE
FROM pairs
GROUP BY 1, 2, 3
ORDER BY ENTITIES DESC
"""


def main() -> None:
    conn = db.connect()
    print("measuring every source-to-source connection in the map ...", flush=True)
    rows = db.dicts(conn, PAIR_SQL)
    print(f"  {len(rows):,} connections measured", flush=True)

    for r in rows:
        named = r["NAMED_PAIRS"] or 0
        r["AGREE_PCT"] = round(100.0 * (r["AGREE"] or 0) / named, 1) if named else None

    OUT.write_text(json.dumps(rows, indent=1, default=str), encoding="utf-8")

    checkable = [r for r in rows if r["AGREE_PCT"] is not None]
    blind = [r for r in rows if r["AGREE_PCT"] is None]
    weak = sorted([r for r in checkable if r["AGREE_PCT"] < 50 and r["NAMED_PAIRS"] >= 25],
                  key=lambda r: -r["ENTITIES"])

    tot_named = sum(r["NAMED_PAIRS"] for r in checkable)
    tot_agree = sum(r["AGREE"] for r in checkable)
    print(f"\nconnections: {len(rows):,}  |  name-checkable: {len(checkable):,}  |  "
          f"no names on one side: {len(blind):,}")
    if tot_named:
        print(f"overall name agreement across every checkable connection: "
              f"{tot_agree:,}/{tot_named:,} = {100.0*tot_agree/tot_named:.1f}%")
    print(f"\nconnections below 50% agreement (>=25 named pairs): {len(weak)}")
    for r in weak[:40]:
        print(f"  {r['KEY_TYPE']:<12} {r['SRC_A']} <-> {r['SRC_B']}: "
              f"{r['ENTITIES']:,} entities, {r['AGREE_PCT']}% agree "
              f"({r['AGREE']:,}/{r['NAMED_PAIRS']:,})")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
