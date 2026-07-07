# FABLE AUDIT — 2026-07-06

**Full-repo + live-warehouse stress-test, aimed at one goal: real, substantial, CONNECTED data queryable from evidence.dev.**
Method: 54 agents — 12 sweep lenses (6 repo readers, 5 live-warehouse auditors, 1 evidence.dev prober) → dedup → one adversarial verifier per defect (every claim re-reproduced against files or live SQL) → completeness critic.
Result: **40 defects confirmed (0 refuted)** · 26 observations · 18 genuinely-good calls · 8 questions only Chris can answer.
Leads/detectors/publishing were explicitly out of scope.

---

## THE VERDICT

**The machinery is better than you think. The map is worse than you think.**

The engineering is real — the load path, the dbt hygiene, the connect measurement core, loadkit, the V_STATE doctrine, THE_LIBRARY reading room all survived hostile verification. What stands between you and evidence.dev is not code quality; it's four gaps, all mostly mechanical to close:

1. **The graph is dark.** The canonical edge table has 0 rows, the incremental engine has been config-locked since Jul 2, and only 45 of 199 landed/modeled sources have ANY queryable edge. "Data that connects" is currently a local JSON file from Jun 29.
2. **The truth layer lies in both directions.** ~31 junk sources read `landed`; meanwhile the 19M-row FHFA NMDB reads `sampled` and 13.25M rows of Open Payments 2022 are catalog-invisible.
3. **The typed layer is thin exactly where it matters.** All 789 new generated staging views are all-TEXT; 171 of 233 reading-room views contain zero casts; 11 of the top-25 tables have no typed object at all.
4. **The read lane doesn't exist.** No reader role, no serve warehouse, no Node.js on the machine. The only credential you could paste into evidence.dev today is an ACCOUNTADMIN PAT.

Two of the four are fixable with SQL files **already written and sitting in the repo**.

---

## SCOREBOARD (live V_STATE, 2026-07-06 11:15 PT)

| metric | value | reality check |
|---|---|---|
| Landing tables / rows | 1,786 / 291.0M | top 10 tables hold 82.5% of rows; 87.5% of tables are portal samples holding 1.2% of rows |
| landed / modeled | 174 / 25 | ~31 of these are junk (HTML, placeholder rows, link catalogs) |
| connect.edges (canonical) | **0** | writer never pointed at it; real graph = 20,907 edges in a gitignored JSON (Jun 29) |
| connect.edges_inc | 1,074 | frozen 2026-07-02; covers 380 of 1,786 tables; no join columns recorded |
| spine entities | 9.79M | 98.1% NPPES; zero person/politics entities ever entered |
| reading-room views | 233 | healthy (25/25 probed OK) but 171 are zero-cast raw passthroughs |
| decisions.total | 0 | the judgment log has never been used |

---

## WHAT'S GENUINELY GOOD (stop underrating it)

