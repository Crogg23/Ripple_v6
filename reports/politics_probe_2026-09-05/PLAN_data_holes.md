# Plan v2: close the data holes behind the politics probes

2026-09-05. v1 came from five research passes. v2 folds in two fresh-context reviews: a fact skeptic, 14 of 14 claims verified, and a sequence reviewer who read the loader machinery, the gate hook, the heartbeat, and the dbt project. Nothing has run. Every load gets a price line and a "go".

## What the reviews changed

| v1 said | v2 says |
|---|---|
| 7 days | 10-12 working days solo; 7 only if the scrapers are cut |
| Phase 0 is 7 items | 13 items; four hidden dependencies surfaced, plus measured coverage |
| gates: rebuild | rebuild, spine, spend; the hook never sees a Python SWAP, so the price-and-go rule is ours |
| resurrect the bills loader from the drawer | CLAUDE.md forbids building from the drawer; this is a fork for Chris |
| FEC donors run in one 4-hour shot | per-cycle staging with resume; a blip no longer restarts at zero |
| LDA gap is 2011-19 | 2022-26 is also empty; ~450k more filings; keyed it is still under 2 hours total |
| HCRIS is a spec change | the only HCRIS-aware loader skips it; it is a loader write, moved to Phase 0 |
| no rollback | keep the old live table as __PREV until the skeptic passes |

## Three forks for Chris before day 1

1. Bills loader: the only code lives in the junk drawer. A: rewrite from scratch, 1 day. B: copy it out with a LEDGER row and treat it as new code. C: skip 113-117, hunch 91 stays dead. I'd take B because the parser is 200 lines of tested XML handling.
2. Heartbeat: it reslices every changed spine table unattended, on the budget, with no price line. A: turn the LINK tier off for the run. B: leave it and accept the spend. I'd take A.
3. Scrapers: 4-6 days of the calendar. A: do them. B: timebox to 2 days, Senate only. C: defer. I'd take B; Senate is the one nobody's dataset covers.

