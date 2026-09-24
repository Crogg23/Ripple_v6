# Deep 5: five health tables, coverage deep pass

2026-09-24. Python door, query tag `coverage-b-2026-09-24`. **29 of 35 SELECT/WITH statements used.** Two of them failed to compile and were rerun. The SQL is in `deep-5.sql`.

Every person or company named below is **a data match, not verified against primary records**.

## The menu

| Table | Verdict | The number that matters |
|---|---|---|
| HOME_HEALTH_OWNERS | **live** | 54 home health owners (5%+ stakes) share a first name, last name and state with someone on the OIG exclusion list. Chance predicts 20.8. After dropping middle-initial conflicts, 44 people are left, and 54 of their 55 agencies are still on Care Compare. |
| NURSING_HOME_FIRE_DEFICIENCIES | probed | Chains land 1.0x their own states at the median and 1.95x at worst. CareCore (OH), Aperion (IL/IN) and Eden repeat the same fire tag in all 3 inspection cycles at 1.8-2.5x their states. Nearly all of it is sprinkler and alarm upkeep. |
| MEDICARE_DIALYSIS_FACILITIES | probed | Against their own states in 2024, DaVita's deaths run 1.021x expected, Fresenius 0.965x and independents 1.102x. That gap is about 6%, and it's known. |
| NADAC | probed | 2024 holds only 20 step-ups of 3x or more in generic prices, across 7 drug groups, and 3 of those are OTC. The 2022-23 prices were never loaded. |
| INPATIENT_BY_PROVIDER_AND_SERVICE | probed | High-charge hospitals bill up to 4.4x their state's median, but Medicare pays them 0.8-1.2x. The high-payment hospitals are public safety-net hospitals, which is what the payment formula predicts. This is the 2013 story. |

---

## 1. HEALTH__FED_CMS_HOME_HEALTH_OWNERS: **live**

**Headline:** People with a 5%+ stake in Medicare home health agencies match the OIG exclusion list by name and state 2.6x more often than chance predicts. The matches sit in FL, TX and new CA agencies.

**Shape**

| Fact | Value |
|---|---|
| Rows | 101,188. One owner role at one agency enrollment, all from one load run |
| Agencies | 10,203 associate IDs, 11,494 enrollments, 11,224 CCNs |
| Owners | 31,847 owner IDs. 79,880 rows are people, 21,308 are companies |
| CCN filled | **99,287 of 101,188 (98%)**. The triage line "85.6K null CCN" misread the facts row: 85.6K was a sum of ownership percents, not a count of rows |

**Checked**
1. Counted distinct agencies per owner ID, limited to 5%+ ownership roles (codes 34 and 35), and took the top 25 people and top 25 companies.
2. For each state, counted the share of agencies with a 5%+ individual owner who holds 3 or more agencies nationally.
3. Joined owners to the OIG exclusion list (`HEALTH__FED_HHS_OIG_LEIE`) on first name, last name and state. Also tried company name plus state, and the agency's own NPI.
4. Built a chance baseline. For owners whose name is anywhere on the list, how many hits land in the same state, against that state's share of the list?
5. Looked up the matched agencies on Care Compare (`HEALTH__FED_CMS_HOME_HEALTH`): are they still listed, and how do their stars and spend compare with their state?

**What came back**

| Check | Number | Denominator |
|---|---|---|
| 5%+ individual owners, counted once per state | 11,611 | all people with ownership roles 34 or 35 |
| Name on the exclusion list, any state | 349 | 11,611 |
| **Name on the list in the same state** | **54** | 349. Chance predicts **20.8** from where the list's people live |
| TX / FL / CA same-state hits | 15 / 17 / 15 | chance predicts 6.0 / 5.1 / 5.6 |
| After dropping middle-initial conflicts | 44 people, 50 person-exclusion rows, 55 agencies | |
| Exclusion dated before the person's latest ownership date | 33 rows (FL 12, CA 11, TX 8) | 50 |
| Agencies still on Care Compare | 54 | 55 |
| CA agencies certified 2023 or later with a matched owner | 12 | 941 new CA agencies (1.3%). The rate across all agencies nationally is 54 of 12,392 (0.44%) |
| FL matched agencies in the top 1% for Medicare spend per episode | 3 (1.31-1.35x the national spend; 4, 6 and 11 FL agencies spend more) | 1,134 FL agencies |

The **CA cluster** is people whose exclusion predates their ownership listing. All of these agencies are LA-area, and most were certified 2023-25:

| Person (data match) | Agencies | Listed as owner | Excluded | OIG category |
|---|---|---|---|---|
| Artur Harutyunyan | Welfare HH, Perfect HH | 2020, 2023 | 2014, 1128a1 | individual |
| Anna Gasparyan | Monarch HH, Safe Choice HH | 2021, 2022 | 2003, 1128a1 | DME company |
| Kristine Arutyunyan | Holy Light and May Light (owner); Restorative HH (managing employee, 2026-04) | 2021-2026 | 2024-01, 1128a1 | business owner/exec |
| Liana Karapetyan | Direct Care HH | 2024-06 | 2023-04, 1128a1 | business owner/exec |
| Anahit Hovhannisyan | Exact HH | 2024-04 | 2014, 1128a1 | business owner/exec |
| Marine Danielyan | Max Care HH | 2022 | 2014, 1128a1 | individual |

One more case is outside the date rule. Arman Danielian was excluded 2026-01 (1128a3) and is still listed as owner of Vita, Valeo and Arva HH. He picked up Arva 2025-12.

**Other things the owner file shows**
- The biggest owners are the known chains: UnitedHealth (355 agencies), LHC (297), Humana/CenterWell (78-82), Amedisys (66), Enhabit (65).
- The biggest individual owners: Angela W and Mark A Eddins (41 and 39 agencies in 11 states), David Jackson (36, of which 19 are in TX), Sam D Kassab (19, of which 11 are in CA).
- **No LA/Houston cluster shows up by owner ID.** Nationally, 3.4% of agencies have an individual owner who holds 3+ agencies. CA is 4.9%, TX 4.0%, CO 6.4%, OK 6.3%. That cluster doesn't show by owner ID. If it's there, it shows through the exclusion list.
- **Hospice owners can't be tested.** LANDING holds `FED_CMS_HOSPICE` and `FED_CMS_HOSPICE_ENROLLMENTS` but no hospice owner file.

**If it's a hit:** CMS's own current owner file lists people the OIG barred from federal health programs, and the agencies are still enrolled. That breaks CMS's enrollment rules. It's a named, checkable story that runs through the LA new-agency boom: CA holds 941 of the 1,606 agencies certified nationally since 2023.

**If it's a miss:** the matches are name collisions. The exclusion list stores no birth date, and 1128a1 people have no NPI, so name plus state is the whole join.

**The boring explanation, not ruled out:**
- **Names cluster by place.** Armenian surnames cluster in LA, and Hispanic names in FL and TX. That pushes same-state collisions above the 20.8 baseline, so the real excess is smaller than 54 minus 20.8.
- **The second field fails.** Only 9 of 141 rows have the exclusion list's city matching the agency's city. The list keeps the address from the time of exclusion, and several of those addresses are prison towns (Coleman FL and Beaumont TX host federal prisons). That makes city useless as a check.
- **Next step:** pull the court record for each CA and FL row. Case number, defendant age and the named business will confirm or kill each one.

---

## 2. HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES: probed

**Headline:** Aperion Care (IL/IN, 33 homes), CareCore Health (OH, 12 homes) and Eden Senior Care (WI/MN/PA, 19 homes) draw 1.6-2x the fire citations of the other homes in their own states. They are cited for the same tag in all three inspection cycles at 1.8-2.5x their states' rate.

**Shape:** 200,030 rows. **That isn't a cap:** every row is a unique home, date and tag.
- 13,914 homes, and every CCN is in `HEALTH__FED_CMS_NURSING_HOME`.
- 3 inspection cycles, with surveys dated 2016-07 to 2026-05.
- Only **215 rows (0.1%)** are severity G or worse.

**Checked**
1. Joined each CCN to the nursing home file's `CHAIN_NAME` and counted citations per home for chains with 10+ homes. Zero-citation homes are in the denominator.
2. Built an expected count for each chain from the state average of every home it owns. That washes out how hard each state inspects.
3. Did the same for widespread citations (F or worse) and for the core life-safety tags: sprinklers K0351/K0353, smoke barriers K0372/K0374, generator K0918.
4. Counted homes cited for the same tag in all 3 cycles, against the expected rate for their states.

| Chain | Homes | States | Citations vs own states | Homes repeating a tag all 3 cycles | Repeats vs own states |
|---|---|---|---|---|---|
| CareCore Health | 12 | OH | 1.95x | 11 of 12 | 2.54x |
| Bria Health Services | 15 | IL | 1.79x | n/a | n/a |
| Aperion Care | 33 | IL, IN | 1.76x | 22 of 33 | 1.83x |
| Eden Senior Care | 19 | WI, MN, PA | 1.62x | 16 of 19 | 2.20x |
| Journey Healthcare | 34 | GA, OH, WV, KY | 1.63x | 11 of 34 | 2.32x |
| Big chains: Ensign / PACS / Life Care / Genesis | 338 / 279 / 194 / 187 | many | 0.80 / 1.15 / 1.04 / 1.03 | n/a | n/a |

