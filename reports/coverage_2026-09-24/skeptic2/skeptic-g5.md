# Skeptic g5: three EPA air (ICIS-Air) leads from deep-2

2026-09-24 · Python door · 22 read-only statements (plus 2 compile errors, re-run) · SQL in `skeptic-g5.sql`, tags [L1-n] [L2-n] [L3-n]
Every facility or company named is **a data match, not verified against primary records.**

| Lead | Verdict | Grade |
|---|---|---|
| ECHO / ICIS-Air: Nebraska formal actions | **CONFIRMED** | **B** |
| ICIS_AIR_FCES_PCES: Texas / New Mexico stale majors | **NARROWED**: Texas falls from 9.1 to 3.0 per 100 and New Mexico is the lead | **B** for NM, **C** for TX |
| ICIS_AIR_STACK_TESTS: Iowa repeat failers | **NARROWED**: the state stat is just Iowa's low formal-action rate; the GPC plant holds up | **B** for GPC, **C** for the state stat |

---

## ECHO / ICIS-Air formal actions (Nebraska): CONFIRMED

**Claim as written:** Nebraska shows zero state formal air enforcement actions in ICIS-Air for 9 straight years (2017-2025), after 4-26 a year in 2000-2014. It resolved 4 of 58 HPVs found since 2015 (6.9%). The state median is 79%.

**What I checked:**
- [L1-1] Every Nebraska ICIS-Air formal action by agency flag, type and era, **including undated rows**:
  - **0 undated rows**, so nothing is hiding in a null settlement date.
  - State (S) filed 394 administrative orders and 87 judicial actions before 2015, then 1 in 2015-16 and **0 since**.
  - Local agencies (L = Lincoln-Lancaster, Omaha) filed 102 orders before 2015, then 3 in 2015-16, then 1 dated 2026, which is outside the claim's window.
  - EPA (E) filed 10 since 2017.
- [L1-2] ACTIVITY_ID works as a rough clock (the median id climbs every year), which backs up the undated-row check. There were none to place anyway.
- [L1-4] Peer check, states with 30+ operating majors, state plus local formal actions settled 2017-2025:
  - Nebraska: **0**, down from 89 in 2005-14.
  - North Dakota: also 0, but it had only 1 in 2005-14. ND never reported; Nebraska stopped.
  - The next-lowest are PR (1), WI (22) and AK (14).
- [L1-3] Nebraska informal actions did not stop. Warning letters gave way to NOVs in 2020, and NOVs ran 46-107 a year from 2020 to 2025 (107 in 2023). The data pipe is live.
- [L1-7] HPVs by day-zero year:
  - Every HPV from 2005-2013 was resolved.
  - For day zero 2017-2026, 2 of 52 were resolved.
  - Since 2015 overall, **4 of 58**, which matches the claim.
  - New HPVs still arrive (4 with 2026 day zero), so the violation feed is also live.
- [L1-6] Local agencies:
  - Omaha has 13 operating majors and Lincoln-Lancaster has 16.
  - **All 58 HPVs since 2015 are state-agency HPVs.** The locals logged none, so delegation does not explain the gap.
- [L1-5, L1-8] ECHO's own frame:
  - 14 air-only Nebraska facilities show a `DATE_LAST_FORMAL_ACTION` after 2017.
  - Only 1 of them has an ICIS-Air formal action: an EPA vehicle/engine case.
  - The other 13 are small ag co-ops and retailers, likely non-air statutes (not checked).
  - This does not contradict the claim.
- [L1-9] Current HPV status of operating majors:
  - NE: **15 Unaddressed-State**, 0 Addressed.
  - IA: 6 unaddressed, 3 addressed. KS: 2 unaddressed, 4 addressed. MO: 6 unaddressed. SD: 0.

**What a hit means / what a miss means:**
- A hit (it held) means NDEE either stopped using formal orders on air violators in 2017, or stopped keying them into the federal file. Violations and NOVs kept flowing, and resolutions stopped.
- A miss would have been undated formal rows, local-agency actions, or a national reporting change. None showed up.
- **Still not ruled out:** NDEE settles cases on paper (for example, consent orders routed through the state AG) that never reach ICIS. The warehouse cannot separate "not enforcing" from "not reporting."
- Either way, it is a federal-oversight story, because HPV reporting is required.

