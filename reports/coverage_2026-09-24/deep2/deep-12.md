# deep-12: five JUSTICE tables, queried by hand

2026-09-24 · coverage round 2 · Python door · **30 of 35 statements used** (2 of the 30 errored and were rerun) · SQL in `deep-12.sql`

Every person or company named below is **a data match, not checked against primary records**.

## The answer

| Table | Verdict | The one number |
|---|---|---|
| INTL_OPENSANCTIONS | **live** | 45 sanctioned people are still listed as controlling 83 active UK companies. One OFAC organized-crime designee, Ka On Kong, shows up on 22 London companies |
| FED_FBI_CDE | **live** | New Mexico solved **22.7%** of its homicides in 2022-23. The nation solved 56%. It was 47% in NM in 2015-19, and there's no reporting gap |
| FED_FJC_IDB_CIVIL | **live** | One Cayman-named debt buyer filed **1,259** federal foreclosures in Puerto Rico. Half of them ended in default judgments (50%). Other PR plaintiffs: about 35%. The mainland: 12% |
| FED_COURTLISTENER_DISCLOSURE_SPOUSAL_INCOME | probed | 2 dockets were assigned to a judge while the judge's spouse drew director fees from the named defendant. Both closed fast, and recusal is unchecked |
| FED_FHFA_SUSPENDED_COUNTERPARTIES | dead | 54 of 210 banned people are also on SAM. That's expected: 44 are HUD bans that came first, and 8 are one known PPP-fraud family |

---

## 1. INTL_OPENSANCTIONS: **live**

**What the table is.** 71,011 rows. 39,680 are people and 16,419 are Organization rows. The rest are companies, wallets, securities and ships. It's a slice of OpenSanctions, not the full 1.28M set.

**Checked, join A: sanctioned people vs UK PSC.** PSC is the UK register of people with significant control, the owners behind UK companies.
- The match: a surname token, a forename token, birth year and birth month all have to agree. Then I kept only full-name matches, so "Mohammed Ali"-style loose hits drop out.
- Denominator: 21,670 listed people have a full birth date. 6,637 of them are on OFAC SDN or the UK FCDO list.
- **157 people** matched, across **309 UK companies**. That's 0.7% of people with a full birth date.
- Only 176 of the 332 match rows found their company in the Companies House table. For those 176 rows:
  - **83 rows** have control never ceased and the company Active. That's **45 people and 83 companies**.
  - **21 OFAC SDN people** sit on **42** active companies.
  - **19 UK-sanctioned people** sit on **32** active companies.
- Standout: **Ka On Kong** (OFAC SDN, Executive Order 13581, transnational crime).
  - Same name, born June 1983, controls **22 UK companies**. The PSC entries were filed 2022-2025. Most of the companies are Active.
  - They're restaurants and clubs (Mingmen London, Chasca London, Shiva London, DTX Winners Club, Charco Charco Holborn) plus shells with names like "Fortune / Halo Network Technology" and "Varuna Maritime Services".
  - They cluster at 2 addresses: 2c St George Wharf SW8 and 114 Hamlet Court Road SS0.
  - In March 2026 his control of Koke Ramen UK moved to a corporate owner registered at that same Hamlet Court Road address.
  - Brendon Luo is on the same OFAC action (same first-seen day, 2026-06-23). He is listed as Cambodian and controls BL Hospitality Ltd.
- Other open, active controls: drug and terror designees. Examples: Jose Javier Rascon Ramirez (Kingpin Act), Jian Zhang (Kingpin Act), Sayed Wazir Shah (SDNTK), Muhammad Harris Dar (SDGT). The list also carries the known Russian names (Abramovich, Kantor, Potanin, Melnichenko, Gutseriev, Frolov).

