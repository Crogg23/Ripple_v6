# Deep pass 7: five tables, 2026-09-24

Chris's words: "no i want coverage first - basically a menu to choose from. Because im not going to spend time on something we found now if its trivial compared to what we could find - get me?"

Door: Python only. Tag `coverage-b-2026-09-24`. **24 SQL statements** (budget 35), plus 2 session-setup lines per connection. All SQL is in `deep-7.sql`, numbered [1] to [24].
Every person or company named below is a **data match, not verified against primary records**.

## The menu

| Table | Verdict | The one number |
|---|---|---|
| IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS | **live** | 231 LA County hospices sit 3 or more to a street address, and all 231 are still on Medicare's certified list. Plus a new lead: 12 hospices named "CFHC NO4" to "CFHC NO22" in San Antonio |
| JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS | probed | 379 judges were assigned 3,650 cases naming a bank they owed money to that year. The rules mostly allow it. The narrow thread: 68 district judges, 424 cases, where the loan was unusual (investment property, guaranty, $250K+) |
| HEALTH__PHARMA_MEAL_CAP_FINGERPRINT | probed | 2024: 47,607 meals at exactly $125.00 and 20,666 at $124.99, against 675 at $126.00. $125 is a common company meal limit, not a law. AbbVie ranks 156th of 502 makers |
| JUSTICE__FED_COURTLISTENER_DISCLOSURE_AGREEMENTS | probed | Only 26 judge-firm pairs, on 42 published opinions, show the judge's old firm as counsel in front of them in the years the agreement ran. Many are name collisions |
| HEALTH__NURSING_HOME_RELIEF_BY_CHAIN | **dead** | The worst chains did not get more. Per matched bed, 3.5-star-plus chains got $10,692 and chains under 2.5 stars got $8,193 |

---

## 1. Hospice enrollments: **live**

**Row count:** 6,066 enrollments, 6,056 distinct NPIs.

### Trap: "one NPI behind 45 enrollments" is false
- The facts file says NPIs 1013548734, 1447931134 and 1487748646 each hold 45 rows.
- In the mart, those three NPIs hold **1 row each** (3 in total). No NPI holds more than 2 rows, and only 10 hold 2 [11], [15].
- That lead is dead. Where facts.tsv got 45 is unexplained.

### What was checked
- I grouped every enrollment by street address (line 1 plus ZIP5) and counted how many hospices share each address [12].
- I split the country into metro areas by ZIP3. LA County is ZIP3 900-918 plus 935, which is a proxy.
- For each area I measured two things: the share incorporated in 2019 or later (denominator: rows with an incorporation date), and the share at a shared address (denominator: all enrollments in the area).

| Area | Enrollments | Incorporated 2019+ | At a shared address | 3+ per address | For-profit |
|---|---|---|---|---|---|
| **LA County** | 981 | **56.1%** (440 of 784) | **44.1%** | 231 | 98.9% |
| Las Vegas | 137 | 66.0% | 36.5% | 30 | 99.3% |
| Houston | 284 | 53.1% | 32.0% | 51 | 97.9% |
| Dallas | 181 | 31.7% | 26.0% | 13 | 95.6% |
| Phoenix | 129 | 53.6% | 20.2% | 12 | 96.1% |
| CA outside LA and San Diego | 485 | 34.2% | 9.1% | 10 | 85.6% |
| Atlanta | 134 | 40.2% | 9.0% | 0 | 93.3% |
| Chicago | 87 | 32.8% | 0.0% | 0 | 87.4% |
| Rest of US | 3,587 | 21.8% | 3.9% | 53 | 71.0% |

- LA holds **16% of every Medicare hospice in the file**.

### Still certified, still stacked [21]
- The 231 LA hospices at 3-plus addresses sit at 59 addresses. **All 231 CCNs are on the current certified list** (HEALTH__FED_CMS_HOSPICE). 206 of them were certified in 2019 or later.
- File age: the newest enrollment ID is O20260203, so this snapshot is from February 2026 or later.

### The addresses [15]

| Address | Hospices | What stands out |
|---|---|---|
| 14545 Friar St, Van Nuys | 9 | 9 suites, 9 owner IDs, all incorporated Mar 2019 to Feb 2021 |
| 12444 Victory Blvd, North Hollywood | 8 | 4 incorporated 2019 or later |
| 2600 Foothill Blvd, La Crescenta | 7 | all 7 incorporated Jun 2020 to Feb 2021 |
| 19634 Ventura Blvd, Tarzana | 6 | all 6 incorporated Aug to Nov 2020 |
| 7630 Vineland Ave, Sun Valley | 5 | all 5 incorporated May 26 to Jun 23, 2020, four weeks apart |
| 8925 S Pecos Rd, Henderson NV | 7 | enrolled 2022 to 2025 |
| 2819 NW Loop 410, San Antonio TX | 8 | includes CFHC NO12, 17, 18, 19 |

