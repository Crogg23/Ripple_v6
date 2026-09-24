# Deep pass 4: insider trades, addiction prescribers, trials, dialysis, hospital cost reports

2026-09-24 · agent deep-4 · Python door · **30 SQL statements** (all SELECT/WITH), plus the 2 required ALTER SESSION lines on each of 13 connections · SQL in `deep-4.sql`, numbered to match the [Qn] tags below.

Every person, company, clinic and hospital named here is **a data match, not verified against primary records**.

---

## The menu

| Rank | Table | Verdict | The one number |
|---|---|---|---|
| 1 | FED_CMS_DIALYSIS | **live (flipped)** | The big chains are average. The outliers are **nursing-home dialysis operators**: 46 clinics, and **20 are rated "Worse than Expected" on survival**. Everyone else: 2.3%. |
| 2 | FED_CMS_HCRIS | probed | Hospitals switching to for-profit show **no charity drop overall** (81 hospitals, median −0.03 pts). One buyer stands out: **Prime Healthcare**, 11 hospitals, charity **$58.1M → $31.4M a year**. |
| 3 | FED_SEC_INSIDER_NONDERIV_TRANS | probed | Of **22,770** owner-months with $5M+ sold, **987** came before the stock halved. There is no 10b5-1 plan flag for these years, and stock splits look like crashes. |
| 4 | FED_CLINICALTRIALS | probed | **706 of 8,234** FDA-regulated US phase 2–4 trials (8.6%) have no results posted, covering **152,850 patients**. The long tail is small sponsors, and trial trackers already publish this. |
| 5 | ADDICTION_PRESCRIBERS_PAID | **dead** | Indivior paid **$170,922** total to 2,604 buprenorphine prescribers, and its brand share did not move (12.0% vs 11.1%). **37% of the table's "addiction" dollars are pain drugs.** |

> **Bad news up front**
> - The dialysis triage premise is **backwards**. DaVita and Fresenius are at or better than average. The problem is small operators that CMS labels "Independent".
> - The addiction table is **mislabeled**. $236.7M of its $636.0M is pain buprenorphine (Belbuca, Butrans, generic patch) plus Part D methadone, which is pain methadone.
> - The SEC "sold before bad news" test can't be made defensible here. The 10b5-1 plan checkbox exists only in a 2026-Q1 table, and the trade table holds **2 rows** from 2026.
> - The HCRIS "charity falls after a sale" story is **null in the pool**. Total charity care at the 81 converted hospitals went **up**, from $322.0M to $373.5M a year.

---

## 1. FED_CMS_DIALYSIS: live, but not the angle triage gave

**The physical thing:** a dialysis unit inside a nursing home. It has 0–2 chairs and serves frail residents, and CMS rates its death rate against what its patient mix predicts.

**Shape first** [Q7][Q8]
- 7,557 clinics, one row each. Death and hospital-stay figures are CMS risk-adjusted rates per 100 patient-years, for example 17.9 and 148.1.
- DaVita has 2,800 clinics and Fresenius has 2,772. The "Independent" label covers 742.

**Checked** [Q22][Q23][Q29]
- I grouped clinics into DaVita, Fresenius, other chains (for-profit / non-profit) and independents (for-profit / non-profit).
- For each group: the patient-weighted death rate, the share of clinics CMS rates "Worse than Expected" on survival, stars, and each clinic minus its own state's clinic average.
- I listed every independent for-profit clinic rated Worse than Expected, then matched facility names for the nursing-home dialysis brands (Dialyze Direct, Dialysis Direct, Concerto, Home Dialysis Services).

| Group | Clinics | Death rate (weighted) | Worse than Expected | vs same-state avg (deaths) | 1–2 stars |
|---|---|---|---|---|---|
| DaVita | 2,800 | 22.11 | 2.5% | +0.30 | 28.2% |
| Fresenius | 2,772 | 21.32 | 1.9% | −0.67 | 32.9% |
| Other chain, for-profit | 773 | 22.01 | 4.0% | +0.11 | 36.1% |
| Independent, for-profit | 452 | **24.76** | **10.6%** | **+3.08** | **45.4%** |
| Independent, non-profit | 290 | 20.21 | 1.7% | −0.37 | 29.7% |
| All | 7,557 | 21.80 | 2.8% | 0 | 32.0% |