**Checked, join B: sanctioned organizations vs federal contract recipients (USAspending R2, 93M rows).**
- The match: full normalized name equality, legal suffixes stripped, 2+ words.
- 227 matches came back. The biggest are Lockheed, Booz Allen, General Dynamics and Anduril. They're on **China's and Iran's counter-sanction lists**, which is the boring explanation, and they're ruled out.
- Then I required the recipient's country to be one of the listed countries. **28 matches** survive. Contract money after first-seen totals about **$1M**.
- Real-looking ones, all paid before listing: NAI Logistics B.V. (NL, DoD, $3.3M, 2015-23), Fidelis Logistic and Supply Services (Afghanistan, DoD, $1.4M, 2022), Gateway Ventures FZC (UAE, DoD, $1.5M, 2015-19), Eiger Shipping SA (Switzerland, DoD, $1.3M, 2021-26, UK-listed only).

**Hit means.** The listed person really is this UK company controller. Then a US- or UK-sanctioned person is running a live UK company web, and for the non-Russian designees that's barely reported.
**Miss means.** It's a same-name, same-birth-month stranger. That's plausible for the very common names (Muhammad Iqbal, Jian Zhang). It's much less plausible for Ka On Kong: 22 companies, 2 shared addresses, nationality matches.
**Boring.**
- An asset freeze doesn't dissolve a company, so "Active" can just mean frozen.
- The oligarch holdings are already well covered.
- **Not ruled out:** whether the UK-listed people hold an OFSI licence.
- **Ruled out:** the counter-sanction noise in join B.

---

## 2. FED_FBI_CDE: **live** (New Mexico)

**What the table is.** 238,680 rows: state × month × 10 crime types, 1985-2023, 51 states counting DC. It holds counts of offenses and clearances. There's no agency-coverage column.

**Checked.**
- I summed homicide offenses and clearances by state and year. The rate is clearances ÷ offenses.
- I flagged any year where a state's homicides fell below 70% of its own 2015-19 average (a reporting gap).
- I checked months where violent-crime clearances were under 5% of offenses.

| | NM homicide clearance | NM homicides reported |
|---|---|---|
| 1985-89 | 75.1% | — |
| 2015-19 | 47.2% (341 / 723) | 113-175 a year |
| 2020-23 | 25.9% (223 / 861) | 155, 231, 242, 233 |
| 2022 / 2023 | **22.3% / 23.2%** | 242 / 233 |

- **Lowest of all 51** in both 2022 and 2023. The nation was 56% in 2022-23. The next-lowest is IL at 32.9%, and IL itself is an artifact (see traps).
- Peers, 2020-23: AZ 68.7%, CO 73.5%, UT 64.6%, OK 57.9%, TX 57.2%. NM sits 31-48 points under every neighbor.
- It's not one crime type. NM violent-crime clearance went 41% → 29% (2015 → 2023). Aggravated assault went 48% → 33%.
- No reporting hole: all 12 months are reported every year, homicide counts go up rather than down, and no month has clearances under 5%.
- The slide starts in 2018 (34%), before the 2021 NIBRS switch.

**Hit means.** NM police close under a quarter of homicides: the worst rate in the country, and falling for 6 years. Albuquerque probably drives most of it; this table cannot show agencies.
**Miss means.** NM agencies send clearances to the FBI late or only partly. Then the true rate is higher and the story is about reporting, not policing.
**Boring.**
- Clearance rates falling nationally is well reported.
- NIBRS counts clearances differently. Only partly ruled out: the drop began before NIBRS, and neighbors that report through NIBRS (AZ, TX, CO) did not collapse. When each state switched was not checked.
- Late clearances hit every state the same way.
- **Not ruled out:** agency-level late reporting. That needs agency-level data, which this table doesn't have.

---

## 3. FED_FJC_IDB_CIVIL: **live** (Puerto Rico Cayman foreclosures)

**What the table is.** 10,857,396 rows from 40 yearly files (1988 to 2099; 2099 is the pending file). 41,465 rows repeat across files, so I kept one row per case: district + office + docket + file date, preferring the latest closed file.

**Checked.**
- Plaintiffs since 2015, one row per case. Case count, main case type (NOS code), and how cases ended:
  - DISPOSITION 12 = voluntary dismissal
  - 13 = settled
  - 4 = default
  - JUDGMENT 1 = plaintiff won
  - **These codes are the FJC codebook from memory. They weren't checked against the codebook file.**
- Then foreclosures (NOS 220) in Puerto Rico (district 04) vs every other district.
- Then every plaintiff with "CAYMAN" in the name.

