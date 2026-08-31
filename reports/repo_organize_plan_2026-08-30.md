# Repo organize plan — 2026-08-30

Built from three fresh-context scouts plus a hand spot-check.
Chain for every verdict: git activity last 7 days, repo-wide import trace, file contents.
Two scout claims failed the spot-check and were corrected (hunch, viz — see §5).

## 1. What stays untouched (LIVE)

| Area | Why |
|---|---|
| `.claude/`, `.snowflake/`, `.vscode/`, `__marimo__/` | rulebook + warehouse door, most-edited area |
| `connect/` (minus spine files, see §3) | 90 importers, core entity/graph library |
| `loadkit/`, `scripts/` (minus one-offs, §4), `tests/` | live loaders, slash-command backends, running suite |
| `library-onboarding/` | dbt project, 295 touches this week |
| `reports/recon/`, `reports/viz/` + `_build/`, `reports/location_index/`, `reports/row1/`, `reports/lab_map/` (md + small tables), `reports/connections_audit_2026-08-27/` | current canonical reference |
| `data/`, `docs/`, `notebooks/`, `notebook.py`, `build-state.md`, `CLAUDE.md`, `THE_SCRIPT.md`, `pytest.ini`, `requirements*.txt` | active |
| `outputs/` still-referenced files: `connect_graph.json`, `connect_fingerprints.json`, `library.json`, `atlas.json`, `terrain_map.html`, `nobrainer_load_checkpoint_2026-08-29.json`, checkpoints, rollback SQL | referenced by live code/reports |

## 2. DEAD → junk drawer (with LEDGER rows)

Zero external importers or months-stale, superseded:

- `mission_control/` (last commit 07-27, zero importers)
- `serve/` (zero importers; only *outbound* deps; superseded by static chain explorer)
- `politics/` (zero importers, last commit 08-01)
- `investigations/` (Jul-03 one-off probes)
- `portal_recon/` (Jul-30, frozen JSON results, no consumers)
- `queues/` (2 sprint JSONs, scheme abandoned)
- `home/` (Streamlit home door, self-only importers, 08-11)
- `archive/` → `_JUNK_DRAWER/archive_pre_2026-08-30/` (old retirement bucket, consolidate; no ledger of its own)
- Root files: `RIPPLE.bat`, `START_HERE.bat` (platform is macOS now), `Ripple Design System - Blueprint (standalone) (9).html` (6.2M browser-download dump)
- Root data files `occ_national_by_name.xlsx`, `occ_thrifts_by_name.xlsx` → `data/` not drawer (raw source, misplaced not retired)

## 3. SPINE-ERA — the entanglement problem

The spine is dead. But it is not yet unpluggable:

**Hard imports of `connect/spine.py`:**
- `connect/entity_index.py:17` and `connect/incremental.py:65` import `_addr_expr`, `_name_expr` — two normalization expressions. Fix: move those two functions into a neutral module (`connect/normalize.py`), repoint both importers, then `spine.py` + `spine_entity.py` have zero live importers.
- `hunch/census.py:43` imports `SPINE_ENTITY_BY_KEY` — moot if hunch retires (§5).

**Live spine tests (5):** `test_spine_batch_2026_08_29.py`, `test_spine_inputs_live.py`, `test_spine_map_visibility.py`, `test_staging_spine_id_parity.py`, `test_politics_spine_keys.py`. These make a dead system a test-failure source. Retire to drawer with the spine code.

**Spine scripts:** `add_spine_columns.py`, `gen_spine_specs.py`, `profile_spine_backfill.py`, `propose_spine_entity_backfill.py`, `spine_wiring_prep.py` → drawer.

