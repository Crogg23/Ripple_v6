# Rebuild the Ripple docket from scratch

You are doing recon on a data warehouse. Your job is to read what's on
the shelf and come back with every idea worth building. Nothing else.

## What Ripple is

A solo project that turns public government data into data visualizations.
The output is a portfolio piece. It needs a wow factor.
"Interesting" beats "rigorous" here — this is the exploratory pass.

## Your two inputs

| File | What it is |
|---|---|
| reports/warehouse_table_inventory_2026-09-07.csv | 704 tables, plain-word description of each |
| reports/viz_join_catalog_2026-09-04.md | 4,512 proven table pairs, 30 key types |

Read the inventory in full. All 704 rows. Do not sample it.
The join catalog tells you which tables actually connect.
If two tables are not in that catalog, do not assume they join.

## What one idea is

Widest possible net. An idea is any of these:

- One data visualization worth making
- A group of visuals that go together
- A story that can be told through data visuals
- Anything interesting
- Anything worth investigating

Do not filter for importance, novelty, or feasibility. If it made you
look twice while reading the inventory, it is an idea. Write it down.

## What each idea must carry

| Field | Rule |
|---|---|
| title | Names the physical thing, not a concept |
| question | One sentence, ends in a question mark |
| why_it_matters | One sentence. What a reader would feel |
| tables | Full names, pipe-separated, from the inventory only |
| joins_on | The key, or "single table" |
| visual | What it looks like — map, flow, timeline, ranking, other |
| notes | Anything you noticed. Optional |

## Rules on evidence

Cite tables. That is the whole standard.
Do not write SQL. Do not run queries. Do not estimate row counts.
Never name a table that is not in the inventory CSV.
Never claim a join that is not in the join catalog.
If you want a table that does not exist, say so in a separate list.

## How to organize it

By subject. Use the schema names already in the inventory.
The big ones, by table count:

HEALTH 106 · POLITICS 85 · ENVIRONMENT 75 · JUSTICE 65 · FINANCE 61
ECONOMICS 42 · TIMELINE 36 · REFERENCE 34 · ENERGY 29 · HOUSING 18

Inside each subject, sort by crawl / walk / run:

- **crawl** — one table, one chart, done in a sitting
- **walk** — two or three tables, one proven join
- **run** — many tables, or a real build

No ranking. No scores. No priority column. Just the shelf, organized.

## Quotas

None. No minimum, no maximum, no coverage target.
Do not pad a thin subject. Do not cap a rich one.
Stop when you run out of interesting, not when you hit a number.

## Voice

Plain words. Short lines. Say the physical thing.
Not "anomaly detection pipeline" — say "duplicate addresses on one P.O. box."
Not "engagement metrics" — say "how many people opened it."
A title a stranger has to decode is a bad title.

## What you hand back

Two files.

1. `docket_v2_YYYY-MM-DD.csv` — every idea, the seven fields above
2. `docket_v2_notes_YYYY-MM-DD.md` — what you found, by subject,
   plus a list of tables you could not make anything of, and why

## The one thing you do last

Only after both files are written, open `docket/docket.csv`.
That is the old docket — 150 ideas built before you.
Do not read it before you finish. Your pass must be independent.

Then add a third file: `docket_v2_vs_v1_YYYY-MM-DD.md`

| Section | What goes in it |
|---|---|
| Both found it | Ideas that appear in yours and the old one |
| Only you | Ideas the old docket missed |
| Only the old one | Ideas you missed, and whether they hold up |
| Dead in the old one | Old lines whose tables no longer exist |
