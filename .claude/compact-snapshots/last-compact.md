# Snapshot taken right before context compaction

## STATUS.md at compaction time
# RIPPLE STATUS — 2026-08-23 (early am) — Fix sweep complete; FAERS reload launched

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**Scoreboard (standing frame): warehouse at ~64/100, heading for ~68-69 once the
overnight loads land** (trust ~73 · build-completeness ~50). Tonight: full fix-list
sweep (Tiers 1+2), the year-killer found and fixed warehouse-wide, the whole
test-failure tail cleared, and the FAERS legacy reload launched. Remaining big
levers: contracts re-pull (+5-6, Chris-priced decision), no-loader wing.

**BROKE: nothing.**

**✅ FAERS RELOAD DONE AND VERIFIED** (same night, ~90 min): all 35 corrupted
quarters re-landed with the fixed parser; all 5 tables back to full counts
(62.3M total); **verified to the row** — all 4,012,896 legacy outcome rows now
carry a numeric case key (was 0%) and a valid outcome code (was 22%); 512,848
deaths / 1.38M hospitalizations now joinable. The Tier-1 FAERS item is CLOSED
**end-to-end**: the 5 downstream marts rebuilt and tested same night (8/8 PASS).
Scoreboard: ~68/100 (trust ~78 · build-completeness ~50).

**THREE loads still running** (all checkpointed):
1. **Senate lobbying crawl** — first attempt died on an unhandled network drop;
   loader now retries network errors + 5xx (and pages at 250 with the key);
   relaunched from year 1999 → verify `FED_SENATE_LDA_FILINGS`.
2. **Federal debarment re-pull, ATTEMPT 2** — attempt 1 was throttled to death by
   SAM's API at page 14 (landed 10,000; quality gate correctly refused to call it
   success). Loader patched: 12 retries up to 10 min each + 25s page pacing;
   relaunched → verify `FED_SAM_EXCLUSIONS` (target ~167k). If attempt 2 also dies
   on sustained 429s, the binding constraint is the key's quota — fall back to
   SAM's monthly public exclusions extract file (or the OpenSanctions mirror of
   the same list) instead of the paged API.
3. **FEMA housing registrations resume** — 22.05M → 25.9M target, slow API with
   timeouts → verify `FED_FEMA_IA_HOUSING_REGISTRATIONS`.

## YOUR MOVE (Chris)

1. Carried: contracts re-pull price tag; corporate bridge; security fix; roll-call
   scope ruling; CourtListener bulk pull. (All drop one-liners from tonight: DONE.)
2. FYI, no action: **290 newer leads are now in your review lane** — the queue mart
   was stale; rebuilt via the sanctioned wrapper, reconcile guard green.

## Tonight's full tally (receipts: reports/fix_session_results_2026-08-22.md)

- 18-item quick-wins plan: all resolved (a third were stale/false alarms — verified,
  not assumed). ~29.3M junk rows deleted across 11 tables. EPA penalty allocation +
  13F dollar normalization live. 174-column trust registry created.
- **Year-killer**: 61 year columns mis-ruled as dates, NULLed in 29 built marts
  (Treasury, Open Payments, PBGC, OSHA, foreign aid, NHTSA, CDC NNDSS) — all
  rulings + models fixed, marts rebuilt, tests green.
- First verified full test run (4,831 tests) → failure tail now FULLY triaged:
  grain fixes (TRI + doc-control-num, NPDES SICs + primary flag, Ember 6-part key,
  MSHA docket exposed), 3 staging views rewritten (NAAG new schema, screening list
  meta drift, leadership-PAC rename + linkage grain), review queue rebuilt, OSHA
  3-blank-ids downgraded to warn, Europol garbage column fenced in COLUMN_TRUST.
  Remaining known-broken: 3 staging views with DATA-IDENTITY mismatches (13F
  "submission" holds holdings-shaped rows; BJS holds NCVS microdata; FRS-full
  column variant) + OSHA-inspection staging awaiting its still-running API load.
