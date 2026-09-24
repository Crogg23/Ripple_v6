# Deep pass 7, round 2: five tables, 2026-09-24

Chris's words: "no i want coverage first - basically a menu to choose from. Because im not going to spend time on something we found now if its trivial compared to what we could find - get me?" ... "im talking about the other 560 somethin marts" ... "go"

Door: Python only. Tag `coverage-r2-2026-09-24`. **24 SQL statements** (budget 35), plus the 2 session lines on each of 5 connections. All SQL is in `deep-7.sql`, numbered [1] to [24].
Every person or company named below is a **data match, not verified against primary records**.

## The menu

| Table | Verdict | The one number |
|---|---|---|
| HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS | **live** | After the 2021 pay change, new rural clinics flipped from hospital-owned to for-profit storefronts: for-profit share of new enrollments went from 27% (2020) to 56% (2023). One chain, Fast Pace, holds **189 clinics under 48 NPIs**, all enrolled from Nov 2021 on |
| HEALTH__FED_CMS_HOSPICE | **live** | Houston, not LA: **five hospices in one suite**, 7322 Southwest Fwy Suite 610, "Rooms A to E", certified in 8 weeks in 2023. Another 6 share one phone in one Rosedale St building. Harris County: 16.7% of hospices share a phone with another hospice, against 4.5% nationally |
| HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | **live** | Reliant Care Management (MO/KS, 32 homes) drew **3.4x the harm citations per bed of its own states**: 152 against 45 expected, 70 of them at immediate-jeopardy level. The median chain sits at 0.98x |
| FOREIGN_INFLUENCE__FED_FARA_BULK | probed | **94 ex-members of Congress** filed FARA short forms after leaving office. 5 filed in 2025, including Rod Blagojevich (Bosnia) and Chaka Fattah (Liberia). The revolving door is a known story, and there are no dollars in this pull |
| HEALTH__FED_CMS_HOSPITAL_COMPARE | probed | The star angle is weak: 21% of 1-star hospitals vs 8% of 5-star paid one officer more than their charity care, on 47 and 72 hospitals. **Bigger news for F-003:** 141 of its 249 hits (57%) are hospitals too small to get a star |

---

## 1. Rural health clinics: **live**

**Rows:** 5,530 enrollments, one per clinic. CCN, NPI and ASSOCIATE_ID are all filled.

### A mechanic worth knowing
- The CCN's last four digits encode the clinic type. 3400-3499, 3975-3999 and 8500-8899 mean provider-based (the clinic is part of a hospital). 3800-3974 and 8900-8999 mean freestanding.
- I checked this against the hospital enrollment file [17]. A hit means the RHC's owner ID (ASSOCIATE_ID) also appears as a Medicare hospital enrollee.

| CCN class | For-profit flag | Clinics | Owner is also a hospital | Share |
|---|---|---|---|---|
| provider-based | N | 3,149 | 3,062 | **97.2%** |
| provider-based | P | 330 | 311 | 94.2% |
| freestanding | N | 367 | 87 | 23.7% |
| freestanding | P | 1,676 | 13 | **0.8%** |

- The state matches on 99% of those hits. The CCN split is real.

### What was checked [15]
- I read the date built into ENROLLMENT_ID (the O is followed by YYYYMMDD) and counted new enrollments by month, split by CCN class and for-profit flag.

| New enrollments | Total | Provider-based | Freestanding | For-profit |
|---|---|---|---|---|
| 2018 | 308 | 237 (77%) | 71 | 97 (31%) |
| 2020 | 389 | 298 (77%) | 91 | 104 (27%) |
| 2021 Jul-Dec | 199 | 57 (29%) | 142 | 130 (65%) |
| 2022 | 312 | 119 (38%) | 193 | 172 (55%) |
| 2023 | 344 | 115 (33%) | 228 | 193 (56%) |
| 2024 | 259 | 103 (40%) | 156 | 159 (61%) |
| 2025 | 207 | 74 (36%) | 133 | 127 (61%) |

- The break comes in mid-2021. The 2021 federal spending law (Consolidated Appropriations Act, 2021) changed RHC pay from April 2021. It raised the per-visit cap for independent clinics on a climb through 2028, and it capped new hospital-owned clinics. Worth confirming the exact rule text before any writing.
- There was no big year-end-2020 rush to beat the grandfather date: December 2020 had 34 provider-based enrollments, against about 25 in a normal 2020 month.
- For-profit freestanding clinics [22]: **191 in the 30 months before July 2021 (6.4 a month), 731 in the 54 months after (13.5 a month).** That is 2.1x the monthly rate.

