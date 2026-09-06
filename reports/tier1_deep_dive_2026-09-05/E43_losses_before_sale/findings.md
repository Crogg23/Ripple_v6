# E43. Were sold hospitals already losing money?

**Short version.** The first pass's 60% is real and reproduces. A quarter of it stands on the seller's stub report. Full year against full year, sold hospitals lose money **55%** of the time vs **34%** for everyone else. Still 1.6x. Confirmed, reframed.

## What "sold" means in the data

- **POS_OTHER** (`HEALTH__FED_CMS_POS_OTHER`, 44,429 rows) is one row per CCN — the Medicare certification number that identifies one facility across every CMS file.
- It carries `CHOW_DT`, the date of the **most recent** change of ownership (CHOW). One date per facility, no history. `CHOW_PRIOR_DT` holds the one before, on 2,967 rows.
- `CHOW_SW` is empty string on all 44,429 rows. Dead column.
- Hospitals = `PRVDR_CTGRY_CD = '01'`: 13,540 rows, 2,532 with a CHOW date ever.
- **Sold FY2022-24 = hospital with `CHOW_DT` in 2022-2024: 128 hospitals.** 14 in 2022, 44 in 2023, 70 in 2024.
- What kind of CHOW: 53 of the 88 studied carry a different name today than on their pre-sale report (Tenet's Orange County hospitals became UCI Health, Steward St. Anne's became Brown University Health, four Everest rehab hospitals became Mercy/Liberty/Longview/Temple). These are sales, not intra-system paperwork. 21 kept the exact name.

## Transaction date or filing date?

- The watch-out: is `CHOW_DT` when the deal happened, or when CMS processed the form?
- Checked day of week on all 1,248 CHOWs since 2015: **Sat 151, Sun 167 — 25% on weekends.** A processing date never lands on a weekend.
- Checked day of month: **937 of 1,248 (75%) on the 1st.** That is how deals are dated.
- Answer: `CHOW_DT` is the effective date the parties put on the CMS-855A. It is the closest thing to a transaction date in any CMS file. No filing date exists in POS at all.
- Caveat: one date per CCN. A hospital sold in 2023 and again in 2025 carries only 2025 and falls out of the window. The 128 is a floor.

## What "losing money" means

- **HCRIS** (`HEALTH__FED_CMS_HCRIS`, 6,103 rows, 6,040 CCNs) — the Medicare cost report every hospital files yearly.
- Money fields found: `NET_INCOME`, `NET_MARGIN_RATIO`, `NET_INCOME_FROM_SERVICE_TO_PATIENTS`, `TOTAL_INCOME`, `NET_PATIENT_REVENUE`, `TOTAL_OPERATING_EXPENSE`. All filled on 6,103 of 6,103.
- Used `NET_INCOME < 0`. Not the patient-service line: 58% of ALL hospitals show a loss on patient service alone; they live on other income, so that line calls everyone a loser.
- One report per hospital, fiscal years ending 2022-11-30 to 2024-09-30. **One vintage, not a series.** "The year before the sale" is really "the last report ending before the sale", which has a report to point at only for 2023-24 sales. 2022 sales: 1 of 14 has one.

## Rebuilding the 60%

| Cut | Hospitals | Losing | Rate |
|---|---|---|---|
| First pass, naive join (fans out to 137 report rows, counts reports filed after the sale) | 121 (137 rows) | 80 rows | 58.4% |
| Rows where the report ends before the sale | 89 rows | 54 | 60.7% |
| **One report per hospital, last one ending before sale** | **88** | **53** | **60.2%** |
| Same, full-year reports only (300+ days) | 62 | 34 | **54.8%** |
| &nbsp;&nbsp;of which sold in 2024 | 55 | 28 | 50.9% |
| &nbsp;&nbsp;of which sold in 2023 | 7 | 6 | 85.7% |
| Not sold in the window, all reports | 5,966 | 2,087 | 35.0% |
| **Not sold in the window, full-year reports only** | **5,782** | **1,975** | **34.2%** |

