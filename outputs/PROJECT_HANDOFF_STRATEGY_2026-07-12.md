# Ripple — Full Project State Handoff (2026-07-12)

Compiled for a strategy/brainstorm session. Facts only, sourced from CLAUDE.md, OVERVIEW.md, README.md, build-state.md (full, all ~1,630 lines), all 15 session memory files, docs/RIPPLE_FOR_THE_FOUNDER.md + RIPPLE_DESIGN_BRIEF.md + RIPPLE_FOR_EVERYONE.md, and the outputs/ artifact set. No recommendations included by design.

---

## 1. What This Is

**One sentence (from the founder doc):** Ripple turns any public dataset on the internet into clean, connected, queryable data — and automatically finds the places where two datasets contradict each other in a way that smells like a story. Banned doctors still cashing pharma checks. Debarred companies still winning federal contracts. Sanctioned ships still broadcasting. That's the product; everything else is plumbing.

**Mission:** Chris (SQL ~6yr, Snowflake+dbt, new to some tooling) is building "the Library of Alexandria for the data analyst and investigative data analyst." Solo-built.

**Dual goal:**
- Floor: a portfolio proving professional-grade skills without needing a title.
- Ceiling: quit day job, go solo as freelance developer / digital investigative journalist.

**Three-layer platform:**
1. **The Library** — Snowflake warehouse. This repo builds/maintains it.
2. **The Catalog** — source registry + connection map (`LIBRARY_META.REGISTRY.SOURCE_REGISTRY`, `INGEST_LOGS.INGEST_RUNS`).
3. **The Publishing Layer** — website turning findings into data-viz stories. **Does not exist yet — visual identity is fully undecided, greenfield.** Explicitly deferred as an engineering priority, but a full design brief exists for whoever eventually builds it (§7).

**Stack (non-negotiable):** Python, Snowflake, dbt, Plotly.

**Operating model:** Chris is the foreman — sets goals, approves checkpoints, does no manual work. The agent (Claude Code) executes everything. Casual/direct tone, full-code-block convention, map-not-essay formatting.

**Strategic pivot (2026-06-29, standing):** stop hand-crafting investigations; build the FOUNDATION first. Detector/lead/pattern work and the publishing layer are explicitly deferred and frozen as-is (existing detectors keep running; no *new* ones are being designed). Foundation = three engines (ACQUIRE / CONNECT / SERVE) + ORGANIZE + TRUST, 7-phase roadmap (blueprint: `outputs/alexandria_foundation_BLUEPRINT_2026-06-28.md`). Phases 0–3 shipped; 4–6 are earn-into.

**Trust doctrine (governing every finding, standing policy):** "AI is the forklift, not the witness." No claim rests on AI judgment. A finding must survive a hostile skeptic who assumes the AI is garbage: hard-ID grounding, reproducible SQL, primary-source gov URLs, base-rate context, a pre-written best-innocent-explanation + the check that refutes it, calibrated (not LLM-emitted) confidence, Chris's recorded sign-off. Concretely enforced as **fact vs. lead**: same hard government ID (NPI/EIN/CIK/UEI/IMO/…) across two sources = FACT, publishable; shared name only = LEAD, human-review-only, never auto-merged, never stated as true.

---

## 2. The Actual Moat — Connection Engine, Entity Resolution, Detectors

This is the core IP, not just plumbing. Three sub-systems, in increasing order of trust required to use their output.

### 2a. The connection graph (`connect/`, ~4,800 lines)

Turns landed tables into scored connections. Pipeline: **fingerprint** (which IDs each table carries, how populated) → **overlap** (do the *values* actually intersect, not just "both have an ID-shaped column") → **discover** (the edge list, tiered) → **explore** (interactive Plotly map).

**Six confidence tiers** (last full measurement, 2026-06-28, pre-ZIP5-fix — see §4 for the 2026-07-06 rebuild that changed these numbers):
| Tier | Meaning | Edges (06-28) |
|---|---|---|
| STEEL | same hard ID | 350 |
| STRONG | same domain ID (NAICS, LEI, etc.) | 9,396 |
| BRIDGE | joined transitively through a 3rd dataset's key | 133 |
| CORROBORATED | name + place agree | 769 |
| GEO | same location only | 5,633 |
| PROBABILISTIC | fuzzy name only | 4,415 |
Total ~20,696 edges at that measurement; 638 connected / 82 isolated datasets. (The 2026-07-06 fingerprint+discover rebuild changed these to STEEL 473 / STRONG 2,224 / total 41,241 with GEO now 53% of the graph after a ZIP5 normalizer fix — see §4/§5. Both measurements are real, at different points in time; always re-query for current.)

**Node/edge encoding conventions (load-bearing, used by every visual artifact):** node size = degree (connectivity), never row count (sizing by rows once buried everything under a few giant tables); edge width = actual matched record count; color = trust tier, never topic (this is deliberate — "trust comes from the strength of the link, not the topic").

### 2b. The bridge layer (crosswalks between domains)

Built 2026-06-24. **The original premise was wrong and got corrected on contact with real data:** the plan assumed a public NPI↔EIN crosswalk existed inside NPPES. It doesn't — CMS masks EIN in the public NPPES file (`<UNAVAIL>` on 9.6M of 9.6M rows), and PPP/SAM redact it too. **A public NPI↔EIN hard crosswalk essentially does not exist anywhere** — that linkage can only ever be an entity-resolution/corroboration job, not a hard join. The achievable bridge instead: CMS "Facility Affiliation" (CCN↔NPI, 2.24M rows, 0% masked) — poured deterministically (LLM-free) along with 7 CCN facility datasets, taking bridge edges 14→59 and making every CMS facility type reach NPPES (9.6M providers) via CCN.

### 2c. Entity resolution — the confidence ladder (Fellegi-Sunter), `connect/match.py` + `calibrate.py`

A full statistical record-linkage system, built and calibrated over ~6 sessions (2026-06-25), separate from and more rigorous than the raw connection graph. Governs when two *fuzzy* (non-hard-ID) records may be treated as the same entity.

