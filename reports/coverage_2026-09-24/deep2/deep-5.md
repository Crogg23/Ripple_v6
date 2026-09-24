# Deep2 group 5: five tables, hand-queried

2026-09-24. Python door, query tag `coverage-r2-2026-09-24`. **27 of 35 SELECT/WITH statements used.** One failed at compile and was rerun. The SQL is in `deep-5.sql`.

Every person, company or committee named below is **a data match, not verified against primary records**.

## The menu

| Table | Verdict | The number that matters |
|---|---|---|
| PHMSA_FLAGGED_INCIDENTS | **live** | 2025 is the worst year for gas lost from US transmission lines in the table's 16 years: 5.21M units, against 1.4-3.0M in every other full year. 63% of it is one Energy Transfer offshore line, Sea Robin, with seven reports at one spot off Louisiana. |
| NOAA_STORM_EVENTS | **live** | One weather office, Phoenix, logged **1,345 of the 2,145 US heat deaths (63%)** in the storm record for 2018-2023, copied from Maricopa County's counts. It logged no heat events after June 2024. The national heat-death count fell from 557 (2023) to 99 (2025). |
| FEC_BULK_COMMITTEES | probed | There is no PAC mill. Woodbend Dr is one person filing 123 joke candidacies. Datwyler is a GOP compliance vendor. His PACs that raised $100K+ from individuals send a median 16% of spending to candidates, against 44% for peers. That's $11M, small. |
| ICIS_FEC_EPA_INSPECTIONS | probed | The top repeat-inspection sites are ports of entry and injection wells, and inspections went up in 2026, not down. One thread is still open: within the hazardous-waste law (RCRA), Regions 6 and 9 took no EPA action on file at 78% of sites they inspected twice or more. Regions 7 and 8 left 33%. |
| FCT_LIBRARY_SNAPSHOT | **dead** | The 94 "vanished" Epstein files are a paging artifact. The live crawl read only page 1 (about 50 links) of each dataset listing. |

---

## 1. ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS: **live**

**Headline:** In 2025 one Energy Transfer offshore gas line, Sea Robin, filed seven incident reports from one spot off Louisiana, about 28.246 N, 91.705 W. Together they claim up to 3.27M units of gas released unintentionally. That turned 2025 into the table's worst year by far.

**Shape**
- 2,039 rows, one per report number, all from one load run. Received 2010-03-10 to 2026-07-31.
- 262 operator IDs and 313 spellings of operator names. 34 deaths and 136 injuries in total.
- **Unit:** the table doesn't say. PHMSA's gas form asks for thousand cubic feet (MCF). Equitrans' 2022 Rager Mountain row reads 1,290,000, which fits the roughly 1.3 billion cubic feet that was publicly reported. That fit is from outside the warehouse and wasn't checked here.

**Checked**
1. Ranked operators by total unintentional release, incident count and deaths.
2. Listed every Sea Robin report since 2022.
3. Summed release per year and pulled out Sea Robin's part.
4. Grouped 2023+ reports by the operator's street address, which works as a company-family roll-up.
5. Searched the whole table for the same volume showing up on more than one report.

**What came back**

