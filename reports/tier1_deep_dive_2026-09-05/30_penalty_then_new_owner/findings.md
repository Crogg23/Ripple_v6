# Hunch 30 — penalty, then a new owner

**The ask:** do new owners show up right after a nursing home gets penalized, like a shell game?
**First pass said:** confirmed, 39 homes did exactly this.

## The chain

**What was checked**

- A home is a CCN, the CMS Certification Number Medicare gives a facility. Penalties: 16,180 rows, 6,831 homes, 2023-06-17 to 2026-05-13. Enrollments: 14,425 rows = 14,425 CCNs, one row per home, the company operating it today.
- How the first pass saw "new owner": the operator's **INCORPORATION_DATE** falls after the home's first penalty. No window. No base rate.
- Reproduced it exactly: 6,831 penalized, 6,660 in the enrollment file, 3,956 with an incorporation date, **39 incorporated after first penalty**. (First pass also said 139 incorporated since June 2023; it is 130 among penalized homes, 216 in the whole file.)

**What is wrong with the clock**

- INCORPORATION_DATE is filled on 8,989 of 14,425 rows, has 103 dates before 1900, and its **newest value is 2024-09-17**. The penalty file runs to 2026-05-13. Anyone who bought after September 2024 cannot show up.
- 149 rows have an incorporation date after the enrollment record date — the two clocks disagree on 1% of rows.
- 13 of the 39 look like one deal: eight Oregon homes incorporated 2024-05-10 and five Washington homes 2024-05-14, all named "<place> SNF Healthcare LLC". That is an inference from name pattern and dates — all 68 "... SNF Healthcare LLC" rows in the file carry 68 distinct ASSOCIATE_IDs across 11 states, so nothing in the table ties them to one buyer. Thirteen same-week single-home LLCs also fits a shell shape. Two more same-date same-state pairs. Counted as events: 13 + 4 + 22 = 25.
- Gap from first penalty: 13 inside 90 days, 15 in 91–180, 9 in 181–365, 2 past a year. "Right after" was never defined.

**Clock-free check**

- NH411 flags 55 homes as changed ownership in the last 12 months. **41 of 55 (75%) are penalized homes** vs 6,829 of 14,713 (46%) of all homes. z = 4.2. No date column involved.

**Rebuilt a different way**

- The ENROLLMENT_ID is `O` + YYYYMMDD + 6 digits. All 14,425 parse. Range 2002-08-01 to **2026-02-12**. A new operator files a new enrollment, so this dates the current operator's arrival.
- Validation: Nursing Home 411's `PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS` is 'Y' on 55 homes (the trap said N everywhere — true for FED_CMS_NURSING_HOME's 14,700 rows, not for NH411). The enrollment clock has a record dated inside those 12 months on **52 of 55**. The incorporation clock has 1.
- On the enrollment clock: **650 of 6,660** penalized homes have a record dated after their first penalty; 391 within a year, 219 within six months; 583 distinct owner IDs. 38 of the original 39 are inside this set.

**Base rate, calendar-matched**

Same calendar window for both groups, so industry churn cancels.

| cohort | penalized | new record next year | not penalized | new record next year | z |
|---|---|---|---|---|---|
| penalty in 2023 H2 → 2024 | 2,229 | 176 = **7.9%** | 11,554 | 590 = **5.1%** | 5.3 |
| penalty in 2024 → 2025 | 3,718 | 223 = **6.0%** | 10,697 | 409 = **3.8%** | 5.6 |

- Dose: fined $100k+ in 2023 H2 → 12.6% changed hands in 2024; $100k+ in 2024 → 9.0% in 2025.
- Inside for-profits only: 8.1% vs 6.3%, then 6.7% vs 4.4%. Inside nonprofits: 7.4% vs 2.7%, then 2.4% vs 1.3%. Not just ownership mix.
- Same test on the incorporation clock, 2023 H2 → Jan–Sep 2024: 1.55% vs 0.89%. Same direction, a fifth of the events.

**Before or after**

- 658 homes have a new record between 2024-06-17 and 2025-05-13, so a full year is visible on both sides. Penalties: **409 in the year before, 331 in the year after — a real 19% drop** (z about 2.9), and no pre-sale hump in the months before month zero.
- Three readings fit the drop and these tables cannot split them: the new operator runs a cleaner home; CMS attaches penalties to the new record with a lag; a fresh enrollment buys a grace period before the next survey.
- 294 of the 650 were penalized again under the new record.

## What a hit means / what a miss means

- **Hit as the hunch was written:** penalties bunch up, then a fresh company appears on the same CCN, then penalties stop. That would be owners shedding a record.
- **What we have:** penalized homes change hands ~1.5x as often as the rest, more if the bill is bigger, penalties do not spike before the change, and they fall 19% after it. That is a distressed asset changing hands, with fines as one of the symptoms. It is consistent with a shell game but does not show one — a shell game and an ordinary forced sale look identical on these two tables.
- **Miss:** would have been rates equal across groups. They are not; z above 5 both cohorts.

## What a skeptic would attack

1. *ENROLLMENT_ID date is not a sale date.* True. It is when the current operator's Medicare record was created. Re-enrollments, revalidations that issue a new ID, or a CHOW processed late all move it. Answer: it catches 52 of 55 CMS-flagged ownership changes, and the base-rate design does not care what the date "is" as long as it means the same thing in both groups.
2. *The snapshot only keeps the current record.* True. A home sold in 2024 and again in 2025 shows once, dated 2025, and the 2023 H2 cohort drops 642 homes whose record is dated after 2024. Both groups lose the same way; the 2024 cohort drops 10.
3. *Penalized homes are for-profit, and for-profits sell.* Checked; the gap holds inside each class.
4. *The 39 was never the point; the enrollment clock is a different claim.* Yes. That is why STATUS is reframed, not confirmed.
5. *Who bought them?* Not in the warehouse. No SNF change-of-ownership file is landed; POS_OTHER's five categories hit zero penalty CCNs. The All Owners file that would name the buyer is catalogued in LANDING.FED_CMS_MAIN and never loaded. "Selling to themselves" cannot be tested here.

## Traps found

- `HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.INCORPORATION_DATE` tops out at 2024-09-17 in a file whose records run to 2026-02-12; 62% filled; 103 pre-1900 values. Never use it as a recency clock. The ENROLLMENT_ID prefix is the working date column.
- `PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS` is all 'N' on FED_CMS_NURSING_HOME (14,700) but 'Y' on 55 rows of FED_NURSINGHOME411. The two tables are not the same flag.
- `HEALTH__FED_CMS_POS_OTHER.MEDICARE_MEDICAID_PRVDR_NUMBER` has ONE distinct value on 15,324 category-21 rows. The CCN column is `CCN`. And no POS_OTHER category is a nursing home.

STATUS: confirmed but reframed
HEADLINE: Penalized nursing homes change hands the next year at 7.9% vs 5.1% for the rest (2023 cohort; 6.0% vs 3.8% for 2024), 650 penalized homes carry a post-penalty operator record — but the first pass's 39 read a clock that stops in Sept 2024 and 13 of them are one Oregon-Washington deal.