- **Blocking** (candidate generation): naive ZIP-based single-pass blocking only reached 23.7% of true matches. Fixed with 3-pass unioned blocking (surname-sound+ZIP / surname-sound+first-initial-anywhere / exact-name-anywhere) + a block-size cap (`PAIR_BUDGET=100k`, drops and logs mega-blocks) → candidate recall **95.9%**.
- **Scoring**: a genuine Fellegi-Sunter match-weight model (bits of evidence), features = surname (TF-rarity weighted) + first name (nickname-aware) + ZIP + street address (USPS-normalized) + middle initial — each three-state and LOG-guarded (present/absent/disagree). NPI is used as a label ONLY for evaluation, never as a feature (no leakage).
- **Calibration**: m/u probabilities estimated from ground truth with a **train/test split by person** (measured strictly out-of-sample) and tier labels set from **measured held-out precision** (Wilson lower-bound), not the model's self-reported confidence. Empirically validated: predicted ZIP agreement-rate 0.25 vs measured 0.246 (the framework is calibrated to reality); address-agreement false-positive rate for different people measured at 0.0002 (negligible).
- **Result (last calibration, persisted to `LIBRARY_META.CONNECT.MATCH_MODEL`/`MATCH_RUNGS`):** CONFIRMED tier (M≥11) → precision 0.876 (lower 95% CI 0.860), covering ~46% of all true matches. STRONG tier (M≥8) → precision 0.576, coverage 0.761. LEAD tier (M≥0) → precision 0.118, coverage 0.992. Name-only matching (no ladder) is flat ~0.036–0.12 precision at any threshold — cannot separate name-twins at all. **Auto-merge threshold (`recommend_HIGH`) is deliberately never reached (0.876 < 0.99) — nothing auto-merges, ever; this tier is a strong human-review recommendation, not a fact.**
- **Safety layer** (`connect/safety.py`): an append-only `DECISIONS` audit log (confirmed/rejected/retracted/stale, latest-verdict-wins), `gate_rows()` drops anything in the suppress set before publish, staleness auto-expiry. `leads.published()` is the single canonical publish-read gate.

### 2d. The entity spine (`connect/spine.py`)

