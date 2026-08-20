# The Ripple Time Index — 2026-08-20

What clock every dataset in the warehouse runs on, what was broken, and what got
fixed. Built in one session from a full read-only scan plus a 21-agent
classification pass.

## What was measured

- **686 tables scanned, zero failures.** 2,223 time-shaped columns,
  1,195,018,298 rows.
- **40 of those 686 turned out to be July backup schemas**, not live marts —
  they hold 237M rows and 8.1M of the junk. Every headline below is the LIVE
  figure with those excluded. (Same double-counting trap an earlier session
  flagged in the row-count catalog; the scanner walked into it too, because it
  enumerates every schema in the marts database.)
- **Live: 647 tables, 2,098 time columns, 958M rows.**
- Every column measured regardless of its Snowflake type. This is the whole
  point: landing is all-VARCHAR by design, so the previous census — which only
  looked at columns already typed DATE or TIMESTAMP — walked past most of the
  real clocks in the building and mistook Ripple's own download stamps for them.

## The headline

**478 live tables have a real, usable clock** — 334 of them down to the day,
covering 738M rows; 12 to the month, 5 to the quarter, 127 to the year only. The
previous census claimed 349 tables had dates and only 164 were trustworthy.

**Most of Ripple's time data is not dates.** Of the 2,098 live columns: 402 hold
a bare year, 34 a year-month, 21 a year-quarter, and 590 turn out not to be time
at all. More columns hold a plain year than
hold a properly formatted date. Any standard that only handles dates covers less
than half the warehouse — which is why the canonical column snaps coarse grains
to the start of their period and carries a grain tag.

## What the junk actually was

57.7M live rows (6.0%) carried something a chart would render wrong. It resolves
into four causes, and only two of them are Ripple's fault:

| cause | rows | whose fault | status |
|---|---:|---|---|
| Source writes `1900-01-01` to mean "not applicable" | 30.9M | nobody's | translated to NULL |
| Our download stamp cast as seconds, not microseconds | 18.6M | ours | fixed |
| Two-digit year, century lost | 16.3M | ours | fixed |
| Genuinely bad rows | **6,084** | real junk | left, documented |

Six thousand genuinely bad rows in 1.2 billion. The warehouse's dates were never
the problem — they were mismeasured. The old census read each column's earliest
and latest value, and one junk row drags that to year 0001 or 9999 and makes an
entire healthy table look destroyed.

### The two real bugs, in detail

**Download stamps read at the wrong scale (18.6M rows, 12 tables).** Two variants
of one bug:

*In the model (9 tables).* `INGESTED_AT` lands as a NUMBER of microseconds since
epoch (e.g. `1785965270036203`). A bare `to_timestamp` reads it as seconds and
puts the row in the year 56,596,956 — which is exactly what poisoned the
offshore-leaks family's measured date range. Fixed with the `, 6` scale
argument; verified, those tables now stamp 2026-08-05.

*In the loader (3 tables).* For the consumer-injury, research-grant and
sanctions files the landing column is **already** a corrupted TIMESTAMP — the
bad cast happened before the row ever reached dbt, so no model change could have
prevented it. The original is exactly recoverable (the stored timestamp's epoch
seconds ARE the original microseconds), and `ripple_recover_ingest_ts()` does
that. Verified: the consumer-injury stamp recovers to 2026-07-26 and the
research-grant one to 2026-08-10, both matching their real load dates.

**The loader itself is NOT fixed** — see "What is NOT done".

**Century lost on two-digit years (16.3M rows).** EPA ships facility dates as
`DD-MON-YY` — `01-MAR-00`, `02-JUN-16`, `25-SEP-25`. A bare parse read the year
literally, putting all 5,300,149 create dates and 2,782,106 update dates in years
0000–0026. **99.3% of this bug is that one dataset, which is loaded twice.** The
other 47 columns originally bucketed here total 1,199 rows, median 5 each — noise.
Fixed with an explicit century pivot. Verified: create dates now run 2000-03-01
to 2026-06-30, zero rows before 1990.

### The judgment call that mattered

Before nulling any `1900-01-01`, every candidate column was tested for whether the
marker is an isolated spike or part of a real distribution: count on exactly
1900-01-01 versus count anywhere else in 1899–1901.

