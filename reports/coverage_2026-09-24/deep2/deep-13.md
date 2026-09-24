# deep-13: hand queries, group 13

2026-09-24. Five JUSTICE tables. The Python door only. 29 SELECTs plus 6 session statements = 35, right at the budget. The SQL is in `deep-13.sql`, numbered [1] to [29].

Every person, company, ship, county or hospital named below is **a data match, not verified against primary records.**

## The call

| Table | Verdict | One line |
|---|---|---|
| JUSTICE__XC_UK_SANCTIONS_LIST | **probed** | 358 ships the UK sanctions over Russian oil are not on the US SDN list. The number is real and checks out two ways, but the trade press already has this gap. |
| JUSTICE__INTL_UK_SANCTIONS_LIST | **dead** | Same list as XC, with its dates day/month-swapped. Use XC. |
| JUSTICE__XC_VERA_INCARCERATION_TRENDS | **probed** | Rural jail rates rose 17.5% from 2010 to 2019 while urban rates fell 19%. That is Vera's own published finding. Top growers are mostly jails that hold people for other agencies. |
| JUSTICE__RACIAL_JAIL_DISPARITY | **probed** | It is a copy of the Vera table (0 differences). The gap widened after 2019, but that sits on a data-source break. NYC boroughs top the list because of how Vera splits the city's jail count. |
| JUSTICE__XC_RANSOMWARELIVE_VICTIMS | **probed** | 32 Medicare hospitals land by exact name, many in small towns. The disclosure angle needs the HHS breach portal, which isn't in the warehouse. |

**No table here is live.** Everything real is either already covered or blocked on a missing table.

---

## 1. JUSTICE__XC_UK_SANCTIONS_LIST: probed

**Headline:** The UK has sanctioned 620 ships under its Russia rules. 358 of them (58%) are not on the US OFAC SDN list. 309 of those 358 were designated in 2024-2025, at least six months before the SDN pull (2026-06-25). So the gap is not just timing.

**Size:** 57,231 name rows. 5,127 OFSI group IDs (3,832 people, 1,280 entities). 657 distinct ship IMOs. Designations run 2000-04-12 to 2026-07-22. 31 regimes. One load run.

**Checked**
- [12] Took the 7-digit IMO from every UK ship row and joined it to SDN IMOs. SDN IMOs come from the IMO column, or from REMARKS when that column is blank. That gave 2,030 SDN IMOs.
- [24] Second opinion: in OpenSanctions, counted the targets tagged "UK FCDO Sanctions List", and how many of those are also tagged "US OFAC SDN".
- [13] Joined the UK IMOs to the NOAA AIS pings (U.S. waters, Jan 1-8 2024). AIS was grouped by IMO first.
- [25] Second-field check on the AIS hits: compared names, ship type and flag.

**UK ships vs SDN, by UK regime**

| Regime | Year designated | Ships | Also on SDN | UK-only |
|---|---|---|---|---|
| Russia | 2024 | 110 | 52 | 58 |
| Russia | 2025 | 433 | 182 | 251 |
| Russia | 2026 | 77 | 28 | 49 |
| North Korea | 2017-18 | 36 | 29 | 7 |
| Libya | 2026 | 1 | 0 | 1 |
| **All** | | **657** | **291** | **366** |

- The two methods agree. OpenSanctions counts 658 UK vessels, 291 of them also on the SDN. My IMO join says 657 and 291.
- People: 3,992 on the UK list, 2,333 also on the SDN (58%). Companies: 1,554, with 879 also on the SDN (57%). Organizations: 734, with 127 (17%).
- Of the 291 IMO matches, only 183 also match on name (63%). Ships get renamed. The IMO is the permanent hull number, so the match holds.

**AIS join:** 8 of 657 UK IMOs (1.2%) show up in the 8-day AIS week. All 8 are Russia-regime and UK-only. All 8 were designated **after** the pings (2025-02-24 to 2026-06-16).