- **Load-path hardening is strong**: prompt-injection env blocklist, compile gate, socket timeouts, atomic corrupt-safe logs, density gate + `_reject_html` doing real work (109 honest `empty` demotions).
- **The registry-driven staging generator (cac68bb) is real and live** — 789 models on disk, ~900+ views in Snowflake, and its `SPINE_ENTITY_ID` formula verifiably joins `ENTITY_GOLDEN` 6852/6852 on spot check.
- **dbt project hygiene**: 894 enabled models parse clean, zero dangling refs, all 850 declared sources exist in LANDING.
- **The connect measurement core is honest** — a hand-audited STEEL edge reproduced byte-exact; the config-guard freeze is the guard *working*.
- **loadkit is textbook** (48 passing unit tests on this Mac); the politics domain is healthy — the old "20 Windows-broken loaders" memory is FALSE, all 17 use relative paths.
- **V_STATE doctrine is real epistemic engineering** — derived numbers verify exactly; the 285 catalog "orphans" fully explained (failed portal attempts + OP2022).
- **The offline test suite is real**: 414 green in 4s, proper snowflake-marker self-skips, CI on every push.
- **THE_LIBRARY reading room is purpose-built for evidence.dev**: 233 documented views in 23 domain schemas, perfect FRIENDLY_LAYER reconciliation, `START_HERE` as a machine-readable index, FUTURE grants already self-maintaining.
- **Budget guardrails are real** (300-credit monitor, all-XS fleet, ~7 weeks headroom) and the service-user pattern evidence.dev needs already exists and is proven (`SVC_CLAUDE_MCP`).
- **Facets on the landed set are near-complete for browsing**: 0 null domains, 1 UNCLASSIFIED, 4 missing unit-of-observation.
- License capture (193/199), the DR unloader (`export_control_plane.py`), and the `REDISTRIBUTION_RESTRICTED` concept are well-designed — just unexecuted/unpopulated.
- The Alexandria blueprint (`outputs/alexandria_foundation_BLUEPRINT_2026-06-28.md`) is a decision-grade roadmap and Phases 0–3 actually shipped.

---

## BLOCKERS — between you and evidence.dev

**[D01] The connection graph is not queryable from Snowflake.** `CONNECT_EDGES` = 0 rows (no writer ever pointed at it; `infra/ddl/06_connect_edges.sql` calls it "the ONE canonical store"). The real graph — 20,907 edges incl. ~9.9k hard-ID — lives only in gitignored `outputs/connect_graph.json` (Jun 29, 764 nodes). Queryable slice: `CONNECT_EDGES_INC` 1,074 edges / 380 tables, frozen Jul 2. Zero views over any of it. → Retarget both writers at CONNECT_EDGES per the existing DDL; stopgap-load the JSON; ship V_CONNECTIONS.

**[D02] Incremental connect engine hard-locked since 2026-07-02.** Commit a580a6 changed NORM_RULES → config fingerprint mismatch → `_guard_config` raises on every call (reproduced live). Checkpoint 6 is best-effort, so the whole pour ran with zero graph linkage: **983-table backlog**, 20 of the top-30 tables are edge-islands (FEC 84.2M, AIS 58.1M, NMDB 19.1M, Open Payments 15.4M…), politics person-entities never entered the spine. → Run the guard's own prescription: `connect spine` → `incremental seed` → `connect-changed --scope all` (~1hr). Bundle D17/D18/D19 fixes into this one rebuild.

**[D03] The evidence.dev read lane was never built.** `scripts/instrument_snowflake_setup.sql` (RIPPLE_READER + role-bound PAT) and `serve/serve_wh.sql` (SERVE_WH + SERVE_MON) are complete, well-written, and **unapplied**. Live: no reader role, no serve warehouse; every surface runs as ACCOUNTADMIN. → One Snowsight session runs both files.

**[D04] CLAUDE_MCP_READONLY is not read-only AND is blind where it matters.** Holds CREATE TABLE/VIEW/STAGE on 18 schemas + OPERATE on ETL warehouses, yet has zero SELECT on CATALOG, V_STATE, marts, staging, or CONNECT (catalog views rebuilt without COPY GRANTS strip its grants). → Don't rehabilitate; create RIPPLE_READER, add COPY GRANTS to view-rebuild paths, strip the CREATE grants.

**[D05] The typed layer mostly does not exist.** All 789 generated staging views keep every column TEXT (generator header admits it); 171/233 reading-room views have zero casts (`COMPANIES.NONPROFIT_ORGANIZATIONS` = literally `SELECT * FROM LIBRARY_RAW.LANDING.FED_IRS_BMF`); flagship views are 332-TEXT-columns wide; donation amounts are strings. Typed surface today ≈ 73 marts + ~53 hand-built staging. → No-LLM type-inference pass in the generator, regenerate, re-point reading-room views.

