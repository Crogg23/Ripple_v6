# RIPPLE STATUS — 2026-08-09 (evening session: scaffolder fix + staging models)

*One screen. Rewritten (never appended) at the end of every session. Sessions read this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE (still open):**
- Production staging views/marts not yet refreshed for the new models: this
  session's dbt build ran against the dev target (personal DBT_CROGERS schema)
  — all 11 models + 42 tests green there, and CI builds staging+intermediate on
  push, but the LIBRARY_MARTS.HEALTH copy of the VA all-cause mart is still the
  old 244-row junk shape until a prod mart build runs.
- 11 orphan twin tables still need dropping (Chris-only, unchanged).
- Old junk marts keep two demoted sources (`fed_faa_data_portal`,
  `fed_va_suicide_appendix`) reading as "modeled" in the catalog — drop with
  the orphans.
- FBI CDE key in `library-onboarding/.env` remains semi-exposed (chat-pasted
  2026-08-09); rotate at leisure.
- API signups still pending on Chris: DOL WHD, Senate LDA.

**INCIDENT FOUND & FIXED THIS SESSION (data corruption, was silent):**
Yesterday's VA *national* suicide load was partially scrambled: each cohort
sheet in the VA workbook stacks a second by-age table below the main one, and
the loader parsed everything under the first header — age brackets landed in
the deaths column, one column shifted, plus header rows as data (700 rows, 125
real keys). Caught via the standing COUNT(DISTINCT) key check while writing
staging models. Parser in `scripts/va_mortality_load.py` now segments sheets on
their internal header rows; all three VA tables relanded and key-verified
(national now 690 rows, unique on year x cohort x age_group). State and
all-cause files were single-table and unaffected.

**DONE this session (all verified, committed, pushed; CI was green on push):**
- Scaffolder gated (commit 8efde4b2): `loadkit/scaffold.py` now REFUSES to
  invent columns (no live DESCRIBE + no key_cols) and REFUSES to overwrite any
  existing schema.yml (the intl_ie_cro gutting path). 4 regression tests.
  Trade-off: specs with key_cols but no connection still get a keys-only
  skeleton (real columns, sparse) — tighten later if wanted.
- VA parser fix + reland (commit a1b74b16, see incident above).
- Real staging models for all 7 rebuilt sources / 10 tables (commit 816f5171):
  VA suicide national/state, VA all-cause, CDC WONDER (rewritten for new
  national grid), NCHS leading-causes-by-state, FBI CDE (rewritten as
  state-month; stale places model deleted), FAA aircraft registry, FRA
  casualties / crossing incidents / equipment accidents. Every grain
  COUNT(DISTINCT)-verified before tests were written. Deliberate calls
  documented in model headers: FRA equipment REPORT_KEY not unique
  (multi-railroad/amended filings — NO dedup, would discard 27k reports);
  FRA crossing 24 dup keys; WONDER deaths null = CDC suppression (<10);
  FAA owner name null on ~4,700 sale-reported registrations.
- health__fed_va_allcause_mortality mart rewritten onto the new staging model
  (was reading the dead raw shape directly).
- intl_ie_cro curated staging model verified to match the current landing
  shape — untouched, still good.
- dbt build (dev target): 11 models + 42 tests all green. Offline suite:
  2,698 passed / 2 skipped / 0 failed (twice today).

**YOUR MOVE:**
1. Nothing blocking. Orphan + junk-mart drop list available on request.

**NEXT SESSION:**
1. Wire the new staging models into marts (rail deaths by railroad, crime
   baselines, mortality baselines) and refresh prod schemas.
2. Run the connection engine over the relanded VA tables (columns changed;
   zip/name keys unaffected so drift is unlikely, but unverified).
3. Start the 73-source real backlog (high-priority landed-but-unmodeled).
4. Phase 0 leftovers: orphan drops, API signups (DOL WHD, Senate LDA).

**COST:** light day — roughly 0.3-0.5 Snowflake credits (~$1): metadata scans,
key checks over the 1.1M-row rail tables, one 690-row reland, dbt views +
tests. No large loads, no fingerprint scans.

**TEST STATUS:** offline 2,698 passed / 2 skipped / 0 failed; dbt build green
on dev target (11 models, 42 tests). CI green on main at push time.
