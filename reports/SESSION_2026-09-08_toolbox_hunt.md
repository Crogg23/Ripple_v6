# Session handoff — 2026-09-08, Tool Box hunt and the machine sweep

For a new session picking this up cold. Everything below was run live
against the warehouse through the Python door, `connect/db.py`,
role ACCOUNTADMIN, warehouse DBT_WH, read-only, SELECT only.

---

## What Chris asked for

A real hunt through the warehouse using `TOOL_BOX.md`. Not brainstorming.
Run queries, chase candidates, walk the chain on each one, and hand back
one file: `reports/toolbox_hunt_YYYY-MM-DD.md`.

Mid-session he asked whether the answer was to keep hunting or to audit
the whole warehouse in one pass. He picked **C**: sweep for the traps a
machine can find, hunt for the ones that need a hunch.

---

## What exists now

| Artefact | What it is |
|---|---|
| `reports/toolbox_hunt_2026-09-08.md` | 5 findings, chains intact, every query |
| `reports/trap_sweep_2026-09-08.csv` | 6,189 flags across 2,916 tables |
| `scripts/trap_sweep.py` | the 5 mechanical sweeps, re-runnable |
| `.claude/traps.md` | 191 lines, 9 added today |

---

## The five findings, one line each

| # | Subject | Finding | State |
|---|---|---|---|
| 1 | LABOR, OSHA 300A | zero-injury story died, filing artefact found | miss, trap kept |
| 2 | ECONOMICS, SBA PPP | 4% of loans land on an exact $10,000 | survives, cut down |
| 3 | ENVIRONMENT, EPA FRS | two facility tables, neither contains the other | survives |
| 4 | LABOR x ECONOMICS | OSHA and DOL headcounts agree, EIN bridges 19% | survives |
| 5 | HEALTH, CMS QPP | "graded as a crowd" | **DEAD**, trap kept |

**Finding 5 was killed at session close and the report shows the corpse.**
It came out of the machine sweep, and the framing was wrong: the file has
a `PARTICIPATION_OPTION` column that already labels individual against
group reporting, so the charges-block heuristic was a lossy version of a
published column and undercounted it by 34 points. The trap underneath is
real and is in the log. Do not rebuild the story.

**So nothing from today is built.** Findings 2, 3 and 4 are the shippable
ones and none has a chart.

---

## What the skeptic did to this session

A fresh-context reviewer got Chris's request verbatim and returned
**DISAGREE**. Findings 1, 3, 4 and the PPP misses survived; finding 2's
two headline numbers were artefacts and are struck in place, with the
struck version left visible in the report.

Every counter-claim was re-run against the warehouse before being
accepted. Three of my own errors it caught:

- a "116x to 2,210x chance" figure using a uniform-digit baseline the
  file's own data refutes
- an all-zeros EIN sentinel asserted from memory of the LEIE trap and
  never counted. It is zero rows in all three OSHA years
- a state rollup that hid 61,485 of 84,926 FRS orphans behind a NULL join

---

## The sweep, and how to re-run it

```
python3 scripts/trap_sweep.py --all --sample 100000 --threads 6
python3 scripts/trap_sweep.py --schema HEALTH        # one subject area
python3 scripts/trap_sweep.py --limit 20             # biggest 20 tables
```

Cost, metered from `snowflake.account_usage.query_history`, not guessed:
**2,916 tables in 43 minutes, 11,339 queries, about 1.7 credits.** Roughly
1.0 of that was cloud-services and 0.7 compute on an X-Small. The whole
day on DBT_WH billed 3.09. An earlier version of this file said "under one
credit"; that was derived from wall clock and was wrong.

Since then a duplicate `columns_for()` call was removed. It was 6,034
metadata lookups for 2,916 tables, about 40% of the sweep's cost. The
LABOR schema went from 98s to 34s after the fix, so a re-run should land
well under the 1.7.

Sampling caps each table at 100,000 rows; `--full` removes the cap and is
much more expensive.

### The five sweeps in plain words