**[D06] The heaviest tables have no staging at all.** 95 of 199 landed/modeled unstaged; 878 landing tables (115M rows) without staging; 60.9% of rows staged. Unstaged: NMDB 19M, USGS water 6.7M, ForeignAssistance 4.0M, BLS QCEW 3.6M, SBA loans/PPP, UNGA votes, FCC, NADAC… (Open Payments + USASpending are covered by hand-built intermediates.) → Value-first pass: hand-resolve grain for the top ~25, regenerate.

**[D07] `lifecycle='landed'` includes ~31 junk sources the density gate structurally can't catch.** Verified row-1 sampling: FED_CDC_WONDER = an HTML page; FED_FBI_CDE/FED_FINCEN_BOI/FED_FRA_SAFETY = loader-written excuse strings ("FBI_CDE_API_KEY not set…") landed as data rows; FED_CMS_HPT_MRF = a GitHub file listing; ~10 link-catalogs-as-data. 9 of 10 sub-10-row stubs have no density probe row. (Correction: fed_cbp_encounters is real data — don't demote.) → Content-reality gate + loader must raise instead of fabricating rows + demote the named list.

**[D08] Pre-gate junk successes are terminal.** `regrade_empty_loads.py` unapplied AND Windows-broken; the collision gate returns `already_cataloged` on any success row, blocking re-landing; 364 sources' latest success landed <50 rows. FED_FJC_IDB (4.1M rows, 100% empty) still logs `success` (though CATALOG already demotes it to `empty` via the partial 06-27 retro-audit). → Fix script path, run `--apply`, one-time retro-audit sweep, use D28's fixed `--include-landed` as the re-land escape hatch.

**[D09] Join-key facets blank on 75% of landed sources — including the crown jewels.** 149/199 empty JOIN_KEYS_STD; Open Payments (literal NPI column), IRS EO BMF (EIN), Medicare providers (NPI) all tier `NONE`. Catalog-driven join discovery returns near-nothing. → Run the existing measured-key machinery over all 199 via preview/--apply.

**[D10] Evidence.dev is 100% greenfield and the machine can't run it.** No Node, no npm, no Homebrew, zero repo references. → Install Node via nvm or the official pkg (not brew — brew isn't installed), `npx degit evidence-dev/template`.

**[D11] Evidence extracts query results at build time — the flagships will OOM a naive build.** INDIVIDUAL_DONATIONS = 84.2M rows; page queries want ≤100k. But: 188 of 232 reading-room datasets are <100k rows and can be sourced naively; only 22 exceed 1M — and those carry 186.5M of 196M reading-room rows. → Source .sql = START_HERE + naive small datasets + curated aggregates for the 22 flagships.

---

## WRONG — will bite, even off the critical path

**Data reality**
- **[D12] fed_eoir_case_data**: 12.6M rows in ONE tab-separated column with embedded NULs, `success`, in no repair queue; chunked path never applies min-rows; no 1-col tripwire. Recoverable in place (SPLIT on `\t`).
- **[D13] Open Payments 2022 invisible**: 13.25M rows from two `STATUS='error'` runs (out-of-vocab status → CATALOG falls to `scouted`), no registry row; `reconcile_op2022.py --apply` pending — but the rows are from failed streams; verify vs CMS's PY2022 count before blessing.
- **[D14] Lifecycle misclassifies downward too**: NMDB 19.05M reads `sampled` (the `LIKE '% sample%'` heuristic matched source-description text); TAGGS reads `failed` with a live table; USASpending bulk/FDIC/SAM/FEC-API sit at `sampled`.
- **[D15] Exact-duplicate sources**: fed_irs_eo_bmf = every fed_irs_bmf row loaded exactly twice **within one run** (3,949,660 = 2×1,974,830; identical EIN universe) — any nonprofit query double-counts. fed_sec_edgar vs fed_us_sec_edgar share a URL.
- **[D25] Stale marts with misleading comments**: AIS mart = 7.3M vs 58.1M landed while SHIP_POSITIONS claims "across 2024 — 7.3M reports" (landing itself is Jan 1–8 2024 = 20% of ALL Library rows); Federal Register mart 5k vs 94.7k.
- **[D22] Generator staged 53 junk taps** (≤5-row landing) into confident, test-passing views — laundering broken sources into trust.
- **[D23] Generated views silently drop up to ~2% of rows**: profiler accepts keys at 0.98 uniqueness while the header claims "proven duplicate-free"; 4 sampled views measurably lose 1–113 rows, and the dropped rows are likely real records (float SHAPE_AREA as a "key").
- **[D24] 4 hand-built staging views hard-broken by re-lands** (NPPES 333 renamed cols; NAAG/slavevoyages/IE-CRO invalid identifiers) — and the 9.6M NPPES mart is `select * from` the broken one, so it can never rebuild. Notably IE CRO re-landed 818,934 REAL rows on Jul 5.

