# E57 — Do the top Medicare billers also take the most industry money?

**Short answer:** yes, at about twice the rate of their peers, in nearly every specialty. But the money is consulting and speaking fees, not royalties. Royalties are an orthopedics story, and orthopedics is where the dollars are.

## What was checked

- **Part B** = Medicare's bill for clinician services (visits, procedures, office-given drugs). Table: `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER`, 1,235,757 individual clinicians (ENT_CD='I'), one snapshot, data year 2024. NPI = the 10-digit national clinician ID. Every row is one NPI, none blank, none `0000000000`.
- **Open Payments** = the federal register of what drug and device companies give clinicians. Table: `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS`, program year 2024 on 100% of 15,385,047 rows, $3.31B. 48,059 rows carry an empty-string NPI (hospitals, mostly); dropped. $2.64B left, 979,136 NPIs.
- **Year-aligned.** Part B DY2024 against Open Payments PY2024. Neither query filters PROGRAM_YEAR; the mart is 100% PY2024 today, and that breaks the day a second year lands (noted in queries.py).
- **The rank.** Each clinician gets two deciles inside their own specialty (RNDRNG_PRVDR_TYPE, 103 values): allowed charges, and industry dollars. "Top payee" also requires money > 0, because 15,902 clinicians with $0 land in decile 10 by construction in specialties where almost nobody gets paid.

## The numbers

| Measure | Number |
|---|---|
| Top-decile billers | 123,529 |
| Also top-decile payees, money > 0 | **22,342 = 18.1%** |
| Lower-decile peers who are top payees | 85,285 of 1,112,228 = **7.7%** (9.1% if the $0 artifact is left in) |
| Ratio | **2.4x** (2.0x on the first-pass definition) |
| Both-top industry money PY2024 | **$356.1M** |
| ...of which royalty | $69.0M = **19%**, to 369 people |
| ...consulting, speaking, honoraria | $187.3M = **53%** |
| ...food, travel, education, gifts | $75.5M = 21% |
| ...other (acquisitions, grants, debt forgiveness) | $24.3M = 7% |
| Research payments | **not in the warehouse.** CMS ships them as a separate file; only general payments are landed. Zero by absence. |

**Rebuilt a different way:** percent_rank >= 0.9 instead of ntile(10), money > 0. Top billers 123,621, both-top 22,373, rate 18.1%. Reproduces.

**The gradient, not just the top.** Share in the top money decile by billing decile: 4.7%, 5.5%, 5.9%, 6.4%, 6.9%, 7.7%, 8.8%, 10.3%, 12.8%, **18.1%**. Every step up.

**Two knock-out tests, both survived:**
- Remove royalties from the money measure entirely: both-top goes 22,342 to 22,298. The overlap is not royalties.
- Rank billing on non-drug allowed charges only (MED_MDCR_ALOWD_AMT): both-top 20,724 of 123,529 = 16.8%, peers 7.8%. Still 2.1x. Drug buy-and-bill inflates it a little, does not make it.

## Royalty vs general vs research — the reframe

The first pass said "79% of overlap dollars are royalties." That number does not reproduce on this table and its method is not recorded. Across all both-top clinicians the royalty share is 19%, and the clinician-level file-wide share is 18%. Both-top money looks like everybody's money, just more of it.

| Cohort | People | Dollars | Royalty | Services | Hospitality |
|---|---|---|---|---|---|
| Every NPI in Open Payments | 979,136 | $2,638M | 18% | 46% | 26% |
| Part B billers, deciles 1-9 | 1,112,228 | $1,484M | 15% | 48% | 29% |
| Part B top-decile billers | 123,529 | $388M | 18% | 49% | 26% |
| Both-top | 22,342 | $356M | 19% | 53% | 21% |

Skew inside both-top: median clinician $1,902. Top 10 people hold $26.2M, top 100 $84.4M, top 1,000 $223.3M (63%).

## By specialty (200+ top billers, 53 specialties)