**Is it famous?** Possibly. EPA's State Review Framework reviews of Nebraska would likely flag HPV timeliness. Check the Round 4 report before pitching this as new. If EPA flagged it and nothing changed, that is the story.

**Corrected headline:** Nebraska's state and local air regulators logged 89 formal enforcement actions in ICIS-Air in 2005-2014 and **zero settled in 2017-2025**. No other state with 30+ majors went from active to zero. Over the same years, Nebraska kept sending NOVs (107 in 2023) and new high-priority violations, but resolved only 4 of 58 HPVs since 2015. 15 operating majors sit "Unaddressed" today.

**Portfolio grade:** B. The chart is ready (formal vs informal vs HPVs by year). It needs one outside check: the NDEE records request or the EPA SRF report.

**Next join that would make it a story:** Join `ICIS_AIR_VIOLATION_HISTORY` (the 15 unaddressed majors) to `AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS` on REGISTRY_ID, for VOC and PM tons from those ethanol plants during the open-violation years.

---

## ICIS_AIR_FCES_PCES (Texas, New Mexico stale majors): NARROWED

**Claim as written:** 227 Texas majors still report emissions or show activity, yet have had no full compliance evaluation (FCE) in 5+ years: 9.1 per 100, against a state median of 1.0. New Mexico is 20.6 (33 of 160).

**What I checked:**
- [L2-4] Rebuilt the method (cutoff 2021-07-01; alive = ICIS activity since then, or a TRI/GHG/CAMD report in 2022+; drop sites where a sibling major got an FCE). Result: **TX 226, NM 33.** It reproduces.
- [L2-1] TCEQ sends ICIS **only FCEs**: 7,736 since 2015, zero state partial evaluations. The PCEs in Texas are all EPA's. Texas investigations below FCE level never reach this file, so "no FCE" can mean "evaluated, but not under this label."
- [L2-2] Classification holds: 2,296 of 2,481 Texas majors have an operating Title V program.
- Python on the L2-5 rows, the 226 Texas plants:
  - **120 are "alive" only because a registry-level emissions report exists.** They have no ICIS activity at all since mid-2021.
  - 46 of those 120 have **no evaluation of any kind ever**. They look like shell records attached to a site registry.
  - 22 had an FCE in 2020-21, so they are barely past 5 years.
- [L2-6] Age check on program begin dates:
  - 44 of 85 Texas "never evaluated" plants began after 2021-07, and 8 of 11 in New Mexico did.
  - These are new sources in their first cycle, not 5 years overdue.
  - Caveat: `BEGIN_DATE` is not a clean start date. 12 plants with pre-2021 FCEs also show a post-2021 begin.
- [L2-7] Named example, **Praxair Texas City (no FCE ever, 1.29M t CO2e):**
  - Two other Praxair majors in Texas City had FCEs: the Hydrogen Complex on 2022-04-27 and Praxair Texas City on 2023-06-20.
  - The sibling check matched on exact registry, so it missed them.
  - The deep report's top-named plant is **probably covered under another record**.
- [L2-8] Rebuilt per state:

| State | Majors | Original | Age fix | Strict (age fix + ICIS activity required) |
|---|---|---|---|---|
| **NM** | 160 | 33 (20.6) | 24 (15.0) | **20 (12.5), rank 1** |
| OH | 547 | 48 (8.8) | 43 (7.9) | 28 (5.1), rank 2 |
| KY | 261 | 14 | 12 | 10 (3.8) |
| **TX** | 2,481 | 226 (9.1) | 170 (6.9) | **74 (3.0), rank 6** |
| State median | | 1.0 | 0.3 | 0.0 |

**What a hit means / what a miss means:**
- New Mexico holds under every filter. 20 plants with live ICIS activity and no FCE in 5+ years, 1 in 8 of its majors.
- By city in the L2-5 list (not recounted by query), about 12 of the 20 are gas plants or compressor stations in the Permian (Artesia, Eunice, Hobbs, Loco Hills, Monument). The rest are power plants, a landfill, a dairy plant and White Sands.
- **Caveat:** most of NM's last FCEs fall in 2019-2021. That makes them 5-7 years overdue, not decades.
- Texas mostly misses: two thirds of its 226 (152) go away once shell records and new sources are removed.
- What is left in Texas is still a TCEQ reporting-habit question, since TCEQ sends FCEs only.

