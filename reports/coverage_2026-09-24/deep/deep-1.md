# Deep look 1: five EPA enforcement tables

2026-09-24 · agent deep-1 · **31 of 35 SQL statements** · Python door, read-only · SQL in `deep-1.sql`

Every person or company named here is a **data match, not verified against primary records**.

---

## The answer first

**None of the five is a big, defensible story as triaged.** Three angles die on their own data. Two leave small leads.

The most useful output is a trap for this whole family of tables:
**EPA enforcement tables copy one case's penalty onto every facility or permit in the case.**
Counting each case once:

| Table | Raw sum | Each case once | Repeats |
|---|---|---|---|
| ICIS-Air formal actions, all penalties | $5.81B | $3.86B | **$1.95B (34%)** |
| NPDES formal actions, federal penalty | $8.13B | $6.99B | $1.15B (14%) |
| NPDES formal actions, state penalty | $1.50B | $0.86B | **$0.64B (43%)** |

| Table | Verdict | One number |
|---|---|---|
| EPA_PENALTY_GAP | **dead** | Split by state, the minority gap flips: minority areas are worse in 8 states and better in 10 |
| ICIS_AIR_FORMAL_ACTIONS | probed | Oklahoma refineries: $3.3K penalty per logged violation; Texas $142K |
| ICIS_AIR_VIOLATION_HISTORY | **dead** | 38 Louisiana refinery sites logged 6 violations in 11 years; the state gaps measure reporting |
| NPDES_FORMAL_ENFORCEMENT_ACTIONS | probed | The "$6.7B BP" is two identical $3.35B entries on the same permit on the same day |
| RCRA_VIOLATIONS | probed | Only 2,247 violations at 715 handlers from 1980-2020 are still open, out of 614K+ |

---

## 1. ENVIRONMENT__EPA_PENALTY_GAP: **dead**

**Headline:** the minority-neighborhood gap goes away when each state is compared with itself. The "never fined / never inspected" flags are mostly drinking-water systems and time-window effects.

**What's in it:** 93,808 facilities, one row each.
53,437 were out of compliance in 8 or more of the last 12 quarters. 18,384 were out in all 12.

**Checked**
- Counted each flag, then checked it against the columns it claims to summarize.
- Pulled each facility's drinking-water flag from ECHO by FRS_ID (all 93,808 matched).
- Took the facilities with 8+ bad quarters and split them by program and by neighborhood minority share. Two rates:
  - share never fined, over the facilities with 8+ bad quarters in that band
  - share with no inspection date on record, same denominator
- Compared each state with itself: facilities in 50%+ minority areas against facilities in areas under 25% minority.

**What the flags really are**
- **41% of rows are drinking-water systems.** 38,522 rows have no air, water or hazardous-waste flag, and all 38,522 are drinking-water systems in ECHO. They are 21,634 of the 53,437 long violators, and 19,994 of the "no fine, no inspection" rows.
- **`CHRONIC_NO_PENALTY` does not mean never fined.** True on 49,622 rows. 5,322 of them have a past penalty in `LAST_PENALTY_AMT`. Example: North & Judd, CT, $100K in 1994, still flagged.
- **`NEVER_INSPECTED_NONCOMPLIANT` does not mean never inspected.** True on 53,587 rows. 12,282 of them have a `DATE_LAST_INSPECTION`. `TOTAL_INSPECTION_COUNT` only covers about the last 5 years: no row has a count of 0 alongside an inspection after 2021-09-24.
- `PCT_MINORITY` is blank on 29,702 rows (32%). Most of those are the drinking-water rows.
- `LAST_PENALTY_SHARED_FACILITY_N` = 3013568 on 78,315 rows, never on a row with a penalty. It's a filler value.

**Fines by neighborhood (8+ bad quarters, share never fined)**

