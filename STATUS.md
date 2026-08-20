# RIPPLE STATUS — 2026-08-20 — Time index built; the warehouse now knows what its own dates mean

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: two items.** (1) The roll-call vote mart still disagrees with its
Python-built twin — untouched, standing since 2026-08-18. (2) Twelve Python test
modules fail to COLLECT in this environment for a missing charting library —
pre-existing, unrelated to today's changes, but it means "the suite passed" now
carries an asterisk until that library is reinstalled.

---

## TODAY (2026-08-20) — the datetime lane, end to end

Chris asked what was worth trending over time. Answering it exposed that nobody
knew what the warehouse's dates MEANT, so the session turned into building that
knowledge and then fixing what it found.

### The finding that reframed everything

**The warehouse's dates were never badly broken — they were badly measured.**
The 2026-08-17 census only looked at columns Snowflake had already typed DATE or
TIMESTAMP. Landing is all-VARCHAR by design, so it walked past most of the real
clocks and, on some tables, measured Ripple's own download stamp instead. It also
reported each column's earliest/latest value, which a single junk row destroys —
that is why 89 tables looked "corrupt."

Counting actual bad ROWS: **6,084 genuinely bad rows in 1.2 billion.** Everything
else was two mechanical bugs of ours plus publishers encoding "not applicable" as
a date.

### Built

- **The datetime standard** (`macros/ripple_time.sql`) — eight rules, one shared
  parser. Shape-guarded: every format is applied only to values that already
  proved they match it, so it structurally cannot commit the bug it exists to
  prevent. A four-digit year never reaches a date parser. Proven against every
  trap case before being applied to anything.
- **The calendar** (`reference__calendar`) — 155,593 days, 1700→2125, matching
  the parser's window exactly. Carries federal fiscal year (Oct 1 start), FEC
  election cycle and Congress number. Verified on the Jan 3 congressional
  handover, the Oct 1 fiscal boundary and the 1st Congress.
- **The guard** (`tests/assert_ripple_time_standard.sql`) — fails the build if
  any of today's repairs regress or the calendar stops being dense. Passing.
- **The time index** (`reports/time_index/`) — every time column in the warehouse
  with its trusted window, grain, value shape and junk counts, plus a
  21-agent adversarially-reviewed labelling of what each column MEANS
  (happened / reported / decided / span / our download stamp / not a date).

### Fixed and verified live — 19 tables re-scanned with the same instrument

**57,664,460 junk rows removed (99.6%). Zero columns got worse.**

- **Download stamps, 12 tables.** `INGESTED_AT` is microseconds; a bare cast read
  it as seconds and put rows in the year 56,596,956. Nine fixed at the cast; three
  were corrupted by the LOADER before dbt ever saw them and are now recovered
  arithmetically. Offshore-leaks now stamps 2026-08-05; consumer injuries
  2026-07-26.
- **Century lost on two-digit years.** EPA ships `02-JUN-16`; the year was read
  literally. 8.1M facility dates were in years 0000–0026, now 2000→2026.
- **Publishers' "not applicable" markers, 18 columns.** 5.26M criminal defendants
  carried a fugitive-end-date of 1900-01-01 because they were never fugitives.
  Now NULL. Criminal sentencing dates went from 4M fake 1900s to a clean
  1995→2026 window.

### The judgment call worth knowing about

Before nulling any 1900-01-01, each column was tested for whether the marker is
an isolated spike or real history. **Two columns were deliberately left alone** —
a bank established-date and UK incorporation dates have thousands of genuine
records in the surrounding years. Blind nulling would have destroyed real
turn-of-the-century history.

## Live/open items

- **The canonical column is not rolled out.** Standard, calendar and guard exist;
  the 686 tables do not yet each expose one canonical timestamp with grain and
  clock tags. That is the build that makes a single shared timeline queryable,
  and it is the obvious next move.
- **The loader can still produce the microsecond bug.** The read side is now
  immune both ways, but the write side was left alone rather than risk breaking
  live ingests during a date cleanup.
- **The scan swept 40 July backup-schema tables** (237M rows) alongside live
  marts. All reported figures exclude them, but the scanner should filter them by
  default — same double-counting trap flagged earlier in the row-count catalog.
- **The trend sweep RAN** (371 series, 307 scored, zero failures) and its result
  is uncomfortable: most of the strangeness it found is about how data was
  COLLECTED, not what happened. That settles the long-parked question in the
  worst way — any trend claim from this warehouse needs its denominator first.
  Six series do look like the world moving (bank failures, nursing-home
  deficiencies up 446x, mine violations down 30%, rail crossings flat 14 years,
  complaints up 50x, pandemic loans). Full read: reports/time_index/TREND_FINDINGS.md.
- **CORRECTION carried forward:** the opioid shipment data covers 2006-2012, NOT
  2006-2026. 178.6M rows is right; the span is seven years. The 2026 end came
  from our own download stamp, which the old census reported as the date range —
  the exact failure this session existed to kill, caught in its own headline.
- **Nobody has read the map.** 4,899 connections, unexamined. Unchanged.
- Carried unchanged: 182 columns with literal 'nan' text; FAERS 76% dup; two FDA
  device tables raw; ~900 gated portal tables; DEA numbers single-source;
  roll-call mart rebuild; source-registry reconciliation; six unparseable polygon
  tables; table-count discrepancy.

**YOUR MOVE:** the sweep says the next real unlock is DENOMINATORS — pairing each
event series with what would explain it (inspections per inspector, filings per
filer, monitors online). Without that, no trend from this warehouse is safely
sayable. The alternative is the canonical-column rollout. Also standing: the
front-door website crash course, queued from 2026-08-19 and untouched today.

**NEXT SESSION (warehouse lane):** denominators for the six candidate real
signals, or the canonical-column rollout.
**NEXT SESSION (website lane):** Webflow crash course per the 8/19 handoff doc.

**Tests:** dbt — all repaired models rebuilt green; both datetime guards pass.
Python suite: **1,671 passed, 2 skipped, 1 failed, 12 collection errors** (14m41s).
The single failure is the KNOWN roll-call mismatch (113,512 rows vs 3,364),
standing since 2026-08-18 and untouched today — verified, not caused by these
changes. The 12 collection errors are a missing charting library in this
environment; they are why the count reads 1,671 rather than the 3,097 of
2026-08-18, and they hide ~1,400 tests that did not run at all.

**COST today:** ~$6–8 of warehouse compute (scan, probes, 20 rebuilds,
verification) — inside the $5–12 quoted. The 21-agent labelling pass was the
larger spend: ~3.4M agent tokens, roughly $20–40, unverified.
