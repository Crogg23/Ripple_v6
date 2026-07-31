# Ripple_v6

Investigative Journalism — a Snowflake-backed data Library, its source catalog, and
the agents that build both.

## Read next

- [`docs/ripple_pitch_deck.md`](docs/ripple_pitch_deck.md) — the best single overview:
  real numbers, real SQL, honest about what's unproven. Start here.
- [`docs/RIPPLE_FOR_EVERYONE.md`](docs/RIPPLE_FOR_EVERYONE.md) — the plain-English version.
- [`honesty/README.md`](honesty/README.md) — the fact/lead/unverified provenance grader;
  the most distinctive piece of architecture in this repo.
- [`OVERVIEW.md`](OVERVIEW.md) — the architecture tour.
- [`PROJECT_SHAPE.md`](PROJECT_SHAPE.md) — an outside reviewer's honest read of the project.

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
- **`library-onboarding/`** — the 6-checkpoint source-onboarding agent. See
  `library-onboarding/README.md`.

> Note: dbt runs/tests the 1,378 models in `library-onboarding/ripple_dbt` — 975
> staging, 399 marts, 4 intermediate — but it is **deliberately not in
> `requirements.txt`**. `dbt-snowflake` requires `snowflake-connector-python~=3.0`,
> which genuinely conflicts with this repo's `==4.4.0` pin (pip refuses both in one
> environment). Install it into its own venv when you need `dbt run` / `dbt test`:
>
> ```bash
> python3 -m venv .dbt-venv && .dbt-venv/bin/pip install -r requirements-dbt.txt
> ```
