# Instrument Hardening Plan — 2026-07-02

**Mission:** address every BAD finding and every instrument-side COULD-BE from the Fable audit
(2026-07-02) in one session. Songs (stories, human review sessions, publishing content) explicitly
deferred — but every *capability* they need gets built.

**Live constraint that shapes everything:** the keyless pour is RUNNING (PID 1720, started 08:04,
`onboard.py --batch --yes --skip-dbt --repair 1 --queue pour_queue_keyless.json`). Rules:
- Never touch `library-onboarding/onboarding_log.json` (pour rewrites it per source).
- Never kill PID 1720 (a mid-chunk kill is what wiped NPPES). All guards land in code; they take
  effect when Chris restarts the pour (resume via onboarding_log is safe by design).
- Warehouse writes are fine (separate tables; Snowflake handles DDL/DML concurrency), but no second
  onboard batch may run (shared log file, no lock).
- The running process read the queue into memory at start — editing pour_queue_keyless.json does NOT
  affect this run. ACLED (entry ~118) is hours away; restart before then makes the license guard policy
  instead of luck.

---

## WAVE 0 — stop the bleeding (inline, minutes)
| # | Fix | Audit finding |
|---|---|---|
| 0.1 | `requirements-dev.txt`: rapidfuzz==9.0.0 → ==3.14.5 (real version) | CI red 14 runs, PRs merged on red |
| 0.2 | gitignore `library-onboarding/*.log`; `git rm --cached` the two pour logs | 84MB pack, 50k-line logs committed |
| 0.3 | Delete dbt FAKE_LLM fixture (fed_smoke_fred staging+schema+mart, gov/ dir); redirect ONBOARD_FAKE_LLM dbt writes to a temp dir so it can never recur | dbt parse broken at HEAD |

## WAVE 1 — pour guards (owner: library-onboarding/*)
| # | Fix | Audit finding |
|---|---|---|
| 1.1 | **Empty gate**: when `load_result['empty']` → skip DBT + REGISTRY, record `status='empty'` (counts toward quarantine attempts, NOT 'complete'); registry never gets INCLUDE='Y' for it | empty loads retired as complete (fed_dea_arcos, fed_ed_fsa_datacenter) |
| 1.2 | **Auth gate**: post-RECON, if `auth.type != 'none'` and its env key is absent → `status='needs_key'`, skip before SCRIPT (no codegen burn); write the measured requirement back to `SOURCE_REGISTRY.AUTH_REQUIRED` | ~15 of 35 failures were key-class; AUTH_REQUIRED has no failure writeback |
| 1.3 | **source_id collision gate**: recon `_resolve` queries SOURCE_REGISTRY for the minted sid; exact hit without a queue pin → `status='already_cataloged'`, skip. Queue schema supports `source_id` pin (already honored) | fed_us_sec_edgar / fed_us_usaspending_api minted next to existing families |
| 1.4 | **exec() env blocklist**: `context['env']` excludes SNOWFLAKE_*/ANTHROPIC_*/`*_PAT`/`*_PASSWORD`/`*_SECRET*`/GITHUB_*/AWS_*; data-source keys still pass | full secret env handed to prompt-injectable generated code |
| 1.5 | `run_batch` returns nonzero when any source failed/needs_key; `_record()` captures error text (500 chars) | exit 0 always; 35/35 failures had no error field |
| 1.6 | `extract_code`: fence-required retry (one re-ask) before prose fallback; `compile()` syntax check at SCRIPT stage so bad code fails into repair with a real message; ingest codegen max_tokens 4096→8192 (streaming already on) | 3× 'invalid syntax line 1', 5× truncation in the live pour |
| 1.7 | Incremental watermark: validate MAX(cursor) looks ISO-orderable, raise loudly otherwise | lexicographic TEXT watermark silently wrong on MM/DD/YYYY |
| 1.8 | onboarding_log keyed on source_id when known (back-compat: lookup falls back to name; never rewrite existing entries) | log keyed on NAME; cross-queue collisions |
| 1.9 | `browser_ignore_https_errors` default OFF (opt-in env) | evidence platform accepts untrusted TLS by default |
| 1.10 | Tests for all of the above in test_onboard_smoke.py | — |

