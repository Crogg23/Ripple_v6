# News-to-warehouse corroboration map — 2026-09-05

Chris's ask, verbatim: "I want you to do a full 'mapping' of real world things that have come to light and whether or not my data would corroborate or 'discover' the same thing. Obviously only things we reasonably believe I already have data for. Go looking"

All queries through the Python door, LIBRARY_RAW.LANDING, run 2026-09-05. Scripts and raw output in the session scratchpad (inv.py, cov.py, probes.py, probes2.py, probes3.py).

## Three grades
| grade | question | proves |
|---|---|---|
| Echo | story says X, table shows X | the file landed and did not rot |
| Retrace | start from the story's first clue, joins reach the end | the joins work |
| Stumble | one dumb query over the whole table, story pops in the top 20 | the warehouse can find |

## The scorecard — 24 stories
| # | story | source | table | years held | grade | result | verdict |
|---|---|---|---|---|---|---|---|
| 1 | WaPo 2019, 76B opioid pills 2006–12, Kermit WV | DEA ARCOS | FED_DEA_ARCOS_FULL | 2006–2014 | Stumble | top 8 WV pharmacies by oxy+hydro pills: Strosnider Kermit 13.2M, Family Discount Mt Gay 12.8M, CVS Huntington 10.7M, CVS Parkersburg 10.3M, Hurley Williamson 8.9M, Tug Valley 8.8M. Four of WaPo's named independents in the top 6 | **HIT** |
| 2 | Reveal 2018 "Kept Out" redlining | HMDA | FED_CFPB_HMDA_HISTORIC | 2015–2017 | Echo | morning: all 19.1M rows "Loan originated", zero denials, MISS. Reloaded same day from the all-records files, 44,992,667 rows, 8 action codes. Philadelphia 2015–16 conventional purchase, owner-occupied: Black applicants denied 27.2%, white 8.1%, raw ratio 3.34. Reveal's adjusted figure was 2.7x. Worst raw ratios: Baton Rouge 3.68, Memphis 3.59, St. Louis 3.56 | **HIT after reload** |
| 3 | 2024 ActBlue/WinRed smurfing | FEC | FED_FEC_INDIV_CONTRIBUTIONS | thru 2026 | Stumble | 1,103 name+state donors with 2,000+ gifts in 2023–24 (708 by name+zip9, which splits people). Top: Makowski MI 48,130 gifts, $99k, ~$2 each | **HIT** |
| 4 | Waco patent-court surge 2020–22 | FJC IDB | FED_FJC_IDB_CIVIL | 1988–2025 | Stumble | by FILEDATE year, district 42 (WDTX per FJC codebook) share of NOS 830: 2019 not top 3, 2020 22.4% #1, 2021 25.2% #1, 2022 23.6% #1, 2023 17.6% #2 after the July 2022 random-assignment order. TAPEYEAR lags a year, do not use it | **HIT** |
| 5 | Global Witness 2018, toddler company owners | UK PSC | UK_COMPANIES_HOUSE_PSC | current | Stumble | 5,053 individual PSCs born 2020+, 24 born before 1900, 17 over 155 | **HIT** |
| 6 | NEJM 2016, 1% of doctors = 32% of paid claims | NPDB | FED_HRSA_NPDB | 1990–2026 | Retrace | 165,248 paid practitioners; top 1% hold 13.3% of dollars, 3.4% of claims; repeaters hold 52.8% of claims | **PARTIAL** — denominator differs, NEJM counted all physicians |
| 7 | Flint lead 2015–16 | SDWA LCR | FED_EPA_SDWA_SDWA_LCR_SAMPLES | 1992–2025 | Echo | PWSID MI0002310 = "FLINT, CITY OF" confirmed. PB90 mg/L by SDWIS period: Jul–Dec 2014 .006, Jan–Jun 2015 .011, Jan–Jun 2016 **.020**, Jul–Dec 2016 .012. Press reported 11 and 20 ppb for the 2015 halves; SDWIS labels the 20 one period later. Action level .015 | **HIT** |
| 8 | Jackson MS lead 2016 | SDWA LCR | same | same | Echo | PWSID MS0250008 = "CITY OF JACKSON" confirmed. Period ending 12/31/2015 **.0286**, 2016 .016, then under .015 | **HIT** |
| 9 | Upper Big Branch 2010, 515 violations in 2009 | MSHA | FED_MSHA_VIOLATIONS | 2000–2025 | Echo + Stumble | echo: 506 violations 2009, 198 S&S, 920 in 2010. Stumble: rank 10 of 192 WV underground coal mines in 2009 | **HIT echo, MISS stumble** |
| 10 | Wells Fargo fake accounts Sep 2016 | CFPB complaints | FED_CFPB_COMPLAINTS | 2011–2026 | Echo | monthly WF complaints ~770 Jan–Aug, **1,592 Sep**, 1,383 Oct | **HIT** |
| 11 | Amazon warehouse injury rate ~2x industry | OSHA ITA 300A | FED_OSHA_ITA_300A_SUMMARY_2024 | 2024 | Stumble | NAICS 4931: Amazon TRIR 6.21 across 458 sites vs 3.51 for 9,405 others | **HIT** |
| 12 | Norfolk Southern after East Palestine | FRA | FED_FRA_EQUIPMENT_ACCIDENTS | 1975–2026 | Retrace | NS 2023: 435 accidents (452 in 2022), 9 hazmat-release cars, the 2018–24 high for hazmat only; UP 776, BNSF 492 | **WEAK** — needs per-mile rate |
| 13 | Life Care Center Kirkland, COVID 2020 | CMS nursing deficiencies | FED_CMS_NURSING_HOME_DEFICIENCIES | 2023–2026 for this CCN | Echo | rows 2023 onward only; 2020 survey absent | **MISS — vintage** |
| 14 | Charles Lieber, undisclosed China ties | NIH RePORTER | FED_NIH_REPORTER | 2000–2026 | Echo | PI_NAMES = "CHARLES LIEBER" confirmed, Harvard. FY2000–2019 $11.4M; FY2017–18 $1.4–1.6M/yr; three small rows FY2024–26 ($36–42k) | **HIT** |
| 15 | Ozempic suicidal-ideation reports 2023 | FAERS | FED_FDA_FAERS_* | 2004q1–**2014q2** | Echo | table ends 2014; semaglutide approved 2017 | **MISS — vintage** |
| 16 | 2025 ICE detention surge | ICE stints | FED_ICE_DETENTION_STINTS | 2004–2026 | Stumble | book-ins/month: 45k Dec 2024 → 104k Jun 2025 → 128k Dec 2025. Release reason "death" codeable only from 2022: 9 (2024) → 15 (2025) | **HIT** |
| 17 | ProPublica 2021, Kabbage fake NJ farms | SBA PPP | FED_SBA_PPP | 150K+ loans only (968,524 rows matches the public 150k+ file) | Stumble | fake farms were ~$20k loans; not in this slice. Address stacking works: 40 loans at one Peoria address | **MISS — slice** |
| 18 | 2024 political ad spend | Google polads | FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND | 2018–2026 | Echo | Harris Victory Fund $67.0M, FF PAC $61.7M, Harris for President $53.6M, Trump 2024 $32.3M | **HIT** |
| 19 | Unusual Whales, most active House traders 2021 | House PTR index | FED_HOUSE_FD_PTR_INDEX | 2008–2026 | Stumble | PTR filings 2021–22: Lowenthal 140, DelBene 36, Blumenauer 34, Green 32, Schrader 28, Rogers 26, Gottheimer 26, Hern 25, Khanna 24, McCaul 24 | **HIT** — counts filings, not trades |
| 20 | WaPo Feb 2022, Tesla phantom braking | NHTSA complaints | FED_NHTSA_COMPLAINTS | thru 2026, headerless | Stumble | all Tesla brake+FCW complaints per month: 42 Sep 21, 83 Oct, 160 Nov, 189 Dec, 342 Jan 22, 884 Feb. Broader filter than WaPo's 107 phantom-braking reads; shape matches, magnitude does not. Feb spike is partly after NHTSA opened its probe | **HIT — shape** |
| 21 | ProPublica 2023, Thomas and Harlan Crow | CourtListener disclosures | FED_COURTLISTENER_DISCLOSURE_GIFTS | — | Echo | one Crow gift on file: Douglass bust $6,484. 2,025 gifts across 1,432 disclosures, SOURCE is OCR text with 58 nulls, and there is no people table to tie a disclosure to Thomas | **MISS — bridge** |
| 22 | Debarred firms still paid | SAM × USAspending | FULL_R2 tables | 2011–2026 | Retrace | 22 vendors, 99 actions, $1.86M (report 2026-09-04). Caveat carried: UEI did not exist before April 2022, the 2011–15 matches ride a backfilled DUNS→UEI map | **HIT** |
| 23 | Dollars for Docs | Open Payments × Part D | 2024 both | 2024 | Retrace | paid $10k+ prescribers write 1.6x–7x costlier scripts (report 2026-09-04) | **HIT** |
| 24 | June 2026 DOJ fraud takedown | NPPES × Part D | 2024 | Retrace | 4 of 5 named prescribers at 91st–99.4th pct before charges; Aquino tops out at the 86th (report 2026-09-05, which overstated this as 5 of 5) | **HIT** |