| Program | <10% minority | 25-50% | 75%+ minority |
|---|---|---|---|
| Air | 35.7% | 30.8% | **25.6%** |
| Hazardous waste | 73.2% | 69.7% | 78.3% |
| Water | 82.5% | 79.2% | 83.6% |

No gradient. For air it runs the other way: long violators in minority areas are *more* likely to have been fined.

**Inspections by neighborhood (share with no inspection date on record)**
- Water: 16.7% in under-10%-minority areas, 35.7% in 75%+ minority areas. Hazardous waste: 9.7% and 22.8%.
- Across the 19 states compared plus Puerto Rico (water and hazwaste, 8+ quarters): 28.3% (1,203 of 4,256) in 50%+ minority areas against 22.0% (2,085 of 9,464) in under-25% areas.
- **State by state it's a coin flip.** Minority areas are worse in 8 states (CA, GA, TX, MI, CO, MD, PA, NC by a hair) and better in 10 (NJ, LA, WA, AK, AL, IL, SC, FL, AR, NY by a hair). MS is tied.
- The national gap comes from state mix. Georgia (67% / 63%) and Colorado (62% / 55%) are high whatever the neighborhood. And "no date on record" is absence, which is weak ground anyway.

**Hit would have meant:** within the same state and program, long violators in minority areas go unfined or uninspected more often. That's a real environmental-justice story.
**Miss means:** the national gap is which states the facilities sit in. There's no neighborhood effect to report.

**Boring explanation:** state programs differ in how they inspect and record, and drinking-water systems fill the flags.
**Ruled in:** checked above.

**The named list (12 of 12 quarters out, never fined, no formal action, most-inspected first)**
Mostly small-town sewage plants and mobile-home parks:
- Hustontown STP, PA: 25 inspections
- Cathlamet WA former lagoons: 24 inspections
- City of West Tawakoni WWTP, TX: 23 inspections

Industrial names in the top 25:
- SK Battery America, Commerce GA: Significant Violation, 12 inspections
- Stella-Jones Corp, Du Bois PA: TRI on-site releases 2,955 lb
- ARI Railcar Services, Tennille GA: 67% minority area

Small towns that break sewage limits for years and don't get fined is a known pattern.

---

## 2. ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS: **probed**

**Headline:** penalties per case vary 20-40x between states. The biggest driver is what each state reports into this federal file, not how hard it fines.

**What's in it**
- 106,009 rows, 103,147 cases (`ENF_IDENTIFIER`).
- 33,400 rows (32%) carry a $0 penalty.
- Who acted: state 69,340 rows, local 20,906, EPA 15,763.

**Checked**
- Grouped by case to find penalties copied across facilities.
- Top cases, with each case's penalty counted once.
- By state, 2015-2025, one row per case per state: share of cases with a penalty, and median penalty per penalized case. Run for all sources and for major sources.
- Repeat facilities.
- Refineries only (NAICS 324110), as a peer group:
  - penalty per refinery-coded facility
  - penalty per logged violation (violations from the violation-history table)

**Numbers**
- **Repeat trap:** 395 multi-facility cases put the same penalty on every facility (1,767 rows).
  - Example: NM000A200275488 (Magnum Compressor Station, NM), $31.6M on 11 facilities = $347.7M raw.
- **$100.7M max:** EES Coke Battery LLC, MI. Case 05-2020-5003, EPA civil judicial, entered 2026-02-24, one facility, one row.
- **Second biggest:** $64.5M, Henry Charging USA well pads, ND. Case 08-2017-0088, 2024. A national settlement sitting on one facility row.
- **Major sources, median penalty per penalized case, 2015-2025:**
  - lowest: TN $3,000, NJ $4,000, AR $4,260, FL $4,500, CA $5,000
  - highest: IL $110,000, MI $75,000, OH $50,850, WV $45,000
  - The high states lean on EPA cases: OH 36.6% EPA, MI 27.2%.
