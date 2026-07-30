<!-- GENERATED FILE. DO NOT EDIT BY HAND.
     Source: LIBRARY_META.BUILD  |  Generated: 2026-07-30T20:45:11Z
     To change anything here, change the row and regenerate:
     python3 scripts/gen_build_state.py --write -->

# Build State

**This file is a printout, not a diary.** Canonical truth: `SELECT * FROM LIBRARY_META.BUILD.V_BUILD_STATE;` (build) and `LIBRARY_META.REGISTRY.V_STATE` (data). Numbers below were live at generation.

## BUILD STATE (V_BUILD_STATE)
- actions_irreversible_pending: **1**
- actions_pending: **2**
- defects_blocker: **0**
- defects_open: **13**
- defects_unverified_7d: **13**
- parked_hot: **4**

## DATA STATE (V_STATE)
- catalog.orphans: 287
- catalog.sources: 2992
- connect.edges: 610
- connect.edges_inc: 1074
- connect.entities: 22623285
- decisions.total: 0
- landing.rows: 875575558
- landing.tables: 1937
- leads.banned_but_operating.active: 10
- leads.banned_but_operating.stale: 1
- leads.banned_but_paid.active: 773
- leads.debarred_but_funded.active: 2
- leads.excluded_but_billing.active: 236
- leads.osha_cohort_outlier_2024.active: 16215
- leads.sanctioned_vessel_broadcasting.active: 4
- leads.sanctioned_vessel_broadcasting_v2.active: 12
- leads.sec_filer_in_irs_bmf.active: 3
- marts.stale_vs_landing: 1
- reading_room.views: 252
- registry.sources: 2705
- taps.empty: 33
- taps.failed: 262
- taps.landed: 11
- taps.modeled: 346
- taps.queued: 7
- taps.sampled: 1577
- taps.scouted: 751
- taps.stale: 5

## OPEN DEFECTS

| sev | area | defect | last verdict | verified |
|---|---|---|---|---|
| high | ci | no ladder regression tests (5 named gaps, no holdout fixture) | clear | 2026-07-12 |
| high | creds | evidence.dev read lane is dark (dead interim token) | clear | 2026-07-12 |
| high | creds | no scoped write lane exists (reader-only PAT) | still_broken | 2026-07-12 |
| medium | creds | keys_ledger.json does not track the live PAT population | still_broken | 2026-07-12 |
| medium | creds | source API keys still missing from .env | still_broken | 2026-07-12 |
| medium | loader | append-mode loaders leave silent partial loads on crash | still_broken | 2026-07-12 |
| medium | politics | politics marts clobberable by selector-less dbt build | never verified | - |
| medium | truth_layer | landed/modeled sources whose landing table holds <=3 rows | still_broken | 2026-07-12 |
| medium | typing | landed/modeled sources with no staging view at all | still_broken | 2026-07-12 |
| medium | typing | staging views that are 100% TEXT | still_broken | 2026-07-12 |
| low | typing | THE_LIBRARY reading-room views still zero-cast | still_broken | 2026-07-12 |
| low | viz | explorer/overlay HTML pull Plotly from CDN, die offline | still_broken | 2026-07-12 |
| low | viz | leads_overlay.html stale (4 detectors/353 leads vs live 6/1030) | still_broken | 2026-07-12 |

Re-verify: `python3 scripts/verify_defects.py` — 'clear' is a recommendation; a human closes.

## RECENTLY CLOSED
- leaked/unrestricted ACCOUNTADMIN PATs still ACTIVE — closed 2026-07-27 by cortex_code
- resolve.py PAIRS spec broken by NPPES re-land (column rename) — closed 2026-07-27 by cortex_code
- V_CONNECTIONS_CORE (trustworthy-core view) does not exist — closed 2026-07-27 by cortex_code
- build-state.md is hand-typed, not generated — closed 2026-07-27 by cortex_code
- FED_FHFA_NMDB (19M rows) misgraded in catalog lifecycle — closed 2026-07-27 by cortex_code
- FED_IRS_EO_BMF is an exact 2x duplicate of FED_IRS_BMF — closed 2026-07-27 by cortex_code
- OP-2022 load mislogged: 13.25M rows live, ledger says error/0 — closed 2026-07-27 by cortex_code

## PENDING ACTIONS (dependency order)

| id | seq | action | flags | depends on |
|---|---|---|---|---|
| A00 | 0 | `(Snowsight, manual)` | HUMAN | - |
| A03 | 3 | `scripts/revoke_straggler_pats.py` | HUMAN IRREVERSIBLE | A00 |

Applied: A10 (2026-07-12 by chris (go 2026-07-12), agent-executed on bootstrap token); A09 (2026-07-12 by chris (go 2026-07-12), agent-executed on bootstrap token); A08 (2026-07-12 by chris (go 2026-07-12), agent-executed on bootstrap token); A11 (2026-07-12 by chris (go 2026-07-12), agent-executed on bootstrap token); A07 (2026-07-12 by chris (go 2026-07-12), agent-executed on bootstrap token); A06 (2026-07-12 by chris (go 2026-07-12), agent-executed on bootstrap token); A05 (2026-07-12 by chris (go 2026-07-12), agent-executed on bootstrap token); A04 (2026-07-12 by chris (go 2026-07-12), agent-executed on bootstrap token); A02 (2026-07-12 by chris (go 2026-07-12), agent-executed on bootstrap token); A01 (2026-07-12 by chris (go 2026-07-12), agent-executed on bootstrap token)