## Phase 0, 2-2.5 days, code only, no gate
0.1 Port `congress_committee_membership_load.py` and `fec_independent_expenditure_load.py` off `build_skeleton` onto loadkit staging-and-swap. Both fail on import today.
0.2 Bills loader per fork 1. Add `--congresses`. Drop its mart DDL.
0.3 `pip3 install pyshp` into the connector python.
0.4 `senate_lda_load.py`: BASE_URL to lda.gov; `--end-year`; `--filings-only`; land years to `__STAGING` then one INSERT SELECT, never straight into live; refuse a year already present; key in library-onboarding/.env; prove the key with one page_size=250 call.
0.5 `federal_register_backfill.py`: `__STAGING` then SWAP; decide `_INGESTED_AT` NUMBER vs TIMESTAMP_NTZ; regenerate the landing_clean view if it flips.
0.6 `irs527_load.py`: record types A and B; chunked staging-and-swap instead of all-in-RAM pandas; `IS_AMENDED` via join to 8872 AMENDED_REPORT_IND; count the extracted 2.9 GB file toward disk.
0.7 `fec_itcont_load.py`: CYCLES 2000-2026; CYCLE_FILE column; per-cycle staging with `--resume-from-cycle`, using loadkit/checkpoint.py; delete each zip after streaming; compare cached zip size to Content-Length; `require_clean` threshold per cycle with the quarantine rate logged; per-cycle blank SUB_ID and blank ENTITY_TP counts; wire loadkit.preflight pat_check and budget_check; `--max-rows` smoke.
0.8 Fix the FEC audit-column mismatch: loader writes `_INGESTED_AT`, staging model reads `INGESTED_AT`. Check the live column via information_schema first; fix the model in the same commit. Port bridge_fuel's schema-vs-live check into itcont.
0.9 `census_boundaries_load.py`: it does `create or replace` per entry, writes no INGEST_RUNS row, stamps no sha. Rewrite as staging-and-swap over a union of cd118 and cd119 with CDSESSN, plus an INGEST_RUNS row. `create or replace` is a destroy word.
0.10 HCRIS loader: bridge_fuel spec of 13 CSVs plus a per-file SOURCE_FILE_YEAR stamped before concat; column names must reproduce landing's `FTE___EMPLOYEES_ON_PAYROLL` style or the pre-swap schema check refuses.
0.11 `loadkit/atomic_load.py`: add `keep_previous`, rename old live to `<TABLE>__PREV_<date>` instead of drop; state Time Travel retention on LIBRARY_RAW.LANDING as the fallback.
0.12 `loadkit/preflight.py`: disk check, free space ≥ 2x the largest zip. 45 GB free today vs 22 needed.
0.13 Measured coverage. `scripts/coverage_probe.py` plus `tests/test_coverage_probe.py`, 28 tests. Fork A taken 2026-09-06: it sits on `build_freshness_ledger.py`'s date parser rather than a second copy. That parser was split into `recency_inner`, the expression, and `recency_expr`, the MAX wrapper; that split alone was behaviour-preserving. 0.14 then changed the ledger on purpose.
Why: two of the six dead probes, 91 and 83, died on time windows that never overlapped, and both were found only by writing the join and getting zero rows. The other four died on keys, on a column-shift and on a mechanism; measured coverage does not touch those. SOURCE_REGISTRY already carries TEMPORAL_COVERAGE, but `library-onboarding/register.py` fills it from a hand-typed config value at register time. Nothing measures it, nothing rechecks it after a load, so it is a claim and not a fact.
Shape: one row per source per data year, with that year's row count, appended to LIBRARY_META.REGISTRY.SOURCE_COVERAGE_YEARS with a MEASURED_AT stamp. Readers take the newest run per source. A year histogram, not a min and a max, because min and max cannot see a hole in the middle, and the lobby table is exactly that case. Sentinel years are bucketed to NULL and counted separately, so CA_LOBBY_COVER's year-5005 rows and FEC indiv's strays to 3312 cannot make a table look like it overlaps everything.
Sources: the 102 in `scripts/freshness_mapping.json`, plus `--table` and `--col` for anything unmapped. The politics probe tables are all unmapped, so that flag is not optional.
`--verify` compile-checks every source with LIMIT 0, scanning nothing. Run 2026-09-06: 80 of 102 compile. 20 have no usable date column in the mapping. Two are wrong and would have failed only mid-scan: `fed_cfpb_complaints` maps DATE_RECEIVED while the live column is `Date received`, with a space, which the shared `col_ref` rejects as prose; `fed_fda_drug_enforcement` maps REPORT_DATE while the table holds a single VARIANT `RAW`, so it needs a `RAW:report_date` path.
Fixed 2026-09-06 on Chris's go. See 0.14.
Modes: no flag prints the SQL; `--verify` compile-checks; `--run` scans and prints; `--write` scans and records. A run that produces nothing for any source exits 1, so a half-failed sweep cannot read as clean. The create runs before any scanning, and each source is saved as it finishes, so a failure at source 90 of 102 keeps the first 89.
Measured live 2026-09-06, read-only, four tables:

| landing table | measured | reads on | unparsed |
|---|---|---|---|
| FED_SENATE_STOCK_WATCHER | 2012-2020, no gaps | TRANSACTION_DATE | 0% |
| FED_GOVINFO_BILLSTATUS | 2023-2026, no gaps | INTRODUCED_DATE | 0% |
| FED_SENATE_LDA_FILINGS | 1999-2021, 9 missing | FILING_YEAR | 0% |
| FED_FEDERAL_REGISTER_DOCUMENTS | 2023-2026, no gaps | PUBLICATION_DATE | 0% |

Read from LANDING, not the marts the dead probes queried. The lobby mart holds 819,649 rows against landing's 831,376, and the same 14 years and the same span, so the answer does not move. Every scan now reports its unparsed share, so a table whose dates mostly fail cannot print "no gaps" unchallenged.

