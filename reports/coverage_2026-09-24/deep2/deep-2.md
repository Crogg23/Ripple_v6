# Deep pass 2 (round 2): five EPA air tables

2026-09-24 · agent deep-2 · Python door · **26 queries**, plus the two required session lines on each of 7 connections · SQL in `deep-2.sql`, numbered to match the [n] tags below.
Bucket and peer math ran in Python on the rows the queries returned.

Every facility, company and plant named here is **a data match, not verified against primary records**.

---

## The menu

| Rank | Table | Verdict | The one number |
|---|---|---|---|
| 1 | ECHO | **live** | **In ICIS-Air, Nebraska shows zero state formal air enforcement actions in 9 straight years (2017–2025).** It filed 4–26 a year from 2000 to 2014. Of 58 high-priority air violations found since 2015, it resolved **4 (6.9%)**. The state median is **79%**. |
| 2 | ICIS_AIR_FCES_PCES | **live** | **227** Texas major air sources still report emissions or show enforcement activity, yet have had no full compliance evaluation in 5+ years. That is **9.1 per 100** Texas majors; the state median is **1.0**. New Mexico's rate is **20.6** (33 of 160). |
| 3 | ICIS_AIR_STACK_TESTS | **live (small)** | **30 of 44** Iowa plants that failed 3+ stack tests since 2015 have no formal action since 2015: **68%**. The state median is **16%**. Grain Processing Corp in Muscatine failed **53** tests in **11 separate years** and has had no formal action since 2015. |
| 4 | AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS | probed | Dow's Plaquemine, LA site reported **34,369 lb** of ethylene oxide air release in 2023. That is 8.7x its highest year from 2015 to 2022 and **21%** of the national TRI total. It fell back to 2,433 lb in 2024. The TRI-vs-EIS angle is dead: EIS copies TRI. |
| 5 | EGRID_PLANT_2022 | probed | No environmental-justice gradient within peers. The dirtiest quarter of coal plants has **9.7%** minority neighbors; the cleanest quarter has **8.6%**. The top "dirtiest per MWh" gas plants are a repowering artifact. |

> **Bad news up front**
> - **ECHO's `FORMAL_ACTION_COUNT` only counts roughly the last 5 years**, meaning actions dated after about 2021-06-18. "Zero formal actions" does not mean never. 1,328 chronic violators show 0 while also holding an older `DATE_LAST_FORMAL_ACTION`.
> - **About 80% of Texas's "never evaluated" majors look like dead records:** no activity and no emissions report since mid-2021. The raw "49% of Texas majors unevaluated" headline is mostly that artifact.
> - **eGRID 2022 carries CO2 twice at repowered sites.** The old plant ID holds the smokestack CO2 and the new plant ID holds an EIA estimate. That produces impossible rates, like 31,855 lb/MWh at AES Huntington Beach.
> - **Ohio sends almost no stack tests to ICIS-Air:** 2 records since 2015 for 547 majors. A state's missing stack tests are a data gap, not a clean record.
> - There is **no county income table** in the warehouse, so the "poor counties" half of the eGRID angle could not run.

---

## 1. ECHO — live (the Nebraska air lead)

**The physical thing:** Nebraska has plants that sat flagged as high-priority air violators for three straight years. From 2017 to 2025, the state logged no formal enforcement action against any plant in ICIS-Air.

**Shape** [1][6][7]
- 3,135,554 rows, one per facility, most of them inactive or never violating.
- `SIGNIFICANT_NONCOMPLIANCE_FLAG` is 'N' everywhere, as the trap file says. I used `THREE_YR_COMPLIANCE_HISTORY` instead: 12 letters, one per quarter, where S means significant violation.

