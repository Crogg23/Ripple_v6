# Alexandria Foundation Blueprint — 2026-06-28

**Vision:** The Library of Alexandria for the data analyst and investigative data analyst.
One place where every public dataset worth having is collected, cleaned, catalogued, and
**connected by identity**, so an analyst can pull every thread on any person/company/ship/place
across every domain. Foundation only — no detective work yet.

**Source:** multi-agent workflow `alexandria-foundation-blueprint` (24 agents, 1.29M tokens, 289 tool
calls) — 7 grounded layer-audits + prior-art benchmark → 4 competing architectures → 3-perspective
judge panel → synthesis. All claims verified against live code + warehouse.

**Design ranking (judge avg /40):** acquire_first 33.3 · connect_first 32.3 · leverage_first 32.3 ·
serve_first 31.7. Close race → the blueprint grafts the best of all four.

---

## Headline

The foundation is a genuinely strong **hand-cranked workshop with one fatal blind spot: it tracks when
data was LOADED, never whether the data is ALIVE.** Its biggest table (AIS, 58M rows) is a 2.5-year-old
snapshot reading as "fresh," and every other engine (connect, organize, trust, serve) is a manual
full-rebuild that drifts the instant a sprint ends. The winning move is a **measured-freshness control
plane** that all five engines subscribe to, a **thin honest reading room** over the already-built
9.8M-entity moat in week one (so value is visible and self-prioritizing), then make the **content-SHA
delta the unit of work** so the whole thing runs incrementally and affordably forever.

## Maturity scorecard

| Layer | Maturity |
|---|---|
| ACQUIRE — ingestion engine | partial (solid loader, **zero heartbeat**) |
| CONNECT — entity/connection engine (the moat) | partial (real, but manual full-rebuild, 98% health) |
| ORGANIZE — catalog / Pinakes | partial (governed skeleton, **empty content**) |
| TRUST — is the data real + traceable | partial (run-provenance solid, **staleness invisible**) |
| SERVE — analyst reading room | prototype (**does not exist** — static HTML only) |
| SCALE / COST / OPS | prototype (single capped warehouse, DR hole) |

## THE ONE THING — the freshness ledger

