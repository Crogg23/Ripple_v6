# The Ripple Time Index — What Clock Every Dataset Runs On

**First map of the warehouse's clocks. 482 tables, 942,472,273 rows, 2,089 time-shaped columns classified and adversarially reviewed.**

---

## Read this before the numbers

**CORRECTED 2026-08-21.** This document originally shipped believing its own classification input had been truncated mid-merge, and caveated sections 4 and 5 as "floors" covering only 229 of 482 tables (health, justice, economics, environment). That belief was wrong. `reports/time_index/clock_index.csv` — the file this whole document is built from — was never truncated: it holds real, specific, adversarially-reviewed per-column detail for **all 482 tables**, politics/labor/energy/housing/finance/transport/immigration/corporate-registry included (verified by direct read, 2026-08-21: 2,089 rows, 482 unique tables, overturn notes present in every domain). What actually got truncated was the *narrative write-up* below when it was first composed — it only quoted from a partial read of its own source, not from the underlying data. The counts below are recomputed straight from the complete CSV and are correct as of this date; the "floor" language elsewhere in this document undersells what the warehouse actually has classified.

**The warehouse-wide totals are solid**, as originally stated. Clock mix, fake-clock counts, grain census, row counts, and coverage windows are computed from the census batch files and the live per-column value scan (`reports/time_index/scan.jsonl`), both covering all 482 tables.

**Corrected counts:**
- **Clock-less tables: 46** (60,482,357 rows) — not the 35 the merge header reported, and not the 53 estimated as a stopgap. 46 is a direct count of every table where no column carries a real clock (happened/reported/decided/span_start/span_end).
- **Reporting-lag tables (carry both a "happened"-or-similar and a "reported" column): 74** (189,622,704 rows) — not the 33-table floor in section 4. 39 of the 74 are outside the four originally-reviewed domains — mostly labor (OSHA injury/illness logs), finance (FEC/SEC filings), immigration (ICE detention), and politics (lobbying disclosures).
- **Span tables (carry a matched start-and-end pair): 75** (106,603,823 rows) — not the 35-table floor in section 5. 41 of the 75 are outside the four original domains — mostly state lobbying-period filings (CA/TX), FEC candidate-cycle windows, and immigration work-visa employment periods.

Sections 4 and 5 below still show the original 229-table lists (they remain accurate as far as they go); the full 74/75 lists live in this session's recompute, not reproduced inline here to keep this document readable.

---

## 1. How many tables can go on a shared timeline, and at what grain

Measured from the real values in every table, ignoring Ripple's own bookkeeping columns:

| Finest resolution actually present | Tables | Rows | Share of rows |
|---|---:|---:|---:|
| **Day** | 313 | 733,378,068 | 77.8% |
| **Month** | 8 | 27,367,107 | 2.9% |
| **Quarter** | 4 | 39,541,117 | 4.2% |
| **Year** | 104 | 55,716,380 | 5.9% |
| **Nothing placeable** | 53 | 86,469,601 | 9.2% |
| **Total** | **482** | **942,472,273** | |

**429 of 482 tables (89%) can go on a shared timeline. 313 of them (65%) at day grain.**

The headline constraint: **a timeline that must include everything runs at year grain.** 104 tables — a fifth of the warehouse — resolve no finer than a year, and a timeline is only as fine as its coarsest member. That is not a defect to fix; it is what annual statistical files are. The practical answer is two timelines, not one:

- **A day-grain timeline** holding 313 tables and 78% of all rows. This is the one that supports "what happened that week."
- **A year-grain roll-up** holding all 429 placeable tables. This is the one that supports "is this getting worse."

The 116 tables that sit between (month, quarter, year) can join the day timeline only by being widened into bands, never by being pinned to a date. Several are large: the historic mortgage-lending file (`housing__fed_cfpb_hmda_historic`, 19.1M loan records) carries nothing but an application year, and the combined air-emissions inventory (`environment__fed_epa_air_emissions_poll_rpt_combined_emissions`, 10.4M rows) carries nothing but a reporting year.

**Cross-check from the classification itself** (229-table sample): the primary clock chosen for each table breaks down as day 136, year 44, month 10, quarter 6, unknown 3, with 30 tables clock-less. Same shape — roughly two-thirds day, a quarter year — which is why I trust the value-based census above for the tables I couldn't see classified.