### The new lead: numbered hospices in San Antonio [22]
- There are **12 enrollments named "CFHC NO4" through "CFHC NO22, INC."**, all in San Antonio.
- 8 were incorporated on **2021-10-07**, 3 on 2021-10-25, and 1 has no date.
- Six of them sit at 2819 NW Loop 410, in suites G, L, O, Q, R and S. The other six are spread across San Antonio.
- They were certified between 2022-07-08 and 2023-09-28.
- **Each has its own ASSOCIATE_ID**, so Medicare's own key does not tie them together.
- The numbers run up to 22 and only 12 are here, so other members of the series may exist or may already be gone.

### Walking the chain
- **Hit means:** many new, for-profit hospices share one building and a founding window. That is the "hospice mill" signature, and it is still in Medicare's 2026 roster.
- **Miss means:** if stacking had been at the national rate, about 4% instead of 44%, it would be ordinary office-building clustering.
- **Boring explanation, partly ruled out:**
  - Small businesses share office buildings. No two LA hospices share an exact suite (0 enrollments), so this is same building, different suites.
  - LA hospice fraud is already a known story: LA Times, ProPublica, and CMS's enhanced oversight of new hospices in CA, NV, AZ and TX.
  - What is new: the stacking still shows in a 2026 file, and the CFHC series in San Antonio.
- **Traps:**
  - There is no hospice owner table in the warehouse, so the people behind these companies are not reachable here.
  - ZIP3 is only a stand-in for county lines.

---

## 2. Judges' debts: **probed**

**Row count:** 18,775 debts, 1,554 judges, disclosure years 2003-2020 (a few 1990 and 2022). DATE_CREATED (2021-23) is CourtListener's own date. It is not the filing year.

### What the debts are [13]

| Kind | Rows | Judges |
|---|---|---|
| Credit card | 7,089 | 701 |
| Mortgage | 3,543 | 485 |
| Student loan | 1,900 | 301 |
| Line of credit | 852 | 178 |
| Other | 5,082 | 802 |

- By size: J-K (up to $50K) is 10,021 rows. Over $1M (P codes) is 280 rows across 45 judges.
- **VALUE_CODE is -1 on 2,728 rows and null on 1,674.**

### What was checked [18]
1. I matched 17 big creditors by name: banks, card issuers, loan servicers.
2. 961 judges owed one of them in some year from 2003 to 2021 (6,210 judge-bank-year pairs).
3. I pulled only those judges' dockets from CourtListener's case list (filtered to those judges before joining).
4. A hit is a case naming the same bank as a party, filed in the disclosure year or the year after, with the judge still assigned.

| Result | Cases | Judges |
|---|---|---|
| **All hits** | **3,650** | **379** |
| Bank of America | 1,424 | 155 |
| Chase / JPMorgan | 925 | 138 |
| Wells Fargo | 664 | 70 |
| Judge held a card with that bank | 2,204 | |
| Judge held a home loan with that bank | 791 | |
| Foreclosure or real-property suits | 899 | 116 |
| Foreclosure suits where the judge held a home loan with the same bank | 192 | |

A rerun on the top 6 banks only [23], [24]:
- 3,504 cases and 351 judges in all.
- **1,198 cases and 92 judges are in bankruptcy courts**, where banks show up in almost every case.
- **Unusual loans** (guaranty, investment or rental property, business, farm, LLC, or $250K and up): 716 cases, 90 judges.
- **Unusual loans in district courts only: 424 cases, 68 judges.**
- Eye check: in 12 of 12 random district-court hits, the bank was a party and was also the judge's creditor. Examples: Wells Fargo mortgages on rental properties, Bank of America "mortgage on investment property #5".

### Walking the chain
- **Hit means:** the judge owed that bank money and stayed assigned to a case naming the bank.
- **Miss means:** either the creditor is never sued by that name (Amex, a local bank), or the OCR broke the name ("AMCRICAN EXPRESS").
- **Boring explanation, mostly stands:**
  - Suits against BofA/Countrywide, Chase and Wells filled every district in 2008-2015, and cases are assigned at random.
  - Under 28 USC 455, a "financial interest" means owning part of the party. A loan on ordinary terms is not ownership.
  - So most of the 3,650 are routine. This is not a twin of F-001, because stock is disqualifying and a Visa card is not.