## WAVE 2 — safety chokepoint (owner: connect/leads*, scripts/dashboard*, scripts/lead_receipt.py, docs/RIPPLE_FOR_EVERYONE.md)
| # | Fix | Audit finding |
|---|---|---|
| 2.1 | dashboard_server + build_dashboard route reads through `leads.published()` semantics: STATUS='active' + DECISIONS anti-join; detail page filters too, cache keyed to include verdict state | libel firewall bypassed by only live consumer |
| 2.2 | leads_overlay derives DETECTORS from `leads_specs.JOBS` (all 6+), deletes frozen 338/353 annotation + 06-27 fallbacks | overlay hardcodes 4 of 6 rules |
| 2.3 | Vessel detector titles → archive-honest phrasing ("appears in N AIS position reports (US-coastal archive)"). PRECONDITION: verify LEAD_ID derivation is title-independent before editing; if title feeds the ID, bump rule to _v3 instead | present-tense overclaim over stale AIS |
| 2.4 | **date_gate engine support**: optional JobSpec fields (left_date_field, right_date/year_field) compile to a timeline evidence column + optional predicate — capability only, existing rules' lead sets unchanged | engine can't date-gate; 1,009 leads unranked on the violation dimension |
| 2.5 | lead_receipt.py parameterized queries (no f-string SQL) | SQL injection in ACCOUNTADMIN tool |
| 2.6 | RIPPLE_FOR_EVERYONE.md line 9 → neutral compliant phrasing; FOUNDER "found 773 taking money" line likewise | public-facing overclaim the safety layer forbids |
| 2.7 | Any surfacing of MATCH_RUNGS tiers must carry measured precision (display mapping; DB rung names unchanged) | 'CONFIRMED' = 1-in-8 wrong will overclaim |

## WAVE 3 — loader repair (owner: loadkit/, scripts/*load*.py, scripts/*backfill*.py)
| # | Fix | Audit finding |
|---|---|---|
| 3.1 | fec_itcont_load: `--max-rows` run skips the swap (leaves __STAGING, logs status='smoke'); add except → `_log_run('failed')` | smoke run would swap truncated table over live 84M rows |
| 3.2 | bridge_fuel_load chunked path → atomic staging swap via loadkit.atomic_load (fixes the engine we consolidate on) | non-atomic chunked writes on live tables |
| 3.3 | issue_batch_load + issue_batch_load2: refuse `_register()` on density-empty (align with bridge_fuel policy) | contradictory empty-registration invariants |
| 3.4 | One-off backfills: DEPRECATED header pointing at bridge_fuel; fix `_INGESTED_AT` epoch-int/name drift for future runs | provenance type drift |
| 3.5 | grant_mcp_readonly_catalog: main() guard; propose_catalog_hygiene rollback file timestamped | import-time GRANTs; rollback overwrite |
| 3.6 | Conformance test: static scan asserting every loader (a) never registers empty, (b) logs failed runs, (c) stamps TIMESTAMP_NTZ provenance | invariants only as strong as whichever loader a source arrived through |
| 3.7 | NPPES chunked spec in bridge_fuel_specs (atomic path from 3.2) — execution in Wave 5 | NPPES landing wiped to 700K |

## WAVE 4 — warehouse truth layer (owner: infra/ddl/, scripts/build_*, live Snowflake)
| # | Fix | Audit finding |
|---|---|---|
| 4.1 | `LIBRARY_META.REGISTRY.V_STATE`: taps by lifecycle, landing tables/rows, leads by rule/status, DECISIONS count, persisted edge count, mart drift flags — DDL in infra/ddl/ + applied live | headline numbers rot in prose; no canonical state |
| 4.2 | Persist graph edges: `"CONNECT".CONNECT_EDGES` written by discover full rebuild; JSON becomes a regenerable projection (export script); serve/plane fall back to the table when JSON absent | 20,696 edges exist only in a gitignored absent JSON |
| 4.3 | **Deploy the freshness ledger live** (it is NOT deployed — verified) + extend with mart watermark: mart LAST_ALTERED vs source last-ingest → MART_STALE flag surfaced in V_STATE | staleness invisible; landing↔mart drift undetectable by design |
| 4.4 | `reconcile_op2022.py --apply` (13.25M rows currently lifecycle='scouted' off two error-mislogged runs) | 13.25M-row table invisible to lifecycle filters |
| 4.5 | `export_control_plane.py --apply` — FIRST DR export ever (DR_STAGE confirmed absent); then scheduled in Wave 7 | the guard for the worst failure has never run |
| 4.6 | `SOURCE_REGISTRY.REDISTRIBUTION_RESTRICTED` column; set for ACLED family + EUvsDisinfo; queue builder + onboard skip respect it; prune intl_acled from pour_queue_keyless.json (takes effect on restart) | non-redistributable source sitting in the unattended queue |
| 4.7 | `regrade_empty_loads.py --apply` in background (slow re-sample of historical success runs) | P0 open since 06-27 |
| 4.8 | Stale-tail cleanup of build-state.md handled in Wave 8 | — |

