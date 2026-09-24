# Deep pass 2: five environment tables

2026-09-24 · agent deep-2 · Python door · 35 SQL statements (one, [19], failed to compile and was rerun as [24]) · SQL in `deep-2.sql`, numbered to match the [n] tags below.

Every water system, company, dam owner and plant named here is **a data match, not verified against primary records**.

---

## The menu

| Rank | Table | Verdict | The one number |
|---|---|---|---|
| 1 | SDWA_VIOLATIONS_ENFORCEMENT | **live** | On tribal land where EPA is the regulator, **13.7–19.2%** of health-based violations since 2015 are still unaddressed. The state median is **1.7%**. West Virginia is at 21.5%. |
| 2 | NID_DAMS | **live** | **753** high-hazard dams rated Poor or Unsatisfactory have the emergency-plan flag set to False. That is 27% of 2,776. Kentucky: 91 of 106. |
| 3 | SDWA_LCR_SAMPLES | **live (small)** | **19** active community water systems serving 10K+ people are over the lead action level on their latest test (2024–25). They serve 724,514 people, and **7 of the 19 are in Illinois**. |
| 4 | FRACFOCUS_REGISTRY | probed | **16.2%** of chemical rows nationally are hidden as trade secrets. Diamondback hides 30.3% in Texas, where the state rate is 16.2%, and has secrets in 96.7% of its jobs. |
| 5 | TRI_BASIC_2023 | probed | The top 1% of sites (218) put out **81.6%** of 2023's 2.98B lb on-site release. Metal mines alone put out 50.4%, and one mine, Red Dog, put out 25.9%. EPA leads with this every year. |

> **Bad news up front**
> - The triage's "370K lead" reading is **copper**, not lead. It is junk in the copper rows.
> - The FracFocus job dates are **empty on all 7.2M rows**. Without them there is no year and no drought overlay.
> - The "years since last dam inspection" angle is **dead**. It is the states' reporting lag, not dams going uninspected.

---

## 1. SDWA_VIOLATIONS_ENFORCEMENT — live

**The physical thing:** a health-based drinking-water violation that nobody has closed. There has been no formal order and no return to compliance on record, and people are still drinking from the system.

**Shape first** [8]
- 15.4M rows. One violation repeats once for every enforcement action on it, so the counts triple unless you dedupe on PWSID + VIOLATION_ID.
- 1.0M rows are enforcement-only and carry no violation ID.
- About 25.5K rows carry `ENFORCEMENT_ID` 99999… placeholders.
- The table holds one release (2026Q2), so there are no stacked snapshots.

**Checked** [16][17][20][24][31][34]
- Health-based violations only (`IS_HEALTH_BASED_IND = 'Y'`), begun 2015-01-01 to today, one row per violation.
- For each violation I counted formal, informal and resolving actions and read its status today.
- I joined the water-systems table for the regulator (primacy agency), the system type and the population served.
- Code **5200** is split out. Every 5200 row in the top list begins **2024-10-17**, the day after the federal lead-pipe inventory deadline. It looks like inventory paperwork carrying a health-based flag. That reading needs the EPA code lookup to confirm.

**Peers: who regulates** [24] (denominator = health-based violations begun 2015+, excluding 5200)

| Regulator | Health-based violations | % unaddressed today | Unaddressed | Community-system people affected |
|---|---|---|---|---|
| EPA Region 9, tribal | 1,005 | **19.2%** | 193 at 74 systems | 89,485 |
| EPA Region 6, tribal | 173 | 13.9% | 24 | 450 |
| EPA Region 10, tribal | 379 | 13.7% | 52 | 9,560 |
| West Virginia | 2,242 | **21.5%** | 482 at 184 systems | 204,494 |
| Louisiana | 7,641 | 9.3% | 710 at 231 systems | 456,263 |
| New Mexico | 5,154 | 8.9% | 461 at 157 systems | 262,668 |
| Arizona | 2,745 | 6.8% | 186 | 270,323 (median oldest open: 1,605 days) |
| **State median (48 states)** | — | **1.7%** | — | — |