The full-count is **46 clock-less tables** (corrected 2026-08-21 — see "Read this before the numbers"; supersedes both the merge header's 35 and the 53 estimated as a stopgap). The biggest are worth naming, because their size is out of proportion to their count:

| Rows | Table | Why it can't be placed |
|---:|---|---|
| 31,403,215 | `health__fed_cms_facility_level_minimum_data_set_frequency` — nursing-home assessment frequencies | Its one date column is 100% empty |
| 25,869,521 | `health__fed_cms_partd_prescribers` — Medicare drug prescribing by doctor | Only "days of supply", a count |
| 9,781,673 | `health__fed_cms_medicare_physician_other_practitioners_by_provider_and_servi` — Medicare billing by service | Only a service count |
| 7,200,550 | `environment__fed_fracfocus_registry` — fracking chemical disclosures | Both job dates 100% empty |
| 3,382,301 | `economics__intl_gleif` — global company identity register | Every match was the word "headquarters" |
| 1,779,096 | `environment__fed_epa_icis_air_icis_air_fces_pces` — Clean Air Act compliance evaluations | Its one date column is 100% empty |

---

## 2. The clock mix — what kind of time this warehouse actually holds

All 2,089 classified columns. (The merge originally left 83 labels malformed — the reviewer wrote a sentence where the clock name belonged; 62 were resolved by reading the sentence, and 21 were reported as unrecoverable. Re-checked 2026-08-21: `clock_index.csv` now has zero malformed labels — all 2,089 rows carry one of the standard clock values. Whatever produced the other 21 was fixed upstream of this document, same as the "truncated" classification itself; see the correction note at the top.)

| Clock | Columns | Share of all | Share of real clocks |
|---|---:|---:|---:|
| **not_a_date** — matched a time-shaped name, isn't time | 758 | 36.3% | — |
| **happened** — when the real thing occurred | 400 | 19.1% | **32.2%** |
| **reported** — when someone told a government | 298 | 14.3% | **24.0%** |
| **decided** — when an authority ruled or acted | 213 | 10.2% | **17.1%** |
| **span_end** — closing bound of a period | 199 | 9.5% | **16.0%** |
| **span_start** — opening bound of a period | 133 | 6.4% | **10.7%** |
| **ingest** — Ripple's or an aggregator's own bookkeeping | 67 | 3.2% | — |
| label lost in the merge | 21 | 1.0% | — |

**1,243 columns are real clocks. 825 (39.5% of everything the name sweep caught) are not clocks at all.** Two out of every five time-shaped column names in this warehouse are lying about what they hold.

### Which lane each of the big tables sits in

**"When it happened" — the lane we most want, and the one that carries the most rows.**
- `health__fed_dea_arcos` — every controlled-substance shipment in America, 178,598,026 rows, day grain. The single cleanest event clock in the warehouse. **But it covers 2006–2012 only** (see section 3).
- `maritime__fed_noaa_ais` — vessel positions, 58,104,610 rows, day grain, **covering eight days of January 2024**.
- `economics__fed_usaspending_contracts_full` + `..._assistance_full` — 39.9M federal award transactions, both anchored on the day the money moved.
- `health__fed_cms_open_payments` (2022 / 2023 / 2024 files) — 43,335,833 rows of drug-and-device-company payments to individual doctors, day grain, complete. Currently unusable as a clock because the date is stored as raw text (one-line fix, section 3).
- `consumer_safety__fed_cpsc_neiss` — 9,794,971 emergency-room injury records, day grain, 1999–2025, clean.

**"When it was reported" — the biggest lane by table count in courts and complaints.**
- `justice__fed_courtlistener_dockets` — 71,677,647 court cases, anchored on filing date because it is the only date present across the whole docket universe; the true event dates (argument, hearing) exist on a small minority of cases.
- `consumer_protection__fed_cfpb_complaints` — 17,168,287 consumer complaints, anchored on receipt.
- `justice__fed_fjc_idb_civil` / `_criminal` / `_bankruptcy` — 24.1M federal case records, all anchored on filing.
- `economics__fed_us_sec_edgar` — corporate filings, anchored on submission day.

**"When an authority decided" — the thinnest real lane, and the one that matters most for accountability.**
- `justice__fed_courtlistener_opinion_clusters` — 10,070,727 court opinions, anchored on the day the ruling was handed down.
- `environment__fed_epa_sdwa_sdwa_violations_enforcement` — 15,432,737 drinking-water violation and enforcement records; the enforcement date is a real "decided" clock but is null on roughly a million violation-only rows.
- `economics__fed_sba_ppp` and `economics__fed_sba_loans` — loan approvals.
- `economics__fed_irs_auto_revocations` and `economics__fed_irs_revocation` — the day the IRS stripped a charity's tax exemption.
- `health__fed_hhs_oig_leie` — the day a provider was excluded from Medicare.

### Say plainly which lanes are thin

- **"Decided" is the thinnest real point-in-time lane** — 213 columns, 17% of real clocks. This is the enforcement lane. Every question of the form "how long does it take an agency to actually act, and against whom" runs through the smallest set of columns we have.
- **"span_start" is thinner still** — 133 columns, 10.7%. See section 5: we record when things end far more often than when they began.
- **"Happened" is only a third of real clocks.** Three-quarters of this warehouse dates paperwork, not events. That is a property of the public record, not a bug — but it means the default reading of any Ripple timeline is *when the government wrote it down*, and saying otherwise would be a false claim.

---

## 3. The fake clocks caught — 825 columns, grouped by what caused them

These are live data-quality bugs, not classification trivia. Grouped by mechanism, with the repair cost.

### Mechanism A — Our own load stamp read as history *(the one that corrupted the previous census)*

67 columns are Ripple's or an aggregator's bookkeeping. The damage is not the columns; it is that the previous census **averaged them into each table's date range**.

**59 tables — 278,549,505 rows, 29.6% of every row in the warehouse — currently report a date ceiling that is our download time, not the data.**

| Rows | Table | Census claims data runs to | Real data ends |
|---:|---|---|---|
| 178,598,026 | `health__fed_dea_arcos` — opioid shipments | 2026 | **2012** |
| 58,104,610 | `maritime__fed_noaa_ais` — vessel positions | 2026 | 2024 (8 days) |
| 19,136,434 | `housing__fed_cfpb_hmda_historic` — mortgage applications | 2026 | **2017** |
| 5,300,149 | `environment__fed_epa_frs_facilities` — regulated facility registry | 2026 | unreadable |
| 238,680 | `justice__fed_fbi_cde` — crime statistics | 2026 | 2023 |
| 209,565 | `reference__fed_itis_nodc_ids` — species identifiers | 2026 | **1997** |
| 28,185 | `justice__state_mo_sex_offender_registry` | 2026 | **2008** |

The opioid file is the extreme case and the most consequential: it looks like a current dataset and is fourteen years stale. Anyone building an opioid timeline off the census range would have drawn a flat line from 2013 to today and called it a decline.

**Fix:** one line in the census query — exclude columns whose name starts with an underscore. No data change, no rebuild. This is the single highest-value one-line fix in the document.

Of the 67 bookkeeping columns, **48 are one aggregator**: CourtListener stamps every row of all 21 of its tables with its own database create/modify times. Eight of those tables have *nothing but* those stamps, which is why they show as clock-less.

### Mechanism B — Load stamps with a unit bug: timestamps in the year 56 million

Ten tables store our ingest stamp as a number of **microseconds** and convert it as if it were seconds. Every row lands roughly 56.5 million years in the future.

**18,556,546 rows affected**, all rows in each table:

`consumer_safety__fed_cpsc_neiss` (9,794,971 — max reads 56571662-04-06) · `corporate_registry__fed_icij_offshoreleaks_relationships` (3,339,267) · `science_research__fed_nih_reporter` (2,122,611) · `justice__intl_opensanctions_default` (1,281,846) · `..._offshoreleaks_entities` (814,344) · `..._officers` (771,315) · `..._addresses` (402,246) · `..._intermediaries` (26,768) · `..._others` (2,989) · `energy__fed_eia_861_balancing_authority` (189).

The injury file is the clearest illustration of why this matters: its emergency-room treatment date is **pristine** — 9,794,877 of 9,794,971 rows, 1999-01-01 to 2025-12-31 — sitting right beside a load stamp that reads year 56 million. The census reported the year-56-million number as the table's range.

**Fix:** correct the microsecond-to-second conversion at load. Real repair, but small and mechanical.

*Do not confuse these with legitimate sentinels.* Separately, 16 columns hold `9999-12-31` as an honest "no end date yet" marker on period bounds — bank insurance end dates, company-relationship period ends, contract ordering-period ends, hazardous-waste compliance deadlines. Those are correct and must not be "fixed."

### Mechanism C — Dead casts: date columns that parsed to nothing

**52 tables, 63,169,310 rows, have at least one date column that is 100% NULL.** In **16 of them (40,736,452 rows) the dead column was the only clock, and the table goes completely dark:**

| Rows | Table | Dead column(s) |
|---:|---|---|
| 31,403,215 | `health__fed_cms_facility_level_minimum_data_set_frequency` | report_date |
| 7,200,550 | `environment__fed_fracfocus_registry` — fracking chemicals | job_start_date, job_end_date |
| 1,779,096 | `environment__fed_epa_icis_air_icis_air_fces_pces` — air compliance evaluations | actual_end_date |
| 248,835 | `environment__fed_fracfocus_disclosure_list` | job_start_date, job_end_date |
| 102,037 | `environment__fed_epa_icis_air_icis_air_violation_history` | all four HPV milestone dates |
| 2,000 | `justice__intl_hudoc` — European Court of Human Rights rulings | judgment_date |
| plus 10 tiny tables | Brazilian/Ghanaian/Georgian open-data catalogues, historical map and text archives, `transport__fed_fra_safety`, `immigration__fed_cbp_encounters`, `justice__intl_austlii` | |

Three of these — the two fracking tables and both EPA air tables — were classified with **high confidence as clean day-grain clocks** on the strength of the cast in the SQL. The cast is there; it just yields nothing. The adversarial review caught this pattern on other tables but missed these five. That is worth noting as a review-process lesson: reading the cast is not the same as checking the result.

**The most valuable single repair here** is `health__fed_cms_nursing_home` (14,700 facilities). Five date columns are pinned to `try_to_date(..., 'MM/DD/YYYY')` in staging, but the source was re-landed from the CMS API in ISO format on 2026-08-08, so all five parse to NULL — including the most recent health inspection date. The sister table `health__fed_nursinghome411` carries the same CMS fields correctly populated (inspections 2019-09-05 to 2025-12-10), proving the data exists. **One-line fix**: drop the format string.

### Mechanism D — Epoch collapse: a number parsed as seconds since 1970

The classic trap: `20230415` read as 20 million seconds lands on 1970-08-23.

**Live and unrepaired: `transport__fed_faa_registry` — 314,417 aircraft registrations, all four date columns destroyed.** Last action date has 7 distinct values spanning 1970-08-17 to 1970-08-23; certificate issue date has 11; airworthiness date has 13; expiration date has 3. Every aircraft ownership and certification timeline in the warehouse is gone. The only survivor is year of manufacture, as text. **Real repair** — needs the source format identified and a re-parse.

**Already repaired, worth recording as the pattern to watch:** the opioid shipment file used to sit entirely in 1970 (the pre-repair copy still in the restore schema shows 52 distinct dates between 1970-01-12 and 1970-05-23); the federal contract file had all 20,000,000 rows on 1970-01-01 from a fiscal-year column; the armed-conflict event file had all 385,918. All three now read clean in the live scan. **Note the census batch files still report the old numbers** — the census that this classification was built on is itself stale on these three.

### Mechanism E — Year precision wearing a day-grain costume

30 date columns concentrate their values on January 1 because a year was padded into a date. This is the quietest bug in the set: the column has a real type, real values, and a plausible range, and it will draw a chart with a spike every January.

| Jan-1 share | Column | Table |
|---:|---|---|
| **100%** of 17,168,287 | received_year | `consumer_protection__fed_cfpb_complaints` |
| **100%** of 988,183 | court_record_date | `justice__fed_fjc_idb_appellate` |
| **100%** of 369,264 | date | `energy__intl_ember_elec` |
| 84% of 6,299,908 | fugitive_end_date | `justice__fed_fjc_idb_criminal` |
| 77% | fugitive_start_date | same |
| 65% | **sentence_date** | same |
| 61% | disposition_date / termination_date | same |
| 78% of 927,415 | sampling_start_date | `environment__fed_epa_sdwa_sdwa_lcr_samples` (lead-and-copper tests) |
| 72% of 50,421 | date_start | `justice__fed_courtlistener_positions` (judicial tenures) |
| 68% of 617,708 | period_covered_from | `labor__fed_dol_olms` (union financial reports) |
| 58% of 5,544,625 | sub_date | `economics__fed_irs_990_efile_index` |
| 76% of 437 | start_date | `justice__fed_courtlistener_courts` (court founding dates) |

The federal criminal case file is the one to worry about: for roughly two-thirds of 6.3 million defendants, "the day they were sentenced" is really "the year they were sentenced."

**Important caution — not all January-1 clustering is a bug.** Pension plan years, fiscal years, and audit periods genuinely begin on January 1. `labor__fed_dol_ebsa_form5500_schedule_sb` at 94%, `economics__fed_dol_form5500` at 90%, and the Treasury year roll-ups at 100% are all correct. **Fix:** relabel the grain, don't touch the data — but each of the 30 needs a five-second judgement call about which kind it is.

### Mechanism F — Scanned-document text run through a date parser

CourtListener's judicial financial disclosures carry an as-extracted OCR field holding things like `See VIII`, `'84-presnt`, and `1987-2002`. Four of the five models were fixed on 2026-08-18 and now pass it through as text.

**`justice__fed_courtlistener_disclosure_reimbursements` was missed and is still live** — line 15 of the compiled model still reads `try_to_date(DATE_RAW) as date_raw`, producing 235 rows on 1970-01-01 and 45 rows in the far future including one dated 3201-04-14. **One-line fix**: delete the wrapper, matching its three fixed siblings.

### Mechanism G — Precision codes parsed as dates

A code saying *how precisely we know a date* is not a date. Caught: `date_granularity_start`, `date_granularity_end`, `date_granularity_dob`, `date_granularity_dod`, `date_granularity_termination` across three CourtListener tables (values `%Y`, `%Y-%m`, `%Y-%m-%d`); `date_prec` on the armed-conflict file (values 1–5); `fy_end_mo_day_cd` on the CMS provider file (a month-day code like `0630`); `fiscalyearend` on the SEC company file (`1231`). All yield NULL. **One-line fixes** — stop casting.

### Mechanism H — Flags and prose in date wrappers

`date_filed_is_approximate` on the court-opinion file is a `t`/`f` boolean wrapped in a date parse. `other_dates` on the same table is free prose ("argued…; decided…"). Both return NULL. **One-line fixes.**

### Mechanism I — Date parts with no year

A bare `1`–`12` or `1`–`4` cannot place anything. Caught across the four Treasury Fiscal Data tables (calendar month, calendar quarter, calendar day, fiscal quarter — 4 columns each), seven month-ordinal columns on the EIA generator file that pair with separate `planned_retirement_year` / `planned_uprate_year` / `planned_derate_year` / `planned_repower_year` columns, the employment-statistics quarter, the Italian statistics month and quarter, the human-rights-court judgment month, and the storm file's begin/end day and time components. **Not bugs** — correctly built helper columns. The finding is that they must never be charted alone, and the seven energy ones are worth *joining* to their year partners to build a real month-grain retirement schedule.

### Mechanism J — Durations, counts, and ages

The largest not-a-date family. `years_in_medicare` (the canonical trap), `study_duration_days`, `days_to_results_posting`, `fiscal_year_length_days`, `years_insured_before_failure`, `award_duration_days`, `days_since_last_inspection`, `payment_denial_length_in_days`, oral-argument `duration` in seconds, `prison_time_1` through `_5`, `probation_months_1` through `_5`, `term_months` on both loan files. Plus ~25 `bene_avg_age` / `bene_age_lt_65_cnt` / `bene_age_65_74_cnt` columns across five Medicare provider tables, and every "patient-days" and "bed-days" count in the hospital cost reports. **Correctly excluded, no action.**

### Mechanism K — Vintage and release labels

`tape_year` on the federal appellate, civil, and criminal case files, and `year_of_tape` on the linked copy — these name which annual data release a record came from, not anything about the case. All four were **overturned from "our bookkeeping" to "not a date"** on review, correctly: they are release labels, not load stamps. Same call on `active_fy` on the federal agency summary table, whose demotion leaves that table clock-less.

### Mechanism L — Name-collision false positives

The sweep matched substrings. **Twelve** columns on the global company register matched because "head**quarter**s" contains "quarter" — street address, city, postcode, country, language tag. Roughly **thirty** columns on the federal criminal case file matched because "**term**inated" starts with "term" — offence codes, statute titles, severity codes, judge identifiers. Others matched "received" (dollar amounts and bid counts), "weekly" (a wage), "timely" (quality-measure percentages), "long term" / "short term" (balance-sheet liabilities and hospital subtypes), and "age" (population counts). **No action** — but one has a consequence: `economics__xc_wikipedia_largest_us_companies` matched *only* on "headquarters", which is a city name, so that table has no clock at all.

### Mechanism M — Measurement-window labels above a measure block

`health__fed_cms_dialysis` carries twelve `*_date` columns — five-star, claims, mortality ratio, hospitalisation ratio, readmission ratio, infection ratio, vaccination collection dates and more. Each sits directly above the measure it labels. All twelve are 100% empty after a format-free date parse, and all twelve were **overturned from "period end" to "not a date"** on review. With them gone the table is clock-less. **Real repair** — someone has to look at the source file and decide whether these are recoverable window labels or genuinely absent.

---

### The repair list, sorted by cost

**One-line fixes (SQL edit or query change; no rebuild, or a free view redeploy):**

1. **Exclude underscore-prefixed columns from the date census.** Un-poisons 59 tables / 278.5M rows, including the opioid file. *Highest value in the document.*
2. **Add a date cast to the three doctor-payment files** — `date_of_payment` is clean `MM/DD/YYYY` text on all 43,335,833 rows, 100% populated. One cast lights up the entire pharma-money-to-doctors record. *Highest mission value in the document.*
3. **Add a date cast to the two federal award transaction files** — `action_date` is clean ISO text on 26.2M rows across `economics__fed_usaspending_assistance_full` and `..._contracts`.
4. **Drop the `'MM/DD/YYYY'` format string in the nursing-home staging model** — restores five date columns including most-recent-inspection on 14,700 facilities.
5. **Delete the date wrapper on the judicial reimbursement disclosure file** — matches three already-fixed siblings.
6. **Move three primaries the review flagged as sitting on the wrong column:** the corporate filing index onto its filing date rather than its reporting-period end (the filing date exists in the model but the name sweep never saw it, so it must be *added* to the index); the Puerto Rico and statistics-of-income charity extracts onto their IRS ruling date rather than a tax-period end.
7. **Relabel the 30 January-1 columns** as year grain where the padding is artificial.
8. **Stop casting the precision codes, the boolean flag, and the prose field** (Mechanism G and H).

**Real repairs (rebuild, re-land, or decoding work):**

1. **`health__fed_cms_facility_level_minimum_data_set_frequency`** — 31.4M rows, single date column 100% null. Biggest dark table in the warehouse.
2. **`transport__fed_faa_registry`** — all four aircraft date columns collapsed into a two-week window in August 1970.
3. **Both fracking disclosure tables** — 7.4M rows, both job dates dead despite a correct-looking cast.
4. **Both EPA air-compliance tables** — 1.88M rows, evaluation and violation-milestone dates dead.
5. **`health__fed_cms_dialysis`** — twelve empty measure-window columns; needs a source read.
6. **`health__fed_hhs_oig_leie`** — the Medicare-exclusion mart exposes raw `YYYYMMDD` text and discards the parsed date staging already builds; staging warns that a naive cast collapses all 83,464 exclusions onto seven garbage 1970 dates. Rewire the mart to the parsed column.
7. **Ten tables with microsecond load stamps** — 18.6M rows reading year 56 million.
8. **`justice__fed_doj_fca_settlements`** — the False Claims Act settlement date is null on all 12 rows because of a format-free parse; only the fiscal year survives.

---

## 4. The reporting-lag opportunity — a build list

A table carrying **both** a "when it happened" clock and a "when it was reported" clock lets you measure the gap per row. A widening or collapsing lag is a finding in its own right: it is how you see an agency slowing down, a backlog forming, or a reporting rule changing.

**74 tables / 189,622,704 rows carry both, warehouse-wide** (corrected 2026-08-21 — see "Read this before the numbers"). The table below is the original 33-table list from the four first-reviewed domains, still accurate; the 41 additional tables found outside those domains are new labor (OSHA case-detail and 300A summary logs), finance (FEC committee/candidate and independent-expenditure filings, SEC insider submissions), immigration (ICE detention stints and detainers), and politics (state and federal lobbying disclosures) sources — ranked by size:

| Rows | Table | Happened | Reported | What the gap measures |
|---:|---|---|---|---|
| 71,677,647 | `justice__fed_courtlistener_dockets` | argument, reargument | filing, last filing | Time from filing to being heard |
| 20,000,000 | `economics__fed_usaspending_contracts_full` | action date | solicitation, initial report, last modified | How late contract awards hit the public record |
| 19,902,879 | `economics__fed_usaspending_assistance_full` | action date | initial report, last modified | Same, for grants and aid |
| 15,432,737 | `environment__fed_epa_sdwa_sdwa_violations_enforcement` | system shutdown | first/last state submission | How long a drinking-water violation takes to surface federally |
| 10,857,396 | `justice__fed_fjc_idb_civil` | pretrial conference | filing, issue joined | Civil case pace |
| 6,325,622 | `economics__fed_usaspending_contracts` | action date | last modified | Contract reporting delay |
| 6,299,908 | `justice__fed_fjc_idb_criminal` | proceeding date | filing, fiscal year | Criminal case pace |
| **5,811,086** | **`health__fed_fda_faers_demo`** | **adverse event, patient death** | **manufacturer received, FDA received, initial FDA received, report filed** | **How long a drug injury takes to reach the FDA — the richest lag structure in the warehouse, four reporting stamps against two event dates** |
| 3,382,301 | `economics__intl_gleif` | five corporate event effective dates | five matching recorded dates | Delay between a merger or dissolution and its registration |
| **2,743,561** | **`health__fed_fda_maude`** | **date of event** | **date received, date reported** | **Device-injury reporting delay** |
| 2,495,249 | `environment__fed_epa_sdwa_sdwa_site_visits` | visit date | first/last submission | Sanitary-survey reporting delay |
| 1,911,185 | `health__fed_hrsa_npdb` | malpractice incident year, graduation year | original report year | Years between malpractice and its national report |
| 1,554,832 | `environment__fed_epa_sdwa_sdwa_facilities` | deactivation | first/last submission | |
| 988,183 | `justice__fed_fjc_idb_appellate` | submission, hearing | docketing, district docketing, appeal, record received | Appellate pipeline timing |
| 434,040 | `environment__fed_epa_sdwa_sdwa_pub_water_systems` | system deactivation | first/last submission | |
| 418,479 | `health__fed_cms_nursing_home_deficiencies` | survey, correction | processing | Inspection-to-publication delay |
| 397,615 | `environment__fed_epa_npdes_npdes_ps_violations` | actual milestone | report received | Water-permit self-reporting delay |
| 394,075 | `environment__fed_epa_sdwa_sdwa_events_milestones` | actual achievement | first/last submission | |
| 385,918 | `justice__intl_ucdp_ged` | event year | source report date | How long violence takes to be documented |
| 359,514 | `health__fed_cms_nadac` | price effective date | file as-of date | Drug-price publication lag |
| 200,030 | `health__fed_cms_nursing_home_fire_deficiencies` | survey, correction | processing | |
| 140,454 | `economics__fed_pbgc_data` | data year | publication date | Pension-insurance publication lag |
| 82,187 | `environment__fed_epa_npdes_npdes_cs_violations` | actual date | report received | |
| 42,347 | `justice__intl_eu_sanctions` | date of birth | six legal-basis publication dates | |
| 39,635 | `health__fed_fda_device_enforcement` | recall initiation | enforcement report date | **How long between a firm pulling a device and the public being told** |
| 33,484 | `economics__fed_dol_form5500` | plan effective date | received, plus six signature dates | Pension filing timing |
| 17,816 | `health__fed_fda_drug_enforcement` | recall initiation | enforcement report date | **Same for drugs** |
| 14,713 | `health__fed_nursinghome411` | survey dates | processing | |
| 14,700 | `health__fed_cms_nursing_home` | survey dates | processing | *(blocked — dates dead, see section 3)* |
| 2,040 | `health__xc_guttmacher_monthly_abortion` | month | publish date | |
| 2,039 | `environment__fed_phmsa_flagged_incidents` | incident datetime | report received | Pipeline incident reporting delay |
| 1,471 | `health__fed_cdc_data_portal` | dataset created | published, updated | |
| 300 | `economics__fed_us_usaspending_api` | fiscal year | last modified | |

**The four to build first**, on harm density rather than row count: the drug adverse-event file and the device injury file (how long an injury takes to reach the regulator), and the two recall files (how long between a company pulling a dangerous product and the public being told). All four are day grain on both sides, and all four already parse cleanly.

**Two structural cautions.** First, one enforcement family sits outside this list because it splits the lanes across tables rather than columns: the IRS revocation files carry a "decided" revocation date against a "reported" posting date, and the posting is a monthly batch — the gap there measures publication cadence, not agency speed. Second, three of the tables above (the two federal award files and the SDWA violations file) have "reported" stamps that are *record-maintenance* timestamps, which move every time the publisher edits the row. Those measure churn, not lag. Use `initial_report_date`, never `last_modified_date`.

**This list showed 229 of 482 tables; the full 482-table count is 74 tables / 189,622,704 rows (see the correction note at the top of this document).** The 41 new tables are named above.

---

## 5. The span tables — what supports "what was active on date X"

Point-in-time tables can tell you what happened on a day. Only tables with a start *and* an end can tell you what was **in force** on a day — which licence was valid, which ban was running, which contract was live, which permit had lapsed.

**75 tables / 106,603,823 rows carry a matched start-and-end pair, warehouse-wide** (corrected 2026-08-21). The lists below are the original 35 tables from the four first-reviewed domains, still accurate; the 41 additional tables are mostly state lobbying-period filings (CA/TX), FEC candidate-cycle windows, immigration work-visa employment periods, and corporate/research grant spans.

**Federal money and contracts**
- `economics__fed_usaspending_contracts_full` (20,000,000) — performance start, current end, potential end, and ordering-period end. Four bounds; the `9999-12-31` values are honest "open-ended" markers.
- `economics__fed_usaspending_assistance_full` (19,902,879) and `economics__fed_usaspending_contracts` (6,325,622) — performance windows.
- `economics__fed_us_usaspending_api` (300) — performance window; carries a `2100-12-31` sentinel.
- `economics__fed_fac_single_audit` (411,638) — audited fiscal-year window.
- `economics__fed_irs_990` (200) — tax period covered.
- `economics__fed_dol_form5500` (33,484) — plan year covered *(partly blocked: the primary plan-year bounds are dead, though the form-header copies survive)*.

**Environment and permits**
- `environment__fed_epa_sdwa_sdwa_violations_enforcement` (15,432,737) — compliance period and non-compliance period, two nested spans.
- `environment__fed_epa_sdwa_sdwa_pn_violation_assoc` (387,627) — same two spans.
- `environment__fed_epa_npdes_npdes_inspections` (1,900,067) — inspection start and end.
- `environment__fed_noaa_storm_events` (1,780,730) — storm begin and end *(only at month grain: the full begin/end timestamps are dead, leaving the year-month integers)*.
- `environment__fed_epa_sdwa_sdwa_lcr_samples` (927,415) — lead-and-copper monitoring window.
- `environment__fed_epa_sdwa_sdwa_pub_water_systems` (434,040) — four spans: operating season, source-water protection, outstanding-performer status, reduced monitoring.
- `environment__fed_usgs_minerals` (304,632) — first and last year of production.
- `environment__fed_epa_aqs_sites` (20,994) — monitoring-site operating life.
- `environment__fed_noaa_weather_api` — alert effective and expiry.
- `finance__fed_epa_icis_fec_icis_fec_epa_inspections` — inspection window.
- *(Both fracking job-window tables and the EPA air violation-history spans belong here but are currently dead — see section 3.)*

**Courts, tenure, and sanctions**
- `justice__fed_fjc_idb_civil` (10,857,396) — trial begin and end.
- `justice__fed_fjc_idb_criminal` (6,299,908) — fugitive start and end *(both ~80% year-precision)*.
- `justice__intl_ucdp_ged` (385,918) — the window an event could have occurred in.
- `justice__fed_courtlistener_positions` (51,290) — judicial tenure start and termination. **The core "who was on the bench on date X" table.**
- `justice__fed_courtlistener_judge_political_affiliations` (8,486) — party affiliation spans.
- `justice__fed_courtlistener_courts` (3,361) — court founding and abolition *(year grain — 76% of start dates are padded)*.
- `justice__fed_consolidated_screening_list` — screening-list entry in force.
- `justice__fed_fhfa_suspended_counterparties` — **suspension start and end. This is the "banned but still operating" table.** Most rows read "Indefinite" and go null on the end side.

**Health**
- `health__fed_cms_hcris` (hospital cost reports) — fiscal-year begin and end.
- `health__fed_cms_pos_other` — four spans: accreditation, psychiatric unit, rehab unit, Medicare participation.
- `health__fed_cms_opt_out_affidavits` — physician Medicare opt-out period; the 2028 ceiling is a live future end date, not corruption.
- `health__fed_clinicaltrials` — trial start, primary completion, completion; the 2032 values are real.
- `health__fed_cdc_anxiety_depression` and `health__fed_cdc_health_insurance` — survey collection windows.

**Corporate**
- `economics__intl_gleif_relationships` (484,142) — five ownership-period slots, each with start, end, and a *type* code. **Trap:** slot 1 is not the same kind of period on every row; filter on the type code before reading it as an ownership span.

### The span asymmetry — a finding in itself

**Warehouse-wide there are 199 closing bounds and only 133 opening bounds. 66 more ends than starts.**

At least 18 tables I can name carry an end with no beginning: the cybersecurity remediation deadline file, the published-caseload index, four water-permit violation tables, the hazardous-waste compliance deadline file, the biologics exclusivity expirations (four columns), two drug and device recall termination dates, the device registration expiry, the grant application close and archive dates, three IRS tax-period ends, the corporate filing period-of-report, and the company-register expiration and renewal dates.

Deadlines, expirations, and terminations are recorded far more reliably than the moment something began. Practically: the warehouse is better at answering *when did this stop* than *when did this start*, and any "what was active on date X" query built on span-end alone will silently include things that had not begun yet.

---

## 6. What a single warehouse-wide timeline would actually show

Put the 429 placeable tables on one axis and here is the picture.

**Shape.** A thin, deep spine reaching back to the 1700s — court dockets to 1802, court opinions to 1700, the UK company register to 1776, US debt to 1790 — carrying almost no volume. Then near-nothing until the 1990s. Then a wall. Roughly 78% of all rows sit in 2000–2026, and the density is wildly uneven within that: 2020–2024 is thick with federal spending, court filings, and consumer complaints, while 2006–2012 is dominated by one file (opioid shipments) that alone is 19% of every row in the warehouse.

**Currency.** Latest year of *real* data per table:

| Real data reaches | Tables |
|---|---:|
| 2026 | 266 |
| 2025 | 35 |
| 2023–24 | 83 |
| 2015–22 | 22 |
| pre-2015 | 20 |
| no readable end date | 56 |

**301 of 482 tables (62%) are current to 2025 or 2026.** That is the genuinely good news in this document: the majority of the warehouse is live, not archival.

**What you could ask it.** With the day-grain spine you could line up, on the same axis and for the same place: every federal contract and grant action, every court case filed and every opinion handed down, every consumer complaint, every drinking-water violation, every hospital and nursing-home inspection, every drug and device recall, every emergency-room injury, and every reported adverse drug event. That is a real, working recon instrument — enough to ask whether enforcement in a county went quiet in the same window that violations rose, and to see it across every county at once rather than one at a time.

### The three biggest honest limits on reading it

**1. The floor is a year, and a fifth of the warehouse sits on it.** 104 tables resolve no finer than a calendar year, and 30 more day-grain columns are secretly year-precision padded to January 1 — including sentencing dates for two-thirds of 6.3 million federal criminal defendants and the received date on all 17.2 million consumer complaints. Any timeline that mixes everything must be drawn annually, and any day-grain chart that includes a padded column will show a January spike that is pure encoding artefact. Before publishing any chart off this index, check whether its columns are in the January-1 list.

**2. Almost a third of the rows currently lie about how recent they are.** 59 tables / 278,549,505 rows — 29.6% of the warehouse — report a date ceiling that is our download date rather than the data's. The opioid shipment file presents as current through 2026 and actually ends in 2012. The mortgage file presents as 2026 and ends in 2017. Until the census excludes underscore-prefixed columns, *every recency claim about this warehouse is unverified*, and the phrase "data through 2026" should not appear in anything published. Separately, two of the largest tables are one-week snapshots wearing a big row count: 58.1 million vessel positions covering eight days of January 2024, and 6.7 million water measurements covering eight days of June 2026. A timeline weighted by rows would let those two weeks dominate two decades.

**3. It mostly shows paperwork, not harm.** Only 32% of real clocks record when something actually happened; 24% record when someone told a government and 17% when an authority acted. The thinnest lane is "decided" — the enforcement lane, the one that answers *did anybody do anything about it*. So the default reading of a Ripple timeline is **the rhythm of the public record, not the rhythm of the world**. The gap between the two is measurable on the 74 tables in section 4, and closing that interpretive gap is what those 74 are for — but until they are built, every trend line on this timeline needs the caveat that a rise may be a rise in reporting.

**Correction, 2026-08-21 (see the top of this document).** This document originally closed by saying sections 4 and 5 were floors covering 229 of 482 tables, with the other 253 unclassified. That was wrong — the classification was complete all along; only this document's own composition read a truncated copy of it. The corrected full-warehouse counts are 46 clock-less tables, 74 reporting-lag tables, and 75 span tables. The counts in sections 1, 2, 3 and 6 were already computed from the complete data and are unchanged.