- Base group is "not sold in 2022-24"; 1,271 of the 5,782 had a CHOW some other year, rate unchanged at 34.2%.
- The 62 full-year cohort is mostly 2024 sales (55 of 62); 2024 alone is 28/55 = 50.9%.
- 60% reproduces three different ways. The first pass got the right number by accident: it counted after-sale reports and double-counted 16 hospitals, and those errors cancelled.
- Of the 128 sold: 88 have a pre-sale report, 33 have only an after-sale report (19 of those losing), 7 have none.

## The stub-report trap (new)

- When a hospital is sold, the seller closes its books and files a cost report **ending the day before the sale**.
- 26 of the 88 pre-sale reports run under 300 days. **25 of the 26 end exactly one day before `CHOW_DT`.** Five Everest rehab hospitals sold 2023-03-01 filed 58-day stubs, one at a -78% margin on $800k revenue.
- Short periods look worse everywhere, not just when sold: across all of HCRIS, sub-180-day reports lose 65% of the time, 180-299 days 60%, full years 34%.
- In the sold group: stubs 85% losing, half-years 62%, full years 55%.
- Stubs are 26 of the 88 reports and carry 19 of the 53 losses. A third of the losses behind the "60%" come from stub reports. The fair test is full year vs full year.

## Mix does not explain it

- Facility type: the 88 are 64 short-term, 9 rehab, 6 long-term, 5 psych, 4 critical access. Base rates by type (35 / 26 / 56 / 43 / 33%) give an expected 31.5 losing of 88 = **36%**. Observed 60%.
- Ownership type: 39 for-profit corporations (base 33%), 22 other for-profit (38%), 8 nonprofit (31%), rest scattered. Expected **36%**. Observed 60%.
- Fiscal year: base rate is 35.3% in FY2023, 35.8% in FY2024. Flat.
- Sale year: 2023 sales 18 of 22 losing (82%, stub-heavy), 2024 sales 34 of 65 (52%).

## How deep

- Median net margin, last pre-sale report: **-1.6%**. Every other hospital: **+1.5%**.
- Full-year only: -0.5% vs +1.6%.
- Distribution: sold group bunches in the -10% to 0% band (38 of 88 = 43%, vs 28% of others). Few catastrophes, mostly quiet bleeding.

## What a skeptic would attack

- **Small n.** 62 full-year hospitals. 34 losing against an expected 21.2 at the 34.2% base rate; binomial sd 3.7, so 3.4 sd out. On the 88, 53 vs 31.2 expected, 4.9 sd. Not chance.
- **Survivor bias in the base.** HCRIS is one vintage; hospitals that closed before filing are absent from both sides. Cuts both ways, does not favor the finding.
- **"Before" is sometimes 14 months before.** Median gap report-end to sale is 3 months, mean 4.6, max 14. One vintage means no closer report exists. This is the year before, as asked.
- **The seller's full-year report also ends the day before the sale** for 17 of the 62 full-year cases. Full-year is full-year; a 365-day report ending at the sale is not a stub.
- **Is a CHOW a sale?** 53 of 88 renamed. Sales.
- **The 40 with no pre-sale report** are missing at random relative to margin as far as we can tell (their after-sale rate is 19 of 33 = 58%). Cannot be ruled out as a bias.
- **No prior-year HCRIS files landed.** The catalog lists 2011-2023 Hospital Provider Cost Report files; only one is landed. Landing FY2021-22 would give a true "year before" for every 2022-23 sale and turn this into a trend, not a cross-section.

## Answer

Yes. Hospitals that changed hands in 2023-24 were losing money on their last full-year cost report 55% of the time, against 34% for hospitals that did not change hands. Median margin -0.5% vs +1.6%. Facility mix and ownership mix each predict 36%, so the gap is not composition. The first pass's 60% counts the seller's terminating stub reports, which lose money 85% of the time and inflate the number.

STATUS: confirmed but reframed
HEADLINE: 55% of hospitals sold in 2023-24 (mostly 2024 sales, of those with a readable prior report: 62 of 128) were losing money on their last full-year cost report, vs 34% of hospitals not sold in the window — the first pass's 60% leans on seller stub reports.