- **16 columns were unambiguous sentinels** — zero neighbouring dates at all, in
  databases that begin in 1970. Nulled. The clearest case: 5.26M criminal
  defendants carry a "date they stopped being a fugitive" of 1900-01-01 because
  they were never fugitives.
- **2 columns were left alone.** A bank branch established-date has 14,034 real
  dates in the surrounding years, and UK incorporation dates likewise. Blind
  nulling would have destroyed genuine turn-of-the-century history.

## The measured result

The 19 repaired tables were re-scanned with the same instrument that found the
problems, so this is measured, not asserted:

| | junk rows |
|---|---:|
| before | 57,884,577 |
| after | 220,117 |
| **removed** | **57,664,460 (99.6%)** |

**Zero columns got worse.** What remains is almost entirely legitimate
future-dated contract and permit end dates, which the scan's single ceiling
flags but the clock labels correctly excuse.

A few windows worth seeing, before and after:

- Criminal sentencing dates: were 4,062,155 rows sitting on a fake 1900-01-01;
  now a clean 1995-10-01 → 2026-03-31.
- EPA facility creation dates: were years 0000–0026; now 2000-03-01 → 2026-06-30.
- The consumer-injury file's load stamp: was the year 56,569,708; now 2026-07-26.
- The appellate court-record date is now entirely NULL — correctly. All 988,183
  rows held the not-applicable marker, so the column never carried real data;
  it now says so honestly instead of claiming every appeal was recorded in 1900.

## What was built

- **`macros/ripple_time.sql`** — the datetime standard. Eight rules, and a
  shape-guarded parser that cannot commit the bug it exists to prevent: every
  format is applied only to values that already proved they match it, and a
  four-digit year never goes near a date parser. Proven against every trap case
  before being applied to anything.
- **`models/marts/reference/reference__calendar.sql`** — 155,593 days,
  1700-01-01 to 2125-12-31, matching the parser's trusted window exactly. Carries
  federal fiscal year (Oct 1 start), FEC election cycle, and Congress number
  alongside the ordinary calendar parts. Verified on the Jan 3 congressional
  handover, the Oct 1 fiscal boundary, and the 1st Congress.
- **`tests/assert_ripple_time_standard.sql`** — the guard. Fails the build if any
  repair regresses, if the calendar stops covering the trusted window, or if it
  stops being one dense row per day.

## Files here

| file | what it holds |
|---|---|
| `scan.jsonl` | raw scan output, one record per table |
| `columns.csv` | one row per time column: window, grain, junk counts, shape |
| `clock_index.csv` | every column labelled happened / reported / decided / span / ingest / not-a-date, with the adversarial review's overturns |
| `CLOCK_FINDINGS.md` | the classification write-up (note: its own section 4–5 lists are floors — it flags that its input was truncated; the CSV is complete) |
| `_raw_format_probe.json` | true raw value samples behind each fixed column |
| `_blank_marker_verdicts.json` | the sentinel-versus-real-history discriminator results |

## What is NOT done

- **The canonical column is not rolled out.** The standard, the calendar and the
  guard exist and the real bugs are fixed, but the 686 tables do not yet each
  expose a canonical timestamp with grain and clock tags. That is the next
  build, and it is what makes one shared timeline actually queryable.
- **~11,000 junk rows remain** across roughly 100 columns, median 5 rows each.
  Below the noise floor; the standard's window clamp nulls them wherever it gets
  applied.
- **The loader can still produce this.** The ingest helper hands `write_pandas` a
  Python datetime; where the landing column already exists as a NUMBER, the raw
  microseconds get written and the next model to cast them naively repeats the
  bug. The READ side is now immune either way — the scale argument covers the
  NUMBER case, and the recovery macro covers the already-corrupt case and passes
  sane values through untouched — but the write side was deliberately left alone
  rather than risk breaking live ingests for a date cleanup. Open item.
- **The scan covers marts only** — not the ~1,200 staging views or the raw
  landing tables beneath them.
- **Day-first versus month-first dates are unknowable from values alone.**
  `03/04/2020` is valid read either way. Nothing here detects that; it needs
  per-publisher knowledge.
