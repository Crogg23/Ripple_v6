# Deep pass 3 (round 2): five EPA tables, 2026-09-24

Agent: deep-3. Door: Python. Read-only. **20 of 35 statements used.** Two of the 20 were wasted: [1] ran another agent's scratch file after a file-name clash, and [7] failed to compile. SQL: `deep-3.sql`.
Every person, company or facility named here is a **data match, not verified against primary records**.

## The menu

| Table | Verdict | The one number |
|---|---|---|
| RCRA_EVALUATIONS | **live** | At sites where **EPA found hazardous-waste violations**, a state inspection of the same site within 2 years found violations **15.5%** of the time in Illinois (41 sites), 28.5% in NJ (87) and 34.5% in PA (78). Wisconsin: **80.8%** (55). |
| NPDES_QNCR_HISTORY | **live** | **553 permits** broke effluent limits in 36+ of 40 quarters, 2016-2025. **152 got no formal action** in that time. In WV, chronic mines got a formal action **26%** of the time (85 mines) vs **58%** for chronic sewer plants in the same state (191). |
| NPDES_SE_VIOLATIONS | probed | DeKalb County GA's Snapfinger Creek plant logged **1,394 sewer overflows** since Oct 2016, against **$52,344** in formal-action penalties since 2015. It's a known consent-decree story, and the national list is a map of which states report overflows. |
| NPDES_CS_VIOLATIONS | probed | 38,091 order milestones: **6,567 never met (17%)**, but only **1,377 are real work**. The top permit has 11. The "Tennessee leads" angle came from summing a sequence number. |
| NPDES_PS_VIOLATIONS | dead | Of 41,769 never-met permit deadlines due 2016 to mid-2025, **98.4% are paperwork**. Real construction or compliance work: 653, max 7 per permit. |

**Bad news for triage:** the CS "Tennessee permits lead" angle is fake. TN0025011's "35.9K" is a sum of `COMP_SCHEDULE_NMBR`, a schedule sequence number that runs to 999. Tennessee holds **1,081 of 82,187 CS rows (1.3%)**.

---

## 1. RCRA evaluations (hazardous-waste inspections): LIVE

**Headline:** State hazardous-waste inspectors in some states cite violations at a fraction of the rate EPA does, **at the same sites**. The spread between states is 5x.

**Checked**
- 1,166,410 rows, 307,092 sites. FOUND_VIOLATION: N 775,248 / Y 381,022 / U 10,140. I dropped U from every denominator.
- **Repeats:** 24,696 site + date + type + agency groups sit on 2-29 rows each. I deduped to one inspection per group, counted as Y if any row says Y.
- Kept only full compliance inspections (CEI, the standard walk-through), 2015-2025, by state (S) or EPA (E).
- **Denominator = deduped CEIs with Y or N.**

| | State CEIs | State % found | EPA CEIs | EPA % found |
|---|---|---|---|---|
| All handlers | 124,556 | 38.9% | 6,327 | 58.4% |
| Large generators only | 38,858 | 44.3% | 3,293 | 70.5% |

- **State vs state, large generators only:** NC 23.9% of 1,514, IL 22.3% of 768, KY 29.3% of 1,731, PA 32.3% of 2,801, CA 28.3% of 8,809. Against WI 84.8% of 768, WA 87.8% of 673, SC 78.4% of 666.
- **Does the flag lie?** Checked Y/N against the RCRA violations table: any violation logged by the same agency at the same site within 60 days.
  - 99.1% of state Y inspections have one; 1.2% of N inspections do.
  - The flag is honest. Low states really cite fewer violations.
  - Exception: **Texas.** 17.3% of TX state "N" inspections have a violation logged within 60 days. TX's real rate is about 62%, not 54.5%.
- **Same-site test** (kills most of "EPA picks the bad sites"): take each EPA CEI, 2015-2025, and pair it with state CEIs at the same site 1-730 days before or after.
  - 1,906 EPA inspections had a pair.
  - EPA found violations at 1,202. The state found violations at those same sites **49.1%** of the time.

| State | EPA found violations at | State also found violations |
|---|---|---|
| IL | 41 | **15.5%** |
| MD | 19 | 26.3% |
| NJ | 87 | 28.5% |
| PA | 78 | 34.5% |
| NC | 74 | 36.3% |
| CA | 106 | 38.2% |
| KY | 78 | 41.3% |
| (all) | 1,202 | 49.1% |
| WI | 55 | 80.8% |
| NE | 23 | 86.2% |
| WA | 13 | 88.5% |

