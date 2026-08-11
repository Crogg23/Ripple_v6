# RIPPLE STATUS — 2026-08-11 — routing bug fixed, 8.1M hidden rows recovered, slices now labelled

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing new.** Two jobs were dead at boot and both are running again:

- The disaster-aid (FEMA) reload had died at 19.52M of 25.89M rows. The page was
  NOT broken — re-requesting the same offset returns data fine. The government's
  API just crawls once you are ~19M rows deep, and the loader's retry budget was
  tuned on shallow pages, so six slow reads in a row killed it. Retries now wait
  far longer and back off harder. Resumed and progressing (19.8M at close).
- The connection-engine rebuild was NOT broken either. It prints one line, at the
  very end. Last session read two hours of silence as a hang and killed a healthy
  job. Confirmed alive this time by watching the warehouse: thousands of small
  updates, about one a second. Still running at close.

**DONE this session:**

- **Found the mis-filing bug, and it is the same failure mode as yesterday's cast
  bug**: a rule meant to match a whole word was matching fragments. "ice" (the
  immigration agency) matched inside "hospice" and "service", so hospice care,
  Medicare fee-for-service and drinking-water service areas were filed as
  immigration. "ed" (the Education Department) matches inside "federal", which is
  how commodity-trading data landed under education. Matching now requires a word
  boundary and the earliest match wins, so the publishing agency decides. 21
  models moved. Filenames deliberately unchanged, so no warehouse table was
  renamed or rebuilt and nothing was added to the drop list.
- **Recovered ~8.1M rows that were already paid for and invisible.** 19 marts had
  been built BEFORE their raw table was last loaded. Four of these were on the
  "needs re-pulling" list and needed no pull at all — the full data landed Aug 5,
  the mart was last built Jul 30. Court financial-disclosure investments went
  500,000 → 1,901,599; Google political-ads creative-id mapping 500,000 →
  4,773,180; creative stats 500,000 → 1,562,870; workplace-injury case detail
  500,000 → 890,934 (2023) and 688,649 (2024); plus the Irish company registry and
  six smaller ones. Two minutes of compute, all data checks passed.
- **Sample-only sources are now visible.** 17 marts said "SAMPLE ONLY — NOT the
  full dataset" in their own file, and nothing surfaced it, so the catalog
  advertised them under the full source's name. Those declarations are now lifted
  into a control table and the catalog exposes both a flag and the author's own
  sentence explaining WHICH slice it is (mortgage data is one state-year; the
  bank directory is a 10,000-row page).
- **Corrected 39 stale row counts in model headers — and they were understating,
  not overstating.** Headers claimed a 500,000-row cap on tables that now hold
  31.4M (nursing-home assessments), 15.4M (drinking-water violations), 12.5M
  (dialysis facilities). Eleven complete national datasets read as samples to
  anyone opening the file. All now match live, each with a dated note saying what
  it used to say.
- Found the checked-in catalog definition had drifted from the live warehouse
  (missing a Jul 30 fix). Replaying it would have silently reverted that fix.
  Re-synced.
- Tests: **2,771 passed, 2 skipped, 0 failures**, including 38 new guards.

**Corrections to what the last handoff assumed — read before doing step 3:**

- The "18 page-capped marts" list is mostly wrong. Five were stale marts, not
  short pulls, and are now fixed. IRS auto-revocations is NOT capped (1,207,295
  rows, not 500,000). What genuinely remains capped is the small stuff: the bank
  directory (10k), Treasury deposits (10k), EPA Envirofacts (5k), USAspending
  subawards (5k), four national open-data portals (1k–5k), the European court
  (2k), and a couple more — and most of those already carry the SAMPLE ONLY
  label now.
- Row counts in the catalog were never stale; they read live. Only the file
  comments had drifted.

**NOT done — carried forward:**

- **No new loaders were written.** The genuinely-capped small sources above still
  need proper paginated loaders. This is what is left of step 3.
- Catalog hygiene: 249 modeled sources still have a blank subject area, 67 are
  unclassified, 139 have no last-ingested timestamp.
- The connection-engine rebuild had not finished at close, so its validation test
  has not been run yet. Do that first next session.
- Worth a look: the guarded folder that blocks rebuilds now holds a number of
  ordinary generated marts, which means those cannot be rebuilt by the normal
  path. Not urgent, not touched.

**Live/open items carried forward:**

- Disaster-aid reload still running, ~19.8M of 25.9M, roughly 14 hours to go. It
  checkpoints every page, so it survives a restart. When it finishes: rebuild
  staging + mart, drop the SAMPLE label, reseed connections.
- UK company-ownership load blocked on the Chris-only wipe:
  `DELETE FROM LIBRARY_RAW.LANDING.UK_COMPANIES_HOUSE_PSC;` then
  `python scripts/uk_ch_psc_load.py --chunks 32 --run` (~30-60 min).
- Drop list (Chris-only, ~50 tables):
  `reports/duplicate_ingest_drop_list_2026-08-10.md`.
- Key-gated on Chris: broadband map, wage-and-hour, Senate lobbying.
- Immigration court re-ingest — still the biggest single unlock, still needs a
  brand new loader. Untouched.
- Bank-enforcement scrape still captures only page text; needs a real parser.

**YOUR MOVE:**

1. Nothing is blocked on you for this session's work.
2. Same two one-liners as before: the UK company-ownership wipe, and the ~50-table
   drop list.
3. Still yours: skim the chart-idea spreadsheet and flag what you want built.

**NEXT SESSION:**

1. Boot trust check; validate the connection rebuild; finish the disaster-aid
   load → rebuild → drop its SAMPLE label → reseed.
2. What is left of step 3: paginated loaders for the small capped sources.
3. Catalog hygiene (blank subject areas, missing timestamps).

**COST:** roughly $1-2 of warehouse credit — the rebuilds were about two minutes
of compute, and everything else was metadata queries, which are free. No agent
spend, single session.