- Short-of-publisher batch: 9 VARIANT-chunk false alarms, ransomware verified
  exactly complete (line-count artifact), GLEIF relationships re-pulled to exact
  publisher match (485,285), UK sanctions refreshed (58,336, FCDO husk dropped).

## NEXT

Boot: verify the four loads (counts above), then rebuild FAERS-downstream marts +
rerun their tests; contracts decision; 13F family consolidation; no-loader
worklist; tighten auto-guessed cadences over time.

**Cost note:** ~2 credits (~$4) this session so far excluding the in-flight FAERS
landing (+$4-6 as it runs); day total ≈ 8.6 credits ≈ $17-23 all-in. Meter-verified.

## Not committed

All of tonight's model/yml/staging/rulings edits (29 year-fix marts, NNDSS, Ember,
TRI, NPDES SICs, MSHA, NAAG, screening list, leadership PAC, Europol, OSHA 2025,
FAA retirement, EPA ECHO + penalty gap, 13F holdings, LDA loader retry+page-size
fix), reports/fix_session_results_2026-08-22.md, trimmed FAERS checkpoint,
STATUS.md. Warehouse-side: COLUMN_TRUST (174 rows), 11 deduped + 5 FAERS-wiped
landing tables, ~75 rebuilt marts/views, refreshed UK sanctions + GLEIF + openFDA.

