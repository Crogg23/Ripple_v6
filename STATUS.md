# RIPPLE STATUS — 2026-08-08

*One screen. Rewritten (never appended) at the end of every session. Sessions read this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE (still open):**
- The old, wrongly-named copy of the mortgage table is STILL in the warehouse. Rename verified (identical 28,301 rows both copies); agent is permission-blocked from running DROP even with Chris's verbal OK. One line for Chris in Snowsight:
  `DROP TABLE LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA;`
- Today's changes (nursing-home fix, checklist updates) are uncommitted — small diff, review anytime.

**FIXED this session (verified live, not just claimed):**
- Nursing-home "silently blank NPI" mystery SOLVED: checked CMS's real source live (all 100 columns of the provider dataset) — the source has NO NPI field at all. The column was phantom. Removed it from staging + mart + schema docs; rebuilt live; all 25 model tests pass. NPI↔facility linking correctly lives in the facility-affiliation bridge instead.
- Entity spine fully rebuilt and reconciled. Chain of events: 3 CMS tables had fresh data the spine hadn't absorbed → ran the cheap incremental catch-up → that EXPOSED pre-existing drift (~99 excluded-provider entities with stale pair/membership records, predating today) that the incremental path can't repair by design → Chris approved the full rebuild (priced first) → rebuild ran clean. Result: 31.85M entities, 4,615 verified connections, incremental state re-synced.
- All 6 spine-health equivalence checks now PASS (were 3 FAIL at worst mid-session).

**WORKS:**
- Full offline suite GREEN after everything: 2,692 passed, 2 skipped, 0 failed.
- Spine validate: all checks pass. Incremental heartbeat is trustworthy again.

**YOUR MOVE:**
1. Run the one-line DROP above (only thing an agent can't do).
2. Commit today's small diff whenever convenient.
3. Phase 0 checklist still open (Snowsight credential grants, orphan-table drops, API signups) — see outputs/phase0_chris_checklist_2026-08-06.md (HMDA section updated today).

**NEXT SESSION:** Loaders off the full-admin credential (blocked on Phase 0 grants), then the cross-agency entity-matching planning session with Chris.

**COST:** One approved warehouse spend: full spine rebuild, ~4.5 hours wall-clock on the X-Small warehouse ≈ 4-5 credits ≈ ~$10-15 (priced and approved before running; original estimate said 30-60 min — wall clock was 4-5x that, dollar estimate held because the warehouse is the smallest size). Plus small read-only checks and two dbt/test runs (minutes).

**TEST STATUS:** 2,692 passed / 2 skipped / 0 failed (full suite, post-rebuild). Spine equivalence validate: 6/6 PASS. Nursing-home staging+mart rebuilt live: 25/25 tests (1 pre-existing warn on ownership-type wording, unrelated).