| UK name now | AIS name, Jan 2024 | Pings | Where (average position) |
|---|---|---|---|
| PIERRE | SEA VINE | 8,422 | off Southern California |
| KUSTO | LOVINA | 4,051 | Texas Gulf coast |
| SEADAR | CAPRICORN SUN | 2,906 | Texas Gulf coast |
| BHILVA | PS GENOVA | 2,547 | Louisiana/Texas Gulf |
| LERUO | ALCYONE T | 1,989 | Louisiana/Texas Gulf |
| MINION | MINDORO | 1,282 | Gulf |
| JEWEL | AMAX AVENUE | 421 | off South Florida |
| NOBLE | SCF NEVA | 195 | near Puerto Rico/USVI |

- These are tankers trading in U.S. waters under their old names a year before the UK named them shadow fleet. NOBLE's old name starts SCF, a Sovcomflot-style prefix. Data match, not verified.
- **Second field fails on name for all 8.** The UK list carries only the new name, with no alias rows for these hulls. Type agrees where the UK filled it (5 of 8 say Oil Tanker; the AIS type codes are 80 and 89, the tanker range). IMO is the only link.

**Hit means:** the UK/US split on shadow-fleet ships is big, and two independent joins confirm it.
**Miss means:** it never got a miss. If the gap had been under 10%, this would have been a timing lag.
**Boring:** US policy slowed new Russia designations in 2025, and trade press (Lloyd's List and others) has covered this gap. **Not ruled out; it is the likely reason.** The AIS angle only reaches pre-designation history, because the warehouse holds 8 days of AIS.

**What would make it live:** a longer AIS window, or port-call data. With that, we could look for these 358 hulls calling at U.S. ports *after* the UK sanctioned them.

---

## 2. JUSTICE__INTL_UK_SANCTIONS_LIST: dead

**Headline:** This is the XC list again, with broken dates.

**Checked**
- [5] OFSI group IDs: 5,127 appear in both tables, 2 only here, 1 only in XC.
- [15] Joined UNIQUE_ID to XC's DESIGNATION_ID (6,315 of 6,334 IDs match) and compared LAST_UPDATED.

**Result**
- 4,352 of the 4,391 comparable IDs have **day and month swapped**. Example: RUS3601 reads 2026-11-05 here and 2026-05-11 in XC.
- 95 IDs are dated in the future.
- About 1,900 IDs have no parsable date. My read, not checked: the day was over 12, so the swapped string wasn't a valid date.
- DATE_DESIGNATED is filled for only 1,776 of 6,334 IDs. XC has it on every row.

**Hit means:** it's a duplicate, so there's no separate story. **Miss means:** if the two tables had diverged, one would hold targets the other lacks. They don't.
**Boring:** it's the same OFSI file, loaded twice by two pipelines. **Ruled in.**

---

## 3. JUSTICE__XC_VERA_INCARCERATION_TRENDS: probed

**Headline:** Take the 1,906 counties with jail counts in 2010, 2015, 2019 and 2023. Rural jails went from 531 to 624 people per 100K residents aged 15-64 (2010 to 2019), then back to 563 in 2023. Urban jails fell from 335 to 227. By 2023 the rural rate is 2.5x the urban rate.

| Urbanicity | Counties | 2010 | 2015 | 2019 | 2023 |
|---|---|---|---|---|---|
| rural | 1,022 | 531 | 549 | 624 | 563 |
| small/mid | 529 | 432 | 412 | 425 | 367 |
| suburban | 290 | 322 | 284 | 274 | 234 |
| urban | 65 | 335 | 283 | 271 | 227 |

Rate = jail population ÷ residents aged 15-64 × 100,000, pooled across the fixed set of counties [21].

**Top growers, 2010 to 2019** [28]: counties with 10K+ residents aged 15-64 and 100+ in jail in 2019. That leaves 1,276 counties, with a national median growth of 1.07x. Each county is compared to peers in the same state and urbanicity.

| County | Jail 2010 → 2019 (2023) | Rate per 100K | Peer median growth | Share held for fed/prison, 2019 |
|---|---|---|---|---|
| Karnes TX | 106 → 454 (549) | 1,026 → 4,524 | 1.22 | 89% |
| Fannin TX | 361 → 955 (869) | 1,640 → 4,196 | 1.22 | 83% |
| Baker FL | 141 → 491 (417) | 774 → 2,615 | 0.79 | 81%, incl. 272 ICE |
| Yazoo MS | 95 → 378 (376) | 501 → 1,890 | 1.03 | 1% |
| Butts GA | 136 → 354 (554) | 834 → 2,097 (3,064 in 2023) | 0.84 | 0%, and 1.12x over rated capacity |

- The top four are mostly **contract jails**: 80-89% of their population is held for federal agencies or the state.
- Butts GA and Yazoo MS are the local-growth leads. Butts is about 3x its suburban-Georgia peers and still rose to 2023.
- Hardee FL shows 10 → 135. The 2010 value looks broken.

**Checked:** [8] fill by year. [21] the fixed-cohort rates. [28] growers with peers and held-for-others share. [22] was a first try that subtracted held-for-others across 2010 to 2023. It is **void**, because those columns go blank after 2020.
**Hit means:** there are named counties whose jails grew 2.5-4x while their peers stayed flat.
**Miss means:** without a fixed cohort, the post-2020 drop in county coverage would fake a national decline.
**Boring:** Vera published the rural jail boom itself, and the top growers hold other agencies' prisoners. **Ruled in for the top 4.** Butts GA and Yazoo MS are not explained by holds.
**Not tested:** the "while crime fell" part. There is no county crime table in the plain catalog.

---

## 4. JUSTICE__RACIAL_JAIL_DISPARITY: probed

**Headline:** In 356 counties with 5,000+ Black working-age residents and 20+ Black and 20+ white people in jail every year, the median Black-to-white jail-rate ratio went 4.57 (2010) → 3.41 (2019) → 3.86 (2023). The gap narrowed until 2019 and widened after. **That widening crosses a data-source break**, so it isn't defensible yet.

**Checked**
- [23] Joined county-year to Vera. On all 128,507 county-years there are **0 differences** in total jail population, Black jail population, Black rate and Black working-age population. This table is a derived copy of Vera.
- [19] 2019 ranking of 599 counties (same filters). National median ratio: 3.2.
- [20] Fixed-cohort trend. [29] Biggest risers 2019 to 2023, plus a check on the NYC boroughs.

| Year | Median ratio | Pooled ratio | Counties at 10x+ |
|---|---|---|---|
| 2010 | 4.57 | 4.52 | 30 |
| 2015 | 3.68 | 3.67 | 21 |
| 2019 | 3.41 | 3.54 | 19 |
| 2023 | 3.86 | 3.77 | 24 |

Rates are per 100K residents aged 15-64 (Vera's working-age denominator), not per 100K total population.

**Top of the 2019 list:**
- Richmond NY (Staten Island) 45.6x, against a New York median of 7.4.
- New York County NY 29.3x.
- Schenectady NY 22.2x.
- Arlington VA 22.1x, against a Virginia median of 3.1.
- District of Columbia 19.2x.
- Waukesha WI 18.6x.

**Why it's not defensible yet**
- **NYC:** the city runs one jail system. Vera splits it across five boroughs, which sum to 12,718 people in 2019. That total looks high against the city's own jail headcount, which I did not pull. Treat the borough ratios as Vera's allocation, not local practice. **Unverified.**
- **After 2020 the white counts halve while totals hold.** Miami-Dade: white 421 → 201, total 4,184 → 4,278. Montgomery MD: white 295 → 146, total 753 → 893. East Baton Rouge: white 352 → 82. That looks like a race-coding change in Vera's newer data, not behavior. **Not ruled out.**
- Coverage of Black rates drops from about 2,700 counties (2019) to about 1,100 (2020-2023).

**Hit means:** a named county jails Black residents at many times its peers' ratio.
**Miss means:** with tiny denominators filtered out, most counties sit at 2-5x.
**Boring:** Vera publishes these ratios. The extreme ratios are either tiny-denominator noise (filtered out here) or allocation and coding artifacts. **Partly ruled out.**

---

## 5. JUSTICE__XC_RANSOMWARELIVE_VICTIMS: probed

**Headline:**
- There are 1,146 U.S. healthcare posts on gang leak sites, and 1,050 of them are from 2024 on.
- 33 of those posts (2.9%) land on a Medicare hospital by exact cleaned name. That's 32 hospitals.
- Of about 79 posts whose title looks like a hospital name, that's about 4 in 10.

**Size:** 30,661 posts, 356 gangs, 2013-11 to 2026-08-11. 10,040 are U.S.

**Checked**
- [16] and [27]: counts by year, blank country, bulk timestamps.
- [17]: U.S. posts by sector. Healthcare 1,146; Education 528; Government & Defense 476.
- [18]: exact cleaned-name join of U.S. healthcare post titles to CMS Hospital General (5.4K hospitals).
- [26]: the same victim posted by two or more different gangs.

**Hospital hits:** 31 of the 33 names are unique in CMS. Two are ambiguous: "University Medical Center" and "Wayne Memorial Hospital" each match 2 CMS hospitals. Where the post carries a description, the city agrees. Examples: Baraga County Memorial (L'Anse MI), Community Hospital of Anaconda (MT), Mile Bluff (Mauston WI). Many hits are in small towns, like Nocona TX, Snyder TX (Cogdell), Lindsay OK, Alturas CA (Modoc), Rupert ID (Minidoka) and Luverne AL (Crenshaw). I did not pull hospital type, so "rural" and "critical access" are not checked, except for Baraga, whose own post says it.

**Repeat victims:** 224 U.S. title keys were posted by 2+ gangs, 16 of them healthcare. Watsonville Community Hospital was posted by termite (2024-12) and again by sinobi (2025-10). The Loretto Hospital was posted by incransom and ransomhouse three weeks apart. Some of the 224 keys are redacted junk, like `*************`.

**Hit means:** leak-site posts can be tied to named Medicare hospitals. **Miss means:** the other 97% of healthcare posts are clinics, labs, billing firms, or domain-only titles that exact-name matching can't place.
**Boring:** a leak-site claim is not a confirmed breach. The sector is widely covered, and rural hospitals being hit is known. **Not ruled out.**
**Blocked:** "did they report to HHS" needs the HHS OCR breach portal. **It isn't in the warehouse.**

---

## Traps found (not saved to memory, since I was told to write only these two files)

- **INTL UK list dates are day/month-swapped:** 4,352 of 4,391 comparable IDs, 95 in the future. Use XC.
- **The two UK lists are the same list:** 5,127 shared group IDs.
- **UK ship rows:** there are only 15 distinct OFSI_GROUP_ID values across 657 ships, so key ships on IMO or DESIGNATION_ID. IMO comes as `9114555` or `IMO9276561`; pull the 7 digits.
- **Ship names don't survive renames:** 108 of 291 IMO matches to the SDN disagree on name, and 8 of 8 AIS hits do.
- **RACIAL_JAIL_DISPARITY is a copy of Vera,** with 0 differences over 128,507 county-years. Its rates are per 100K residents aged 15-64.
- **Vera coverage falls off a cliff after 2019:** about 2,900 counties in 2019, about 2,200 in 2020-23, 1,441 in 2024, 860 in 2025, 597 in 2026. 2025-26 are marked stub years. ICE holds are empty from 2024 and prison columns are empty from 2020. Use a fixed cohort.
- **Vera held-for-others columns can exceed total jail population** (Decatur GA 2010: 415 held vs 130 in jail). They also go blank after 2020, so never subtract them across that break.
- **Vera before 1999:** only 1970, 1978, 1983, 1988 and 1993 have near-full county jail coverage. Race jail columns are text, and COUNT() counts blanks, so use try_to_double.
- **Ransomware COUNTRY is blank** for 87% of 2021 rows, 80% of 2022 and 56% of 2023, against about 6% from 2024 on. Any U.S. trend across 2023 to 2024 is a fill artifact.
- **Unresolved:** the fact line says maersk.com, fedex.com and renault.fr have 182 rows each. An exact WEBSITE match finds 4 rows total. Probably variant spellings; not chased.

parked: loading the HHS OCR breach portal would turn the ransomware-to-hospital join into a disclosure check (the 32 hospitals are ready to test).