- 45 of 53: top billers ahead of peers.
- 7 are therapy and counseling fields where nobody gets paid: 0.0% both sides.
- **1 real reversal: Medical Oncology, 8.2% vs 10.2%.** Its top billers are ranked on drug pass-through cost; industry money does not follow the biggest drug bill.

| Specialty | Top billers | Both-top | Rate | Peers | Both-top $ | Royalty share |
|---|---|---|---|---|---|---|
| Anesthesiology | 4,108 | 1,525 | **37.1%** | 7.0% | $5.4M | 2% |
| Critical Care | 503 | 164 | 32.6% | 7.5% | $1.6M | 0% |
| Neurosurgery | 514 | 149 | 29.0% | 7.9% | $16.2M | 49% |
| Physician Assistant | 11,251 | 3,169 | 28.2% | 8.0% | $15.1M | 0% |
| Psychiatry | 1,977 | 546 | 27.6% | 8.0% | $14.0M | 0% |
| Internal Medicine | 9,362 | 2,538 | 27.1% | 8.1% | $14.2M | 1% |
| Family Practice | 8,363 | 2,188 | 26.2% | 8.2% | $11.0M | 0% |
| Neurology | 1,658 | 413 | 24.9% | 8.3% | $21.8M | 0% |
| **Orthopedic Surgery** | 2,167 | 502 | 23.2% | 8.5% | **$84.9M** | **65%** |
| Nurse Practitioner | 20,321 | 3,120 | 15.4% | 9.4% | $13.2M | 0% |
| Diagnostic Radiology | 3,284 | 356 | 10.8% | 9.9% | $4.0M | 3% |

Orthopedics is 2% of both-top people and 24% of both-top dollars. Neurosurgery is the only other specialty where royalties matter. Everywhere else the money is consulting, speaking and meals.

## The named ten

Each NPI checked: one Open Payments profile ID, one Part B row, no name collisions.

**Top 10 both-top by industry money (PY2024, allowed charges beside it):**

| Clinician | Specialty, state | Industry $ | Kind | Top payer | Medicare allowed |
|---|---|---|---|---|---|
| Mark Frankle | Ortho, FL | $7,333,021 | $6.95M royalty | Encore Medical | $370,724 |
| Alexander Frank | Family Practice, OK | $3,082,225 | debt forgiveness | Skye Orthobiologics | $289,402 |
| Patrick Denard | Ortho, OR | $2,500,389 | $2.02M royalty | Arthrex | $429,801 |
| Reuben Gobezie | Ortho, OH | $2,341,674 | $2.25M royalty | Arthrex | $376,767 |
| William Hamilton | Ortho, VA | $1,973,382 | $1.88M royalty | DePuy Synthes | $608,863 |
| Gary Gelbfish | Vascular Surgery, NY | $1,928,678 | acquisition | Stryker | $1,906,232 |
| Jonathan Yerasimides | Ortho, KY | $1,925,722 | $1.68M royalty | Zimmer Biomet | $526,226 |
| Adolph Lombardi | Ortho, OH | $1,880,954 | $1.13M royalty | Zimmer Biomet | $598,919 |
| Richard Hynes | Ortho, FL | $1,603,505 | $1.51M royalty | Medtronic | $571,655 |
| John Dearborn | Ortho, CA | $1,599,852 | $1.60M royalty | Zimmer Biomet | $1,650,137 |

- Frank's $3.08M is a bad-debt write-off, not a cheque — already worked in `reports/molina_debt_forgiveness_2026-09-05.md`. Gelbfish's is Stryker buying his company. Neither is "industry pays the doctor" in the hunch's sense.
- Seven of the eight royalty surgeons bill Medicare under $610k. They are top-decile for orthopedics, not national outliers. The royalty runs from about equal to their Medicare book (Dearborn, Lombardi) to 19x it (Frankle).