Tally after the HMDA reload: 17 hits, 1 partial, 1 weak, 5 misses. Four misses are a vintage, a load slice, or a missing bridge table. The fifth, MSHA stumble, was my query, not the data.

## What each miss means, plainly
- **HMDA (2)**: was originations only because the 2026-08-05 loader chose the first-lien-owner-occupied file family, a scope call. Fixed 2026-09-05: `scripts/hmda_historic_lar_load.py --family all --run`, 3.4 GB downloaded, 45.0M rows swapped in, registry and quality gate updated. The registry MERGE had a latent SQL bug (adjacent string literals), fixed with `||`.
- **FAERS (15)**: 42 quarters, stops 2014q2. Any drug approved after 2014 has no adverse-event trail here.
- **Nursing home deficiencies (13)**: CMS publishes a rolling ~3-year window; 2020 is gone from the public file. Not a load bug.
- **PPP (17)**: only the 150K+ file landed. Small-loan fraud, which is most PPP fraud, is out of reach.
- **MSHA stumble (9)**: raw violation count ranks UBB 10th. The story was withdrawal orders and S&S density. Right table, wrong dumb query.
- **Thomas gifts (21)**: the gifts table has no path to a judge's name. Needs the CourtListener people table, not landed.

## Skeptic pass, same day
Fourteen disagreements. Fixed in the table above: takedown was 4 of 5 not 5 of 5; FEC donor count was name+zip9 pairs; Lieber sum was $11.4M not $13M; FJC needed FILEDATE not TAPEYEAR and the peak is 2020–22; Thomas downgraded to miss; SAM caveat restored; three top-N lists were non-contiguous; PWSIDs now name-checked. Not fixed: no negative controls were run, every grade is one query. Skeptic's suspicion that SDWIS sample periods sit a step late is left open; SDWIS start and end dates are what the table says.

