# Warehouse pre-launch QA/QC — 2026-09-20

Six-dimension audit, 24 agents, 738 live tool calls, adversarial verify pass on every
moderate+ finding (a second agent tried to refute each one against live data before
severity was finalized). Scope: is the MARTS/THE_LIBRARY layer — the stuff that
actually feeds findings and visuals — safe to build real work on right now.

Severities below are POST-VERIFICATION (`updated_severity` where a verify pass ran).

---

## 1. Staging dedupe fix (2026-09-19) — is it actually done

**Grade impact: moderate**

- **Renamed models leave the old, broken view alive** — MODERATE
  7 staging models were renamed during the fix (e.g. `__PLACES` -> `__RECORDS`,
  `__RECORDS` -> `__FACILITIES`). Renaming doesn't drop the old view — it just stops
  managing it. All 7 old-named views are still live in `LIBRARY_STAGING.DBT_CROGERS`
  today, still holding the pre-fix undercount (e.g. `STG_FED_EPA_ECHO__RECORDS` =
  3,135,554 rows, old and short, vs correct `__FACILITIES` = 3,157,891). Confirmed
  zero mart or THE_LIBRARY consumption. Not currently poisoning output, but anyone
  querying the old name by hand gets a silently wrong count.

- **42 views (not 44) still hide rows on one load** — MINOR
  2 with a real share: `FEC_PAC_SUMMARY` (5.6% hidden, live-verified, untouched by
  the fix), `UK_SANCTIONS_LIST` (1.1%, down from 41.6%, not closed). The other 40 are
  sub-1%, mostly ~20 headerless EIA860/861 tables each missing exactly 1-2 rows —
  same root cause, one investigation would likely close all of them.

- **A frozen pre-fix schema copy sits live** — MINOR (`LIBRARY_STAGING.DBT_CROGERS_RIPPLE`,
  a one-shot before/after baseline, not read by anything, but a same-view-name trap
  for anyone who queries the wrong schema).

- 4 of 5 named worst pre-fix offenders verified live today: exact match to landing,
  fix genuinely reached production, not just the dbt files. FCA_SETTLEMENTS (19 rows)
  is the one small source never touched by the same-day hand-fix batch.

---

## 2. Type-cast integrity feeding marts

**Grade impact: severe**

- **Marts routinely re-cast raw landing columns with zero guard, zero check — and it
  already broke once** — SEVERE
  371 of 679 mart files (54.6%) read straight from `source()`, bypassing staging
  entirely. 240 of those use ONLY bare `try_to_date/try_to_number/try_to_double`
  with no guard. `economics__fed_usaspending_contracts_full.sql` carries a comment
  documenting a real incident: a bare `try_to_date()` read a small integer as epoch
  seconds and collapsed 20M rows onto 1970-01-01, caught by hand. `check_staging_casts.py`
  only globs `models/staging/*.sql` — structurally cannot see this file or this bug.
  One whack-a-mole regression test (`assert_no_epoch_or_pivot_dates.sql`) guards the
  one column that already broke; every other column in that same file, and ~230+
  other bare-cast mart files, have zero guard.

- **Bare TRY_TO_NUMBER rounding is live and active today, not theoretical** — SEVERE
  (escalated from moderate on verify). `health__fed_cms_pos_other.sql` casts ~200
  nursing-facility staffing columns with bare `try_to_number`, bypassing an
  already-existing guarded staging model for the same source. Live-confirmed: 20 of
  201 cast columns hold real decimal values today (e.g. `PHYSN_CNT` 17% of rows),
  and `try_to_number('1.5') -> 2`, `try_to_number('4.5') -> 5` — silent rounding on
  real physician/RN/therapist staffing counts, right now. Recurs in 28 of 139
  similarly-generated mart files.

- **36.5% of staging models never touch the checked macro layer** — MODERATE
  512 of 1,402 staging files are hand-written, use zero `stg_*` macros, and are
  invisible to `check_staging_casts.py`'s 8,635-column sweep. ~half of those (235)
  have hand-rolled casts with unmeasured loss risk; the rest do no casting at all
  (stay TEXT).

- `lost_null_words` nonzero on 84/8,635 columns — traced, all correctly-nulled
  placeholder words, not lost real values. INFO.
- `_partial.tsv` / `staging_cast_overrides.tsv` are working as designed, not gaps —
  traced to source. INFO.
- Script and macro are hand-synced by comment convention only, currently in sync,
  no test enforces it — future drift risk. MINOR.

---

## 3. Money / corporate / political traps — code-enforced or tribal-knowledge-only

**Grade impact: severe** — 5 of 6 traps are NOT enforced in mart code.