**Checked** [12]
- I pulled every active facility whose history shows S in at least the first 11 of 12 quarters: **5,619** facilities.
- **4,415 (78.6%)** of them have `FORMAL_ACTION_COUNT = 0`.
- **By program:** water-only 3,360 (2,978 with zero formal actions), air-only 210 (110 with zero), RCRA-only 199 (109 with zero).
- **Second field:** I joined ICIS-Air `CURRENT_HPV` by registry ID. For air-only facilities, ICIS shows an HPV status (Addressed or Unaddressed) on 200 of 210, so the S-string and ICIS agree.
- **Trap found:** 79 of the 110 air-only "zero formal" facilities carry ICIS status *Addressed*, which means a formal action does exist. The count is a window, not a lifetime.
- For the real "nobody acted" set, I kept facilities with **12 of 12 S quarters AND an ICIS status of Unaddressed**. That leaves 261 facilities, 217 of them majors; 109 have no formal action in the window.

**Peers** [14][19] (denominator = operating major air sources in ICIS-Air, 49 states with 30+ majors)

| State | Operating majors | Unaddressed HPV every quarter for 3 yrs | Per 100 majors |
|---|---|---|---|
| **Nebraska** | 120 | **13** (all 13 with zero formal actions in the window) | **10.8** |
| California | 1,015 | 79 | 7.8 |
| Indiana | 560 | 27 | 4.8 |
| **State median** | — | — | **0.4** |

**Then the state roll-up** [19][22][26]

| Measure (since 2015) | Nebraska | State median |
|---|---|---|
| State-filed formal actions per operating major | **0.04** (5 since 2015, 4 of them in 2015–16) | 0.79 |
| HPVs resolved | **4 of 58 (6.9%)** | 79% |
| HPVs open 3+ years, per 100 majors | **29.2** (35 open) | 1.35 |

- **By year:** Nebraska's state formal actions ran 7, 14, 11, 12, 26, 9, 16… per year from 2000 to 2014. Then 1 in 2015, 3 in 2016, and **0 every year from 2017 to 2025**. EPA itself filed 0–2 a year in Nebraska over the same stretch.
- **Nebraska still inspects and still writes letters:** 53–69 full evaluations of majors a year [23], and 668 informal actions since 2015 [19]. The data flow is alive; only formal actions and resolved dates stopped.
- **9 of the 13 chronic Nebraska majors are ethanol, corn or soy plants:**
  - E Energy Adams, Green Plains Central City and Green Plains Wood River
  - KAAPA Ravenna and KAAPA Aurora, Siouxland Ethanol, POET Fairmont
  - ADM Corn Processing Columbus, AGP Soy Hastings
- Their open HPVs are dated 2020-10 to 2024-09. Most are VOC and PM10 violations, with some NOx and SO2 [22].

**Hit means:** Nebraska's air regulator has either stopped formal enforcement or stopped reporting it to EPA, which is required for HPVs at majors. Either one is a story about state enforcement and EPA oversight.

**Miss would have meant:** Nebraska looks like its peers once you divide by majors. It doesn't, on any of three separate measures.

**Boring explanation:** NDEE may resolve cases through consent orders or letters that never get keyed into ICIS-Air. **Not ruled out.** A records request for NDEE air consent orders from 2017 to 2025 settles it. Also check whether local outlets such as the Flatwater Free Press have covered NDEE enforcement.

**The other ECHO angle, the biggest penalties** [21]
- The top of `LAST_PENALTY_AMT_ALLOCATED` is national settlements booked on one address: BP Deepwater $3.37B, Volkswagen $1.45B, Chrysler $305M.
- These are known and not a lead.

**Water-only chronic violators** (3,360, led by LA 800, WV 671, WA 615 in the full list)
- These are probably missed monthly discharge reports, not pollution. I did not check the letter codes against the NPDES source.
- **Unverified; do not build on it.**

---

## 2. ICIS_AIR_FCES_PCES — live (Texas, New Mexico)

**The physical thing:** big air-permitted plants that are still running and reporting emissions, but with no record of a full compliance evaluation in 5+ years. A full evaluation is the inspection EPA policy expects about every 2 years at a major.

