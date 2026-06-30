# infra/ddl — version-controlled Snowflake DDL (disaster recovery)

The platform's control-plane objects used to live **only as live Snowflake state**. A predecessor infra
database was already lost to a `DROP` once. This directory codifies that state as idempotent SQL so the
structure is rebuildable from git. Phase 0 of the foundation blueprint.

## Files (apply in order)

| File | What | Safe to re-apply? |
|---|---|---|
| `01_meta_base_tables.sql` | Run-log + registry + facet tables | **Yes** — `CREATE TABLE IF NOT EXISTS` never touches existing rows |
| `02_catalog_views.sql` | CATALOG (Pinakes) + bridge views | Yes — `CREATE OR REPLACE VIEW`, fully rebuildable |
| `03_warehouses_roles_monitor.sql` | Warehouses, `RIPPLE_BUDGET` monitor, roles | Yes — agent-reconstructed; **review before relying on** |
| `04_freshness_ledger.sql` | `SOURCE_FRESHNESS` table + `V_SOURCE_FRESHNESS` view | Yes — populated by `scripts/build_freshness_ledger.py` |
| `05_serve_wh.sql` | Read-only serving warehouse (`SERVE_WH`) + its own budget monitor (`SERVE_MON`) + grant to `CLAUDE_MCP_READONLY` | Yes — run as ACCOUNTADMIN; `CREATE ... IF NOT EXISTS`, but `ALTER WAREHOUSE SET RESOURCE_MONITOR` + `GRANT` re-run on apply |

## What this DOES protect

The **structure** of the control plane: re-run these files into a fresh account/database and the run-log,
registry, catalog, facet vocab, warehouses, monitor, and freshness ledger all come back.

## What this does NOT protect (must be exported separately)

DDL recreates empty tables. The **data inside the non-rebuildable base tables is judgment that cannot
regenerate from raw**:

- `INGEST_LOGS.INGEST_RUNS` — the heartbeat's memory (skip-if-unchanged, resume, lifecycle all read it)
- `REGISTRY.SOURCE_REGISTRY` — the catalog content (domains, facets, join keys — hand + agent curated)
- `REGISTRY.FACET_VOCAB` / `FACET_CROSSWALK` — the governed vocabulary
- `"CONNECT".ENTITY_LINKS` — gated fuzzy entity-resolution verdicts
- `"CONNECT".DECISIONS` / confirmed `LEADS` — human review sign-offs

> The content-addressed entity spine (`ENTITY_MAP`/`ENTITY_GOLDEN`, `ENTITY_ID = MD5(key_type|val)`) and
> all landing tables **do** rebuild from code + raw, so they are not listed here.

**Manual data export shipped:** `scripts/export_control_plane.py` does a `COPY INTO` a stage + `GET` to
`backups/dr/<ts>/` for the non-rebuildable control-plane tables above plus the freshness ledger (8 tables
total; preview by default, `--apply` to run). The remaining gap is **scheduling + replication to cloud
storage** (S3/GCS) so a `DROP` is recoverable end-to-end without a manual run.

## Provenance

Captured 2026-06-29 via `GET_DDL` / `SHOW` (workflow `phase0-freshness-ledger`, 20 objects). The base-table
DDL was transformed from `CREATE OR REPLACE TABLE` → `CREATE TABLE IF NOT EXISTS` so applying these files
can never clobber live data. `05_serve_wh.sql` was authored later (serving-layer build) and is not part of
that 20-object capture.
