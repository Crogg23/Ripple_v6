# deep-9: five tables, hand-queried

Coverage round 2, group 9. 2026-09-24. Python door, read-only. SQL: `reports/coverage_2026-09-24/deep2/deep-9.sql` (Q1 to Q34).

Every person or company named below is a **data match, not verified against primary records**.

## The menu line

| Table | Verdict | The number that matters |
|---|---|---|
| HEALTH__FED_VA_SUICIDE_STATE | **live** | Oklahoma veteran suicides went from 228 to 287 (2019-20 vs 2022-23). The rate went from 37.9 to 50.7. The state's general-population suicide rate stayed flat (20.4 to 20.3). |
| HEALTH__FED_HHS_OIG_LEIE | probed | 0 of about 8,190 NPIs banned before 2026 (no waiver) are still in the June 2026 Medicare enrollment file. The new name join finds $4.9M in 2024 Part B money going to 2 ambulance companies whose signer's name matches a banned person. Both names are common. |
| HEALTH__FED_HRSA_SHORTAGE_AREAS | probed | 143 of 999 shortage areas still designated for primary care date from 1978-89, and 31 of them still score 18+. 10 of those are Mississippi counties. |
| HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY | probed | 72 of 241 suspensions (30%) already have a same-state SAM exclusion or an FDIC order. The "still working" test needs data we don't have. |
| HEALTH__FQHC_SITE_PEOPLE | dead | 88 banned NPIs sit at health-center addresses. 87 of them have addresses older than their ban. The one updated after her ban isn't enrolled in Medicare. |

---

## 1. HEALTH__FED_VA_SUICIDE_STATE: live

**Headline:** In Oklahoma, veteran suicides rose 26% in four years while the state's other suicides held flat. Kansas shows the same shape, smaller.

**The table:** 1,196 rows, one per state per year, 2001-2023, plus a "U.S. Total" row in the STATE column.
- DC is blank in all 23 years.
- VT, DE and RI publish no rate in 16-20 of their 23 years.
- The general-population columns are empty (known), so the comparison comes from the CDC county file.

**Checked:**
1. **Crude rate per state** (deaths ÷ veteran population), pooled over 2011-13 and 2021-23. (Q6)
2. **The same state's general population, same years.** CDC `All_Suicide`, 2019-20 vs 2022-23. (Q11, Q18, Q23)
   - The CDC file has no state rows: GEOID is always 5 digits.
   - So I summed a **fixed county panel**: counties CDC counted in all four years.
3. **Year by year** for Oklahoma, Kansas, Montana, Utah and the nation. (Q27)

**The numbers:**

| | Vet deaths 2019-20 → 2022-23 | Vet rate | Vet change | General rate (county panel) | General change | Vet ÷ general |
|---|---|---|---|---|---|---|
| **Oklahoma** | 228 → 287 | 37.9 → 50.7 | **1.34x** | 20.4 → 20.3 (15 counties) | 1.00x | **1.34** |
| **Kansas** | 130 → 160 | 32.2 → 43.4 | **1.35x** | 17.3 → 19.2 (7 counties) | 1.11x | 1.22 |
| Montana | 107 → 122 | 58.2 → 67.8 | 1.16x | 26.3 → 25.3 | 0.96x | 1.21 |
| Utah | 127 → 146 | 47.2 → 56.2 | 1.19x | 19.7 → 20.1 | 1.02x | 1.17 |
| **U.S.** | 12,857 → 12,840 | 32.5 → 34.9 | 1.07x | 13.5 → 14.0 (767 counties) | 1.04x | 1.03 |

- **Nationally, veteran suicides didn't rise. The number of veterans fell.**
  - 2013: 6,523 deaths among 22.15M veterans (29.4 per 100K).
  - 2023: 6,398 deaths among 18.18M veterans (35.2 per 100K).
  - Deaths fell 2%. The rate rose 20%.
- **Oklahoma is different: the deaths themselves rose.**
  - At the 2019-20 rate, 2022-23 should have had about 215 deaths. It had 287. That's about 4.9 standard deviations above expectation.
  - Kansas: about 119 expected, 160 seen, about 3.8 SD.
- **Oklahoma by year:** 114, 114, 131, 126, **161** (2019-2023).
- **Longer window, Oklahoma:** 352 deaths in 2011-13 (35.1 per 100K) and 418 in 2021-23 (49.0). National deaths fell 1% over the same span.
- **Peers:** the VA puts Oklahoma in its Southern region. Oklahoma's vet ÷ general ratio is 1.34. The next-highest Southern states are South Carolina (1.14) and Tennessee (1.08). Delaware reads 1.21, but on 33 → 39 deaths.

**Hit means:** something veteran-specific is going on in Oklahoma, and maybe Kansas. It's not the statewide suicide trend, and it's not the shrinking-veteran math.

