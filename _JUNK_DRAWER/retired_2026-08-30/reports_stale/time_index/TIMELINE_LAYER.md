# The canonical clock layer — 2026-08-20, extended 2026-08-21

Every table in the warehouse that can be placed in time now exposes the same four
columns, and all of them roll up onto one shared timeline.

Built in 92 seconds. 435 models, zero failures. The guard test passes.

**2026-08-21 update: added the "planned" clock.** A happened/reported/decided
value that turns out to sit in the future — a proposed rule's effective date, a
scheduled hearing, an upcoming compliance deadline — used to either get read as
an ordinary past event (wrong) or get silently dropped once it was more than a
year out (data loss). Now every such value is checked per row: if it's after
today, `ripple_clock` reads `planned` instead of the base label, and the value
is kept, not nulled. span_start/span_end are untouched — their future values
were always correct data. See `ripple_row_clock` in `macros/ripple_time.sql`
and check #7 in `tests/assert_ripple_timeline_registry.sql`, which fails the
build if a `planned` row isn't actually in the future or vice versa.

## What exists now

| thing | where | what it is |
|---|---|---|
| 403 canonical views | `LIBRARY_MARTS.TIMELINE.<TABLE_NAME>` | every original column, untouched, plus the canonical four |
| 31 domain rollups | `LIBRARY_MARTS.TIMELINE.TIMELINE__<DOMAIN>_INDEX` | one row per (source, clock, grain, day) with a count |
| the shared timeline | `LIBRARY_MARTS.TIMELINE.TIMELINE__WAREHOUSE` | all of them together — 1,160,701 rows covering 719,999,851 underlying rows |
| the control table | `LIBRARY_MARTS.TIMELINE.RIPPLE_TIME_REGISTRY` | all 647 live tables, the clock chosen for each, and why |
| the guard | `tests/assert_ripple_timeline_registry.sql` | fails the build if the registry and the views drift apart |

## The canonical four

| column | what it holds |
|---|---|
| `ripple_ts` | TIMESTAMP_NTZ, snapped to the start of its period, clamped to 1700–2125 |
| `ripple_grain` | `day` / `month` / `quarter` / `year` — how precise that timestamp really is |
| `ripple_clock` | `happened` / `reported` / `decided` / `span_start` / `span_end` / `planned` — what it MEANS |
| `ripple_source` | the schema-qualified table it came from |

## The three rules you must respect when querying

**1. Always honour `ripple_grain`.** A year-grain source snaps to January 1st. Draw
a daily chart across mixed grains without filtering and you invent a New Year's
Day spike out of nothing. 121 of the 403 sources are year-grain.

**2. Always honour `ripple_clock`.** Summing a `happened` source and a `reported`
source into one line adds two different questions together. 230 sources are
`happened`, 95 are `reported`, 33 `decided`, 45 are span boundaries.

**3. Exclude `planned` by default.** A `planned` row hasn't occurred yet and might
still change — it comes from a happened/reported/decided column whose value turns
out to be in the future. Any "what occurred" analysis (a FLOW rule, a timeline of
past events) must filter it out unless the question is specifically about what's
upcoming. It is a per-row tag, not a per-table one: the same enforcement-date
column can carry mostly `decided` rows and a handful of `planned` ones.

## Coverage, stated honestly

- **647 live mart tables.** 403 have a usable clock and get a view.
- **244 do not**, and the registry says which kind of nothing each one is:
  - 165 were never examined — no column name in them looks like a clock
  - 43 have time-shaped column names that hold no readable time value
  - 20 carry nothing but Ripple's own download stamp, which is not a clock for
    anything in the world
  - 16 have no time data at all

A table missing from the registry would be indistinguishable from one that was
checked and found to have no clock. That ambiguity is what the registry exists to
remove, so every live table is listed whether or not it made it into the layer.

## What the layer can already answer

- **What was happening anywhere in the warehouse in a given month.** March 2020,
  day-grain sources only: FDA device adverse events (94,483), Canadian political
  contributions (92,882), federal bankruptcies (67,144), consumer complaints
  (29,480), emergency-room injury records (23,559).
- **Which sources have gone quiet, and exactly when.** Open Payments stops dead
  at 2023-12-31 (14.7M rows), the FBI crime explorer at 2023-12-01, pandemic
  loans at 2021-07-19.
- **Whether any source covers a date at all**, before a question is asked.
- **How many independent sources touch the same day** — the cheapest available
  test of whether a pattern is one publisher's artifact or something wider.

## The edges, checked

- **Earliest: 1700.** Real history, not junk — slave-voyage records, 18th-century
  court opinions, roll-call votes from the 1st Congress (1789), CO₂ estimates
  from 1750.
- **Latest: 2105.** 45 rows in total, every one a `span_start` — a corporate
  relationship recorded as beginning in 2088, a federal exclusion starting in
  2099. Almost certainly typos at the source. Left as-is and visible rather than
  silently clamped.

## Why views and not columns in the marts

Adding three columns to 600+ mart models would mean rebuilding every mart: hours
of warehouse time, real money, and rebuild risk on tables that are currently
correct. A view computes the same three columns at query time, costs nothing to
create or store, leaves the underlying tables untouched (rule 8 of the datetime
standard: the raw column is never overwritten), and regenerates in seconds when a
clock label is corrected.

That last point is the deciding one. The clock labels are a day old — a 21-agent
review pass produced them this morning — so cheap regeneration matters more than
saving a parse at query time.

## What is NOT done

- **The layer counts; it does not join.** The shared timeline holds counts per
  source per day. Row-level detail lives in the per-table views, one source at a
  time. A true row-level cross-warehouse timeline would be ~720M rows and has not
  been built.
- **The 244 unclocked tables stay unclocked.** Most genuinely have no time data.
  The 20 carrying only a download stamp are the fixable ones — they need a real
  clock at ingest, upstream of here.
- **A clock label being CORRECT is not tested.** The guard enforces that the
  registry and the warehouse agree; whether `SURVEY_DATE` really means "happened"
  is a judgement from this morning's review pass, and revisable.

## Regenerating

`python scripts/census/gen_time_views.py --clean` rewrites all 435 model files
and the registry seed from `reports/time_index/clock_index.csv`. It runs no SQL.
Then `dbt seed --select ripple_time_registry` and
`dbt run --select path:models/timeline`.