`V_SOURCE_FRESHNESS`: per source, measured **DATA_THROUGH** (max real date in the landing table) vs a
normalized **CADENCE_BUCKET** vs now → a **FRESHNESS_STATE** {fresh/due/overdue/stale/dead/unknown}.
One object that ACQUIRE (what's due), ORGANIZE (currency axis), TRUST (auto-demote stale) and SERVE
(inline badge) all subscribe to — **one artifact, four payoffs.** Days-not-weeks (the run log + date
columns already exist). The day it lands, AIS flips from "modeled/fresh" to "overdue 2.5 years."

---

## The five layers — target / gap / moves

### ACQUIRE
- **Target:** a self-sustaining heartbeat — catalog-driven scheduler re-pulls every source on its own
  cadence, incremental-by-default, with a measured data-freshness SLA. New sources onboard unattended;
  Chris approves policy + exceptions, not 5 checkpoints per source.
- **Gap:** solid hand-cranked loader, **zero heartbeat** (0 cron; CI is push/PR-only). Refresh ≈ 0: only
  12 of 842 sources ever logged a content change, all same-sprint backfills. Freshness = LOAD recency,
  not DATA recency. UPDATE_CADENCE is free-text prose, not machine-readable. exec() of model-generated
  fetch code is unsandboxed.
- **Moves:** ship the freshness ledger · normalize CADENCE_BUCKET enum · catalog-driven `refresh` on
  GitHub Actions cron · flip big movers to incremental-by-default · sandbox the exec() before any cron.

### CONNECT (the crown jewel)
- **Target:** continuous, incremental, all-domain identity service that fires the moment a source lands
  and links against the persisted spine — O(changed tables), not O(all 762). Any of ~20 identity types
  anchors a cross-domain dossier automatically.
- **Gap:** fully manual full-rebuild, decoupled from ingestion (onboard.py stops at REGISTRY). Every
  `connect all` re-scans all 762 tables + rebuilds a 38.3M-row keyset + 9.79M-row spine regardless of
  what changed. Graph is **98.2% NPI providers**; only 4 entity types — EIN/DUNS/LEI/MMSI/FIPS exist as
  edges, not spine entities, so a company-by-EIN or vessel-by-MMSI dossier returns nothing.
- **Moves:** persist KEYSET + CONNECT_WATERMARK (re-derive only changed-SHA tables) · carry resolve.py
  blocking into discover (bounded connect-on-land) · spine.py CREATE-OR-REPLACE → MERGE upsert (safe:
  content-addressed ENTITY_ID) · Checkpoint 6 (CONNECT) in onboard.py · **promote EIN/DUNS/LEI/MMSI/FIPS
  to first-class spine entities** (breaks 98%-health concentration with zero new ingestion).

### SERVE (the reading room)
- **Target:** ONE persistent app — single search box over everything → live entity dossier (pull every
  thread) → connection graph one click away, with freshness + provenance inline on every row, plus a
  workspace that remembers searches/watchlists/notes. Always live against Snowflake.
- **Gap:** no reading room. dashboard_server.py is a localhost throwaway; everything else is frozen 17MB
  HTML. The dossier — the most vision-aligned feature — is **CLI-only** despite the 10.7M-row
  ENTITY_INDEX + 9.79M ENTITY_GOLDEN backbone (952k multi-source entities) **already built and wasted.**
  No search across the library. No isolated SERVE_WH.
- **Moves:** stand up ONE Streamlit-in-Snowflake app (SiS already available) · promote dossier.py to a
  live ENTITY DOSSIER page · Cortex Search over ENTITY_INDEX + CATALOG · freshness badge + provenance
  receipt inline · dedicated read-only SERVE_WH.

### ORGANIZE (the Pinakes)
- **Target:** living catalog where every landed source carries a complete governed facet set + a
  data-currency stamp, discoverable by facet AND natural-language; review queue drains; vocab governance
  fails the build on drift.
- **Gap:** skeleton built and governed (CATALOG, FACET_VOCAB 0-drift) — the gap is **content.**
  ENTITY_TYPES 0/102 (the axis the whole vision rests on); 53/102 UNCLASSIFIED; JOIN_KEYS_STD on only
  38/102; THEMES is a single tag; no data-currency axis; catalog DDL lives only in a markdown spec (DR
  hole).
- **Moves:** backfill ENTITY_TYPES (agent proposes, human approves batch) · classify 53 UNCLASSIFIED +
  suppress 77 orphans · derive JOIN_KEYS_STD from the Phase-2 keyset (free byproduct) · data-currency
  facet from the ledger · vocab tests warn→error + DDL to infra/ddl/.

### TRUST
- **Target:** an investigator can stake their name on any cell — resolves in one query to primary-source
  URL + fetch timestamp + content SHA + immutable versioned snapshot; freshness is first-class so stale
  auto-demotes; dead data can never read as real; published claims reproduce byte-for-byte; spine reads
  only trust-gated sources.
- **Gap:** run-level provenance solid (all 102 have INGEST_RUNS + SHA + per-row stamps). Holes:
  **staleness invisible** (AIS masquerades live); dead-source guards are manual one-shots (~10 stubs ride
  as "landed"); snapshot-replace **overwrites the rows a receipt cites** (so "reproducible SQL" can't
  reproduce); provenance column split _SRC_SHA256 vs SRC_SHA256; DECISIONS empty; catalog/run-log
  live-only (a predecessor infra DB was already lost to a DROP).
- **Moves:** freshness ledger doubles as trust instrument (auto-demote stale out of trusted use + rarity
  corpus) · one scheduled standing guard → TRUST_HEALTH table · immutable per-run zero-copy CLONE
  snapshots (receipts reproduce) · unify provenance + V_LANDING_PROVENANCE · codify DDL + export
  non-rebuildable judgment state.

---

## Roadmap

**Phase 0 — Insurance + the keystone.** infra/ddl/ (idempotent DDL for run-log, registry, catalog,
budget monitor, warehouses, roles) + LIBRARY_WRITER least-priv role + **SOURCE_FRESHNESS ledger** +
unified provenance view. *Why now: the ledger has four consumers; DR codification must precede adding any
more live-only state.*

**Phase 1 — Honest reading room v0.** ONE Streamlit-in-Snowflake app replacing all frozen HTML + live
ENTITY DOSSIER page + Cortex Search front door + freshness/provenance inline + dedicated SERVE_WH.
*Why now: the 9.8M-entity moat is paid-for and trapped behind a CLI — cheapest "feels like Alexandria"
moment, and it becomes the self-prioritizing QA dashboard for everything after.*

**Phase 2 — The incremental engine.** Persisted KEYSET + CONNECT_WATERMARK (O(changed)) + bounded
connect-on-land + spine MERGE upsert + Checkpoint 6 in onboard.py. *Why now: biggest cost+correctness win
and the gate on the heartbeat — scaling onto a non-incremental connect blows the cap.*

**Phase 3 — Heartbeat + standing guards.** Catalog-driven `refresh` on cron (matrix by cadence) +
incremental-by-default on big movers + standing TRUST_HEALTH guard + immutable per-run snapshots. *Why
now: the library stops silently rotting; affordable only because connect is now incremental.*

**Phase 4 — Fill the Pinakes.** ENTITY_TYPES 0→~100% · classify 53 UNCLASSIFIED · JOIN_KEYS from the
keyset · data-currency facet · promote EIN/MMSI/FIPS to spine entities · vocab tests → error. *Why now:
mostly free byproducts of earlier phases; lights up search + cross-domain dossiers instantly.*

**Phase 5 — Scale acquisition: 100 → thousands.** Hardened autonomous lane (sandboxed exec + secret
broker + budget throttle) · seize the 474 portals + 657 sampled · human-as-foreman batch exception
review. *Why now: only safe after connect is O(changed) and trust is standing.*

**Phase 6 — Deepen (earn-into).** NL→SQL box · case folders · multi-user auth · Splink fuzzy ER beyond
leie_nppes · FollowTheMoney ontology · Dagster. *Why now: each is its own project, none blocks the
foundation.*

---

## Risks
- Solo multi-quarter march. **Phases 0–3 ARE the foundation and are solo-tractable; 4–6 are an earn-into
  horizon.** Drift risk = treating all six as one block.
- Unattended exec() of model-generated code on a cron is a real security surface — its own hardening
  project; must land before any autonomous lane (Phase 5); keyless-first until then.
- 30cr cap, no slack (~70% used). Cortex Search + Streamlit serving + incremental refresh all compete;
  isolate SERVE_WH/CONNECT_WH; incremental-by-default is the only thing that keeps refresh affordable.
- Incremental-correctness seams: deletion/retraction under snapshot-replace, golden recompute scope,
  run-SHA-vs-table-SHA for multi-file sources. Mitigate with periodic full-rebuild reconciliation.
- Human-approval catalog backfills can stall like the 708-row queue that drained 23 — agent proposes in
  batch, human approves N-per-session, never per-source.
- DR remains live-only until Phase 0 ships — a single DROP erases catalog + run-log + keyset at once.

## What we are explicitly NOT doing (anti-drift)
- No detective work, detectors, leads, or stories. Existing LEADS machinery frozen as-is.
- No new fuzzy ER / Splink in the foundation — broaden the moat by adding entity TYPES, not probabilistic
  matching.
- No NL→SQL / case management / multi-user auth in the early reading room.
- No Dagster/Airflow up front — GitHub Actions cron + SHA-skip is enough.
- No off-stack stores (no Neo4j-primary, no Elasticsearch) — strictly Python/Snowflake/dbt/Plotly;
  Cortex Search is native, the graph is projected read-only.
- No publishing layer.
- Not chasing 100% catalog backfill by hand — fill the ~102 real sources; the long tail waits for Phase 5.