| Cut [Q29] | Clinics | Rated Worse than Expected | Death rate | Median chairs |
|---|---|---|---|---|
| **Nursing-home dialysis brands** (21 states) | 46 | **20 (43.5%; 20 of 38 with a rating)** | **32.27** | 1 |
| Other independent for-profits | 421 | 33 (7.8%) | 23.67 | 14 |
| Everyone else | 7,090 | 161 (2.3%) | 21.65 | 17 |

- Examples [Q23]: Dialyze Direct Memphis TN (death rate 55.2), Dialyze Direct MD Glen Burnie (52.1), Dialyze Direct Sugarland TX (42.2), Concerto Dialysis Lincolnwood IL (30.1 on 3,224 patients), Spectrum Dialysis Reseda CA (43.5).
- Hospital stays at independent for-profits run **+16.1 per 100 patient-years** above their same-state average. Long-term catheter use is 28.2%; the chains run 16.8–18.3%.
- **Maryland:** 9 of the state's 12 Worse-than-Expected clinics are independent for-profits.

**Hit means:** a small, identifiable set of operators, many of them multi-state brands, carries a death rate about 50% above everyone else's even after CMS adjusts for patient mix. The names and CCNs are in hand.
**Miss means:** the rating model already adjusts for nursing-home residence and the gap closes on a like-for-like check. Then this is only the frailty of nursing-home patients.

**Boring explanation, not ruled out:** nursing-home residents are the sickest dialysis patients. I did **not** check whether CMS's death-rate model adjusts for nursing-home status. That is the first thing to read. The chain-vs-independent angle itself is ruled out: the two big chains sit at or below the average.

**Traps**
- `CHAIN_ORGANIZATION = 'Independent'` does not mean a single clinic. Dialyze Direct alone has 6+ CCNs in 5+ states under that label. The brand name match also picked up clinics labeled DaVita, DCI and Other.
- `MORTALITY_RATE_FACILITY` is a rate per 100 patient-years, not a 1.0-centered ratio. Some clinics show 0.

---

## 2. FED_CMS_HCRIS: probed; one buyer worth a look

**The physical thing:** Worksheet S-10 of a hospital's yearly Medicare cost report. It gives the cost of free care (charity) and the bills the hospital wrote off (bad debt).

**Shape first** [Q9][Q10][Q24]
- 80,077 reports and 7,028 CCNs, for fiscal years 2011–2024 (2011 and 2024 are partial).
- There are 78,987 CCN-years, so **1,090 extra reports** land in the same year. 2,916 reports cover under 300 days.
- The bad-debt max of **$20.4B** is Sullivan County Community Hospital (151327), FY2016. That is a typo; every other year's max is $0.25–1.03B.
- 2–10 reports a year show bad debt above total costs.

**Checked, angle A: bad debt vs charity** [Q25][Q26]
- I took the latest FY2022 report per short-term hospital and grouped by ownership type.
- I compared bad debt with charity twice: raw, and with bad debt converted to cost (× cost-to-charge ratio).

| FY2022 | Hospitals | Median bad debt ÷ charity (raw) | Same, bad debt at cost |
|---|---|---|---|
| For-profit | 757 | 3.72 | **0.52** |
| Nonprofit | 1,991 | 2.15 | **0.53** |
| Government | 471 | 3.38 | 0.95 |

- The raw gap is a **markup artifact**: for-profits charge more per dollar of cost. At cost, the gap is gone.
- Only **one** hospital has bad debt at cost over $20M and more than 5× its charity: **St. Mary's Regional Medical Center, Reno NV**. Its enrollment is held by Prime Healthcare. Bad debt is $106.0M at charges ($22.7M at cost), charity is $2.98M, a ratio of 7.6×, and net income is −$54.0M.

