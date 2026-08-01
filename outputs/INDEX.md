# outputs/ — the filing cabinet

Dated reports, handoffs, audits, and generated artifacts from the build.
**Everything here is history, kept on purpose as a paper trail.** Nothing in
this folder is a current instruction, and no number in these files should be
trusted over `build-state.md`. For the living documentation, read
`docs/RIPPLE.md`.

Newest and most useful first, then by drawer.

## Start here if you're digging

- `PORTFOLIO_READINESS_AUDIT_2026-07-30.md` — the last full readiness audit
  before the cleanup sweep; the most honest recent picture.
- `HANDOFF_remediation_2026-07-30.md` — the punch list that drove the final
  July hardening sweep.
- `bug_dataquality_sweep_2026-07-30.md` / `portfolio_polish_sweep_2026-07-30.md`
  — what that sweep found and fixed.
- `FINDING_osha_cohort_2024.md` — the OSHA peer-cohort outlier finding (the
  detector that filled most of the lead queue).
- `CONNECTION_STRATEGY_2026-07-30.md` — how the connection graph is meant to
  grow next.

## Audits & health checks

`FABLE_AUDIT_2026-07-02.md`, `FABLE_AUDIT_2026-07-06.md`,
`GOVERN_RECON_2026-07-12.md` (+ `govern_recon_battery_2026-07-12.py`,
`govern_recon_results_2026-07-12.json`),
`DATA_AUDIT_AND_BACKFILL_PLAN_2026-07-23.md`,
`tap_health_audit_2026-07-05.html`, `tap_repairs_2026-07-05.{md,json}`,
`build_state_DIVERGENCE_2026-07-12.diff`, `SPRINT_VERIFY_2026-07-20.md`,
`RECEIPT_PARITY_2026-07-21.md`, `FEE_SCHEDULE_CHECK_2026-07-21.md`,
`pour_final_qa_2026-07-01.md`, `pour_readiness_REPORT_2026-07-01.md`.

## Handoffs & session briefs

`HANDOFF_connect_the_spine.md`, `HANDOFF_explain_ripple_2026-07-30.md`,
`SESSION_HANDOFF_2026-07-23.md`, `PROJECT_HANDOFF_STRATEGY_2026-07-12.md`,
`PLANE_handoff.md`, `POUR_HANDOFF.md`,
`INSTRUMENT_BUILD_HANDOFF_2026-07-03.md`,
`INSTRUMENT_HARDENING_{PLAN,HANDOFF}_2026-07-02.md`,
`INVESTIGATOR_TOOL_BRIEF_FOR_FABLE_2026-07-03.md`,
`ANALYSIS_SESSION_BRIEF_2026-06-27.md`.

## Build plans & runbooks

`BACKFILL_RUNBOOK_2026-07-23.md`, `POLITICS_BUILD_RUNBOOK.md`,
`POUR_GO_CHECKLIST.md`, `LAND_EVERYTHING_build_program_2026-06-27.md`,
`missing_data_BUILD_PLAN_2026-06-26.md`,
`library_org_BUILD_SPEC_2026-06-25.md`,
`library_organization_design_2026-06-25.md`,
`alexandria_foundation_BLUEPRINT_2026-06-28.md`,
`housekeeping_{PLAN,HARDENED}_2026-07-01.md`.

## Dataset frontier research (what to load next)

`ripple_frontier_MASTER_LIST.md` and rounds:
`ripple_frontier_datasets_2026-06-30.md`, `..._round2` → `..._round5`,
`ripple_nonobvious_investigations_2026-06-30.md`,
`deep_research_prompt_GAPS_2026-06-27.md`, `FABLE_KEY_HUNT_2026-07-22.md`,
`PATTERN_MAP_2026-07-21.md`.

## Politics domain research

`us_politics_coverage_audit_2026-06-30.md`,
`us_politics_dark_frontier_2026-06-30.md`,
`us_politics_load_stresstest_2026-06-30.md`,
`us_politics_tier1_tier2_STRESSTEST_2026-06-30.md`,
`us_politics_tier1_tier2_build_queue_2026-06-30.md`,
`politics_phase0_GAPS.md`.

## Detector calibration

`DETECTOR_CAL_battery_2026-07-13.md`,
`DETECTOR_CAL_innocent_explanations_2026-07-12.md`,
`detector_bunching_battery_2026-07-13.html`,
`detector_threshold_bunching_2026-07-12.html`, `LEADS_2026-07-08.md`,
`cohort_outliers_2024.csv`.

## Spine & connection engineering reports

`spine_backfill_report_2026-07-05.md`,
`spine_entity_backfill_report_2026-07-06.md`,
`spine_wiring_evidence.csv`, `spine_wiring_rejects.csv`,
`join_keys_std_backfill_report.md`, `join_key_tier_review.csv`,
`xref_bridges.csv`, `xref_rejects.csv`, `xref_sweep_log.txt`,
`match_eval.json`, `resolve_eval.json`, `calibrate.json`,
`discoveries_2026-06-27.md` (+ `_findings.json`),
`issue_coverage_SUMMARY_2026-06-27.md`, `issue_scout_DETAIL_2026-06-27.md`,
`_scout_de_silo_raw_2026-06-27.json`, `DR_SIZING_2026-07-20.md`,
`HOUR_DOSSIER.md`.

## Generated visuals & data (snapshots; may be stale vs the live warehouse)

`erd/` (entity-relationship diagrams per key type), `library_map.html`,
`library_map_2026-07-04.html`, `library_catalog_2026-07-06.html`,
`terrain_map.html`, `trail_atlas.html`, `trail_map.html`, `plane.html`,
`leads_overlay.html`, `ripple_dashboard.html`, `graph_nodes.csv`,
`library_inventory_2026-06-25.xlsx`, `plotly.min.js`, `mermaid.min.js`.

## Rollback snapshots & operational residue

`_rollback_*.sql` (pre-change SQL snapshots — keep; they're the undo
buttons), `_thelibrary_typed_views_plan_*.sql`, `_panel_jobs.jsonl`,
`pour_queue_keyless.json`, `wave1_specs.py`, `wave2_specs.py`,
`wave1_log.txt`, `wave2_log.txt`, `genall_log.txt`.
