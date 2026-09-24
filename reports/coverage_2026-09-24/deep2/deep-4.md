# deep-4: five environment tables, hand-queried

2026-09-24 · coverage round 2 · 33 SQL statements (budget 35) · Python door, read-only
SQL: `reports/coverage_2026-09-24/deep2/deep-4.sql`
Every person, company or utility named here is a **data match, not verified against primary records**.

## The menu

| Table | Verdict | The one number |
|---|---|---|
| SDWA_SITE_VISITS | **live** | 117 big water systems, 8.7M people, have no sanitary survey on file in 5 years. The legal limit is 3. |
| SDWA_EVENTS_MILESTONES | **live** (lead thread only) | 1,029 systems tested over the lead action level since the new notice rule started. They serve 3.27M people. Only 276 have a notice row. |
| RCRA_VIOSNC_HISTORY | probed | All 2,513 of the 10-year-plus "in violation" runs end the month someone typed in a fix date |
| FRACFOCUS_DISCLOSURE_LIST | probed | Midland TX: 131B gallons of frack water. Permian operators all sit within 0.74x to 1.46x of the basin median. |
| SDWA_PUB_WATER_SYSTEMS | dead (as a story) | Private systems had *fewer* health-based violations than city systems, in every size band |

---

## 1. SDWA_SITE_VISITS: live

**What was checked.** For every active community water system (the kind that serves homes), I took the latest sanitary survey date. That counts full surveys (SNSV), partial ones (SNSP) and follow-ups (SNSF). I joined that to the system roster for the number of people served.

- **Every state reports surveys.** Nationally, 96.9% of 49,378 community systems have one since 2021-07. So a gap here is a system gap, not a whole state that never uploads.
- Among big systems (10K+ people), **117 of 4,622 have nothing since 2021-07-01**. They serve **8.73M people** (7.51M if you drop wholesalers).
- The federal clock for community systems is 3 years. On that clock, **713 of 4,622 big systems (15.4%) are past due. They serve 43.2M people.**

**Peers, share of big systems past the 3-year clock:**

| State | Big systems | Past 3 years | Share |
|---|---|---|---|
| WA | 131 | 57 | 43.5% |
| OR | 65 | 27 | 41.5% |
| CA | 446 | 131 | 29.4% |
| NJ | 161 | 42 | 26.1% |
| TN | 147 | 5 | 3.4% |
| National | 4,622 | 713 | 15.4% |

**Largest with no survey of any sanitary kind since 2021-07:**

| System | People | Last survey | Last visit of any kind |
|---|---|---|---|
| Veolia Water NJ Hackensack | 792,713 | 2019-06-13 | 2024-06 (RSCH) |
| Eastern Municipal WD, CA | 666,581 | 2019-05-14 | 2024-08 (PRMT) |
| City of Fresno (wholesaler flag Y) | 545,716 | 2019-10-25 | 2025-06 (SITE) |
| Passaic Valley Water Commission, NJ | 310,483 | **2014-04-23** | 2025-08 (INVG) |
| Riverside, CA | 298,398 | 2019-11-06 | none since |
| Helix WD, CA | 277,668 | 2019-04-11 | none since |
| Jersey City MUA | 262,000 | **2015-04-28** | 2020-10 |
| Trenton Water Works | 217,000 | **2015-06-30** | 2022-04 (INVG) |

- **Hit means:** big utilities had no sanitary survey logged with EPA for 5 to 12 years. The misses bunch up in CA and NJ, while peer states run near zero.
- **Miss would have meant:** big systems all current, with gaps only at campgrounds and trailer parks. That's not what came back.
- **Boring explanations:**
  - *Partial surveys logged under another code.* **Ruled out in part.** Counting SNSP and SNSF drops LA DWP (3.9M people, partial survey 2025-09) and 3 others. 117 are left.
  - *Outstanding performers get 5 years.* **Ruled out.** The 117 are past even 5 years.
  - *States upload late.* **Not ruled out.** The data runs to 2026Q2.
  - *NJ's big systems get visits under other codes.* **Not ruled out.** They show investigation and records visits (INVG, RSCH) in 2022-2025.
  - Next step: ask NJDEP and CA's Division of Drinking Water for survey dates on 5 named systems.
- **Side check: repeat "significant deficiency" grades.** 16,473 of 48,807 surveyed systems (34%) got at least one S grade since 2016. So S is common, and "keeps getting S" is weak. 6,544 systems got S on 2 or more surveys (45.0M people), 559 of them big.

## 2. SDWA_EVENTS_MILESTONES: live on lead notices; the triage angle is dead