- **FEC MEMO_CD earmark double-count: unfiltered** — SEVERE
  `finance__fed_fec_indiv_contributions` drops MEMO_CD entirely (can't even filter).
  `finance__fed_fec_committee_to_candidate` carries it with zero WHERE — live: 18,643
  memo rows worth $86M sit unfiltered beside 848,087 real rows worth $5.7B. The
  itoth/committee-to-committee file has no mart at all (93.3% memo rows, $3.66B of
  $23.0B, live-confirmed). Worse: `scripts/build_giant_aggs.py` builds the actual
  PUBLIC campaign-finance aggregates (`MONEY_IN_POLITICS__FEC_INDIV_BY_STATE_CYCLE_AGG`,
  feeding THE_LIBRARY.CAMPAIGN_FINANCE) straight from raw landing, bypassing dbt
  entirely, with no MEMO_CD filter — live check: excluding memo rows shifts the
  total by ~$1.9B of $79.5B (2.4% system-wide). Same table is ALSO stale: sums to
  84.17M records against a raw table that now holds 283.8M across 14 cycles — missing
  10 of 14 cycles, never rebuilt after expansion.

- **USASpending per-FY/day caps: mischaracterized or undocumented** — SEVERE
  Live-confirmed: `FED_USASPENDING_CONTRACTS_FULL` = exactly 1,000,000 rows for
  every FY 2007-2026 (20/20 years, a hard page cap). `FED_USASPENDING_ASSISTANCE_FULL`
  has the identical signature (19/20 years at exactly 1M, the one exception is the
  one year true volume fell under it) — zero documentation anywhere, worse than the
  contracts table where at least a comment half-explains it. `LIBRARY_META` registry
  notes say "expect 100M+ rows" — stale and wrong. A corrected reload (`_FULL_R2`,
  93.1M rows, real per-FY counts) already exists, but the TIMELINE layer
  (`timeline__economics__fed_usaspending_contracts_full.sql`) is wired to the OLD
  capped mart and its own comment calls it "the real clock for all 20M rows."
  Assistance has no R2 fix at all.

- **Portal 10,000-row page cap: 2 live, currently undetected instances found** — SEVERE
  (escalated from moderate on verify). The only cap-catcher (`scripts/verify_mart_defects.py`)
  is a one-time manual script, never re-run, output not kept. Live sweep of
  `LIBRARY_MARTS` found 8 tables at known page-cap round numbers; 6 are correctly
  labeled "SAMPLE ONLY." 2 are not: `CRIMINAL_JUSTICE__FED_BJS_DATA` (1,000 rows
  live) and `JUSTICE__INTL_HUDOC` (2,000 rows live) — both have a corrected full
  reload already sitting in landing (`FED_BJS_DATA_FULL` 68,852 rows,
  `INTL_HUDOC_FULL` 211,778 rows) that nobody repointed the mart to. Also found a
  dead capped copy of `FED_SAM_EXCLUSIONS` (10,000 rows) left behind after the mart
  was correctly moved to `_FULL_R2` — harmless today, a trap if queried directly.

- Registry name-vs-SOURCE_ID join and registry VOLUME-as-text: both confirmed N/A —
  neither lives in the dbt mart layer or is touched by any mart today. INFO.
- **NPPES EIN sentinel: the one trap that IS fixed in code, and it held** — INFO.
  Staging model masks the fake-populated sentinel; mart passes the fix through;
  one downstream mart independently documents "no EIN or CCN to bridge on."

---

## 4. Health / regulatory / facility traps

**Grade impact: moderate** — 2 of 7 traps enforced, 1 half-baked, 4 tribal-knowledge-only.

- **Part D DY2022 vintage: half-baked** — MODERATE. The 2 places a Part D join
  actually happens today handle the vintage gap explicitly (one refuses a timeline
  verdict, one hardcodes matching years). The 3 general Part D marts carry zero
  year/vintage column — the next join anyone builds gets no protection.

- **Part B suppressed subset: no floor caveat anywhere in code, and the floor is
  live and hard** — SEVERE (confirmed, held at severe). Live: service-level table
  has 9,781,673 rows / 1,207,473 distinct NPI vs provider-level's 1,296,739 rows /
  1,296,739 distinct NPI — 89,266 providers with zero surviving service rows.
  `TRY_TO_NUMBER(TOT_BENES)` floor is exactly 11, zero exceptions, live, today. One
  sampled NPI: provider-level shows $1,229,994; service-level sums to only $223,658
  for the same provider — 90.2% of the money invisible at the service grain, with
  zero caveat in any SQL, schema, or doc file in the whole dbt project.

- **Facility affiliation under-reporting** — downgraded to MINOR on verify: real gap,
  but the flagged mart is orphaned (zero downstream consumers), so it's inert today.

- **CHOW flag + HUD/SNF owner flags: mixed** — MODERATE. 2 of 3 flags never leave
  staging (moot). The CHOW flag in `health__fed_cms_nursing_home` is a live-confirmed
  constant 'N' on all 14,700 rows, uncommented, in a heavily-referenced general mart.
  Verify pass found a sharper wrinkle: the SAME column name in the sibling mart
  `health__fed_nursinghome411` is NOT constant (55/14,713 rows = 'Y') — identical
  undocumented name, opposite behavior in two marts.

- HMDA historic file family: correctly wired to the all-records reload, documented
  in both model and schema. INFO — clean pass.
- Percentile/cohort rule: the only live example (`justice__county_double_burden`)
  does it correctly, common cohort enforced before ranking. INFO — clean pass.

- **DME by-referrer/supplier: already fired once, still unprotected** — SEVERE
  (escalated from moderate on verify). Suppression flags exist in the mart but
  aren't filtered or documented. `.claude/traps.md` already has a full quantified
  investigation of this exact trap (families undercount TOT_ by 21-40%). Worse: the
  mart is already in live use — `reports/tier1_deep_dive_2026-09-05/E41_.../queries.py`
  joins to it and feeds a published finding. That one query happened to only pull
  TOT_ columns, so it likely survives — but nothing in code stops the next query
  from summing family columns and landing 20-40% off.

---

## 5. dbt test coverage, marts layer — plus the untestable-unique bug, one layer up

**Grade impact: moderate**

- Full census: 561 model definitions across 535 yml files / 25 domains. 468 (83.4%)
  test a real key column; 550 (98.0%) have some test; 11 (2.0%) have zero tests of
  any kind. Weakest domains: immigration 42%, history 60%, finance 71%, justice 72%.

- **The staging "untestable unique test" bug recurs one layer up, unfixed by the
  2026-09-19 patch** — downgraded from severe to MODERATE on verify (mechanism
  confirmed real, but live check found 5 of 6 currently show zero actual row loss —
  latent, not active). 6 models dedupe on a key via `QUALIFY ROW_NUMBER` and then
  declare that same key unique in schema.yml — structurally guaranteed to pass
  forever, identical to the 289-view staging bug before the fix: `int_nursing_home_prf_match`
  (2 tautological tests), `economics__fed_sba_ppp` (loan_number), `environment__fed_epa_frs_facilities`
  (registry_id), `finance__fed_sec_insider_submission` (accession_number),
  `labor__fed_msha_mines` (mine_id), `procurement__fed_sam_exclusions` (sam_number).
  None were touched by the staging fix commit.

- 11 marts have zero tests of any kind; verify pass found only 3 of those actually
  self-dedupe (the dedup-correctness risk), the other 8 are a plain coverage gap —
  downgraded to MINOR, with one named example (FAERS drug) corrected as a false
  positive (it does have a test).

---

## 6. Live output-layer spot-check — mart keys + THE_LIBRARY (full census, not a sample)

**Grade impact: severe**

- **12 of 254 THE_LIBRARY public views (4.7%) throw a hard SQL error on open** — SEVERE.
  Ran a compile-only probe against all 254, not a sample. Two mechanisms: (1) 10
  views have a frozen column list from creation time; the source table has since
  gained/lost columns, so Snowflake refuses the query (e.g. `NURSING_HOMES` declares
  98 columns, source now produces 97). (2) 2 views point at a landing table name
  that was renamed and never repointed (`CREDIT_UNION_CALL_REPORTS` ->
  `FED_NCUA_CALL_REPORTS_FS220`, `AIRCRAFT_REGISTRY` -> `FED_FAA_AIRCRAFT_REGISTRY`;
  data exists under the new name in both cases). Affected topics: nursing homes,
  individual campaign donations, outside spending, FBI crime incidents, pollution
  enforcement, tribal lands, revolving-door appointees, CDC mortality queries,
  hospital cost reports, veteran mortality, credit unions, aircraft registry.

- **DEA ARCOS opioid-shipment table (178.6M rows, 2nd-largest mart table) has no
  usable per-row key** — SEVERE. `TRANSACTION_ID` has only 11,678,713 distinct
  values across 178,598,026 rows (~15x average repeat, 0 nulls). Value '30' repeats
  5,356 times across unrelated shipments (different drugs, buyers, years). Tested
  a 7-column compound key as a fallback: still only 99.998% unique (3,841 true
  collisions) — there is no clean surrogate key anywhere nearby.

- **2 THE_LIBRARY views run clean but hold placeholder junk, not real records** — MODERATE.
  `JUSTICE.FRAUD_SETTLEMENTS` (12 rows) is scraped DOJ webpage nav-menu text, not
  settlement records. `COMPANIES.BENEFICIAL_OWNERSHIP_REGISTRY` (1 row) is the
  literal string "ACCESS RESTRICTED..." stored as if it were a data record.

- **EPA drinking-water VIOLATION_ID: null on 1M rows, not unique on the rest** — MODERATE.
  15,432,737 rows, only 2,323,774 distinct VIOLATION_ID, 1,002,550 (6.5%) NULL.
  Confirmed inherent to the EPA source extract itself (violation x enforcement
  grain), not a Ripple ingestion bug — usable once the grain is understood, not
  corrupting anything by itself.

- 2 more "ID-shaped" columns (Part D `NPI`, UK Companies House `COMPANY_NUMBER`) are
  legitimate dimension keys, not row keys, by design — flagged as a join trap for
  awareness, not a bug. MINOR.

- **3 of the biggest, most central mart tables are fully clean** — INFO, the
  counter-evidence: FEC individual contributions (283.8M rows, `SUB_ID` 100% unique,
  0 nulls — largest mart table in the warehouse), CMS Open Payments (15.4M rows,
  `RECORD_ID` 100% unique), federal civil docket / FJC IDB (10.9M rows,
  `CASE_RECORD_ID` 100% unique). 310M rows combined, no surprises.

---

## Fix list, roughly ordered by blast radius

1. FEC MEMO_CD filter — add to both dbt marts and `build_giant_aggs.py`'s public
   aggregate tables; rebuild the stale 84M-vs-283M-row aggregate.
2. Repoint `stg_fed_bjs_data` and `stg_intl_hudoc` to their existing `_FULL` landing
   tables; drop/mark the dead `FED_SAM_EXCLUSIONS` capped copy.
3. Repoint the 12 broken THE_LIBRARY views (10 need a column-list refresh, 2 need a
   table-name fix) — all mechanical, data already exists.
4. Give ARCOS a real per-row surrogate key (or clearly document there isn't one) and
   add a caveat to any query/finding logic touching it.
5. Fix `health__fed_cms_pos_other`'s bare `try_to_number` — reuse the existing
   guarded staging model instead of re-casting raw; recur across the other 27
   similarly-generated marts.
6. Repoint the USASpending timeline layer to `_FULL_R2`; add a cap caveat to
   assistance_full and contracts_full descriptions; correct the stale registry notes.
7. Add a floor/suppression caveat to the Part B service-level mart and DME
   by-referrer/supplier marts (the DME one already feeds a published finding).
8. Add per-load key re-proof (same mechanism as the staging fix) to the 6
   untestable-unique marts/intermediate models.
9. Drop the 7 zombie renamed-away staging views; document or drop the frozen
   `DBT_CROGERS_RIPPLE` schema copy.
10. Delete/replace the 2 junk THE_LIBRARY views (FRAUD_SETTLEMENTS, BENEFICIAL_OWNERSHIP_REGISTRY).

None of this requires a rebuild or new architecture — every item above is a targeted
SQL change, a repoint, or a test addition against tables that already exist and are
already correctly loaded somewhere in the warehouse.

---

## Fix round, same day — code-side status

Chris said "Go. I want at least 95/100." Two waves of parallel fix agents (14 total)
plus direct edits closed the code-level side of every item above. Hard rule the whole
way: file edits only, never `dbt run`/`build`/`--apply`, never a warehouse write —
everything verified via `dbt parse`/`dbt compile` and read-only Snowflake queries.

**Wave 1** (6 agents): FEC memo filter + flag, USASpending timeline repoint to the
corrected `_r2` mart, 5 health-trap caveats, BJS/HUDOC repoint to their `_FULL`
landing tables, 6 untestable-unique-test fixes. A skeptic pass (fresh-context,
adversarial) checked this wave and found the bare-cast rounding fix was scoped wrong —
it used a 139-file population instead of the real 206, so only 96 were actually fixed,
not the claimed 110. Skeptic also confirmed: zero warehouse writes happened (three
independent proofs), every live number re-checked came back exact, and the FEC
committee-to-candidate mart still had `stg_int` truncating a dollar-amount column,
and the FEC individual-contributions mart's two casts were invisible to the original
sweep (it reads `ref()`, not `source()`).

**Closed directly, by hand:** FEC individual-contributions mart's `transaction_date`/
`transaction_amt` casts (now `stg_date`/`stg_float`), FEC committee-to-candidate's
`transaction_amt` (`stg_int` → `stg_float`, so a future decimal load keeps the cents
instead of losing them), a stale row-count comment on the SAM exclusions mart, a
misleading percentage-denominator comment on the CMS POS-other mart. The skeptic's
"missing CHOW caveat" finding turned out to be a false alarm on re-check — the
caveat is there, just phrased without the literal abbreviation "CHOW".

**Wave 2** (8 agents): fixed the real remaining 123 generator-style marts with
unguarded casts (674 individual bare-cast call sites), organized by domain
(environment x2, health x2, justice x2, finance, economics+labor+uncategorized).
Re-verified independently afterward (not by the agents — by re-running the same
detection method myself): of 10 files the detector still flagged, all 10 turned out
to be false positives — guarded expressions that still contain the literal
`try_to_date(`/`try_to_number(` substring inside their own guard. One minor,
non-corrupting inconsistency remains: the three OSHA case-detail year-marts
(2023/2024/2025) each handle `DATE_OF_DEATH` slightly differently (macro, explicit
format, or left as text) — no misparse risk in any of the three, just not identical.

**Full-project `dbt compile` after both waves: 9,727/9,727 succeeded.** 270 files
touched across the whole session, all git-tracked, zero warehouse writes.

## Live rebuild — Chris ran `scripts/run_fix_rebuild.ps1`, 2026-09-20

**Result: 892 steps | 791 success | 20 warn | 42 error | 39 skipped, 12m 7s.**
The 42 errors split cleanly into two causes, both measured live before naming them:

1. **13 politics marts BLOCKED by the project's own standing guard** (`macros/guard_politics_mirror.sql`):
   these are dbt mirrors of Python-built canonical POLITICS tables reconciled against
   OpenFEC/GovTrack, and the guard refuses a dbt rebuild so untested SQL can't overwrite
   audited numbers. Correct by design, not a failure. The 39 "skipped" are their tests.
   Consequence: the cast-guard edits to those 13 politics files are moot at the live layer —
   dbt isn't what serves that data. Nothing to fix; noting so nobody chases it.

2. **29 `not_null` tests failed, all one mechanism — blank strings, not lost data.** Checked
   the raw landing values live for the worst offenders: `FED_CMS_POS_OTHER.MEDICARE_MEDICAID_PRVDR_NUMBER`
   is `''` on all 44,429 rows; `FED_NOAA_WEATHER_API.STATION_ID` is `''` on all 287 rows;
   `INTL_EU_SANCTIONS.ADDR_NUMBER` is `''` on all 42,347 rows; `FED_DOL_FORM5500.TYPE_PENSION_BNFT_CODE`
   is `''` on exactly 16,428 rows — the failing count to the row; `FED_USGS_MINERALS.MRDS_ID`
   is `''` on exactly 150,804 rows. These columns were always empty. The old tests passed only
   because a blank string is not NULL. The guarded casts now read a blank as a real NULL —
   the cast is right, the tests were asserting something that was never true. Same trap as
   the NPPES EIN column (memory: non-null reads 100% because the value is an empty string).
   Verified no alphanumeric IDs were destroyed: `mrds_id`/`mas_id` are plain passthroughs
   (values like `M013595` survive); the form5500 code column's real values (`2E2G2R3D`) were
   untouched — only the blanks flipped. The 3 HUDOC failures (country 4, appno 57, ecli 2,334)
   are a different flavor of the same thing: tests calibrated on the old 2,000-row capped
   sample, now running against the real 211,778 rows, which have genuine source nulls.
   **The tables themselves built fine — live data is correct. Only the test expectations are stale.**

   Proposed fix (needs Chris's go — the auto-mode classifier blocked me from editing tests):
   downgrade exactly those 29 `not_null` tests to `severity: warn`, with a one-line note on
   each saying the column is blank in source. The 10 yml files: staging/intl_hudoc/schema.yml,
   schema_fed_dol_form5500, schema_fed_noaa_weather_api, schema_fed_usgs_minerals,
   schema_fed_cms_pos_other, schema_fed_cms_medicare_provider, schema_intl_eu_sanctions,
   schema_fed_nursinghome411, schema_fed_cms_hospice, schema_fed_noaa_storm_events.

   **Done 2026-09-20 (Chris said "keep going"):** all 29 downgraded to `severity: warn` with a
   one-line reason on each. Verified by running it: `dbt test` on the 10 affected models ->
   56 tests, 24 pass, 32 warn, **0 errors**.

3. **Public catalog re-censused after the rebuild: still exactly the same 12 broken views** —
   the rebuild added columns to several marts and broke nothing new.

## The 12 broken THE_LIBRARY views — `scripts/repair_library_views.py`

Dry-run by default; `--apply` saves rollback DDL to `outputs/` first, keeps each view's
catalog COMMENT, uses COPY GRANTS + explicit re-grant, and compiles every rewritten body
against the warehouse before changing anything. A view whose declared column names don't
match what its body really outputs is skipped, not guessed at. Dry-run result:

**7 ready (compile clean, comment kept):** INDIVIDUAL_DONATIONS (list 15 -> data 18: gained
CYCLE_FILE, MEMO_CD, IS_MEMO_TRANSACTION), OUTSIDE_SPENDING (23 -> 26), POLLUTION_ENFORCEMENT
(42 -> 44), REVOLVING_DOOR_APPOINTEES (46 -> 44), HOSPITAL_COST_REPORTS (125 -> 126),
NURSING_HOMES (98 -> 97: NPI left the mart), AIRCRAFT_REGISTRY (renamed table swapped in,
37 = 37).

**5 skipped — not drift, the source was reloaded in a different shape:**
FBI_CRIME_INCIDENTS (21 declared names absent from `FED_FBI_CDE`), TRIBAL_LANDS_GEO (11),
CDC_MORTALITY_QUERIES (13), VETERAN_MORTALITY_APPENDIX (6), CREDIT_UNION_CALL_REPORTS (the
renamed `_FS220` table has no `ACCT_CODE` — it is a wide form, the view expects a long one).
A blind `select *` would open, but it would serve different data under a catalog description
written for the old columns. Each needs a new projection written against the current table.

**Still open, needs Chris:**
1. The FEC committee-to-candidate public aggregate (`build_giant_aggs.py`) can't be
   rebuilt as-is — its grain is now 163,388 distinct combos, over the script's own
   100k-row cap (raised by the 2-cycle → 14-cycle reload). Needs a design call:
   coarser grain, a raised cap, or a different rollup shape.
2. Every fix above needs an actual `dbt build`/`dbt run` to take effect in Snowflake.
   Real cost, from the query log: effectively $0 (X-Small warehouse, sub-second
   runs historically). Still a shared-state write under this project's rules — needs
   Chris's go, not an agent's.

## Afternoon round, 2026-09-20 — public shelf repair and two timestamp fixes

**What was checked:** every THE_LIBRARY view and every LIBRARY_MARTS.TIMELINE view opened with a
real one-row fetch through the Python door. A hit means the view either fails to compile or
holds a value the Python client cannot read. A miss means it compiles and the first row converts;
it cannot prove a later row converts.

- `scripts/repair_library_views.py --apply` repaired 7 public views. Rollback DDL:
  `outputs/library_view_rollback_2026-09-20.sql`. **The rollback file uses unqualified view names.
  Qualify each with THE_LIBRARY.<schema> before running it.**
- The true before-count was 13, not 12. The morning probe was compile-only and could not see
  `HEALTH.BANNED_HEALTHCARE_PROVIDERS`, whose `_INGESTED_AT` read year 56,656,460 on all 83,816 rows.
  Cause: landing `FED_HHS_OIG_LEIE.INGESTED_AT` is NUMBER epoch micros and staging ran a bare
  `to_timestamp_ntz`. Fixed in `stg_fed_hhs_oig_leie__exclusions.sql` with `landing_parse_audit_epoch`.
  Verified after rebuild: 83,816 rows, one value, 2026-08-27 15:03:47, fetches clean.
- 30 staging files share that bare cast. Landing types checked live: 28 are ISO text, 1 is a real
  timestamp, only LEIE is a raw number. No other file needed the change.
- Skeptic catch: Snowflake stores a `select *` view with its column list expanded, so the repaired
  views can drift again. The script docstring claim "can't drift again" is false.
- Skeptic catch: grants after repair are RIPPLE_READER and CLAUDE_MCP_READONLY. No before-snapshot
  was taken, so a third role, if one existed, cannot be proven kept.
- TIMELINE shelf, 405 views: 5 errored. 4 were frozen column lists under marts that gained columns
  today (ARCOS, FEC individual, FEC committee-to-candidate, SDWA geographic areas); rebuilt with
  dbt, 6 of 6 models succeeded including `timeline__health_index`. The 5th,
  `ECONOMICS__FED_USASPENDING_CONTRACTS_FULL`, has `_LOADED_AT` at year 56,645,473 on all
  93,119,582 rows: the landing column `_INGESTED_AT` is itself a TIMESTAMP that took epoch micros
  as seconds. Fixed in `stg_fed_usaspending_contracts_full_r2__organizations.sql` by re-reading
  the epoch. The landing loader still writes it wrong on future loads.
- Still open on the public shelf, 5 views needing new projections: FBI_CRIME_INCIDENTS,
  TRIBAL_LANDS_GEO, CDC_MORTALITY_QUERIES, VETERAN_MORTALITY_APPENDIX, CREDIT_UNION_CALL_REPORTS.

## Evening round, 2026-09-20 — both timestamp fixes live, last 5 public views repaired

- dbt rebuilds ran: 4 frozen timeline views plus `timeline__health_index` and `timeline__warehouse`
  (6 of 6, 65s); USAspending R2 staging, mart, timeline (3 of 3 views, 15s). After: TIMELINE shelf
  405 of 405 open; USAspending `_LOADED_AT` 0 of 93,119,582 rows past year 9999, 0 null, range
  2026-08-23 14:45:28 to 2026-08-25 15:21:17. Skeptic confirmed the micros reading against the
  tables' own CREATED stamps: LEIE 10 seconds apart, USAspending 4 seconds apart.
  `timeline__health_index` 139,557 rows, up from 132,735 in the 2026-09-06 snapshot table.
- `scripts/repair_library_views_reshaped.py --apply` repaired the last 5 public views by pointing
  them at cleaned marts. Two were 1-row stubs when the friendly layer was built 2026-07-12 and hold
  real data now, so they were renamed with `alter view rename`, never a drop:
  FBI_CRIME_INCIDENTS -> FBI_CRIME_STATE_MONTHLY, CDC_MORTALITY_QUERIES -> CDC_MORTALITY_BY_CAUSE_AND_SEX.
  The same names and comments were written to `LIBRARY_META.REGISTRY.FRIENDLY_LAYER` (5 rows,
  still 251 total) and `outputs/thelibrary_content.json`. Rollback plus friendly-layer before-rows:
  `outputs/library_view_rollback_reshaped_2026-09-20.sql`.
- FBI check before trusting the mart: landing 477,360 rows, one run id, grain fully distinct;
  mart 238,680 because it sets OFFENSES and CLEARANCES side by side. 238,680 x 2 = 477,360.
- CREDIT_UNION_CALL_REPORTS now reads the FS220 wide form, 4,336 rows, 249 columns. Claude's pick.
- After: THE_LIBRARY 254 of 254 views open with a real one-row fetch. Started the day at 13 broken.

### Skeptic pass on the 5-view repair — DISAGREE on two claims, both verdicts recorded

Holds: 254 of 254 open; FBI, CDC, VA, BIA comments true phrase by phrase; no rows hidden (FBI pivot
sums match to the unit: OFFENSES 846,949,378, CLEARANCES 168,442,694; other four marts 1:1 with
landing); grants kept on all 5; no live object still uses the two old names.

Broken, claim "the rename survives a refresh": `thelibrary_build.py` looks a name up by the
inventory key, which is the MART fqn; the names file was keyed by LANDING fqn. Fixed locally by adding
5 mart-keyed entries to `outputs/thelibrary_content.json`. NOT proven against a real refresh.
Bigger and older than this repair: the names file covers 35 of 428 inventory keys (inventory file
dated 2026-07-29, 421 mart keys; names file 171 landing keys). A `thelibrary_refresh.py --apply` today
would fall back to physical mart names for most of the shelf, prune the friendly names as orphans,
and `CREATE OR REPLACE` the FRIENDLY_LAYER table. Do not run it until the keys are reconciled.

Broken, claim "rollback is saved": the file is a record, not a runnable undo. The 5 before-views
already errored on open, one source table no longer exists, and the DDL has no COPY GRANTS. A
READ FIRST header now says so and gives the two rename-back statements, the only meaningful undo.

Wrong phrase, fixed live: the credit union comment said join to the credit union list on CU_NUMBER.
That list is keyed by CHARTER_NUMBER. The FOICU table joins 4,336 of 4,336 on CU_NUMBER. Comment and
FRIENDLY_LAYER row corrected; also now says the table holds one cycle date, 2026-03-31.

### Shelf refresh key reconcile — local files only, no warehouse write

What was checked: `thelibrary_inventory.py` re-run (read-only, 764 datasets: 689 marts, 75 landing), then
the builder's naming and prune logic replayed in Python against the 254 live THE_LIBRARY views. A hit
means a live view keeps its schema and name through a refresh. A miss means the refresh drops it.

- Cause of the key mismatch: the builder looks a name up by inventory key, which is the MART fqn; the
  names file was mostly keyed by LANDING fqn. Before: 51 of 764 inventory keys had a names entry.
- Fix: for each of the 251 live FRIENDLY_LAYER rows, wrote a names entry under its inventory key, using
  the live table as the truth. Matched 60 by same key, 177 via landing name, 4 via table name,
  2 by hand (NCUA to FS220, FAA to the renamed aircraft registry). After: 243 of 764 keyed.
  Backups of both files from before this step sit in the session scratchpad.
- 8 live views have no home in the inventory, so a refresh would drop them: BANK_CALL_REPORTS 302 rows,
  FDIC_ENFORCEMENT_ACTIONS 14, DOJ_CIVIL_RIGHTS_CASES 1, JAPANESE_INTERNMENT_RECORDS 36, SWISS_COMPANIES 18,
  GREEK_COMPANIES 40, MONEY_LAUNDERING_COUNTRY_RATINGS 200, HHS_GRANT_AWARDS 0. All tiny landing samples.
- Replay result AFTER the fix. A refresh would build 771 views against 254 live. 159 live views keep
  schema and name. 75 live views get dropped as orphans, and 83 names reappear under a DIFFERENT topic
  schema, because the inventory re-derives the topic from the mart schema (CAMPAIGN_FINANCE to
  INVESTIGATIONS, COMPANIES to ECONOMY, ELECTIONS to GOVERNMENT, ENERGY_ENVIRONMENT to INVESTIGATIONS).
  612 views would be brand new; 521 of those fall back to the raw table name because no friendly
  content was ever generated for them.
- So the names are reconciled, the shelving is not. Still: do not run `thelibrary_refresh.py --apply`.

### Shelf builder patched to keep a live view on its shelf — file edits only

`scripts/thelibrary_build.py`: new `load_live_shelves()` reads the live FRIENDLY_LAYER and a dataset that
already sits on the shelf keeps its schema and domain. Match order: object_fqn, landing_fqn, then
unique friendly name, which catches a renamed landing table (NCUA, FAA). Orphans are now listed in
PREVIEW too, and removing one needs `--apply` AND a new `--prune` flag; before, `--apply` alone removed them.

Builder preview after the patch, nothing written: 771 datasets, 244 of 254 live views keep shelf and
name, 527 brand-new, 9 would be orphaned, START_HERE is rebuilt on its own. The 9: GREEK_COMPANIES,
SWISS_COMPANIES, JAPANESE_INTERNMENT_RECORDS, DOJ_CIVIL_RIGHTS_CASES, FDIC_ENFORCEMENT_ACTIONS,
BANK_CALL_REPORTS, MONEY_LAUNDERING_COUNTRY_RATINGS, all tiny landing samples the inventory skips, plus
two hand-built views that were never in FRIENDLY_LAYER: FEDERAL_CONTRACTS_BY_AWARD and
PHARMA_PAYMENTS_TO_DOCTORS_ALL_YEARS. Before the patch the same replay moved 83 and orphaned 75.
Still open: 521 datasets have no friendly content, so a refresh would shelve them under raw table names.
Skeptic pass on the patch was launched; verdict to follow.

### Skeptic pass on the builder patch — DISAGREE, both verdicts recorded

Holds: a no-flag run writes nothing (FRIENDLY_LAYER still 251 rows dated 2026-07-12 after a preview);
244 kept + 9 orphans + START_HERE = 254; the two views renamed today survive with shelf, name, table and
comment intact; the apply path compiles and its control flow is right.

Broken, claim "no live view is silently repointed": keeping the SHELF does not keep the BODY.
- 33 of the 244 kept views would read a different table. 27 go landing to their own mart, same dataset,
  but column names and types differ. 4 go to a mart in the dev schema DBT_CROGERS: INTRA_AMERICAN_SLAVE_VOYAGES,
  FEDERAL_REGISTER_DOCUMENTS, AG_MULTISTATE_SETTLEMENTS, FRAUD_SETTLEMENTS. 2 swap a curated mart for raw
  landing: CONGRESS_ROLLCALL_VOTES (POLITICS__VOTEVIEW_ROLLCALLS to FED_VOTEVIEW_ROLLCALLS) and
  FOREIGN_AGENT_REGISTRATIONS (FOREIGN_INFLUENCE__FED_FARA_BULK to FED_FARA).
- 113 of the 244 are typed projections today, not plain select-star. A refresh without `--typed`
  rewrites all 113 as select-star and loses every cast.
Half broken, claim "the name fallback cannot mis-shelve": it fires 6 times today, each time onto a
different physical object than the registry row (NCUA to FS220, FAA to the renamed registry, four
DBT_CROGERS to real-schema pairs). No name collision results. Skeptic's view: a friendly name is a label,
not an ID, so require source_id to match too. Claude's view: those 6 are exactly the renamed sources the
fallback was written for, and the name was assigned on purpose in the names file; requiring source_id
would send NCUA and FAA back to the wrong shelf. Chris decides.
Also noted: the shelf-keeper reads the 2026-07-12 registry snapshot, not the live views; drift is 2 views today.
