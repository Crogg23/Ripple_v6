# Join patterns — 2026-09-23

Door: Python scripts, `connect/db.py`. All tables in `LIBRARY_MARTS.HEALTH`.

## 1. Pharma money vs brand-name prescribing — 2 tables

Join: `HEALTH__FED_CMS_PART_D_PRESCRIBERS` (DATA_YEAR=2024, per-NPI summary) LEFT JOIN
`HEALTH__FED_CMS_OPEN_PAYMENTS` (PROGRAM_YEAR=2024, summed per NPI) on NPI.
Filter: prescribers with >=100 claims; rows where BRND_TOT_CLMS or GNRC_TOT_CLMS is suppressed ('#') DROPPED.
Suppression hides ~606K of 1.42M prescribers, so the sample leans to big prescribers.
Brand % = sum(BRND_TOT_CLMS) / (sum brand + sum generic). Cost/claim = sum(TOT_DRUG_CST)/sum(TOT_CLMS).
Skeptic-corrected: first run zero-filled suppressed rows; numbers below are the rerun.

| Specialty | none | <$100 | $100-1K | $1K-10K | $10K+ | $/claim none -> $10K+ |
|---|---|---|---|---|---|---|
| Cardiology | 16.7 | 16.4 | 16.7 | 18.3 | 24.9 | 211 -> 398 |
| Endocrinology | 50.8 | 51.3 | 51.7 | 52.3 | 53.1 | 433 -> 511 |
| Family Practice | 12.0 | 12.5 | 13.5 | 14.0 | 16.1 | 81 -> 155 |
| Internal Medicine | 12.8 | 13.2 | 14.0 | 15.6 | 24.1 | 94 -> 355 |
| Neurology | 10.3 | 10.4 | 10.7 | 12.2 | 17.8 | 377 -> 879 |
| Nurse Practitioner | 12.3 | 13.1 | 14.5 | 17.4 | 23.4 | 110 -> 616 |
| Psychiatry | 4.6 | 5.1 | 6.0 | 7.2 | 10.7 | 102 -> 231 |

Top tier beats no-payment tier in all 7. Step-by-step rise holds in 6; Cardiology dips at <$100.
Correlation only: companies may target doctors who already prescribe brand.
Specialty label is CMS's PRSCRBR_TYPE; "Internal Medicine" at $10K+ may hide subspecialists.

## 2. Excluded providers still paid by pharma — 3 tables

LEIE (`HEALTH__FED_HHS_OIG_LEIE`): NPI_IS_REAL, not reinstated, 10-digit NPI -> 8,656 NPIs.
Join to Open Payments 2024 on NPI, exclusion date before 2024-01-01.
- 193 NPIs hit; 183 last-name match, 177 full first+last match. 190 after dropping waivers.
- Dollars: ~$160K total, $114,040 of it one row.
- Top: Hector Molina, TX, excluded 2019-06-20 under 1128(a)(1); Skye Orthobiologics, "Debt forgiveness", 2024-01-22.
- Eduardo Miranda, TX, excluded 2015 under 1128(a)(1), WAIVER HOLDER: 201 payments from many oncology firms in 2024.
Join to Part D prescribers 2024 on NPI: **1** excluded-before-2024 NPI present: Miranda, 1,382 claims.
Miranda holds an OIG waiver, HAS_WAIVER=True: OIG allowed him to keep billing. Weakest example, not strongest.
WAS_REINSTATED is False on all 83,816 LEIE rows; the filter removes nothing. LEIE lists current exclusions only.
Skeptic reran name matches as 185/179 vs 183/177 here; total dollars $166,468. 8,660 NPIs by bucket sum.

Exclusion year vs paid-in-2024:
| Excluded | NPIs | Paid 2024 |
|---|---|---|
| before 2014 | 1,637 | 29 |
| 2014-19 | 2,935 | 82 |
| 2020-22 | 1,401 | 53 |
| 2023 | 618 | 29 |
| 2024+ | 2,069 | 186 |

## 3. Nursing homes: ownership and chain vs fines — 2 tables

`HEALTH__FED_CMS_NURSING_HOME` LEFT JOIN `HEALTH__FED_CMS_NURSING_HOME_PENALTIES` (fines summed per CCN).

| Owner | Homes | Staff hrs/res/day | Turnover % | Stars | Fines/bed | % fined |
|---|---|---|---|---|---|---|
| For profit | 10,851 | 3.70 | 47.5 | 2.83 | $320 | 47.5 |
| Non profit | 2,908 | 4.40 | 41.5 | 3.58 | $205 | 35.4 |
| Government | 941 | 4.26 | 44.3 | 3.29 | $203 | 40.8 |

Worst chains by fines per bed, 20+ homes:
| Chain | Homes | Staff hrs | Turnover | Stars | Fines | $/bed |
|---|---|---|---|---|---|---|
| Arcadia Care | 22 | 3.00 | 49.6 | 1.45 | $3.59M | 1,357 |
| Reliant Care Management | 32 | 2.36 | 60.8 | 1.19 | $3.87M | 1,238 |
| Tutera Senior Living | 26 | 3.60 | 55.5 | 2.24 | $2.57M | 1,026 |
| Ephram Lahasky | 23 | 3.48 | 53.1 | 1.86 | $2.30M | 851 |
| Cascades Healthcare | 20 | 3.51 | 61.6 | 2.00 | $1.57M | 825 |
| ... #12 of 127: Avir Health Group | 117 | 3.17 | 57.8 | 2.23 | $7.55M | 592 |

Penalty table is CMS's rolling ~3-year window, not lifetime.
