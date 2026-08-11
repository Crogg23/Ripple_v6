# RIPPLE STATUS — 2026-08-10 (late, second session) — mart defects verified and fixed

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing new. Two pre-existing problems were confirmed and could NOT be
fixed by shaping — they need a re-ingest:**
- **Immigration court (12.6M rows) is worse than last session thought.** It is not
  a bad model. The *landing table itself* holds one real column. Every judge,
  court, date, charge and outcome field was thrown away at ingest, so there is
  nothing in the warehouse to remodel. No loader for it exists in the repo — it has
  to be re-downloaded and re-loaded from scratch. The model now carries a header
  saying exactly this so nothing gets built on it by mistake.
- **FDIC enforcement**: the scrape only ever captured page text and a URL. No bank,
  date or penalty. Its mart isn't built at all.

**DONE this session:**
- Checked every claim in last session's defect list against live data before
  touching anything. A good share of it was wrong — the original doc is now marked
  superseded, verdicts in `reports/mart_defect_verdicts_2026-08-10.md`.
- **Found and fixed the real bug: 133 columns across 82 marts were 100% empty.**
  The model generator matched its casting rules as bare text, so "COUNT" matched
  COUNTRY and COUNTY, "RATIO" matched INCORPORATION and REGISTRATION. Snowflake's
  try-to-number returns blank instead of failing, so every model built green while
  the column was gone. Casualties: every country field in the SEC quarterly
  submissions, both Senate lobbying country fields, EPA county fields, FDA reporter
  country, ten labour worksite-county fields, EU/UN sanctions countries.
- Un-wrapped 173 columns across 101 model files and rebuilt all of them.
  **143 of 150 checked columns now carry data**; the other 7 are blank at the source.
- County/state FIPS codes are now text, not numbers — casting them was stripping
  the leading zero and breaking every join keyed on them.
- Restored real column names on the four FEC marts (candidates, committees,
  linkage, PAC summary), verified field-by-field against the official FEC layout.
- Deleted three stale duplicate model files (NHTSA under transport; the named
  consumer-safety copies are the live ones). **No table was dropped.**
- Added 44 offline tests that fail the build if this cast bug ever comes back.
- Offline suite green: 2,727 passed, 2 skipped.

**Also verified and worth knowing (not acted on):**
- 18 marts sit on an exact loader page boundary (500,000 / 10,000 / 5,000 rows) —
  strong sign of a truncated pull. IRS revocations, IRS Pub 78, three Google
  political-ads tables, CourtListener investments, both OSHA case-detail years,
  Treasury deposits, FDIC BankFind, EPA Envirofacts, USAspending subawards.
- 49 marts have a live row count that disagrees with the catalog or their own
  header comment by more than 1%.
- The eleven "one-column shell" marts flagged last session were a false alarm —
  they are JSON sources and the marts already unpack them properly.

**Live/open items carried forward:**
- FEMA IA full reload STILL RUNNING (19.5M of 25.9M at close; rerun
  `python scripts/fema_ia_load.py` to resume if dead). When done: rebuild
  staging+mart, remove SAMPLE label, reseed connections.
- UK Companies House PSC blocked on the Chris-only wipe:
  `DELETE FROM LIBRARY_RAW.LANDING.UK_COMPANIES_HOUSE_PSC;` then
  `python scripts/uk_ch_psc_load.py --chunks 32 --run` (~30-60 min).
- Drop list (Chris-only, ~50 tables):
  `reports/duplicate_ingest_drop_list_2026-08-10.md`.
- Key-gated on Chris: FCC broadband map, DOL WHD, Senate LDA.
- Small tail: OFCCP audit list (manual), DTCC directory (manual), PHMSA's other 3
  pipeline files.

**TEST STATUS:** offline suite green (2,727 passed, 2 skipped) — re-run this
session after the model changes. Connection-engine reseed was still running at
close; validate it (`python -m connect.incremental seed --reseed`, then the
connection tests) at next boot. CI not re-checked.

**YOUR MOVE:**
1. Nothing is blocked on you for the fix work. The two open calls are the same as
   before: the UK PSC wipe one-liner, and the ~50-table drop list.
2. Still yours from last session: skim the brainstorm spreadsheet and flag what you
   want built; the portal-probe universe (~1,800 rows).

**NEXT SESSION:**
1. Boot trust check, validate the connection reseed, FEMA finish → rebuild →
   un-SAMPLE → reseed.
2. Steps 3 and 4 of the defect plan, still open: re-pull the 18 page-capped tables,
   and flag every sample-only source in the catalog so a chart builder can see it.
3. The immigration-court re-ingest — biggest single unlock, needs a new loader.

**COST:** roughly $3-6 of warehouse credit (the verification scan plus rebuilding
101 marts). Agent spend: none, single session.
