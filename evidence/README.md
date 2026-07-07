# The Library — evidence.dev reading room

A [evidence.dev](https://evidence.dev) site over the Ripple Library. It queries the
curated `THE_LIBRARY` views in Snowflake, extracts each query's result to a parquet
file at build time, and renders charts/tables in the browser (DuckDB-WASM). Scaffolded
2026-07-06 as Phase 0 of the evidence.dev roadmap (`outputs/FABLE_AUDIT_2026-07-06.md`).

## Run it

Node isn't on the system `PATH` — it lives at `~/.local/node22`. Either add it:

```bash
export PATH="$HOME/.local/node22/bin:$PATH"
```

or prefix commands with that path. Then, from this directory:

```bash
npm run sources      # extract every sources/*.sql from Snowflake -> parquet
npm run dev          # dev server at http://localhost:3000
npm run build        # production build -> ./build (static site)
```

To view a production build locally: `cd build && python3 -m http.server 8080`.

> **Dev-server gotcha:** deep-linking a page (e.g. hitting `/scotus` directly on a
> cold server) can 500 with "Failed to fetch dynamically imported module" — SvelteKit
> compiles routes on demand and the direct hit races the compile. Load `/` first and
> click through, or just reload. A production `build` compiles everything ahead of time
> and never has this.

## The connection

`sources/library/connection.yaml` points at Snowflake. The password lives ONLY in
`sources/library/connection.options.yaml` (gitignored, base64-encoded — Evidence
requires b64 there). Two lanes:

- **Interim (today):** the main PAT as password, `role` unset (ACCOUNTADMIN),
  `warehouse: COMPUTE_WH`. Works now; it's the same client-guard lane every other
  Ripple surface uses.
- **Enforced (recommended):** run `python3 ../scripts/apply_read_lane.py --apply` from
  the repo root (creates `SERVE_WH` + `SERVE_MON` + the provably-read-only
  `RIPPLE_READER` role + a role-restricted 90-day PAT written to `.env` as
  `SNOWFLAKE_SERVE_PAT`). Then swap `connection.options.yaml` to that PAT and set
  `warehouse: SERVE_WH`, `role: RIPPLE_READER` in `connection.yaml`. Now a runaway
  query can't touch ETL or drain the account budget, and the credential isn't admin.

## How the source queries are shaped

evidence.dev extracts each `sources/*.sql` result to parquet at build time, so **every
source query must stay small** (aggregate/filter Snowflake-side; ~100k rows max — the
flagship views like `INDIVIDUAL_DONATIONS` are 84M rows and must never be `SELECT *`d).
Current sources are all aggregates or naturally-small tables. `catalog.sql` (the
`START_HERE` index, 232 rows) is the spine — loop over it to template more pages.

## Casting note

`status = raw` datasets in the catalog read the as-landed TEXT views, so numbers and
dates arrive as strings — the page queries hand-cast with `TRY_TO_NUMBER` / `TRY_TO_DATE`
(see `sources/gun_checks.sql`, `banned_providers.sql`). Once the typed staging layer
lands (Phase 3 of the audit roadmap), those casts move server-side and the raw-backed
views get re-pointed at typed staging.

## Pages

`pages/index.md` (the card catalog + shelves) plus six exhibits: national debt,
banned healthcare providers, gun background checks, fatal police shootings, foreign
agents, the Supreme Court. Each is a thin markdown file with a SQL block and a chart.