Trades against bills is the hunch 91 death, visible in two scans instead of a join. The lobby table's 9 missing years are the 2011-2019 hole, which a min and max pair would have hidden inside a 1999-2021 span.
Recorded 2026-09-06 on Chris's go, then re-run once after the third skeptic pass to store the unparsed counts. Newest run per source now holds 2,406 rows across 80 source ids. That is 79 physical tables: the federal register was measured twice, once by its mapped id and once by its fully qualified name, and the two agree exactly. Priced beforehand at p50 $0.00 and max $0.08 per statement on X-Small. Actual, from the query log: 173 scans, 65.4 seconds, 6.2 GB, about 0.007 credits.

Overlap run end to end on the two dead pairs:

| pair | answer |
|---|---|
| senate trades vs bills | NO OVERLAP, hunch 91 reproduced |
| lobby filings vs federal register | NO OVERLAP, hunch 83 reproduced |
| house PTR index vs bills | shared 2023-2026 |

The third line is a lead, not a rescue. The House index overlaps the bills years, but `.claude/traps.md` records that it carries no ticker, asset or amount, and hunch 35 says the same. A House version of 91 still needs the PDF trade lines from 4.2. The shared-year row counts are the whole index; periodic transaction reports alone run about 469 in 2023 and 375 in 2026.

27 of 102 stored nothing on the first sweep. After 0.14 that is 22. The remaining gap is 20 sources with no usable date column, plus two with no per-row date that exists to find.

Interior holes found, none of which a min and max pair would show:

| source | span | missing | unparsed |
|---|---|---|---|
| fed_epa_echo | 1908-2026 | 62 | 82.1% |
| fed_cdc_suicide_rates | 1950-2018 | 27 | 0% |
| xc_nagix_dprk_missile_tests | 1984-2026 | 24 | 2.4% |
| intl_nti_cns_dprk_missile_tests | 1984-2024 | 20 | 0% |
| fed_cms_ltch | 1966-2025 | 19 | 0% |

EPA ECHO is not a coverage hole. Its mapped column is FAC_DATE_LAST_INSPECTION, a per-facility attribute, so the histogram shows when facilities were last inspected and 82% of its rows carry no such date. CMS LTCH is the same shape on CERTIFICATION_DATE, though every row there parses. This is the reuse's real cost: the freshness ledger picks the column that answers "how recent", which is the right column on an event table and the wrong one on a snapshot. Every scan now stores its unparsed count and its row total, and any reader over 25% prints a warning, so a span built on a quarter-parsed column can no longer pass as clean.

The 1900 floor was the parser's, not the data's, and 0.14 removed it.

0.14 Parser and mapping repairs, 2026-09-06, in `build_freshness_ledger.py` and `scripts/freshness_mapping.json`. These change what the freshness ledger measures, so they carry their own skeptic pass.

Four date shapes were landing unread. Each got a guarded branch, so a wrong guess still yields NULL and never a false date:

| shape | example | source |
|---|---|---|
| US 12-hour datetime | 5/1/2000 12:00:00 AM | CA_LOBBY_COVER |
| long month name | September 29, 2025 | DOJ FCA settlements |
| month and year | Oct 2025 | IPC food insecurity |
| year and month | 2023-09 | FBI NICS checks |

Two rules were wrong rather than missing. Snowflake's REGEXP_LIKE matches the whole string, not a prefix, so every anchored pattern silently failed on any longer value; the new branches all end in `.*`. And the bare-year rule accepted only 19xx and 20xx, which pinned four sources at 1900. Explicit year kinds now accept 1000 onward, while `mixed` keeps the narrow rule so a stray four-digit id is never read as a year.

`col_ref` now accepts a column name wrapped in double quotes in the mapping, which is how a name holding a space gets through. It still refuses an unquoted string with spaces, because guessing which of those are names and which are prose is how prose gets quoted.