**Checked, angle B: charity after a switch to for-profit** [Q27][Q28][Q30]
- A switch is `TYPE_OF_CONTROL` moving from nonprofit or government to proprietary (3–6) between back-to-back fiscal years. The hospital must hold the old type for the 2 years before and the new type for the 2 years after. 172 raw flips gave **81 clean** ones.
- I measured charity as a % of total costs, 2 years before vs 2 years after.
- Peers are same-state short-term hospitals that never changed type, over the same years.

| Buyer (enrolled today) | Hospitals | Charity $/yr before → after | Median change | Net of same-state trend |
|---|---|---|---|---|
| All | 81 | $322.0M → **$373.5M** | −0.03 pts | — |
| Other buyers | 58 | $230.2M → $323.1M | +0.38 pts | **+0.53 pts** |
| **Prime Healthcare** | 11 | **$58.1M → $31.4M** | −1.40 pts | **−1.49 pts** (7 of 11 below trend) |
| Prospect | 3 | $9.0M → $4.4M | −1.85 pts | +0.18 (the RI drop matches the state trend) |
| No enrollment match | 9 | $24.7M → $14.5M | −0.69 pts | −0.56 |

- The Prime dollars are mostly New Jersey: St. Mary's Passaic ($11.61M → $2.11M), St. Clare's ($16.68M → $8.57M) and St. Michael's ($12.00M → $6.46M).
- NJ's own trend fell over those years, by 0.36 to 3.07 pts (Medicaid expansion). That explains part of the drop.
- Prime also drops in states that did not expand Medicaid then: Providence KS (−3.00 net) and St Mary's MO (−2.25 net).

**Hit means:** one named buyer's hospitals cut free care by about 46% after purchase, while other for-profit buyers' hospitals rose.
**Miss means:** with only 11 hospitals, and NJ's charity-care subsidy rules shifting, the gap is noise plus policy.

**Boring:** charity follows Medicaid expansion. I ruled it out for the pool by netting out the same-state trend. For Prime it is only partly ruled out, since n = 11 and Prime has had press coverage before.

**Traps**
- `HOSPITAL_ENROLLMENTS` names **today's** owner, not the buyer at the switch. For example, MUSC Health Kershaw switches to for-profit in 2019 but is enrolled today under the Medical University Hospital Authority, and the for-profit owner in between appears in neither table.
- `TOTAL_BAD_DEBT_EXPENSE` is at charges and `COST_OF_CHARITY_CARE` is at cost. Never divide one by the other raw.

---

## 3. FED_SEC_INSIDER_NONDERIV_TRANS: probed

**The physical thing:** a Form 4 line in which an insider reports an open-market sale (code S), with the shares and the price.

**Shape first** [Q1][Q2]
- 2,672,841 rows on 1,354,644 filings. Only 43 dates fall outside 2000–2026.
- Coverage is heavy before 2022 (1.71M rows). There are about 290K rows a year for 2022–2024, only 97,575 for 2025 and **2 for 2026**.
- 751,436 sales. 614 rows over $10B. 651,300 rows at price 0.

**Checked** [Q11][Q12][Q13][Q14]
- **Top sellers:** sales only, 2015–2026, price $0.01–10,000, value ≤ $10B. I summed per filing, then attached the issuer (submission table) and the first reporting owner.
- **Plan flag:** I searched both databases for the 10b5-1 checkbox column.
- **Recalls:** 25 issuers matched FDA Class I recall firms on the full name. For each, I compared sales in the 30 days before a recall with the 60–90-day window before, same issuer.
- **Sold before a fall:** owner-months with $5M+ sold. I compared the sale price with the issuer's own median insider trade price 4–9 months later.

