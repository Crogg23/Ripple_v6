# RIPPLE STATUS — 2026-08-09 (late session: marts for the rebuilt sources, prod refreshed)

*One screen. Rewritten (never appended) at the end of every session. Sessions read this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE (still open):**
- 11 orphan twin tables still need dropping (Chris-only, unchanged).
- Old junk marts keep two demoted sources (`fed_faa_data_portal`,
  `fed_va_suicide_appendix`) reading as "modeled" in the catalog — drop with
  the orphans.
- FBI CDE key in `library-onboarding/.env` remains semi-exposed (chat-pasted
  2026-08-09); rotate at leisure.
- API signups still pending on Chris: DOL WHD, Senate LDA.

**DONE this session (all verified, committed 784f7c32, pushed):**
- Four new marts built to production LIBRARY_MARTS and live-test-verified:
  - transport__fed_fra_rail_deaths_by_railroad — deaths by railroad x year x
    person type from FRA Form 55a casualties (per-person unique report keys,
    so no multi-railroad double-count; 53,105 deaths total, exact match to
    the fatality flag count; 12 two-digit years normalized to 2020).
    Top-5 since 2015: UP 2,280 / Amtrak 1,550 / BNSF 1,383 / CSX 1,123 / NS 1,045.
  - health__fed_cdc_leading_causes_state — NCHS leading causes by state
    1999-2017 (10,868 rows, incl. 'United States' rollup).
  - health__fed_va_suicide_state — veteran suicide by state x year (1,196
    rows; filters the by-state sheet from the 4-sheet stacked staging model).
  - health__fed_va_suicide_national — cohort x year x optional age group (690).
- Two stale marts that still read RETIRED raw shapes were rewritten onto the
  new staging models (they'd have failed or served junk on any prod build):
  - justice__fed_fbi_cde — now state x offense x month back to 1985 with
    OFFENSES/CLEARANCES pivoted to columns (238,680 rows). States are 2-letter
    abbreviations.
  - health__fed_cdc_wonder — now the national year x ICD chapter x sex grid
    (880 rows; deaths NULL = CDC suppression).
- health__fed_va_allcause_mortality rebuilt to prod (rewritten last session;
  prod had still been serving the old 244-row junk). Prod refresh item from
  last session is now CLOSED for all these models.
- Connection engine re-run over the three relanded VA tables: zero entity-key
  partitions (they're statistical aggregates — no zip/name keys), no drift.
- dbt build (marts, prod): 7 models + 26 tests green. Offline suite:
  2,698 passed / 2 skipped / 0 failed. CI was in progress at close
  (marts aren't in CI's staging+intermediate scope; low risk).

**YOUR MOVE:**
1. Nothing blocking. Orphan + junk-mart drop list available on request.

**NEXT SESSION:**
1. Start the 73-source real backlog (high-priority landed-but-unmodeled).
2. Phase 0 leftovers: orphan drops, API signups (DOL WHD, Senate LDA).
3. Optional: lens/KPI definition session if Chris opens it (his call).

**COST:** light — well under 0.5 Snowflake credits (~$1): metadata + value
checks, seven small mart builds (largest 238k rows), 26 tests, three
connection-engine runs over tiny VA tables.

**TEST STATUS:** offline 2,698 passed / 2 skipped / 0 failed; dbt marts build
green (7 models, 26 tests) against production databases.
