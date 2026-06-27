# Ripple Source Onboarding Agent

A CLI agent that onboards data sources into the **Ripple** Library end to end.
Give it a URL (or run the batch) and it does recon, writes the ingestion script,
lands the data in `LIBRARY_RAW`, scaffolds dbt models, and registers the source in
`LIBRARY_META` — pausing at **five checkpoints** so you (the foreman) approve every
step before it runs.

```bash
python onboard.py --url https://earthquake.usgs.gov/fdsnws/event/1/
python onboard.py --name FRED            # or look one up in the queue by name
python onboard.py --batch                # the pre-loaded queue, resumable
```

At every checkpoint: `go` | `edit <feedback>` | `skip` | `abort`.

---

## The 5-checkpoint flow

```
[1] RECON     reads the source docs -> a SOURCE_REGISTRY-shaped profile + SOURCE_ID
[2] SCRIPT    Claude writes the ingestion script (returns a DataFrame of strings)
[3] LOAD      runs it, hashes the source, snapshot-replaces the landing table, logs the run
[4] DBT       generates staging + (optional) intermediate + mart models, writes them
[5] REGISTRY  upserts the source into LIBRARY_META.REGISTRY.SOURCE_REGISTRY
```

Nothing executes without your `go`. Batch mode shows a `[3 of 37]` counter and
tracks state in `onboarding_log.json` so an interrupted run resumes.

---

## Where everything lands (the live Ripple v6 layout)

```
LIBRARY_RAW.LANDING.<UPPER(SOURCE_ID)>      raw landing  (every column TEXT)
LIBRARY_META.REGISTRY.SOURCE_REGISTRY       the catalog  (keyed on SOURCE_ID)
LIBRARY_META.INGEST_LOGS.INGEST_RUNS        one row per ingest run
LIBRARY_STAGING / LIBRARY_MARTS              dbt outputs
```

**`SOURCE_ID` is the linchpin.** It's `<prefix>_<slug>` where the prefix is the
jurisdiction — `fed_` / `intl_` / `xc_` (cross-cutting) / `loc_` / `st_` — and the
landing table is literally `UPPER(SOURCE_ID)` (e.g. `fed_usgs_earthquakes` →
`LIBRARY_RAW.LANDING.FED_USGS_EARTHQUAKES`).

Every landing table is a verbatim, all-TEXT mirror of the source plus three
provenance columns:

| Column | Type | Meaning |
|--------|------|---------|
| `_INGESTED_AT` | TIMESTAMP_NTZ | when the agent loaded the row |
| `_SOURCE_RUN_ID` | VARCHAR | the run's UUID (joins to `INGEST_RUNS.RUN_ID`) |
| `_SRC_SHA256` | VARCHAR | SHA-256 of the source payload (joins to `INGEST_RUNS.SHA256`) |

Loads are **snapshot-replace** → re-running never duplicates. If the source's
SHA-256 matches its last successful run, the reload is skipped
(`ONBOARD_SKIP_IF_UNCHANGED=0` forces it).

---

## Setup

Install the repo's runtime deps from the **top-level** `requirements.txt` (it's the
complete, pinned set — covers this agent *and* the connect engine). From the repo root:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt            # ../requirements.txt from here
cp library-onboarding/.env.example library-onboarding/.env   # then fill in the blanks
```

(`library-onboarding/requirements.txt` still exists as the agent's own minimal,
unpinned subset, but the top-level file is the source of truth — use that.)

Minimum to fill in:

| Variable | Needed for |
|----------|-----------|
| `ANTHROPIC_API_KEY` | recon + codegen (any real run) |
| `SNOWFLAKE_PASSWORD` + `SNOWFLAKE_WAREHOUSE` | the LOAD + REGISTRY checkpoints |
| `DBT_PROJECT_PATH` | the DBT checkpoint (dir with `dbt_project.yml`) |

`.env` is gitignored. **No credentials are ever committed.** Account/user and the
`RIPPLE_*` database names default to the live values; override via env if needed.

### dbt source

The generated staging models read from `{{ source('ripple_raw', '<TABLE>') }}`.
Define that once in your dbt project's `sources.yml`:

```yaml
sources:
  - name: ripple_raw
    database: LIBRARY_RAW
    schema: LANDING
    tables:
      - name: FED_USGS_EARTHQUAKES   # etc.
```

---

## Try it offline first (no API key, no network, no Snowflake)

```bash
ONBOARD_FAKE_LLM=1 python onboard.py --name FRED
# add ONBOARD_AUTO_APPROVE=1 to auto-"go" every checkpoint (smoke test)
```

In fake mode the LOAD / DBT / REGISTRY steps run as dry runs (they print what they
*would* do) when the relevant credentials are absent.

---

## Files

```
onboard.py        entry point: single + batch modes, the checkpoint loop
sources_queue.py  the pre-loaded source queue
recon.py          [1] fetch docs + Claude recon -> resolved registry profile
ingest.py         [2][3] generate script, run it, hash + snapshot-replace + log the run
scaffold_dbt.py   [4] generate + write staging / intermediate / mart + schema.yml
register.py       [5] upsert SOURCE_REGISTRY
checkpoint.py     rich rendering + the go/edit/skip/abort prompt
naming.py         SOURCE_ID / landing-table / dbt-model conventions
snow.py           shared Snowflake connection + query helpers
llm.py            Claude client, prompt loading, offline fixtures
config.py         env-driven configuration (nothing hard-coded)
prompts/          recon / generate_ingest / generate_dbt / generate_catalog
onboarding_log.json  batch state (auto-created, gitignored)
```

---

## Known risks (and how the agent handles them)

- **Recon accuracy** — Claude reads docs pages that aren't always well structured.
  Checkpoint 1 is the safety net; use `edit` to correct it.
- **API keys** — some sources need one. Recon detects it and tells you the key and
  where to get it *before* the LOAD step.
- **Schema drift** — the loader fails loudly (e.g. on 0 rows) rather than loading garbage.
- **Generated code** — the ingestion script is model-generated; you review the exact
  code at Checkpoint 2 before it ever runs at Checkpoint 3.
- **Idempotency** — snapshot-replace + SHA-256 means re-running is safe and cheap.