**Top 10 both-top by Medicare billing:** the other end of the cohort, and a different story. Ravi Kapadia, General Surgery, CA: $97.1M allowed, 99.7% of it drug, $29,753 industry money, top payer Organogenesis (skin substitutes, hunch E40). Jack Azad $31.5M, Thomas Rambacher $28.6M, David Warrow $25.8M, John Storheim $24.3M — all under $60k in industry money, mostly meals. Both-top clinicians run 39.8% drug in their allowed charges against 10.2% for everyone else.

**Top 10 by both measures at once** (rank product of national ranks): Kapadia (#3 allowed, #10,420 money), Khanani, Wykoff and Dhoot (retina, $300-400k consulting each, $7-10M drug billing), Frankle (#5 money, #39,721 allowed). Nobody is top-100 on both. Volume and money are two different populations that overlap at the decile, not at the summit.

## What a hit means, what a miss means

- **Hit (this):** the clinicians Medicare pays the most inside a specialty are the ones companies pay the most, ~2.4x their peers, on every rung of the ladder, with or without royalties, with or without drug cost. That is the red flag the hunch asked for: volume and money move together.
- **Blind spot on the peer rate:** 7.7% is the rate among lower-decile *Medicare-billing* peers, not among all clinicians in Open Payments. Clinicians who never bill Part B are not in the denominator at all.
- **What it does not say:** direction. One Part B year, no before/after. Companies may pay the busy ones because they are busy (key opinion leaders), or the paid ones may get busy. This table cannot tell.
- **Miss would have been:** a flat gradient, or top billers no more likely than peers. Not what the warehouse shows.

## What a skeptic would attack

1. *"18% vs 10% is an ntile artifact."* Answered: peers with real money are 7.7%, the percent_rank rebuild gives 18.1%, and the gradient runs through all ten deciles.
2. *"It's the royalty surgeons."* Answered: royalties removed, 22,298 vs 22,342.
3. *"It's oncologists buying drugs."* Answered: non-drug billing, 16.8% vs 7.8%. And Medical Oncology is the one specialty that reverses.
4. *"General payments only."* True. Research payments and ownership interest are not landed. Both-top dollars are a floor.
5. *"One billing year."* True. No trend, no direction. Tier stays where the first pass left it.
6. *"Specialty labels differ between files."* Deciles use the Part B type only; Open Payments specialty is never joined on. The named ten agree on specialty in both files (Rambacher is Podiatry in Part B, General Practice in Open Payments; Mattar and Birhiray Hem-Onc vs Internal Medicine — same people, coarser label).

## Traps

- **Ruled out:** `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID` on the landing twin is an id: 1,730 distinct values, range 100000000053 to 100001451204, and summing it reads $1.54 quintillion. The mart drops the column; the mart money column `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS` (FLOAT) sums to $3,313,801,737.39, matching `try_to_number` on landing to the cent.
- **New:** dropping the 48,059 blank-NPI rows removes $361.2M of royalty — 43% of the file's $846.8M royalty dollars, more than any other nature (services loses $120M, other $184M, hospitality $10M). Every royalty share in this report is clinician-level only; the file-level royalty share is higher.
- **New:** Open Payments "Debt forgiveness" and "Acquisitions" rank people into the top money decile with no cheque ever cut. 413 acquisition rows carry $213M, 7,687 debt-forgiveness rows $40.8M. Any top-payee list needs the nature split before a name goes on it, or a write-off reads as a payment.
- **Reconfirmed:** blank NPI is an empty string, not null (48,059 rows in PY2024). `ntile(10)` on a mostly-zero money column manufactures a top decile of zeros (15,902 here).

STATUS: confirmed but reframed
HEADLINE: 18.1% of top-decile Medicare Part B billers are also top-decile industry payees vs 7.7% of peers (2.4x, 22,342 clinicians, $356.1M PY2024) — but only 19% of that money is royalty; it is 53% consulting and speaking, and the royalty story is orthopedics ($84.9M, 65% royalty).
