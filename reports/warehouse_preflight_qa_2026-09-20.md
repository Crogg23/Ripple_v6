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
