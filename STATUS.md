# RIPPLE STATUS — 2026-08-10 (backlog wave 4: 46 sources modeled; NIH full history landed)

*One screen. Rewritten (never appended) at the end of every session. Sessions read this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing.** Open items, none blocking:
- Two truncated SAMPLEs still await full re-ingest (both queued, priced work):
  UK Companies House PSC (7M of ~10M; needs fresh-snapshot re-ingest ~30-60 min)
  and FEMA IA registrations (3.08M of 25.9M via OpenFEMA API — sizeable, price
  before running).
- Drop list for Chris grew: the ~30 dupe rows from wave 3 PLUS (added this
  session, all verified) 4 corrupted power-plant vintage twins, 3 junk 1-row
  loads (SEC tickers JSON-in-one-row, FinCEN BOI legally-restricted placeholder,
  CMS hospital-price GitHub-listing), and 1 leftover internal staging table —
  reports/duplicate_ingest_drop_list_2026-08-10.md. DROPs are Chris-only.
- FBI CDE key still semi-exposed in library-onboarding/.env; API signups still
  pending on Chris: DOL WHD, Senate LDA.

**DONE this session (commit 1dae94e2 pushed; NIH rebuild after it):**
- NIH RePORTER full-history reload FINISHED CLEAN: 27 fiscal years (2000–2026),
  2,122,611 rows, distinct APPL_ID = row count, zero gaps vs the publisher's
  own per-year counts. Staging+mart rebuilt; catalog shows modeled, full,
  not a sample.
- Backlog wave 4 — 46 sources flipped landed→modeled (catalog 452→511 modeled,
  89 landed rows remain incl. ~30 dupes = ~55 real backlog). Every grain
  COUNT(DISTINCT)-verified live first. Highlights:
  - ITIS taxonomy family ×19 → REFERENCE (core taxa 993k, ref links 1.97M).
  - NYC CFB campaign contributions ×5 cycles (2001–2025) → POLITICS
    (1.25M contribution rows total; 2001 cycle needed the surrogate-key idiom).
  - EIA-860 power plants ×10 + EIA-861 utility survey ×18 → ENERGY (2024
    vintage; upgraded from auto-generated passthrough staging). Vintage
    decision made: sheet-numbered family kept, 4 corrupted twins → drop list.
    Five 861 tables lost their first data row into the Excel header at load —
    modeled with that caveat in every affected description.
  - EPA GHGRP emissions+facilities, SBIR/STTR awards, NTSB aviation injuries,
    FDA UNII substance crosswalk hub, DailyMed label map, PCAOB audit-partner
    filings → their domain folders.
- dbt build: 119 models + 311 tests all green (one warehouse pass).
- Three 1-row landing tables inspected and condemned (junk loads, not modeled).

**TEST STATUS:** offline 2,698 passed / 2 skipped / 0 failed (full run after
authoring). dbt wave-4 build 430/430 green; NIH rebuild 7/7 green. Wave-4
commit pushed (CI state not re-checked this session — verify at next boot).

**YOUR MOVE:**
1. Nothing blocking. The enlarged drop list is ready whenever you want to
   clear it (Chris-only DROPs).

**NEXT SESSION:**
1. Verify CI went green on the wave-4 push (boot trust check).
2. Full re-ingests for the two truncated SAMPLEs: UK PSC (fresh snapshot),
   FEMA IA (25.9M — show Chris the price line first, §8.7).
3. Drain the ~55 real remaining backlog sources (biggest left: retraction
   watch 72k, dams 93k, orphaned wells 118k, HPSA 79k, EPA TRI facility 65k,
   HUD/USDA housing tables, credit-union/bank registries, long tail <65k).
4. Phase 0 leftovers: drops (Chris), API signups (Chris).

**COST:** moderate — roughly 1-2 Snowflake credits (~$3-6): grain checks over
~60 mostly-small tables, 119-model build + NIH mart rebuild (2.1M rows), two
catalog verification queries; NIH reload API pull ran to completion (small
steady writes). Agent spend: 5 parallel model-writers, ~395k tokens.