**Engine / catalog**
- **[D17] NAICS/SIC tiered as STRONG entity keys**: theoretical 10^6 value-space vs ~2,500 in use → ~70% of the headline graph is shared-vocabulary co-occurrence, not entity linkage. Honest entity-grade graph ≈ 378 STEEL + ~150 entity-STRONG + 789 CORROBORATED. (Careful: measured-domain fix is booby-trapped by concatenated multi-code junk columns.)
- **[D18] ZIP never truncates to ZIP5**: NPPES 8.7M ZIP9 rows can never equi-join LEIE's ZIP5 (live keysets: 3.36M nine-char vs 251k five-char values). Guts GEO + NAME@ZIP. NORM_RULES change → bundle with the D02 rebuild.
- **[D19] Edges don't record join columns**: no A_COL/B_COL in the warehouse table; the top STEEL edge reproduces ONLY on SPONS_DFE_EIN (the literal EIN column normalizes to NULL on every row → naive join = 0 rows) — and for this edge the column knowledge exists NOWHERE (not even the JSON). An edge that can't name its columns is a rumor, not a receipt.
- **[D20] register.py's facet guard self-defeats**: `COALESCE` fed non-null defaults ('UNCLASSIFIED', `[]`, 'NONE', False) — every re-registration clobbers curated facets. Fix BEFORE the D09 backfill or it erodes.
- **[D26] V_STATE's stale-mart metric double-broken**: `NOT LIKE '\_RESTORE%'` without ESCAPE (never fires) + a Jul-4 metadata sweep bulk-bumped LAST_ALTERED — reports one false positive, misses every true positive.
- **[D27] Snapshot-replace destroys the good table BEFORE the density verdict**; SHA-skip trusts run history over table state. (`_latest_success_rows` has one caller — politics — but zero in the main lane.)
- **[D28] `registry_batch.py --include-landed` is broken**: selects candidates, burns recon, then the collision gate skips them anyway (flag never threaded through). One-line fix; it's also the D08 escape hatch.
- **[D21] 182 orphan staging views in Snowflake with no model on disk** (105 rename leftovers = TWO live views per source; 77 from deleted models) + 13 disk models never materialized. dbt can't rebuild, test, or drop them.
- **[D29] Politics marts wipeable by one selector-less `dbt build`** — only guard is a YAML comment; 7 of 9 politics staging views they ref don't exist live, so a build clobbers rather than fails. Recoverable via the Python builders, but define the safe build in config, not memory.

