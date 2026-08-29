# apply-config — the end of "every new key needs a full rebuild" (2026-08-29)

Chris, 2026-08-29: "I should not have to do a 5 hour rebuild every time. This is a living
breathing warehouse. Make this a more efficient system."

## What was actually true (measured this session)

- The last full rebuild (08-28) was **~50 busy-minutes on X-Small** (query history: 310
  write queries, 20:09 → ~22:00 wall). The "4.5h / $10–15" quote was stale since 08-11,
  when a rebuild took 25 minutes. Real cost: ~$2–3.
- The freeze was **not physics**. Entity ids are `hash(key_type | normalized value)`. A new
  key family, a new spec table, or a new extra-key column adds rows; it never re-keys an
  existing entity. Even a changed normalizer for an existing family only moves that family's
  values. The incremental engine's per-table reslice (`reslice_spine`) already retracts
  old values / inserts new ones / re-derives golden + index for touched entities, and
  `validate()` proves it equals the full rebuild. The only thing forcing rebuilds was a
  guard that hashed the WHOLE config and refused on any drift.

## What changed

**Config is pinned per unit, not as one hash.** New control table (one row per unit):
- `norm/<KEY>` — the emitted normalizer SQL for that family (catches implementation edits).
- `spec/<TABLE>` — the spine spec (key, key column, extra keys, survivorship).
- `tck/<TABLE>` — that table's table-scoped graph keys.

**Drift is classified, then applied — bounded:**

| Change | Work |
|---|---|
| new key family | reslice only the spec tables that carry it |
| changed normalizer | reslice every table carrying that family (old values retract, new insert) |
| new / changed spec table (incl. new extra key) | reslice that table |
| removed spec table | retract its slice; shared entities re-derived from remaining members |
| scoped graph key on a non-spine table | discover reslice of that table |

**One command:** `python -m connect apply-config` (`--dry-run` to preview). The heartbeat
(`connect-changed` / `connect-one`) now applies drift automatically instead of refusing.
A full rebuild re-pins everything (`sync_after_rebuild`), so the backstop still works and
remains the equivalence oracle.

**First-run baseline:** the live spine was pinned by a rebuild that ran with the staged
batch flag OFF. `apply-config` detects that the flags-off config reproduces the live
sentinel, pins that as the baseline, then applies the flagged batch as ordinary drift.
Verified offline: flags-off fingerprint `740eaaf6…` == live sentinel `740eaaf6…`.

## The 08-29 batch as a bounded plan (offline preview)

54 config unit changes → **19 spine reslices, 11 graph reslices, 0 retractions**:
- spine: 9 CMS enrollment/affiliation tables, EIA utility + plant masters, eGRID plants,
  FDIC master + branch deposits, FHLB members, NCUA call reports, SAM exclusions,
  USAspending assistance + contracts R2 (the 93M-row one — the slow reslice).
- graph: 8 EIA-860 detail tables, EIA-861 utility data, the 6.3M contracts table, subawards.

Expected cost: minutes on X-Small (each reslice is O(one table)); the contracts R2 reslice
is the long pole. Nothing else in the spine is touched.

## Tests

`tests/test_apply_config.py` — 8 pure tests over the classifier (new family / changed
normalizer / extra key / removed spec / graph-only table / unit coverage).
`tests/test_spine_batch_2026_08_29.py` updated to the flag-on world. Offline suites:
112 passed.

## Not done / caveats

- Not run live: the auto-mode classifier blocks warehouse writes from this session. Chris
  runs `python -m connect apply-config --dry-run` then `python -m connect apply-config`.
- The graph map snapshot (`connect fingerprint` cache) is a separate staleness the 08-18
  report already documented; reslice refreshes the live keyset partitions, not that file.
- `_baseline_units_and_fingerprint` knows only the 08-29 staged batch; a future staged
  batch adds one tuple to its list (or, better, stops using flags — apply-config makes
  them unnecessary).

## Addendum — bug found while proving the plan

The live `--dry-run` previewed `affected=0` on brand-new tables. Cause: the incremental
engine's symmetric difference was `NEW MINUS OLD UNION OLD MINUS NEW` with no
parentheses. Snowflake evaluates MINUS/UNION at equal precedence left-to-right, so it
collapsed to `OLD MINUS NEW`: only removed keys ever reached the membership merge; added
keys were silently skipped in ENTITY_MAP / CONNECT_NODES / MATCH_PAIRS (ENTITY_INDEX and
ENTITY_GOLDEN use NEW ∪ AFFECTED and were correct). Fixed by parenthesizing; pinned by
`test_symmetric_difference_sql_is_parenthesized`. Verified live: FDIC master
54,406 affected; hospital enrollments 5,280 added / 14,683 untouched.

Blast radius: every `connect-one` / `connect-changed` run before 2026-08-29 under-merged
additions. The 08-28 full rebuild reset the live state and no incremental run has happened
since, so the live spine is clean today.