**The triage angle is dead: "missed the lead-pipe inventory (LSLI) or PFAS deadline."**
- LSLI rows are all or nothing by state. **15 oversight agencies have zero LSLI rows**, among them PA, FL, OH, WA, MA, MN and CO. The states that do report have 95-100% of systems covered. A missing row means a missing upload.
- An LSLI row is a schedule, not proof the inventory was sent in. EVENT_ACTUAL_DATE sits on the 2024-10-16 deadline itself.
- PFAS rows are **future due dates, 2027-04-26 to 2028-12-31**. Nothing is past due yet.

**The live thread: LALE, "Tier 1 public notice for lead action level exceedance."** A system only gets one of these rows after its lead test goes over the limit.
- 288 systems have a LALE row, serving 1.195M people. All 288 matched the roster.
- **Second field agrees.** 276 of the 288 (96%) show a lead 90th percentile (PB90) over 0.015 mg/L since mid-2024 in the LCR samples table.
- **Illinois leads: 38 systems, 803K people.** Many share one date, 2025-07-15. Aurora (183,000), Illinois American-Peoria (137,575), Elgin (114,797), Palatine, Bartlett, Calumet City, Northbrook. Michigan is next: 21 systems, 205K people (Taylor, Madison Heights, Hamtramck, Inkster).
- **The bigger number: 1,029 systems had PB90 over 0.015 in a sampling period ending on or after 2024-10-16. They serve 3.27M people.**

| Group | Systems | People |
|---|---|---|
| Over the limit, has a LALE row | 276 | 1,129,991 |
| Over the limit, no LALE row, in a state that does log LALE | 360 | 840,094 |
| Over the limit, in a state with no LALE rows at all | 393 | 1,301,340 (largest system 675,647) |

- **Hit means:** since the new rule, 1,029 systems have tested over the federal lead limit, with 3.27M people and a named Illinois suburban cluster.
- **Miss would have meant:** LALE rows that don't match lead results, which would make them schedule noise. That's not what came back: 96% match.
- **Boring explanations:**
  - *The new rule changed where samples are taken.* **Not ruled out.** Since the 2024 lead rule, sampling targets homes with lead pipes, so exceedances climb where lead pipes are, and Illinois has the most. That can be a rule change, not worse water.
  - *The 753 systems with no LALE row look like missed notices.* **Not usable as a finding.** It's absence, and 393 of them sit in states that never log LALE at all.

## 3. RCRA_VIOSNC_HISTORY: probed

**What was checked.** For each site, I found the unbroken runs of months flagged "in violation" (VIO_FLAG = Y). For every run of 10 years or more, I checked it against the site's violation records: when each was found, and when it got a return-to-compliance (RTC) date.

- The table only holds months when a site was in violation or a serious violator. Every one of the 106,419 VIO_FLAG = N rows has SNC_FLAG = Y. **So "96% Y" is built in.**
- There are 2,513 runs of 10 years or more. **In all 2,513, the last flagged month is the month an RTC date lands, or the month just before it.**
- Median gap from the last violation found to the end of the run: **8 years**. **1,098 runs (44%) went 10+ years with no new violation found.** The flag stays up because one old violation was never closed.
- **Only 2 sites are in a 10-year-plus run today** (TX 1, IL 1), out of 592 sites flagged right now.
- **Close-out wave:** 64 of the 10-year-plus runs ended in 2025-26, 32 of them over 20 years long. The ones in the top 25 are IL, CT and OH sites. The state split for all 64 was not run.

| Site (data match) | Run | Months | What's behind it |
|---|---|---|---|
| Reserve Environmental Services, Ashtabula OH | 1982-04 to 2025-04 | 517 | 125 violations, the last found 2019; 143 serious-violator months; 91 inspections. **The one that looks real.** |
| Medallic Art, Danbury CT | 1982-09 to 2025-07 | 515 | Last violation found 1993, closed 2025-07-31 |
| Indian Refining, Lawrenceville IL | 1991-09 to 2025-05 | 405 | 1 violation (1991-09-13), 1 inspection ever |
| Brower Mfg, Quincy IL | 1989-04 to 2026-07 | 448 | Last violation 2004, last inspection 2005, closed 2026-07-20 |

- **Hit means:** mostly that states left 1980s-90s violations open for 20-40 years and closed them in bulk in 2025. That's a records-upkeep story, and a small one.
- **Miss:** a site polluting for decades. Only a handful, like Reserve Environmental with violations found through 2019, look like real repeat violators.
- **Boring explanation, "the flag carries forward until someone closes it":** **Confirmed**, 2,513 of 2,513.

## 4. FRACFOCUS_DISCLOSURE_LIST: probed

- 248,835 disclosures, 236,632 wells. **The job start and end date columns are empty. There is no date column.** The only stand-in for era is the form version (FF_VERSION, 1 to 4).
- **Median water per job by form version:** 1.58M gal (v1), 2.82M (v2), 12.0M (v3), 19.3M (v4). About 12x from first to last. That's the known longer-lateral trend.
- **Top counties** (jobs over 100M gal dropped as likely typos):