- **Tighter window, 180 days:** 347 EPA-found sites, state also found 44.1%. NJ 18.2% of 33, MI 17.7% of 16, PA 32.9% of 19, KY 33.9% of 21. WI 91.7% of 12, SC 85.7% of 14. Same direction, thin counts.
- Example pairs where EPA found violations and the state's inspection within 180 days found none:
  - Safety-Kleen Systems: Santa Ana CA, Dolton IL, Charlotte NC, Linden NJ
  - Clean Earth: Calvert City KY, Kearny NJ
  - Calgon Carbon: Catlettsburg KY, Pittsburgh PA
  - Arkema, Calvert City KY; Nalco, Chicago; Univar, Charlotte
  - Mostly treatment/storage/disposal sites. All data match, not verified.

**Hit means:** state programs differ in what they write up. Illinois, New Jersey, Pennsylvania and North Carolina inspectors pass sites that EPA writes up. It's a story about state enforcement culture, with named sites.

**Miss means:** if the same-site gap had closed, the raw state-vs-EPA gap would be pure targeting. It didn't close.

**Boring**
- *EPA targets bad actors.* Mostly ruled out by the same-site test. Still, in the pairs, EPA's pick of site is itself a signal.
- *Things got fixed between visits.* Narrowed by the 180-day window. Not fully ruled out, since counts per state are 10-90.
- *Joint inspections logged twice* (EPA leads and writes it up, the state rides along and logs N). **Not ruled out.** Next check: pairs 1-14 days apart.
- *South Dakota's 1.8%* (775 state CEIs) looks like a recording habit; EPA's SD inspections are also low (5.3% of 19). Not a story yet.
- Skipped the "handlers never inspected" angle: that's building on absence.

**Next pass:** by state and year, is IL/NJ/PA's rate falling? Split joint vs separate pairs. Roll the examples up by company (Safety-Kleen, Clean Earth).

---

## 2. NPDES QNCR history (quarterly water-permit compliance): LIVE

**Headline:** Enforcement mostly tracks chronic violators, but 152 of the worst 553 got no formal action in ten years. And West Virginia's chronic mines get formal action at half the rate of its chronic sewer plants.

**Checked**
- 7,951,656 permit-quarters, 690,126 permits, YEARQTR 19734-20332.
- **Quarters before 1996 and after 2026 Q3 exist only when there's a violation** (100% carry one), so I used 2016 Q1-2025 Q4 only.
- The HLRNC letters don't sort clean from dirty. Only 39% of "S" quarters carry any violation count; U carries 1.4%. So I ranked on `NUME90_Q` (effluent-limit violations) > 0, which is all numeric. Confirms ledger trap R-286.
- Kept permits with 36+ of 40 quarters present (20,058). Joined formal actions (settled 2016+), informal actions (2016-2025) and facility names. I didn't measure the name land rate here; the SE table's permits land at 99.99%.
- **Peer ladder** (denominator = permits in the bucket):

| Quarters with effluent violations | Permits | Share with formal action | With neither formal nor informal |
|---|---|---|---|
| 0 | 9,461 | 7.9% | 6,220 |
| 1-9 | 4,177 | 21.4% | 1,749 |
| 10-19 | 2,661 | 42.1% | 768 |
| 20-29 | 2,192 | 57.2% | 446 |
| 30-35 | 1,014 | 68.7% | 152 |
| 36-40 | 553 | 72.5% | 69 |

- **The 553 worst** logged 177,841 effluent violations.
  - 152 have no formal action settled since 2016.
  - Only 4 of those 152 have a formal action with a blank settlement date, so a pending order doesn't explain them.
  - 84 never had a formal action at all.
  - 37 also had no informal action in ten years.
- Chronic, no formal action since 2016 (quarters with violations / total violations):

| Permit | Quarters | Violations | Enforcement record |
|---|---|---|---|
| Sugartree Surface Mine, Madison WV | 36 | 1,373 | no formal action ever; no informal 2016-25 |
| Westridge Mine, Madison WV | 37 | 744 | no formal action ever; no informal 2016-25 |
| Madison Mine, Fredericktown MO | 40 | 744 | no formal action ever; no informal 2016-25 |
| Waterfall Creek Subdivision outfalls, Ketchikan AK | 40 | 1,744 | 1 informal |
| 4 Star MHP STP, Marseilles IL | 40 | 1,047 | 2 formal ever, none since 2016; 3 informal |
| Campbell Soup Supply Co soup plant, Napoleon OH | 38 | 625 | 1 formal ever, 2 informal |
| Puerto Rico Electric Power Authority, San Juan | 40 | 465 | 3 formal ever |