Across 301 chains (8,496 homes), the chain ratio has a median of 1.00, a 90th percentile of 1.43 and a max of 1.95. **22 chains sit at 1.5x or more.** Nationally, 27.4% of homes repeat a tag in all 3 cycles.

**If it's a hit:** a handful of mostly one-state chains let sprinkler and alarm testing lapse at home after home, cycle after cycle. Bria ties to F-029, the Illinois abuse-flag finding.

**If it's a miss:** it's noise. With 12-19 homes, a ratio of 2x is within reach of chance, and the spread is narrow.

**The boring explanation, partly ruled out:**
- State inspection intensity is controlled, because each chain is compared with its own states.
- **Not controlled:** the age of the building. Old buildings draw more K-tags.
- The top tags are K0353 (sprinkler inspection and testing) and K0345 (fire alarm testing): upkeep and paperwork, with 0-1 G+ citations per chain.
- Arcadia Care, the chain F-021 flagged as worst for fines, runs 1.06x here, so there's no tie to F-021.

---

## 3. HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES: probed

**Headline:** In 2024, measured against their own states, DaVita clinics recorded about 650 more deaths than CMS expected (1.021x). Fresenius recorded about 1,160 fewer (0.965x). Independent clinics ran worst, about 690 more (1.102x).

**Shape**
- 12,456,456 rows, 8,241 clinics, 2021-2024, 71 chains.
- There are **2,678 measure IDs**, and the ID carries the year (`smry4_f` is SMR for 2024).
- MEASURE_SCORE mixes counts, percents, ratios, p-values and ranks, so its sum means nothing.

**Checked**
1. Pivoted the 2024 measures for each clinic: deaths, expected deaths, SMR, SMR p-value, admissions, expected admissions, SHR and SHR p-value.
2. Pooled each chain as observed over expected. Then re-based it on each clinic's own state, using the pooled state ratio.
3. Flagged "worse" as ratio above 1 with p under 0.05.
4. Joined the infection ratio from the clinic file (`HEALTH__FED_CMS_DIALYSIS`), because this table has no bloodstream infection ratio for 2024.

| Chain (2024) | Clinics | Deaths / expected | SMR vs own states | Share significantly worse | SHR vs own states | Median SIR | Infection "worse" |
|---|---|---|---|---|---|---|---|
| DaVita | 2,822 | 31,545 / 31,231 | 1.021 | 2.9% | 1.020 | 0.25 | 0.2% |
| Fresenius | 2,775 | 32,050 / 33,223 | 0.965 | 2.3% | 0.971 | 0.26 | 0.3% |
| Independent | 717 | 7,481 / 6,964 | 1.102 | 5.3% | 1.047 | 0.43 | 2.0% |
| US Renal Care | 392 | 3,682 / 4,082 | 0.918 | 1.0% | 0.998 | 0.20 | 0.0% |
| DCI | 245 | 2,214 / 2,264 | 0.968 | 2.9% | 0.977 | 0.22 | 0.8% |

**If it's a hit:** DaVita runs about 6% above Fresenius on deaths and 5% on hospital admissions, for patients CMS has already risk-adjusted.

**If it's a miss:** the chains sit within a few percent of each other, and the flags are rare everywhere.

**The boring explanation:**
- The expected counts already adjust for patient mix.
- The gap is small. ProPublica covered chain quality in 2010.
- Independents are a grab bag of hospital-based and rural clinics.
- **Too small and too known to lead.**

---

## 4. HEALTH__FED_CMS_NADAC: probed

**Headline:** In 2024, generic drug prices halved 542 times and jumped 3x or more only 20 times. The real jumps: acetaminophen-codeine solution 30x, hydrocodone-APAP solution 5.6x, naproxen DR 375 mg 4.9x, and saxagliptin 5 mg 4.2x (then up to 4.9x a month later).

**Shape**
- 359,514 rows, 32,881 NDCs. Each row is one NDC at one effective date: a price change, not a weekly price.
- **Only the 52 weekly files of 2024 are loaded.**
- The pre-2024 effective dates are 26,600 rows across 26,587 NDCs: the starting price carried into 2024, one per NDC. **There is no 2022-23 series.**

**Checked**
1. For each NDC, compared each price with the one before it. Kept only generics (G) whose pricing unit didn't change between the two prices.
2. Counted step-ups and step-downs.
3. Grouped the jumps by drug and checked whether the next price fell back.

