# Deep look 2/1: company owners, colleges, Google ads, power outages, power prices

2026-09-24 · agent deep2/deep-1 · **30 of 35 SQL statements** · Python door, read-only · SQL in `deep-1.sql`

Every person or company named here is a **data match, not verified against primary records**.

---

## The answer first

**None of the five is a big, defensible story as triaged.** All five come back **probed**.
Each triage angle hit its own boring explanation, or the known story everyone has already run.

**Best lead: the company-ID exception file (REPEX).** One registrar is behind the US number:
- Current US company IDs that won't name their owner: **5.0%**. Second only to Hong Kong, level with the BVI (4.8%).
- 91% of those US refusals sit with one registrar, Bloomberg. Its US rate is **5.7%**; every other registrar's US rate is **2.3%**.
- Outside the US, Bloomberg's rate matches the other registrars (UK 1.69% vs 1.69%).
- Not ruled out yet: Bloomberg's US clients may just be a different kind of company.

| Table | Verdict | The one number |
|---|---|---|
| GLEIF_REPEX | probed | US company IDs managed by Bloomberg refuse to name the owner at 5.7%; other registrars' US IDs at 2.3% |
| EIA861_RELIABILITY | probed | Altamaha's "12 days" is Hurricane Helene: its own storm-excluded number still reads 17,060 min, so the split was never done |
| EIA861_SALES_ULT_CUST | probed | The top of the price list is the famous coastal big utilities; price vs outage correlation inside a state is 0.08 |
| GOOGLE_POLADS_CREATIVE_STATS | probed | $861M of US Google political spend comes from buyers who gave only a tax ID (EIN); much of it is state races, not hidden money |
| COLLEGE_SCORECARD_INSTITUTION | probed | The triage filter (earn < $30K, debt > $20K, 500+ students) catches just **6 schools**; debt is capped by federal loan limits |

---

## 1. ECONOMICS__INTL_GLEIF_REPEX: **probed**, closest to live

**What it is:** 6,313,372 rows = 3,169,671 company IDs (LEIs). Each appears twice by design: once for the direct parent, once for the ultimate parent.
**Land rate:** 3,142,422 of 3,169,671 LEIs (99.1%) are in the main GLEIF register.

**Reasons given for not naming the ultimate parent**

| Reason | LEIs | Plain meaning |
|---|---|---|
| NATURAL_PERSONS | 1,166,586 | owned by people, not a company. The normal answer |
| NON_CONSOLIDATING | 1,093,611 | no parent that files consolidated accounts |
| NO_KNOWN_PERSON | 665,043 | nobody controls it (widely held) |
| NO_LEI | 118,224 | a parent exists but has no LEI |
| **NON_PUBLIC** | **107,624** | refuses: says disclosure is barred or harmful |
| 5 newer specific refusal codes | 1,999 | e.g. CONSENT_NOT_OBTAINED 1,392 |

**Checked**
- Joined REPEX (ultimate-parent rows, one per LEI) to GLEIF on LEI.
- Refusal share = LEIs with NON_PUBLIC or the 5 newer codes ÷ **every** LEI in that country, including LEIs with no exception at all.
- Ran it on all records, then on current (ISSUED) records only.
- Split US and 9 peer countries by registrar: Bloomberg vs all other offices.
- Grouped US refusals by the first line of the registered address.
- Pulled LEI-shaped IDs out of OpenSanctions company records and joined them in.

**What came back**
- All records: US **11.25%** (40,088 of 356,413), top of every 10K+ country. But **83%** of those sit on lapsed or retired records.
- Current records only:

| Country | Current LEIs | Refuse share |
|---|---|---|
| Hong Kong | 7,986 | 7.84% |
| **US** | **134,287** | **5.01%** (6,721) |
| BVI | 16,561 | 4.84% |
| Singapore | 8,720 | 4.84% |
| Jersey | 7,394 | 4.60% |
| Cayman | 26,580 | 2.28% |
| UK | 93,481 | 1.69% |
| Germany | 183,177 | 0.99% |

- Same country, split by registrar (current records):