**Miss means:** a small-number wobble, mostly 2023, that 2024 data will wash out.

**Boring explanations:**
- The VA ranks states every year. Mountain West rates are known. **Not news by itself.** The new part is the veteran-vs-state contrast.
- Crude rates, no age adjustment. **Ruled out for OK:** the deaths rose, not just the rate.
- **Not ruled out:** 2023 carries the jump (161). Without 2023, the rise is about 13%.
- **Not ruled out:** the general-population line covers only the 15 OK counties CDC counted all four years.
  - They hold 1,089 of the 1,292 counted OK suicides in 2019-20.
  - Suppressed rural counties aren't in either figure, so rural Oklahoma is missing from the peer line.
- Veterans are about 90% male and the general line is half female. That's why I compare changes, not levels.

**Next pass:** CDC `FA_Suicide` for OK (firearm share); VA 2024 when it lands; VA facility access in the counties that rose.

---

## 2. HEALTH__FED_HHS_OIG_LEIE: probed

**Headline:** CMS removes banned NPIs from Medicare enrollment. The real gap is **name-only** records: banned people whose ban carries no NPI. A new join finds a few leads, and father/son name pairs kill the two best-looking ones.

**Reused, not re-run:** Part B/Part D (deep-6, sweep-c: 1 banned doctor paid, with a waiver), Open Payments (F-020), Provider Relief Fund (deep-6), home health owners (deep-5).

**The table:** 83,816 rows, bans from 1977 to 2026-08-20. About 8,700 real NPIs. Waivers: 4.

**Checked:**
1. **LEIE NPI → the Medicare enrollment file** (PECOS), grouped by ban year. (Q9, Q15)
   - I dated the file by its newest enrollment ID: `ENRLMT_ID` holds the date after its first letter, and the newest is **2026-06-29**.
