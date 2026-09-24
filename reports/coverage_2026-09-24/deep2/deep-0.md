# Deep pass 2-0: car defect probes, offshore officers, offshore links, revoked charities, PBGC plans

2026-09-24. Python door, tag `coverage-r2-2026-09-24`. **30 of 35 statements**, all logged in `deep-0.sql` (S01-S30). Each of the 9 connections also ran the two required `ALTER SESSION` lines. Those aren't counted.
Every person, company or group named here is a data match. None is checked against primary records.

## The menu

| Table | Verdict | The one number | Headline |
|---|---|---|---|
| ECONOMICS__FED_IRS_AUTO_REVOCATIONS | **live** | 64 nonprofits spent $940M in federal money in years after the IRS pulled their exemption. They're not reinstated and not in today's master file. 27 of them are elderly or disabled housing ($435M) | Revoked HUD elderly-housing owners kept filing federal single audits. 5 still hold active HUD Section 202 rent contracts |
| CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS | **live** | Nissan false-emergency-braking probe PE19010 has been open 2,572 days. The median probe closes in 234. There were 75 complaints before it opened and 273 after | Two defect probes have sat open 7-8 years with no recall while complaints kept coming |
| CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS | probed | 61 of 22,112 US person names match an SEC insider with the city agreeing (0.28%) | The join works, but it mostly finds US executives on the boards of their own companies' Malta subsidiaries |
| CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS | dead | officer_of: 1,720,357 rows, only 1,291,429 distinct links (25% repeats) | It's a good join table (it holds the addresses) but has no story of its own. The top US intermediaries are ICIJ's own 2013/2016 reporting |
| ECONOMICS__FED_PBGC_TRUSTEED_PENSION_PLANS | **dead** | 13 of 20,835 EINs are in the real trusteed list. The top plan is GM hourly with 322,604 people, still running | ⚠ **Mislabeled.** These are ongoing PBGC-insured plans, not failed ones. The "dumped pensions" angle can't run here |

---

## 1. IRS auto-revocations: **live**

**Checked**
- 1,207,295 rows, 1,187,976 EINs. Every EIN is 9 digits, with no zero fillers. Revocations run 2010-05-15 to 2026-05-15. 180,455 rows carry a reinstatement date. 795,096 rows were 501(c)(3).
- **Join 1: FAC single audits, EIN to EIN.** I kept audit years whose fiscal year *starts* on or after the revocation date, with no reinstatement before that fiscal year *ends*.
  - All auditees: 421 EINs, 2,042 reports, $48.9B. Most of it is governments: state 20 EINs $23.9B, local 210 EINs $17.0B. Governments don't need an exemption.
  - Non-profit auditees: 207 of 37,503 EINs (0.55%), 824 reports, $3.40B. The name agrees (Jaro-Winkler 85+) on 156.
- **Second-field check against the current IRS master file (EO BMF):** 116 of the 207 are in it today, so they were reinstated or re-recognized. 59 of them have a ruling month after the revocation.
- **Clean set:** the name agrees and the EIN is in neither the master file nor the Puerto Rico file. **64 EINs, $939.8M.**
  - Sorted by name, by eye:
    - Housing: 27 EINs, $434.8M
    - Government or public bodies: 14, $304.3M
    - Puerto Rico: 8, $117.6M
    - Charter or tribal schools: 9, $55.0M
    - Credit unions: 2, $3.4M
    - Other: 4, $24.8M
  - The housing names carry HUD project numbers like `012-EE-314`, `053-EE-163`, `176-EE038` and `053-HH053`. EE is Section 202 elderly and HH is Section 811 disabled.
- **Join 2: HUD Section 8 contracts, by name only.** 6 of 27 housing names land on a distinctive name (22%):
  - Camellia Manor (GA): PRAC/202, active, 32 units
  - Jaycee Estates (OH): 202/8 NC, active, two contracts of about 50 units each
  - Hoover Seniors (CA): PRAC/202, active, 37 units
  - Hillside Gulfport Manor: PRAC/202, active, 28 units
  - Tupqich Elder Apartments (AK): PRAC/202, active, 4 units
  - Winchester Senior Housing (NV): PRAC/202, expired 2025-07
  - Generic names like "Independent Living" and "Sunflower" also hit. I threw them out as noise.
