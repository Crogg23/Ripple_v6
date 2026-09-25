# skeptic-g3: three deep-12 leads, attacked

2026-09-24 · round 2 skeptic · Python door · SQL in `skeptic-g3.sql`
Statements: OpenSanctions 7 (1 errored), FBI_CDE 6, FJC civil 5, shared metadata 2. All under the 12-per-lead cap.
Every person or company named is **a data match, not verified against primary records.**

## Verdicts up front

| Lead | Verdict | Grade | What changed |
|---|---|---|---|
| INTL_OPENSANCTIONS | NARROWED | B | Signal is real (91 true-DOB hits vs 5-8 fake-DOB hits). Counts shrink. Kong is 19 open, not 22. The Prince Group part is already famous |
| FED_FBI_CDE | NARROWED | B | Rank and rate hold. "No reporting gap" is overclaimed: the check can't see one agency sending offenses without clearances |
| FED_FJC_IDB_CIVIL | NARROWED | C (B as a volume story) | The 15-point default gap is mostly a filing-year effect. Matched by year, it's about 6 points |

---

## INTL_OPENSANCTIONS: NARROWED

**Claim as written:** 45 sanctioned people still listed as controlling 83 active UK companies. OFAC designee Ka On Kong is on 22 London companies.

**What I checked:**
- **O4, null test.** People on OFAC SDN or UK FCDO with a full birth date, matched to UK PSC individuals. The match: full name as a sorted token set, plus birth year and month.
  - True DOB: **91 people, 171 companies**. 76 people still hold an open control, on 132 companies.
  - Birth year shifted by -2/-1/+1/+2: **8 / 7 / 5 / 7 people**.
  - So about 7 of the 91 (~8%) are expected same-name strangers. **The aggregate is not noise.**
- **O5, strict list with open control, joined to Companies House.** **25 people** have at least one open control on a company the Companies House table marks active, **51 companies** in all. The deep pass got 45/83 with a looser name rule.
- **O3, every PSC row with surname KONG and forename starting KA.** The Ka On Kong born June 1983 shows up as 6 name/nationality variants:
  - 24 PSC rows. **19 are still open.**
  - PSC nationality: mostly "British", 3 rows "Hong Konger".
  - Postcodes: SW8, SW11, SS0, E14, WC1A.
  - No other Ka On Kong in the PSC table shares his birth month and year.
- **O5 + O1:** of Kong's 19 open companies, **14 are in the Companies House table, all Active**. 5 are missing from that table (the known 47% gap).
- **O6, OFAC SDN table:**
  - Kong: ENT_NUM 57850. DOB 03 Jun 1983, born Hong Kong, nationality Hong Kong, HK ID Z512299, "Linked To: HU, Xiaowei".
  - Luo: ENT_NUM 57522, "Linked To: PRINCE GROUP TRANSNATIONAL CRIMINAL ORGANIZATION".

**Problems in the claim:**
- **"22 companies":** it's 24 rows ever and 19 open, and only 14 of those are confirmed active.
- **"Brendon Luo is on the same OFAC action (same first-seen day)":** this contradicts deep-12's own trap (FIRST_SEEN is the day OpenSanctions picked the entry up). The SDN entry numbers are 330 apart. Luo is linked to Prince Group, Kong to Hu Xiaowei. Don't tie them together.
- **"Nationality matches":** OFAC says Hong Kong, PSC mostly says British. A Hong Kong-born British national fits both, but that's consistent, not a match.
- **The proposed disproof can't be run.** Public Companies House pages show birth month and year, never the day. Use a different second field (below).
- **Already famous:** Zhi Chen (Chen Zhi, Prince Group, OFAC TCO and UK-sanctioned, Cambodian) sits on 3 active UK companies. So do Luo and several cn/cy/kh TCO names. The US and UK Prince Group action, including London property, was widely reported (from memory, no web).
- **Leftover false hits:** Muhammad Iqbal (SDGT, Pakistan) matches a PSC with **Italian** nationality. Yi Li (Iran program, cn) matches a **British** PSC.

**What a hit means / what a miss means:**
- **Hit:** the 91-vs-~7 gap says most of these matches are the listed person, not a stranger. For Kong it's his name, birth month and year, and a Hong Kong origin that fits the PSC rows.
- **Miss:** any single match can still be a stranger. About 1 in 12 are, and the common Chinese and Muslim names carry most of that risk.
- **Asset freezes don't dissolve companies.** "Active" doesn't mean trading.

