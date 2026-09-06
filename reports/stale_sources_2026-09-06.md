# The 52 stale sources, 2026-09-06

From LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS, rebuilt today after the parser repairs.
"Stale" means past the last grace window for that cadence. That single word hides three
different situations, so they are split here. "Cycles late" is days behind divided by the
source's own update period — a daily feed 30 days old is 30x late, an annual one 1.5x.

## Rotting: a fast feed that stopped (31)

These update daily, weekly or monthly and have not. This is the bucket worth acting on.

| source | data through | cadence | rows | cycles late |
|---|---|---|---|---|
| fed_noaa_ais | 2024-01-08 | daily | 58,106,517 | 972x |
| fed_usaspending_contracts | 2025-09-30 | daily | 6,325,622 | 341x |
| xc_biorxiv_medrxiv | 2026-05-18 | real_time | 432 | 111x |
| intl_es_borme | 2026-06-01 | daily | 25 | 97x |
| intl_ec_sercop | 2026-06-05 | daily | 132,995 | 93x |
| fed_cms_nadac | 2024-12-25 | weekly | 1,497,925 | 89x |
| xc_wapo_fatal_force | 2024-12-31 | weekly | 10,430 | 88x |
| fed_usgs_earthquakes | 2026-06-13 | real_time | 443,274 | 85x |
| fed_treasury_debt_to_penny | 2026-06-15 | daily | 8,329 | 83x |
| fed_clinicaltrials | 2026-06-16 | daily | 500 | 82x |
| fed_federal_register_documents | 2026-06-16 | daily | 94,731 | 82x |
| intl_opensanctions | 2026-06-26 | daily | 71,011 | 72x |
| fed_cfpb_complaints | 2026-07-23 | daily | 17,179,788 | 45x |
| fed_fara_bulk | 2026-07-30 | daily | 221,900 | 38x |
| fed_cdc_anxiety_depression | 2024-09-16 | monthly | 16,794 | 24x |
| fed_cisa_kev | 2026-08-21 | daily | 1,674 | 16x |
| xc_ransomwarelive_victims | 2026-08-22 | daily | 31,089 | 15x |
| fed_epa_echo | 2026-06-19 | weekly | 3,157,891 | 11x |
| fed_cms_home_health | 2025-10-09 | monthly | 12,392 | 11x |
| fed_cms_hospice | 2025-10-15 | monthly | 6,852 | 11x |
| fed_noaa_storm_events | 2025-12-01 | monthly | 1,780,730 | 9x |
| fed_sec_edgar_financials | 2024-12-31 | quarterly | 55,635 | 7x |
| fed_cms_ltch | 2025-02-01 | quarterly | 311 | 6x |
| xc_guttmacher_monthly_abortion | 2026-03-15 | monthly | 2,040 | 6x |
| fed_cms_nursing_home | 2026-05-01 | monthly | 14,700 | 4x |
| fed_treasury_avg_interest_rates | 2026-05-31 | monthly | 4,961 | 3x |
| fed_cms_nppes | 2026-06-08 | monthly | 9,606,683 | 3x |
| xc_wayback_doj_epstein | 2026-06-09 | monthly | 1,537,352 | 3x |
| fed_irs_revocation | 2026-06-09 | monthly | 1,206,628 | 3x |
| fed_doj_epstein_library | 2026-06-11 | monthly | 777 | 3x |
| fed_cms_pos_other | 2026-03-26 | quarterly | 44,429 | 2x |

## Waiting on the publisher (15)

Annual and irregular sources sitting at the publisher's own latest release. Nothing is
broken; the next file does not exist yet. The annual grace window of 400 days is simply
tighter than the real publishing lag.

| source | data through | cadence | rows | cycles late |
|---|---|---|---|---|
| xc_owid_fertility | 2023-12-31 | annual | 19,402 | 3x |
| intl_it_istat | 2023-12-31 | irregular | 213,284 | 3x |
| fed_va_suicide_appendix | 2023-12-31 | annual | 144 | 3x |
| xc_owid_life_expectancy | 2023-12-31 | annual | 21,565 | 3x |
| fed_cms_open_payments_2023 | 2023-12-31 | annual | 14,700,786 | 3x |
| fed_cms_hcris | 2024-09-30 | annual | 6,103 | 2x |
| xc_owid_homicide | 2024-12-31 | annual | 4,912 | 2x |
| fed_cms_open_payments | 2024-12-31 | annual | 15,385,047 | 2x |
| xc_owid_refugees | 2024-12-31 | annual | 7,442 | 2x |
| intl_voeten_unga_votes | 2024-12-31 | annual | 1,823,352 | 2x |
| xc_owid_fossil_share | 2024-12-31 | annual | 6,379 | 2x |
| xc_owid_co2 | 2024-12-31 | annual | 29,384 | 2x |
| intl_ucdp_ged | 2024-12-31 | annual | 385,918 | 2x |
| fed_cdc_injury_violence_county | 2024-12-31 | annual | 132,000 | 2x |
| xc_owid_cpi | 2024-12-31 | annual | 2,312 | 2x |