Five mapping entries were corrected and two were set to no column, with the reason recorded in the entry. FDA drug enforcement landed one row holding the whole API envelope, meta and results together, so no per-record date exists until it is re-landed. CMS dialysis maps to a range string, `01Jan2021-31Dec2024`, identical on every row.

Result, newest run: 3,126 rows across 86 source ids and 85 tables, spanning 1543 to 2028.

| source | before | after |
|---|---|---|
| xc_owid_life_expectancy | 1900-2023 | 1543-2023 |
| xc_owid_co2 | 1900-2024 | 1750-2024 |
| xc_owid_temp_anomaly | 1900-2026 | 1850-2026 |
| fed_slavevoyages_intraamerican | unmeasured | 1550-1841 |
| CA_LOBBY_COVER | unmeasured | 1927-2028 |
| fed_cfpb_complaints | unmeasured | 2011-2026 |
| fed_fbi_nics_checks | unmeasured | 1998-2023 |

Two more moved and were missed on the first write-up: xc_owid_fertility from 1900-2023 to 1891-2023, and xc_nagix_dprk_missile_tests from 19 years to 23, which makes the interior-holes table above stale by four years. Six of the seven report 0% unparsed; CA_LOBBY_COVER reports 0.03%. No source lost span or years.

The freshness ledger gains three dates it read as unmeasured: DOJ FCA settlements, FBI NICS checks, IPC food insecurity. It loses one. FDA drug enforcement carried 2026-06-10 before, which is identical to that entry's hand-typed expected value, so it was a claim rather than a measurement, but the ledger row does go away. Its own sanity clamp still drops anything before 1900, so SlaveVoyages stays unmeasured there while coverage reads it fine; that clamp is right for a freshness question and wrong for a coverage one.

Stray years. CA_LOBBY_COVER holds 17 rows scattered from 1927 to 1999 against 568,988 from 2000 on, plus three in 2028. Reported raw, that claims 73 phantom years and would overlap any pre-2000 table, which is the exact failure the histogram exists to prevent. Storage keeps every year; readers trim years holding under a thousandth of the table, and only from the two ends, so an interior hole is never trimmed. The lobby table's 2011-2019 gap survives untouched. CA_LOBBY_COVER now reads 2000-2026 with nine stray years trimmed.

Also caught: the widened year rule at first ended in `.*`, which made an id like 1234567 and a date like 20240108 parse to a year and clear every downstream clamp. The trailing group now allows a non-digit remainder only. The test written to guard the whole-string rule was vacuous and passed everything; it was rewritten.

Applied 2026-09-06 on Chris's explicit permission, priced at $0.00 from 378 prior runs in the query log. `apply` clears SOURCE_FRESHNESS and reinserts, so the old table was copied to SOURCE_FRESHNESS__PREV_20260906 first, 102 rows, and that copy is the rollback.

102 rows written, 79 now carrying a date against 77 before. Eight sources changed:

| source | before | after |
|---|---|---|
| fed_doj_fca_settlements | none | 2026-06-16 |
| fed_fbi_nics_checks | none | 2023-09-01 |
| intl_ipc_food_insecurity_global | none | 2026-05-01 |
| fed_fda_drug_enforcement | 2026-06-10 | none |
| fed_cfpb_complaints | 2026-05-29 | 2026-07-23 |
| fed_cisa_kev | 2026-07-01 | 2026-08-21 |
| fed_hhs_oig_leie | 2026-06-18 | 2026-08-20 |
| xc_ransomwarelive_victims | 2026-06-27 | 2026-08-22 |

Three gained a date the parser could not read before. One lost the hand-typed value it never measured. Four moved forward, which is data landed since the last apply rather than anything this change did. State counts now read 52 stale, 26 fresh, 20 unknown, 3 overdue, 1 due.

Final stored state: 3,126 rows, 86 source ids, 85 tables, 1543 to 2028. Six sources carry an unparsed share above 30%, led by xc_biorxiv_medrxiv at 86% and fed_epa_echo at 82%; each prints a warning when read.