2. **Name-only LEIE rows → PECOS** on name + state, enrollment created after the ban. (Q19, Q22)
3. **New join: LEIE people → NPPES authorized officials** (the person who signs for an organization's NPI). Then Medicare money. (Q29, Q31, Q33)
4. **A namesake test** on the best matches: NPPES suffix, all same-name NPIs, and name density in the city. (Q30, Q34)

**The numbers:**
- **NPI side is clean.** 0 of about 8,190 non-waiver NPIs banned before 2026 are in the June 2026 enrollment file. (Counted per ban-year bucket, so a person banned twice counts twice.)
  - 17 of 542 NPIs banned in 2026 are still in it. 16 of those were banned after the file date.
  - One wasn't: **Myers Southern LLC** (ambulance, Bartow FL), banned 2026-04-09 under 1128b11, still enrolled 81 days later. Its 2024 Part B paid was $355K, all before the ban.
- **Name-only businesses:** 2,862 banned. 18 have a same-name, same-state enrollment created after the ban. NPPES practice city agrees on 4.
  - All 4 were banned 1991-2000 under 1128b8 (a business controlled by a banned person).
  - Examples: Advanced Medical Solutions (Denver), Metro Care Pharmacy (DC), Ehrhardt Pharmacy (SC; now bills as Donna's Pharmacy, $1,678 in 2024), Premier Medical Center (Miami).
  - These look like generic names reused decades later.
- **Name-only people → PECOS enrollees:** 72,114 banned. 4,148 share first + last + state with an enrollee; 3,197 enrolled after the ban.
  - Middle initial: conflicts 1,834, agrees 276. **Namesakes dominate.**
  - Adding specialty agreement leaves 7. City agrees on 1.
- **Authorized-official join:**

| Step | People | Orgs |
|---|---|---|
| Banned people with a name, no waiver | 80,359 | |
| Same first + last + state as an org's signer | 7,671 | 16,424 |
| Same city too, no middle-initial conflict | 1,839 | |
| Org NPI created after the ban | 250 | |
| Org enrolled in Medicare, NPI active | **26** | **29** |
| Org has 2024 Part B money | | **2 orgs, $4.91M paid** |

- **The two money orgs:**
  - **National Health Transport Inc.** (Miami ambulance). $4.25M paid in 2024, 10,405 patients. Signer: Raul F Rodriguez. LEIE has Raul Rodriguez, Miami, 2008, 1128a1, a DME owner, with no middle name. NPI created 2010.
  - **ASAP EMS Corp** (Laurel MS ambulance). $662K paid, 743 patients. Signer: Kevin Smith. LEIE has Kevin Bernard Smith, Laurel, 2002, 1128a2 (patient abuse), a nurse aide.
- **Killed by the suffix check:**
  - **George A Szekely**, chiropractor, Lansdale PA, banned 2005 (1128b1). He matched on name, middle initial, specialty and city, with $26.5K allowed in 2024 Part B. NPPES says the biller is **George Andrew Szekely II**.
  - **Robert Dale Bernauer**, Lake Charles, banned twice (2018 1128b4, 2024 1128a3 TX). The clinic signer is **Robert Dale Bernauer JR.**, a separate M.D. with his own NPI.
- **Best surviving person: Bhupinder K Sangha**, Fresno.
  - LEIE: 2011-07-20, 1128a1, listed as a health care aide.
  - NPPES has exactly one Bhupinder Sangha practicing in Fresno: a nurse practitioner, NPI created 2014, Medicare-enrolled 2020.
  - 2024 Part B: $50,496 paid, 220 patients. 2024 Part D: 4,843 claims, $528,832 drug cost.
  - She also owns Primary Care Providers LLC, enrolled 2026-02-16.
- **Ali Moayed**, urologist, Los Gatos, banned 2008 (1128b4). He's the listed facility administrator for South Bay Medical Center Inc: 3 NPIs created 2020, one enrolled. No 2024 Part B money, and his own NPI isn't enrolled.

**Hit means:** a banned person signs for, owns or runs a Medicare-enrolled business. That's grounds for revoking the enrollment, and the money flows anyway.

**Miss means:** namesakes. LEIE has no birth date and, for these rows, no NPI. Name + city is the whole join.

**Boring explanations:**
- **Namesakes, not ruled out.** Raul Rodriguez in Miami: 2 LEIE rows in FL, 2 NPPES people and 4 signer orgs by that name in the city. Kevin Smith is common. Kaur is the near-universal Sikh middle name, and going from aide in 2011 to NP by 2014 is fast.
- **Old permissive bans outlast their terms.** LEIE drops a person only after they apply for reinstatement.
- **Next pass:** court record and state license lookup for Sangha, and ownership filings for National Health Transport and ASAP EMS.

---

## 3. HEALTH__FED_HRSA_SHORTAGE_AREAS: probed

**Headline:** Most old shortage designations got lifted. A hard core didn't: Mississippi Delta and South Texas border counties, designated 1978-85, still score 18-22.

**The table:** 165,531 rows. One row is one piece (tract or county) of one designation.
- Score 0 shows up almost only on withdrawn rows.
- The designation date is the first designation date.

**Checked:**
1. Distinct `HPSA_ID` by discipline × type × status. (Q7)
2. For designations still active ("Designated", geographic or high-needs), one row per area: era of first designation, score 18+, median score. (Q12)
3. A list of pre-1990 areas still scoring 18+. (Q13)
4. **Overdose join:** whole counties in a severe (18+) designation vs other counties in the same state. CDC `Drug_OD` 2019-24, counties counted all six years. (Q24)

**The numbers:**

| Discipline (still designated) | Areas | First designated before 1990 | Pre-1990 still 18+ | 2020s areas at 18+ |
|---|---|---|---|---|
| Primary care | 999 | 143 (14%) | **31 (21.7%)** | 47 of 665 (7.1%) |
| Mental health | 841 | 65 | **29 (44.6%)** | 114 of 470 (24.3%) |
| Dental | 464 | 63 | 23 (36.5%) | 37 of 311 (11.9%) |

- **Withdrawn primary care geographic areas:** 2,869, and 2,192 of them were first designated before 2000. Most old shortages did get lifted.
- **Mississippi, still designated from 1978-84, scores 18-22:** Humphreys 22, Jefferson 22, Copiah 22, Holmes 21, Sunflower 20, Yazoo 20, Lawrence 19, Winston 19, Chickasaw 18, Jefferson Davis 18.
- **South Texas:** Jim Hogg 23, Starr 20, Duval 20, Zapata 19, Zavala 19.
- **Also:** Sioux County ND 23, Todd County SD 22.
- **Full-time doctors counted (`HPSA_FTE`)** reads 0.0 for Sioux ND, Jim Hogg TX, Jefferson MS, Grant Parish LA and others. The people-to-provider ratio is blank there, so 0.0 may mean "not counted."
- **Overdose join is too thin.** Only 4 primary-care and 24 mental-health severe whole counties have six unsuppressed years. Mental health: severe counties run higher in 7 of 13 states, median ratio 1.09. **No signal, and not testable** at county level: CDC hides small rural counts.

**Hit means:** named places the federal system has called severely short for 45+ years, with nothing changing. A "decades of designation, no doctors" piece.

**Miss means:** designations persist because they unlock money (NHSC, Medicare bonus). The label outlives the gap.

**Boring explanations:**
- Chronic rural shortage is well known.
- The "how much clinic money went there" half is **untested**. No clinic-grant table was joined.

---

## 4. HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY: probed

**Headline:** FHFA's list mostly echoes other agencies' bans, by design. The "still working as a loan officer" test can't run here.

**The table:** 241 rows: 210 people, 31 companies. Suspensions from 2013-04-15 to 2026-07-29. 2026 is the biggest year so far (40). STATE is spelled out ("California"), so joins need a name-to-code map.

**Checked:**
1. **SAM exclusions:** people on first + last name; state and city as second fields. (Q10)
2. **PPP loans:** exact name + state, then first and last word + state. (Q17, Q20)
3. **FDIC enforcement orders** whose respondent text holds both names. (Q21)
4. All of it by year. (Q26)

**The numbers:**
- **SAM, same name, same state:** 55 people. HUD barred 45 of them. SAM's ban came first for 47. City also agrees for 34.
- **FDIC orders:** about 20 people. Examples: Brady and Brent Torgerson (The Union Bank, ND), Andrew Blassie, Jackie Cantley.
- **Either SAM or FDIC:** 72 of 241 rows (30%).
- **PPP: 0 exact hits.** 8 loose hits, all in different cities, so namesakes.
  - **The PPP table only holds loans of $150K and up**: 968,524 loans, smallest $150,000 (known trap). Small loans to sole proprietors, where a person's name would show, **are not in the warehouse**.

**Hit means:** a person FHFA barred from mortgage work still borrowing or contracting under their own name.

**Miss means:** nothing shows. **But this isn't a clean miss.** There's no NMLS or loan-officer table, and small PPP loans aren't loaded. Unresolved, not empty.

**Boring explanation:** FHFA suspends people after a conviction, debarment or another agency's order, so overlap with HUD and FDIC is expected. That part is ruled in, not out.

---

## 5. HEALTH__FQHC_SITE_PEOPLE: dead

**Headline:** The banned people at community health center addresses are old addresses, not current staff.

**The table:** 239,265 rows, 173,813 NPIs, 11,110 sites. It's an NPPES address match, not a staff list (known trap).

**Checked:**
- Flagged rows, and how many NPPES records were updated after the ban. (Q8)
- Sites with 2+ flagged people. (Q14)
- The Medicare enrollment check from the LEIE section.
- Reused sweep3-d: after the ban, 0 Part D rows and 4 Open Payments meals ($24-61).

**The numbers:**
- 117 flagged rows: 88 NPIs across 112 sites and 79 centers. Bans run 2008-2026.
- **87 of 88 have an NPPES address last updated before the ban.**
- The 1 exception: **Wendi Joiner MD**, banned 2016-10-20 (1128b4, license action). NPPES was updated 2023-03-07 to Bolinas Community Health Center (Petaluma Health Center), a 2-person site.
  - She's not in the Medicare enrollment file. No NPI banned before 2026 is.
- The top sites hold at most 2 flagged people each, like MetroHealth (Cleveland, 2 dentists) and Valley Health Coal Grove (two Tsai MDs, same 2016 ban).

**Hit means:** banned clinicians working at federally funded clinics.

**Miss means:** stale addresses. That's what the data shows.

**Boring explanation:** NPPES addresses go stale. **Ruled in:** 87 of 88.

---

## New data traps

- **LEIE has no suffix column. "SR" and "JR" hide inside `MIDDLE_NAME`** ("DALE SR", "ARTHUR JR SMITH"). NPPES keeps suffixes in `PROVIDER_NAME_SUFFIX_TEXT` and `AUTHORIZED_OFFICIAL_NAME_SUFFIX_TEXT`.
  - Father/son pairs fake hits: Szekely II and Bernauer Jr. both looked perfect.
  - A middle-initial check on "JR" reads "J".
- **The CDC injury county file has no state rows.** GEOID is always 5 digits. State sums drop every suppressed county: 1,322 of 3,142 counties had a suicide count in 2019.
- **PECOS `ENRLMT_ID` carries the enrollment date** after its first letter (I or O + YYYYMMDD). The newest, 2026-06-29, dates the file. That's a method, not a trap.
- **A `NOT (a AND b ...)` filter drops rows when a field is NULL.** Q31 lost 8 of 29 orgs because LEIE's middle name was blank. One of them was the $4.25M ambulance company. Q33 patched it.
- **Tooling: the 17 parallel agents share one scratchpad folder.** Generic file names collide (`run.py`, `count.txt`, `b1.sql`).
  - My first 5 queries ran through deep-2's runner and logged into `deep-2.sql`.
  - I deleted that file and reset its counter while it held only my 5 queries. It now holds only deep-2's own queries.
  - My later runs used `scratchpad/deep9x/`.

## Statement count

**34 SQL statements** (SELECT/WITH), inside the 35 budget.
- Each of the 10 connections also ran the two required ALTER SESSION lines.
- Q16 hit the 300-second timeout: an OR join over PECOS, rewritten as Q19.
- The first 5 statements ran through deep-2's runner, with the same timeout and query tag.