Hard-ID-only resolution (same NPI/CCN/EIN/etc. value across sources = one entity; deliberately zero false-merge risk — cross-ID-type identity, e.g. NPI↔CCN, is a *relationship* not identity, so it is NOT fused). **9,678,735 entities resolved, of which 952,930 are multi-source** (appear in 2+ datasets). Each entity gets a content-addressed stable `ENTITY_ID` (a rebuild renumbers no one — proven) and a "golden name" chosen by an authority ladder (e.g. NPPES ranked above LEIE when they disagree on a doctor's name). Backed by `dossier.py` (CLI + HTML entity profile pages) and `entity_index.py` (search index).

### 2e. The detectors — where connections become story candidates

A detector ("JobSpec" in `connect/leads_specs.py`) is a declarative rule: a hard-key intersection between a "flag" list (banned/sanctioned/debarred/excluded) and an "active" list (paid/operating/funded/broadcasting), with optional name corroboration. Adding a new detector in an existing domain is config-only, not new architecture (proven: the original doctor-specific detector was generalized into this domain-agnostic engine in one session with the flagship output byte-identical after migration).

**Six detectors live as of the last full run (2026-06-28) — read this as a structural, persisted system distinct from the ad-hoc "lead hunt" reports (§6):**
| Detector | The pattern | Key | Leads |
|---|---|---|---|
| `banned_but_paid` | OIG-excluded doctor still appears in pharma payment records | NPI | **773** |
| `excluded_but_billing` | OIG-excluded provider still in Medicare Part D prescriber data | NPI | 236 |
| `banned_but_operating` | Excluded provider still active at a facility | NPI | 11 |
| `sanctioned_vessel_broadcasting_v2` | OFAC-sanctioned ship still broadcasting (all years) | IMO | 6 |
| `debarred_but_funded` | Debarred company still receiving federal money | UEI | 2 |
| `sanctioned_vessel_broadcasting` | OFAC-sanctioned ship still broadcasting (original, narrower) | IMO | 2 |

**Total ~1,030 leads, ALL sitting at `review_state='pending'`, `published=False`.** No detector currently sets the code's structural `auto_ok` auto-confirm path, so nothing has ever auto-published.

**The flagship finding, verified with a receipts methodology (2026-06-26, "how do we know it's not a clerical error"):** triangulated the `banned_but_paid` leads against NPPES as an independent third source. 327 of the (then-)338 leads were FACT-grade (surname agrees across all 3 federal sources: NPPES, LEIE, Open Payments); 13 held for manual check (registry blank); 1 held for a genuine surname conflict. 206 of 338 were paid ON/AFTER the exclusion date (the strict "paid while banned" claim); 185 were excluded before the observed payment window (still real, weaker framing). A reusable tool, `scripts/lead_receipt.py`, prints this 3-source receipt for any provider (NPPES identity + LEIE ban reason + Open Payments dollars + a timeline verdict + a confidence tier + verify-yourself government URLs). Flagship individual case: Eduardo Miranda (NPI 1285673012), excluded 2015, paid by pharma through 2024, 3-source corroborated.

**The known concentration risk (unresolved, explicitly flagged in the founder doc as the real bottleneck):** ~75% of all leads (773 of ~1,030) ride a single edge — LEIE × Open Payments on NPI. This is not a flaw in the engine; it's a direct function of which hard IDs are currently wired. **No new detector can fire without a new identifier landing** — e.g., a "shell-company contractor" story needs IRS EO BMF's EIN wired in; a "public company doing X" story needs SEC EDGAR's CIK (blocked today only by a fixable User-Agent bug in the fetch).

---

## 3. Architecture — The Four Verbs (Pipeline Mechanics)

```
SCOUT           COLLECT              CONNECT           EXPLORE
portal_recon →  library-onboarding → connect/       →  evidence.dev / outputs/*.html
(find sources)  (load them)          (wire them up)    (walk the map)
```
*(A fifth, human-only step — REVIEW — sits after EXPLORE: a person confirms a lead via `connect review` before it can ever be called true. This step is deliberately never automated.)*

- **`library-onboarding/`** — the collector. 6-checkpoint agent: RECON → SCRIPT → LOAD → DBT → REGISTRY → CONNECT. Chris approves each checkpoint (`go` / `edit [feedback]` / `skip` / `abort`).
  - Run modes: `--url <url>` (single), `--batch --queue <file.json>` (real pours, resumable via `onboarding_log.json`), `--batch` bare (legacy demo queue), flags `--yes` (unattended), `--skip-dbt`, `--limit N`, `--repair N`.
  - Load modes in `ingest.py`: **snapshot** (default, replace, SHA-idempotent), **incremental/C2** (watermark cursor, append, staging dedups on PK), **chunked/streaming/C3** (generator-based, bounded memory, resumable, for multi-GB single files — proven on NPPES ~9.6M rows and FJC IDB ~4.1M rows, crash-resume proven mid-load), **static scrape/C1** (BS4+lxml), **headless-browser scrape/C1b** (Playwright, for JS-rendered/bot-walled sources, `access_pattern=scrape_js`, autonomously chosen by recon on an empirical "blocked static, works rendered" signal).
  - Density/HTML gates exist (`assess_density`, `_reject_html`) but have known holes (§5).
- **`portal_recon/`** — the scout. Crawled open-data portals into a catalog of 338,520 datasets, tagged by join-key type. As of 2026-06-26 the "easy" connectable pool (~731 entity-key portal datasets) was already ~80% harvested (593 landed); the next portal net would be coarser (GEO/FIPS-based, not entity-key).
- **`connect/`** — the connector + explorer (§2). Steps: `fingerprint` (must always run first — samples tables, writes local JSON; running `discover` alone on a stale fingerprint is a documented trap) → `discover` (edges) → `spine`/`explore`/`dossier`/`leads`/`resolve`/`calibrate`/`review`/`safety`.
- **`serve/`** — legacy Streamlit reading room (superseded by evidence.dev as of 2026-07-06, kept as fallback).
- **`evidence/`** — the current SERVE surface: a full evidence.dev project (Node 22, user-space install). Extracts to parquet at build time (page queries want ≤100k rows — the "two-walls thesis" driving the 2026-07-07 leverage build, §5).
- **`viz/` + `ripple chart`** — the Investigator Instrument (2026-07-03): `python ripple.py chart "<SQL>"` → live editable Plotly chart + a runnable card in `investigations/`. Guarded read lane (`viz/sqlrun.py`): name-only joins badge as LEAD, raw `"CONNECT".LEADS` reads refused (routes to `V_LEADS_PUBLISHED`).
- **`ripple/`** — the control panel (`python3 ripple.py panel` → `localhost:8899`): KPI tiles, source browser, run/audit log, job runner with live-previewed refresh commands.
- **`loadkit/`** — shared loader toolbelt used by hand-written loaders (not the LLM agent): pre-flight gates (PAT/budget/dep checks before a load starts), atomic staging-swap loads (crash leaves the live table untouched), durable per-window checkpointing, a reconciliation "smoke" referee (ties a load's numbers to an independent source like OpenFEC as a *precondition* to going live), a windowed-pagination planner for cursor-hostile APIs, quarantining FEC fixed-width parsers. 31 offline unit tests, zero Snowflake/network dependency.
- **`politics/`** — deterministic Python-built US-politics domain spine (member crosswalk, committee/FEC bridges); dbt only mirrors/tests it (§6 — this workstream is at plan/audit stage, not yet executed at scale).
- **`infra/`** — warehouse infra as DDL (registry tables, views, monitors, heartbeat/keep-alive config).

**Snowflake account:** `ONEAFDA-UMB20733`, user `CROGG23`. DBs: `LIBRARY_RAW` (LANDING, all-TEXT — deliberate: sources lie constantly about type, so land as a dumb perfect mirror and cast later where you can see the junk), `LIBRARY_META` (REGISTRY, INGEST_LOGS, CONNECT schemas), `LIBRARY_STAGING`, `LIBRARY_MARTS` (dbt outputs), `LIBRARY_TOOLS` (hosts the read-only MCP server only, no data), `THE_LIBRARY` (friendly read-only views, human front door). Warehouses: `RIPPLE_WH` (ingest/connect, X-Small), `DBT_WH` (dbt), `COMPUTE_WH`, `SERVE_WH`/`SERVE_MON` (evidence.dev read lane, live but not yet the default connection).

**Naming convention:** `SOURCE_ID` = `<prefix>_<slug>` (`fed_`/`intl_`/`xc_`/`loc_`/`st_`); landing table = `UPPER(SOURCE_ID)`. Pipeline layers: LANDING (raw TEXT mirror, "bronze") → staging (`stg_<source>__<entity>`, "silver": rename/cast/dedup, views) → intermediate (`int_<source>_<description>`) → marts (`<domain>__<source>`, "gold": analytics-ready).

---

## 4. Current Scale

**Doctrine: never trust a number written in prose (including this doc) — it rots.** Canonical live counts: `LIBRARY_META.REGISTRY.V_STATE` (one row per metric) or direct `CATALOG` queries. The figures below are point-in-time snapshots, dated, not a live read.

- 2026-06-20: 45 landing tables, 23,788,352 rows.
- 2026-06-23/24 (connect engine built): 638 landing tables, ~24.3M rows, 12,804 connections across 547 datasets.
- 2026-06-24 (bridge layer): 646 tables, 14,694 connections (bridge edges 14→59).
- 2026-06-25 (faceted catalog live): registry 1,592 rows (1,506 + 86 run-orphans); lifecycle scouted 853/sampled 595/failed 59/modeled 34/empty 28/landed 20/stale 3.
- 2026-06-26 (portal firehose + Open Payments Load #1): +63 connected sources, +4,851 connections (→20,696 total), +15.4M rows from Open Payments alone.
- 2026-06-27/28 (75-issue coverage sprint): Library 61→101 landed/modeled sources (+66%, ~4.92M rows loaded); entity spine = 9,678,735 entities (952,930 multi-source); ~20,696 connections; ~1,647 catalog rows; "~101 sources with real trustworthy data" is the number the founder doc says to lead with externally (not the raw 638/720 landing-table count, which includes unverified freshly-landed and stub tables).
- 2026-06-28 reconciled figure: ~63 first-class sources (29 landed + 34 modeled, ~9 of "modeled" were broken stubs), 720 physical landing tables, 20,696 connections.
- 2026-07-01 reading room build: 160 datasets catalogued (61 marts + 99 mart-less landing), later refreshed to 232 (2026-07-04): THE_LIBRARY = 22 schemas, 233 views, 0 broken views.
- 2026-07-06 Fable audit: CONNECT_EDGES 0 → 20,907 → 41,241 after a fresh fingerprint+discover rebuild (STEEL 378→473, STRONG 9,396→2,224 after NAICS/SIC/NCES noise removed; GEO/bare-ZIP now 53% of the graph after a ZIP5 correctness fix traded one noise problem for another). Trustworthy core (`tier IN (STEEL,STRONG,CORROBORATED)`) ≈ 4,308 edges.
- Tap census (2026-07-01/02): 124 taps ON (99 landed + 25 modeled); ~1,516 turn-on-able (852 scouted + 7 queued + 657 sampled), of which ~900 are confirmed-keyless; ~1,386 keyless overall / ~129 free-key / ~21 paid; 1,090 carry a join key.
- Registry catalog carries 22 `DOMAIN_PRIMARY` values, `JOIN_KEY_TIER` (STEEL/STRONG/GEO/PROBABILISTIC), derived `LIFECYCLE` (scouted/queued/sampled/landed/modeled/stale/empty).

**Query to get the real current numbers:**
```sql
SELECT domain_primary, COUNT(*) FROM LIBRARY_META.REGISTRY.CATALOG
WHERE lifecycle IN ('landed','modeled') GROUP BY 1 ORDER BY 2 DESC;
SELECT * FROM LIBRARY_META.REGISTRY.V_STATE;
```

---

## 5. Build Timeline (condensed, chronological)

- **2026-06-16 — Repo created.** Initial commit; 5-checkpoint onboarding agent added same day.
- **2026-06-16/17 — Engine build.** First live sources onboarded (USASpending, SEC EDGAR, Federal Register, FDIC, Treasury debt, FDA). Registry-driven queue built and proven. Load modes C1/C1b/C2/C3 all built and proven live. Several real agent bugs found and fixed via live onboarding attempts (false-success on HTML scrapes, dbt-gen JSON truncation on wide tables, OOM on big files, streaming LLM calls needed for >10min operations).
- **2026-06-18 — Registry batches 3–5, ~40 more sources attempted.** DB rename (`RIPPLE_*` → `LIBRARY_*`); dead DBs dropped; MCP server relocated after a DB drop destroyed its original host.
- **2026-06-20 — Env recovery.** Fresh container, dead PAT recovered, dbt reconciled (ghost model removed, YAML bombs fixed), 53 models green.
- **2026-06-23/24 — Connect + explore engine built.** Library scaled 45→638 tables. `connect/` package built: fingerprint→overlap→discover→explore. Portal loader (LLM-free bulk ArcGIS/Socrata harvester) built. An adversarial audit found 23 issues; fixed (per-key NORM_RULES padding, a confidence gate killing chance-level "connections" — cut 809 raw edges to 307 honest ones), set-based O(n) discovery replacing an O(n²) crawl.
- **2026-06-24 — Bridge layer activated.** Discovered NPI↔EIN crosswalk doesn't exist (masked everywhere); pivoted to CCN↔NPI via CMS Facility Affiliation (2.24M rows). Bridge edges 14→59. First "banned but operating" ground-truthed finding (38 facility affiliations of 11 excluded providers).
- **2026-06-25 — Entity layer + confidence ladder + faceted catalog, all in one intensive day.** Built: hard-ID-only entity spine (9.68M entities), dossier/search, name/address normalization, gated fuzzy resolver, the repo's first eval harness + CI. Then designed and built the full Fellegi-Sunter confidence ladder over 6 builds (blocking fix, FS scorer, address/middle-initial features, out-of-sample calibration, safety/audit layer) — see §2c. Separately built the faceted catalog (`CATALOG` view, 11 new facet columns, controlled vocabulary, review queue) after an 11-agent adversarial stress-test.
- **2026-06-25 (later) — Money + maritime domains.** OFAC SDN landed (19,115 rows); a new `sanctioned_vessel_broadcasting` detector found 2 Iran-sanctioned tankers broadcasting under changed names. USASpending + SAM Exclusions loaders built. Generalized the "banned but active" pattern from a doctor-specific query into a domain-agnostic declarative detector engine (JobSpec dicts).
- **2026-06-26 — Portal firehose + missing-data load queue + audit/hygiene.** Ran the portal harvester (+63 sources, +4,851 connections); found the connectable pool was ~80% drained. An 11-agent audit found the catalog's stub-mart gate had a floor hole (letting 7 broken 1-row marts read as "modeled") and that 'epstein' was the only theme in the system, over-applied to 193 sources including NPPES/AIS/SEC-EDGAR (zero actual connection). A 12-cluster research workflow found the core problem was LOADING, not scouting: 1,506 sources scouted, only 54 landed (~3.5%). Shipped the `debarred_but_funded` detector (2 leads, flagship: Bella Mia Donna LLC, $1.29M in DoD contracts while DLA-debarred). **Loaded Open Payments (15.4M rows) same day** → the `banned_but_paid` detector fired for the first time (338 leads) → verified via the 3-source receipt methodology (§2e).
- **2026-06-27 — 75-issue coverage map + backend readiness audit.** Compared the Library against a "World's Top 75 Issues 2026" list; loaded 40 sources (~4.92M rows) same session (scope decision: clean public sources only, keyless-first, budget raised to ~100cr for the sprint — see §8). Separately, a 37-agent audit found the trust chain was broken (a 100%-empty 4.1M-row table had logged `success` and read as a trusted mart) — shipped a density gate and a live leads-overlay viz.
- **2026-06-29 — Alexandria pivot.** Strategic reframe: build the foundation before more detective work (§1). Blueprint written; incremental connect (Phase 2) built and seeded live same window. Politics-domain Phase 0 gap-mapping also started this day (§6).
- **2026-06-30 — 07-01 — Politics domain planning + frontier scouting series (parallel workstreams, both plan-stage).** See §6 and §7.
- **2026-07-01 — Snowflake housekeeping + THE_LIBRARY reading room v1 + pour-readiness hardening.** Dropped expired trial mounts, snapshotted+dropped 12 broken marts, added plain-English comments across the warehouse, built the first friendly-name reading room (160 datasets). Separately: a 64-agent pour-readiness stress test fixed 7 code-side blockers (null-handling, batch resilience, unattended mode, Windows crash, timeouts) so a full unattended pour became possible; a follow-up 25-agent QA round caught fixes composing adversarially and closed them.
- **2026-07-02 — Fable audit → instrument-hardening.** Full-repo audit fed a single hardening pass; `V_STATE` established as the sole source of truth for scale numbers going forward.
- **2026-07-03 — The Investigator Instrument shipped.** `ripple chart` — ask any table a question, get a real editable Plotly chart plus a runnable card. Live-proven on 4 domains; safety lane proven (LEAD badging, DML refusal).
- **2026-07-04 — Library Map + reading room refresh + Control Panel.** Interactive ER-style connection map; reading room refreshed 160→232 views; the full control panel shipped (44 hardening findings fixed across two review rounds).
- **2026-07-05 — PAT rotation, spine-entity backfill.** Backfilled `SPINE_ENTITY` for grain-proven/entity-unknown sources: 462→559.
- **2026-07-06 — Fable audit (54-agent) + evidence.dev Phase 0.** Full repo+warehouse stress test: engineering verdict solid, 40 confirmed defects in four gap areas (graph dark, truth-layer lies both ways, typed layer thin, no read lane). Same session: stood up evidence.dev end-to-end, lit up the connection graph (0→41,241 edges), shipped the read-only lane, ran a DR export, fixed ~10 code defects, fixed catalog lifecycle mis-gradings. Registry-driven staging generator built (811 sources resolved).
- **2026-07-07 — Leverage hunt + 8 evidence-readiness scripts.** Established the "two-walls thesis" (warehouse splits at evidence.dev's ~100k-row cap into a TEXT problem and a TOO-BIG problem; cost/perf explicitly ruled out as a lever). Built 8 preview-tested scripts, all awaiting Chris's `--apply` (§9).
- **2026-07-08 — Lead hunt + PAT revocation.** A *separate, ad-hoc* 43-agent hunt over the live warehouse (distinct from the persisted detector engine in §2e) produced 8 verified investigative leads (`outputs/LEADS_2026-07-08.md`). Also shipped a script to revoke stale programmatic access tokens.
- **2026-07-09 — Lead sheet.** Added a formatted lead sheet for July 2026 with detailed analysis and SQL receipts (latest commit, `402c43f`).

---

## 6. Politics Domain Workstream (separate track, plan/audit stage — nothing new landed by these docs)

A parallel effort to build a dedicated US-politics data spine, started 2026-06-29/30. **As of the last documents produced (2026-06-30), this is entirely at the planning/audit stage — no new politics-specific data has been confirmed landed by the planning documents themselves**, though later commits (`bf1a7df` 2026-07-06 SPINE_ENTITY backfill, `cac68bb` 2026-07-06 registry-driven staging generator) suggest incremental progress since.

**Coverage audit finding (411 sources surveyed):** federal Congress core (DW-NOMINATE scores, roll-calls, bill status, FEC summary money) is strong and modeled. Eleven categories are at zero: federal lobbying, bill text, committee membership, nominations, all state legislative data, election results at any level, interest-group scorecards, opinion surveys, 527s/dark money, political ads, earmarks, lower judiciary, PTR/financial disclosure, local politics. `lda.senate.gov` (the lobbying-disclosure host) died the same day as this audit.

**"Dark frontier" framing:** a hard wall at the county line — above it, everything keys to bioguide/ICPSR/FEC/EIN (a "steel" spine); below it (state/local), there is no unified national person key, ever — only geography or fuzzy name-match. Deliberately deferred until the federal spine is solid. Several sunsetting/single-maintainer sources flagged as "grab now or lose forever" (FiveThirtyEight archive, a personal-Dropbox-hosted DIME dataset, a personal-Squarespace-hosted Judicial Common Space dataset).

**Concrete code-level defects found by an adversarial stress-test (31/37 confirmed material) — not yet all fixed:** `build_money_spine.read_fec` splits FEC's pipe-delimited files with no quotechar and pads/truncates malformed rows silently instead of failing — a real money-figure corruption risk if run as-is. The itcont (individual contributions) firehose file would OOM if loaded as planned (30–40GB, zero streaming code exists yet in the politics loaders). `usaspending_load.py` reuses the *contracts* column list for *assistance* data, silently dropping CFDA/FAIN/URI. A proposed swap to a simpler SAM CSV would be a regression (the existing API loader has UEI+dates; the CSV drops UEI, disabling the debarred_but_funded detector).

**The credential landmine (new, not in prior memory):** `~/.snowflake/connections.toml` points at a *different* Snowflake account (`UKB67948`, OAuth) than `.env` (`ONEAFDA-UMB20733`, PAT) — dbt and the `snow` CLI read the toml, not `.env`, so an unguarded dbt run in this domain could silently target the wrong account.

**A full build runbook exists** (`outputs/POLITICS_BUILD_RUNBOOK.md`), gated behind a purpose-built toolbelt (`loadkit/`: pre-flight gate, atomic staging-swap, an independent-source reconciliation "referee" as a precondition to any load going live, durable per-window checkpointing, a windowed-pagination planner, quarantining FEC parsers — 31 offline tests, zero network dependency). Six-phase order: P0 human gate (PAT/budget/checkpoint-table, **PAT step already done**) → P1 cheap bolt-ons + small FEC files (also fixes committee-membership scope, which turned out to require flattening two YAML files, not one trivial file) → P2 USASpending assistance+sub-awards → P3 SAM exclusions via the windowed API (not the simpler CSV, deliberately) → P4 LDA lobbying 2021-2026 → P5 the itcont firehose (last, gated behind a penny-reconciliation referee against OpenFEC) → P6 deferred (1999 LDA backfill, freshness-ledger entries). Tracked as GitHub epic #44 with per-phase issues #33–#43.

**Known duplicate/stale source IDs requiring reconciliation, not fresh loads:** committee-membership, House PTR, IRS BMF, Senate LDA (×3 variants), bill text, Voteview (×3), SCDB — `register_political_sources.py` is append-only so these need scoped UPDATE scripts, not new INSERTs.

---

## 7. Forward Scouting Backlog — The Frontier (137 datasets not yet in the Library)

A 5-round scouting exercise (2026-06-30 → 2026-07-01) surfaced 137 publicly-obtainable datasets that would compound with the existing Library but are not yet acquired. Full list: `outputs/ripple_frontier_MASTER_LIST.md` (+ per-round detail docs with evocative pairings, and `outputs/ripple_nonobvious_investigations_2026-06-30.md` for verified cross-domain angles on data already landed). Organized thematically:

- **Round 1 — the present** (~29 items): Census/ACS, HUD geography crosswalks, BLS employment, OSHA, FDA FAERS, NIH RePORTER, CMS price transparency, SBA PPP, SEC private-fund/subsidiary filings, USASpending sub-awards, county parcels, federal lobbying, congressional stock trades, state campaign finance, IRS 990, HMDA, FEMA flood claims, FAA, customs bills of lading, OFAC crypto wallets.
- **Round 2 — deep time & the seams** (~30 items): full-count historical census (1850-1940), Chronicling America newspapers, SlaveVoyages/Freedmen's Bureau, CDC WONDER mortality, patent databases, clinical trials, SEC insider trades, pension funded-status, violent-death records, EOIR immigration courts, ICE detention, FCC political ad/ownership files.
- **Round 3 — offshore, future, hidden** (~30 items): OpenSanctions, UK Companies House beneficial ownership, Global Fishing Watch, ICIJ Offshore Leaks, FinCEN SAR stats, shell-jurisdiction registered-agent data, organ transplant registry, cannabis licensing, the BIS Entity List, IRS donor-advised-fund and 527 filings, whistleblower/retaliation records.
- **Round 4 — populations & seams the graph couldn't see** (~20 items): tribal/ANC ownership flags, territories' disaster funding, prison-phone rate filings, civil-asset-forfeiture data, police-use-of-force crosswalks, disability-appeals judge data, dialysis facility reports, book-ban index.
- **Round 5 — local & liberated** (~24 items): state-level court case data (Virginia 33.5M cases, Cook County, NY bail), a FOIA-litigated ICE arrests dataset, House Epstein-estate files, NYC building/violation-by-owner data, state tax-incentive-vs-jobs-delivered data, fracking chemical disclosures, EPA leak/discharge data, EU procurement corruption scoring.

---

## 8. Known Issues / Open Defects (as last verified)

From the 2026-07-06 Fable audit (40 confirmed, 0 refuted) plus other sessions:

1. **Truth layer lies both ways.** ~31 junk sources still read `landed`. `FED_FHFA_NMDB` (19M rows) was misread as `sampled`. `FED_CMS_OPEN_PAYMENTS_2022` (13.25M rows) was invisible. `fed_irs_eo_bmf` is an exact 2× duplicate of `fed_irs_bmf`. Some fixed live 2026-07-06; reconcile/dedup scripts for the rest await `--apply` (§9).
2. **Typed layer thin.** All 789 generated dbt staging views are all-TEXT. 171/233 THE_LIBRARY reading-room views are zero-cast. 95/199 landed sources are unstaged entirely. Typing script built, preview-tested, awaiting apply.
3. **No production read lane (partially closed).** `RIPPLE_READER`/`SERVE_WH` are live and verified read-only, but no role-restricted serving PAT exists yet — evidence.dev still runs on an interim ACCOUNTADMIN-scoped PAT (a page query could in principle `DROP DATABASE`). Minting the restricted PAT requires a manual Snowsight step Chris hasn't done yet.
4. **Connection graph composition.** 53% of the current batch graph is weak bare-ZIP geographic coincidence (a ZIP5 normalizer fix traded a NAICS/SIC/NCES noise problem for a ZIP noise problem). A tier-filtered view (`V_CONNECTIONS_CORE`, ~4,308 edges) exists; structurally excluding bare ZIP/FIPS edges (like NAICS was excluded) is an open, deferred design call.
5. **Empty-tables root cause (systemic).** Recon frequently targets a source's human-facing HTML help/landing page instead of the real file/API endpoint. Two gates have holes: `_reject_html()` only fires on exactly-1-column HTML; `assess_density()` has no minimum-row-count floor. Three failure classes: ~25 broken curated taps (fixable by repointing URL), ~9 sources where real data IS landed but a stale dbt model shows only 1-3 rows (data already present, just needs a regenerated staging model), ~284 portal auto-harvest churn entries (expected noise, isolated).
6. **Warehouse query traps (durable, must check before analysis):** Open Payments is split by year into disjoint tables (2023/2024), though the `banned_but_paid` detector already reads a unioned view — only *ad-hoc* queries against the bare table are at risk. `FED_NOAA_AIS` is a single stale 8-day Jan-2024 snapshot pre-dating the entire 2025-26 Iran sanctions wave (any "sanctioned vessel in US waters" match off it is reverse-causality unless date-checked). LEIE's `EXCLDATE` needs explicit date parsing (`TRY_CAST` collapses to 1970); LEIE's NPI is the literal string `'0000000000'` on ~89.6% of rows — a naive join treats all of those as the same doctor (this is the trap the founder doc calls the one that "could libel someone"). OFAC `SDN_TYPE` has a trailing-space sentinel. USASpending contracts are one row per transaction, not per award, and "Lockheed Martin" alone fragments across 77 child UEIs / 26 parent UEIs.
7. **Reserved-word / RLIKE gotcha:** Snowflake `RLIKE`/`REGEXP` match the whole string, not a substring — unanchored patterns silently return zero rows on catalog searches.
8. **Politics domain footgun:** the 13 politics dbt marts mirror Python-built canonical tables; a selector-less `dbt build` can clobber them.
9. **Loader-level gap (deferred, documented):** append-mode loaders (AIS, storm events) killed mid-unit leave a partial day/year silently treated as "loaded" on the next run.
10. **Visual artifacts are stale relative to the live detector count.** `outputs/leads_overlay.html` (the red-string board) was last rendered 2026-06-27 with 4 detectors/353 leads; the live system already had 6 detectors/~1,030 leads by 2026-06-28. Needs a re-render before being shown as current.
11. **Offline-ability is inconsistent across visual artifacts.** `plane.html` is genuinely offline (vendored mermaid.js). `connection_explorer.html` and `leads_overlay.html` pull Plotly from a CDN and render blank with no internet — a vendored local copy (`outputs/plotly.min.js`, 4.8MB) already sits in the folder but isn't wired in.

---

## 9. Built But Not Yet Applied (Chris's pending queue)

The agent's auto-mode permission classifier hard-blocks direct mutations to shared warehouse/catalog infrastructure regardless of role (even ACCOUNTADMIN) — deliberate, matches the foreman model. Every mutation ships as a preview-by-default, `--apply`-gated Python script.

**Pending as of the last build-state.md update (2026-07-07), in dependency order:**
1. `reconcile_op2022.py --apply` — flips a mislogged run so 13.25M Open Payments 2022 rows go live.
2. `build_v_connections_core.py --apply` — creates the 4,308-edge trustworthy-core view.
3. `revoke_straggler_pats.py --apply` — drops 5 stale/unrestricted PATs. *(A related PAT-revocation script was committed 2026-07-08 — verify whether this is already run/superseded.)*
4. `dedup_irs_eo_bmf.py --apply --prune-edges` — quarantines the IRS EO BMF duplicate (reversible), optionally prunes 140 redundant graph edges.
5. `rebuild_frozen_marts.py --apply` — recovers 926k rows trapped behind 7 stale dbt models.
6. `build_giant_aggs.py --apply` — builds 14 pre-aggregated marts (<100k rows each) for the 24 "too-big" tables.
7. `thelibrary_inventory.py && thelibrary_build.py --apply --typed` — one atomic reconcile-and-type pass (self-healing, safe to re-run).
8. `backfill_join_keys_std.py --apply` — measures real join keys for 82 sources.
9. `gen_evidence_pages.py --apply` — generates 226 evidence.dev pages (deliberately last).

One-command runner: `bash scripts/apply_evidence_readiness.sh` (chains 1–9, stops on error). Two steps excluded from the runner, must be run manually: `revoke_straggler_pats.py --apply` (irreversible) and the Snowsight serving-PAT mint (manual UI step).

**Also still pending (lower priority):** `regrade_empty_loads.py --apply` (correct but slow); pointing dbt CI at a least-privilege role instead of ACCOUNTADMIN; excluding bare ZIP/FIPS from the connection graph (open design call).

**Two named "plays" explicitly on the shelf** (from the founder doc, framed as ready-to-run options, not yet chosen):
- **"Fix-Everything"** (~2 sessions): finish cleaning macros, fix broken loads, drain catalog debt, wire 3 new detectors, rotate the PAT, codify infra-as-DDL.
- **"The Plane"** (~1 session): finish the offline visual warehouse explorer (see §10 — v0 exists but is unfinished; CARD altitude, domain coloring, and lifecycle coloring are all not-yet-built).
- A third listed lever: land one new identifier (EIN or CIK) specifically to break the ~75%-leads-on-one-edge concentration risk (§2e).

---

## 10. The Publishing / Visual Layer (does not exist yet — full design brief on file)

Explicitly deferred as an engineering priority, but a complete, self-contained design brief exists (`docs/RIPPLE_DESIGN_BRIEF.md`) for whoever eventually builds it — visual identity is described as fully greenfield ("no logo, no palette beyond a functional tier-color mapping, no typeface, no design system — go nuts"). Key constraints that ARE fixed (ethically load-bearing, not aesthetic):
- Keep the confidence ladder's tier *meaning and ordering* sacred — trust must always encode connection strength, never topic.
- Any lead card for an unconfirmed/unpublished finding about a named person **must** visually read as internal/draft (watermark, no shareable URL) — this is called "the single most ethically load-bearing state change you'll design."
- Four data traps constrain what any chart may honestly claim: AIS is a single 24-hour snapshot (never draw it as a time series), same-name is never the same person in a visual merge, top-contractor rankings are floors not truths (UEI fragmentation), and LEIE's all-zero NPI must never be drawn as a confirmed fact.

**Two phases identified, explicitly sequenced:** Phase 1 = Chris's private investigative workbench (dense, Bloomberg-terminal-style, build for this now). Phase 2 = a public newsroom storytelling site (narrative, one investigation at a time), gated behind the safety layer, not yet in scope.

**What currently exists as visual artifacts (all in `outputs/`):**
- `connection_explorer.html` — the full force-directed graph (720 nodes, 20,696 edges at last render, CDN-dependent, ~17MB). Done and usable, but a near-hairball until tier-filtered (73% of edges are the two weakest tiers).
- `leads_overlay.html` — the "red-string board" (flag sources vs. active sources, edge width = lead count). Done but stale (§8, item 10).
- `plane.html` — **"The Plane," a Google-Earth-style semantic-zoom explorer of the warehouse itself** (not entities/leads — explicitly out of scope for this tool). Four altitudes (ORBIT → REGION → STREET → CARD), fake semantic zoom via a single Plotly relayout listener with debounce+hysteresis. **v0 only — CARD altitude (click a dataset for its full profile) is not implemented, no domain/lifecycle coloring, no search/filter.** Full spec at `outputs/PLANE_handoff.md` (an entire self-contained build handoff, ~200 lines, with a phased v0/v1/v2 plan and 8 named "landmines" learned the hard way — bbox scaling, WebGL text rendering, edge restyle performance).
- Not built at all yet: a lead-detail dossier card, an interactive entity "corkboard," a web lead-review UI (confirm/reject/retract is CLI-only today), a treatment for the 82 keyless/isolated datasets.

---

## 11. Durable Decisions / Policy

- **Scope discipline:** land+wire+catalog only; no new detector/lead/pattern work; publishing layer deferred. (2026-06-29, standing.)
- **Source scope:** clean public sources only for the land-everything sprint; paid/ToS-grey sources dropped or deferred to a specific story need.
- **Ordering:** crosswalk/bridge sources before domain-specific spines; keyless-before-keyed; deterministic-before-agentic.
- **Every catalog/warehouse-infra mutation ships as preview/`--apply`, never executed directly by the agent** (classifier-enforced).
- **`V_STATE` is the only place scale numbers may be quoted from** — prose numbers (including in CLAUDE.md/build-state.md/this doc) are explicitly untrusted and rot.
- **Any `CREATE OR REPLACE VIEW` on a `LIBRARY_META` view must include `COPY GRANTS`** — without it, a rebuild silently strips the read-role SELECT grant every time.
- **SERVE surface is evidence.dev**, not Streamlit-in-Snowflake (superseded 2026-07-06); `serve/` kept as legacy fallback.
- **Fact vs. lead is the non-negotiable trust boundary** (§1, §2e) — the single design decision the whole credibility case rests on.
- Naming, layering, and registry-field conventions per CLAUDE.md — unchanged since repo inception.

---

## 12. Parked Ideas

**HOT:**
- Tier-aware bridge dedup — a weak GEO/ZIP edge currently suppresses a strong CCN→NPI entity bridge in `bridge.discover_bridged`; fix would only dedup against equal-or-stronger-tier direct edges.
- Per-watchlist fanout relax — the FANOUT_MAX=40 guard correctly kills junk edges but also drops legitimate high-value hospital→banned-provider hops for small curated watchlists (e.g. LEIE's 8,775 banned NPIs).
- Materialize a `connect__banned_but_operating` dbt mart from the crosswalk×LEIE join — flagged as the first shippable "story" from the connected Library.
- Land one new identifier (EIN via IRS EO BMF, or CIK via a one-line SEC EDGAR User-Agent fix) specifically to break the 75%-leads-on-one-edge concentration.

**SOMEDAY:**
- Pour IRS EO BMF (1.97M nonprofit EINs) as a dedicated EIN endpoint for follow-the-money work.
- Central `sources.yml` instead of per-model `sources:` blocks in dbt (cosmetic).
- dbt deprecation sweep — 148 generic-test-arg and 57 severity-placement warnings that will become errors on a future dbt major bump.
- Wire the Library Map as `ripple map` so it self-refreshes.
- Hide raw-vs-cleaned duplicate objects in the Reading Room (ugly collision-suffixed names when both exist).
- Vendor Plotly locally in `connection_explorer.html`/`leads_overlay.html` so they work fully offline (the file already exists, just isn't wired in).
- Sketch what an EIN (revoked-org), NAICS (polluter), DOCKET (regulatory), or ZIP (county-burden) detector would look like as templates for engineering, even before building them (raised in the design brief as an open call).

---

## 13. Open Questions

- The primary PAT authenticates as `ACCOUNTADMIN` — no least-privilege ingest/dbt role has been carved out yet.
- Whether to structurally exclude bare ZIP/FIPS coincidence edges from the connection graph, versus relying on the tier filter to hide them.
- Whether/when to point dbt CI and routine batch writes at a scoped service role instead of ACCOUNTADMIN.
- Who builds the publishing/visual layer and on what timeline — the design brief is written but unassigned; "Phase 1 private workbench" vs. "Phase 2 public site" is explicitly a sequencing call not yet made.
- Whether/how to break the ~75%-of-leads-on-one-edge concentration (which new identifier to land first: EIN vs. CIK vs. something else).
- Web vs. CLI-only for the lead-review workflow (confirm/reject/retract) — currently CLI-only, undecided per the design brief.

---

## 14. Environment / Credential State (last known)

- `.env` (gitignored) in `library-onboarding/` holds `SNOWFLAKE_PAT`, `ANTHROPIC_API_KEY`, and data-source keys (Census/BLS/EIA/NASS/LegiScan/College-Scorecard would unlock ~10 more issue-coverage sources if added; a free OpenFEC key is also referenced by the politics build plan for referee reconciliation).
- Main PAT: rotated 2026-07-05 (that replacement token was pasted in a chat Chris flagged as public — intended to rotate again; if Snowflake auth fails, that's the likely cause). Canonical expiries in `infra/keys_ledger.json`.
- `ANTHROPIC_API_KEY` was restored to `.env` 2026-07-05 after an accidental file rewrite dropped it (also dropped CENSUS/COURTLISTENER/SOCRATA/RIPPLE_CONTACT_UA keys — worth checking those are still present). It authenticated but the Anthropic account had zero purchasable API credits as of that check, blocking LLM-driven recon/codegen until credits are added.
- `RIPPLE_BUDGET` (Snowflake resource monitor) has been raised/lowered repeatedly (15 steady-state → 30 → 100 for sprints → 300). Check the live value before assuming headroom for a large batch job or `connect all` rebuild.
- Node 22 installed user-space at `~/.local/node22` (off PATH by default) for evidence.dev.
- `~/.snowflake/connections.toml` holds a DIFFERENT account/auth (`UKB67948`, OAuth) — dbt and the `snow` CLI read this file, not `.env`; a stale/conflicting toml has caused dbt to silently target the wrong account before.
- SAM_API_KEY (SAM.gov exclusions data) has a documented ~89-day expiry from issuance (2026-06-25) — check freshness before a SAM-dependent load.

---

## 15. Key Reference Docs (in-repo)

- `CLAUDE.md` — full operating rules/conventions for the agent.
- `OVERVIEW.md` / `README.md` — plain-English repo map and quick-start.
- `docs/RIPPLE_FOR_THE_FOUNDER.md` — the honest deep self-assessment (moat, bottleneck, four silent data traps, two plays on the shelf). **Read this first if the goal is strategy** — it's written for exactly that purpose.
- `docs/RIPPLE_DESIGN_BRIEF.md` — the standalone spec for whoever builds the publishing/visual layer.
- `docs/RIPPLE_FOR_EVERYONE.md` — the plain-language, no-jargon pitch.
- `build-state.md` — full chronological build log (this doc's primary source; 1,600+ lines).
- `outputs/FABLE_AUDIT_2026-07-06.md` — the 40-defect stress test.
- `outputs/alexandria_foundation_BLUEPRINT_2026-06-28.md` — the foundation roadmap.
- `outputs/LEADS_2026-07-08.md` — the 8 ad-hoc verified investigative leads (distinct from the persisted detector-engine leads in §2e).
- `outputs/issue_coverage_SUMMARY_2026-06-27.md` + `_DETAIL_` — the 75-issue world-coverage matrix.
- `outputs/ripple_frontier_MASTER_LIST.md` + 5 round docs — the 137-dataset forward scouting backlog (§7).
- `outputs/POLITICS_BUILD_RUNBOOK.md`, `us_politics_coverage_audit_2026-06-30.md`, `us_politics_dark_frontier_2026-06-30.md` — the politics-domain plan set (§6).
- `outputs/PLANE_handoff.md` — The Plane's full build spec (§10).
- `connect/HOWTO.md`, `connect/design-confidence-ladder.md` — the entity-resolution design doc and CLI manual.
- `viz/README.md`, `evidence/README.md` — subsystem manuals.
- `docs/design-incremental-and-scrape.md` — ADRs for the C2/C1b load-mode trade-offs.