**Shape** [3][9][15]
- 1,779,096 rows. Of those, 629,344 are on-site full evaluations (FCE) at 100,637 facilities, and 21,532 are off-site FCEs.
- Dates run 0025 to 2026. There are 25 junk dates before 1970, and I dropped them.
- At least 98% of evaluation facility IDs land in the ICIS-Air facility table. 2,597 IDs (1.8%) come back with no class or status: either unmatched, or blank facility rows [15].

**Checked** [14][20]
- For each of the **13,559 operating major sources**, I took the last FCE date.
- **Nationally:** 10,369 had an FCE within 2.5 years, 1,187 between 2.5 and 5 years, 1,348 more than 5 years ago, and 655 never.
- **Texas:** 1,221 of 2,481 majors (49.2%) are 5+ years stale or never evaluated. The state median is 3.6%.
- **Then the alive test.** A stale major only counts if it shows life since mid-2021: a stack test, violation, or informal or formal action in ICIS, or a TRI, GHG or CAMD emissions report for 2022 or later.
- I also dropped any plant where another major permit at the same registry ID got an FCE since mid-2021.
- **Result:** 79% of the stale Texas majors show no life. They are dead records still marked "operating."

**Peers** (denominator = operating majors; 49 states with 30+)

| State | Majors | Alive, no FCE 5+ yrs, no sibling covered | Per 100 |
|---|---|---|---|
| **New Mexico** | 160 | 33 | **20.6** |
| **Texas** | 2,481 | **227** | **9.1** |
| Ohio | 547 | 48 | 8.8 |
| California | 1,015 | 63 | 6.2 |
| **State median** | — | — | **1.0** |

- **Texas volume** [23]: 1,210 major FCEs in 2014, then 661–745 a year every year since 2015. About 1,500 Texas majors look alive (1,260 current plus 257 stale-but-alive). At one FCE every 2 years they need about 750 a year, and Texas logs about 700. So the yearly total is close, and the gap sits on specific plants.
- **By industry:** 55 of the 227 Texas plants are oil and gas extraction and 40 are landfills. 85 have never had an FCE on record.
- **Biggest by 2023 GHG** (joined by registry ID, so it may include other permits at the site):
  - Praxair, Texas City: no FCE ever, 1.29M t CO2e
  - Performance Materials NA, Orange: last FCE 2012-11, 1.23M t
  - Cemex Balcones Quarry, New Braunfels: last FCE 2009-04, 1.12M t
  - Targa Midstream Mont Belvieu: last FCE 2005-12, 1.10M t

**Hit means:** a named list of running Texas and New Mexico majors that the state has not fully evaluated in 5 to 20 years. The rate is 9–20x the median state.

**Miss would have meant:** the stale plants are all dead records. About 80% of Texas's are, which is why the raw 49% headline is wrong.

**Boring explanation:**
- TCEQ may log inspections under a minor or area permit at the same site; I only checked sibling majors.
- It may also keep investigations in its own system without flowing them to ICIS.
- **Partly ruled out** (sibling majors checked; minors were not).
- **Next step:** check 10 names against TCEQ's CCEDS investigation search.

---

## 3. ICIS_AIR_STACK_TESTS — live, small (Iowa)

**The physical thing:** a smokestack test that measured more pollution than the permit allows, repeated at the same plant year after year.

**Shape** [2][8][15]
- 620,302 rows. Since 2015 there are 293,647 passes and 8,867 fails: a **2.9% fail rate**, at 2,689 failing facilities. All 2,689 land in the ICIS-Air facility table with a name.
- `POLLUTANT_DESCS` is empty, as the trap file says. The pollutant sits in `POLLUTANT_CODES` and is blank on about a third of rows.
- **One row is one unit × pollutant test, not one test day.** Ampersand Chowchilla logged 120 fails on 2021-05-10 alone.

**Checked** [13]
- For each facility: its fails since 2015, and whether each fail was followed by a pass on the same pollutant within 180 days.
- Then its ICIS-Air formal actions (by settlement date), informal actions and violations since 2015.
- **53.7% of fail rows were retested and passed within 180 days.**

**The national angle mostly fails**