## Abandoned: over three years old (6)

| source | data through | cadence | rows | cycles late |
|---|---|---|---|---|
| fed_oyez | 1973-01-22 | irregular | 25 | 54x |
| fed_cdc_drug_poisoning_county | 2015-12-31 | annual | 53,387 | 11x |
| fed_cdc_suicide_rates | 2018-12-31 | annual | 6,390 | 8x |
| fed_naag_multistate_settlements | 2021-07-23 | irregular | 882 | 5x |
| xc_owid_terrorism_deaths | 2021-12-31 | annual | 10,481 | 5x |
| fed_fbi_nics_checks | 2023-09-01 | monthly | 16,445 | 37x |

---

# What can be done, and how fast

## The machine already exists and is running on an empty list

`infra/ddl/09_scheduled_refresh.sql` built a server-side refresh: Snowflake fetches the
URL itself, checks the origin ETag, COPYs, guards against shrink, swaps atomically and
writes INGEST_RUNS. No laptop in the loop.

`RIPPLE_BULK_REFRESH_TASK` is not suspended. It is **started**, on cron 0 8 UTC daily, and
it succeeded on 2026-09-04, 09-05 and 09-06. It refreshed nothing on any of those days,
because the control table `LIBRARY_META.REGISTRY.BULK_REFRESH` holds 23 entries and every
one has `ENABLED = FALSE`. One entry has ever recorded a `LAST_REFRESH_AT`.

That is the single largest lever here. The scheduler runs daily and is opted out of.

## The 31 rotting sources, by what it takes

| tier | count | what it takes | how fast |
|---|---|---|---|
| A. spec already written | 2 | one command each, cloud-to-cloud | today |
| B. plain bulk download, no auth | 20 | one client run to record the schema, then schedulable | 2-3 days |
| C. API or scrape | 9 | needs its client loader; no unattended path today | per-source work |

Tier A is `fed_usaspending_contracts`, 341 cycles late on 6.3M rows, and
`fed_cfpb_complaints`, 45 cycles late on 17.2M rows. Both have a `server_side_load.py`
spec today.

Tier B is every source the registry marks `bulk` or `bulk_download` with `AUTH_REQUIRED
= none`. `server_side_load.py` writes a `BULK_REFRESH` row on each success, so a single
successful run is what converts a source from hand-run to scheduled. The heavy ones are
`fed_cms_nppes` at 9.6M rows and `fed_epa_echo` at 3.2M.

Tier C is the API and scrape sources: opensanctions, clinicaltrials, biorxiv, usgs
earthquakes, borme, sercop, and the wayback pulls. Server-side fetch cannot page an API.

## Price

From the query log, 223 prior `RIPPLE_FETCH_TO_STAGE` calls in 90 days: p50 6 seconds and
$0.00, max 13.8 minutes and $0.46, all on X-Small. That is the per-source fetch. There is
no prior run of `RIPPLE_REFRESH_ENABLED` with sources turned on, so the nightly cost of an
enabled task has **no real number** yet.

## The order I would take

1. Refresh the two tier-A sources by hand. Confirms the path end to end before anything
   is scheduled.
2. Turn on `ENABLED` for the 22 schedulable entries already in `BULK_REFRESH`. They are
   mostly not yet rotting; this is what stops the next 52.
3. Work tier B in descending cycles-late, one client run each, which registers each one
   for the nightly task as a side effect.
4. Re-measure coverage after each, so a refresh that landed nothing is visible.
5. Leave tier C for a separate decision; those are loader work, not config.

## The annual threshold, separately

15 of the 52 are annual or irregular sources sitting at their publisher's own latest
release. The grace window for `annual` is 400 days, which is tighter than the real
publishing lag for most federal annual files. Widening it would move 15 rows out of
'stale' without touching any data. That is a judgement call about the word, not a fix.

---

# Tier A, run 2026-09-06

## CFPB complaints: refreshed, now fresh

`server_side_load.py --spec FED_CFPB_COMPLAINTS --run --refresh`. Snowflake fetched the
1.43 GB zip itself, unzipped to 1.84 GB, COPYed and swapped.