## PARKED IDEAS
- [IDEA — HOT] Land one new identifier (EIN wired, or CIK via User-Agent fix) | WHY: Breaks the 75%-of-leads-on-one-edge concentration. EIN is LANDED (see already_done row) but not wired into detectors; CIK needs RIPPLE_CONTACT_UA in .env first.
- [IDEA — HOT] Materialize connect__banned_but_operating as a dbt mart | WHY: First shippable story from the connected Library (crosswalk x LEIE).
- [IDEA — HOT] Per-watchlist FANOUT_MAX relax for small curated watchlists | WHY: FANOUT_MAX=40 kills junk but drops legit hospital->banned-provider hops (LEIE 8,775 NPIs).
- [IDEA — HOT] Tier-aware bridge dedup (weak GEO edge suppresses strong CCN->NPI bridge) | WHY: Fix: only dedup against equal-or-stronger-tier direct edges.
- [IDEA — SOMEDAY] Central sources.yml instead of per-model sources blocks | WHY: Cosmetic.
- [IDEA — SOMEDAY] Hide raw-vs-cleaned duplicate objects in the Reading Room | WHY: Ugly collision-suffixed names when both exist.
- [IDEA — SOMEDAY] Sketch EIN/NAICS/DOCKET/ZIP detector templates | WHY: Design-brief open call; engineering templates only, no new detectors built.
- [IDEA — SOMEDAY] Structurally exclude bare ZIP/FIPS edges from the graph (design call) | WHY: 52.2% of edges are ZIP-key at recon. OUT OF SCOPE for the govern brief — recorded so it stops living in prose.
- [IDEA — SOMEDAY] Vendor Plotly locally in explorer/overlay HTML | WHY: Tracked as an open viz defect too; file already on disk, just unwired.
- [IDEA — SOMEDAY] Wire the Library Map as 'ripple map' so it self-refreshes
- [IDEA — SOMEDAY] dbt deprecation sweep (148 generic-test-arg + 57 severity warnings) | WHY: Become errors on a future dbt major bump.
- [ALREADY_DONE] Pour IRS EO BMF (1.97M nonprofit EINs) | superseded by: defect 'FED_IRS_EO_BMF is an exact 2x duplicate' + action A04

## STANDING POLICY
- **agent_never_closes_defects** (2026-07-12): The verifier reports still_broken/clear; only a human sets STATUS/CLOSED_BY on a defect.
- **copy_grants_library_meta** (2026-07-06): Every CREATE OR REPLACE VIEW in LIBRARY_META carries COPY GRANTS.
- **fact_vs_lead** (2026-06-25): Same hard government ID across two sources = FACT. Shared name only = LEAD: human-review-only, never auto-merged, never stated as true.
- **foundation_before_detectives** (2026-06-29): Land+wire+catalog only; no new detector/lead/pattern work; publishing layer deferred.
- **no_selectorless_dbt_build** (2026-06-30): Never run a selector-less dbt build: POLITICS__* marts mirror Python-built canonical tables and a bare build clobbers them.
- **ordering_bridges_first** (2026-06-29): Crosswalk/bridge sources before domain spines; keyless-before-keyed; deterministic-before-agentic.
- **preview_then_apply** (2026-06-25): Every warehouse/catalog mutation ships as a preview-by-default script with --apply. The agent never executes DDL/DML against shared infra directly.
- **serve_surface_evidence_dev** (2026-07-06): SERVE surface is evidence.dev; serve/ (Streamlit) is legacy fallback.
- **source_scope_clean_public** (2026-06-27): Clean public sources only; paid/ToS-grey dropped or deferred to a specific story need.
- **trap_ais_snapshot** (2026-06-28): FED_NOAA_AIS is a stale 8-day snapshot: 58,106,517 rows spanning exactly 2024-01-01..2024-01-08. It pre-dates the 2025-26 sanctions wave — any 'sanctioned vessel in US waters' match off it is reverse-causality unless date-checked. Never draw it as a time series.
- **trap_leie_npi_and_dates** (2026-06-26): FED_HHS_OIG_LEIE: NPI='0000000000' on 74,780/83,464 rows (89.6%) — a naive NPI join merges them all into one 'doctor' (the libel trap). EXCLDATE needs explicit date parsing; TRY_CAST collapses to 1970.
- **trap_ofac_sdn_type** (2026-06-25): FED_OFAC_SDN.SDN_TYPE uses the literal sentinel '-0- ' (trailing space, 9,785 rows) for entities; also one empty-string row. Filter explicitly.
- **trap_open_payments_split** (2026-06-28): Open Payments is split across THREE landing tables (base 15.4M / 2022 13.25M / 2023 14.7M). Ad-hoc queries against one bare table under-count; the banned_but_paid detector already reads a unioned view.
- **trap_rlike_whole_string** (2026-06-25): Snowflake RLIKE/REGEXP match the WHOLE string: 'catalog' RLIKE 'cat' is FALSE. Wrap patterns in .*...* or catalog searches silently return zero rows.
- **trap_usaspending_grain** (2026-06-27): USASpending contracts are one row per TRANSACTION, not per award; a company fragments across child/parent UEIs (Lockheed: 77 child / 26 parent). Top-contractor rankings are floors, not truths.
- **v_state_numbers_only** (2026-07-02): Scale numbers are quoted only from V_STATE (data) / V_BUILD_STATE (build) or a live query. Prose numbers rot and are untrusted, including in this table.

## NEXT ACTION
A00: `(Snowsight, manual)`