| Fails since 2015 | Facilities | No formal action since 2015 |
|---|---|---|
| 10+ | 113 | **9** |
| 5–9 | 173 | 41 |
| 3+ (all repeat failers) | 671 | 141 (21.0%) |

**Peers** (denominator = facilities with 3+ fails; 31 states with 5+ such facilities)

| State | Repeat failers | No formal action since 2015 | % |
|---|---|---|---|
| North Dakota | 5 | 5 | 100% |
| Nebraska | 10 | 8 | 80% |
| **Iowa** | **44** | **30** | **68.2%** |
| **State median** | — | — | **15.7%** |

- **Iowa's fail rate is 9.3%** (435 of 4,701 tests since 2015). The state median is 3.5% [19].
- **Iowa state formal actions:** 1–6 a year since 2015, against 9–80 a year from 2000 to 2014 [26].
- **Iowa still closes its HPVs,** 41 of 55 [19]. So Iowa is resolving cases through informal letters (843 since 2015), not ignoring them.
- **Grain Processing Corp, Muscatine IA:**
  - 53 failed tests out of 220, in 11 separate years from 2015 to 2025
  - 0 formal actions since 2015 (3 ever), 41 informal actions, 38 violations, 1 HPV
  - The failed pollutants are PM2.5, PM10, SO2 and VOC.

**Hit means:** Iowa lets repeat stack-test failures ride on warning letters. Muscatine is the named case.

**Miss would have meant:** repeat failers everywhere draw formal actions. Nationally they mostly do.

**Boring explanation:**
- Iowa may record more fails simply because it records more honestly; Florida logs 0.6% fails.
- Iowa may treat stack fails as lower-tier violations that a retest clears.
- **Not ruled out.** Pull GPC's Iowa DNR file.
- **Also:** this lead overlaps the Nebraska lead in #1. Nebraska's 8 of 10 is the same pattern.

---

## 4. AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS — probed

**The physical thing:** pounds of a named chemical out of one plant's stacks and leaks in one year.

**Shape** [4][10][11]
- 10,411,826 rows, from four programs:
  - EIS: 9.4M rows, only 2008, 2011, 2014, 2017 and 2020
  - TRIS: 2015–2024
  - E-GGRT: 2015–2023
  - CAMDBS: 2015–2024
- **TRI and EIS overlap only in 2017 and 2020.**

**TRI vs EIS — dead** [16]
- Of 80,723 TRI facility-pollutant-years, 36,653 match an EIS row on registry ID, pollutant and year.
- **The median TRI/EIS ratio is exactly 1.00 for every top pollutant.** EIS fills point-source toxics from TRI, so it is not an independent check.
- 2,385 of 33,851 both-positive pairs (7.0%) differ by 10x or more.

**Ethylene oxide** [17][24]
- The TRI national air total averaged **216.8K lb/yr in 2015–19**, then **149.1K lb/yr in 2022–24**, then **120.7K** in 2024. It went down, not up.
- **Dow Chemical, Louisiana Operations (Plaquemine):**
  - Reported 2,849–4,512 lb every year from 2015 to 2022, then **34,369 lb in 2023** (8.7x its previous high), then 2,433 in 2024.
  - TRI_BASIC_2023 confirms the 34,369 lb, and says **32,106 lb of it was fugitive**, meaning leaks rather than stacks.
  - That is 21% of 2023's national TRI EtO air total of 160,219 lb.
  - ECHO lists 54% minority neighbors.
- **Sterilization Services of Virginia, Henrico:** 13,821 lb in 2022, #2 nationally; 72% minority neighbors. This sterilizer is probably already on EPA's public EtO lists (known).

**Hit means:** a one-year leak spike at Dow Plaquemine worth one records pull (LDEQ incident reports for 2023).

**Boring explanation:** a single reported upset event, likely already disclosed to LDEQ. **Not ruled out.** A **probed** row, not live.

---

## 5. EGRID_PLANT_2022 — probed

**The physical thing:** pounds of CO2 per megawatt-hour from one named power plant.