**Spine reports/outputs (~9.5M):** `reports/spine_wiring_drafts/` (598 files, 8.8M), `SPINE_WIRING_PLAN_2026-08-24.md`, `spine_tree_data.json`, `spine_axis_table_membership_2026-08-24.csv`, `spine_connection_audit_2026-08-11.md`, `spine_rebuild_openbox_2026-08-18.md`, `library_spine_audit_2026-07-28.md`, `reports/viz/warehouse_spine_tree_2026-08-24/`, `the_audit_2026-08-24/spine_connect_edges_live.csv`, `census_grid_2026-08-12/fill/spine_batch_verification.jsonl*`, `outputs/spine_*`, `outputs/wave1_specs.py`, `wave1_log.txt`, `wave2_specs.py`, `wave2_log.txt`, `outputs/HANDOFF_connect_the_spine.md` → drawer.

**Also:** pass-2 report's parked item "register pass-2 families in the spine" is void. New join registrations need a non-spine home — open design question, Chris's call.

## 4. STALE reports/outputs → drawer (dated one-off sessions, ~67M)

- `reports/the_audit_2026-08-24/` (26M, superseded by 08-26)
- `reports/census_grid_2026-08-12/` (21M)
- `reports/time_index/` except `clock_index.csv` (~15M; clock_index has 8 live refs)
- Aug-21 ripples session: `ripples_*_2026-08-21.*`, `grow_wiring_2026-08-21.md`, `handoff_naming_2026-08-21.md`, `wiring_scout_2026-08-21.json`
- Aug-01 hunch reports, Aug-10 mart-defect cluster, Aug-12 ladder/question files, Aug-18 value_shape cluster, Aug-20 trend files, fix-session files, `_*.json` intermediates, viz sketchbook HTMLs, `_clockwork/`, `typing_index/`, `vendor/`, `rebuild_explorer.py`, `build_from_cache.py`, `VIZ_OPTIONS_MAP_2026-08-25.md` + plan
- `outputs/` Jun–Jul sediment: all dated Jun/Jul md/sql/log/err files, the 08-05 ID-sweep cluster, the 08-11 audit cluster, dedup/recon batch dirs, `FABLE_KEY_HUNT_2026-07-22.md` (1M md — context hazard)
- Dated one-off scripts in `scripts/` (13 files with dates in names) and the `row1*` script family — keep or drawer, Chris's call; they are receipts generators
- 20 unreferenced scripts incl. `fix_errored_models.py` and `spine_wiring_prep.py` — both touched this week but wired to nothing

## 5. UNCLEAR — needs Chris

| Item | Situation |
|---|---|
| `viz/` + `bench/` + `ripple/` + `playground/` | one connected cluster; imports each other + 2 live scripts; untouched 3+ weeks |
| `hunch/` | imported by 2 scripts + 3 tests, all in-cluster; also imports spine_entity |
| `honesty/`, `glossary/` | only in-cluster importers, stale since early Aug |
| `evidence/`, `web/` | separate site projects, stale 1–2 weeks |
| `reading_room/` | zero importers but README calls it primary entrypoint |
| `infra/` | stale but `keys_ledger.json` looks operationally load-bearing; launchd not audited |
| `README.md`, `CHRIS_DECISIONS.md`, `Laboratory_Warehouse_Map.md` | stale front-door docs, predate rulebook v2 |
| Heavy machine files (~110M) | column CSVs, count_possibilities, jsonl dumps → move to `reports/_heavy/` or drawer |

## 6. Spot-check corrections applied

- Scout called `hunch/` dead with zero importers — wrong, 5 importers found.
- Scout said `viz/` importers were all circular — wrong, playground/serve/2 scripts import it.
- Both moved from DEAD to UNCLEAR (§5).

## 7. Execution order (when approved)

1. Move DEAD dirs + root junk to drawer, add LEDGER rows.
2. Extract `_addr_expr`/`_name_expr` to `connect/normalize.py`, repoint 2 importers, run tests.
3. Drawer the spine code, scripts, tests, reports, outputs. Run full suite.
4. Drawer STALE reports/outputs.
5. Chris rules on §5 UNCLEAR items; execute those calls.
6. Rewrite `README.md` to match the post-clean layout.