| Check | Number | Denominator / peer |
|---|---|---|
| Sea Robin, all years | 32 reports, 3.37M MCF, **10% of the 16-year total** | 33.88M MCF, all operators. The median operator has 2 reports and 8,896 MCF |
| Sea Robin, 2025 | 3.29M MCF | 2025 all operators: 5.21M. Next-worst year: 2022 at 2.98M. Typical year: 1.4-2.2M |
| Biggest single report | Sea Robin, 2025-05-17: 1,587,069 | Next biggest: Equitrans 2022, 1,290,000 |
| 1300 Main Street, Houston (Sea Robin, Trunkline, Transwestern, Enable, Gulf Run: 12 operator IDs) | 68 reports, 4.29M MCF, **45.6% of all 2023-2026 release** (a floor, because other spellings of the address weren't summed) | Next family: 1001 Louisiana St (Kinder Morgan lines), 18.8% across four spellings of the address |

The Sea Robin spot, 2025:

| Date | Unintentional | Intentional |
|---|---|---|
| 2025-01-13 07:33 | 793,534 | 0 |
| 2025-01-13 12:10 | 793,534 | 0 |
| 2025-05-17 | 1,587,069 | 0 |
| 2025-07-22 | 3,508 | 527,853 |
| 2025-08-02 (two reports) | 229 each | 527,853 each |
| 2025-10-19 | 93,467 | 27,882 |

- **Hit means:** one offshore segment lost more gas in 2025 than any other single incident filed since 2010. That's a methane story and a regulator story: seven reports from one spot in 10 months.
- **Miss means:** if the volumes are one estimate copied onto several reports, Sea Robin's floor is about 1.69M MCF. It's still the biggest single report, and 2025 is still the top year at about 3.62M.
- **Boring:** offshore leaks are estimated, not metered. An operator can put a segment's whole estimate on every report. Load duplication is **ruled out**: each row has its own report number and its own NRC call number. Copying is **not ruled out**. Sea Robin put 793,534 on two reports the same day and 527,853 on three reports. 1,587,069 is almost exactly 2 × 793,534.5. Across the table there are only 6 same-operator, same-volume repeats of 10K MCF or more, and 3 of them are Sea Robin.
- **Can't do:** a leak rate per mile. The warehouse has no PHMSA mileage table; I searched for one and found none. Press coverage of Sea Robin 2025 wasn't checked.

---

## 2. ENVIRONMENT__FED_NOAA_STORM_EVENTS: **live** (on how the data is recorded, not on the reporter's angle)

**Headline:** The federal storm record's heat-death count mostly comes from one Weather Service office in Phoenix, which copies Maricopa County's counts. When Phoenix stopped logging heat after June 2024, the national count fell 82%.

**Shape**
- 1,780,730 rows, one per event ID, 1996-2025. The table's last month is 2025-12.
- 19,289 direct deaths, 4,509 indirect deaths, 86,922 direct injuries. DAMAGE_PROPERTY is blank on 612,832 rows (34%).

**Checked**
1. Summed direct deaths by event type for 1996-2009 and for 2010+.
2. Listed the top places by hazard.
3. Pulled heat deaths per year for the Phoenix office (PSR), Las Vegas (VEF), Texas and California.
4. Read the narratives on the Phoenix rows.
5. Looked for any renamed heat event type.
6. Listed Phoenix's summer filings of any type for 2023-2025.

**What came back**

| Direct deaths, 2010-2025 | Number |
|---|---|
| Heat (Heat 1,405 + Excessive Heat 1,947) | **3,352** |
| Flood (Flash Flood 1,295 + Flood 426) | 1,721 |
| Tornado | 1,313 |
| Rip current | 911 |

| Heat direct deaths | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|
| US | 284 | 188 | 352 | 376 | 388 | 557 | 250 | 99 |
| Phoenix office | 157 | 127 | 303 | 187 | 219 | 352 | 73 | 1 |
| Las Vegas office | 72 | 23 | 1 | 10 | 27 | 36 | 64 | 35 |
| All of Texas | 2 | 7 | 2 | 0 | 53 | 56 | 3 | 0 |

- **2018-2023:** Phoenix is 1,345 of 2,145 (62.7%). Phoenix plus Las Vegas is 70.6%. All of Texas is 120 (5.6%).
- **Offices logging any heat death:** 9-19 of 122-123 offices in each of those years.
- **Where Phoenix's numbers come from:** its rows say "fatalities were reported by the Maricopa County Department of Public Health". The top 2023 row carries 94 direct deaths.
- **The cutoff:** Phoenix's last heat row is 2024-06, then one hiker row in 2025-05. The office kept filing everything else: July 2024 has 82 events (thunderstorm wind, dust storms, floods) and none of them are heat. July 2023 had 144 heat events and 222 deaths.
- **Without Phoenix:** national heat deaths run 205 (2023), 177 (2024), 98 (2025).
- **Hit means:** Storm Data heat deaths measure which office does the paperwork, not the heat. Any "heat is the deadliest weather" ranking built on this table leans on Phoenix, and the 2024-25 "drop" is fake.
- **Miss means:** if heat deaths were spread across offices, the table would be a usable national count. They aren't.
- **Boring:** Storm Data only counts deaths an office can confirm, and it's known to undercount heat compared with death certificates. A late-filing lag for Phoenix's summer 2024 heat is **not ruled out**. The table runs to 2025-12 and Phoenix filed other event types through 2025-11, so this is not where the load stops.
- **Reporter angle (do disaster dollars follow the deaths):** unresolved. FEMA Individual Assistance codes its incidents with single letters that need a lookup. Code H has 15.2M registrations and $16.5B in IHP aid since 2010; F has 1.67M and $4.5B. You can't tell from the codes whether heat has any code at all, so "no heat aid" isn't claimed.
- **Damage-per-event angle: dead.** The median damage per damaged event fell from $10,000 (1996-2011) to $5,000 (2018-24) to $3,000 (2025). That's a change in how damage is estimated. The totals are driven by single years: 2005 at $96.7B and 2017 at $80.4B, nominal.

---

## 3. FINANCE__FED_FEC_BULK_COMMITTEES: probed

**Headline:** Neither cluster is a scam mill. Datwyler's larger unauthorized PACs do spend a thin share on candidates. The two biggest are politicians' own PACs, and that's a known genre.

**Shape**
- 20,007 rows, one per committee ID, and 19,850 names. `CYCLE` is 2026 on every row, a known trap.
- **The triage's "names repeat 148 times" is false.** No committee name appears more than 20 times.

**Checked**
1. Grouped committees by treasurer and by street, city and state.
2. Read the Woodbend Dr and Datwyler rows.
3. Joined to `POLITICS__FED_FEC_PAC_SUMMARY`. That table holds cycles 2018-2024, plus 7,897 rows with no date, and only 6 rows for 2026, so I matched to the **2024** cycle.
4. Scored each PAC's political share: money to other committees plus independent spending, divided by all spending.

**What came back**
- **1742 Woodbend Dr, Claremont CA:** 123 committees under one street, city and state. Nearly all are named for one person, "Quinci Renee Smith Slater", with names like "…ON ITUNES MUSIC" and "…YALE UNIVERSITY". They are House, Senate and presidential committees, most with the treasurer written as "N, N N". This is one self-filer. Their money wasn't checked.
- **Datwyler:** 322 committees under the exact name, more with spelling variants. Most are GOP leadership PACs and joint fundraising committees at PO Box 183 or 502 6th St, Hudson WI. That's a compliance vendor.

| 2024 cycle, unauthorized PACs | Datwyler | All other |
|---|---|---|
| Committees / found in the PAC summary | 134 / 68 | 6,093 / 4,414 |
| Receipts | $11.1M | $13.0B |
| Political share, by dollars | 31.8% | 75.2% |
| Median share, PACs with $100K+ from individuals | **16.2%** (n=15) | **44.4%** (n=1,153) |

- Lowest Datwyler shares:
  - Defend Freedom, Inc. (connected org GABBARD): $2.40M from individuals, $20,019 to committees, **1.1%**.
  - GatorPAC: $3.73M from individuals, 7.8%.
  - Women for America's Freedom: $309K, 2.9%.
  - Defense of Freedom PAC: $291K, 3.6%.
- **Hit means:** a short list of PACs where donor money mostly paid for things other than candidates.
- **Miss means:** the share measure is weak. The lowest-share PACs nationwide are union funds and turnout groups that send money to non-federal accounts or pay field staff, like Heartland Patriots at $22.7M and 0%. The summary file doesn't count those as political spending.
- **Boring:** leadership PACs paying for travel and fundraising is legal and widely covered, and compliance treasurers legitimately serve hundreds of committees. Both are **ruled in**.

---

## 4. FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS: probed

**Headline:** Both triage angles are artifacts. The one open thread is regional follow-up inside a single law.

**Shape**
- 260,556 rows but 259,861 activity IDs, so 695 rows repeat an ID. 156,326 registry IDs, 1,419 of them null.
- Dates run from year 0201 (a typo) to 2026-07-24.

**What came back**
- **Top repeat sites are ports of entry:**
  - Tevra Brands at the Omaha port: 2,235 pesticide desk audits.
  - Blaine WA port: 1,807.
  - Pembina: 726.
  - Amazon: 649.
- **No inspection desert over time.** Jan-Jun inspections ran 3,068 (2019), 3,165 (2023), 3,253 (2024), 3,359 (2025) and **4,800 (2026)**. Import checks went 308 → 1,221. Everything else rose 17%.
- **Join to enforcement cases and informal actions:** of 1,102 sites with 5+ on-site inspections since 2015, 44.7% have no action on file.
  - The top no-action sites are injection wells (Seneca Resources wells with 59 and 34 inspections), military bases (Minot AFB 68, Kings Bay 51), and a Hawaii townhome complex inspected 53 times in one day.
  - That's how those programs work, not a failure to follow up.
- **Peer check inside one law** (sites inspected twice or more, no case or informal action):

| Law | Highest | Lowest |
|---|---|---|
| RCRA hazardous waste | **R6 78.5%, R9 78.4%** | R7 32.8%, R8 33.5% |
| CWA | R8 76.7% | R3 56.2% |
| TSCA | R1 92.9% | R8 33.9% |

- **Hit means:** EPA regions differ by more than 2x in how often an inspection ends in any recorded action.
- **Miss means:** the gap is state enforcement or program mix inside the law, and there's no story.
- **Boring, not ruled out:** the case tables carry **no dates**, so "no action" means none at any time. State-led enforcement isn't in these tables. TSCA R1 is probably lead-paint contractor inspections.

---

## 5. FCT_LIBRARY_SNAPSHOT (Epstein file watch list): dead

**Headline:** The "vanished files" are pages the live crawler never read.

**What came back**
- 619 files; 525 were seen on the last crawl, 2026-06-11.
- **The 94 not seen:** 79 PDFs and 15 dataset zips. Wayback is the only source that ever saw them.
- **The live side is `POLITICS__FED_DOJ_EPSTEIN_LIBRARY`:** one fetch on 2026-06-11, 13 listing pages, 525 file links. It matches exactly the 525 seen.
- **Each live page holds about 50 links.** DataSet 1 live is EFTA 1-50, and its 50 "vanished" files are EFTA 612-668. DataSet 12's missing files all sit above the page's highest number. That's paging.
- **The Wayback table can't settle it.** `OPEN_DATA__XC_WAYBACK_DOJ_EPSTEIN` (1.54M rows) holds **zero** URLs under `/epstein/files/`, so 0 of 619 land.
- **Only thread left:** DataSet 3's EFTA00003488 and EFTA00003855 sit inside the live page-1 range but are missing from it. They were seen 2026-02-20 to 2026-03-18. Two files, unresolved.

---

## New data traps

| Table | Trap |
|---|---|
| PHMSA flagged incidents | The same release volume gets copied onto several reports. Sea Robin put 793,534 on two reports and 527,853 intentional on three. Units aren't stated; probably thousand cubic feet |
| NOAA storm events | Heat deaths are mostly Phoenix's paperwork. Phoenix logged no heat after 2024-06. Heat events are zone-based (`CZ_TYPE='Z'` on 19,676 of 19,677 Excessive Heat rows since 2010), so county-FIPS joins drop every heat death |
| NOAA storm events | The median damage estimate halved over time. That's a change in how it's estimated, not a trend |
| FEC PAC summary | No 2026 cycle (6 rows); 7,897 rows have no coverage date |
| FEC bulk committees | The facts-line "names repeat 148x" is an artifact. No name repeats more than 20 times |
| ICIS-FEC inspections | The top registry IDs are ports of entry (import desk audits). `ACTIVITY_ID` has 695 repeats. The case tables carry no dates |
| Wayback DOJ Epstein | It holds no `/epstein/files/` URLs at all, so it can't check file removals |

## Statements

27 of 35.

parked: all 17 agents share one scratchpad root. Early on I overwrote another agent's `q.py` and `s1.sql` there, and my first two runs bumped a shared `count.txt`, so another agent's statement counter may be off by 1-2. That agent has since rewritten its `q.py`. After that I worked only in the private subfolder `deep2_g5_mine/`.
