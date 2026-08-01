# Library Snapshot

Generated at 2026-07-13 10:31 PDT · rerun with `python3 scripts/library_snapshot.py`

## The 2-minute version

You have **5 databases**, **45 schemas** (4 of them empty), **1,916 tables** and **1,292 views** in Snowflake, holding about **471.4M rows** in total. The most recent change to any of them was **2026-07-12**.

On the code side: **895 dbt models** (manifest.json (compiled dbt state)), **97 standalone Python scripts/entry points**, plus 118 more .py files inside 10 packages. Git is on `main` with **1 uncommitted change**.

Of everything in the warehouse, **879 objects are dbt-built** and **2,329 are not** (raw landing tables, agent-written meta, serve views). **9 flag(s)** need eyes — see the last section.

## Warehouse (Snowflake)

Audited as role `RIPPLE_READER` on warehouse `SERVE_WH` (user `CROGG23`). Row counts are metadata-based (INFORMATION_SCHEMA — real-time, no COUNT(*) scans; ACCOUNT_USAGE was not accessible to this role). Objects not granted to `RIPPLE_READER` are invisible to this audit — per CLAUDE.md, `LIBRARY_TOOLS` exists (MCP host, no data) but isn't visible here. System databases excluded from the breakdown but present: `SNOWFLAKE`, `USER$CROGG23`.

Empty schemas (exist but hold no tables/views): `LIBRARY_META.PUBLIC`, `LIBRARY_RAW.EPSTEIN`, `LIBRARY_RAW.PUBLIC`, `LIBRARY_STAGING.PUBLIC`.

| Database | Schema | Tables | Views | Rows (metadata) | Last altered |
|---|---|---|---|---|---|
| `LIBRARY_RAW` | `LANDING` | 1784 | 0 | 284.8M | 2026-07-12 |
| `LIBRARY_META` | `CONNECT` | 18 | 4 | 161.6M | 2026-07-12 |
| `LIBRARY_MARTS` | `DBT_CROGERS` | 33 | 0 | 18.4M | 2026-07-12 |
| `LIBRARY_RAW` | `RETIRED` | 1 | 0 | 3.9M | 2026-07-12 |
| `LIBRARY_MARTS` | `POLITICS` | 24 | 0 | 1.5M | 2026-07-12 |
| `LIBRARY_META` | `REGISTRY` | 10 | 8 | 351k | 2026-07-12 |
| `LIBRARY_MARTS` | `PUBLIC` | 14 | 0 | 229k | 2026-07-12 |
| `LIBRARY_MARTS` | `EPSTEIN` | 3 | 0 | 204k | 2026-07-12 |
| `LIBRARY_MARTS` | `CORE` | 5 | 0 | 167k | 2026-07-12 |
| `LIBRARY_STAGING` | `SEEDS` | 6 | 0 | 136k | 2026-06-14 |
| `LIBRARY_META` | `INGEST_LOGS` | 2 | 0 | 2,372 | 2026-07-12 |
| `LIBRARY_META` | `BUILD` | 4 | 1 | 60 | 2026-07-12 |
| `LIBRARY_MARTS` | `_RESTORE_20260701` | 12 | 0 | 22 | 2026-07-01 |
| `LIBRARY_STAGING` | `CORE` | 0 | 8 | 0 | 2026-06-12 |
| `LIBRARY_STAGING` | `DBT_CROGERS` | 0 | 1017 | 0 | 2026-07-06 |

*Top 15 of 41 — full list in Appendix: “All schemas”.*

*Views store no rows — the Rows column counts base tables only.*

## Codebase

dbt project: `library-onboarding/ripple_dbt/dbt_project.yml` — counts from manifest.json (compiled dbt state) (compiled 2026-07-12 19:00).

| Layer | table | view | total |
|---|---|---|---|
| `staging/` | 0 | 844 | 844 |
| `marts/` | 47 | 0 | 47 |
| `intermediate/` | 0 | 4 | 4 |

Plus 5 seeds, 2821 tests, 857 declared sources.

### Standalone scripts (outside dbt)

| Script | What it does | Warehouse touch | Confidence |
|---|---|---|---|
| `scripts/add_spine_columns.py` | Preview (and optionally apply) the spine-taxonomy columns on SOURCE_REGISTRY. | writes LIBRARY_META | confirmed (docstring) |
| `scripts/apply_read_lane.py` | The evidence.dev / Investigator read lane -- one command, Chris runs it. | writes LIBRARY_META | confirmed (docstring) |
| `scripts/backfill_join_keys_std.py` | Measure the REAL join keys every landed source carries and write them to the | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/backfill_specs.py` | AUTO-GENERATED backfill specs (2026-06-26) from the verify-backfill-specs workflow | — | confirmed (docstring) |
| `scripts/bridge_fuel_load.py` | Deterministic (LLM-free) bulk loader for known-good entity-crosswalk sources. | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/bridge_fuel_specs.py` | Source specs for scripts/bridge_fuel_load.py — verified bridge-fuel sources. | — | confirmed (docstring) |
| `scripts/budget_sprint.py` | Raise / restore the RIPPLE_BUDGET resource monitor for a backfill sprint. | — | confirmed (docstring) |
| `scripts/build_dashboard.py` | Build a single self-contained HTML page so Chris can SEE the backend: | reads LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/build_freshness_ledger.py` | Build the DATA-FRESHNESS LEDGER — the keystone of the platform foundation (Phase 0). | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/build_giant_aggs.py` | Giant pre-agg mart generator -- collapse the >1M-row giants into <100k-row rollup | writes LIBRARY_MARTS, LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/build_ladder_fixture.py` | Build the ladder-holdout test fixture (Move 4 of RIPPLE_GOVERN_THYSELF). | — | confirmed (docstring) |
| `scripts/build_registry_setup.py` | Create + seed LIBRARY_META.BUILD — Ripple's state about itself, as data. | writes LIBRARY_MARTS, LIBRARY_META, LIBRARY_RAW, LIBRARY_STAGING, THE_LIBRARY | confirmed (docstring) |
| `scripts/build_v_connections.py` | Build the friendly connection views over LIBRARY_META.CONNECT.CONNECT_EDGES. | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/build_v_connections_core.py` | Build the trustworthy-core connection view: LIBRARY_META.CONNECT.V_CONNECTIONS_CORE. | writes LIBRARY_META | confirmed (docstring) |
| `scripts/check_keys.py` | Cross-check the credential ledger against reality: env presence + decoded expiry. | — | confirmed (docstring) |