- **WV, same state, same years:** chronic = 20+ of 40 quarters.
  - Mine permits: 85 of 710 chronic, **25.9%** got formal action.
  - Chronic public sewer plants: 191, **57.6%** got formal action.
  - **63 chronic WV mines** have no formal action.
- **Louisiana operators** (facility name prefix before " - "):
  - Magnolia Water Utility Operating Company LLC: 17 of 20 plants chronic (85%). But other LA municipal sewer plants run 80.7%, so it's **in line**, not an outlier.
  - **National Water Infrastructure, LLC**: 216 LA permits, 186 on general permits.
    - Share of reported quarters with an effluent violation: **28% in 2016-23 (762/2,730) jumped to 82% in 2024-25 (638/778)**.
    - Its own individual permits went 61% to 88%.
    - Its formal-action penalties look like $43.9M, but see the traps: the real total is about $0.4M.

**Hit means:** named chronic violators with no formal action, and a within-state enforcement gap (WV mines vs WV sewer plants) that a peer comparison supports.

**Miss means:** if the no-action permits had turned out to be pending orders (blank dates) or dead permits, there'd be nothing. Checked both: 4 of 152 blank-dated, and all 553 report 36+ quarters.

**Boring**
- *State orders that never reach EPA's system.* **Not ruled out.** WV reports **zero informal actions** to ICIS for any permit kind, so WV mine orders may live in a state mining system. Next check: WV DEP's own enforcement list for Sugartree and Westridge.
- *Old consent decrees* (before 2016) could cover some mines. Not checked.
- *Small villages can't afford fixes*, which explains the AK, IL and OH sewer entries. It doesn't explain mines or Campbell Soup.
- *NWI's 2024 jump* could be a new general-permit limit or new monitoring, not worse plants. Not ruled out.

---

## 3. NPDES single-event violations (spills, one-off violations): PROBED

**Headline:** The top 25 is all Georgia and Florida sewer overflows. DeKalb County is #1, a known consent-decree story. Florida's counts start in late 2018, when it began reporting.

**Checked**
- 305,445 rows, 76,438 permits. Since 2015: 230,540 rows, 229,356 distinct permit + date + code. **Duplicates are rare (0.5%),** except US MCAS Cherry Point (NCL003816): 219 rows, **6 distinct events.**
- Overflow codes (desc has SSO, CSO or overflow): 28,033 events since 2015. Top code D0017 is "violation specified in comment", a catch-all.
- Top permits since 2015, with names (land rate 61,918 of 61,919) and formal actions since 2015:

| Permit | Events | Overflows | Formal actions | Penalties |
|---|---|---|---|---|
| DeKalb Co. Snapfinger Creek, GA0024147 | 1,406 | 1,394 | 4 | $52,344 |
| City of Atlanta (3 plants), GA0039012 | 1,217 | 1,114 | 8 | $1,425,924 |
| Cobb Co. R.L. Sutton, GA0026140 | 441 | 438 | 9 | $184,565 |
| Tampa H. Curren, FL0020940 | 359 | 356 | 6 | $92,878 |

- **Who reports:** overflow events nationally went from 371 (2016) to 3,731 (2025). Only 21-36 states report any in a given year. FL went from 0-1 a year before 2018 to 1,278 in 2024; GA from 40 (2016) to 700-900 a year since 2019.
- **Within one permit:** DeKalb has run 131-176 a year since 2018, then **202 in 2025, its high**. Atlanta has fallen from 208 (2020) to 84 (2025).
- Penalty per overflow: DeKalb about **$38**, Atlanta about $1,280. That uses only formal actions in this system.

**Hit means:** DeKalb's overflows rose in 2025 while it's under a federal decree, with almost no penalty dollars here. That's a local story.

**Miss means:** national rankings are dead. The counts track reporting regimes, not spills.

**Boring:** size and reporting drive counts (confirmed). DeKalb's decree-stipulated penalties may be paid outside this table or before 2015 (not checked). The table has no gallons.

---

## 4. NPDES compliance-schedule violations (order deadlines): PROBED

**Headline:** 17% of enforcement-order milestones were never met. But it's small-town sewer plants with a handful each, much of it probably never closed out in the database. No decades-long Tennessee story.