| | before | after |
|---|---|---|
| rows | 17,179,788 | 17,589,039 |
| data through | 2026-07-23 | 2026-09-06 |
| coverage years | 2011-2026 | 2012-2026, one stray trimmed |
| state | stale, 45 cycles late | fresh |

`--refresh` was the right flag. A plain `--run` refuses a source already landed;
`--force` would reload regardless. `--refresh` re-fetches and skips the COPY when the
content hash is unchanged.

## USAspending contracts: not a refresh job, a naming problem

The tier-A match was wrong and running the spec would have written the wrong table.

| landing table | rows | covers | in the ledger |
|---|---|---|---|
| FED_USASPENDING_CONTRACTS | 6,325,622 | 2024-10-01 to 2025-09-30 | yes, reads stale |
| FED_USASPENDING_CONTRACTS_FULL | 20,000,000 | FY2007-FY2026 | no |
| FED_USASPENDING_CONTRACTS_FULL_R2 | 93,153,424 | 2006-10-01 to 2026-08-22 | no |

The source the ledger calls stale holds a single fiscal year. The same data, wider and
current to two weeks ago, is already in the warehouse under two other names, and neither
is tracked. Refreshing the 6.3M table would have been work spent on a slice that the
93M table already supersedes.

Its spec is broken separately. The manifest is a frozen list of 20 dated URLs stamped
`20260706`, and USAspending deletes the previous month's archive. Only `20260806` exists
today, so every URL 404s. The listing is an S3 XML index, paginated at 1000 keys, and the
20 files sit between position 302 and 4596, so the existing regex resolver cannot reach
them all in one fetch. Fixing this means paginating the resolver, not editing 20 URLs
that expire again next month.

## What tier A actually taught

Two of the three lessons are about the ledger, not the data:

1. A source id in the ledger is not the same thing as the best table for that data.
   Three contract tables exist; the ledger tracks the smallest and oldest.
2. A frozen list of dated URLs is a refresh that expires. Any spec whose manifest is a
   literal list of dated files will rot on the publisher's schedule, silently, as a 404.
3. `--refresh` exists and is cheap. The path works end to end; CFPB proves it.

---

# The manifest resolver, fixed 2026-09-06

A manifest spec loads many files that share a schema and appends them into one landing
table. The resolver is the step that answers "which files?" before anything downloads.
It took a static list of URLs, a JSON index, or a regex over a listing page.

Both USAspending specs used the static list: 20 URLs each, every one stamped 20260706.
USAspending publishes monthly and deletes the previous archive, so all 40 were 404.

## What changed

`paginate: "s3"` walks a truncated bucket listing via `?marker=`. That listing caps at
1,000 keys; the archive holds 4,597 and the 20 contract files sit between position 302
and 4,596, so a single fetch found some and silently missed the rest. Verified live:
five pages, 4,597 keys, 3.9 seconds.

`latest_re` captures a version stamp and keeps only the newest. That is what makes the
spec self-heal: whichever snapshot is live today is the one it loads.

`expect_files` refuses a short resolve. A publisher caught mid-sweep holds two stamps at
once, and keeping only the new half would load clean while the table quietly lost years.
Both specs declare 20.

The staged path for a zip member was `part_0007.gz`, index only. After a rotation,
`--reuse-staged` would have served last month's part under this month's URL. It now
carries the filename, which carries the stamp.

## Verified

Both specs resolve to 20 live files stamped 20260806, FY2007 through FY2026. HEAD 200 on
every one. 13 offline tests.

## Not run, on purpose

The two loads total about 50 GB compressed, several hundred GB expanded. That total was
measured by the reviewer in one pass over the listing. My own re-check reached 8 of the
40 files, 6.29 GB, before files.usaspending.gov started closing connections — which is
itself worth knowing: forty sequential requests is enough to get cut off, and the load
issues forty fetches. Four reasons to wait:

1. The current stamp is 20260806, last modified 2026-08-10, and the cadence is monthly
   around the 6th to the 10th. Today is the 6th. The resolver snapshots its URL list once
   at the start of a run; if the September sweep lands mid-run, the back half 404s.
2. No prior run of either spec is in the query log, so there is no real number for what
   this costs. A guess is not a price.
3. `fed_usaspending_contracts`, the source the ledger calls stale, is a different table
   from either of these. Loading these does not clear that row.
4. The host rate-limits. Snowflake fetches these server-side, not from here, so the limit
   may not bite the same way, but nothing has tested forty server-side fetches in a row.

Re-run around the 12th, once the September archive has settled.