| Step between consecutive generic prices | Count | Denominator |
|---|---|---|
| Up 2x or more | 127 | 308,054 steps |
| Up 3x or more | 20 (7 drug groups, 3 of them OTC) | 308,054 |
| Down to half or less | 542 | 308,054 |

| Drug (Rx generic) | Old price per unit | New price per unit | Date | Held? |
|---|---|---|---|---|
| Acetaminophen-codeine 120-12 mg/5 mL solution | $0.0145 | $0.434 | 2024-04-17 | yes ($0.409 next) |
| Hydrocodone-APAP 7.5-325 mg/15 mL solution | $0.062 | $0.349 | 2024-04-10 | yes |
| Naproxen DR 375 mg tablet | $0.226 | $1.106 | 2024-12-18 | last price in the window |
| Saxagliptin 5 mg tablet | $1.354 | $5.621, then $6.674 | 2024-04-17 | rose again |
| Phenobarbital 16.2 mg tablet | $0.069 | $0.172 | 2024-06 | fell back to $0.105 |

**If it's a hit:** a few old generics repriced several-fold overnight.

**If it's a miss:** it's rare and small in dollars. One year of data can't show a trend.

**The boring explanation:**
- Makers leaving the market and shortages (methylphenidate shows up at 2x) explain most of it.
- Generic spikes were a big story in 2014-16.
- The 2022-23 window the angle wanted isn't in the warehouse. **That part stays unresolved, not empty.**

---

## 5. HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE: probed

**Headline:** Some hospitals bill 3-4x their state's median for the same DRG, but Medicare pays them about the median. The hospitals Medicare pays 2-5x the median are public safety-net hospitals (Parkland 5.07x, JPS 3.87x, Kings County 2.82x, Grady 2.31x).

**Shape**
- 145,879 rows: one per hospital and DRG, with no duplicates.
- 2,906 hospitals, 540 DRGs, at least 11 discharges per row (smaller counts are suppressed).
- 4,952,481 discharges. Medicare paid **$75.1B** (discharges times average payment). Hospitals billed $457.6B, which is 6.1x what Medicare paid.
- **The table has no year column.**

**Checked**
1. For each state and DRG with 5+ hospitals, took the median charge and median Medicare payment.
2. For each hospital with 20+ DRGs, took its median charge ratio and median payment ratio against those medians.
3. Summed the dollars above the median, weighted by discharges.

| List | Example | Median charge ratio | Median Medicare payment ratio | $ above state median |
|---|---|---|---|---|
| High charges | Capital Health Regional (NJ), 41 of 46 DRGs at 3x+ | 4.39 | 1.24 | $2.8M |
| High charges | Gadsden Regional (AL) | 3.51 | 0.97 | -$0.4M |
| High charges | CJW Medical Center (VA), 163 DRGs | 2.77 | 0.90 | -$11.7M |
| High payment | Parkland (TX) | 1.29 | **5.07** | $44.9M |
| High payment | Jackson Memorial (FL) | 0.81 | 2.03 | $50.6M |
| High payment | University Health System (TX) | 0.92 | 2.04 | $40.1M |

**If it's a hit:** Medicare pays some hospitals far more per case for the same DRG.

**If it's a miss:** charges are list prices that don't move Medicare payment. The data proves that here: the high-charge hospitals get paid 0.8-1.2x the median.

**The boring explanation, which fits the data:**
- The payment list is the safety-net list, which is exactly what the teaching, disproportionate-share and outlier add-ons predict. Per CMS's method notes, those add-ons are included in the payment column; that wasn't re-checked here.
- The charge gaps are the 2013 chargemaster story.

---

## Data traps found

1. **NADAC holds 2024 only.** Effective dates before 2024 are one carried-in starting price per NDC (26,600 rows), not history.
2. **A NADAC generic price is set for a whole drug group.** All NDCs in a group move by the same ratio, so "5 NDCs jumped" is one price change, not five makers confirming it.
3. **Home health owner CCN is 98% filled.** The "85.6K null CCN" in triage came from a sum of ownership percents.
4. **Exclusion-list city is the address at exclusion,** often a prison town. It can't serve as a second-field check on a name match.
5. **The dialysis measure ID carries the year** (`...4_f` is 2024). This table has no bloodstream infection ratio for 2024; use `STANDARD_INFECTION_RATIO` in `HEALTH__FED_CMS_DIALYSIS`.
6. **The inpatient by-provider-and-service table has no year column.** The data year can't be read from the table.
7. **No hospice owner file is landed.** "Do the same people own hospices?" needs a load first.

## Statement count

29 SELECT/WITH statements out of a budget of 35. [5] and [9] failed at compile because those tables have no `_SOURCE_RUN_ID` column; [11] and [12] reran them. Each connection also ran the two required session settings, which aren't counted.