| Sweep | What it looks for | Flags raised |
|---|---|---|
| S1 | the same numbers typed on many rows by one filer | 30 |
| S2 | a box that reads as filled but is empty | 3,331 |
| S3 | one value sitting in every row | **0 — it was broken, see below** |
| S4 | a column labelled a date, id or money that is not | 2,811 |
| S5 | one key in two tables that should agree | 13 |

S1 is the one that finds stories. The other four find chores that stop
you publishing a false number.

### S3 never ran in the 2026-09-08 CSV

`APPROX_TOP_K` returns pairs, `[["Group",360752]]`, and the script read
them as objects inside a bare `try/except`. Every column of every table
came back with a null top value. S3 raised zero flags across all 2,916
tables and that looked like a clean result. The S4 bare-year guard was
dead for the same reason, so all 506 `S4_date_name_not_date` rows in the
CSV are unguarded and some are noise.

Fixed 2026-09-08 and proved on the LABOR schema: S3 now raises 41 flags
on 12 tables where it previously raised 0. **The full CSV predates the
fix. A re-run would produce a materially different file.**

### Two gates S1 needs, both learned the hard way

- **cardinality** — without it S1 keys on YEAR columns and flags everything
- **tail** — without it S1 flags 76,365 MSHA rows at the standard $100
  minimum fine, which is the rulebook working, not an anomaly

Both are in the script. Do not remove them.

### Four tables the sweep could not read

`MARITIME__FED_NOAA_AIS`, `REFERENCE__CENSUS_CB_ZCTA`,
`REFERENCE__CENSUS_CB_COUNTY`, `REFERENCE__CENSUS_CB_STATE`.
All four fail with `Invalid argument types for function 'HLL'`, which is
`approx_count_distinct`, not `approx_top_k`. Almost certainly a GEOGRAPHY
column. Not investigated.

---

## The queue — S1 flags, ranked, verdicts where checked

Block sizes below are the sweep's `biggest block` figure, not the block
that was opened. On the QPP row the biggest block is 1,099 and the one
examined held 1,060 rows.

| Table | Block | Repeated value | Verdict |
|---|---|---|---|
| `HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE` | 1,099 | $329,265,077 | opened, story died, trap kept |
| `HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY` | 54,245 | 100, 100, 100 | noise, percent columns at 100 |
| `POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION` | 681 | $4,950 | the contribution limit, expected |
| `JUSTICE__FED_FJC_IDB_CIVIL` | 1,812 | 9,999 demanded, 0 received | unchecked, looks like a placeholder |
| `CORPORATE_REGISTRY__INTL_IE_CRO` | 3,310 | 1, 2,025 | unchecked |
| `LABOR__FED_OSHA_ITA_CASE_DETAIL_2023/24/25` | 142-370 | 8-figure hours | same Caltrans shape, already trapped |
| `HEALTH__FED_DEA_ARCOS` | 131 | 32, 54,000, 1,200 | unchecked |
| `JUSTICE__INTL_UCDP_GED` | 788 | -117, 33, 0 | unchecked, looks like coordinates |
| `TRANSPORT__FED_FRA_CASUALTIES` | 149 | 0, 0, 365 | unchecked |

NYC campaign contributions appear four separate times, in the 2001, 2009,
2013 and 2021 files, always at that cycle's contribution limit. That is
the ceiling, not a scandal, but the four-cycle repeat has never been drawn.

---

## Scale, so nobody re-derives it

```
tables in the warehouse, both sides        2,916
rows, both sides                     2.9 billion
real source files, not portal scrapes        660
agency families behind them                  196
state and city portal scrapes              1,563

Tool Box combos, moves x lenses x subjects  32,940
run on 2026-09-08                                4
file pairs never tried                     217,470
```

The hunt unit that works is **one subject area x one move**, and four of
those fills a session. That question is settled; it does not need
re-designing.

---

## Open, in Chris's hands

- Findings 2, 3 and 4 are unbuilt. No chart, no page
- Finding 5 is dead; only its trap is worth carrying forward
- The sweep CSV predates the S3 fix and is worth re-running
- The 9,999 in federal civil court is one query from a verdict
- Nothing has been published or shared anywhere

## Money

Everything today was read-only on DBT_WH, an X-Small. The full sweep ran
43 minutes. No spend gate was opened and no write, DDL or
`connect/incremental.py` command was run.
