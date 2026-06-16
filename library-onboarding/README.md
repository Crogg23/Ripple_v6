# Source Onboarding Agent

A CLI agent that onboards data sources into the Library end to end. Give it a
URL (or run the full batch) and it does recon, writes the ingestion script,
loads to Snowflake, scaffolds dbt models, and registers the table in
OpenMetadata — pausing at **five checkpoints** so you (the foreman) approve every
step before it runs.

```bash
# One source
python onboard.py --url https://fred.stlouisfed.org/docs/api/fred/
python onboard.py --name FRED            # or look it up in the queue by name

# The whole landscape sweep (37 sources), resumable
python onboard.py --batch
```

At every checkpoint you type one of:

```
go                     proceed
edit <feedback>        regenerate this step with your feedback, re-present
skip                   skip this source (batch mode moves to the next)
abort                  stop
```

---

## The 5-checkpoint flow

```
[1] RECON     reads the source docs, shows access pattern / auth / schema / IDs
[2] SCRIPT    writes the ingestion script, shows it
[3] LOAD      runs it, shows row counts + sample rows
[4] DBT       generates staging + mart models + schema.yml, writes them
[5] CATALOG   registers the raw table in OpenMetadata
```

Nothing executes without your `go`. In batch mode a `[3 of 37]` counter on each
banner tells you where you are.

---

## Setup

```bash
cd library-onboarding
python -m venv .venv && source .venv/bin/activate      # recommended
pip install -r requirements.txt
cp .env.example .env                                   # then fill in the blanks
```

Edit `.env` and provide, at minimum:

| Variable | Needed for | Notes |
|----------|-----------|-------|
| `ANTHROPIC_API_KEY` | recon, codegen | required for any real run |
| `SNOWFLAKE_PASSWORD` (+ `SNOWFLAKE_WAREHOUSE`) | the LOAD checkpoint | account/user/db default to your values |
| `DBT_PROJECT_PATH` | the DBT checkpoint | absolute path to the dir with `dbt_project.yml` |
| `OPENMETADATA_TOKEN` | the CATALOG checkpoint | `localhost:8585` → Settings → Access Token |

`.env` is gitignored. **No credentials are ever committed.** Per-source API keys
(e.g. a FRED key) are read from the environment by the generated ingestion
script — recon tells you exactly which ones you need and where to get them.

---

## Try it offline first (no API key, no network, no Snowflake)

A built-in fixture mode runs the entire flow with canned data so you can see the
checkpoints before wiring up credentials:

```bash
ONBOARD_FAKE_LLM=1 python onboard.py --name FRED
# add ONBOARD_AUTO_APPROVE=1 to auto-"go" every checkpoint (smoke test)
```

In fake mode the LOAD / DBT / CATALOG steps run as dry runs (they print what they
*would* do) when the corresponding credentials are absent.

---

## Where data lands

Every source gets a raw table laid out as (default `SNOWFLAKE_RAW_LAYOUT=schema_per_source`):

```
DISASTER_IMPACT.<SOURCE>.<TABLE>      e.g. DISASTER_IMPACT.FRED.SERIES_OBSERVATIONS
```

Every raw table carries three standard metadata columns alongside the source
columns (which land untransformed):

| Column | Type | Meaning |
|--------|------|---------|
| `_LOADED_AT` | TIMESTAMP_NTZ | when the agent loaded the row |
| `_SOURCE_URL` | VARCHAR | exact URL the data came from |
| `_SOURCE_FILE` | VARCHAR | filename, for bulk downloads |

Set `SNOWFLAKE_RAW_LAYOUT=single_schema` to instead use
`DISASTER_IMPACT.RAW.<SOURCE>_<TABLE>`.

---

## Files

```
onboard.py          entry point: single + batch modes, the checkpoint loop
sources_queue.py    the 37 pre-loaded sources
recon.py            [1] fetch docs + Claude recon -> resolved source config
ingest.py           [2][3] generate ingestion script, run it, load to Snowflake
scaffold_dbt.py     [4] generate + write staging/mart/schema.yml
register.py         [5] register the raw table in OpenMetadata (REST API)
checkpoint.py       rich rendering + the go/edit/skip/abort prompt
naming.py           shared table / model / schema naming conventions
llm.py              Claude client, prompt loading, offline fixtures
config.py           env-driven configuration (nothing hard-coded)
prompts/            recon / generate_ingest / generate_dbt / generate_catalog
onboarding_log.json batch state (auto-created, gitignored)
```

### Batch state

`onboarding_log.json` records `complete` / `skipped` / `aborted` per source. If a
batch run is interrupted, re-running `--batch` skips the sources already marked
`complete` and resumes.

---

## Known risks (and how the agent handles them)

- **Recon accuracy** — Claude reads docs pages that aren't always well structured.
  Checkpoint 1 is the safety net; use `edit` to correct it.
- **API keys** — some sources need one. Recon detects this and tells you the key
  and where to get it *before* the LOAD step.
- **Schema drift** — the loader fails loudly (e.g. on 0 rows) rather than loading
  garbage.
- **Generated code** — the ingestion script is model-generated. You review the
  exact code at Checkpoint 2 before it ever runs at Checkpoint 3.
- **OpenMetadata auth** — needs a token from `localhost:8585`; the CATALOG step
  fails loudly with that instruction if it's missing.

---

## Notes for this environment

This agent was scaffolded in a Linux cloud container, so a few things from the
original build plan are handled differently:

- **dbt project path** is configured via `DBT_PROJECT_PATH` (no machine-specific
  filesystem search). The DBT checkpoint validates that `dbt_project.yml` exists
  there before writing.
- **Credentials are not fetched from any secrets repo.** Fill in `.env` yourself;
  `.env.example` lists every variable and `.env` is gitignored.
- The default model is `claude-sonnet-4-6`; set `ANTHROPIC_MODEL` to trade cost
  for capability on recon/codegen.