### Who is doing it [16], [22]

| Owner (legal name in file) | Clinics since Jul 2021 | States | NPIs |
|---|---|---|---|
| **Fast Pace (all entities)** | **189** | TN, IN, MS, NC, AR, KY, AL | 48 |
| Williams Medical Group Practice LLC | 33 | KS, OK | 33 |
| Access Medical Clinic (3 legal names) | 31 | AR, TX, AL, TN, IN, OK | 31 |
| DCS Medical PA | 14 | TX | 14 |
| Rural Urgent Care LLC | 12 | AL | 12 (all Jun-Aug 2025) |

- The triage lead checks out: NPI 1316602774 is **FAST PACE MEDICAL CLINIC PLLC, TN, with 75 clinics**. All 75 are freestanding and for-profit, enrolled 2021-11-23 to 2025-05-22.
- Every Fast Pace clinic in the file was enrolled on or after 2021-11-23. It is **26% of all for-profit freestanding RHC enrollments since July 2021**.

### Walking the chain
- **Hit means:** an urgent-care chain turned its storefronts into Medicare rural health clinics right after Congress raised the independent-clinic pay cap. One chain then took a quarter of the new for-profit slots.
- **Miss means:** if Fast Pace's clinics predated 2021 or were hospital-owned, this would be the hospital-system boring case.
- **Boring explanation:**
  - Hospital systems legitimately run many clinics. That is true for provider-based clinics, 97% of which are hospital-owned. **Ruled out for Fast Pace:** freestanding and for-profit, with 0.8% of its class tied to a hospital.
  - Survivorship: the file holds only clinics enrolled today, so older years are undercounted. That shrinks old counts evenly. It does not explain the switch from provider-based to freestanding. **Partly ruled out.**
  - The law may be doing exactly what Congress meant, which is more rural clinics. The story is who captures the higher rate and whether the clinics are really rural. **Not ruled out; it is the frame.**