## Mart rebuild, same day, after the skeptic caught it stale
The landing swap does not touch the dbt mart. LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC still held 19,136,434 rows until `dbt run -s +housing__fed_cfpb_hmda_historic+` on 2026-09-05. Now 44,992,667 rows, 8 action codes, 6,967,834 denials; TIMELINE view and timeline__housing_index rebuilt with it. Tests: not_null and unique on lar_record_id pass at both staging and mart, the staging unique took 6m59s over 45M rows. Log: library-onboarding/ripple_dbt/logs/hmda_historic_rebuild_2026-09-05.log. Registry and gate receipt: scripts/hmda_historic_scratch/register_rerun_2026-09-05.log.
Skeptic's second pass, applied: loader now refuses --family all without denials and asks before a first-lien swap; download.sh all-records loop is live behind FAMILY=all; warehouse_topo_map report corrected; per-year null check run, all three years evenly populated. "Reproduces Reveal" is retired: the raw rate ratio is 3.4x, the raw odds ratio 4.35, Reveal's regression-adjusted odds ratio 2.7 on 2012–2016. Same direction, different statistic.

## Mart rebuilt, same day
dbt run on +housing__fed_cfpb_hmda_historic+ after `greenlight rebuild`: staging view, HOUSING mart (3m43s), TIMELINE view, timeline index, timeline warehouse, 5 of 5 succeeded. dbt test 4 of 4 passed in 7m11s, including the unique test on lar_record_id over 45M rows. Warehouse count on LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC: 44,992,667 rows, 6,967,834 denials. Log: library-onboarding/ripple_dbt/logs/hmda_historic_rebuild_2026-09-05.log. Registry and gate receipt: scripts/hmda_historic_scratch/register_rerun_2026-09-05.log.

## Broken-load traps found on the way
- FED_EOIR_CASE_DATA: 12.6M rows, one column, tab-separated text. Unparsed.
- FED_NHTSA_COMPLAINTS: headerless C1..C54. Usable: C3 mfr, C4 make, C5 model, C6 model year, C8 date YYYYMMDD, C12 component. 110k rows with blank date.
- FED_MSHA_VIOLATIONS: every value carries literal double quotes. Filter with '"46%'.
- FED_HRSA_NPDB: PAYMENT is a string with a leading $.
- FED_DEA_ARCOS_FULL: TRANSACTION_DATE is MMDDYYYY text; two rows hold floats.

## Cost
HMDA reload: 3 downloads totalling 3.4 GB, ~45M rows through write_pandas on X-Small. Last load of the 19M-row slice priced at ~$0.80 across 125 statements; this one is 2.4x the rows, so ~$2, exact figure in the query log tomorrow.

Roughly 60 queries. Largest scanned ARCOS 178M rows (year distribution, top WV pharmacies) and FEC 84M rows (smurf group-by). No prior run of this pattern in the query log to price against.