Still open: 20 mapped sources have no usable date column and read the same as unmeasured. A table with no date column at all, such as the committee roster that killed 78, cannot be helped by this. Year grain is the floor, so a table holding only January of each year reads as having no gaps.
Run order: measure everything before Phase 1, so each backfill has a before and an after on the record. Re-measure each table right after its swap.

Smoke: every loader with `--max-rows 1000` into staging only. Skeptic: one fresh reader over the diffs.

## Phase 1, one full day: the cheap five
Order: 1.4 FR, 1.5 HCRIS, 1.2 committee snapshots, 1.3 bills, then 1.1 CD shapes last, its loader being the least ready.

| # | table | rows | prior cost | whole-load check vs publisher |
|---|---|---|---|---|
| 1.4 | FED_FEDERAL_REGISTER_DOCUMENTS 2010-2026 | ~480k | 42 COPY, 1-2 s each | per-month count = API count, all under the 10k cap; 2010-22 = 384,993; CMS-tagged 2,971 |
| 1.5 | FED_CMS_HCRIS 2011-2023 + SOURCE_FILE_YEAR | ~80k | landing 13 s; mart CTAS 0.001 cr | per-year count = data-viewer stats; rpt_rec_num distinct across years; mart NaN count 0 |
| 1.2 | FED_CONGRESS_COMMITTEE_MEMBERSHIP_SNAPSHOTS | ~700k | cosponsors 367k in 13 s | newest snapshot = 3,879 live rows; each snapshot ≥40 codes, ≥400 bioguides; max gap reported |
| 1.3 | FED_GOVINFO_BILLSTATUS + COSPONSORS 113-119 | ~100k + ~1.2M | 10 s + 13 s for two congresses | per-congress count vs GPO directory; cosponsor reconcile zero; null rates by congress |
| 1.1 | XC_CENSUS_CB_CD, cd118 + cd119 | 882 | county COPY 2.2 s | 441 per session; 56 states; 0 null geographies; every House member hits one GEOID |

After each: `dbt run --select <model>`, never bare `dbt run`; registry n_rows; gen_landing_date_views and gen_time_views regen; `connect-one` for the spine tables billstatus and HCRIS.
Gates: rebuild for dbt; spine for connect-one and for adding DISPLAY_SPECS entries. Price line per load. Skeptic per load.
Breaks if skipped: HCRIS mart grain moves from one row per CCN to per CCN-year, its unique tests and E43/E47/E48 findings change by design; ENTITY_INDEX and DISPLAY_KEYSET_LIVE stale until connect-one; FR `_INGESTED_AT` type flip breaks the generated view.

## Phase 2: the big three, one each on days 3-5
2.1 LDA 2011-2026, keyed, staging then INSERT. ~1.15M filings. 694,236 for 2011-19 by API count; 2022-26 counted at run time. Arithmetic: 250 per page at 120 per minute is 23 min for 2011-19, under 2 hours all in. Checks: per-year = API count; distinct FILING_UUID = rows; 1999-2010 and 2020-21 unchanged. Price: re-pull from the query log, the v1 "3 COPY 15 s" line does not match the 831k-row table.
2.2 IRS 527 A and B. 9,701,960 and 8,191,194 rows, footer 18,300,798. Checks: counts match footer; distinct SCHED_A_ID = rows; sums per FORM_ID_NUMBER vs 8872 TOTAL_SCHED_A/B; IS_AMENDED share reported; sums per org-period not double-counted. Nearest price: itoth 28.5M rows, 8.7 min COPY, 21 min wall.
2.3 FEC individual contributions 2000-2026. Runs overnight, last of the loads, nothing else writing. 15 GB zipped new, ~285M rows total. Before: write a vintage line into the probe INDEX, "FEC indiv = cycles 2024+2026, 84,172,112 rows", because 8 probes change on success. After: `connect-one` priced, `dbt run --select finance__fed_fec_indiv_contributions` priced as 285M CTAS plus a 285M unique test with no prior, `build_giant_aggs.py` for the PUBLIC aggs which dbt does not own, skeptic, then drop __PREV. Prior: 84M rows in 69 min wall, 27 min statement time, credits under 1. Extrapolated 4 h wall; not measured. ENTITY_GOLDEN rebuilds slow 3.4x.
Gates: rebuild, spine, spend for 2.3.