- **Share of formal cases with any penalty:** CA, TX, PA, IN all 94-96%. LA 39.9%. IL 20.9%.
- **Repeat facilities are all California local-district cases.**
  - Kern Oil & Refining, Bakersfield: 532 cases 2015-2025, $9.2M total, median $8,625
  - Chevron Richmond refinery: 248 cases, $3.2M, median $3,000
  - The districts log every settled notice of violation as its own formal action.

**Refinery peers, 2015-2025, all agencies, each case once**

| State | Refinery-coded facilities | Violations logged | Formal cases | Penalty | Per facility | Per violation |
|---|---|---|---|---|---|---|
| CA | 44 | 2,216 | 1,551 | $51.4M | $1.17M | $23K |
| TX | 58 | 203 | 263 | $28.8M | $496K | **$142K** |
| PA | 13 | 135 | 34 | $2.6M | $200K | $19K |
| OK | 9 | 148 | 39 | $0.48M | **$54K** | **$3.3K** |
| LA | 38 | **6** | 85 | $3.45M | $91K | n/a |
| IL | 19 | 9 | 15 | $4.5M | $238K | n/a |

**Hit would have meant:** the same kind of plant, breaking rules at the same logged rate, pays far less in one state than another.
**Miss means:** the gaps come from what each state logs, not what it charges.

**Boring explanation, not ruled out:**
- California districts log every notice of violation.
- Louisiana logs almost no violations: 6 for 38 refinery-coded sites over 11 years.
- EPA-heavy states show bigger medians.
- "Refinery-coded" includes terminals and small units, and nothing here weights by plant size.

**Worth a deeper pass?** Oklahoma is the one clean peer number: 148 violations logged, $3.3K penalty per violation, against Texas at $142K. But that's only 9 facilities. It needs the state agency's own penalty records to settle.

---

## 3. ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY: **dead**

**Headline:** the "states let high-priority violators ride" angle measures which states report into this table.

**What's in it**
- 102,037 rows: 57,250 lower-level violations (FRV) and 44,787 high-priority violations (HPV).
- **`COMP_DETERMINATION_UID` is unique on every row.** The automated facts line says "751 repeats" and triage built a warning on it. **Both are wrong.**
- Junk dates: 134 HPV start dates before 1990, the earliest in year 0218. 474 HPVs are "resolved" before they started. One start date is 2026-09-28, after today.

**Checked**
- Took HPVs that started 2012-2021, giving each at least 4 years to be acted on.
- Joined formal actions for the same facility (`PGM_SYS_ID`), aggregated per case first.
- By state:
  - share still unresolved
  - median days to resolve
  - share with a formal action within 2 years
  - share with no formal action ever after the start date
- Listed the oldest open HPVs with no action since the start date, with the facility file's operating status.

