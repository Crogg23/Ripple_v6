# The ICIJ "different vintage" scare — resolved: same snapshot, three blank spellings

**Date:** 2026-08-31. Read-only queries via the Python-scripts door.

## The chain

**What was feared (08-31 drop session):** 8 skipped copies had matching row counts
but different content hashes → "different snapshot vintage", drop refused. Right call
at the time — count-identity is not content-identity.

**What was checked now:**
1. Ingest stamps: canonical `FED_ICIJ_OFFSHORELEAKS_*` loaded 2026-08-05,
   `XC_ICIJ_OFFSHORE_*` loaded 2026-08-07, bare-prefix `ICIJ_OFFSHORE_LEAKS_*`
   loaded manually 2026-08-05 minutes after canonical.
2. Row-level diff on ENTITIES: every "differing" row differed ONLY as
   `''` (canonical) vs `NULL` (XC) or `'NA'` (bare-prefix). No data difference.
3. Blank-normalized `HASH_AGG` (trim, `''`→NULL, `'NA'`→NULL, `'None'`→NULL,
   `'N/A'`→NULL, case-sensitive so `'n/a'` needed its own look) across every
   surviving pair:

| canonical | copy | verdict |
|---|---|---|
| RELATIONSHIPS | XC | identical |
| ENTITIES | XC | identical |
| OFFICERS | XC | identical |
| ADDRESSES | XC | identical |
| INTERMEDIARIES | XC | identical |
| OFFICERS | bare-prefix | identical after full normalize |
| ADDRESSES | bare-prefix | identical after full normalize |
| ENTITIES | bare-prefix | 5 rows differ, all `NULL` vs `'n/a'` in IBCRUC |

**What a hit means:** all three families are the SAME publisher snapshot,
loaded by three loaders with three blank-handling conventions.
The "vintage" difference never existed.

**What a miss would have meant:** real value differences (names, statuses,
dates) between copies — none were found anywhere.

## Verdict

All 8 surviving copies are content-duplicates of canonical. Safe to drop
once Chris greenlights destroy. Canonical keeps `''` blanks (LEIE-style trap —
blank-aware counting still applies to canonical itself).

## Receipts

- `reports/row1/icij_vintage_compare_2026-08-31.json` — stamps, counts, ranges
- `reports/row1/icij_blank_normalized_hash_2026-08-31.json` — XC-family hashes
- `reports/row1/icij_blank_normalized_hash_bareprefix_2026-08-31.json` — bare-prefix hashes
- `scripts/icij_vintage_compare_2026_08_31.py` — rerunnable