- **The live sliver:** 68 district judges holding unusual loans from a bank while hearing 424 suits against it. Also the 192 foreclosure suits where the judge's own home loan was with the same bank; if any of those is a class action over loan terms, the judge could be a class member.
- **Known:** probe 95 on 2026-09-05 already found 831 cases and 150 judges with a narrower name key.
- **Top pairs** [20], data match only:
  - Richard Story (N.D. Ga.): BofA card, 93 BofA cases, 71 of them housing or lending suits.
  - Thomas Thrash (N.D. Ga.): BofA student loan, 75 cases.
  - Steve Jones (N.D. Ga.): Wells Fargo mortgage on rental property, 41 cases.
  - Timothy Dore (W.D. Wash. bankruptcy): Chase guaranty of an LLC loan, 62 Chase cases.

---

## 3. Meal-cap fingerprint: **probed**

**Row count:** 2,469 maker-years, 2022-2024, only makers with 100 or more meals a year.

### What the $125 is
- **The Sunshine Act has no $125 reporting line.** The reporting floor is about $13.82 per item.
- $125 is a common **company policy** cap. One industry survey found 28.6% of companies use it, and dinner caps average about $150.
- Sources: [qordata survey](https://www.qordata.com/hcp-meal-limit-survey-insights/), [ezCater on Sunshine Act limits](https://www.ezcater.com/lunchrush/office/compliance-in-food-spending-and-the-sunshine-act/), [bioxconomy on meal caps](https://www.bioxconomy.com/legal/pharma-companies-navigate-complex-hcp-meeting-compliance-with-meal-caps-averaging-50-150-per-event-type).
- **Trap:** the dbt model and the catalog both call it the "$125 reporting cap". That is wrong.

### What was checked
- **Raw Open Payments 2024** [17], all 14,101,484 food-and-drink payments:

| Price | Meals |
|---|---|
| exactly $124.99 | **20,666** |
| exactly $125.00 | **47,607** |
| exactly $126.00 | 675 |
| exactly $123.99 | 192 |
| exactly $150.00 | 12,172 |
| exactly $100.00 | 4,430 |
| anything over $125 | 424,896 (3.0% of meals) |

- $100 to $124.99 holds 460,953 meals. $125.01 to $149.99 holds 248,521. That is a ratio of 1.85, but a falling price curve would do that anyway. **The signal is the cent-exact spike, not the band ratio.**
- **Industry by year** [9]: the $124.00-124.99 band beats $125.01-126.00 by 5.2x (2022), 4.9x (2023) and 4.4x (2024).
- **Makers ranked** [10]: 502 makers with 3,000+ meals across 2022-24. The measure is meals in the $124.00-124.99 band per 1,000 meals. The median maker has 2.91.

| Maker | Meals | Per 1,000 in the band | Rank |
|---|---|---|---|
| Dompé US | 16,900 | 33.2 | 1 |
| Bausch & Lomb | 184,325 | 25.4 | 5 |
| Horizon Therapeutics | 131,153 | 23.0 | 8 |
| Phathom | 89,333 | 19.4 | 12 |
| **AstraZeneca** | 1,422,379 | **11.1** | 37 |
| **AbbVie** (both spellings) | 4.35M + 0.48M | **5.0 / 5.2** | 156 / 145 |
| **Novo Nordisk** | 1,463,676 | **4.3** | 190 |
| **Pfizer** | 1,326,660 | **0.6** | 409 |

### Walking the chain
- **Hit means:** a maker prices meals at its own policy line.
  - AstraZeneca does this 18x as often as Pfizer, with sales forces of the same size.
  - Exact $125.00 entries could mean the reported value is the cap, not the real bill. That would be under-reporting. The data cannot tell a set-price $125 menu from a capped entry.
- **Miss means:** a smooth price curve, no policy line.
- **Boring explanation, stands:** company per-head caps. **The triage premise is rejected:** AbbVie leads on meal count because it is big. Its bunching rate is barely above the median.
- **Trap:** the mart's "just above" band (125.01-126.00) leaves out exactly $125.00. That is the biggest spike, so the cliff ratio understates the pile-up.
- **Overlap:** sits beside F-004 and F-019.

---

## 4. Judges' agreements with law firms: **probed**

**Row count:** 10,007 lines, disclosure years 2003-2022.

### What was checked
- **Classified** [14]:
  - Law-firm-like: 2,517 rows.
  - Government or public plans: 3,962.
  - Other: 3,528.
  - Rows with payout words (deferred, capital account, buyout, installment): 608.
- **Firm names** [16]: no firm is tied to more than about 3 judges. Examples: Stroock, Foley & Lardner, Debevoise, Haynes and Boone. Most lines say "pension plan, no control" or "401(k)".
- **Firm as counsel** [19]:
  1. I matched about 160 named firms in the agreement text, giving **171 judge-firm pairs (164 judges)**.
  2. I searched the ATTORNEYS field of CourtListener's 10.1M published opinions: **147,098 opinions** name one of those firms.
  3. A hit is an opinion where the judge is the docket's assigned judge, or is named in the JUDGES text.

| Result | Pairs | Opinions |
|---|---|---|
| Firm was counsel before that judge, any year | 66 | 356 |
| **In the agreement window** (disclosure years -2 to +1) | **26** | **42** |

### Eye check
- **Many hits are name collisions.** Andrew Peck matched bankruptcy judge James M. Peck. The two Brodericks matched a New Hampshire state court. John Roberts matched a different Roberts in D.D.C. Robert Wilkins matched William Wilkins on the 4th Circuit.
- **Real-looking hits:**
  - Sandra Ikuta (O'Melveny pension) sat on 5 en banc opinions in Sarei v. Rio Tinto (2010), where O'Melveny is in the attorney list.
  - Several bankruptcy judges matched by docket ID: Shelley Chapman with Willkie (6), Mark Mullin with Haynes and Boone (11), Gregory Taddonio with Reed Smith (8).

### Walking the chain
- **Hit means:** the judge was paid by the firm's plan while the firm argued before them.
- **Miss means nothing.** The warehouse has no docket-level attorney data, only the ATTORNEYS field on published opinions (mostly Harvard CAP, through 2018).
- **Boring explanation, stands:**
  - Most firm agreements are fixed pensions, closed plans or 401(k)s with "no control". The money does not ride on the firm's wins.
  - The small count also keeps it small.
- **What would open it:** PACER/RECAP attorney appearances. That data is not landed.

---

## 5. Nursing-home relief by chain: **dead**

**Row count:** 617 chains, 10,162 homes, $939.2M name-matched.

### What was checked [7], [8]
- I ranked chains by relief per bed and compared the top 10% with the rest.
- Then I re-cut the chains by star band and by fines-per-bed quartile. Per matched bed = matched dollars ÷ (matched homes × the chain's average beds per home).

| Group | Chains | Homes matched | Per matched bed | Fines per bed | Abuse-icon share | Avg stars |
|---|---|---|---|---|---|---|
| Top 10% by relief per bed | 61 | **56.3%** | $10,500 | $234 | 9.5% | 3.12 |
| Other 90% | 556 | **6.1%** | $7,710 | $342 | 11.2% | 2.85 |
| Stars under 2.5 | 201 | 8.2% | **$8,193** | $538 | 17.6% | 1.94 |
| Stars 3.5+ | 158 | 14.7% | **$10,692** | $119 | 3.6% | 4.03 |
| Lowest-fines quartile | 155 | 14.0% | $9,129 | $52 | 3.9% | 3.52 |
| Highest-fines quartile | 154 | 7.7% | $7,991 | $748 | 18.3% | 2.27 |

### Walking the chain
- **Hit would have meant:** the worst chains took more per bed.
- **What we got:** they took **about 12-23% less per matched bed**. The same shape holds after removing parent-cheque matches (strict: $8,008 vs $10,912).
- **The "top relief" ranking is a match-rate ranking.** The top decile matched 56% of its homes and the rest matched 6%.
- **Among the worst-fines chains, 68% show $0** (105 of 154), against 55% in the cleanest quartile. That is a naming artifact, not missing money.
- **Boring explanation, stands:**
  - Relief was paid by formula: per facility, per bed, and incentive payments tied to infection and death rates. That would favor better homes, which fits what we see.
  - Top dollars: National HealthCare Corp $66.0M across 44 matched homes, 3.8 stars. The name match there looks clean (all exact).
- **Trap:** ArchCare's $13.1M is $7.1M "contains" matches at 347 beds per home, so check before quoting.
- **Overlap:** F-021 and F-029 already cover chain quality.

---

## New data traps (for the trap file, if Chris wants them)
1. **facts.tsv, hospice NPI top values are wrong.** "NPI 1013548734 45" does not exist in the mart. The max is 2 enrollments per NPI.
2. **The "$125 reporting cap" is not a reporting cap.** Open Payments has no $125 line. The catalog and the dbt comment both say otherwise. The mart's just-above band also leaves out exactly $125.00, the biggest spike.
3. **Relief per bed ranks name-match rate, not money.** Divide by matched beds.
4. **Opinion-cluster JUDGES text collides on surnames** (Peck, Broderick, Roberts, Wilkins). Use ASSIGNED_TO_ID, or check the court.
5. **Same hospice address means same building, not same suite.** LA has 0 exact-suite matches.
6. **Debt VALUE_CODE** is -1 on 2,728 rows and null on 1,674. **A third of bank-party docket hits are in bankruptcy courts**, where banks are in almost every case.
