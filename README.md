# Ripple_v6

Investigative Journalism — a Snowflake-backed data Library, its source catalog, and
the agents that build both.

## Quick start (one command)

From the repo root, create a virtualenv and install every runtime dependency:

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

That's everything `python -m connect all` and `python onboard.py` need (plotly,
snowflake-connector-python, pandas, pyarrow, rich, etc. — all pinned in
`requirements.txt`).

Running the tests too? Add the dev/test deps:

```bash
pip install -r requirements-dev.txt
```

Then drop your Snowflake token into `library-onboarding/.env` (see
`library-onboarding/.env.example`) and you're live.

## The two entry points

```bash
python -m connect all                       # profile every landed table, find real
                                            # cross-dataset connections, draw the graph
python library-onboarding/onboard.py --batch   # onboard new sources into the Library
```

- **`connect/`** — the connection engine (entity resolution, the confidence ladder,
  the graph + connection explorer). See `connect/HOWTO.md`.
- **`library-onboarding/`** — the 5-checkpoint source-onboarding agent. See
  `library-onboarding/README.md`.

> Note: `dbt-snowflake` is listed in `requirements.txt` (it runs/tests the 73 dbt
> models in `library-onboarding/ripple_dbt`) but is **not** installed in the dev
> environment by default — install it when you need to `dbt run` / `dbt test`.