**Checked**
- 82,187 rows, 10,589 permits. **One milestone sits on up to 4 rows** (11,787 event IDs appear 4 times), so I counted distinct `COMP_SCHEDULE_EVENT_ID`: **38,091 milestones.**
- Never met (no actual date on any row): **6,567 (17.2%)**.
  - Real work (construction or final compliance, codes CS015/016/017/022/031): 1,377.
  - "Pay required civil penalty": 442.
- Land rates: 100% of 10,589 permits in facilities and in formal actions. 7,771 are still reporting in 2025+ ("alive"); they hold 5,901 unmet, 1,163 of them work.
- Top alive permits by unmet work milestones:
  - Binghamton-Johnson City Joint STP, NY: 11, oldest due 2005
  - Wingo STP, KY: 13 unmet (6 of them work), oldest due 1989, 17 effluent-violation quarters in 2021-25
  - Cadiz WWTP, OH: 6
  - Max is 11 work milestones per permit.
- **Region 6 data entry:** LA, TX, AR and OK hold 49,826 of 82,187 rows (**61%**).
- Unpaid penalty milestones by state:
  - LA: 116 of 688 (105 still flagged unresolved)
  - Virgin Islands: 61 of 65 (93.8%)
  - MS: 50 of 103
- The unpaid rate tracks each state's overall habit of leaving milestones open (VI leaves 78.9% of everything open), so it's data entry more than unpaid fines.

**Hit means:** a live permit with a decades-old unmet construction order and current effluent violations (Wingo KY) is a small local story.

**Miss means:** there's no big "missed court deadlines for decades" pattern. The max is 11 per permit.

**Boring:** milestones never closed out in the system after the order ended. Not ruled out, and likely. CS has no dollar amounts.

---

## 5. NPDES permit-schedule violations (permit deadlines): DEAD

**Headline:** It's a table of late paperwork.

**Checked**
- 397,615 rows, 44,872 permits; **189,289 distinct milestones** (63,338 event IDs sit on 4 rows each).
- Milestones due 2016 to mid-2025 that drew a violation: 97,436. **Never met: 41,769.**
  - 41,116 paperwork: annual inspection certification 8,642; permit application 4,901; monitoring report 4,597.
  - **653 work** (keyword match on construct / final compliance / install / implement), 619 on alive permits across 433 permits.
- Top: Suncor Energy Commerce City refinery, CO: 7 unmet work milestones, oldest due Oct 2024. Then Colorado gravel pits with 4-5 each.

**Hit means:** nothing big. **Miss means:** confirmed. The "decades of missed construction" angle isn't here.

**Boring:** paperwork (confirmed, 98.4%).

---

## Traps (new unless marked)

| Table | Trap |
|---|---|
| NPDES_FORMAL_ENFORCEMENT_ACTIONS | **One case's penalty repeats on every permit it covers.** LA-SAWE180039 ($357,000, 2019) sits on 123 NWI permits, which reads as $43.9M. Sum by `ENF_IDENTIFIER` before summing dollars. |
| NPDES CS and PS violations | One milestone sits on up to 4 violation rows (CS: 11,787 event IDs, PS: 63,338). Count distinct event IDs. |
| NPDES CS violations | `COMP_SCHEDULE_NMBR` is a sequence number up to 999; the triage "TN leads" came from its sum. LA/TX/AR/OK hold 61% of rows: data-entry practice. |
| NPDES SE violations | Overflow counts map which states report. FL went from 0 before 2018 to 1,000+ a year; 21-36 states report any. US MCAS Cherry Point: 219 rows, 6 events. |
| NPDES informal actions | **WV reports zero informal actions** to ICIS, 2016-2025, for every permit kind. "No action" in WV means "no formal action on record." |
| NPDES QNCR | Confirms R-286: HLRNC "S" quarters carry a violation count only 39% of the time. Also: quarters before 1996 and after 2026 Q3 exist only when violating. |
| RCRA evaluations | 24,696 site-date-type-agency groups repeat (2 to 29 rows). Dedupe before any rate. Every 2015-2025 CEI site landed in RCRA_FACILITIES (100%). |
| RCRA evaluations | TX state "N" inspections have a same-agency violation logged within 60 days 17.3% of the time. TX's flag undercounts; everywhere else it's 0-3%. |

## Statement count
20 of 35. [1] was wasted (another agent's scratch file ran after a name clash; read-only schema listing). [7] failed to compile and was re-run as [8].