| Country | Bloomberg | Other registrars |
|---|---|---|
| **US** | **5.66%** (6,142 of 108,541) | **2.25%** (579 of 25,746) |
| UK | 1.69% | 1.69% |
| Jersey | 4.55% | 4.61% |
| Singapore | 5.03% | 4.69% |
| Hong Kong | 5.61% | 9.12% |
| BVI | 6.37% | 3.71% |

- Who the 6,721 current US refusers are:
  - 3,953 are Delaware entities.
  - 6,603 are marked "fully corroborated".
  - All were renewed in 2025 or 2026 (3,587 and 3,134), so these are not dead records.
  - Every one uses the old catch-all NON_PUBLIC code, not the five specific codes.
- Registered-agent addresses:
  - CSC, Wilmington: 48,029 LEIs, 15.2% refuse.
  - CT Corp: 44,937 LEIs, 13.1% refuse.
  - Both are close to the US base. That's the normal Delaware registered-agent pattern, not a pile of shells.
- Sanctions join:
  - 1,390 sanctioned company targets carry an LEI-shaped ID, and 1,246 of them land in GLEIF (89.6%).
  - Second-field check: the first five letters of the name agree on 709 of 1,246 (57%). Many GLEIF names are in Cyrillic, so this undercounts real matches.
  - **72 refuse** to name the owner: 7.1% of those that filed an exception, vs 3.5% for the whole file. Double the rate, but only 72 companies.