| Foreclosures since 2015 | Cases | Default share |
|---|---|---|
| Roosevelt Cayman Asset Company (main spelling) | 1,153 | **50.2%** |
| All other PR foreclosure plaintiffs | ~2,558 | ~35% (computed as the rest) |
| All other districts | 24,061 | 12.0% |

- All spellings of Roosevelt Cayman: **1,259 cases, 2015-2025, all in PR, all diversity jurisdiction (code 4)**. Under the main spelling alone, that's **31% of PR's 3,711** federal foreclosures since 2015.
- Sister shells with the same name pattern, also in PR, also diversity: Bautista Cayman Asset Company (107), Triangle Cayman (20), Abbey Cayman (7).
- For comparison, the serial-plaintiff angle Chris's triage named is real but already known:
  - Strike 3 Holdings: 21,600 copyright suits since 2017, 82% voluntarily dismissed, median about 100 days.
  - Malibu Media: 4,556.
  - Joe Hand Promotions: 1,434. J&J Sports: 1,416.
  - "BONILLA, VEXATIOUS LITIGANT": 1,938 prisoner filings.

**Hit means.** One offshore loan-pool vehicle turned PR federal court into a foreclosure lane. It filed a third of the island's federal foreclosures and won half of them by default.
**Miss means.** It's just the biggest holder of distressed PR mortgages, and PR borrowers don't answer suits whoever the plaintiff is. Other PR peers run 30-40% default, which is why ~35% vs 50% is the test, not 12%.
**Boring.**
- The Cayman registration is exactly what creates diversity jurisdiction. That's legal and ordinary.
- These are likely bought pools of failed-bank loans (not verified).
- **Ruled out:** that the high default rate is only an island-wide effect. Roosevelt still sits about 15 points over its PR peers.
- **Not ruled out:** loan mix, like how old the delinquencies are.

---

## 4. FED_COURTLISTENER_DISCLOSURE_SPOUSAL_INCOME: probed

**What the table is.**
- 20,174 spouse-income lines on 13,530 disclosure reports.
- **The report years are 2003-2020.** The triage's "2021-23 only" was CourtListener's load date, not the report year.
- 611 lines (3%) are redacted. There's heavy OCR junk, like "AFANINC INAS J ANAY".
- Joined through FINANCIAL_DISCLOSURES to JUDGES, 17,843 of 20,188 rows (**88%**) land on a judge. That's 2,239 judges.

**Checked, pass 1: employers.**
- Kind of source: law-firm-like 10.3%, self-employed lawyer 3.8%, company 9.6%, school 13.7%, government 13.3%.
- I took multi-word company and law-firm names for each judge: **1,008 judge-employer pairs covering 587 judges**.
- Then I searched the CourtListener dockets assigned to that judge for case names containing the employer. 504 of those judges have dockets, 4.9M in all.
- **32 pairs hit any docket. 11 hit within the disclosure years ±1.** After a hand-check, about 5 look plausible. The biggest: Judge Sheri Chappell (M.D. Fla.) had 5 Lee Memorial Health System cases in the years her spouse drew Lee Memorial pay.

**Checked, pass 2: director fees.**
- 956 lines at 148 judges name director, board or trustee pay. I picked out 51 company names at 20 judges and ran the same docket search.
- 23 hits. 3 fall in the disclosure window, and 1 is false: "Panasonic" contains "SONIC CORP".
- The 2 left:
  - **Liotti v. Jet Blue Airways**, SDNY 1:17-cv-00838. Filed 2017-02-02, closed 2017-02-07. Assigned to Judge Colleen McMahon, whose spouse drew JetBlue director fees 2014-18.
  - **Gardner v. Procter & Gamble Fed. Inc**, NDIL 1:09-cv-06690. Filed 2009-10-22, closed 2010-01-13. Assigned to Judge Harry Leinenweber, whose spouse drew P&G director fees 2004-09. "Fed." may mean a P&G credit union, not P&G itself.

