# RIPPLE STATUS — 2026-08-11 — trust work: labels, stale marts, two full pulls, one data-corruption bug

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing new.** Both jobs that were dead at boot are fixed and one is
still running by design (see live items).

**The theme of this session: the warehouse had data that lied about itself.**
Four separate bugs, all the same shape — something that read as complete or
populated and was not. Every one of them would have produced a confident, wrong
chart. All four are now fixed AND guarded by tests that fail the build if they
come back.

**DONE this session:**

- **Fixed the mis-filing bug — same failure as yesterday's cast bug.** A rule
  meant to match a whole word was matching fragments. "ice" (the immigration
  agency) matched inside "hospice" and "service", so hospice care, Medicare
  fee-for-service and drinking-water service areas were filed as immigration.
  "ed" (the Education Department) matches inside "federal", which is how
  commodity-trading data landed under education. 21 models moved; filenames left
  alone, so no warehouse table was renamed and nothing joined the drop list.
- **Recovered ~8.1M rows that were already paid for and invisible.** 19 marts had
  been built before their raw table was last loaded. Four were on the "needs
  re-pulling" list and needed no pull at all. Court financial-disclosure
  investments went 500,000 → 1,901,599; one political-ads table 500,000 →
  4,773,180; another 500,000 → 1,562,870; workplace-injury case detail 500,000 →
  890,934 and 688,649; plus the Irish company registry and six smaller ones.
- **Sample-only sources now declare themselves.** 16 marts said "this is a slice,
  not the full source" in their own file and nothing surfaced it. Those
  statements are now in the catalog, with the author's sentence explaining WHICH
  slice (mortgage data is one state-year; a portal is a 5,000-row page).
- **Corrected 39 stale row counts in model headers — they were UNDERSTATING.**
  Headers claimed a 500,000-row cap on tables now holding 31.4M, 15.4M, 12.5M.
  Eleven complete national datasets read as samples to anyone opening the file.
- **Two capped sources pulled in full**, each checked against the source's own
  advertised total, not assumed:
  - Bank directory: 10,000 → **27,836** institutions, founded 1782–2026. Only
    4,254 are still active, so ~23,600 closed or merged banks are now visible.
  - Federal daily cash ledger: 10,000 → **478,149** records, 5,237 business days
    from Oct 2005 to Aug 2026 — money in and money out, by category, per day.
- **Found and fixed a real data-corruption bug in five loaders.** Missing values
  were being written as the literal text "nan". A bank identifier looked 6,260
  populated; 4,008 of those were junk. The branch-deposits table held **4.2
  million** corrupted cells, including a branch identifier and both map
  coordinates. Loaders fixed, that table repaired and verified clean, marts
  rebuilt. A repair tool exists for any other table.
- Connection engine rebuilt (2,076 tables pinned), passes 20/20. The boot blocker
  from the last two sessions is cleared.
- Checked-in catalog definition had drifted from the live warehouse; replaying it
  would have silently reverted a fix. Re-synced.
- Tests: **2,807 passed, 2 skipped, 0 failures** — 63 new guards this session.
  CI is green on everything pushed. Five commits sit locally, unpushed.

**Two things the last handoff got wrong — don't redo them:**

- The "18 page-capped marts" list was mostly wrong. Five were stale marts, not
  short pulls. One supposedly capped at 500,000 actually holds 1,207,295.
- Catalog row counts were never stale; they read live. Only file comments drifted.

**One claim I corrected myself on:** the bank data does NOT join directly to the
global company register. The government publishes that identifier truncated to 16
characters against a real one's 20, so a straight join matches zero rows. Joining
on the first 16 characters works and matches 2,224 of the 2,252 banks that carry
one — but only ~8% of banks have one at all. Both model headers say this now.

**Live/open items carried forward:**

- Disaster-aid reload still running: **20.07M of 25.9M**, roughly 13 hours left.
  It rides through the government API's slow patches now and checkpoints every
  page, so it survives a restart. When it finishes: repair the "nan" cells,
  rebuild, drop its sample label, reseed connections.
- UK company-ownership load blocked on the Chris-only wipe:
  `DELETE FROM LIBRARY_RAW.LANDING.UK_COMPANIES_HOUSE_PSC;` then
  `python scripts/uk_ch_psc_load.py --chunks 32 --run` (~30-60 min).
- Drop list (Chris-only, ~50 tables):
  `reports/duplicate_ingest_drop_list_2026-08-10.md`.
- Key-gated on Chris: broadband map, wage-and-hour, Senate lobbying.

**NOT done — the honest list:**

- **Immigration court records, 12.6M rows, are still a husk.** Every judge, date,
  charge and outcome was thrown away at ingest. Biggest single unlock left,
  needs a loader built from scratch. Untouched.
- Bank enforcement actions captured web page text, not data. Needs a real parser.
- Smaller capped sources still need paginated loaders: EPA chemical facilities,
  federal spending subawards, four national open-data portals, the European
  court. Most now carry an honest sample label at least.
- Catalog hygiene: 249 modeled sources have no subject area, 67 unclassified,
  139 have no last-ingested timestamp.
- Worth a look someday: the guarded folder that blocks rebuilds now holds a
  number of ordinary generated marts, which cannot be rebuilt by the normal path.

**YOUR MOVE:**

1. Nothing is blocked on you for this session's work.
2. Same two one-liners as before: the UK company-ownership wipe, and the ~50-table
   drop list.
3. Still yours: skim the chart-idea spreadsheet and flag what you want built.

**NEXT SESSION:**

1. Boot trust check. Finish the disaster-aid load → repair the sentinel cells →
   rebuild → drop its sample label → reseed connections.
2. Loaders for the remaining small capped sources.
3. Catalog hygiene, then the immigration-court re-ingest.

**COST:** roughly $2-4 of warehouse credit all session — a few minutes of mart
rebuilds, one repair pass over 2.8M rows, and metadata queries, which are free.
No agent spend, single session.