**Ops / hygiene**
- **[D16] Zero working refresh automation**: launchd plists never installed, LINK tier never ran (would crash on the D02 guard), 1 enabled acquire recipe, and RIPPLE_INGEST_BOT fails 100% on pre-rename `RIPPLE_*` database names.
- **[D30] 6–8 scripts still Windows-hardcoded** (`c:/Code`) — including both MCP grant scripts (the templates for evidence.dev grants) and `regrade_empty_loads.py`. Politics loaders are NOT among them (stale memory).
- **[D31] Evidence.dev auth**: connector supports only user/password, key-pair, browser, okta. PAT-as-password works (repo already does it; live PAT good to 2027-07-05) but couples BI to your personal rotating credential. Durable: SERVICE user + key-pair — needed only when you publish/CI.
- **[D32] The 07-05 tap-repair pour half-failed and nothing recorded it**: 7/13 complete, 6 failed (fjc_idb needs the parse fix, not a re-URL), 5 key-gated never attempted; runbook still reads as untouched.
- **[D33] Credential sprawl**: 9 active PATs incl. one unrestricted to 2027-06-19 and the un-revoked old ACCOUNTADMIN PAT; `keys_ledger.json` stale (its own checker returns BLOCK — trains you to ignore it); 4 tracked API keys unset. (Correction: ANTHROPIC_API_KEY IS in .env.)
- **[D34] dbt CI ships ACCOUNTADMIN into GitHub Actions** while RIPPLE_TRANSFORM_RW exists with exactly the right grants (must switch user AND role: RIPPLE_INGEST_BOT + RIPPLE_TRANSFORM_RW).
- **[D35] heartbeat rewrites COMPUTE_WH's statement timeout with no restore** (mitigated: something reasserts 2400s between ticks).
- **[D36] usaspending_load.py**: bare `--run` still snapshot-replaces the 6.3M-row contracts table with ~1 day of data (this file only; the other deprecated loaders are safe).
- **[D37] propose_snapshot_flag.py collides with the repurposed TEMPORAL_COVERAGE column** — `--apply` would clobber scout-written coverage text on 4 of its 8 targets. Retire or re-column.
- **[D38] Bare pytest on this Mac runs ZERO tests**: one PEP-604 annotation under Python 3.9 kills collection. One-line fix; suite is otherwise 414-green.
- **[D39] The state ledger is broken**: build-state 2 days behind (the staging generator — the most evidence.dev-relevant thing ever built — is invisible); the 07-06 handoff commit message is "sadfsadf"; ≥8 handed-to-Chris steps have no run/skipped record anywhere; decisions.total=0.
- **[D40] Prose numbers rotted beside the ban on prose numbers**: "20,696 connections" in 11 files (warehouse says 0/1,074); README "86 dbt models" vs 905 on disk.

**From the completeness critic**
- **Publishing legality is a no-op**: REDISTRIBUTION_RESTRICTED is NULL on all 199 landed (so the guard passes everything), and CATALOG exposes no license/cost columns. Matters the day evidence.dev output leaves your laptop (ACLED-class licenses, CC BY-SA copyleft).
- **DR designed, never executed**: `backups/dr/` is EMPTY. The registry — the one un-regenerable asset — has zero off-Snowflake backup, and a control-plane DROP has already happened once in this account's history.
- **No dbt source-freshness blocks anywhere** despite `_INGESTED_AT` on every table — the cheapest staleness detector, absent.
- **Semantic navigability**: 801/913 staging models are hash-named portal slugs; 666 say "spine not determined"; zero column descriptions. For a human writing SQL, names are the interface.

---

## FUNKY — worth knowing, not urgent

