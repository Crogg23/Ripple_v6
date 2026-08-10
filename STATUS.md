# RIPPLE STATUS — 2026-08-09 (night session: backlog wave 1 — ICIJ, ICE, OpenSanctions, FRA)

*One screen. Rewritten (never appended) at the end of every session. Sessions read this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE (still open):**
- 11 orphan twin tables still need dropping (Chris-only, unchanged).
- Old junk marts keep two demoted sources (`fed_faa_data_portal`,
  `fed_va_suicide_appendix`) reading as "modeled" in the catalog — drop with
  the orphans.
- FBI CDE key in `library-onboarding/.env` remains semi-exposed; rotate at
  leisure. API signups still pending on Chris: DOL WHD, Senate LDA.

**DONE this session (two commits, 784f7c32 + 1a6a83ab, both pushed):**
Part 1 (earlier close, see git): 4 new marts + 2 stale-shape rewrites +
prod refresh for the rebuilt sources (rail deaths by railroad, FBI crime
state-month, CDC WONDER national, NCHS by-state, VA suicide state/national).
CI green on both those pushes.

Part 2 — backlog wave 1, 12 sources flipped landed→modeled in the catalog
(verified live), every grain COUNT(DISTINCT)-checked before tests:
- ICIJ Offshore Leaks, 6 tables / 5.36M rows → CORPORATE_REGISTRY marts:
  entities/officers/intermediaries/addresses/others all unique on node_id;
  relationships edges NOT unique (multi-leak republication, kept as landed).
  29 unnamed entities and a few absurd incorporation dates (year 199, 2812)
  are ICIJ's own data, kept as published.
- ICE detention stints (2.62M, person-level anon hashes, 2004-2026) + ICE
  detainers (610k, Oct 2022-2026) → IMMIGRATION marts. Stint mart excludes
  only publisher-flagged duplicate rows (2,571,975 kept). Known quirks
  documented, not "fixed": person hash blank on 7,341 stint rows and 74,751
  detainer rows; detainer rows only unique with file+row provenance; some
  dates future-dated as published.
- OpenSanctions default collection (1.28M worldwide sanctions/PEP targets,
  unique id) → JUSTICE mart, distinct from the smaller sanctions-only
  collection already modeled.
- FRA passthrough marts (casualties / crossing / equipment) so the three
  rail sources register as modeled; the intended detail-vs-rollup row-count
  difference on casualties is documented in the duplication guard with its
  reconciliation (53,105 deaths both ways).
- Connection engine: all nine new tables were already linked at land time
  (content-key no-ops) — nothing to redo.
- dbt build green (21 models, 52 tests). Offline suite 2,698 passed /
  0 failed (the one failure during the session was the duplication guard
  correctly catching the FRA detail/rollup pair — resolved by documenting).

**YOUR MOVE:**
1. Nothing blocking. Orphan + junk-mart drop list available on request.

**NEXT SESSION:**
1. Continue the backlog: next biggest are
   IRS exempt-orgs master file (281k), NIH grants (206k), plus the sampled
   API sources (USAspending bulk, HMDA, FDIC) which may need fuller loads
   before modeling — check before building.
2. Phase 0 leftovers: orphan drops, API signups (DOL WHD, Senate LDA).
3. Optional: lens/KPI definition session if Chris opens it (his call).

**COST:** light-moderate — roughly 1 Snowflake credit (~$2-3): key checks
over the 3.3M-row edge table and 2.6M-row stints, twelve mart builds
(largest 3.3M rows), 52 tests, two offline-suite warehouse-check runs.

**TEST STATUS:** offline 2,698 passed / 2 skipped / 0 failed; dbt build
green (21 models, 52 tests) against production databases. CI green on all
four pushes this session.
