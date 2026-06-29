# Ripple — the Reading Room (Phase 1 SERVE layer)

The moat is already built — a 9.8M-entity backbone that \"pulls every thread\" on any
person/company/ship/place across every domain. Until now it was trapped behind a CLI.
**This is the reading room: a single, persistent Streamlit app that surfaces it live.**

```
streamlit run serve/app.py
```

## What it does

| Page | What it is |
|------|------------|
| **Search** | One box over **entities** (the backbone) *and* **sources** (CATALOG). Name search (token-AND on the spine's `NAME_NORM`) or a pasted hard ID (NPI / CCN / UEI / CIK / IMO). |
| **Dossier** | A resolved entity → every cross-domain thread + provider affiliations, with a **freshness badge** + **provenance receipt** inline on every row, and a jump into the graph. |
| **Graph** | The cached `connect_graph.json` drawn live in WebGL Plotly (720 source nodes, 20,696 measured edges). Retires the 17 MB frozen HTML. Click/select a node → its source page. |
| **Source** | Catalog metadata, freshness, the run-it-yourself receipt (run id · SHA-256 · verify-URL), and a 25-row live sample. |

Deep links: `?view=dossier&eid=ENT_…` · `?view=source&src=fed_…` · `?view=graph&focus=TBL1,TBL2`.

## Why local Streamlit (not Streamlit-in-Snowflake) for Phase 1

Both were verified deployable on the account. Local wins for v0 because it **reuses
everything verbatim** — `library-onboarding/snow.py` (PAT-as-password), the
`connect/` query logic, and the 7 MB graph read straight off disk. SiS would force a
Snowpark rewrite of the data layer + staging the graph JSON — that's Phase 2.

The data layer is written to run in **both** anyway (`serve_session.py`): in SiS it
uses `get_active_session()`; locally it uses `snow.connect()`. Both hand back a
snowflake-connector cursor, so every query uses ordinary `%s` binds and is portable.

## One-time setup

1. **Create the serving warehouse + budget guard** (as ACCOUNTADMIN):
   ```
   snowsql -f serve/serve_wh.sql
   ```
   Creates `SERVE_WH` (X-Small, auto-suspend 60s), `SERVE_MON` (5 cr/mo cap so the
   reading room can't drain the ETL budget), and grants usage to `CLAUDE_MCP_READONLY`.

2. **Env** — already in `library-onboarding/.env` (PAT-as-password). The app forces
   `USE ROLE CLAUDE_MCP_READONLY` + `USE WAREHOUSE SERVE_WH` at connect. Override with:
   ```
   RIPPLE_SERVE_ROLE=CLAUDE_MCP_READONLY
   RIPPLE_SERVE_WH=SERVE_WH
   RIPPLE_GRAPH_PATH=/abs/path/to/connect_graph.json   # optional
   ```
   If `SERVE_WH` doesn't exist yet the app still boots on a fallback warehouse and
   says so in the sidebar **System** panel.

3. **Install + run**:
   ```
   pip install -r serve/requirements.txt
   streamlit run serve/app.py
   ```

## Freshness & provenance (graceful degradation)

- **Freshness** comes from `LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS` — which is
  **absent today**. The app probes `INFORMATION_SCHEMA.VIEWS`; if missing it shows
  `⚪ recency unverified · last loaded <ts>` and **never** calls a load-stamp \"fresh\"
  (that's the NOAA-AIS false-fresh bug the ledger exists to kill). Build the real
  ledger with `python scripts/build_freshness_ledger.py --apply` to light the badges.
- **Provenance** comes from `LIBRARY_META.INGEST_LOGS.INGEST_RUNS`: the latest
  successful run per source → run id, SHA-256, and the exact `SOURCE_URL` a skeptic
  re-fetches. Mirrors `connect/receipt.py` (pin on the run, not a per-chunk SHA).

## Notes / Phase-2 hooks

- Backbone is ~98% NPPES providers; only NPI/CCN/UEI/CIK/IMO resolve today. EIN is
  intentionally not offered (no rows in the index yet).
- Graph nodes are **source tables**, not entities — clicking one opens its source
  page. Entity-to-entity edges (`ENTITY_LINKS`, 2,324 rows) are a separate, tiny
  layer deferred to a later pass.
- Name search full-scans 9.8M rows with a leading-wildcard `LIKE` (sub-1.1s warm for
  one analyst). Cortex Search is the Phase-1.5 upgrade when concurrency grows.
