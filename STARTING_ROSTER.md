# STARTING ROSTER — what is live, 2026-08-30

This file is the line between live work and dead work.
If a folder is not on this roster, it is not part of current work.
Dead work lives in `_JUNK_DRAWER/` with rows in its LEDGER.md.
The spine is dead. Nothing new gets called a spine.

## The live core

| Folder | What it is |
|---|---|
| `connect/` | entity resolution + join-key engine; the heart |
| `loadkit/` | atomic load / checkpoint / preflight toolkit |
| `library-onboarding/` | dbt project + source downloaders |
| `scripts/` | operational tools; slash-command backends live here |
| `tests/` | the suite; 724 collect, 694 pass offline |
| `data/` | loader resume logs, staged dumps, `raw_dropins/` |
| `docs/` | canonical prose: RIPPLE.md, tech spec, Laboratory |
| `reports/recon/` | pass-1/pass-2 connections work — current |
| `reports/viz/` + `_build/` | the join handbook + chain explorer |
| `reports/location_index/`, `reports/lab_map/`, `reports/row1/` | live reference indexes |
| `.claude/` | rulebook v2: hooks, gates, slash words |
| `.snowflake/` | the Python-scripts warehouse door |

## Supporting cast (kept, low churn)

| Folder | Why kept |
|---|---|
| `viz/` | chart library; ripple CLI imports it |
| `ripple/` + `ripple.py` | CLI; three live scripts import ripple.common |
| `portal_recon/` | looks dead, is NOT: connect/keys.py reuses its tagger |
| `glossary/` | looks dead, is NOT: census script + a live test use it |
| `reports/typing_index/` | looks dead, is NOT: the typing scripts read its rulings |
| `infra/` | keys ledger + launchd; operational |
| `web/` | the Astro portfolio site, separate project |
| `outputs/` | slimmed to referenced artifacts + checkpoints |
| `reports/_heavy/` | big machine CSVs/JSON, kept out of context paths |
| `notebooks/`, `__marimo__/`, `notebook.py` | marimo notebooks |

## Dead — in the drawer

bench, evidence, home, honesty, hunch, investigations,
mission_control, playground, politics, queues, reading_room, serve,
old `archive/`, stale reports and outputs, bat launchers.
All under `_JUNK_DRAWER/retired_2026-08-30/`. Reference only.

## Spine — dead and drawered (2026-08-30, greenlit)

The spine code, its 5 tests, 6 scripts, and all spine reports are in
`_JUNK_DRAWER/retired_2026-08-30/spine_era/`. The two shared SQL
expressions live code needed were lifted into `connect/normalize.py`;
both importers were repointed, behavior unchanged. `python -m connect
spine` now exits with a retired message; `all` skips it.

## After-effects of retiring the full rebuild

The old rebuild ran two tail steps automatically.

Entity index: the all command now refreshes it again, Chris's call.

Post-rebuild sync: only the seed subcommand reaches it now.

## Traps found during this organize

- `portal_recon/` reads as dead by imports; `connect/keys.py` needs it.
- Spine tests run green against a dead system; failures there are noise.