**Corrected headline:** 20 of New Mexico's 160 operating major air sources, 12.5 per 100 and the highest of any state, show enforcement or test activity since mid-2021 but no full compliance evaluation in 5+ years. The median state has none. Most last had an FCE in 2019-2021, and about 12 are Permian gas plants. Texas's figure shrinks to 74 (3.0 per 100) once shell records and new plants are removed.

**Portfolio grade:** B for New Mexico. It needs the NMED inspection list, or a check of 5 names against NMED records. C for Texas. Drop the Praxair example.

**Next join that would make it a story:** Join the NM 20 to `AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS` (E-GGRT, 2022-2023) on REGISTRY_ID for size, and to `ICIS_AIR_VIOLATION_HISTORY` on PGM_SYS_ID. Plants that are violating but not being inspected are the story.

---

## ICIS_AIR_STACK_TESTS (Iowa repeat failers, Grain Processing Corp): NARROWED

**Claim as written:** 30 of 44 Iowa plants that failed 3+ stack tests since 2015 have no formal action since 2015 (68%), against a state median of 16%. GPC Muscatine failed 53 tests in 11 years with no formal action.

**What I checked:**
- [L3-1] Iowa stack tests are clean on units: 1 activity id = 1 row, and fails are mostly 1 per facility-day (435 rows on 393 days). This is unlike California's local agencies, where 3,480 local fail rows sit on 615 days.
- [L3-4] Recounted by distinct **fail days**, not rows:
  - Iowa: **27 of 41, 65.9%**. State median 14.3%.
  - The rank holds: behind ND, NE and KY, all of them small n.
- [L3-4] **The base-rate check breaks the framing:**
  - 88.3% of all Iowa operating majors have no formal action since 2015. The median state is 66.9%.
  - Among Iowa majors that never failed a test, **5.6%** got a formal action. Among repeat failers, 34% did.
  - In Iowa, failing a stack test makes a formal action **about 6x more likely**. The 66% is Iowa's general low formal-action rate (the same "letters, not orders" pattern as Nebraska), not special leniency on stack tests.
- [L3-2] GPC Muscatine (IA0000001913900025):
  - Confirmed: 53 fail rows on **49 separate days**, in 11 years, out of 221 tests on 150 days.
  - 41 informal actions since 2015.
  - Lifetime formal actions: **3, all from 2005-2007**, with a $10,000 penalty.
- [L3-2] **The sister plant: GPC in Washington, Indiana**, a data match on name:
  - 31 fail rows on 20 days since 2015.
  - **8 Indiana state administrative orders since 2015**, $997K in penalties. 7 of them ($687K) fall in 2015-2025, and the 8th ($310K) is dated 2026-06-02.
  - Same company and same kind of failures; one state orders and fines, the other writes letters.
  - The "PA Grain Processing LLC" hit is a different company. Ignore it.
- [L3-3] From 2017 on, GPC's fail rows carry a **blank pollutant code**. The "retest passed within 180 days" match on blank-to-blank is meaningless, so you cannot tell from this file which pollutant failed after 2016.

**What a hit means / what a miss means:**
- The GPC contrast held, and it is the story.
- The Iowa-wide stat is real but not specific to stack tests. It restates "Iowa rarely uses formal orders."

**Is it famous?** Partly. GPC Muscatine's air pollution is a long local fight. The resident nuisance class action (Freeman v. Grain Processing Corp.) reached the Iowa Supreme Court around 2014. That is from memory; check it. The Iowa-vs-Indiana sister-plant angle is probably not covered.

**Corrected headline:** Grain Processing Corp's Muscatine, Iowa corn mill failed stack tests on 49 separate days across 11 years (2015-2025), and Iowa's last formal order against it is from 2007. The same company's Washington, Indiana plant failed on 20 days and drew 7 Indiana state orders and $687K in penalties in 2015-2025, plus an 8th order ($310K) in June 2026.

**Portfolio grade:** B for the GPC Iowa-vs-Indiana contrast. It needs the Iowa DNR file, plus confirmation that the Indiana plant is the same company. C for the Iowa-wide stat.

**Next join that would make it a story:** Join both GPC registry IDs (110017404548 IA, 110041204265 IN) to `AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS` on REGISTRY_ID, for PM/SO2/VOC tons per year. Same company, two regulators, emissions side by side.