## WAVE 5 — re-land NPPES + rebuild drifted marts (sequenced, background)
1. Re-land FED_CMS_NPPES via bridge_fuel chunked+atomic (~9 GB download, ~30-60 min) → verify ~9.6M rows.
2. THEN `dbt build --select stg_fed_cms_nppes__providers+ health__fed_cms_nppes maritime__fed_noaa_ais stg_fed_noaa_ais__*` — NEVER before the re-land (building now would nuke the mart to 700K).
3. **Do NOT `dbt build` politics mirrors** — they'd CREATE OR REPLACE the Python-built canonical tables. `dbt test --select` politics only.
4. Mart schema normalization (DBT_CROGERS → domain schemas) is explicitly DEFERRED: THE_LIBRARY's 160 views point at DBT_CROGERS FQNs; moving marts breaks the reading room until regenerated. Follow-up session.

## WAVE 6 — spine/graph expansion + full rebuild (background, after Wave 5 step 1)
| # | Fix |
|---|---|
| 6.1 | keys.py + entity_index_specs: FEC_CAND_ID, FEC_CMTE_ID, BIOGUIDE, ICPSR as first-class keys (verify live column names first); validate_key_config green |
| 6.2 | EIN detector: verify IRS BMF + SEC EDGAR EIN columns live; enable the commented ein_bridge JobSpec |
| 6.3 | Full rebuild AFTER NPPES lands: fingerprint → discover (writes CONNECT_EDGES + fresh JSON) → spine → entity-index → `leads --run` (all rules incl. EIN). Key-config change forces full rebuild anyway (fingerprint gate) — one rebuild covers everything |
| 6.4 | incremental.reslice_spine also refreshes the table's KEYSET_LIVE partition |
| 6.5 | Portal auto-targeting: script ranking PORTAL_DATASET_INDEX STEEL/STRONG by spine-key overlap → outputs/pour_queue_portal_ranked.json (build, don't pour) |

## WAVE 7 — keep-alive (owner: scripts/heartbeat*, infra/, loadkit/preflight.py)
| # | Fix |
|---|---|
| 7.1 | preflight `live_pat_expiry`: decode JWT exp from the PAT locally; BLOCK <7 days, warn <21; wire into onboard preflight + heartbeat |
| 7.2 | `infra/keys_ledger.json`: every credential + expiry (PAT 09-20, SAM 09-22, others unknown-but-listed); checked by preflight |
| 7.3 | heartbeat.py Windows port: platform.uname, psutil/taskkill process-tree kill, pidfile lock path (fcntl fallback exists); `--selftest` green on this machine |
| 7.4 | `scripts/register_windows_tasks.ps1`: schtasks for (a) weekly control-plane DR export, (b) daily freshness-ledger rebuild, (c) weekly deterministic `bridge_fuel --refresh`. Every task script first checks no onboard.py process is running (no concurrent pours) |
| 7.5 | POUR_GO_CHECKLIST: post-pour step referencing `budget_sprint.py --restore` (policy: sprint ≤100, steady-state 15) |

## WAVE 8 — docs reconciliation (owner: *.md + two docstrings)
- CLAUDE.md: 6 checkpoints, --queue mechanism, both stale scale numbers → "query V_STATE", ~900→current, needs_key/empty statuses documented.
- OVERVIEW.md: real folders (serve/, loadkit/, politics/, infra/), scale → V_STATE pointer.
- build-state.md: new CURRENT FOCUS; the rotten non-dated tail (final NEXT ACTION from 06-24, DECISIONS-MADE PAT line) explicitly superseded.
- Stale PAT alarms (FOUNDER FIVE-ALARM, HEARTBEAT_README, POLITICS_BUILD_RUNBOOK, loadkit/preflight.py docstring, connect/HOWTO.md) → rotated, exp 2026-09-20, pointer to keys_ledger.
- library-onboarding/README provenance contract: document per-chunk SHA vs manifest SHA truthfully.
- connect/README stale 0.77 fuzzy line → current calibrated numbers.

## WAVE 9 — verification + ship
1. Full offline pytest (expect >120 tests green), dbt parse green.
2. Live acceptance queries: V_STATE returns; NPPES landing ≈9.6M = mart; CONNECT_EDGES > 0; DECISIONS gate query; DR_STAGE has files; ledger deployed.
3. Logical commits per wave; push; PR to main via gh with full description.

## STRESS-TEST AMENDMENTS (v2, 2026-07-02 — 8-lens adversarial review, 39 blockers/corrections folded in)
- **Ship strategy:** work on current branch with per-wave commits; at ship time replay trees onto a fresh
  `instrument-hardening` branch off main via `git commit-tree` (zero working-tree disturbance, keeps
  ee1cb55's 51k-line log blobs out of main's history). Never stage onboarding_log.json or *.log.
- **Pour stop procedure (the restart IS load-bearing):** watch pour_keyless.log for an inter-source
  boundary, Ctrl+C there (handled cleanly, log saved), validate onboarding_log.json parses, restart same
  command. Deadline: before queue entry ~110 (ACLED at 118, ~3.5-4.5h from 08:04 start). Wave 1 adds
  atomic save_log + fail-loud load_log so a bad kill can't wipe resume state.
- **1.2 auth gate:** recon prompt must emit `auth.env_var` (recon returns only {type,notes} today — the
  env-key name doesn't exist post-RECON); gate lives in onboard_source (non-raising), NOT _resolve;
  writeback = targeted UPDATE, never register MERGE; bypass under fake_llm.
- **1.3 collision gate:** gate on LANDED EVIDENCE (INGEST_RUNS success / lifecycle landed|modeled), not
  registry existence (854 scouted rows would false-skip); applies to pinned sids too (with
  --include-landed escape); near-family prefix check = warn-only.
- **1.1/1.2 resume semantics:** quarantine check + attempts increment must include 'empty' (both
  onboard.py:299 and :316); 'needs_key' skips on resume UNLESS its env key is now present;
  'already_cataloged' terminal. Exit code from THIS run's counters only (shared log poisons it);
  needs_key does NOT force nonzero. Update test_onboard_smoke rc==0 assertion.
- **1.4:** blocklist BOTH exec sites (ingest.py:488 AND :664); anchored patterns (prefix SNOWFLAKE_/
  ANTHROPIC_/GITHUB_/GH_/AWS_, suffix _PAT/_PASSWORD, substring _SECRET) — naive '_PAT' strips PATH;
  _TOKEN stays allowed (COURTLISTENER_TOKEN is a data key).
- **1.6:** fence-retry lives in generate_ingest_script (extract_code is a pure parser); compile() check
  there too so it feeds auto-repair; gates must live in onboard_source (registry_batch/live_batch bypass
  run_batch).
- **1.7:** validate watermark AFTER ingest.py:243-251's blanket except (inside it, the error is swallowed
  → since=None → duplicate-append corruption).
- **3.2 retrofit ordering (pinned):** chunks → __STAGING; except handler drops STAGING ONLY (today it
  DROPs the LIVE table — a failed re-land would delete the surviving 700K NPPES rows); density gate on
  staging → empty: drop staging + log 'empty', live untouched → execute_swap → THEN log 'success' →
  register last. Qualify atomic_load's INFORMATION_SCHEMA check; add repo-root sys.path.
- **3.x bridge_fuel _register clobber:** skip _register when a registry row already exists — otherwise a
  re-land/weekly-refresh wipes curated facets (MERGE overwrites non-null defaults: UNCLASSIFIED/NONE/[]).
- **Wave 5:** re-land needs `--force` (a 2026-06-17 success row makes default --run skip); spec = NO
  key_cols aliasing (333 live column names are the dbt/connect contract), member regex
  npidata_pfile_\d{8}-\d{8}\.csv, chunk_rows 50k, NPI_Files.html resolver (download.cms.gov rotates
  monthly); realistic wall time 1.5-3h; run on COMPUTE_WH to avoid pour contention. dbt: pip
  dbt-snowflake==1.8.4 in a venv (installed dbt-fusion preview REFUSES this project — 208 errors);
  run from inside ripple_dbt (a stale ~/.dbt 'ripple' profile targets the dead RIPPLE db); selectors are
  `stg_fed_cms_nppes__npi_providers+ stg_fed_noaa_ais__ais_vessel_positions+`; politics = `dbt test
  --select marts.politics` ONLY (dbt build would CREATE OR REPLACE the Python-built canon).
- **Wave 4:** ONE canonical edge store — create CONNECT_EDGES shell via DDL now (V_STATE view compiles),
  discover full-rebuild replaces it, incremental retargets into it (Wave 6 verifies shape match);
  export_control_plane needs dest.as_posix() in the GET (backslashes corrupt the quoted SQL path) +
  re-raise on row_count errors (silent-skip = partial backup that looks complete) + smoke-test on
  FACET_VOCAB first; mart-drift lives in V_STATE (INFORMATION_SCHEMA LAST_ALTERED w/ CONVERT_TIMEZONE,
  exclude _RESTORE%), NOT the ledger view (daily rebuild would revert it — or land it in BOTH VIEW_DDL
  copies same commit); regrade --apply DEFERRED post-pour (sampling race vs live loads + warehouse
  contention); run ledger build/export on COMPUTE_WH.
- **Wave 6:** making a key first-class = 5 files (tag_portal_index KEY_TOKENS, discover KEY_DOMAIN,
  keys NORM_RULES ['alnum_upper' mode pre-built for this], entity_index_specs.ENTITY_TYPE_BY_KEY,
  spine._ENTITY_TYPE_SQL + incremental._entity_type_sql) as ONE atomic commit; compound tokens only —
  bare 'fec' matches EPA's Formal-Enforcement-Case columns, bare 'icpsr' matches STATE_ICPSR; do NOT put
  the 84M itcont in DISPLAY_SPECS (spine scan cost) — route member↔candidate via BIOGUIDE + FEC bulk
  tables (FEC_IDS on legislators is a JSON-array string, unusable as key_col); EIN spec must be AUTHORED
  (the stub is a skeleton): FED_SEC_EDGAR_FINANCIALS.EIN (5,773 distinct; NOT the poisoned FED_US_SEC_EDGAR)
  × FED_IRS_BMF.EIN (1.97M) — expected yield ~3 leads (capability > count); BMF provenance cols lack the
  underscore prefix → EIN receipts resolve 'unresolved' until BMF re-lands (accepted + documented).
  **Full rebuild (6.3) DEFERRED to post-pour** — it would be stale for the pour tail the moment it
  finished; keys.py edit makes checkpoint-6 refuse (gracefully) for the pour remainder; post-pour rebuild
  + connect-changed sweep re-links everything. `connect leads --run` IS safe today (independent of the
  fingerprint guard) → run after title fix + EIN spec so live titles update and the EIN rule fires.
- **Wave 7:** heartbeat port MUST replace _alive's os.kill(pid,0) — on Windows that TERMINATES the probed
  process (verified empirically) — with ctypes OpenProcess; stdlib-only (no psutil — not installed);
  taskkill /T /F for tree kill; selftest spawns its own child (2**22 can be a real PID). Scheduler via
  Register-ScheduledTask with -StartWhenAvailable (schtasks.exe can't express it; sleeping laptop misses
  every trigger silently) + S4U logon; add an hourly `heartbeat --run` task (else LINK/RECONCILE never
  run) with a Win32_Process CommandLine check for a live onboard.py (tasklist can't see it); every
  wrapper writes outputs/_task_<name>_LAST.json + a daily nag surfaces stale/failed ones. PAT verified a
  decodable JWT (exp=2026-09-20T14:58:55Z) — live_pat_expiry is zero-network; keep pat_check untouched
  (different, tested semantics) — new pure check alongside.
- **Deferred to post-pour session (explicit):** full connect rebuild + CONNECT_EDGES population + spine/
  entity-index refresh + connect-changed sweep; regrade_empty_loads --apply; portal-ranked pour; THE_LIBRARY
  refresh; LDA load execution (loader script ships today, run deferred); itcont donor-ER recipe (needs its
  own calibration session); git history rewrite for pack size.

## Sequencing / risk register (stress-test seeds)
- R1: pour running — file edits safe (process has old code in memory); onboarding_log.json untouchable; restart note to Chris.
- R2: dbt build before NPPES re-land nukes the mart → hard ordering (Wave 5).
- R3: dbt build of politics mirrors would replace Python-built canon → test-only.
- R4: mart schema moves break THE_LIBRARY views → deferred.
- R5: vessel title edits may mint new LEAD_IDs → verify derivation first.
- R6: keys.py change invalidates incremental fingerprint → full rebuild scheduled anyway; checkpoint-6 connect-one during the pour will refuse incremental safely (verify refuse-path is non-fatal).
- R7: discover full rebuild cost (spatial phase) — run with spatial capped/skipped if flag exists; budget headroom 267 credits.
- R8: env blocklist must not break generated scripts reading data keys → blocklist (not allowlist) chosen.
- R9: schtasks must not launch concurrent loads during a pour → process check in every task wrapper.
- R10: editing files the pour will re-import on restart — all changes must keep CLI back-compat (--batch/--yes/--queue/--repair semantics unchanged).