**Corrected headline:** 25 people on the US SDN or UK sanctions list match, on full name and birth month and year, a still-open controller of 51 active UK companies. A fake-birth-year control finds only 5-8 such matches, so most are real. The biggest is Ka On Kong, OFAC-listed for transnational crime and linked to Hu Xiaowei: 19 open UK controls, 14 confirmed active.

**Portfolio grade:** B. The null-test method is itself portfolio-worthy. Kong needs one outside check.

**Next join that would make it a story:**
- Kong's companies → their registered postcodes (SW8 2LE, SS0 7LP) in `CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE`. That finds every company at those addresses.
- Then corporate PSC rows (`KIND` corporate) on those companies, on COMPANY_NUMBER. That finds the owner Koke Ramen moved to.
- Outside the warehouse: search Hu Xiaowei in the SDN list and the OFAC press release.

---

## FED_FBI_CDE: NARROWED

**Claim as written:** New Mexico solved 22.7% of homicides in 2022-23 vs 56% nationally. It was 47% in 2015-19. No reporting gap.

**What I checked:**
- **F1, NM by year.**
  - Homicide clearance 2012-2017: 54-70%. **2018: 34.2%**, then 36.6, 28.4, 30.7, **22.3 (2022), 23.2 (2023)**.
  - All 12 months are present every year.
- **F1, coverage from the rate column.** OFFENSES x 100,000 / OFFENSE_RATE_PER_100K gives the population covered by reporting agencies.
  - NM: ~2.0M in 2012-19, **~1.86-1.89M in 2021-23**.
  - Albuquerque is roughly a quarter of the state. If its offenses were missing, coverage would sit near 1.5M. **So APD's offenses are in.**
- **F2, all 51.** Coverage ratio, 2022-23 over 2015-19:
  - NM: **0.936**.
  - Lower: IL 0.849, PA 0.878, WY 0.893, FL 0.898, LA 0.925.
  - NM homicide clearance 2022-23: **108 of 475 = 22.7%, last of 51.** IL is next at 32.9% (an artifact).
- **F3, nation excluding NM:** homicide clearance 57.7% in 2015-19, **56.4% in 2022-23**.
  - NM fell on **every** offense type, not just homicide.
  - Rape: 22.6% -> 8.1%. Aggravated assault: 45.6% -> 31.9%. Larceny: 17.6% -> 11.0%.
- **F4, NM monthly homicides 2016-23.** No month has offenses but zero clearances, except Feb 2018 (9/0).
- **F5:** `HEALTH__FED_CDC_WONDER` is national only. It can't cross-check NM death counts.

**The blind spot in "no reporting gap":**
- Deep-12's test, and my F4, look at state totals.
- Suppose one large agency sends its offenses but few or no clearances. The state rate sinks, and no state month ever drops to zero or under 5%. That's exactly the Albuquerque scenario.
- The drop hitting every offense type at once fits a real collapse. It fits a clearance-reporting failure at one big agency just as well.
- The 2018 break predates the 2021 NIBRS switch. When NM's agencies moved to NIBRS was not checked.
- **Not ruled out.** Coverage shows the offenses are there. It says nothing about whether the clearances are.

**What a hit means / what a miss means:**
- **Hit:** NM police, likely led by Albuquerque, close under a quarter of homicides: worst in the nation for two years running.
- **Miss:** an agency's clearances aren't reaching the FBI. Then it's a data-plumbing story, still newsworthy but a different one.
- **Also:** NM was already under the nation before the slide (47% vs 58%).

**Corrected headline:** New Mexico agencies reported clearing 108 of 475 homicides in 2022-23 (22.7%), the lowest of 51. The rest of the nation cleared 56.4%. NM's own rate was 47.2% in 2015-19 and broke in 2018. Agencies covering about 94% of the earlier population still report, so it isn't missing offenses. Whether one agency's clearances are missing is untested.

**Portfolio grade:** B. The chart is clean. The claim needs agency-level numbers before anyone says "police."