- Biggest single-year federal spend in the clean housing set: Bishop Richard B Martin HDFC (NY), 7 years in the window, $91.9M summed. Hoover Seniors: max year $5.36M. Jaycee Estates: max year $3.75M.
- **Join 3: PPP loans of $150K and up, by name plus ZIP5.** Loans flagged nonprofit:
  - 415 matched
  - 103 approved after revocation with no reinstatement
  - 96 of those with the city agreeing
  - 25 left after dropping master-file EINs and same-name successor orgs
  - Those 25 loans total $31.2M approved and $28.4M forgiven, out of 56,850 nonprofit loans in the table (0.04%). Small.

**Hit means:** HUD elderly-housing money kept flowing to owner nonprofits that lost federal tax exemption years ago. 5 of them still show active HUD rent contracts.

**Miss means:** if HUD's 202/811 rules don't require IRS exemption, or the IRS quietly reinstated them, this is paperwork, not a story.

**Boring:**
- The revocation file misses reinstatements (trap below). The master-file check handles most of this, but not all: a group that was reinstated and later dissolved drops out of both files.
- ⚠ **FAC "federal expended" for HUD 202 includes the loan balance every year.** The capital advance recurs, so summing across years double-counts. Use the max single year, not the $435M.
- Governments, Puerto Rico co-ops and credit unions are not a story. They're dropped from the headline.
- Group-exemption subordinates can look revoked. Not ruled out.
- **Not checked:** the HUD rule itself (does Section 202/811 require 501(c)(3)/(4) status?). That is the hinge.

**Traps**
- ⚠ **A blank REINSTATEMENT_DATE does not mean still revoked.** 29,792 of the 1,011,649 EINs with no reinstatement date are in today's IRS exempt master file. 21,110 of those carry a ruling month after the revocation. Check the master file before calling anything "still revoked."
- The single-audit "non-profit" type includes government bodies: Hawaii Health Systems Corp, Des Moines schools, UNC Hospitals, a housing authority.

---

## 2. NHTSA defect investigations: **live**

**Checked**
- 154,380 rows, but only 5,348 probes. One row is one probe × make/model/year × recall number: Kia PE19004 repeats once per recall. MODEL_YEAR is a float (2012.0).
- Scope: preliminary evaluations (PE) and engineering analyses (EA) opened 2010 or later. That's 530 probes: 485 closed, 45 open.
  - Closed with a recall: 259 of 485 (53.4%).
  - Median open-to-close: 234 days. For probes that closed with no recall, 303.
- **Per maker, the triage angle.** Tesla's raw share was 4 of 15 (27%). But 5 of its "closed, no recall" probes were PEs upgraded to EAs.
  - I folded in upgrades: a PE that closed within 30 days of an EA opening at the same maker. 91 of 485 were upgrades.
  - Overall: 238 of 394 = 60.4%.
  - Hyundai 80% (12/15), BMW 75% (6/8), Honda 71% (15/21), GM 63% (15/24), Ford 59% (27/46), VW 56% (5/9), Chrysler 49% (20/41), Nissan 48% (11/23), Daimler Trucks 47% (8/17), Kia 42% (5/12), Tesla 40% (4/10).
  - Counts this small can't carry a maker ranking. **Not a story.**
- **Long-open probes.** PE/EA opened 2010 or later, still open, 2+ years old:
  - EA15001 Takata: 4,230 days
  - EA16003 ARC inflators: 3,703 days
  - **EA18003 VW air-bag clockspring: 3,081 days, no recall**
  - **PE19010 Nissan false automatic emergency braking: 2,572 days, no recall**
  - PE21012 Ferrari fuel leak: 1,956 days
  - EA21002 desiccated inflators, 23 makers: 1,833 days
  - EA23001 BMW fuel pump: 1,287 days
