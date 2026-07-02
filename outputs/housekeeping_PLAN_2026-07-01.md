# Ripple Housekeeping — Comprehensive Plan (2026-07-01)

**Goal:** Make Snowflake navigable for a human (Chris) without breaking the machine.
Three workstreams: **B) Cleanup**, **A) Plain-English comments**, **C) The Reading Room**.

## North-star principles (non-negotiable)
1. **Zero downstream breakage.** The pipeline keeps its stable codenames. Every physical
   table, dbt model, `connect` table, registry key, and MCP grant stays exactly as-is.
   Human-friendly names exist ONLY as an additive VIEW layer.
2. **Voice = "explain it so anyone gets it."** Plain, concrete, explains the *why*, no
   jargon, not dumbed down. NOT a Vsauce/Cox impersonation — that's just shorthand for
   "clear + accessible." A smart 12-year-old and a busy adult both understand instantly.
3. **Everything reversible.** Snapshot before every destructive step. Every generator is
   idempotent (`CREATE OR REPLACE`, re-runnable). Destructive steps preview first.
4. **Self-maintaining.** The friendly layer regenerates from `CATALOG` — a new source lands,
   re-run one script, it appears. No hand-maintained lists.

---

## Ground truth (from live recon, 2026-07-01)
- 9 databases: 5 are Ripple (`LIBRARY_RAW/META/MARTS/STAGING/TOOLS`), 4 are noise
  (`SNOWFLAKE`, `SNOWFLAKE_SAMPLE_DATA`, `SNOWFLAKE_PUBLIC_DATA_PAID`, `USER$CROGG23`).
- `LIBRARY_RAW.LANDING`: 784 tables = **129 named sources + 655 `PORTAL_` firehose samples**.
- `LIBRARY_MARTS`: 73 marts across CORE / DBT_CROGERS / EPSTEIN / POLITICS.
- `LIBRARY_META`: REGISTRY (catalog), INGEST_LOGS, CONNECT (entity-resolution engine, 1.9 GB).
- Warehouses: RIPPLE_WH / DBT_WH / COMPUTE_WH all actively used (DBT_WH biggest burner).
- `CATALOG` view columns available for the Reading Room: SOURCE_ID, NAME, DOMAIN_PRIMARY,
  JOIN_KEYS_STD, JOIN_KEY_TIER, LIFECYCLE, LANDED_ROW_COUNT, MART_ROW_COUNT, IS_SAMPLE,
  TRUST_LAYER, LANDING_FQN, IS_ORPHAN, URL, PUBLISHER, DESCRIPTION.
- **52 landed sources are `domain_primary='UNCLASSIFIED'`** (issue-coverage batch, never tagged).
- Scratch tables (`KEYSET_SCRATCH`, `CROSSWALK_SCRATCH`, `SPINE_KEYSET`) are TRANSIENT working
  sets rebuilt by `connect discover`; durable twins are `KEYSET_LIVE` / `SPINE_KEYSET_LIVE`.
  Referenced by `connect/{discover,incremental,bridge,spine}.py` — NOT dead orphans.
- `_SOURCE_REGISTRY_BAK_20260625` (1,503 rows): static backup, **no code references** — safe.
- No SQL objects/views depend on the scratch tables (ACCOUNT_USAGE, ~3h latency caveat).

---

## WORKSTREAM B — Cleanup (destructive; authorized via checkpoint)

### B1 — Drop the sample-data mount  ✅ safe
- `DROP DATABASE SNOWFLAKE_SAMPLE_DATA;` — inbound share, zero code refs, no billing.
- **Reverse:** re-create from the SFC_SAMPLES share (standard, one statement) any time.