- Sampled data presents as full datasets everywhere; no completeness signal at any layer (→ Q4).
- Scale headline is ~10x breadth-inflated: 87.5% of tables are portal samples with 1.2% of rows.
- Generated tests are largely tautological (unique-test the key the QUALIFY just deduped).
- CATALOG can't see the new staging layer: `modeled`=25 while 900+ landing tables have live staging views — the biggest modeling event in repo history is invisible to navigation.
- "9.79M entities" = 98.1% NPPES; 9.7% multi-source; `SPINE_ENTITY` now means two unrelated things (registry column vs CONNECT schema).
- Chunked resume can silently lose rows if generated fetch honors `resume_from_row` (double-skip); watermark read swallows all exceptions.
- SID minting: "St. Louis Crime Data" mints `st_louis_crime_data` as a STATE source.
- WPRDC portal crawled twice under two slugs → 158 perfect registry duplicate pairs.
- `DBT_CROGERS` (a personal dev-target name) is becoming the permanent address of the staging layer — rename before evidence.dev queries freeze it.
- Requirements sprawl (3 files, contradictory pinning); `.mcp.json` depends on an env var no shell exports.
- DR DDL codifies a 30-credit budget vs live 300 — a fresh-account rebuild would self-strangle.
- RIPPLE_WH/DBT_WH sit at the 48-hour default statement timeout.
- CLAUDE.md's "non-negotiable stack … never suggest outside it" now forbids the tool you chose — amend it or every future agent session fights evidence.dev.
- build-state.md is structurally unusable as a state file: 1,460 lines, ~85% history, SEVEN competing NEXT ACTION sections.

---

## QUESTIONS FOR CHRIS

1. **Q1 — Is evidence.dev the canonical serving surface, and what does it see?** Recommend: THE_LIBRARY as the single door (233 curated views), full-warehouse RIPPLE_READER grants so ad-hoc SQL still works, and amend CLAUDE.md's stack line + the blueprint's SERVE section (which currently says Streamlit-in-Snowflake).
2. **Q8 — Deployment: local-only, static self-host, or paid Studio?** (Evidence Cloud is sunset.) Recommend local-only `npm run dev` now — zero credential exposure, and it defers the PII/license questions until the Publishing Layer is actually in scope.
3. **Q3 — What does "connections" mean for the query surface?** Retarget INC→CONNECT_EDGES and drop INC, or bless INC? Should the BI-facing view expose only STEEL/entity-STRONG/CORROBORATED, with NAICS/SIC/ZIP as a separate "shared dimensions" surface? Rebuild cadence vs budget?
4. **Q2 — Politics dbt marts: mirrors or owner?** Decides the D29 fix (disable in dbt_project.yml vs views-over-canon vs make Python the model).
5. **Q5 — Which SID survives each duplicate pair** (irs_bmf/irs_eo_bmf, sec_edgar/us_sec_edgar, WPRDC twins)? And are ENTITY_TYPES/THEMES required for "done" or best-effort?
6. **Q4 — Should load scope (sample/bounded/full) be first-class** in INGEST_RUNS + registry? 364 landed sources' latest success is <50 rows and nothing says whether that's the whole dataset.
7. **Q6 — Is single-column RECORD-as-JSON landing a blessed pattern** (wayback/subawards/epstein-library) or an accident to forbid? Determines the EOIR-class tripwire design.
8. **Q7 — Which machine is canonical, and is ANYTHING scheduled anywhere right now?** The weekly DR export may be scheduled nowhere; `backups/dr/` is empty.
9. **(Critic) Publishing governance for personal data** (NPPES addresses, named-physician payments) — only needed when output goes public, but decide before it does.

---

## THE ROADMAP TO EVIDENCE.DEV

### Phase 0 — First chart this week (~half a day, mostly one Snowsight session)
1. Install Node 22 (nvm curl installer or official pkg — Homebrew is NOT installed).
2. Snowsight as ACCOUNTADMIN: run `serve/serve_wh.sql`, then `scripts/instrument_snowflake_setup.sql` top-to-bottom → SERVE_WH + SERVE_MON + RIPPLE_READER; mint the role-restricted PAT; add `SNOWFLAKE_SERVE_PAT` to `.env` + a row in `infra/keys_ledger.json`.
3. `npx degit evidence-dev/template ripple-evidence && npm install`. Connection: authenticator `snowflake`, user CROGG23, PAT as password, role RIPPLE_READER, warehouse SERVE_WH, database THE_LIBRARY.
4. First sources: `catalog.sql = SELECT * FROM THE_LIBRARY.PUBLIC.START_HERE` (232 rows) + naive selects for any of the 188 sub-100k datasets + 2–5 curated aggregates per flagship (the 22 >1M-row datasets). Hand-cast TEXT columns in source SQL until Phase 3 (`TRY_TO_NUMBER`, `TRY_TO_DATE`).