**What came back**
- Top sellers: Jeff Bezos (Amazon) $39.47B, Elon Musk (Tesla) $39.36B. Alice, Rob and Jim Walton show **$24.63B each, and it is the same trades three times**.
- James Cassidy and James McKillop show **$19.5B** in "sales" of blank shell companies at $975–1,000 a share. Those are fake prices.
- The plan flag `AFF10B5ONE` exists only in `FINANCE__FED_SEC_EDGAR_INSIDERS`: 69.3K filings, filed Jan–Mar 2026, with no overlap with this table.
- Recall test: $78.2M sold before recalls vs **$605.8M** in the control windows ($559.6M of that is Walmart). Without Walmart it is $76.7M vs $46.2M, driven by Pfizer ($39.7M vs $10.8M across 10 recalls). Small either way.
- Sold before a fall: **987 of 22,770** owner-months (4.3%, $71.7B of $1,479.7B) came before a price at least 50% lower.
  - The top of that list is **stock splits**: Tesla 3:1, Walmart 3:1, Alphabet 20:1.
  - After the splits come real 2021–22 crashes: Daniel Loeb in Upstart ($712M at $225 → $51), Ernest Garcia II in Carvana ($329M at $353 → $105), Artal Group in WW ($456M at $76 → $20, Aug 2018), Frank Slootman in Snowflake ($344M at $344 → $168), and the DeSantis family in Celsius (about $549M, Mar 2024 → $32).

**Hit means:** the table can produce a named candidate list of big sellers ahead of collapses.
**Miss means:** without the plan flag and a real price feed, every name can be explained as a scheduled plan, a lockup expiring, a secondary offering or a market-wide crash.

**Boring:** 10b5-1 plans (not rule-out-able), lockup expiries at the 2021 top, and the 2022 drawdown. The recall angle is ruled out as small.

**Traps**
- Joint filers repeat the same trades: the Waltons count 3×.
- Tiber Creek-style shell companies report $1,000-a-share "sales" worth up to $19.5B under the $10B-per-row cap.
- A stock split looks like a crash in insider prices. My split guard was useless in both directions: it flagged Unity and Snowflake, which did not split, and missed Tesla and Walmart, which did.
- In Q13, `\b` word boundaries don't work in Snowflake regex, so no suffixes were stripped. Matches were on the full upper-case name.

---

## 4. FED_CLINICALTRIALS: probed

**The physical thing:** a ClinicalTrials.gov record that says the trial finished but has no results section.

**Shape first** [Q5][Q6]
- 601,694 studies, one per NCT_ID, with the snapshot dated 2026-09-04.
- `HAS_RESULTS` agrees with `RESULTS_FIRST_POSTED_DATE` on all 80,018 rows.
- `IS_FDA_REGULATED_DRUG` is null on 223,743 rows.

**Checked** [Q19][Q20][Q21]
- Interventional, phase 2/3/4 (including 1/2), a US site, completed or terminated.
- Primary completion between 2017-01-18 and 2022-06-30, so the 1-year deadline plus a 2-year delay has passed.
- Split by the FDA-regulated flag, then by sponsor.

| Set | Trials | No results | Share | Patients in no-result trials |
|---|---|---|---|---|
| FDA-regulated | 8,234 | 706 | 8.6% | 152,850 |
| · Industry | 4,410 | 397 | 9.0% | 56,106 |
| · Academic/other | 3,380 | 276 | 8.2% | 92,973 |
| · NIH | 301 | 6 | 2.0% | 2,972 |
| Flag blank (older records) | 2,504 | 250 | 10.0% | 43,889 |
| Not FDA-regulated (not bound by the law) | 271 | 160 | 59% | 35,513 |

- A long tail: **537 sponsors** hold the missing results, and **435 of them hold exactly one**.
- The top holders are Brigham and Women's (9 of 35), UC San Diego (9 of 26), "Therapeutics, Inc." (7 of 7), Colgate Palmolive (7 of 7) and Repurposed Therapeutics (5 of 5).
- Big pharma is at zero: BMS 0 of 101, Gilead 0 of 86, Lilly 0 of 80.

**Hit means:** named academic centers and small biotechs sit on finished trials.
**Miss means:** the table can't tell "never submitted" from "submitted, stuck in NLM review" or "certified delay". Some of the 706 are those.

**Boring:** the FDAAA TrialsTracker already publishes sponsor league tables, and the counts here are small per sponsor. Not ruled out.

