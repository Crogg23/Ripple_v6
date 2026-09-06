# E39 — Do the paid ones prescribe way more opioids than unpaid ones?

**Short answer:** paid by anyone, barely. Paid by an opioid maker, massively. And it reads as targeting, not buying.

---

## What was checked

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS` — Medicare Part D (the drug benefit) by-provider summary. One row per prescriber, keyed by NPI (the 10-digit national provider ID). 1,416,883 rows, NPI unique (checked: count = distinct). **One year, data year 2024** — no year column; pinned via the registry note "Data year 2024, release RY26" (`reports/row1/registry_dump.json:10890`). The hunch said "two years." It is one.
- `LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS` — Open Payments, the federal ledger of industry money to clinicians. The undated table is **program year 2024** (PROGRAM_YEAR single-valued). 15,385,047 rows, 979,137 distinct NPIs. Used the LANDING copy, not the mart: the mart keeps 22 columns and drops the drug-name columns the opioid-maker test needs.
- `..._OPEN_PAYMENTS_2022` and `_2023` — prior program years, for the persistence check.

**Measure:** `OPIOID_PRSCRBR_RATE` = opioid claims as a share of all Part D claims, per prescriber. Reported three ways so no single one can carry the story: aggregate (sum opioid claims / sum claims over the group), mean of per-prescriber rates, and share of prescribers at 10%+.

**Groups:** unpaid in 2024 / paid but no opioid brand named / paid on an opioid painkiller brand (Belbuca, Xtampza, RoxyBond, Nucynta, Dsuvia, Olinvyk, OxyContin, Dilaudid, Opana and 30 more; addiction-treatment products like Suboxone and Sublocade deliberately excluded). Teaching-hospital payment rows dropped.

---

## The numbers

**1. All industry money, 2024 — the first-pass claim, rebuilt**

| | unpaid | paid by anyone |
|---|---|---|
| prescribers | 682,081 | 734,802 |
| opioid share of claims (aggregate) | **3.09%** | **3.63%** |
| mean of per-prescriber rates | 5.13 | 6.99 |
| median rate | 0.0 | 0.0 |
| share at 10%+ opioid | 11.3% | 14.3% |
| median claims | 136 | 373 |

- The mean-of-rates gap (5.1 vs 7.0, +36%) is most likely what the first pass saw. The aggregate gap is +18%. The median is zero on both sides.
- **Specialty mix eats half of it.** Direct standardisation: give the unpaid the paid group's specialty mix and their mean goes 5.41 → 6.24, against 7.04 for the paid.
- **Flat across deciles of money.** Aggregate opioid share by decile of 2024 dollars: D1 ($17 median) 3.23%, D5 ($171) 3.69%, D9 ($1,394) 3.69%, D10 ($4,417) 3.80%. Ten times the money, same opioid share.
- **Within the top 5 specialties, paid $2k+ vs unpaid (aggregate):** Nurse Practitioner 2.93% vs 3.17%. Physician Assistant 4.28% vs 5.12%. Internal Medicine 2.06% vs 2.30%. Family Practice 2.77% vs 2.69%. Dentist 8.93% vs 5.64%. Four of five flat or lower.

**Verdict on the first pass:** direction reproduces, size does not. "Much higher" is a mean-of-ratios artefact plus specialty mix. Not a story.

**2. Opioid-maker money, 2024 — the actual story**

| | unpaid | paid, no opioid brand | paid by an opioid maker |
|---|---|---|---|
| prescribers | 682,081 | 728,325 | **6,477** |
| opioid share of claims (aggregate) | 3.09% | 2.93% | **38.71%** |
| mean of rates | 5.1 | 6.6 | **39.5** |
| median rate | 0.0 | 0.0 | **46.7** |
| share at 10%+ opioid | 11.3% | 13.7% | **75.4%** |
| **standardised to the opioid-maker group's specialty mix** (claim-weighted, 60 specialties) | **15.82%** | **17.39%** | 38.71% |
| median claims | 136 | 367 | **2,267** |
| median opioid-brand $ | — | $0 | **$55** |

- **The fair comparator is the matched-specialty one.** Raw, 38.7% vs 3.1% reads as 12x. Give the unpaid the opioid-maker group's specialty mix and they write 15.8%; the paid-by-others 17.4%. The honest gap is **2.4x**, and it is not spread evenly:

| specialty (aggregate opioid share) | unpaid | paid, no opioid brand | paid by opioid maker | ratio vs unpaid |
|---|---|---|---|---|
| Nurse Practitioner (n=2,142 on the list) | 3.2 | 2.6 | **41.4** | **13x** |
| Physician Assistant (1,240) | 5.1 | 4.4 | **44.5** | **8.7x** |
| Family Practice (320) | 2.7 | 2.7 | 9.9 | 3.7x |
| Internal Medicine (219) | 2.3 | 2.1 | 6.2 | 2.7x |
| Physical Medicine & Rehab (518) | 22.9 | 30.6 | 54.7 | 2.4x |
| Anesthesiology (559) | 39.8 | 46.5 | 56.1 | 1.4x |
| Pain Management (625) | 46.5 | 49.7 | 56.5 | 1.2x |
| Interventional Pain (430) | 48.3 | 52.7 | 59.5 | 1.2x |

  Plainly: **the effect is carried by nurse practitioners and physician assistants.** Pain doctors on the list write 1.2x their unpaid peers, who already write about half their scripts as opioids. Dentist: only 2 took opioid-brand money, no comparison.
- **Who pays:** Collegium Pharmaceutical (Belbuca, Xtampza) — 36,839 payments to 6,454 NPIs, $607,920, median $17, 99.98% food and beverage. Protega (RoxyBond) 691 NPIs, $35,926. Everyone else under 120 NPIs. This is one company's rep call list.
- **Dose response inside the 6,477, fifths by opioid-brand dollars:** Q1 (median $17, 1 payment) 24.8% → Q2 ($30) 27.8% → Q3 ($55) 39.2% → Q4 ($107) 45.3% → Q5 ($219, 14 payments) 52.7%. Monotonic.
- **Sized:** 0.46% of prescribers write 8,836,497 Medicare opioid claims. Against the 59,133,014 unsuppressed opioid claims that is 14.9%; fill every suppressed blank with 10 and the denominator grows to 62,637,174, so the share is **14.1% to 14.9%**.

**3. Persistence — earlier money, same prescribers**

Payments made in 2022 and 2023 against the same 2024 prescribing:

| payment year | paid by opioid maker (n) | their 2024 opioid share | paid by others | unpaid |
|---|---|---|---|---|
| 2022 (Kowa's Seglentis dominated: 14,914 NPIs) | 19,060 | 11.6% | 2.94% | 3.17% |
| 2023 | 17,399 | 15.7% | 2.87% | 3.13% |
| 2024 (Collegium) | 6,477 | 38.7% | 2.93% | 3.09% |

Different company, different year, same kind of prescriber. The 2022 group is diluted because Kowa's Seglentis (tramadol + celecoxib) was pitched broadly, including to dentists.

---

## What a hit means, what a miss means

- **Hit (what we got):** prescribers an opioid maker chooses to buy lunch for already write 12x the raw opioid share of everyone else — 2.4x once specialty mix is matched, and that 2.4x lives almost entirely in nurse practitioners (13x) and physician assistants (8.7x) — and the ones bought more lunches write more still. That is a rep targeting the heaviest writers of their drug. It is exactly what a sales force is supposed to do, and it is a public list of the 6,477 heaviest opioid prescribers in Medicare with a company's name next to each.
- **Miss (what we did NOT get):** money in general buying opioid prescriptions. $17 to $1,400 a year from all of industry moves the opioid share from 3.1% to 3.7%. No purchase visible.
- **Causation is not shown and cannot be from here.** Part D is one year; there is no before. The 2022/2023 rows show ordering (payment before the measured prescribing) but prescribing is sticky, so ordering proves nothing. Frame: **targeting.** The money finds the prescribers; the data cannot say it changes them.

---

## What a skeptic would attack, and the answer

| Attack | Answer |
|---|---|
| Mean of ratios is dominated by tiny-volume prescribers (a surgeon with 47 claims at 31%). | Every headline number is the **aggregate** (sum/sum). Mean and median shown beside it; all three agree on the opioid-maker gap, and all three disagree on the all-money gap — which is the point. |
| It's specialty mix — pain doctors get pain-drug lunches. | Partly, and it is now in the numbers: standardised to the opioid-maker group's mix the unpaid write 15.8%, not 3.1%, so the gap is 2.4x. Pain specialists on the list write only 1.2x their unpaid peers. What survives is NPs (41.4% vs 3.2%) and PAs (44.5% vs 5.1%). |
| CMS suppression: `OPIOID_TOT_CLMS` is blank on 350,416 rows (24.7%). Blanks are 1–10 claims, not zero. | Bounded: fill every blank with 1 or with 10. Opioid-maker group 38.72% → 38.73% (only 4.7% of them are blank). Unpaid 3.12% → 3.41%. Nothing rides the blanks. |
| Brand regex catches non-opioids or addiction drugs. | The first version carried bare generics including BUPRENORPHINE, which would catch Suboxone/Sublocade generic strings; it hit 1 NPI in PY2024 by luck. Regex tightened to the brand list only (queries.py, noted at the top) and everything re-run: 6,477 NPIs, 38.71%, identical. Matched names eyeballed: Belbuca 4,529 NPIs, Xtampza 4,028, RoxyBond 691, Nucynta 194, Dsuvia 121, Olinvyk 41, then single digits. |
| Year misalignment. | Both sides data year 2024. The 2022/2023 payment years are shown as a separate persistence check, labelled as such. |
| NPI join fan-out. | Part D NPI unique (1,416,883 = 1,416,883). Payments aggregated per NPI before the join. Teaching-hospital rows excluded. |
| Part D is Medicare only; the lunch is about all patients. | True and unavoidable. Medicare is the only public per-prescriber opioid rate. Stated in the story. |
| 6,477 is tiny. | It writes 14.1% to 14.9% of Medicare's opioid claims. Tiny on people, not on pills. |
| The first pass said "two years." | It is one year of Part D. Three of Open Payments (2022, 2023, 2024). The undated Open Payments table is PY2024. |

---

## What changed vs the first pass

- "Paid prescribers write much more opioids" → **any** money: 3.1% → 3.6%, half of it specialty mix, flat across money deciles. Not the story.
- The story is **who pays**: 6,477 prescribers on an opioid maker's lunch list (6,454 of them Collegium's) at 38.7% opioids vs 3.1% raw, 15.8% once the unpaid are given the same specialty mix — 2.4x, carried by NPs and PAs, with a dose-response, writing 14.1% to 14.9% of Medicare's opioid claims.
- Framed as **targeting**: reps find the heaviest writers; $17 lunches are the footprint, not the cause.

## Traps found

- **`HEALTH__FED_CMS_PART_D_PRESCRIBERS` is data year 2024, not 2022.** `traps.md` says "Part D prescriber-drug ... DY22" — that is the by-drug table (`FED_CMS_PARTD_PRESCRIBER_DRUG`, run 431c13fc, URL `..._DY22_NPIBN.csv`). The by-provider summary landed 2026-06-26 from the generic CMS page URL (run 3c2495ce, no DY in the ingest log); the registry note pins it to DY2024. Two Part D tables, two years — never join them as one vintage.
- **`OPIOID_TOT_CLMS` blank ≠ zero.** '0' is a real zero (608,000 rows). '' is a suppressed 1–10 (350,416 rows). `OPIOID_PRSCRBR_RATE` is null on exactly the blank rows. Any "share with zero opioids" that counts blanks as zero overstates by 58%.
- **The undated `FED_CMS_OPEN_PAYMENTS` is program year 2024**, sitting beside `_2022` and `_2023`. Not a union, not "all years."
- **The Open Payments mart drops the product columns.** `NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1..5` and `PRODUCT_CATEGORY_OR_THERAPEUTIC_AREA_1..5` exist only in LANDING. Any "which drug was this payment for" question has to go to landing.

## Cost

51 queries through the Python door, all under 10 seconds; the heavy ones scan one Open Payments year (13–15M rows) with a regex over five name columns, then join to 1.4M Part D rows. No prior run of this pattern in the query log to price against.

---

STATUS: confirmed but reframed
HEADLINE: 6,477 prescribers on an opioid maker's lunch list write 38.7% of their Medicare scripts as opioids vs 3.1% unpaid, 15.8% once you match their specialty mix (2.4x, carried by NPs and PAs) — 0.46% of prescribers, 14.1% to 14.9% of Medicare opioid claims — while industry money in general moves it only 3.1% to 3.6%.
