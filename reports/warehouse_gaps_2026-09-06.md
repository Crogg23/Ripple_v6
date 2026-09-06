# Where the warehouse is thin

Combed 2026-09-06 against the live warehouse. Metadata only, no table scans.

## The size of the place

| | count |
|---|---|
| tables | 2,893 |
| views | 552 |
| rows | 2,331,081,937 |
| landing tables | 2,212 |
| mart tables | 676 |

Of the landing tables, 1,563 came from open-data portals and hold 13.4 million rows
between them. The other 649 hold 1.36 billion. So the portal side is 71% of the tables
and 1% of the data.

## Gap 1: 335 portal tables stopped at a page limit

197 tables hold exactly 2,000 rows. 126 hold exactly 10,000. Another 12 sit at 5,000 or
1,000. That is not what those datasets contain; it is where a fetcher stopped asking.

The same bug was found and fixed for Oklahoma on 2026-09-05. Thirty two tables went from
320,000 rows to 992,000, then to 7,396,758 once the pager was reading every page of every
resource. Every portal loaded before that fix is still capped.

Fixing it means re-running the portal fetcher against the same list. Nothing new has to be
found, and no schema changes.

## Gap 2: 14 real sources stopped at a round number too

| rows | table |
|---|---|
| 50,000 | FED_USASPENDING_BULK |
| 10,000 | FED_SAM_EXCLUSIONS |
| 5,000 | FED_USGS_3DEP |
| 5,000 | FED_EPA_ENVIROFACTS |
| 5,000 | FED_USASPENDING_SUBAWARDS |
| 5,000 | INTL_DE_GOVDATA, INTL_GR_DATAGOV, INTL_CH_OPENDATASWISS |
| 2,000 | FED_DOL_OFCCP_CSAL, FED_ATF_FFL_LOCATIONS, INTL_HUDOC |
| 1,000 | FED_BJS_DATA, INTL_CL_DATOSGOB, INTL_ES_DATOSGOB |

These are not portals. Each is a named federal or international source that stopped at a
suspiciously flat number. `FED_SAM_EXCLUSIONS` at exactly 10,000 matters most: it is the
federal debarment list, and it feeds any question about banned companies winning work.

## Gap 3: 45% of landing tables have no date column

1,015 of 2,212 carry nothing date-shaped that is not a load stamp. For those tables it is
impossible to say what years they cover, so it is impossible to know whether they can be
joined to anything time-based.

Some of that is correct: a lookup list of state codes has no date. The rest is a real hole.

## Gap 4: coverage is measured on 215 tables of 2,893

Everything else has no recorded year span. Measuring is cheap, about 0.14 credits for 105
tables, and it is the check that catches two tables which can never overlap.

## Gap 5: half the tracked sources read stale

The freshness ledger tracks 102 sources. 51 read stale, 3 overdue, 20 unknown. Only 27
read fresh. The full breakdown, split into what is genuinely rotting and what is just
waiting on a publisher, is in `reports/stale_sources_2026-09-06.md`.

## Gap 6: 8 tables are empty and 544 hold under 100 rows

An empty table is either a failed load or a source with nothing to say. Nothing
distinguishes the two today.

## What I would fix, in order

1. Re-run the portal fetcher. 335 tables, a known fix, no new work.
2. Reload the 14 round-number sources, starting with the debarment list.
3. Measure years on the rest of the tables that have a date column.
4. Work the stale list, which already has its own plan.