| County | Jobs | Billion gallons | Median per job, v4 |
|---|---|---|---|
| Midland, TX | 8,139 | 131.4 | 21.1M |
| Lea, NM | 7,701 | 116.8 | 19.9M |
| Martin, TX | 7,638 | 116.1 | 21.6M |
| Weld, CO | 12,424 | 112.6 | 18.2M |
| Eddy, NM | 7,066 | 107.5 | 20.3M |
| Reeves, TX | 6,230 | 101.6 | 22.3M |

- **Operators compared to their own basin.** I kept Permian v4 jobs only, so the era lines up: 17,206 jobs, basin median 21.0M gal.
  - The top operator is SM Energy at 1.46x (30.6M median, 177 jobs), then Apache at 1.23x.
  - Most sit between 0.80x and 1.25x.
  - Blackbeard is 0.19x: shallow wells, median TVD 5,196 ft.
  - **No outlier operator.**
- **The fresh-water join lands badly.** The water source table covers 20,302 of 248,835 disclosures (8.2%). "Fresh vs produced water" can only be told on that slice.
- **Hit means:** Permian counties each burned 100B+ gallons, and Midland alone is 5.9% of all frack water on file. Real, but reported many times before.
- **Miss:** a single operator using far more water than its basin peers. There isn't one.
- **Boring explanation, "water per well grows with lateral length":** **Confirmed** as the whole shape. Water per job is set by basin and era, not by company.

## 5. SDWA_PUB_WATER_SYSTEMS: dead as a story, fine as a denominator

- 434,040 systems. 142,891 are active, and 49,378 of those are community systems serving 331M people.
- **Wholesalers double count:** 2,485 active wholesaler community systems carry **56.6M** of that 331M. Drop them for any per-person rate.
- **Private owners** (P): 22,523 active community systems, 37.6M people (11%). **Local government** (L): 24,096 systems, 280M people.
- **The join:** health-based violations since 2021-01-01, counted as distinct violation IDs, private against local government within the same size band.

| Size | Private: share with a health-based violation | Local government: share |
|---|---|---|
| 500 people or fewer | 22.3% | 24.6% |
| 501-3.3K | 20.7% | 23.9% |
| 3.3K-10K | 18.3% | 22.0% |
| 10K-100K | **9.9%** | **17.8%** |
| 100K+ | 12.3% | 15.4% |

- **Hit would have meant:** private systems break health rules more. **Miss is what came back:** they break them less, in every band.
- **Boring explanation:** big private systems are investor-owned utilities with paid staff. It fits and wasn't tested further.
- **As a join partner it works:** 288 of 288 LALE systems and 1,029 of 1,029 lead-over-limit systems matched it on PWSID.

---

## Data traps found

- **RCRA_VIOSNC_HISTORY is an open-violation register, not a pollution record.** A run of Y months ends on the day an RTC date is typed in (2,513 of 2,513). The flag stayed up for decades on violations found in the 1980s and 90s. VIO_FLAG = N rows exist only when SNC_FLAG = Y.
- **SDWA LSLI rows are all or nothing by state.** 15 oversight agencies (PA, FL, OH, WA, MA, MN, CO and others) have zero. EVENT_ACTUAL_DATE on LSLI and PFAS rows is a due date, not a done date. PFAS dates run 2027-2028.
- **SDWA sanitary surveys come in three codes.** SNSV is full, SNSP partial, SNSF follow-up. Counting only SNSV flags LA DWP (3.9M people) as unsurveyed since 2017, but it has a partial survey dated 2025-09.
- **SDWA site-visit grades:** S means significant deficiency and is common (34% of surveyed systems since 2016). M means minor, R recommendation, N none, X not evaluated, Z not applicable, D is rare (29 rows).
- **FracFocus has no date at all.** Job dates are empty, and _SRC_FILE is one file, DisclosureList_1.csv. Form version is the only era stand-in. Water volume is filled on only 31% of v1 rows. The water source table covers 8.2% of disclosures.
- **Operator names drift in FracFocus.** OCCIDENTAL OIL AND GAS and OXYROCK OPERATING are separate rows, and COG OPERATING (Concho, bought by ConocoPhillips) stands alone. Operator sums undercount parent companies.

## Housekeeping

- The scratchpad folder is shared by all 17 agents. On my first run I copied a runner another agent had just overwritten, so one failed text block (5 queries sent as one, compile error, no data) got logged into **deep-1.sql**. I removed that block from deep-1.sql right away. deep-1's statement counter file (`scratchpad/count.txt`) may read one too high.
- My queries after that ran from a private folder. That failed block is counted in my 33.