- **Join to complaints.** Same make/model/year, with the complaint component containing the probe's top-level component. Received 2005 on.

  | Probe | Complaints before open | After open | Injury complaints after | Last complaint |
  |---|---|---|---|---|
  | PE19010 Nissan false AEB | 75 | 273 | 9 | 2026-07-14 |
  | EA18003 VW clockspring | 1,413 | 714 | 34 (plus 2 with deaths) | 2026-06-11 |
  | EA24002 Honda false AEB | 1,264 | 695 | 24 | 2026-07-21 |

- **Peers:** the other open false-braking probes are Honda EA24002 (892 days), VW EA24004 (645), Honda EA25002 (615) and Daimler Trucks EA25006 (336). Nissan's is the oldest by 4.6 years. It sits at 11x the 234-day median.
- **Is the open flag real?** 34 probes from the 1990s and 5 from the 2000s show open with no close date, which is an artifact. For the 2010s, 5 of 525 are open, and every one of the other 520 has a close date. So the flag looks kept up for recent probes.

**Hit means:** a preliminary evaluation, the short first step, has sat for 7 years on phantom braking. 273 matching complaints came in after it opened, against 75 before. The windows differ in length. "Before" runs from when those 3 model-years went on sale to September 2019. "After" is 7 years. So compare the counts, not rates.

**Miss means:** if nhtsa.gov shows PE19010 or EA18003 closed, the flat file is stale and there's nothing.

**Boring:**
- The file could be stale on these two. **Not ruled out.** Check nhtsa.gov first.
- Takata and ARC are known megaprobes that are kept open on purpose. They're left out of the headline.
- Complaints can rise *because* a probe gets press. Not ruled out.
- The component match is loose for air bags, and tight for FORWARD COLLISION AVOIDANCE.

**Traps**
- Rows are exploded by make/model/year and recall. Always dedupe to NHTSA_ACTION_NUMBER.
- ⚠ A PE that was upgraded to an EA reads as "closed, no recall." That's 91 of 485 closed probes since 2010.
- 39 probes from before 2010 are flagged open with no close date. 108 probes have no open date, and 107 of them show open.

---

## 3. ICIJ Offshore Leaks officers: probed

**Checked**
- 771,315 rows, one per node, 538,100 names. 86,403 rows are bearer placeholders (THE BEARER, EL PORTADOR). 31,666 rows are tagged USA.
- I dropped company-looking names (INC, LLC, TRUST, FUND and the like). That leaves 23,972 US person nodes and 22,112 name keys, built as last name + first name.
- The same key on the SEC side: SEC insider reporting owners, 1.9M rows, 119,889 person keys. SEC writes names last name first.
- **Funnel:**
  - 828 keys match (3.7%).
  - 546 map to exactly one SEC CIK.
  - Middle initial: 105 agree, 197 conflict (different people), 257 have one side blank.
  - **Second field:** for 83 keys, the SEC owner's city appears in the ICIJ registered address.
  - **Strong** (one CIK, no initial conflict, city agrees): **61 keys, 0.28% of US person keys.**
- **Who they are:** mostly the Paradise Papers Malta corporate registry. They are US executives on the boards of their own companies' Malta subsidiaries: Principal Financial staff, Charles Ergen of DISH/EchoStar, Kellogg's chief legal officer, Devon's COO, a Yum China director.
- Top by entity count: William Vrattos (20 entities) and Matthew Bonanno (18). They share one New York office address, and both are 10% owners of NextDecade.
- Also in the list: Howard Lutnick (shareholder of 1 Malta entity) and Arthur Laffer (director of 1). One entity each. Data matches.

**Hit means:** a US-listed insider has a documented offshore role. That's a lead for disclosure checks, person by person.

**Miss means:** zero strong matches would mean the join is broken. It isn't broken. It just finds ordinary corporate plumbing.

**Boring:** Malta's registry is a public company register, and sitting on a subsidiary's board is normal. ICIJ already searched and published US names. Being in the leaks is not wrongdoing. Not ruled out for any single name.

**Traps**
- 197 of 546 single-CIK name matches have *conflicting* middle initials. A last-plus-first name match is not a person match.
- "THE BEARER" and its variants: 86,403 rows are anonymous shares, not people.

---

## 4. ICIJ Offshore Leaks relationships: dead (join partner only)

