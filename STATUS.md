# RIPPLE STATUS — 2026-08-18 (evening) — Second rebuild done: sniffer batch live, map at 4,899, all checks green

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: one standing item only.** The roll-call vote mart still disagrees with
its Python-built twin. Not new, not touched today. Suite after all of today's
wiring: 3,096 passed, 2 skipped, that one failure (deselected on the final run;
final-run result pending at close — see Tests line).

---

## THE DAY IN ONE LINE

Two rebuilds, both clean: the morning one lit the 2026-08 staged batch (courts,
water, credit unions, ICE); the evening one lit the **value-shape sniffer
batch** — 18 columns that hold real IDs under names no detector could read,
found by scanning all 11,547 non-portal landing columns by VALUE and proving
each by live overlap.

## THE EVENING REBUILD (Chris approved ~$12–20; ran clean)

- **Spine: 33,312,349 entities over 178 sources** (morning: 33,283,474 / 173).
  +28,875 entities, +34,108 newly multi-source.
- **Map: 4,899 connections** (morning: 4,762). Hard-ID 1,249 → 1,375 (+126),
  crosswalk bridges 485 → 496.
- **What's newly wired:** the four multi-cycle FEC history tables (positional
  C1/C4/C10/C15 headers — the BIGGER copies of the wired single-cycle twins,
  dark since landing), candidate↔own-committee crosswalk at hard-ID,
  leadership-PAC→candidate, independent-expenditure spender committees, EPA
  enforcement-case→facility-registry (105k, 100%), ECHO→drinking-water
  (99.3% of the live water-system world), Medicare facility parent/chain
  columns (graph-only, per the no-mislabeling rule).
- **Bonus audit while it cooked:** four OLDER spine columns were map-blind for
  weeks — the 168k-row federal contractor EXCLUSION list's entity ID, SEC
  insider filers (1.9M rows, 100% ID), leadership-PAC's own committee ID, the
  credit-union merger ledger. Wired, and a new test now FAILS the build if any
  spec column is ever map-invisible again.
- **Pipeline done in the proven order:** rebuild → re-profile the 15 touched
  tables → map redraw → re-seed WITH the overwrite flag → **all 6 validation
  checks PASS.** Incremental is unfrozen and pinned (2,109 watermarks).
- Deliberately excluded: legislators' FEC-IDs JSON list (flatten build is the
  fix — wiring it raw would mint concatenated-ID phantom entities).

Receipts: `reports/value_shape_findings_2026-08-18.md` (findings + outcome
addendum, per-candidate JSON alongside).

## Live/open items

- **Nobody has read the map.** Now 4,899 connections, unexamined — including
  the brand-new multi-cycle money→politics wiring. Cheapest next move.
- FEC-IDs flatten build (small; the sniffer proved the values are live).
- FEC positional-header tables: load-layer header repair parked as the cleaner
  long-term fix (needs table-alter rights).
- 182 columns still hold literal 'nan' text (inventory in reports/) — joins
  the standing data-trap repair list (FAERS 76% dup, contracts epoch dates,
  NEISS future dates, SEC year-zero, 2 broken staging views).
- Two FDA medical-device tables reloaded as raw JSON, unflattened (map-blind).
- ~900 gated portal tables incl. offshore-leaks (name-keyed; real decision,
  not a bug).
- DEA numbers: single-source, inert until a second DEA source lands.
- Roll-call mart rebuild via Python builder (standing).
- Source-registry reconciliation (onboarding-log leg), CourtListener
  citation-network retry (standing).
- Six polygon tables unparseable geometry; some EPA/NTSB coordinates invalid
  (longitude 435.8). Pre-existing.
- Table-count discrepancy (2,216 claimed vs 1,871 live) unchased; non-portal
  landing = exactly 302 base tables (measured).

**YOUR MOVE:** nothing is blocked. Open question stands from this morning:
point the next session at reading the map (now with the politics history in
it), or at one of the repairs above.

**NEXT SESSION:**
1. Boot trust check vs this file and git log.
2. Read the map: what the two batches newly connected, what's newly askable —
   the multi-cycle FEC world and the enforcement chains first.
3. Otherwise: FEC-IDs flatten build or top data-trap repairs.

**Tests:** targeted key/visibility tests green after every edit; full suite
green at the wiring step (3,096/2-skip/standing-failure only); a final
full-suite run was still finishing at session close — result lands in the next
boot trust check.

**COST:** evening leg ≈ $8–15 (spine ~2h + map redraw ~1h + re-seed + targeted
re-profiles on X-Small; estimate, not metered). Day total including the
morning rebuild + repair: ~$30–48. The sniffer scan itself was ~$2–4 of that.