**Next join that would make it a story:** there's no agency-level crime table in the warehouse, and FBI_CDE is state x month only. Outside: FBI CDE agency-level clearances for Albuquerque PD and Bernalillo County SO, 2017-2023. Subtract them from the state and see whether the rest of NM looks like AZ or CO. Albuquerque's low homicide clearance has likely been covered in local press (from memory, no web).

---

## FED_FJC_IDB_CIVIL: NARROWED

**Claim as written:** One Cayman-named debt buyer filed 1,259 federal foreclosures in PR. 50% ended in default judgments, vs ~35% for other PR plaintiffs and 12% on the mainland.

**What I checked:** One row per case (district + office + docket + file date), same dedup as deep-12.
- **J4, any case type, any district, since 2005.**
  - Roosevelt Cayman's first filing is in **2015**. All of its filings are in PR.
  - About 1,260 cases in all, about 1,230 of them foreclosures (NOS 220). The rest are other real property (NOS 290), plus 2 recovery cases (150) and 1 other (430).
  - So "1,259 foreclosures" slightly overcounts.
- **J1, 2015+ PR foreclosures, share of CLOSED cases.** Open cases are under 1% for these groups, so open cases don't bias the rate.

| Group | Cases | Default, share of closed |
|---|---|---|
| Roosevelt (any spelling) | 1,230 | **50.7%** |
| Other Cayman shells | 130 | 28.7% |
| Other PR diversity plaintiffs | 1,924 | 38.8% |
| PR cases with a US-govt party | 367 | 23.3% |
| Mainland | 24,061 | 12.9% |

- **J2, the filing-year mix.** Roosevelt filed **694 in 2015** and 266 in 2016. That's **78% of its cases in two years**.
  - PR diversity peers defaulted **50.9% in 2015**, 34.8% in 2016.
  - Year by year, Roosevelt vs peers:

| Year | Roosevelt default | Peer default | Gap |
|---|---|---|---|
| 2015 | 59.6% | 50.9% | +9 |
| 2016 | 43.2% | 34.8% | +8 |
| 2017 | 29.2% | 35.9% | -7 |
| 2018 | 34.6% | 45.5% | -11 |
| 2019 | 38.8% | 37.6% | +1 |

  - Weight peer rates by Roosevelt's own year mix and you'd expect **~44.7%**. Actual is 50.7%. **The gap is ~6 points, not 15.**
- **J3, named peers.** CitiMortgage defaults **60.9%** (70 cases) and 66.7% ("ET AL" spelling). Reverse Mortgage Solutions Inc: 58.8%. Roosevelt is not the top defaulter by rate.
- **J5, sample of 23 cases from March 2015:**
  - One row per case, no copies across tapes.
  - Individual defendants.
  - Amounts demanded $79K-$363K (the column is in thousands).
  - Default rows carry JUDGMENT=1 (plaintiff).
  - These look like real residential foreclosures, not statistical closings.
- **Codes:** DISPOSITION 4 = judgment on default matches the FJC codebook as I know it. The JUDGMENT=1 rows agree. I didn't open the codebook file.

**What a hit means / what a miss means:**
- **Hit:** a Cayman vehicle that didn't exist in PR federal court before 2015 filed two-thirds of the island's non-government diversity foreclosures that year (694 of 1,046). That looks like one bulk loan-pool purchase being worked through the courts.
- **Miss on the default angle:** its default rate is ordinary for PR in the years it filed. The "wins half by default" line mostly reflects 2015 PR, not Roosevelt.

**Corrected headline:** Roosevelt Cayman Asset Company first appears in Puerto Rico federal court in 2015. It filed 694 foreclosures that year, two-thirds of the island's non-government diversity foreclosures, and about 1,230 by 2025, 78% of them in 2015-16. Half ended in default, but same-year PR lenders defaulted about 45%, so the default gap is roughly 6 points.

**Portfolio grade:** C as a default-rate story. B as a "one offshore buyer's 2015 foreclosure wave" story, once someone names the pool it bought. The 2015 start fits Doral Bank's failure that February (not verified).

**Next join that would make it a story:** `JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED` on district + docket. That gives docket links for the 694 cases filed in 2015, which name plaintiff counsel and the servicer. Also `FED_FJC_IDB_BANKRUPTCY` in PR (district 04) by filing month, to see whether Chapter 13 filings spiked as the wave landed. That's aggregate only; names won't join cleanly.