**Hit means:** one registrar's US book lets companies skip naming their owner at 2.5x the rate of every other registrar's US book. That's a process story about who checks the exception.
**Miss means:** if the gap came from the company mix (Bloomberg's US clients are swap counterparties and fund vehicles), it's just who shops where.
**Boring explanation:** client mix. **Not ruled out.** The UK, Jersey and Singapore numbers point toward registrar practice, because the same office matches its peers there. A deeper pass would compare the same legal form, the same Delaware jurisdiction and the same registration year across registrars.
**The triage angles:** "shell-registration addresses" is dead (registered agents, at the base rate). "Near sanctioned names" is small (72).

---

## 2. ENERGY__FED_EIA861_RELIABILITY: **probed**

**What it is:** 971 utility-state rows, 2024 only.
- 744 have the standard (IEEE) outage minutes.
- 221 report only the utility's own method, which can't be ranked alongside the rest.

**Checked**
- Outage minutes per customer (SAIDI), with and without major-event days (MED).
- Ranked 1K+-customer utilities on the with-MED number and 10K+-customer utilities on the without-MED number. Compared each to its state median.
- Customer-weighted averages for the 6 Helene states (GA, NC, SC, FL, TN, VA) vs the rest.

**What came back**
- **16 of the top 20** with-MED utilities are in the Helene states. The other 4 are 3 Texas utilities (Beryl country in July 2024; that's from outside the data) and one Mississippi co-op.
- Helene states vs the rest, customer-weighted:
  - with major events: **1,471 min vs 454**
  - without major events: **131.9 vs 131.6**. Identical.
  - Outside storm days, the Helene states are average.
- **Altamaha EMC (GA):**
  - 17,310 min with major events. The without-MED number is still **17,060**, so only 254 minutes were carved out.
  - Georgia neighbors did carve Helene out: Jefferson EMC went from 10,320 to 109, Washington EMC from 6,930 to 429.
  - Altamaha's own figures agree with each other: 3.246 outages × 5,255 min each = 17,058. It's a reporting choice, not a typo.
  - Georgia median without major events: 128 min.
- Without-MED top list: **6 of the top 14 are East Texas co-ops**, e.g. Jasper-Newton 1,512 and Upshur 1,249. Most sit near the path Hurricane Beryl took in July 2024. That storm path comes from outside the data and wasn't checked here.
- Customer-weighted without-MED by owner:

| Owner | Minutes |
|---|---|
| Co-op | 188 |
| Investor-owned | 128 |
| Municipal | 90 |

**Hit means:** a utility whose outages stay high even after storm days are taken out.
**Miss means:** the high number is a storm, or storm days that were never taken out.
**Boring explanation:** Helene, and the triage note named it. **Confirmed.** The "chronic" list can't be called chronic from one year: the table holds 2024 only, and 2024 had Beryl and the Texas derechos.

---

## 3. ENERGY__FED_EIA861_SALES_ULT_CUST: **probed**

**What it is:** 2,815 rows. Clean comparison set: Part A, Bundled (full service), DATA_TYPE 'O'. That's 1,673 rows, 1,228 utilities, 118.9M home customers, 15.79¢/kWh overall.

**Checked**
- Home price = residential revenue ($K) × 100 ÷ residential MWh, giving cents per kWh.
- Compared each utility with 10K+ home customers to its state median. The state pool is Part A utilities with 1K+ homes.
- Then compared again within the same state *and* the same ownership type.

**What came back**

| Utility | ¢/kWh | State median | x state | Same-owner median |
|---|---|---|---|---|
| Massachusetts Electric | 33.6 | 16.3 | 2.06 | **34.4** |
| San Diego Gas & Electric | 43.6 | 21.2 | 2.06 | 31.5 |
| Con Edison | 35.7 | 18.5 | 1.92 | 18.8 |
| PG&E | 39.6 | 21.2 | 1.87 | 31.5 |

- The "2x the state" gap is mostly **big company vs small town/co-op**. Small cheap utilities pull the state median down.
- Investor-owned median ratio: 1.076. 22 of 153 sit at 1.3x+ (15.5M homes). Co-ops 1.021, munis 0.958.
- Small non-obvious leads:
  - **Roanoke EMC (NC):** 12,049 homes, 21.1¢ vs NC co-op median 14.2¢, average bill **$240/month** vs NC median $131.
  - **USBIA–San Carlos Project (AZ):** 11,432 homes, 19.5¢ vs AZ 13.9¢.
  - **Orcas Power & Light (WA island co-op):** 18.4¢ vs WA co-op median 9.3¢.
- **Join tried:** price × outages, on utility number + state.
  - 722 of 1,347 utilities land (53.6%).
  - Within-state price ratio vs outage ratio: correlation **0.08**. No link.
  - Only one clean overlap: Buckeye Rural Electric Coop (OH), 1.3x the state price and 12.4x the state's outage minutes (1,159).

**Hit means:** a utility charging far more than its own-type peers in its state.
**Miss means:** the gap is the known big-utility-vs-co-op split.
**Boring explanation:** Hawaii/California/New England big companies are high and already published by EIA. **Confirmed.**
The demographics join for Roanoke (does a poor, majority-Black service area pay more?) was not possible: no county census table in the marts.

---

## 4. EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS: **probed**

**What it is:** 1,562,870 ads, 2018–2026.

**Checked**
- US vs non-US spend ranges by year.
- Targeting shares in 2024. Share = spend-range midpoint on that kind of ad ÷ all 2024 US midpoint.
- Joined the sibling ADVERTISER_STATS table (exact US spend and the ID each buyer gave Google) to the FEC committee list by cleaned name.

**What came back**
- **Non-US USD ranges are placeholders.** Every non-US row reads $0–100. Example: 312,139 non-US ads in 2024, all "0–100". India's BJP tops by row count only.
- US ads started in 2024: 168,787, $731M–$881M in range terms.
  - 4 ads have a blank top of range; one has a $3M floor.
- 2024 US targeting:

| Kind | Share of midpoint spend |
|---|---|
| ZIP-level geography | 25.9% (71,527 ads; Harris campaign 93%) |
| One gender only | 6.7% |
| Narrow age (1–2 bands) | 4.3% |

- US buyers by the ID they gave Google (exact spend, all years):

| ID given | Buyers | Spend | Name found in FEC list |
|---|---|---|---|
| FEC ID | 3,117 | $1,389.1M | 91.8% |
| **EIN only** | **8,368** | **$861.4M** | 11.9% |
| State registration / other | 3,449 | $204.3M | 2.4% |
| Blank | 1,167 | $41.8M | 0.7% |

- The no-FEC-ID pile is mixed (EIN only, state registration or blank):
  - Federal campaigns that used an EIN: MIKE BLOOMBERG 2020 INC $61.9M, TOM STEYER 2020 $8.6M.
  - State races: Steyer for Governor 2026 $14.2M, JB for Governor $8.1M.
  - Ballot measures.
  - 501(c)(4)s: AFP Action $21.9M, American Action Network $10.3M, One Nation $10.2M.
  - Companies: Money Metals Exchange LLC (a gold dealer, no ID listed) $18.5M, Kalshi $7.75M, SmartNews $7.8M.
- One targeting lead: **SECURING AMERICAN GREATNESS INC**, EIN only, $7.1M exact.
  - 84% of its 2024 midpoint spend ($5.5M) went on one-gender ads.
  - Which gender was not pulled.

**Hit means:** a no-FEC-ID group spending big and targeting narrowly.
**Miss means:** it's state politics, or a company buying ads that mention politics.
**Boring explanation:**
- State candidates and ballot committees have no FEC ID by law.
- Google itself publishes this ranking.
- Google caps political targeting at age, gender and location.
- **Mostly confirmed.** The dark-money slice can't be sized from names alone.

---

## 5. EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION: **probed**

**What it is:** 6,273 campuses, 6,243 open. By owner: 2,047 public, 1,901 private nonprofit, 2,325 for-profit.

**Checked**
- Completer debt ÷ 10-year earnings, ranked against peers with the same owner type and main award.
- Counted schools under $30K at 10 years, by owner.
- Counted the repeats: campuses vs parent IDs (OPEID6) vs distinct earnings/debt pairs.

**What came back**
- The triage filter (500+ undergrads, earnings < $30K, completer debt > $20K) finds **6 schools, 9,800 students**.
  - Why so few: completer debt tops out at **$43,021**, because this is undergrad federal loans only. No Parent PLUS, no grad debt.
- For-profit certificate schools (1,777): median earnings **$27,393**, median debt **$9,500**. The problem is low pay, not big debt.
- Under $30K at 10 years:

| Owner | Share of campuses with earnings data | Undergrads |
|---|---|---|
| For-profit | **49%** (850 of 1,732) | 188,081 |
| Private nonprofit | 6.4% (91 of 1,414) | 78,218 |
| Public | 3.3% (65 of 1,957) | 52,319 |

- **The 850 for-profit campuses are only 572 parent IDs and 571 distinct number pairs.** Outcomes repeat across branches.
- The top of the ratio list:
  - **Strayer** fills 14 of the top 25 with one repeated number: $40,621 debt, $40,092 earnings.
  - HBCUs (Allen, Benedict, Lane, Miles, Livingstone, Shaw). The driver is low graduate earnings, a known pay gap by race, not heavy debt.

**Hit means:** named chains where students borrow a lot and earn little.
**Miss means:** low earnings but small debt, which is the known cosmetology/certificate story.
**Boring explanation:** heavily reported; it's what the gainful-employment rule targets. **Confirmed.**
NUC University's 27 Puerto Rico campuses all sit under $30K. Puerto Rico wages explain that.

---

## New data traps

- **Scorecard outcomes repeat across branch campuses.** Earnings, debt, repayment and default are copied from the parent (OPEID6) to every branch.
  - Strayer: 27 campuses, 1 parent, 1 number.
  - Empire Beauty: 73 campuses, 11 parents.
  - Count by OPEID6, never by campus.
- **Google creative table: non-US USD spend ranges are placeholders.** Every non-US row reads $0–100. Only sum USD on `REGIONS='US'`.
- **EIA outage "without major events" can still hold a hurricane.** Altamaha EMC never did the storm-day split: 17,060 of 17,310 minutes stayed in.
  - Check with-minus-without before calling anything chronic.
- **EIA sales: DATA_TYPE 'I' rows are the state adjustment rows** (utility 99999, 177 rows).
- **EIA sales: rooftop-solar companies (Sunrun, Sunnova) sit in Part A Bundled** as "Behind the Meter" owners, with up to 57K "home customers".
- **REPEX: 83% of US refusals sit on non-current records.** Filter `REGISTRATION_REGISTRATIONSTATUS='ISSUED'` before ranking countries, or the US looks twice as secretive as it is.
- My own miss: Snowflake regex has no `\b`. The first ZIP-targeting share (Q16) read 0 because of that; Q19 redid it right.

---

parked: other agents share this scratchpad and overwrote a runner named `run.py` mid-run. My Q1 went through the wrong script and its output was lost, but it still counts against the budget.