**The long-open list** [31]
- **514** active community systems have a health-based violation that has been Unaddressed for 2+ years, excluding 5200. They serve **1.59M** people.
- Louisiana fills the list: mostly code 0700 treatment-technique violations with informal letters only. Examples are Tallulah (9 open) and Jonesboro (9 open).
- Pala North (090605153, EPA Region 9) has 2 open since 2019 with no action at all.

**Hit means:** the regulator, not the water, sets whether a violation gets closed. A 10x gap to the state median on tribal land is a story about EPA's own backlog.

**Miss means:** if the tribal, WV and LA rates had sat near 1.7%, the gap would be noise.

**Boring explanation, and whether I ruled it out**
- **The "no action" rate is mostly paperwork habit.** The tribal regions show 65% of violations with no action, but [34] shows most of those carry a "compliance achieved" close-out (SOX/EOX). States log a notice letter on most violations and EPA regions don't. So I led with *unaddressed today*, not "no action". Not fully ruled out: slow data entry could still inflate the unaddressed rate.
- **Portland** (0800 open since 2017-12-18) and **Jackson MS** (lead rule open since 2020) are known stories.
- The **MT0002988** 25K severity pile was not checked (budget).

---

## 2. NID_DAMS — live

**The physical thing:** a dam whose failure would probably kill people, rated in bad shape, with no written plan for warning the town below.

**Checked** [12][27][28][29][32][33][35]
- `HAZARD_POTENTIAL = 'High'` and `CONDITION_ASSESSMENT` in Poor or Unsatisfactory.
- Associated structures dropped, so each dam counts once.
- Grouped by owner type and by state, then the top owners, then the largest Unsatisfactory dams by storage.

**Numbers**
- **2,776** of **16,443** high-hazard dams are Poor or Unsatisfactory (16.9%).
- **753** of those have the emergency-plan flag set to False (27%). Among Satisfactory high-hazard rows the plan rate is about 95% (5,054 of 5,313), so plans go missing on exactly the bad dams.
- By state:

| State | Bad high-hazard dams | No plan |
|---|---|---|
| Kentucky | 106 | **91** |
| New Mexico | 145 | 94 |
| North Carolina | 246 | 120 |
| South Carolina | 162 | 65 |
| Indiana | 91 | 46 |

- **Peers by state:** New Mexico has 57.8% of its high-hazard dams in bad shape (145 of 251). Hawaii has 74.4% (87 of 117, a known post-Ka Loko story). The all-state figure is 16.9%.
- **Owners:** BIA owns **60** bad high-hazard dams across 10 states, 24 of them Unsatisfactory.
  - Grady Hamilton (NM) and Wolf Creek (SD, Pine Ridge) are Unsatisfactory, have no inspection date, no plan, and "Enforcement Pending."
  - Other top owners: NH DES (25), ODNR Parks (19), Limestone Valley SWCD in Georgia (19), NY Canal Corp (19), Caballo SWCD in New Mexico (17).
- **Biggest Unsatisfactory dams:**
  - Livingston (TX, Trinity River Authority, 3.2M acre-ft)
  - Mossyrock (WA, City of Tacoma, 606 ft)
  - Both are "Under Remediation," with plans and yearly inspections.

**Hit means:** 753 dams could fail and kill people with no written warning plan, and they cluster in a few states. That is nameable and checkable against the state dam-safety offices.

**Miss means:** if the False flags turn out to be "not reported," the count shrinks to a list of states that don't report.

**Boring explanation**
- **AP did the poor-dam count in 2019** (1,688 then). The methods differ, so I make no trend claim.
- **The inspection-staleness angle is killed** [32]. In Georgia, Indiana and Pennsylvania, good and bad dams show the same median years since inspection (9.6 vs 9.7, 7.2 vs 7.9, 5.9 vs 5.9). The three states' NID records are a median of about 1,950 days old, so this is reporting lag.
- **The plan flag has no NULLs** [35]. "Not reported" may be folded into False, and I have not ruled that out. That is the first check for a deeper pass.
- **Federal dams are 78.4% unrated**, so every federal count is a floor.