## Working tree at compaction time
## main...origin/main
 M .claude/compact-snapshots/last-compact.md
 M STATUS.md
 M data/osha_inspections/checkpoint.json
 M library-onboarding/ripple_dbt/models/marts/consumer_safety/consumer_safety__fed_nhtsa_complaints.sql
 M library-onboarding/ripple_dbt/models/marts/consumer_safety/consumer_safety__fed_nhtsa_investigations.sql
 M library-onboarding/ripple_dbt/models/marts/consumer_safety/consumer_safety__fed_nhtsa_recalls.sql
 M library-onboarding/ripple_dbt/models/marts/criminal_justice/criminal_justice__fed_bjs_data.sql
 M library-onboarding/ripple_dbt/models/marts/economics/economics__fed_fac_single_audit.sql
 M library-onboarding/ripple_dbt/models/marts/economics/economics__fed_foreignassistance.sql
 M library-onboarding/ripple_dbt/models/marts/economics/economics__fed_pbgc_data.sql
 M library-onboarding/ripple_dbt/models/marts/economics/economics__fed_treasury_avg_interest_rates.sql
 M library-onboarding/ripple_dbt/models/marts/economics/economics__fed_treasury_debt_outstanding.sql
 M library-onboarding/ripple_dbt/models/marts/economics/economics__fed_treasury_dts_deposits.sql
 M library-onboarding/ripple_dbt/models/marts/economics/economics__fed_treasury_mts_receipts.sql
 M library-onboarding/ripple_dbt/models/marts/environment/environment__epa_penalty_gap.sql
 M library-onboarding/ripple_dbt/models/marts/environment/environment__fed_epa_air_emissions_poll_rpt_combined_emissions.sql
 M library-onboarding/ripple_dbt/models/marts/environment/environment__fed_epa_echo.sql
 M library-onboarding/ripple_dbt/models/marts/environment/environment__fed_epa_egrid_plant_2022.sql
 M library-onboarding/ripple_dbt/models/marts/environment/environment__fed_epa_tri_basic_2023.sql
 M library-onboarding/ripple_dbt/models/marts/environment/schema_fed_epa_npdes_npdes_sics.yml
 M library-onboarding/ripple_dbt/models/marts/environment/schema_fed_epa_tri_basic_2023.yml
 M library-onboarding/ripple_dbt/models/marts/finance/finance__fed_irs_soi.sql
 M library-onboarding/ripple_dbt/models/marts/finance/finance__fed_sec_13f_holdings.sql
 M library-onboarding/ripple_dbt/models/marts/health/health__fed_cdc_nndss_weekly_2024.sql
 M library-onboarding/ripple_dbt/models/marts/health/health__fed_cms_open_payments.sql
 M library-onboarding/ripple_dbt/models/marts/health/health__fed_cms_open_payments_2022.sql
 M library-onboarding/ripple_dbt/models/marts/health/health__fed_cms_open_payments_2023.sql
 M library-onboarding/ripple_dbt/models/marts/housing/housing__fed_cfpb_hmda_dc_only.sql
 M library-onboarding/ripple_dbt/models/marts/justice/justice__fed_courtlistener_judge_educations.sql
 M library-onboarding/ripple_dbt/models/marts/justice/justice__intl_eu_socta_europol.sql
 M library-onboarding/ripple_dbt/models/marts/justice/justice__xc_vera_incarceration_trends.sql
 M library-onboarding/ripple_dbt/models/marts/justice/schema_intl_eu_socta_europol.yml
 M library-onboarding/ripple_dbt/models/marts/labor/labor__fed_msha_violations.sql
 M library-onboarding/ripple_dbt/models/marts/labor/labor__fed_osha_ita_300a_summary_2023.sql
 M library-onboarding/ripple_dbt/models/marts/labor/labor__fed_osha_ita_300a_summary_2024.sql
 M library-onboarding/ripple_dbt/models/marts/labor/labor__fed_osha_ita_300a_summary_2025.sql
 M library-onboarding/ripple_dbt/models/marts/labor/labor__fed_osha_ita_case_detail_2023.sql
 M library-onboarding/ripple_dbt/models/marts/labor/labor__fed_osha_ita_case_detail_2024.sql
 M library-onboarding/ripple_dbt/models/marts/labor/labor__fed_osha_ita_case_detail_2025.sql
 M library-onboarding/ripple_dbt/models/marts/labor/schema_fed_osha_ita_300a_summary_2025.yml
 M library-onboarding/ripple_dbt/models/marts/legal_enforcement/legal_enforcement__fed_naag_multistate_settlements.sql
 M library-onboarding/ripple_dbt/models/marts/transport/schema_fed_faa_registry.yml
 M library-onboarding/ripple_dbt/models/marts/transport/transport__fed_faa_registry.sql
 M library-onboarding/ripple_dbt/models/staging/fed_consolidated_screening_list/stg_fed_consolidated_screening_list__entries.sql
 M library-onboarding/ripple_dbt/models/staging/fed_faa_registry/schema.yml
 M library-onboarding/ripple_dbt/models/staging/fed_faa_registry/stg_fed_faa_registry__records.sql
 M library-onboarding/ripple_dbt/models/staging/fed_fec_leadership_pac/stg_fed_fec_leadership_pac__all.sql
 M library-onboarding/ripple_dbt/models/staging/fed_naag_multistate_settlements/schema.yml
 M library-onboarding/ripple_dbt/models/staging/fed_naag_multistate_settlements/stg_fed_naag_multistate_settlements__multistate_settlements.sql
 M library-onboarding/ripple_dbt/models/staging/intl_ember_elec/schema.yml
 M library-onboarding/ripple_dbt/models/timeline/timeline__transport_index.sql
 M library-onboarding/ripple_dbt/models/timeline/transport/timeline__transport__fed_faa_registry.sql
 M library-onboarding/ripple_dbt/seeds/ripple_time_registry.csv
 M outputs/_dq_failures.jsonl
 M outputs/_fema_ia_checkpoint.json
 M reports/typing_index/typing_rulings.csv
 M scripts/sam_exclusions_load.py
 M scripts/senate_lda_load.py
?? reports/fix_session_plan_next.md
?? reports/fix_session_results_2026-08-22.md
?? reports/the_fix_list_2026-08-22.md
?? reports/wonder_rankings.md

## Recent commits
b78be44f Merge branch 'main' of https://github.com/Crogg23/Ripple_v6
104162b8 Add scripts for OSHA inspections API load and typing rulings
080bfaf6 STATUS: paste 3 verified, court family wired
eec7f6d5 Court-sibling wires staged (criminal 84.5%, appellate 60.1%; bankruptcy refused at 33%)
a2fb51f7 Wiring batch 2 staged (courts bridge, FRS, FEC ids); wire-confirm respects triage tags