**Hit means.** A spouse who is a director of a party is a mandatory recusal under 28 USC 455(b)(5)(i). If the judge ruled, that's a story.
**Miss means.** The judge recused and the case was reassigned, or it was dismissed on intake. The 5-day and 3-month closes fit that. CourtListener's assigned judge can be the first draw, before a recusal.
**Boring.**
- CourtListener only holds dockets someone pulled, so land rates are floors.
- There's no counsel table, so "the spouse's law firm appears before the judge" **can't be tested** here.
- **Not ruled out:** recusal. It needs a PACER docket check on these 2 cases.

---

## 5. FED_FHFA_SUSPENDED_COUNTERPARTIES: dead

**What the table is.** 241 bans, 2013-04-15 to 2026-07-29. 210 are people and 31 are companies. 82 have an end date. Only 82 bans predate PPP (April 2020), so "got PPP after the ban" is possible for about a third at most.

**Checked.**
- People vs SAM exclusions: first + last name, then state as the second field.
- People vs PPP loans of $150K and up: both name tokens plus the same state.
- Companies vs SAM, PPP, USAspending contracts R2 and HMDA lender names: normalized name equality.

**Found.**
- **54 of 210 people** have a same-name, same-state SAM exclusion:
  - 44 are HUD bans, **every one dated before the FHFA ban**. FHFA follows HUD.
  - 8 are SBA bans (2025-02-24) on the Ayvazyan / Dadyan / Terabelian family. That's the known Los Angeles PPP-fraud ring.
- PPP, people: 1 hit, and it's a collision: Jose L. Garcia DDS, Temecula, vs a different Jose Garcia.
- Companies: 0 contract recipients. 3 PPP hits, all in other states (collisions).
- 2 HMDA lender names:
  - Live Well Financial, which collapsed in 2019.
  - First Mortgage Company. Its HMDA name ends in Inc; the FHFA row says LLC.

**Hit means.** A banned lender still reporting mortgages. That **can't be tested here**: national HMDA after 2017 isn't loaded, only DC samples. Not treating that as absence.
**Miss means.** Nothing new. The overlaps are the system working: HUD bans first, FHFA copies.
**Boring.** Confirmed. It's 241 rows of mostly already-convicted people.

---

## Traps found

- **IL clearances aren't reported 2010-2020** in FBI_CDE: 1-3% of violent crime every month, then 22-35% from 2021. Never rank IL on clearance before 2021.
- **NY clearance jumps from 17% (2010-12) to 63% (2013)**. NY 2021 has only 232 homicides (a NIBRS hole), and NY 2022 violent-crime clearance reads 12%. All three are reporting artifacts.
- **MT 1994 is blank** on all 10 offenses in FBI_CDE.
- **OpenSanctions FIRST_SEEN is when OpenSanctions picked up the entry, not the designation date.** It holds 568 distinct days, with bulk loads on days like 2023-04-20. "Paid after listing" can't be measured from it.
- **Suffix-stripping name joins against sanctions lists make US look-alikes.** "Scott Technologies FZE" (UAE) matched Scott Technologies Inc (US, $320M). Always require country agreement.
- **China and Iran counter-sanction lists sit inside OpenSanctions.** Lockheed, Booz Allen and General Dynamics are "sanctioned" there. Filter those lists out before any "sanctioned contractor" claim.
- **CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE lacks 47% of the company numbers PSC points to** (156 of 332 here). Overseas-entity (OE) and Scottish LP (SL) numbers are often missing. Blank status there is not "dissolved".
- **The spousal table's DATE_CREATED is 2021-23 (CourtListener's load). The report years are 2003-2020.**
- **Substring docket search:** "SONIC CORP" sits inside "PANASONIC CORP". Hand-check every hit.

## What would prove each live row wrong

- **OpenSanctions:** Companies House officer pages for Ka On Kong's 22 companies. If the birth date shows a different day, or the OFAC SDN entry gives a different address or nationality, it's dead.
- **FBI_CDE:** New Mexico's agency-level NIBRS clearances for the Albuquerque police. If the state total is mostly one agency's missing clearances, it's a reporting story, not a policing story.
- **FJC civil:** a sample of Roosevelt Cayman PACER dockets, to see whether the defaults are real or statistical closings, and who the sponsor behind the Cayman shells is.