---

## 3. SDWA_LCR_SAMPLES — live, smallest of the three

**The physical thing:** the 90th-percentile lead reading from a town's kitchen-tap samples, in a sampling period, over 15 parts per billion.

**Shape first** [7][15][18]
- 927,415 rows: 888,760 lead (PB90) and 38,655 copper (CU90). One release.
- **The 370,000 max is copper, not lead**, at KS2013505. The 144 copper rows over 1,000 are whole-number junk.
- The lead max, 30,037 at PA4110043, is one bad row.
- Lead rows between 1 and 15 "mg/L" (2,314 of them) are ppb typed into a mg/L column, mostly Ohio and before 2015. Since 2015 no state has more than 0.7% of its rows above 1.
- So I kept lead readings over 0.015 and up to 1 mg/L, one per system per period, for periods ending 2015-01-01 to today.

**Checked** [13][14][30]: periods over the action level per system, joined to the water-systems table for name, type and population.

**Numbers**
- **497** systems went over in 3+ periods since 2015. They serve 4.25M people, and 260 of them are active community systems.
  - The top of that list is known ground: Boston-area MWRA towns, Portland OR, Pittsburgh, Providence, Newark (6 of 17 periods), Trenton, Jackson MS and Benton Harbor.
  - Most of them test under 15 ppb now.
- **Still over now** (latest period ends 2024+, active community systems of 10K+): **19 systems, 724,514 people.**
  - **Seven are Illinois:** Aurora (183K people, 24 ppb), **Elgin** (115K, 53 ppb, over in 7 of 13 periods), Bartlett, Morton Grove, Lockport, Lake Forest and Lemont.
  - Others: Kingman AZ (60 ppb), Hibbing MN (32 ppb), Aliquippa PA (33.5 ppb), Smithfield UT (46 ppb).
- **Peers by size** (active systems with a lead period ending since 2015; share ever over):

| System type | Size | Share ever over |
|---|---|---|
| Community | ≤500 people | 8.6% (2,031 of 23,606) |
| Community | 10K–100K | 3.6% |
| Community | >100K | 4.6% (22 of 479) |
| Non-community (schools, plants) | small | **12.5–12.7%**, the highest rate |

**Hit means:** a named town over the lead action level on its latest test, with a cluster in one state's suburbs, is a current story, not a Flint rerun.

**Miss means:** without the Illinois cluster this is a history list of cities already covered.

**Boring explanation**
- The persistent list is the known cities. That is not ruled out; it *is* the explanation for that list.
- **Illinois may have changed how it samples** (for example, a new rule for which liter gets tested) and not how much lead is in the water. Unchecked.
- For a tiny system, the 90th percentile of 5 samples is basically the worst tap.
- Big systems test every 6 months and small ones every 3 years, so "periods over" can't be compared across sizes.

---

## 4. FRACFOCUS_REGISTRY — probed

**The physical thing:** a frack job's chemical list where the ID number is replaced by the word PROPRIETARY.

**Shape** [10][11][26]
- 7.2M rows, 248,835 disclosures, 236,632 wells.
- **JOB_START_DATE and JOB_END_DATE are empty on every row.** There are no years, so no drought overlay and no way to line anything up in time.
- 12,203 disclosures are repeat filings on a well that was already disclosed.

**Checked** [25]
- One row per disclosure first.
- Secret share = rows marked PROPRIETARY, CONFIDENTIAL, TRADE SECRET, CONFIDENTIAL BUSINES or CBI, divided by rows with a non-blank chemical-ID (CAS) field.
- Each operator is compared against its own state's share.

**Numbers**
- Nationally **16.2%** of chemical rows are withheld.
- Operators well above their own state:

| Operator | State | Operator's share | State's share | Note |
|---|---|---|---|---|
| **Diamondback** | Texas | **30.3%** | 16.2% | Secrets in 96.7% of 3,164 jobs; 64.45B gal of water |
| **QEP Energy** | Wyoming | 28.3% | 14.1% | |
| **Chesapeake** | Texas | 28.8% | 16.2% | |
| Chesapeake | Oklahoma | 24.3% | 14.3% | |
| Chesapeake | Ohio | 26.5% | 16.9% | |
| Cimarex | Texas | 26.3% | 16.2% | |
| Cimarex | New Mexico | 27.8% | 18.0% | |

- **Water**, deduped: 2,226B gallons across all jobs, a median of 7.67M gallons per job, and 28 jobs over 100M gallons (suspect). Pioneer in Texas: 98.4B gallons over 7,357 jobs.

**Hit means:** a driller hiding twice its state's rate is a named outlier worth asking about.

**Miss means:** everyone near 16% would mean secrecy is simply the industry norm.

**Boring explanation**
- Trade-secret claims are legal and industry-wide. Advocacy reports have covered this.
- The facts line's TVD numbers are dead. Well depth repeats on every row, the Clayton Williams max is **1.19 billion feet** in one disclosure, and 74 disclosures claim depths over 40,000 ft.
- The facts line's 72.5T water sum is the same repetition. On all 248,835 disclosures the water volume is identical on every row.

---

## 5. TRI_BASIC_2023 — probed

**Checked** [9][21][22][23]
- Pounds rows only. Form A rows (8,838) are zero by design, and 770 dioxin rows are in grams.
- On-site release summed per facility, then per sector.

**Numbers**
- 2.98B lb on-site across 21,859 facilities.
- **Red Dog** (Teck, Kotzebue AK) released 771M lb, **25.9%** of the national total. Its biggest single line is 399.5M lb of zinc compounds.
- Metal mining: 91 sites, **50.4%**. The top 1% of sites hold 81.6%.
- Outside the mines:
  - **Hydrogen sulfide at gas plants:** Dark Horse Treating Facility, Jal NM, 73.6M lb, no parent listed; Targa Midway 42.0M lb; Targa Sand Hills 20.3M lb.
  - **Carcinogen air releases** (8,704 sites, 60.7M lb) are topped by fiberglass boat and bathtub makers releasing styrene: Onyx Collection, Belvue KS, 751,599 lb; Yamaha Jet Boat, Vonore TN. Lyondell Channelview released 596,843 lb of 1,3-butadiene.

**Hit means:** a non-mining plant at the very top would be a named-plant story.

**Miss means:** mines on top means this is EPA's annual headline, and that is what came back.

**Boring explanation**
- Mines count moved waste rock as a release. Confirmed as the reason for the ranking.
- The hydrogen-sulfide lines may be acid gas pumped underground and counted as a release. Unchecked.
- "Near people" was not tested. That needs a census join, which was out of budget.

---

## New data traps

- **LCR mixes lead and copper in one column.** Never sum SAMPLE_MEASURE across CONTAMINANT_CODE. The 370K max is copper junk.
- **LCR lead rows with values of 1–15 are ppb in a mg/L column** (2,314 rows, mostly Ohio, mostly before 2015).
- **SDWA violations repeat once per enforcement action.** Dedupe on PWSID + VIOLATION_ID.
- **SDWA "no enforcement" mostly means only a Resolving close-out.** Every Resolved violation carries one (SOX/EOX), so "no action" measures how many notice letters got logged.
- **SDWA code 5200 inflates the health-based unaddressed counts.** It reads as lead-pipe inventory paperwork (start date 2024-10-17). Split it out.
- **FracFocus has no job dates on any of its 7.2M rows.** Water and depth repeat on every ingredient row, and depth over 40K ft appears on 74 jobs.
- **NID LAST_INSPECTION_DATE is only as fresh as the state's last upload.** GA, IN and PA records are about 5.3 years old.
- **NID HAS_EMERGENCY_ACTION_PLAN has no NULLs.** False may mean "not reported." 33 "no plan" rows carry a plan revision date.
- **NID junk dates:** inspection dates as late as 5023-05-25, plus 1901-01-01 placeholders, plus 1980-01-01 on 1,599 rows.
