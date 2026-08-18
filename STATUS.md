# RIPPLE STATUS — 2026-08-18 — Rebuild done, map repaired, all connection checks green

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: one standing item only.** The roll-call vote mart still disagrees with
its Python-built twin (113,512 vs 3,364 rows). Not new, not touched today.
Full suite: 3,096 passed, 2 skipped, that one failure.

---

## THE HEADLINE: the rebuild ran, and then took all afternoon to actually work

The full spine rebuild went at 08:48 and finished clean at 10:57 — 33,283,474
entities (16,859,563 in 2+ sources) over 173 sources. But the step right after
it, the one that redraws the connection map, crashed. Repairing that exposed
two more problems underneath, one of them older than today.

**Three real causes, all fixed:**

1. **Stale schema snapshot.** The map reads a cached picture of the warehouse's
   shape, last taken 8/9. An EPA superfund table had been reloaded with its
   columns renamed since, so the map asked for a column that no longer exists
   and died. Re-profiled the 5 tables whose columns had moved, dropped 2 that
   no longer exist.

2. **The five new ID types were never taught to the column recognizer.** The
   spine is told explicitly which table and column to use, so it resolved them
   fine. The map has to recognize ID columns by name — and had no rules for
   these. So the whole 2026-08 batch produced ZERO connections while sitting
   perfectly in the spine. Refreshing the snapshot alone would have fixed
   nothing.

   Checked every candidate column name against all 2,212 tables before writing
   a rule: each occurs only inside its own family. Bare "ID" (the judge and
   court registry columns) exists on 180 tables and got a table-specific
   override instead of a name rule.

3. **A tier bug older than today.** Hard ID numbers are trusted and skip the
   "could this be coincidence?" filter; names and zips are not. The code
   deciding which bucket a key falls in only looked in one of the three places
   a key can be registered. So the UK company-number link — 2,335,951 matched
   companies — has been labelled a guess in every map since 8/5, and the
   court-ID family scored zero today because the coincidence filter ate six
   real, dense overlaps.

**Also mine, not the code:** the re-seed command silently skips the copy that
matters unless you pass an explicit overwrite flag. This morning's rebuild
script and my first two re-seeds all ran the default, which is why one check
stayed red and its number kept moving without converging. Correct order is
profile → redraw map → seed with overwrite → validate.

## WHERE THINGS STAND

- **All 6 connection checks pass.** Green for the first time today.
- **Map: 4,762 verified connections**, 8,902 coincidences rejected, from
  2,705,233 pairs tested. By trust level: 2,670 name-pinned-to-place, 1,249
  hard-ID, 485 via crosswalk, 353 geographic, 5 other.
- **The guess tier went 81 → 0.** All 81 were hard-ID matches wearing the wrong
  label. Hard-ID went 1,160 → 1,249.
- **All five new families are on the map:** water permits 45 links, judges 28,
  courts 6, credit unions 6, detention 3. Courts' 6 is every possible pair of
  its 4 tables — that family is fully wired.

## WHAT THE REBUILD ACTUALLY BOUGHT (still unopened)

Nobody has asked this data a question yet. Sitting there, resolved and wired:

- **Judges — 16,232, at a 96.6% multi-source rate.** For a typical federal
  judge: who they are, every position held, schooling, political affiliation,
  race, financial disclosures, and their dockets, all keyed together.
- **Water permits — 1,213,740 permitted facilities**, with the full chain from
  permit → quarterly non-compliance → inspection → violation → enforcement.
- **Credit unions — 99.9% multi-source**, including a 53-row charter merger
  ledger (how you trace a credit union that got absorbed).
- **Detention — 1,490 facility codes, 707 with actual stints.**
- Plus charity golden names (1.98M), 527 dark money, failed pensions, and the
  first DUNS entities (which carry old and new federal contractor IDs on the
  same row — a free crosswalk).

## Live/open items

- **Nobody has read the map.** 4,762 connections, unexamined. Cheapest next
  move by a distance.
- Roll-call mart rebuild via Python builder (standing).
- Two FDA medical-device tables reloaded as raw JSON — data complete inside
  (7,085 and 39,635 records, matching source totals) but unflattened, so the
  map can't see them.
- The ~900 gated portal tables include the four offshore-leaks files (3.34M
  relationships, 814k entities, 771k officers), the 527 orgs and a UK sanctions
  list. Gated because they key on names, not ID numbers. Whether to build a
  name-based path for those is a real question, not a bug.
- DEA numbers: 149,244 entities, zero cross-source merges. Single-source, inert
  until a second DEA-carrying source lands.
- Data-trap repairs ranked by the census fill (FAERS 76% dup, contracts epoch
  dates, NEISS future dates, SEC year-zero, 2 broken staging views).
- FEC-IDs flatten build (small; flips money→votes to hard-ID).
- Source-registry reconciliation (onboarding-log leg still open).
- CourtListener citation-network load retry (standing).
- Six polygon tables have unparseable geometry; some EPA/NTSB coordinates are
  invalid (longitude 435.8). Pre-existing.

**YOUR MOVE:** nothing is blocked. The open question is what to point at first —
reading the map, or one of the repairs above.

**NEXT SESSION:**
1. Boot trust check vs this file and git log.
2. Read the map: what got newly connected, what's newly askable.
3. Otherwise: FEC-IDs flatten build or the top data-trap repairs.

**COST:** 2026-08-18 total 11.22 credits ≈ $22–33. Roughly $9–13 of that was
the morning rebuild Chris approved; the rest was the afternoon repair — three
map redraws, a profiling pass, two re-seeds and several suite runs. That is
more than the $5–8 quoted for the afternoon work, because the tier bug forced
two extra map redraws that were not in the estimate.