### B2 — Drop the paid-marketplace mount  ⚠️ billing gate
- `SNOWFLAKE_PUBLIC_DATA_PAID` = inbound Marketplace share, 370 views, zero code refs.
- **RISK:** `DROP DATABASE` removes the mount but may NOT cancel a paid subscription.
- **Action:** Chris cancels/verifies the subscription in Snowsight → Marketplace FIRST.
  Agent drops the mount only after confirmation. **DEFAULT: HOLD until Chris confirms.**
- **Reverse:** re-subscribe from Marketplace.

### B3 — Registry backup  ✅ safe
- `DROP TABLE LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_20260625;`
- **Pre-step:** re-snapshot current `SOURCE_REGISTRY` to a dated backup first, so we always
  keep exactly one restore point (drop the OLD one, keep a FRESH one).

### B4 — Scratch tables  ⚠️ RECLASSIFIED — do NOT blanket-drop
- `KEYSET_SCRATCH` (38M), `CROSSWALK_SCRATCH` (4M), `SPINE_KEYSET` (10M) are LIVE pipeline
  transients. Dropping them forces a full `connect discover` rebuild (compute cost) and leans
  on the incremental fallback (`_rebuild_spine_keyset_from_landing`).
- **Decision:** the win Chris wanted was decluttering — but the Reading Room hides CONNECT
  entirely, so dropping buys ~0 navigation value at real pipeline risk. **RECOMMENDATION:
  do NOT drop.** Instead (optional, deferred): convert them to true `TRANSIENT` so they stop
  counting as permanent storage (build-state's original P2 intent). Storage saved ≈ $0.02/mo.
- **If Chris still wants them gone:** drop ONLY after a clean full `connect` run, verify the
  `_LIVE` twins are populated, and document that the next run rebuilds them.

### B5 — Broken stub marts  ⚠️ resurrection risk
- 12 one-row marts in `LIBRARY_MARTS.DBT_CROGERS` (fjc_idb, doj_crt_cases, naag, zefix, gemi,
  borme, cro, hhs_taggs, fdic_enforcement, nara_wra, slavevoyages) + EPSTEIN ledger (3 rows).
- Each has a dbt model file. **Dropping the table alone = next `dbt run` rebuilds the stub.**
- **Action:** (a) disable the mart model in dbt (`{{ config(enabled=false) }}`, kept in git);
  (b) `DROP TABLE` the stub. Staging views left intact (harmless, needed for future re-ingest).
- **Reverse:** flip `enabled=true`, `dbt run`. The root cause is bad ingestion (documented in
  build-state) — a separate per-source re-ingest project, out of scope here.
- **NOTE:** the EPSTEIN compliance ledger (3 rows) may be intentional (small by design) — verify
  before dropping; do not assume it's broken just because it's small.

---

## WORKSTREAM A — Plain-English comments (additive; safe)

### A1 — Database + schema comments (hand-written, ~14 objects)
- `COMMENT ON DATABASE/SCHEMA … IS '…'` for the 5 Ripple DBs + their schemas.
- Explains what each layer IS (loading dock / prep kitchen / finished shelves / catalog+wiring).

### A2 — Table comments on the ~129 named sources + ~73 marts (generated)
- For each, generate a plain-English comment from its real contents: what it holds, grain
  (1 row = ?), row count, the join keys it carries, what it connects to, any quirk.
- Source material: `CATALOG` (NAME/DESCRIPTION/join keys/counts) + a live `DESCRIBE` + a small
  sample. `COMMENT ON TABLE … IS %s` (parameterized; escape single quotes).
- **Scale/voice consistency:** run as a Workflow — parallel agents each take a batch, read the
  table, write the comment to the voice spec, emit the `ALTER`. Human review before apply.

### A3 — Portal tables (655) — ONE templated comment each
- `Portal-net feed harvested from <portal>. Thin sample (<n> rows) carrying <keys> — a
  connector for cross-source matching, not yet a full source.` Generated, not hand-written.

### A4 — Column comments — DEFERRED (thousands; low ROI). Optional later on marquee marts only.

---

## WORKSTREAM C — The Reading Room (additive; safe)

### C0 — Pre-req: domain-tag the 52 UNCLASSIFIED landed sources
- A domain-organized Reading Room dumps half the Library into "UNCLASSIFIED" otherwise.
- Use/adapt `scripts/propose_issue_domain_tags.py` (preview → apply) to assign
  `DOMAIN_PRIMARY` to the 52. Preview for Chris before writing to the registry.

### C1 — Front-door database `THE_LIBRARY`
- `CREATE DATABASE IF NOT EXISTS THE_LIBRARY COMMENT='…front door…';`
- Schemas = friendly domains: HEALTH, MONEY, CAMPAIGN_FINANCE, GOVERNMENT, JUSTICE, ELECTIONS,
  COMPANIES, GOVERNMENT_SPENDING, SANCTIONS, TRANSPORT, ENERGY_ENVIRONMENT, SCIENCE, HISTORY,
  HOUSING, ECONOMY, INVESTIGATIONS. (Map from `domain_primary` vocab.)

### C2 — Friendly views (generated from CATALOG)
- One view per real dataset (landed/modeled, excluding portals + samples), named by plain
  concept (e.g. `HEALTHCARE_PROVIDERS`, `SHIP_POSITIONS`, `ELECTION_RESULTS`).
- Each view = `CREATE OR REPLACE VIEW THE_LIBRARY.<DOMAIN>.<CONCEPT> COMMENT='<Cox comment>'
  AS SELECT * FROM <best layer>` where best layer = the mart if `_REAL_MART`, else `LANDING_FQN`.
- **Concept-name source of truth:** a generated `friendly_name` per source. Collisions within a
  domain get a source suffix. Name style: plain concept; provenance in comment + START_HERE.
- Idempotent + re-runnable. New source → re-run → appears.

### C3 — `THE_LIBRARY.START_HERE` master index
- One view: every dataset with friendly_name, domain, one-line description, row count,
  freshness, join keys, `curated` vs `portal-net` tag, and the real FQN (for when he needs it).

### C4 — Grants
- Grant `CLAUDE_MCP_READONLY` USAGE on `THE_LIBRARY` + SELECT on its views (extend
  `scripts/grant_mcp_readonly_catalog.py`) so the MCP server can read the friendly layer.

---

## Ordering & dependencies
1. **B** first (clears noise). B1/B3/B5 now; **B2 held on billing**; **B4 recommend skip**.
2. **A** next (comments on real objects) — A2 via workflow.
3. **C** last: C0 (tag 52) → C1 (db+schemas) → C2 (views, inheriting A2 comment text) →
   C3 (index) → C4 (grants).
- A2 and C2 share the same generated per-source description → generate ONCE, use in both.

## Cross-cutting risks to stress-test
- Cross-database views (`THE_LIBRARY` → `LIBRARY_MARTS`/`LIBRARY_RAW`): grants, ownership,
  future-grants, view-invalidation if an underlying table changes.
- `DROP DATABASE` on inbound shares: reversibility + billing (B2).
- dbt model resurrection (B5); connect rebuild cost (B4).
- `CATALOG` drift: if it mislabels lifecycle/mart, the Reading Room inherits the error.
- Idempotency: re-running generators must not orphan stale friendly views when a source is
  renamed/removed (need a prune step or full-rebuild-of-schema pattern).
- PAT expiry (~89 days from 2026-06-25) + RIPPLE_BUDGET credits (30.79 remaining).
- Comment escaping (single quotes / length limits) at scale.
- The `friendly_name` mapping quality: collisions, acronyms, honesty (don't oversell a thin source).

## Success criteria
- Chris opens `THE_LIBRARY`, sees ~16 domain shelves, each with plainly-named datasets, each
  explained in one clear sentence. `START_HERE` answers "what do I have and what connects."
- `python -m connect` and `dbt run` still work unchanged. Zero pipeline edits.
- Every destructive action has a written one-line reverse.
