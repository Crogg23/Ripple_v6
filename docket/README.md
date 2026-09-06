# The idea list

Every question worth asking the data, in one place, with what it would take.

## Just want something to work on

Open `INVESTIGATIONS.md`. The top five lines are the smallest jobs with nothing
missing. Pick one.

## The four files

| file | what it is |
|---|---|
| `investigations.csv` | the real list. This is the one you edit. |
| `INVESTIGATIONS.md` | the page you read. Built from the list. |
| `investigations_open.csv` | only what is still unanswered. Built from the list. |

The two built files get overwritten. Edit them and your changes vanish next rebuild.

Rebuild after any edit:

    python scripts/build_docket.py

## What a row says

| column | what it holds |
|---|---|
| `id` | its number. Stays the same forever, never reused. |
| `title` | who is involved |
| `question` | the question, one line |
| `why_it_matters` | why anyone should care |
| `where_it_stands` | one of seven phrases, below |
| `needs` | data that is missing or thin, if any |
| `tables` | the exact warehouse tables it would use |
| `rows` | how much data that is, all tables added up |
| `time_window` | what years the data covers |
| `effort` | rough guess at the work |
| `watch_out` | the trap, or what came back if it ran |
| `probe` | the folder holding the write-up, if it ran |

## The seven ways a question can stand

| word | means |
|---|---|
| `open` | nobody has run it |
| `partial` | started, not finished |
| `confirmed` | ran, and something real came back |
| `modest` | ran, real but thin |
| `dead` | ran, and there was nothing, or a piece was missing |
| `merged` | same question as another entry, folded in |

`dead` covers two endings.

One: there is no pattern.
Two: the years do not line up.

Both mean stop. The `watch_out` column says which one it was.

## Two columns that fill themselves

`probe` finds itself. A folder named `91_trade_then_bill` under `reports/` links
to entry 91 on the next rebuild. Thirty five entries have one.

`needs` is copied from the missing-data plan for the politics work. Eleven open
entries name something. When that data lands, those entries become pickable, and
nobody has to reread the plan to notice.

`needs` on an answered entry is not a blocker.

Entry E43 ran on one year of hospital finances.
More years would widen it, not undo it.

## The ordering, and why it is rough

The page ranks by how many tables a question touches, then by how many rows.

Fewer of both usually means a faster answer.

It is a guess, not a promise. Two tables and forty million rows is not a morning.
Nobody has timed all 150 by hand, so this is the best the sheet can do.

## Adding one

Add a row. Next free number, `where_it_stands` of `open`, and whatever you know about the
tables and years. Leave `probe` empty. Rebuild.

## Where it came from

Four spreadsheets written 2026-09-05.

All four held the same 150 rows with different column names.
The date in the filename meant a fresh copy every regeneration.
And `where_it_stands` had grown to 89 different phrasings for six states.

They still sit in `reports/`, marked superseded. Nothing reads them now.

## Checking the data is really there

    python scripts/docket_data_check.py

It reads the warehouse and asks, per entry: do these tables exist, how many rows,
what years, and is any of it stale. Results land in `DATA.md` and `docket_data.csv`.

As of 2026-09-06 every table the docket names exists.

That is the only thing that check proves. A question also needs the two sides to
share years, a column that really joins them, and a match that means what you
think. None of those three is checked yet. Every question that failed last week
would still read `all tables here`.