**Traps**
- `RESULTS_FIRST_POSTED_DATE` is the public posting date after review, not the submission date the law counts. By it, 6,512 of 7,528 reporters look "late", which is meaningless.
- Max `ENROLLMENT` in this set is 72,000, one UCSF trial. The table-wide 188.8M max falls outside the set.

---

## 5. ADDICTION_PRESCRIBERS_PAID: dead as framed

**The physical thing:** a Medicare Part D prescriber's 2022 claims for six generic names, joined to all drug-company money they got in 2022.

**Shape first** [Q3][Q4][Q15]
- 44,335 prescribers, all DATA_YEAR 2022. 26,193 were paid by someone.
- The six generic names hide pain drugs. Part D 2022 by brand:

| Brand | Cost | What it is |
|---|---|---|
| Buprenorphine-Naloxone (generic) | $225.2M | addiction |
| **Belbuca** | **$123.0M** | **pain film** |
| Suboxone | $90.2M | addiction |
| **"Buprenorphine" (generic)** | **$88.0M** | **most likely the pain patch** ($330 a claim; mono tablets file as "Buprenorphine Hcl" at $70) |
| Vivitrol | $22.4M | addiction |
| Zubsolv / Buprenorphine Hcl / Sublocade | $19.2M / $18.2M / $13.4M | addiction |
| **Butrans** | **$13.9M** | **pain patch** |
| **Methadone Hcl** | **$11.8M** | **pain.** Addiction methadone comes from clinics, not Part D |
| Naltrexone Hcl | $10.6M | addiction |

These lines sum to $635.9M, the table's total. **The pain lines are $236.7M, or 37%.**

**Checked** [Q16][Q17][Q18]
- Payment buckets inside each prescriber type.
- Open Payments 2022 money from Indivior, Alkermes, Orexo and BDSI/Collegium, per NPI, against each prescriber's share of that maker's own brand.

| Maker | Paid prescribers | Their total money | Own-brand share: paid vs not |
|---|---|---|---|
| Indivior (Suboxone + Sublocade) | 2,604 | **$170,922** | 12.0% vs 11.1% |
| Orexo (Zubsolv) | 919 | $35,786 | 3.9% vs 1.9% |
| Alkermes (Vivitrol) | 2,033 | $2.77M | **12.0% vs 5.8%** |
| BDSI/Collegium (Belbuca) | 2,602 | $208,004 | 44.8% vs 30.8% |

- Paid prescribers run bigger panels (Indivior median 71 claims vs 37), so volume drives both.
- The top 20 by maker money ($41K–$134K each, mostly speaker fees) are **all Alkermes-paid psychiatrists and NPs**, with Vivitrol claims at 0 for 15 of 20.
  - The top one is Jakub Juros (Psychiatry, CA), $133,539, 40 Vivitrol claims.
  - Alkermes also sells antipsychotics. The fees are almost surely for those; the Open Payments mart has no product column to prove it.
- Within prescriber type, spend rises with all-company money up to $10K and then flattens. PAs go from $3,788 to $14,515 median.

**Hit means:** only the Vivitrol 2× share among Alkermes-paid prescribers, on $2.77M of money. That is the known "money follows prescribing" pattern.
**Miss means:** Indivior's money is meal-sized and moves nothing. The story as pitched is not here.

**Boring:** volume and specialty drive both the money and the claims. That is confirmed, not ruled out.

**Traps**
- The table's "addiction drugs" are **37% pain drugs by cost**.
- Part D hides drug rows under 11 claims, so a 0 means "under 11 or none".

---

## Statement count
30 SQL statements (Q1–Q30), all read-only, none failed, tagged `coverage-b-2026-09-24`. Each of the 13 connections also ran the 2 required ALTER SESSION lines.

parked: the session scratchpad is shared by all ten deep agents, and plain file names (`run.py`, `count.txt`) collide. My first runner was overwritten mid-run. That run printed nothing and logged nothing; if it reached the warehouse at all, it was the same 10 read-only count and sample statements.