- **Traps:**
  - No RHC owner file is in the warehouse, so "private equity" cannot be tested here. PECOS owner data for RHCs is not landed.
  - The enrollment ID date is when the enrollment was created. A change of owner may re-date it.
  - KY/TX/TN lead the state counts partly because they are rural (triage's boring note). Fast Pace's 189 are a separate thing.

---

## 2. Hospice roster: **live** (Houston)

**Rows:** 6,852 certified hospices, one per CCN. Certification dates run 1983-11-01 to 2025-10-15.
Round 1 (deep-7) already found LA's shared addresses in the enrollment file. This pass used what only this table has: **phone number and county**.

### What was checked [12]
- I grouped hospices by county and certification year, and counted how many share a phone number (10 digits, punctuation stripped) with at least one other certified hospice.
- Denominator: all certified hospices in the county.

| County | Hospices | Certified 2019+ | Certified 2024+ | Share a phone | In a 3+ phone group |
|---|---|---|---|---|---|
| **All US** | 6,852 | 42.9% | 6.0% | **4.5%** (309) | 115 |
| Los Angeles, CA | 1,274 | 77.0% | 3.0% | 2.9% (37) | 14 |
| **Harris, TX** | 221 | 71.0% | 12.2% | **16.7%** (37) | 19 |
| **Bexar, TX** | 137 | 62.0% | 4.4% | **14.6%** (20) | 10 |
| **Clark, NV** | 155 | 79.4% | **25.2%** (39) | 6.5% | 7 |
| Maricopa, AZ | 159 | 67.9% | 2.5% | 5.0% | 3 |
| Dallas, TX | 126 | 46.8% | 9.5% | 4.0% | 0 |

- LA stopped growing: 38 certified since 2024, 3.0%. California's state license freeze is the likely reason; not checked here.
- **Clark County (Las Vegas) is still growing**: 39 of 155 certified since 2024, 4x the national share.
- **Houston's signature is shared phones**: 16.7% of Harris County hospices share a phone with another hospice.

### The Houston buildings [13], [14], [24]

| Address | Hospices | Phone | Certified |
|---|---|---|---|
| **7322 Southwest Fwy, Suite 610, "Room A" to "Room E"** | **5** (Origins, Timeless Moments, Heart & Soul, Loving Hands, Blue Rose) | 4 share (281) 410-1013; Room D lists none | 2023-04-13 to 2023-06-08 |
| 2922 Rosedale St, suites 1200-1410 | 6 (Loving Touch, Celestial, Grand, Houston First, Eternal Light, Specialty), plus 2 more on other phones | all 6 on (713) 874-1234 | 2022-04-01 to 2022-10-14 |
| (same phone, other addresses) | Heritage Hospice (Houston), Compassion Hospice of Texas (San Antonio) | (713) 874-1234 | 2020-12-23, 2022-02-04 |
| 7207 Regency Square Blvd, Suite 260-23/26 | 4 (Veteran Memorial x2, Kush, Memorial Health) | 3 on (623) 565-3922, an Arizona area code | 2022-10-19 to 2024-01-28 |
| 2646 S Loop W, Suites 635 and 440D | 3 (Blue Stream, Life Wave, Suncrest) | all (713) 667-7202 | 2021-05-14 to 2022-11-23 |

- The (713) 874-1234 group: 8 hospices with **8 different brand names**. 4 land in the enrollment file, and they carry **4 different owner IDs** (Tulip Hospice LLC, New Dawn Hospice Inc, Eternal Light, Grand Hospice), incorporated 2018-12 to 2021-07.
- Outside Texas, other phone groups tie LA and Nevada: (818) 470-6457 covers 6 hospices in Glendale, Thousand Oaks, Burbank, Camarillo, North Hollywood and Phoenix. (323) 552-3300 links LA to 8925 S Pecos Rd, Henderson NV, round 1's 7-hospice address.

### Walking the chain
- **Hit means:** several licenses with different names, owner IDs and even "rooms" share one phone line and one suite. That is the hospice-mill signature, it is in Texas, and all of them are on the current certified roster.
- **Miss means:** if shared phones were only real chains using one brand, it would be ordinary central scheduling. Moments, Agape, Beacon, Brighton and Harbor are exactly that: same brand, one phone.
- **Boring explanation:**
  - A shared answering service or billing company could own the phone line. **Not ruled out.** Five licenses in one suite split into lettered rooms is harder to explain that way.
  - LA hospice fraud is widely covered (LA Times, ProPublica, CMS). Houston's clusters and Clark County's growth since 2024 are less covered, but Texas hospice prosecutions exist. **Partly new.**
- **Traps:**
  - `(909) 000-0000` is a filler phone on 4 San Bernardino hospices; exclude it.
  - 876 of the 6,852 certified CCNs (13%) have no row in the hospice enrollment file [14], so they have no owner ID. In the clusters above, most misses are new letter CCNs (A9xxxx, B4xxxx); not checked across the whole file.
  - The warehouse has no hospice owner file, so the people behind these companies cannot be reached here.

---

## 3. Nursing-home deficiencies: **live**

**Rows:** 418,479 health citations at 14,632 homes. Survey dates run 2017-03-23 to 2026-05-20, and 84% are from 2023 on.

### What was checked [20], [21], [23]
- Severity letters [20]: G-I = actual harm; J-L = immediate jeopardy. The file holds 23,087 harm-level citations, 9,661 of them at J-L.
- The dispute flags (IDR/IIDR) read Y on about 1% of rows or fewer, in every severity letter. Nothing to filter on.
- **Lining up years:** the penalty file runs 2023-06-17 to 2026-05-13 (13,710 fines, 2,470 payment denials). I kept only citations from 2023-06-17 on: 19,953 G-L citations.
- **Peer comparison:** for each state, harm citations per certified bed. A chain's "expected" count = its beds × its own states' rates. Observed ÷ expected = O/E. Chains = CMS's CHAIN_ID in FED_CMS_NURSING_HOME, joined by padded CCN.

| Chain | Homes | States | Harm citations | Expected | O/E | Immediate jeopardy (J-L) | Homes with harm on 2+ surveys | Fines |
|---|---|---|---|---|---|---|---|---|
| **Reliant Care Management** | 32 | MO, KS | **152** | 45.2 | **3.37** | **70** | 19 of 32 | $3.87M |
| **Bria Health Services** | 15 | IL | **195** | 81.7 | 2.39 | 31 | 14 of 15 | $5.44M |
| Plainview Healthcare Partners | 12 | TN, FL, KY | 37 | 10.8 | 3.43 | 28 | 5 | $0.64M |
| Hurlbut Care | 13 | NY | 28 | 3.4 | 8.19 | 12 | 1 | $0.91M |
| Ephram Lahasky | 23 | 10 states | 64 | 25.7 | 2.49 | 42 | 9 | $2.30M |
| Tutera Senior Living | 26 | 5 states | 117 | 63.0 | 1.86 | 28 | 18 | $2.57M |
| Genesis Healthcare (big-chain reference) | 187 | many | 330 | 243.1 | 1.36 | 178 | n/a | n/a |
| Life Care Centers (big-chain reference) | 194 | many | 198 | 297.9 | 0.66 | 61 | n/a | n/a |

- Spread across about 300 chains with 10+ homes: **median O/E 0.98**. 14 chains at 2x or more, 56 at 1.5x or more, 154 under 1x.
- Round 1's fire-citation pass found chains at a median of 1.00x and a max of 1.95x. Harm citations spread much wider.

### "Cited for severe harm and never pay": dead
- Harm-cited homes in the top chains are fined **more** often than their states predict.
- Reliant: 2 unfined harm homes against 6.8 expected. Bria: 1 against 3.3.
- The penalty file records fines imposed, not paid, so "never pay" cannot be tested either way.

### Walking the chain
- **Hit means:** a mid-size chain draws 2-3x the harm citations its own states' inspectors hand out per bed, across most of its homes, on separate visits.
- **Miss means:** if O/E sat near 1, the chain would be as bad as its neighbors and the count would only reflect size or state strictness.
- **Boring explanation:**
  - State survey strictness: **ruled out** by comparing each chain with its own states per bed. That also covers the Illinois abuse-flag trap for Bria.
  - One bad survey can produce many tags: **ruled out for Reliant and Bria**, with harm on 2+ separate survey dates at 19 of 32 and 14 of 15 homes. Not ruled out for Hurlbut: harm at 4 of 13 homes, and only 1 on 2+ surveys.
  - Chain membership is CMS's current label. A home bought after its citations still counts toward the new chain, and the CHOW flag is a constant (trap), so timing cannot be checked. **Not ruled out.**
  - F-021 and F-029 already cover nursing-home chains. This cut, harm per bed against own state, is new.
- **Trap:** no home in FED_CMS_NURSING_HOME has a null CHAIN_ID, so independents carry some other value. "About 300 chains" may include one bucket of independents. Unresolved; it does not move the top of the list.

---

## 4. FARA bulk: **probed**

**Rows:** 221,455, four files stacked [1]:

| File | Rows | What is filled |
|---|---|---|
| RegistrantDocs | 152,224 | document stubs; FOREIGN_PRINCIPAL_COUNTRY on 37,452 |
| ShortForms | 44,508 | the individual agents: first and last name, date |
| ForeignPrincipals | 17,663 | principal, country, dates, active flag |
| Registrants | 7,060 | the firm. **Its name sits in PERSON_NAME, not REGISTRANT_NAME** |

- Active flag [6]: 807 foreign principals are active, at 504 registrants in 151 countries. Every active row has no termination date, so the flag agrees with the dates.
- **There are no dollar amounts in any of the four files.**

### Countries [7]: distinct US registrants, by principal registration date

| Country | 2017 on | Active now | All time |
|---|---|---|---|
| Ukraine | **89** | 13 | 137 |
| Qatar | 85 | 30 | 106 |
| Saudi Arabia | 69 | 28 | 185 |
| Japan | 59 | **50** | 551 |
| China | 55 | 14 | 196 |

- Top firms by active principals [8], [10]: Mercury Public Affairs (16 active, 15 countries), Dickens & Madson Canada (15), MMGY Global (14; its principals look like tourism boards), BGR Government Affairs (13), and Sonoran Policy Group (13).

### The join that could make it a story [9], [11]
- **Checked:** short-form agents matched to Congress legislators by first and last name. I kept only names held by one legislator, terms ending 1970 or later, and short forms filed **after** the member left office.
- **Result:** 174 name-and-registration pairs; 133 after leaving office; **94 distinct people**. 26 filed a first post-office short form in 2017 or later.
- **Filed in 2025:** Robert Wexler (Ballard Partners), Rod Blagojevich (RRB Strategies LLC; Bosnia & Herzegovina), Chris Stewart (Skyline Capitol; the firm's principals include Azerbaijan, Rwanda, Taiwan and Turkey), Chaka Fattah (Blackwood International Strategic Advisors; Liberia), and John Seymour (Sasakawa Peace Foundation USA; weak match).
- **Second-field check:** firms named for the member confirm the match: Moran Global Strategies, Waxman Consulting, Harper & Bailey, Nickles Group, Kemp Partners, Solarz Associates, Breaux Lott Leadership Group, and RRB (Rod R. Blagojevich).
- **One sure false match:** "Stephanie Jones" filed in 2019. Rep. Stephanie Tubbs Jones left office in 2008 because she died. Doubtful common names: David Levy, Timothy Johnson (Quebec Government Office), James Tucker, John Seymour.

### Walking the chain
- **Hit means:** ex-members of Congress keep registering as foreign agents. Two of the 2025 filers, Fattah and Blagojevich, have federal convictions on the public record (not checked here).
- **Miss means:** if matches were mostly common-name collisions, there would be no list. Most of the list is well-known real cases (Boxer, Vitter, Lott, Breaux, Daschle, Gephardt).
- **Boring:** OpenSecrets Foreign Lobby Watch and POGO already track this, and the 2025 names made the news. **Not ruled out: known story.**
- **Traps:** REGISTRANT_NAME is empty in the Registrants and ForeignPrincipals files; use PERSON_NAME in the Registrants file. Short-form dates include junk like 1900-01-07.

---

## 5. Hospital Compare: **probed**

**Rows:** 5,432, one per FACILITY_ID (the CCN), all distinct.

### Ratings [18]
- 3,182 hospitals are rated (58.6%). 2,250 are not (41.4%).
- The unrated: footnote 16 (too few measures) on 1,341, 930 of them critical-access hospitals. Footnote 19 on 810, mostly not acute care.

### The F-003 join [19]
- F-003's set, rebuilt from its own SQL, is 919 nonprofit hospitals: 2022 officer pay (990) against 2022 charity care (HCRIS).
- **Land rate: 919 of 919 CCNs are in Hospital Compare. State agrees on 919 of 919.**

| Stars | Hospitals | Median beds | Median top officer | Median charity care | Top officer > charity | Charity per discharge |
|---|---|---|---|---|---|---|
| 1 | 47 | 134 | $437K | $1.49M | 21.3% (10) | $411 |
| 2 | 140 | 165 | $462K | $2.34M | 15.7% (22) | $343 |
| 3 | 211 | 122 | $496K | $2.67M | 16.6% (35) | $576 |
| 4 | 206 | 134 | $478K | $2.70M | 17.0% (35) | $587 |
| 5 | 72 | 198 | $512K | $6.20M | 8.3% (6) | $719 |
| **No rating** | **243** | **25** | $226K | **$133K** | **58.0% (141)** | $558 |
| All | 919 | 76 | $401K | $1.24M | 27.1% (249) | $512 |

- 1-star hospitals do **not** pay their top officer more: $437K against $512K at 5-star.
- The 1-star vs 5-star gap in "officer over charity" is 10 hospitals against 6. Too thin to stand on.

### Walking the chain
- **Hit means:** low stars go with officers out-earning charity care. The rate is 2.5x worse at 1-star than at 5-star, but on 10 hospitals.
- **Miss means:** if pay tracked stars, 1-star executives would earn more. They earn less.
- **Boring:** 5-star hospitals are bigger (198 beds) with bigger charity budgets, so size drives the ratio. **Not ruled out.**
- **The real catch, for F-003:** **141 of its 249 hits (57%) are unrated hospitals with a median of 25 beds and 242 discharges a year.** At a tiny rural hospital, one $226K salary tops a $133K charity-care line. F-003's "27%" drops to **16% (108 of 676)** among hospitals big enough to get a star.
- **Trap:** there is no system or chain field in this table, so "cluster in chains" cannot be tested here.

---

## New data traps
1. **FARA REGISTRANT_NAME is empty** in the Registrants and ForeignPrincipals files. The firm name is in PERSON_NAME, and plain.json calls that column "the person".
2. **FARA has no money columns** anywhere in the four files.
3. **Hospice phone `(909) 000-0000`** is a filler on 4 rows.
4. **RHC CCN digits code the ownership model**: provider-based vs freestanding. Checked against the hospital enrollment file (97% vs 0.8%).
5. **F-003's 27% leans on tiny unrated hospitals**: 57% of its hits. Among rated hospitals it is 16%.
6. **Nursing-home CHAIN_ID is never null**, so independents carry some other value. Check before treating "chain" as one group.

## Housekeeping
- The shared scratchpad root is used by other agents. My first batch wrote `b1.sql`, `runq.py` and `count.txt` there at 14:49, and `b1.sql` already existed; I may have overwritten another agent's file. Everything after that ran from `scratchpad/deep7r2/`.

**Statements: 24 of 35.**