### Phase 1 — Make "landed" mean landed (2–3 sessions; do BEFORE building many pages)
- Mechanical: fix the `c:/Code` paths (D30) + the pytest 3.9 annotation (D38) + `--include-landed` threading (D28) + register.py COALESCE clobber (D20 — before anything re-registers).
- Retro-audit sweep: fixed `regrade_empty_loads.py --apply`, plus density + single-column tripwire + HTML/banner matcher over every landed table head → demote the D07 list (~31, minus cbp_encounters).
- CATALOG lifecycle fixes: add `error` branch (rescues OP2022 visibility), fix the `' sample'` message false-positive (rescues NMDB 19M), success+table ⇒ landed.
- Data repairs: EOIR re-parse in place (SPLIT the 1 column); OP2022 decide re-land vs bless (verify against CMS PY2022 count); dedupe fed_irs_eo_bmf; rebuild the 4 stale marts + regenerate the 4 broken staging views (IE CRO's 818k re-land is real data waiting); fix the SHIP_POSITIONS comment.

### Phase 2 — Light the graph (1–2 sessions + ~1hr compute; the guard already demands the rebuild)
- Bundle INTO one rebuild: ZIP5 truncation normalizer (D18) · NAICS/SIC demoted to vocab tier + measured key domains (D17, mind the concatenated-code junk) · A_COL/B_COL added to the edge schema (D19) · writers retargeted at CONNECT_EDGES (D01).
- Run: `python -m connect spine` → `python -m connect.incremental seed` → `connect-changed --scope all` (drains the 983-table backlog; politics person-entities finally enter).
- Backfill JOIN_KEYS_STD measured for all 199 landed (D09, preview/--apply).
- Ship `V_CONNECTIONS` / `V_TABLE_CONNECTIVITY` + grant to RIPPLE_READER → evidence.dev can render the join map from SQL, with join columns named.

### Phase 3 — Type the Library (parallelizable with Phase 2)
- Generator upgrades: no-LLM type inference (profile → TRY_TO_NUMBER/TRY_TO_DATE) · row-count floor so junk taps don't get staged (D22) · uniqueness=1.0 for the "proven" claim or a loud header + parity test (D23) · emit DROP for renamed outputs (D21).
- Regenerate; reconcile the 182 orphan views against manifest; hand-stage the top ~25 by value (D06 list).
- Re-point the 171 raw-backed THE_LIBRARY views at typed staging. Decide the `DBT_CROGERS` schema name NOW, before saved evidence.dev queries freeze it.

### Phase 4 — Keep it alive (background)
- Install the launchd heartbeat plists (README exists); unblock LINK after the rebuild; init reconcile watermark honestly.
- Fix RIPPLE_INGEST_BOT's `RIPPLE_*`→`LIBRARY_*` config; point dbt CI at RIPPLE_INGEST_BOT + RIPPLE_TRANSFORM_RW; revoke the unrestricted + old-admin PATs; refresh keys_ledger.
- **Run `export_control_plane.py` today and schedule it weekly** — the registry currently has zero off-Snowflake backup.
- Add `freshness:` + `loaded_at_field: _INGESTED_AT` to dbt sources; surface staleness as a trust badge on evidence.dev pages.
- Fix V_STATE's stale-mart metric (ESCAPE clause + rowcount-based drift).

---

*Full machine-readable findings: workflow wf_8488df0d-63a journal. Every defect above was independently re-verified (files re-read, SQL re-run) by an adversarial agent before inclusion; corrections from verification are folded in.*