**Checked**
- 3,339,267 rows but 2,901,722 distinct links (13% repeats).
- officer_of: 1,720,357 rows, 1,291,429 distinct (25% repeats). START_DATE runs 0003-06-24 to 5015-08-28.
- It's the only path from an officer to an address. 23,550 of the 23,972 US person nodes have one, and that's what made the SEC city check above possible.
- US-address intermediaries by distinct entities: Michael B. Edge 448 (Panama Papers), Westglobe Corporate Services 397, Corporate Solutions Inc. 392, Juris Magister 385, Corporate Creations International 375, American Corporate Services 310.

**Hit means:** a US intermediary nobody has written about would be one. **Miss means:** the top of the list is ICIJ's own 2013 and 2016 reporting, which is what came back.

**Boring:** already published. Ruled in, not out.

**Traps:** the same link repeats across leaks, so count `DISTINCT node_id_start, node_id_end, rel_type`. Dates like year 0003 and 5015 are junk.

---

## 5. PBGC "trusteed" pension plans: **dead** (mislabeled)

**Checked**
- 21,596 plans, 20,835 EINs, 17.6M participants, median 11. Effective dates run 1903 to 2026.
- Top by participants:
  - GM hourly: 322,604
  - AT&T: 274,710
  - RTX: 260,058
  - UPS: 246,785
  - FedEx: 213,710
  - Also near the top: Kaiser, JPMorgan, Bank of America, Wells Fargo, IBM.
  - **These plans are all still running.** The fact line's "top EIN 391K" is UPS's two plans combined.
- 11,039 (51%) are cash balance plans. 12,644 (59%) took effect in 2015 or later.
- **Against the real trusteed table** (`LABOR__FED_PBGC_TRUSTEED_PLANS`, 5,176 failed plans), with EINs padded to 9 digits: only **13 of 20,835 EINs** overlap.
  - Delta: the pilots' plan was dumped in 2006, and Delta still runs 5 insured plans with 145,914 people.
  - Avaya: the salaried plan was dumped in 2017, and a 5,638-person plan is still insured.
  - Four plans (Cardone, Dalton, FRAM and Southeast Alabama Community Action) sit in both lists with the same plan name and the same participant count. They're plans taken over in 2024 or 2026 that are still on the insured list.
- **Redirect:** I ran the angle on the real table joined to Form 5500 ("are the sponsors still around?").
  - The Form 5500 mart is 33,484 filings. PLAN_YEAR_BEGIN_DATE and FORM_YEAR came back empty.
  - 17 of 5,176 trusteed plans have a sponsor that still files: True Value, Times Publishing, Mohawk Fine Papers.
  - The slice is too thin to say any sponsor *isn't* around. Never build on absence.

**Hit means:** a known plan dumper that still sponsors insured plans. That's just Delta and Avaya, and both are known.

**Miss means:** this table can't tell you who dumped anything. It's a list of ongoing insured plans.

**Boring:** the famous dumps (Bethlehem 92,174, LTV 63,757, Sears 52,849 + 29,538, Pan Am, Delphi, United, US Airways) are all in the *other* table, and all well covered.

**Traps**
- ⚠ **The table name and the catalog summary say "trusteed." The contents are ongoing insured plans.** Use `LABOR__FED_PBGC_TRUSTEED_PLANS` for failed plans.
- ⚠ **Form 5500 mart:** SPONSOR_DFE_EIN is 100% empty, like EIN (the trap file names only EIN). SPONS_DFE_EIN is the filled one, on 33,484 of 33,484 rows. PLAN_YEAR_BEGIN_DATE and FORM_YEAR are empty.

---

## Process note
- At the start I wrote my query runner to the shared scratchpad as `run.py`, which overwrote another agent's file of the same name. They rewrote it within seconds, and I moved mine to its own folder. It didn't touch the warehouse or the repo. If a deep2 agent's SQL log is missing statements from about 14:49, this is why.

parked: `REVOKED_BUT_DEDUCTIBLE` (22,512 "revoked yet deductible" leads) looks built on the blank-reinstatement trap above. Many of those groups are probably just reinstated. Unchecked.