**Numbers**
- 8,896 HPVs. 964 (10.8%) unresolved. 558 (6.3%) never drew a formal action at the facility.
- California holds 4,659 of them (52%).
- Outliers (share of that state's HPVs):
  - Ohio: 53.4% of 133 never drew a formal action
  - Wisconsin: 56.6% of 113 never drew one
  - Michigan: 64.4% of 101 unresolved, median 1,830 days to resolve
  - Colorado: 43.7% unresolved
- 173 HPVs are open with no action since their start date.
  - The oldest include plants the facility file lists as Permanently Closed (Pilkington, Lathrop CA; Precision Specialty Metals, Los Angeles).
  - Also on the list: Greka Energy Cat Canyon leases (Santa Maria CA), Phillips 66 Santa Maria refinery, Drake Cement (AZ), Clark-Floyd Landfill (IN), Mullins Cheese (WI), Motiva Port Arthur Terminal (TX).

**Hit would have meant:** specific states sit on serious air violations for years and never act.
**Miss means:** the gaps sit where formal actions or violations are simply not reported to ICIS-Air.

**Boring explanation, confirmed:**
- Ohio logged 347 formal air cases for 2015-2025. Indiana logged 1,176.
- Louisiana refineries logged 6 violations against 85 formal cases.
- An HPV with no formal action in Ohio is mostly a reporting gap. Never build on absence.

**Parked:** Michigan's 64% unresolved HPVs (101 of them) is small but unexplained.

---

## 4. ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS: **probed**

**Headline:** the famous number is doubled. Once it's set aside, the biggest water fines are one Texas recycler, a bankruptcy claim and a likely typo.

**What's in it**
- 112,373 rows, 104,520 cases, 49,662 permits.
- Federal penalty filled on 4,533 rows (4.0%). State penalty filled on 48,135 (42.8%).

**Checked**
- Grouped by case to find repeats across permits.
- Top cases with each case counted once.
- Every row on GMG290110 (the BP Gulf permit) and on TN0021547.
- By state, 2015-2026, BP case removed: share of cases with a penalty, and median penalty per penalized case.
- Permits with the most repeat formal cases.

**Numbers**
- **BP:** two cases, 04-2010-9036 (EPA Region 4) and 06-2011-4881 (EPA Region 6).
  - Both on GMG290110, both entered 2012-06-18, both exactly **$3,352,250,000**. State amounts: $15M and $10M.
  - The "$6.7B, 82% of federal dollars" in triage is these two lines.
  - It looks like one settlement logged by two regions, or one total split in halves. Not checked against the consent decree.
- **Repeat trap:** 1,943 cases span several permits.
  - The same federal amount repeats in 258 of them; the same state amount in 998.
  - Example: 04-2006-9037, Martin County Coal (KY): $6.7M on 76 permits = $509.2M raw.
- **Likely typo:** Jonesborough STP, TN, $30,000,000 state penalty in 2009. The plant's only other penalty was $600 in 2003.
- **Biggest after BP, each case once:**
  - Altair Recycling Facility, TX: **$57.0M** state civil judicial, 2025-06-06, case TX-D-1-GN-19-002002
  - ATP Oil & Gas: $39M, a 2015 bankruptcy claim
  - Jonesborough: $30M (above)
  - NYC DEP Newtown Creek: $29.0M, 2002
- **By state, 2015-2026:** 32,983 case-state rows; 61% carry a penalty.
  - North Carolina: 4,520 cases, 99.2% penalized, median **$787**
  - Oklahoma: 12.2% penalized. Illinois: 10.0%. Louisiana: 36.6%, median $2,000.
  - New Mexico (EPA runs its permits): 4.1%
- **Top 20 repeat permits are all North Carolina small plants.** Pace Mobile Home Park, Clayton NC: 80 cases, 79 penalized, $226K total, median $870. North Carolina logs each monthly limit-breach penalty as a formal action.

**Hit would have meant:** a state or permit holder that racks up formal actions while fines stay at zero, compared with peers.
**Miss means:** what counts as a "formal action" differs by state, so per-case comparisons mostly compare paperwork styles.

**Boring explanation:**
- BP is famous.
- North Carolina's per-breach penalties crowd the repeat list.
- A 10-12% penalized share (OK, IL) could be orders logged here while penalties land in separate actions.
- Not ruled out.

**Lead:** Altair Recycling Facility, TX, shows up in RCRA too (section 5). A $57M state water judgment plus hazardous-waste violations still open since 2019 is one named thread for a deeper pass. Small, one site.

---

## 5. ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS: **probed**

**Headline:** almost every hazardous-waste violation gets a fix date. The "open for years" pool is small and mostly abandoned or cleanup sites.

**What's in it:** 708,114 rows. 91% were found by states.

**Checked**
- Share with no fix date (`ACTUAL_RTC_DATE` null), by the 5-year bucket the violation was found in.
- Open violations found 1980-2020, by handler.
- Joined handler names, then **EPA's own monthly violation flag file** (`RCRA_VIOSNC_HISTORY`) as a second check on whether the site is still in trouble.
- By state, violations found 2010-2020:
  - share open
  - share with a due date
  - share fixed after the due date
  - median days late

**Numbers**
- Share still open by when found:
  - 0.0-0.4% for every bucket 1980-2014
  - 1.2% for 2015-19
  - 5.4% for 2020-24
  - 19.7% for 2025-26
- **Open violations found 1980-2020: 2,247 at 715 handlers**, out of more than 614K found in those years.
  - 222 of the 715 still carry an EPA violation or serious-noncomplier flag in 2026.
  - 184 never appear in the flag file.
- Due date (`SCHEDULED_COMPLIANCE_DATE`) is filled on about 35% of rows, mostly in WA, WI, KY and GA. Most states barely use it.
  - Fixed more than a year late: 1,166 of 140,550 violations found 2010-2020 in the 21 biggest states.
- Named open handlers (open count, when found, EPA flag):
  - Dynachem, Georgetown IL: 24, 1985-2002, last flagged 2008
  - Elpaco Coatings, St Louis MO: 23, 2011-2020
  - City Foundry, San Antonio TX: 16, from 1995, **flagged Aug 2026**
  - US Oil Recovery, Pasadena TX: 15, from 2009, flagged 2026
  - Chemetco, Hartford IL: 13, 1982-2019, flagged 2026
  - Clean Harbors of Colfax, LA: 11, 2016-2020, flagged 2026
  - Altair Recycling Facility, TX: 12, 2019, flagged 2026
  - Santolubes, Spartanburg SC: 11, 2019-2020, flagged 2026

**Hit would have meant:** live hazardous-waste handlers sitting on found violations for years, still flagged by EPA today.
**Miss means:** open violations are rare, and the old ones are closed, bankrupt or cleanup sites where no one records a fix.

**Boring explanation, partly confirmed:**
- The open pool is tiny.
- The oldest names read like abandoned or cleanup sites.
- The 2020+ open share is ordinary lag.
- Most violations are generator paperwork: 262.A (189K rows) and 262.C (113K).

**Unresolved:** the flag file holds only three flag pairs: Y/N, Y/Y and N/Y. "N/Y" (serious noncomplier but not in violation) is odd. It could mean the columns are swapped or the file uses its own meaning. Read it before relying on it.

---

## New data traps

1. **Copied penalties in EPA enforcement tables.** Count each case's penalty once, by `ENF_IDENTIFIER`, before summing.
   - ICIS-Air: $1.95B of $5.81B are repeats.
   - NPDES state penalties: $0.64B of $1.50B are repeats.
2. **The NPDES BP $6.7B is two identical $3.35B lines,** 04-2010-9036 and 06-2011-4881, same permit, same day.
3. **NPDES Jonesborough STP (TN0021547) $30M state penalty, 2009,** is a likely typo; the plant's other penalty was $600.
4. **`EPA_PENALTY_GAP` flags lie by name.**
   - `CHRONIC_NO_PENALTY` fires on 5,322 facilities with a past penalty.
   - `NEVER_INSPECTED_NONCOMPLIANT` fires on 12,282 with an inspection date.
   - 41% of rows are drinking-water systems with no program flag.
   - 3013568 is a filler value.
5. **ICIS-Air violation history `COMP_DETERMINATION_UID` is unique.** The facts.tsv "751 repeats" is wrong.
6. **ICIS-Air state coverage is uneven.** Louisiana refineries logged 6 violations for 85 formal cases; Ohio logged 347 formal cases to Indiana's 1,176. Cross-state comparisons in ICIS-Air measure reporting first.

## Parked
- Michigan: 64% of its 2012-2021 high-priority air violations are unresolved (101 HPVs).
- Altair Recycling Facility, TX: in both the NPDES and RCRA tables. The one named cross-table thread.
- Oklahoma refineries at $3.3K per logged air violation against Texas at $142K. Only 9 facilities.