*Top 15 of 97 — full list in Appendix: “All standalone scripts”.*

### Packages (rolled up)

| Directory | .py files | References |
|---|---|---|
| `ripple/` | 10 | LIBRARY_META |
| `connect/` | 28 | LIBRARY_META, LIBRARY_RAW, LIBRARY_STAGING |
| `viz/` | 8 | LIBRARY_MARTS, LIBRARY_META |
| `loadkit/` | 7 | LIBRARY_META |
| `serve/` | 5 | LIBRARY_META, LIBRARY_RAW |
| `politics/` | 20 | LIBRARY_MARTS, LIBRARY_META, LIBRARY_RAW, LIBRARY_STAGING |
| `portal_recon/` | 4 | LIBRARY_META |
| `reading_room/` | 4 | LIBRARY_MARTS, LIBRARY_META, LIBRARY_RAW |
| `infra/` | 0 | — |
| `tests/` | 32 | LIBRARY_MARTS, LIBRARY_META, LIBRARY_RAW, LIBRARY_STAGING |

### Git

Current branch `main`, 1 uncommitted change.
| Branch | Last commit | Age | Subject |
|---|---|---|---|
| `main` | 2026-07-13 | 0d | Merge pull request #48 from Crogg23/detector-calibration |
| `detector-calibration` | 2026-07-13 | 0d | feat(detector): v2 plateau-shift metric + calibration batter |
| `reading-room` | 2026-07-12 | 0d | feat(reading-room): Phase 3 — close-the-loop spec as a BUILD |
| `politics-tier12-step0` | 2026-07-01 | 12d | Docs: frontier research corpus + consolidated master list |
| `claude/issue-coverage-loads` | 2026-06-28 | 14d | Fix-Everything Handoff: discovery-sweep remediation (Phases  |
| `claude/backend-readiness-p0` | 2026-06-27 | 15d | Backend readiness audit + reconcile build-state to live real |
| `claude/portal-firehose-and-loader-fix` | 2026-06-27 | 16d | Move #2 portal firehose: +62 connectable datasets, regraph,  |
| `claude/unhealth-the-spine` | 2026-06-26 | 16d | Unhealth the entity spine: add money/maritime/corporate tabl |
| `claude/backend-window-and-audit` | 2026-06-26 | 17d | Backend visibility window + debarred_but_funded detector + c |
| `origin/politics-itcont-money-mart` | 2026-07-03 | 9d | Add offline tests for BIOGUIDE and ICPSR spine keys integrat |
| `origin/claude/money-maritime-layer` | 2026-06-25 | 17d | Money + maritime layer: generalized detector engine + OFAC/U |
| `origin/claude/entity-layer` | 2026-06-25 | 17d | Confidence ladder: multi-pass blocking, Fellegi-Sunter score |
| `origin/claude/connect-engine-and-bulk-loader` | 2026-06-24 | 18d | Bridge + corroboration layer: entity-only crosswalk hops + n |
| `origin/claude/kind-euler-i98k1e` | 2026-06-21 | 21d | Wave 3: execute the load — table live + count-verified (338, |
| `origin/claude/zealous-archimedes-ilinpp` | 2026-06-21 | 21d | Wave 2: platform index readers — harvest 338k-dataset index  |

*Top 15 of 24 — full list in Appendix: “All branches”.*

## dbt-built vs. everything else

| How it got there | Objects | Rows (metadata) |
|---|---|---|
| raw landing — loaded by Python (onboard.py loaders / scripts/*_load.py) | 1784 | 284.8M |
| dbt view | 837 | 0 |
| serve-layer domain views — built by scripts/thelibrary_build.py (reads the catalog, not dbt) | 252 | 0 |
| orphan in a dbt database (not in manifest — old run, restore, or manual) | 233 | 1.6M |
| meta/system — agent-written (registry, ingest logs, connect graph, build ledger) | 47 | 162.0M |
| dbt table | 42 | 19.0M |
| restore artifact from 2026-07-01 backup recovery — not dbt-managed | 12 | 22 |
| retired raw tables — parked by cleanup, not dbt | 1 | 3.9M |

## Flags — broken, duplicated, or stale

- **Sibling repo `Ripple_v5` also contains a dbt project** (1 dbt_project.yml) — stale duplicate? Not audited here.
- **Sibling repo `The_Sandbox` also contains a dbt project** (1 dbt_project.yml) — stale duplicate? Not audited here.
- **1 uncommitted change** in the working tree: `scripts/library_snapshot.py` (LIBRARY_SNAPSHOT.md itself is not counted).
- dbt manifest is stale: 1 model file(s) modified after manifest.json was compiled (`marts/review/lead_queue.sql`) — manifest counts may lag the files.
- dbt: 11 model file(s) on disk are deliberately disabled (enabled=false — excluded from builds): civil_rights__fed_nara_wra_aad, corporate_registry__intl_ie_cro, economics__fed_hhs_taggs, economics__intl_ch_zefix, economics__intl_gr_gemi, government_records__fed_nara_aad, historical_records__fed_slavevoyages_intraamerican, justice__fed_doj_crt_cases…
- **1 zero-row table(s)** — loaded but empty. First few: `LIBRARY_META.CONNECT.DECISIONS` (full list in appendix).
- **233 orphan object(s) in dbt databases** that the current manifest doesn't know about: `LIBRARY_MARTS.CORE.DIM_COUNTY`, `LIBRARY_MARTS.CORE.DIM_DATE`, `LIBRARY_MARTS.CORE.DIM_STATE`, `LIBRARY_MARTS.CORE.DIM_TRACT`, `LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY`, `LIBRARY_MARTS.DBT_CROGERS.CORPORATE_REGISTRY__INTL_IE_CRO`… (full list in appendix).
- 21 dbt model(s)/seed(s) declared but not found in the warehouse (never built, or dropped): `LIBRARY_STAGING.DBT_CROGERS.STG_FED_US_USASPENDING_API__FEDERAL_AWARDS`, `LIBRARY_STAGING.DBT_CROGERS.STG_FED_BJS_DATA__BJS_DATA_COLLECTIONS`, `LIBRARY_STAGING.POLITICS.STG_FED_GOVINFO_BILLSTATUS__BILLS`, `LIBRARY_STAGING.POLITICS.STG_FED_FEC_BULK_CANDIDATES__CANDIDATES`, `LIBRARY_STAGING.POLITICS.STG_FED_FEC_BULK_SUMMARY__CANDIDATE_SUMMARY`, `LIBRARY_STAGING.POLITICS.STG_FED_GOVINFO_BILL_COSPONSORS__COSPONSORS`…
- Onboarding log statuses: complete=7, failed=6

---

## Appendix

<details>
<summary><b>All schemas</b></summary>

| Database | Schema | Tables | Views | Rows (metadata) | Last altered |
|---|---|---|---|---|---|
| `LIBRARY_RAW` | `LANDING` | 1784 | 0 | 284.8M | 2026-07-12 |
| `LIBRARY_META` | `CONNECT` | 18 | 4 | 161.6M | 2026-07-12 |
| `LIBRARY_MARTS` | `DBT_CROGERS` | 33 | 0 | 18.4M | 2026-07-12 |
| `LIBRARY_RAW` | `RETIRED` | 1 | 0 | 3.9M | 2026-07-12 |
| `LIBRARY_MARTS` | `POLITICS` | 24 | 0 | 1.5M | 2026-07-12 |
| `LIBRARY_META` | `REGISTRY` | 10 | 8 | 351k | 2026-07-12 |
| `LIBRARY_MARTS` | `PUBLIC` | 14 | 0 | 229k | 2026-07-12 |
| `LIBRARY_MARTS` | `EPSTEIN` | 3 | 0 | 204k | 2026-07-12 |
| `LIBRARY_MARTS` | `CORE` | 5 | 0 | 167k | 2026-07-12 |
| `LIBRARY_STAGING` | `SEEDS` | 6 | 0 | 136k | 2026-06-14 |
| `LIBRARY_META` | `INGEST_LOGS` | 2 | 0 | 2,372 | 2026-07-12 |
| `LIBRARY_META` | `BUILD` | 4 | 1 | 60 | 2026-07-12 |
| `LIBRARY_MARTS` | `_RESTORE_20260701` | 12 | 0 | 22 | 2026-07-01 |
| `LIBRARY_STAGING` | `CORE` | 0 | 8 | 0 | 2026-06-12 |
| `LIBRARY_STAGING` | `DBT_CROGERS` | 0 | 1017 | 0 | 2026-07-06 |
| `LIBRARY_STAGING` | `POLITICS` | 0 | 2 | 0 | 2026-06-29 |
| `THE_LIBRARY` | `CAMPAIGN_FINANCE` | 0 | 19 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `COMPANIES` | 0 | 14 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `CRIME_SECURITY` | 0 | 11 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `ECONOMY` | 0 | 13 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `EDUCATION` | 0 | 1 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `ELECTIONS` | 0 | 5 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `ENERGY_ENVIRONMENT` | 0 | 12 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `GEOGRAPHY` | 0 | 11 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `GOVERNMENT` | 0 | 31 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `GOVERNMENT_SPENDING` | 0 | 10 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `HEALTH` | 0 | 43 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `HISTORY` | 0 | 8 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `HOUSING` | 0 | 5 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `IMMIGRATION` | 0 | 8 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `INVESTIGATIONS` | 0 | 7 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `JUSTICE` | 0 | 22 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `MISC` | 0 | 1 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `MONEY` | 0 | 6 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `OPEN_DATA` | 0 | 6 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `PROCUREMENT` | 0 | 2 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `PUBLIC` | 0 | 1 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `SANCTIONS` | 0 | 4 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `SCIENCE` | 0 | 6 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `SPENDING` | 0 | 1 | 0 | 2026-07-12 |
| `THE_LIBRARY` | `TRANSPORT` | 0 | 5 | 0 | 2026-07-12 |

</details>

<details>
<summary><b>All standalone scripts</b></summary>

| Script | What it does | Warehouse touch | Confidence |
|---|---|---|---|
| `scripts/add_spine_columns.py` | Preview (and optionally apply) the spine-taxonomy columns on SOURCE_REGISTRY. | writes LIBRARY_META | confirmed (docstring) |
| `scripts/apply_read_lane.py` | The evidence.dev / Investigator read lane -- one command, Chris runs it. | writes LIBRARY_META | confirmed (docstring) |
| `scripts/backfill_join_keys_std.py` | Measure the REAL join keys every landed source carries and write them to the | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/backfill_specs.py` | AUTO-GENERATED backfill specs (2026-06-26) from the verify-backfill-specs workflow | — | confirmed (docstring) |
| `scripts/bridge_fuel_load.py` | Deterministic (LLM-free) bulk loader for known-good entity-crosswalk sources. | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/bridge_fuel_specs.py` | Source specs for scripts/bridge_fuel_load.py — verified bridge-fuel sources. | — | confirmed (docstring) |
| `scripts/budget_sprint.py` | Raise / restore the RIPPLE_BUDGET resource monitor for a backfill sprint. | — | confirmed (docstring) |
| `scripts/build_dashboard.py` | Build a single self-contained HTML page so Chris can SEE the backend: | reads LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/build_freshness_ledger.py` | Build the DATA-FRESHNESS LEDGER — the keystone of the platform foundation (Phase 0). | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/build_giant_aggs.py` | Giant pre-agg mart generator -- collapse the >1M-row giants into <100k-row rollup | writes LIBRARY_MARTS, LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/build_ladder_fixture.py` | Build the ladder-holdout test fixture (Move 4 of RIPPLE_GOVERN_THYSELF). | — | confirmed (docstring) |
| `scripts/build_registry_setup.py` | Create + seed LIBRARY_META.BUILD — Ripple's state about itself, as data. | writes LIBRARY_MARTS, LIBRARY_META, LIBRARY_RAW, LIBRARY_STAGING, THE_LIBRARY | confirmed (docstring) |
| `scripts/build_v_connections.py` | Build the friendly connection views over LIBRARY_META.CONNECT.CONNECT_EDGES. | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/build_v_connections_core.py` | Build the trustworthy-core connection view: LIBRARY_META.CONNECT.V_CONNECTIONS_CORE. | writes LIBRARY_META | confirmed (docstring) |
| `scripts/check_keys.py` | Cross-check the credential ledger against reality: env presence + decoded expiry. | — | confirmed (docstring) |
| `scripts/cisa_kev_load.py` | Deterministic loader for the CISA Known Exploited Vulnerabilities (KEV) Catalog. | — | confirmed (docstring) |
| `scripts/congress_committee_membership_load.py` | Load current congressional committee membership (who sits on / chairs what). | reads LIBRARY_RAW | confirmed (docstring) |
| `scripts/dashboard_server.py` | Ripple backend window — a LIVE, clickable local view of the library + insights. | reads LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/dedup_irs_eo_bmf.py` | Retire the exact-duplicate FED_IRS_EO_BMF landing table (evidence.dev cleanup). | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/degenerate_load_detector.py` | Standing check: flag DEGENERATE landed sources -- tables that landed rows but | reads LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/detector_bunching_battery.py` | Threshold-bunching detector v2 — calibration battery. | reads LIBRARY_RAW | confirmed (docstring) |
| `scripts/detector_threshold_bunching.py` | Threshold-bunching detector — calibration harness. | reads LIBRARY_RAW | confirmed (docstring) |
| `scripts/erd.py` | Render the warehouse as ER diagrams — boxes = datasets, lines = measured joins. | — | confirmed (docstring) |
| `scripts/export_control_plane.py` | Export the NON-REBUILDABLE control-plane tables off Snowflake (Phase 0 DR close). | writes LIBRARY_META | confirmed (docstring) |
| `scripts/export_graph.py` | Export outputs/connect_graph.json into formats real graph tools eat. | — | confirmed (docstring) |
| `scripts/fec_independent_expenditure_load.py` | Load the FEC Independent Expenditure file (Schedule E), cycles 2024 + 2026. | reads LIBRARY_RAW | confirmed (docstring) |
| `scripts/fec_itcont_load.py` | Stream-load FEC itcont -- itemized individual contributions, the ~70M-row donor | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/fec_pas2_load.py` | Load FEC pas2 -- committee->candidate contributions (+ coordinated/independent | reads LIBRARY_RAW | confirmed (docstring) |
| `scripts/federal_register_backfill.py` | DEPRECATED (2026-07-02) — one-off, NON-ATOMIC backfill. Kept for provenance only. | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/fix_catalog_lifecycle.py` | Fix two lifecycle misclassifications in LIBRARY_META.REGISTRY.CATALOG (D13 + D14). | writes LIBRARY_META | confirmed (docstring) |
| `scripts/gen_build_state.py` | Generate build-state.md from LIBRARY_META.BUILD. Deterministic. Zero LLM. | reads LIBRARY_META | confirmed (docstring) |
| `scripts/gen_evidence_pages.py` | Auto-generate evidence.dev pages from the card catalog (THE_LIBRARY.PUBLIC.START_HERE). | reads THE_LIBRARY | confirmed (docstring) |
| `scripts/generate_staging_models.py` | Deterministic staging-model generator -- the actual build, not the LLM one. | reads LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/grant_mcp_readonly_catalog.py` | Pass 0h of the faceted-catalog build: grant the read-only MCP role (CLAUDE_MCP_READONLY) | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/grant_mcp_readonly_staging.py` | Close the verifier-reach gap: grant the read-only MCP role SELECT on LIBRARY_STAGING. | writes LIBRARY_STAGING | confirmed (docstring) |
| `scripts/heartbeat.py` | THE HEARTBEAT — keep the Library alive on a cadence with no hand on the wheel. | reads LIBRARY_META | confirmed (docstring) |
| `scripts/housekeeping_cleanup.py` | Workstream B — Ripple Snowflake housekeeping cleanup. | writes LIBRARY_MARTS, LIBRARY_META | confirmed (docstring) |
| `scripts/irs_bmf_load.py` | Loader for the IRS Exempt Organizations Business Master File (EO BMF) -- the | — | confirmed (docstring) |
| `scripts/issue_batch_load.py` | Generic batch loader for the keyless/public-domain first-wave sources from the | — | confirmed (docstring) |
| `scripts/issue_batch_load2.py` | Second keyless tranche for the 75-issue coverage build: a spread of Our World | — | confirmed (docstring) |
| `scripts/lead_receipt.py` | Show the RECEIPTS for a banned-but-paid lead — how we know it's real, in plain English. | reads LIBRARY_RAW, LIBRARY_STAGING | confirmed (docstring) |
| `scripts/library_snapshot.py` | Library Snapshot — read-only inventory of this repo + the connected Snowflake account. | — | confirmed (docstring) |
| `scripts/load_connect_graph.py` | Load a connect_graph.json edge list into LIBRARY_META.CONNECT.CONNECT_EDGES. | reads LIBRARY_META | confirmed (docstring) |
| `scripts/naag_multistate_settlements_load.py` | Deterministic loader for the NAAG / attorneysgeneral.org multistate AG settlements database. | — | confirmed (docstring) |
| `scripts/noaa_ais_backfill.py` | DEPRECATED (2026-07-02) — one-off, NON-ATOMIC backfill. Kept for provenance only. | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/noaa_storm_events_backfill.py` | DEPRECATED (2026-07-02) — one-off, NON-ATOMIC backfill. Kept for provenance only. | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/ofac_load.py` | Deterministic (LLM-free) loader for the OFAC SDN sanctions list. | reads LIBRARY_RAW | confirmed (docstring) |
| `scripts/open_payments_2022_load.py` | DEPRECATED (2026-07-02) — one-off, NON-ATOMIC backfill. Kept for provenance only. | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/profile_spine_backfill.py` | Deterministically profile every landed source and propose GRAIN / NATURAL_KEY / | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/propose_catalog_domaining_fixes.py` | Preview (and optionally apply) DOMAIN_PRIMARY fixes for mis-filed catalog rows. | writes LIBRARY_META | confirmed (docstring) |
| `scripts/propose_catalog_hygiene_fixes.py` | Two catalog-hygiene fixes the 2026-06-26 audit found. SAFE BY DEFAULT (preview). | writes LIBRARY_MARTS, LIBRARY_META | confirmed (docstring) |
| `scripts/propose_catalog_trust_gate.py` | CATALOG TRUST-GATE — stop the catalog lying about broken data. SAFE BY DEFAULT (preview). | writes LIBRARY_MARTS, LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/propose_dead_scrape_demote.py` | Preview (and optionally apply) STATUS='empty' demotions for the dead-scrape pile | — | confirmed (docstring) |
| `scripts/propose_domain_retag.py` | Preview (and optionally apply) DOMAIN_PRIMARY for the 49 UNCLASSIFIED landed/ | writes LIBRARY_META | confirmed (docstring) |
| `scripts/propose_entity_theme_tags.py` | Propose ENTITY_TYPES + THEMES facet tags for the 54 landed/modeled sources. | reads LIBRARY_META | confirmed (docstring) |
| `scripts/propose_issue_domain_tags.py` | Domain-tag the 40 issue-coverage sources landed this session (all currently | reads LIBRARY_META | confirmed (docstring) |
| `scripts/propose_registry_volume_sync.py` | Preview (and optionally apply) SOURCE_REGISTRY.VOLUME updates for the sources the | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/propose_snapshot_flag.py` | Preview (and optionally apply) a SNAPSHOT-vs-PANEL temporal-coverage flag on the | writes LIBRARY_META | confirmed (docstring) |
| `scripts/propose_spine_entity_backfill.py` | Propose SPINE_ENTITY for sources that have a PROVEN grain/natural_key but a | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/rebuild_frozen_marts.py` | Recover real rows trapped behind stale / LIMIT-capped marts (evidence.dev readiness). | writes LIBRARY_MARTS, LIBRARY_RAW, THE_LIBRARY | confirmed (docstring) |
| `scripts/reconcile_op2022.py` | Reconcile the mislogged fed_cms_open_payments_2022 load (2026-07-01). | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/regrade_empty_loads.py` | Re-grade historical INGEST_RUNS using the load-time DENSITY gate (P0-1). | reads LIBRARY_RAW | confirmed (docstring) |
| `scripts/revoke_straggler_pats.py` | Revoke the stale / over-privileged programmatic access tokens on CROGG23 and | — | confirmed (docstring) |
| `scripts/sam_exclusions_load.py` | DEPRECATED (2026-07-02) — one-off, NON-ATOMIC loader. Kept for provenance only. | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/sec_edgar_financials_backfill.py` | DEPRECATED (2026-07-02) — one-off, NON-ATOMIC backfill. Kept for provenance only. | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/secrets_check.py` | Preflight: confirm creds/secrets are in place before a backfill wave. | — | confirmed (docstring) |
| `scripts/slavevoyages_intraamerican_load.py` | Deterministic loader for the SlaveVoyages Intra-American Slave Trade Database. | — | confirmed (docstring) |
| `scripts/thelibrary_a1_comments.py` | A1 -- plain-English COMMENTs on the 5 Ripple databases + their schemas. | reads LIBRARY_MARTS, LIBRARY_META, LIBRARY_RAW, LIBRARY_STAGING | confirmed (docstring) |
| `scripts/thelibrary_build.py` | Build THE_LIBRARY reading room + the friendly layer (C1 + C1.5b + A2 + C2 + C3). | writes LIBRARY_META, LIBRARY_RAW, THE_LIBRARY | confirmed (docstring) |
| `scripts/thelibrary_c0_tag_domains.py` | C0 -- assign DOMAIN_PRIMARY to the UNCLASSIFIED landed/modeled sources. | reads LIBRARY_META | confirmed (docstring) |
| `scripts/thelibrary_inventory.py` | C1.5a -- build the DATASET inventory that drives the Reading Room. | reads LIBRARY_MARTS, LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `scripts/thelibrary_refresh.py` | Post-pour refresh: rebuild the friendly layer + THE_LIBRARY reading room after | — | confirmed (docstring) |
| `scripts/thelibrary_typed_views.py` | Generate a TYPED tier over THE_LIBRARY reading-room views (evidence.dev readiness). | writes LIBRARY_META, LIBRARY_RAW, THE_LIBRARY | confirmed (docstring) |
| `scripts/ucdp_ged_load.py` | Deterministic loader for the UCDP Georeferenced Event Dataset (GED) Global. | — | confirmed (docstring) |
| `scripts/usaspending_load.py` | DEPRECATED (2026-07-02) — one-off, NON-ATOMIC loader. Kept for provenance only. | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/usgs_quake_backfill.py` | DEPRECATED (2026-07-02) — one-off, NON-ATOMIC backfill. Kept for provenance only. | writes LIBRARY_RAW | confirmed (docstring) |
| `scripts/verify_defects.py` | Run every open defect's evidence check and report still_broken / clear. | reads LIBRARY_META | confirmed (docstring) |
| `scripts/verify_staging_models.py` | Step 4 -- verify generated staging models, per-model, as they're built (not | reads LIBRARY_STAGING | confirmed (docstring) |
| `library-onboarding/browser.py` | Headless-browser rendering (C1b) -- Playwright. | — | confirmed (docstring) |
| `library-onboarding/build_library_map.py` | Build an interactive 'octopus map' of every LIBRARY_* database. | — | confirmed (docstring) |
| `library-onboarding/checkpoint.py` | Checkpoint rendering + the foreman approval prompt. | — | confirmed (docstring) |
| `library-onboarding/config.py` | Central configuration for the Ripple Source Onboarding Agent. | reads LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `library-onboarding/connect_hook.py` | Checkpoint 6 bridge: onboard.py -> the incremental CONNECT engine. | reads LIBRARY_META | confirmed (docstring) |
| `library-onboarding/first_live_load.py` | First live load -- prove the onboarding agent's write path end to end. | reads LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `library-onboarding/ingest.py` | Checkpoints 2 + 3 -- SCRIPT and LOAD. | writes LIBRARY_META, LIBRARY_RAW | confirmed (docstring) |
| `library-onboarding/live_batch.py` | Unattended live batch -- grow the Library through the FULL agent. | reads LIBRARY_META | confirmed (docstring) |
| `library-onboarding/llm.py` | Thin wrapper around the Anthropic API plus prompt-template loading. | — | confirmed (docstring) |
| `library-onboarding/naming.py` | Naming conventions for the Ripple warehouse. | reads LIBRARY_RAW | confirmed (docstring) |
| `library-onboarding/onboard.py` | Source Onboarding Agent -- entry point. | writes LIBRARY_META | confirmed (docstring) |
| `library-onboarding/recon.py` | Checkpoint 1 -- RECON. | reads LIBRARY_RAW | confirmed (docstring) |
| `library-onboarding/register.py` | Checkpoint 5 -- REGISTRY. | writes LIBRARY_META | confirmed (docstring) |
| `library-onboarding/registry_batch.py` | Registry-driven live batch -- onboard candidates straight from the catalog. | reads LIBRARY_META | confirmed (docstring) |
| `library-onboarding/registry_queue.py` | Registry-driven onboarding queue. | reads LIBRARY_META | confirmed (docstring) |
| `library-onboarding/scaffold_dbt.py` | Checkpoint 4 -- DBT. | — | confirmed (docstring) |
| `library-onboarding/snow.py` | Shared Snowflake connection + tiny query helpers. | — | confirmed (docstring) |
| `library-onboarding/sources_queue.py` | The pre-loaded landscape sweep. | — | confirmed (docstring) |
| `ripple.py` | Convenience shim so `python ripple.py <verb>` works from the repo root | — | confirmed (docstring) |

</details>

<details>
<summary><b>All branches</b></summary>

| Branch | Last commit | Age | Subject |
|---|---|---|---|
| `main` | 2026-07-13 | 0d | Merge pull request #48 from Crogg23/detector-calibration |
| `detector-calibration` | 2026-07-13 | 0d | feat(detector): v2 plateau-shift metric + calibration batter |
| `reading-room` | 2026-07-12 | 0d | feat(reading-room): Phase 3 — close-the-loop spec as a BUILD |
| `politics-tier12-step0` | 2026-07-01 | 12d | Docs: frontier research corpus + consolidated master list |
| `claude/issue-coverage-loads` | 2026-06-28 | 14d | Fix-Everything Handoff: discovery-sweep remediation (Phases  |
| `claude/backend-readiness-p0` | 2026-06-27 | 15d | Backend readiness audit + reconcile build-state to live real |
| `claude/portal-firehose-and-loader-fix` | 2026-06-27 | 16d | Move #2 portal firehose: +62 connectable datasets, regraph,  |
| `claude/unhealth-the-spine` | 2026-06-26 | 16d | Unhealth the entity spine: add money/maritime/corporate tabl |
| `claude/backend-window-and-audit` | 2026-06-26 | 17d | Backend visibility window + debarred_but_funded detector + c |
| `origin/politics-itcont-money-mart` | 2026-07-03 | 9d | Add offline tests for BIOGUIDE and ICPSR spine keys integrat |
| `origin/claude/money-maritime-layer` | 2026-06-25 | 17d | Money + maritime layer: generalized detector engine + OFAC/U |
| `origin/claude/entity-layer` | 2026-06-25 | 17d | Confidence ladder: multi-pass blocking, Fellegi-Sunter score |
| `origin/claude/connect-engine-and-bulk-loader` | 2026-06-24 | 18d | Bridge + corroboration layer: entity-only crosswalk hops + n |
| `origin/claude/kind-euler-i98k1e` | 2026-06-21 | 21d | Wave 3: execute the load — table live + count-verified (338, |
| `origin/claude/zealous-archimedes-ilinpp` | 2026-06-21 | 21d | Wave 2: platform index readers — harvest 338k-dataset index  |
| `origin/claude/charming-einstein-15maxw` | 2026-06-21 | 21d | portal_recon: refresh README — remove resolved blocker, add  |
| `origin/claude/pensive-allen-lrdevo` | 2026-06-21 | 22d | Add full connectivity audit brief (recon-only) |
| `origin/claude/wizardly-gates-rj4oa4` | 2026-06-21 | 22d | Add connectivity (join-density) audit of the Library |
| `origin/claude/lucid-ritchie-ee6ihs` | 2026-06-21 | 22d | Add peel investigative skill |
| `origin/claude/trusting-ptolemy-9r0ri3` | 2026-06-21 | 22d | feat: add fed_cfpb_complaints staging and mart |
| `origin/claude/happy-mayer-6dgdu3` | 2026-06-18 | 24d | Switch .mcp.json to http transport with PAT auth headers |
| `origin/claude/laughing-knuth-fmjka8` | 2026-06-18 | 24d | docs: record relocated MCP server at LIBRARY_TOOLS.PUBLIC.CL |
| `origin/claude/reconcile-onboarding-agent` | 2026-06-17 | 26d | Build C1 Phase 1: static scrape (BS4 + lxml) + fix the HTML  |
| `origin/claude/serene-wozniak-c9hva7` | 2026-06-16 | 26d | Add Source Onboarding Agent (5-checkpoint CLI) |

</details>

<details>
<summary><b>Zero-row tables</b></summary>

| Table | Last altered |
|---|---|
| `LIBRARY_META.CONNECT.DECISIONS` | 2026-06-25 |

</details>

<details>
<summary><b>Orphans in dbt databases</b></summary>

| Object | Type | Rows | Last altered |
|---|---|---|---|
| `LIBRARY_MARTS.CORE.DIM_COUNTY` | table | 3,222 | 2026-07-12 |
| `LIBRARY_MARTS.CORE.DIM_DATE` | table | 31k | 2026-07-12 |
| `LIBRARY_MARTS.CORE.DIM_STATE` | table | 56 | 2026-07-12 |
| `LIBRARY_MARTS.CORE.DIM_TRACT` | table | 85k | 2026-07-12 |
| `LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY` | table | 47k | 2026-07-12 |
| `LIBRARY_MARTS.DBT_CROGERS.CORPORATE_REGISTRY__INTL_IE_CRO` | table | 819k | 2026-07-12 |
| `LIBRARY_MARTS.DBT_CROGERS.HISTORY__FED_SLAVEVOYAGES_INTRAAMERICAN` | table | 12k | 2026-07-12 |
| `LIBRARY_MARTS.DBT_CROGERS.JUSTICE__FED_NAAG_MULTISTATE_SETTLEMENTS` | table | 882 | 2026-07-12 |
| `LIBRARY_MARTS.DBT_CROGERS.SPENDING__FED_HHS_TAGGS` | table | 45 | 2026-07-12 |
| `LIBRARY_MARTS.EPSTEIN.FCT_DATASET_SIZE_HISTORY` | table | 339 | 2026-07-12 |
| `LIBRARY_MARTS.EPSTEIN.FCT_LIBRARY_SNAPSHOT` | table | 619 | 2026-07-12 |
| `LIBRARY_MARTS.EPSTEIN.FCT_WAYBACK_PAGE_CHANGES` | table | 203k | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE` | table | 41k | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT` | table | 4,766 | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE` | table | 4,067 | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK` | table | 40 | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__JCS_MEDIANS` | table | 102 | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_COA` | table | 703 | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_SCOTUS` | table | 782 | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_INDIV_DONATIONS` | table | 1,057 | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_PAC_MONEY` | table | 1,258 | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__SCOTUS_JUSTICE` | table | 40 | 2026-07-12 |
| `LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON` | table | 11k | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.CORPORATE_ENTITIES__IRS_BMF_BY_STATE_NTEE_AGG` | table | 7,677 | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.CORPORATE_ENTITIES__IRS_REVOCATION_BY_STATE_YEAR_AGG` | table | 1,011 | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.ENERGY_ENVIRONMENT__NOAA_STORMS_BY_STATE_EVENT_AGG` | table | 28k | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.GOVERNMENT_POWER__FCC_LICENSES_BY_STATE_SERVICE_AGG` | table | 8,765 | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.HEALTH_MEDICINE__MEDICARE_PROVIDER_BY_STATE_TYPE_AGG` | table | 4,976 | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.HEALTH_MEDICINE__NPPES_BY_TAXONOMY_STATE_AGG` | table | 63k | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.HEALTH_MEDICINE__OPEN_PAYMENTS_BY_MFR_NATURE_AGG` | table | 19k | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.HEALTH_MEDICINE__OPEN_PAYMENTS_BY_SPECIALTY_STATE_AGG` | table | 35k | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.HEALTH_MEDICINE__PART_D_BY_STATE_TYPE_AGG` | table | 5,321 | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.MONEY_IN_POLITICS__FEC_INDIV_BY_CMTE_CYCLE_AGG` | table | 30k | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.MONEY_IN_POLITICS__FEC_INDIV_BY_STATE_CYCLE_AGG` | table | 400 | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.SPENDING_BUDGET__SBA_LOANS_BY_STATE_PROGRAM_AGG` | table | 3,893 | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.SPENDING_BUDGET__USASPENDING_BY_AGENCY_NAICS_AGG` | table | 17k | 2026-07-12 |
| `LIBRARY_MARTS.PUBLIC.SPENDING_BUDGET__USASPENDING_BY_AGENCY_STATE_AGG` | table | 3,925 | 2026-07-12 |
| `LIBRARY_STAGING.CORE.STG_EPSTEIN__COMPLIANCE_EVENTS` | view | — | 2026-06-12 |
| `LIBRARY_STAGING.CORE.STG_EPSTEIN__EFTA_OBLIGATIONS` | view | — | 2026-06-12 |
| `LIBRARY_STAGING.CORE.STG_EPSTEIN__LIBRARY_MANIFEST` | view | — | 2026-06-12 |
| `LIBRARY_STAGING.CORE.STG_EPSTEIN__REPLAY_LINKS` | view | — | 2026-06-12 |
| `LIBRARY_STAGING.CORE.STG_EPSTEIN__WAYBACK_CAPTURES` | view | — | 2026-06-12 |
| `LIBRARY_STAGING.CORE.STG_LEIE__EXCLUSIONS` | view | — | 2026-06-12 |
| `LIBRARY_STAGING.CORE.STG_META__SOURCE_REGISTRY` | view | — | 2026-06-12 |
| `LIBRARY_STAGING.CORE.STG_USASPENDING__SUBAWARDS` | view | — | 2026-06-12 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_FED_CONGRESS_COMMITTEE_MEMBERSHIP__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_FED_DHS_YEARBOOK__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_FED_USASPENDING_BULK__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_INTL_EU_SANCTIONS__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_ATLANTA_DATAATLA_51A606F539__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_ATLANTA_DATAATLA_5D9B9C30A9__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_ATLANTA_DATAATLA_EAD25CBDC7__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_ATLANTA_DATAATLA_FD3576897B__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_HARRIS_COUNTY_OP_1966AC023B__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_HARRIS_COUNTY_OP_6CDCF96CA7__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_HARRIS_COUNTY_OP_E87E81379A__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_LA_COUNTY_OPEN_D_0A94DB308E__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_LA_COUNTY_OPEN_D_E034245E05__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_OPEN_BALTIMORE_751D91C991__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_OPEN_DATA_DC_5B867C795C__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_OPEN_DATA_DC_D74755206A__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_OPEN_DATA_DC_D8E55D5B7F__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_OPEN_DATA_RALEIG_5E5B26DC88__PLACES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_OPEN_DATA_RALEIG_F18F09F22F__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_ORANGE_COUNTY_OP_644FB9535B__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_TUCSON_OPEN_DATA_14C7AA5CCF__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_TUCSON_OPEN_DATA_32A72D9D1D__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_TUCSON_OPEN_DATA_3A7E0821D1__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_TUCSON_OPEN_DATA_63C0193FF1__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_TUCSON_OPEN_DATA_7468CF46DB__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_TUCSON_OPEN_DATA_CDFFE1002A__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_TUCSON_OPEN_DATA_E0EDEA39BE__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_TUCSON_OPEN_DATA_F0203665DD__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_ARC_TUCSON_OPEN_DATA_F919285F50__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ANALYZE_BOSTON_0012B002BE__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ANALYZE_BOSTON_1321CB60B5__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ANALYZE_BOSTON_4EDDC3919B__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ANALYZE_BOSTON_5288DB6955__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ANALYZE_BOSTON_94AE63A33F__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ANALYZE_BOSTON_9FE0838E9F__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ANALYZE_BOSTON_DD269D0A1D__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ANALYZE_BOSTON_E4C004D662__PLACES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ANALYZE_BOSTON_F1B3F76830__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_CALIFORNIA_OPEN_490B55C81B__PLACES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_CALIFORNIA_OPEN_6611464444__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_CALIFORNIA_OPEN_A5D78A8B63__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_CALIFORNIA_OPEN_C19A7C8625__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_HOUSTON_OPEN_DAT_18A3CA22AF__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_HOUSTON_OPEN_DAT_A4490182BA__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_HOUSTON_OPEN_DAT_AB35BB6552__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_INDIANA_DATA_HUB_78F3E49D13__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_INDIANA_DATA_HUB_83BA6435C2__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_INDIANA_DATA_HUB_D4DAE8D984__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_INDIANA_DATA_HUB_FE00D42ACC__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ISRAEL_NATIONAL_03D9D0D534__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ISRAEL_NATIONAL_148FDFE63D__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ISRAEL_NATIONAL_33BAA6B58A__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ISRAEL_NATIONAL_52AD02EBE0__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ISRAEL_NATIONAL_6272F09A75__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ISRAEL_NATIONAL_936E1A0BA2__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ISRAEL_NATIONAL_94CE459E75__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ISRAEL_NATIONAL_C05E5881A0__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ISRAEL_NATIONAL_CB289C316E__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_ISRAEL_NATIONAL_E3D369B05F__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_OPEN_DATA_SA_18A877DDC9__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_OPEN_DATA_SA_1C37EE3869__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_OPEN_DATA_SA_2FCD3AEFD6__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_OPEN_DATA_SA_9DCA88D285__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_OPEN_DATA_SA_A8EF161189__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_98849B65EE__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_VIRGINIA_OPEN_DA_3E67A117FB__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_VIRGINIA_OPEN_DA_651C0C423A__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_VIRGINIA_OPEN_DA_CBC7FE8B75__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_VIRGINIA_OPEN_DA_E4498C978C__PLACES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WESTERN_PENNSYLV_070A16004D__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WESTERN_PENNSYLV_20E1A330CE__PLACES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WESTERN_PENNSYLV_23B8B5B7D2__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WESTERN_PENNSYLV_2DFC1ADDEA__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WESTERN_PENNSYLV_4FC22C2C30__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WESTERN_PENNSYLV_51B8DCF278__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WESTERN_PENNSYLV_ED65B530A3__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WESTERN_PENNSYLV_F810ADDEEC__PLACES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WESTERN_PENNSYLV_F82E02E6B2__PLACES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WPRDC_ALLEGHENY_12C9244C06__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WPRDC_ALLEGHENY_16A0BB67B4__PLACES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WPRDC_ALLEGHENY_1C103EE2CD__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WPRDC_ALLEGHENY_692C217FC7__PLACES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WPRDC_ALLEGHENY_9CCBEFBACC__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WPRDC_ALLEGHENY_A4E9CE945B__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WPRDC_ALLEGHENY_BB0184F847__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WPRDC_ALLEGHENY_CE7A2694FC__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_CKA_WPRDC_ALLEGHENY_FA3191E7A1__PLACES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_AUSTIN_OPEN_DATA_B5E56C7A67__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_COLORADO_INFORMA_1D5CFAD830__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_COLORADO_INFORMA_502999772D__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_COLORADO_INFORMA_6BE19A7323__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_COLORADO_INFORMA_C4D7351098__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_COLORADO_INFORMA_DE6C8A6901__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_COLORADO_INFORMA_E80CA7800E__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_CONNECTICUT_OPEN_28F32B559B__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_CONNECTICUT_OPEN_7909C84EE4__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_CONNECTICUT_OPEN_886AEF6AC6__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_CONNECTICUT_OPEN_AEB46F6C94__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_CONNECTICUT_OPEN_B2B9303A5F__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_CONNECTICUT_OPEN_F42EDA9B76__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_CONNECTICUT_OPEN_FF2B86A533__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_DATALA_LOS_ANGEL_361B8161B7__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_DATALA_LOS_ANGEL_DC3670AFE1__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_NEW_YORK_STATE_O_9BB5326481__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_OPEN_DATA_BR_C110D5CF59__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_SEATTLE_OPEN_DAT_C8F2072189__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_SF_OPENDATA_DATA_79618299A6__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_SF_OPENDATA_DATA_C19EE9EB44__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_TEXAS_OPEN_DATA_28E2F49084__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_TEXAS_OPEN_DATA_354E3ABF4F__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_TEXAS_OPEN_DATA_5410A1009F__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_TEXAS_OPEN_DATA_6F798A64FA__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_TEXAS_OPEN_DATA_A415622C5D__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_TEXAS_OPEN_DATA_D83872D208__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_TEXAS_OPEN_DATA_DA657010B1__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_0028F23236__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_08BA00868C__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_103F7D641F__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_1C0C156DA7__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_1E3F70C6A8__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_2065CE1D57__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_21E87270E6__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_275CD55E37__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_27F4752A1B__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_2FDF78BD22__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_36BE408253__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_376293FCF7__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_37975584A8__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_42CA38B0B0__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_447082E18E__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_49602BAEC5__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_4DA2A1E62F__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_4DDE6E2C89__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_4ED1B6FFA6__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_50B9839DCD__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_55B6E45F3F__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_55EF6EF0C6__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_5D4CAAD7FB__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_5E52F5D62F__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_5EF68422FF__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_617EBA9CD6__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_6223211050__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_623DBEE2EF__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_645B93D1C3__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_6679F2DEDB__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_79CFD825BF__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_7DACFB4113__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_8196274D0D__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_9837982623__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_9875D7F6E3__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_A396F5D252__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_A5AE4FD7A4__FACILITIES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_A6AF8166D5__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_A8921E729F__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_A9B7E273C8__FACILITIES` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_AC57352C67__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_AFAD2153EA__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_B0241DEE4B__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_B55A5210A0__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_B84814B0C6__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_BF328ADD84__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_BF857F3B65__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_CAEBCFEEAF__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_CC88C02100__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_CEE3F16579__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_D5F7CA2621__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_E776045748__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_E7A8212053__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_EEFC28CE6F__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_F1292B8D2F__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_F6E04B3D02__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_F9EFC33574__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_FA2123B348__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_UTAH_OPEN_DATA_P_FB657AA744__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_PORTAL_SOC_WASHINGTON_STATE_1A95FB1665__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_ST_CANNABIS_POLICY_BUNDLES__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_XC_OWID_AI_INCIDENTS_ANNUAL__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_XC_OWID_CPI__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_XC_OWID_FERTILITY__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_XC_OWID_NUCLEAR_WARHEADS__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_XC_OWID_REFUGEES__RECORDS` | view | — | 2026-07-06 |
| `LIBRARY_STAGING.DBT_CROGERS.STG_XC_OWID_TEMP_ANOMALY__RECORDS` | view | — | 2026-07-05 |
| `LIBRARY_STAGING.SEEDS.SEED_COMPLIANCE_EVENTS` | table | 17 | 2026-06-12 |
| `LIBRARY_STAGING.SEEDS.SEED_DIM_COUNTY` | table | 3,222 | 2026-06-14 |
| `LIBRARY_STAGING.SEEDS.SEED_DIM_STATE` | table | 56 | 2026-06-14 |
| `LIBRARY_STAGING.SEEDS.SEED_DIM_TRACT` | table | 85k | 2026-06-14 |
| `LIBRARY_STAGING.SEEDS.SEED_EFTA_OBLIGATIONS` | table | 3 | 2026-06-12 |
| `LIBRARY_STAGING.SEEDS.SEED_XWALK_ZCTA_COUNTY` | table | 47k | 2026-06-14 |

</details>

---
Rerun this audit any time: `python3 scripts/library_snapshot.py`
