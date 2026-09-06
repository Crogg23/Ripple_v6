# E38 — Are drug and device companies still paying Medicare opt-out doctors?

**Terms, once.** NPI = the ten-digit National Provider Identifier every clinician has. Opt-out = a clinician filed an affidavit saying they bill no Medicare at all. Open Payments = the federal ledger of every dollar, meal and royalty a drug/device company gives a clinician. PY = Open Payments program year.

## The first pass: $70.8M in PY2023

**What was checked.** Rebuilt three ways against `HEALTH__FED_CMS_OPEN_PAYMENTS_2023` (14.7M rows) x `HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS` (57,209 rows, 56,455 NPIs).

| Cohort rule for PY2023 | Dollars | People paid |
|---|---|---|
| Anyone on today's roster | $92.5M | 11,779 |
| Opted out on or before the payment date | **$70.78M** | — |
| Opted out before 2023-01-01 (fixed cohort) | $68.9M | 8,301 |
| Naive raw-row join (affidavit dupes) | $95.6M | — |

**Hit.** $70.8M reproduces exactly as "opted out on or before the day of payment." The first pass was time-correct. It was not wrong; it was one year with no context.

## The deepened version: same 27,547 clinicians, three years

**What was checked.** Froze the cohort to NPIs whose earliest OPTOUT_EFFECTIVE_DATE is before 2023-01-01. Joined to PY2022 (`_2022`), PY2023 (`_2023`) and PY2024 (the bare `HEALTH__FED_CMS_OPEN_PAYMENTS` table, which holds PROGRAM_YEAR 2024 only, zero RECORD_ID overlap with the other two).

| PY | Dollars | People paid | Payers | Median payment |
|---|---|---|---|---|
| 2022 | $88.3M | 8,198 | 698 | $20 |
| 2023 | $68.9M | 8,301 | 696 | $22 |
| 2024 | $59.0M | 7,821 | 672 | $23 |

Three-year total **$216.2M**. Fell 13% on recurring money ($67.6M → $67.0M → $58.9M without the Acquisitions nature), 33% counting the one-time 2022 buyout. Same people. Loose cohort (anyone on roster) falls too: $154.6M → $92.5M → $78.6M — so the "roster growth inflates the trend" worry runs the other way here; the roster's newcomers (therapists) bring no money.

**What moved.** Nature of payment, fixed cohort:

| Kind | 2022 | 2023 | 2024 |
|---|---|---|---|
| Royalties & licenses | $46.0M | $42.6M | $34.8M |
| Acquisitions | $20.7M | $1.9M | $0.1M |
| Speaking, consulting, honoraria | $16.8M | $18.8M | $18.3M |
| Meals, travel, gifts, other | $4.8M | $5.6M | $5.9M |

The drop is royalties plus one $20.7M acquisition year. Everyday industry money (talks, consulting, meals) is flat.

**Top 10 payers, pooled, names case-folded.** AbbVie $51.6M (of which $41.1M is royalties to one TN plastic surgeon, opted out since 2017; the rest is $3.5M/yr of psychiatry talks and meals to 2,600 people). Arthrex $30.8M to 40 people. Smith+Nephew $25.7M to 96. DePuy Synthes $15.1M to 12. Stryker $8.6M. Zimmer Biomet $7.6M. Medtronic $5.3M. ZimVie $2.8M (dental implants, 1,390 people). Merit Medical $2.6M to 2 people. Axsome $2.5M (drug, meals and talks, 628 psychiatrists).

**Specialty (affidavit label).** Orthopedic surgery: 242 in cohort, 173 paid, $101.2M. Plastic surgery: 324 in cohort, $44.1M. Psychiatry: 4,014 in cohort, $20.7M. Oral surgery + dentists: 7,415 in cohort, $13.6M. Therapists (psychologists, counselors, social workers, MFTs): 7,830 in cohort, effectively zero. 607 ortho/plastic/neurosurgeons = 2% of the cohort, 69% of the money.

**Concentration.** 11,263 of 27,547 (41%) got anything in three years; 5,089 got something all three years. Median recipient: $251 over three years; 3,355 got under $100. Top 10 people: $113.8M (53%). Top 100: $182.1M (84%). Top 1: $41.1M (19%).

## What a hit means / what a miss means
- A hit (money flows to opted-out clinicians): confirmed, $59-88M a year. But the mechanism is patents and royalties to a hundred surgeons, plus speaker fees to psychiatrists. Opting out of Medicare and holding a device patent are unrelated facts about the same person. There is no "industry keeps them on the hook after they leave Medicare" story in the data — the money predates and outlasts the opt-out.
- A miss would have been: money to the fixed cohort near zero or rising sharply after opt-out. Neither.

## What a skeptic would attack, and the answer
- **"The roster is a current snapshot."** True. Every end date is 2026-06-30 or later. Anyone who opted out before 2023 and later re-enrolled is gone. The cohort is survivors; it cannot inflate the numbers, it can only miss ex-opt-outs. OPTOUT_EFFECTIVE_DATE runs 1998-2026 while end dates are all 2026-2028, so effective date is the original opt-out, not the latest renewal — the pre-2023 cut is real.
- **"Affidavit rows duplicate."** 57,209 rows, 56,455 NPIs (address changes). Cohort is built with one row per NPI; the naive join over-counts by $3.1M in PY2023.
- **"NPI in Open Payments has junk."** 44,233 of 14.7M PY2023 rows have a non-10-char NPI (blanks/sentinels). Cohort NPIs are all 10 chars, so they cannot match junk.
- **"The PAYMENT_ID column is money."** Not touched. Only TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS (FLOAT) was summed.
- **"Payer names split."** Yes: 'ABBVIE INC.' and 'AbbVie Inc.' — folded with upper + strip punctuation. Only AbbVie had two spellings in the top 12.
- **"Roster specialty is stale."** Cross-checked PY2023 against Open Payments' own COVERED_RECIPIENT_SPECIALTY_1: ortho → Orthopaedic Surgery and its sub-specialties, plastics → Plastic Surgery, psychiatry → Psychiatry. One outlier: a roster 'Otolaryngology' NPI that Open Payments tags Pediatrics ($1.1M). Not material.
- **"Opted out before 2023 is not opted out for all of PY2022."** Right: 2,389 of the 27,547 (9%) have an effective date inside 2022, and $1.6M of the PY2022 total landed before the person's own opt-out date. The cohort rule is 'opted out before 2023', not 'opted out for all three years'; PY2023 and PY2024 are fully clean, PY2022 is $1.6M (1.8%) soft.
- **"Three years is not a trend."** Agreed; it is what the warehouse holds (PY2022-2024). Says so on the chart.

## Traps found
- Payer name column carries mixed-case duplicates of the same company ('ABBVIE INC.' / 'AbbVie Inc.'); raw group-by splits the top payer. Fold before ranking.
- The bare `HEALTH__FED_CMS_OPEN_PAYMENTS` mart is PY2024 only, not a multi-year table; `_2022` and `_2023` are separate tables with zero RECORD_ID overlap. A "trend" needs a UNION of three tables.
- The opt-out affidavit file is a live snapshot with 754 duplicate NPI rows (address changes) and no history of lapsed opt-outs.

STATUS: confirmed but reframed
HEADLINE: $216M in industry money reached 27,547 clinicians who had opted out of Medicare before 2023, PY2022-24 — but 53% went to ten surgeons' royalties, the total fell 13% on recurring money (33% counting a one-time 2022 buyout), and the median recipient got $251.