**Shape** [5]
- 11,974 rows. One is a header row (`PNAME`), so 11,973 plants.
- Numbers are stored as text, and the mercury columns are empty.

**Checked** [18][25]
- I ranked the 1,281 plants that made over 100,000 MWh.
- Medians: coal 2,273 lb/MWh, gas 908.

**The top of the ranking is an artifact.** Five gas plants show 3,419–31,855 lb/MWh, which is physically impossible. Three are repowered sites, where the old plant ID and the new plant ID both carry CO2. The other two, Gleason TN and Antelope Elk TX, are unexplained:

| Old plant (CO2 from EPA smokestack monitors) | New plant (CO2 from EIA estimates) |
|---|---|
| AES Huntington Beach, ID 335: 1.69M t on 106K MWh | HB Energy Project, ID 62116: 1.57M t on 3.9M MWh |
| AES Alamitos, ID 315: 1.94M t on 630K MWh | Alamitos Energy Center, ID 62115: 1.40M t |
| Lauderdale, ID 613: 1.65M t on 315K MWh | Dania Beach 7, ID 65978: 1.47M t |

- The old IDs' fuel burn is impossible too: Alamitos implies about 51,700 Btu/kWh.
- **This looks like up to about 5.3M t of CO2 counted twice.**

**The real top is known:** Pennsylvania waste-coal plants, for example Mt. Carmel Cogen at 5,052, Rausch Creek 4,890 and Scrubgrass 3,254.

**The EJ join** (eGRID plant ID → the CAMD rows in the combined emissions table → registry ID → ECHO)
- 829 of 1,106 fossil plants over 100K MWh (75%) have a registry ID.
- 791 of those land in ECHO (71.5%), and the state agrees on **791 of 791**.

**Peers** (median % minority neighbors, by CO2-rate quarter, within fuel)

| Fuel | Cleanest quarter | Dirtiest quarter |
|---|---|---|
| Coal (200 plants) | 8.6% | 9.7% |
| Gas (576 plants, impossible rates dropped) | 32.6% | **20.7%** |

**Hit would have meant:** dirtier-per-MWh plants have more minority neighbors than their own fuel peers.

**Miss (what happened):** coal is flat and gas runs the other way.

**Boring explanation:** big coal plants sit in rural places. That is ruled in, not out.

**Verdict:** probed. The ranking is EPA's own product, and the one surprise is a data artifact.

---

## New data traps

| Table | Column / thing | The catch |
|---|---|---|
| ECHO | `FORMAL_ACTION_COUNT` | Counts roughly the last 5 years only. Among chronic violators, every row reading 0 has its last formal action on or before 2021-06-18, and 1,328 of them read 0 with an older date on file. 99% of rows with a count have a last action after 2021-07. |
| ICIS-Air stack tests | coverage by state | Ohio: 2 records since 2015 for 547 majors. One row is one unit × pollutant, so San Joaquin Valley logs 100+ a day. |
| ICIS-Air facilities | "operating" majors | About 80% of Texas majors with no FCE in 5 years show no activity or emissions since mid-2021. They are dead records still marked OPR. |
| eGRID 2022 | repowered plants | The old plant ID carries smokestack CO2 and the new ID an EIA estimate. Impossible lb/MWh and a double count (Huntington Beach, Alamitos, Lauderdale). |
| Combined emissions | EIS vs TRI | EIS copies TRI for point toxics (median ratio 1.00). It is not a second source. |
| Combined emissions | sums by REGISTRY_ID | A site's GHG repeats on each of its permits. The Clear Lake plants of Clariant, Celanese and Praxair each show 845,112 t. |
| Combined vs TRI_BASIC_2023 | Port Neches EtO plant | The same 20,180 lb report sits under registry 110072129444 (named Indorama) in one table and FRS 110000599567 (named Huntsman) in the other. |

---

## Statement count

**26 queries** against a 35 budget, plus the two required `ALTER SESSION` lines on each of 7 connections. All were SELECT or WITH. None failed.