## Phase 3, half a day, moved ahead of 2.3: IE mart
Reland IE 2010-2026 with the fixed loader; CYCLE_FILE already exists. Landing today is 2024 73,449 and 2026 14,092 rows; the seven older cycles have no row estimate until fetched, 11-42 MB each. Mart adds IS_SUPERSEDED, FILE_NUM appears as another row's PREV_FILE_NUM, 13,171 today, and IS_OUTLIER, ≥$10M or spender absent from the committees DIM. Flag, never drop. Check: 2024 sum after both flags within 10% of the FEC's $4.4B, rebuilt from the raw csv by the skeptic. Note 24/48-hour notices vs periodic reports can still double-count; bulk has no is_notice. IE is a spine table with a STEEL key; reslice after.
Gates: rebuild, spine.

## Phase 4, per fork 3: scrapers
4.1 Senate PTRs from efdsearch. Sequence tested live: agreement POST, DataTables POST per year, GET each filing. 799 filings 2021-26, 699 HTML, 100 scanned. Land FED_SENATE_EFD_PTR with the old core columns plus FILING_ID, IS_AMENDMENT, FILING_KIND, LINE_NO; paper filings one row with null trade fields. Match on FILER_LAST plus term span. Mart = UNION old ≤2020 and new ≥2021. Unknown until run: line count, throttling, cookie life. Journalism-only tag as today.
4.2 House PTR lines from the Clerk's PDFs. 3,105 PTRs 2021-26, 2,633 text, 421 scans, 51 untested 9-prefix. pypdf plus the tested regex; keep RAW_LINE. Match surname + state + district + term span. No tesseract installed.
Gate: rebuild. Skeptic: 20 filings hand-checked against the source.

## Phase 5, decisions not loads
5.1 Revolving door: drop PERSON_NAME, fix the description, remove the not_null test, filter the doc row. OPM Plum as a people layer: fork.
5.2 Open Payments 2019-21: 3-6.5 GB each, 2019-20 need a column map, 2013-18 archive 404s. Fork.
5.3 Hunch 37 retired: no address on either side.
5.4 Re-probe 78 91 35 83 92 34 and the 8 FEC probes with the new data; price the re-probe. Regenerate the Join Handbook once at the end; it is built from a static 08-29 CSV and is stale, not broken.

## Calendar, honest

| day | work | gates |
|---|---|---|
| 1-2 | Phase 0 all 13, smokes, coverage baseline, diff skeptic | none |
| 3 | Phase 1 five loads, dbt selects, connect-one x2 | rebuild, spine |
| 4 | 2.1 LDA, Phase 3 IE | rebuild, spine |
| 5 | 2.2 527; vintage line; 2.3 starts overnight | rebuild |
| 6 | 2.3 verify, connect-one, mart, aggs, skeptic, drop __PREV | spine, rebuild, spend |
| 7-8 | 4.1 Senate, timeboxed | rebuild |
| 9-10 | 4.2 House if fork 3 = A | rebuild |
| 11 | Phase 5, re-probes, handbook regen | none |

## Standing rules
- Price line from the warehouse log, then wait for go. "No real number" where nothing comparable ran.
- Staging then SWAP, old live kept as __PREV until the skeptic passes.
- Whole-load proof against the publisher's own count, never our last run.
- `dbt run --select`, never bare.
- Heartbeat LINK tier off for the run, or say the spend is accepted.
- PAT expires 2026-09-20; preflight checks it before every multi-hour run.
- The chat door is 401; every price comes through the scripts door.
- Re-measure coverage after every swap; a backfill that moves no min date did not land.
- Run the overlap check before writing any cross-source join.
- Traps found go in .claude/traps.md the same day.
