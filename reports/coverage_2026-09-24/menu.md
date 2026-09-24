# Coverage menu, 2026-09-24

Chris asked for coverage first: a menu of what could be found, so a found lead is not chased if it is trivial next to the rest.

## What ran

| Step | What | Result | Cost |
|---|---|---|---|
| Battery A | one scripted read-only pass over all 549 untouched single tables: row count, lead number, top-1% share, top actors, date span | 549 fact lines, 61 data traps, 0 failures | 1,452 SELECTs, ~0.1 credit |
| Triage | 24 agents scored every table 0-10 from its facts, reporter lens + data lens | 549 scored; cut line 6.0 for the top 50 | no warehouse |
| Deep | 10 agents, 5 tables each, up to 35 queries | 10 live, 36 probed, 4 dead | 305 SELECTs |
| Skeptic | fresh agent per live row, tried to refute | 10 of 10 narrowed, 0 confirmed as written, 0 broken | 75 SELECTs |
| Judge | ranked the new leads against the 37 existing findings | 47-row menu below | no warehouse |

Whole pass: about 0.3 credits on the X-Small warehouse, upper bound from execution seconds. Every statement was a SELECT; three failed on syntax.

**Scope:** single tables only. Joins (pairs 2.7% worked, hops 2.0%) were not in this pass.

## The judge's verdict

No lead from the coverage pass beats the best existing ones. All 10 new leads came back narrowed, several hard, and none tops the $593M alginate pair (F-032), the $96.8M skin-substitute surgeon (F-033) or the pill-to-death chart (F-002). The bottom of the old ledger is trivial next to the new finds: the null results (F-009, F-011 to F-018 and F-023) rank below every new lead and should come off the menu, while the 527 charity groups, the barred home-health owners and the CFHC hospices move into the upper-middle of the list.

## The menu

Scores 1-5. size = money, harm, people touched. novelty 1 = famous story. defensible = survives a hostile data editor. days = solo analyst to publish.

| # | from | lead | the number | size | novelty | defensible | days |
|---|---|---|---|---|---|---|---|
| 1 | F-032 | Two suppliers own a Medicare code (alginate dressings) | Two suppliers took $593M of the $649M Medicare paid for alginate dressings in 2024. That's 91%, at 8-11x a normal supplier per patient. | 5 | 4 | 4 | 7 |
| 2 | F-033 | Bakersfield surgeon's skin-substitute billing | $96.8M allowed for 28-35 patients in 2024: about $3M a patient. | 5 | 3 | 4 | 7 |
| 3 | NEW | Police, fire, veteran and cancer 527s that pay telemarketers, not candidates | $195M raised in police, fire, veteran and cancer names since 2014. About three-quarters went to fundraisers and $0.36M to anything called a contribution. | 4 | 3 | 4 | 10 |
| 4 | NEW | SpaceX, Ford, Bath Iron Works injuries, third year running | SpaceX ran 3.2x its industry's injury rate in 2025, the third year in a row. Ford ran about 1.9x GM, Toyota, Honda and Tesla head to head. | 4 | 3 | 4 | 4 |
| 5 | F-027 | ICE detainers: fewer have a conviction | The share of detainers on people with a criminal conviction fell from 43% to 16%, same months, FY23 to FY26. | 5 | 3 | 3 | 6 |
| 6 | F-002 | Pill counties became death counties | The counties with the most opioid pills in 2006-12 had 2.7x the overdose deaths in 2019-24. | 5 | 2 | 4 | 3 |
| 7 | F-001 | Judge Gilstrap's stock vs his docket | 183 cases naming Apple, Microsoft, AT&T or Walmart while he held their stock. | 4 | 3 | 3 | 12 |
| 8 | NEW | Barred people still listed as home health owners | 3 people on the federal ban list are listed as owners of 6 home health agencies, mostly in LA. One was barred in Jan 2026 and is still listed. | 3 | 4 | 3 | 10 |
| 9 | NEW | CFHC numbered hospices in San Antonio | 12 San Antonio hospices named CFHC NO4 to NO22. 8 were incorporated the same day, 6 share one building, and they trade under about 10 brand names. | 3 | 4 | 3 | 10 |
| 10 | F-025 | ICE bond by state | Settled immigrants (arrested 2+ years after entry) got bond 7% of the time in Louisiana, against 29% in Pennsylvania. | 4 | 3 | 3 | 7 |
| 11 | F-030 | Rail trespasser deaths | Trespasser deaths rose 26% to 838 from 2017 to 2025 while other rail casualties fell. All 41 Brightline deaths in 2024 were trespassers. | 4 | 2 | 4 | 3 |
| 12 | F-036 | Ford plants' injury rate (2023-24) | Ford's truck plants ran 10.6 injuries per 100 workers, against about 5.5 at peers. | 4 | 3 | 3 | 4 |
| 13 | F-003 | Hospital officer pay vs charity care | 27% of 919 nonprofit hospitals paid one officer more than their whole charity-care cost in 2022. | 4 | 2 | 3 | 5 |
| 14 | NEW | Poor high-hazard dams with no emergency plan | 634 high-hazard dams rated Poor or Unsatisfactory flatly say 'No' emergency plan. That's about 300 more than their own states' good dams would predict. | 4 | 2 | 3 | 6 |
| 15 | F-029 | Illinois nursing-home abuse flags | Illinois flags 30% of its nursing homes for abuse, 3x the 9% rate everywhere else. | 4 | 3 | 2 | 8 |
| 16 | F-019 | Pharma money and brand-name prescribing, 2024 | Doctors paid $10K+ cost 1.2-5.6x more per claim, and brand share rises with payments in all 7 specialties. | 4 | 2 | 3 | 5 |
| 17 | NEW | Lower Brule Sioux Tribe: 10 straight years of audit flags | Lower Brule is the only 1 of 67,777 auditees flagged for going-concern doubt and material noncompliance in all 10 years, 2016-2025. | 2 | 3 | 4 | 10 |
| 18 | NEW | Nursing-home dialysis operators flagged on survival | Dialyze Direct and Concerto: 18 of 26 rated clinics flagged Worse on survival. But nursing-home patients run only about 9% worse than at similar nursing-home-heavy units. | 3 | 4 | 2 | 14 |
| 19 | F-034 | San Antonio NP's specialty-drug prescribing | $24.9M of specialty Part D drugs in 2022, the most of any NP, then $1.37M in 2024. | 3 | 4 | 2 | 8 |
| 20 | F-021 | For-profit vs nonprofit nursing homes | For-profits staff 3.70 hours per resident against 4.40 at nonprofits, and pay $320 vs $205 a bed in fines. | 4 | 1 | 4 | 4 |
| 21 | F-035 | SpaceX injuries (2023-24) | 2.8x the injury rate of other space-vehicle makers, with $5.8B in federal contracts. | 3 | 2 | 4 | 3 |
| 22 | F-022 | Newington CT SBIR firms | Five small firms at one address won $13.35M in 41 research awards. The Air Force barred all five in July 2026. | 2 | 2 | 4 | 4 |
| 23 | NEW | Unfixed water-system inspection defects | Pre-2022 unfixed inspection defects are still open at 19% in West Virginia, 11% on EPA-run tribal land in Region 9 and 9% in Louisiana. Other states: 3%. | 3 | 3 | 2 | 12 |
| 24 | F-010 | Coal controllers' serious violations | Eight coal controllers logged 900-1,960 serious violations per 1,000 miners, 2018-24. | 3 | 3 | 2 | 7 |
| 25 | F-020 | Banned providers paid by drug companies | 193 providers on the federal ban list took about $166K from drug companies in 2024. | 2 | 3 | 3 | 5 |
| 26 | F-024 | Barred Amerihost's HUD Section 8 money | $1.54M of HUD Section 8 in 27 payments during a 2021-26 government-wide ban. | 2 | 4 | 2 | 8 |
| 27 | NEW | California family therapists opting out of Medicare | CA family therapists opted out of Medicare at 37%, 3.5x CA social workers. CA holds 70% of US family-therapist opt-outs. | 2 | 3 | 3 | 4 |
| 28 | F-026 | loanDepot refinance denials | loanDepot denied 74% of refinance applications in 2015-17, but 8% of home-purchase ones. | 2 | 3 | 3 | 5 |
| 29 | F-037 | Shipyard injuries (GD, HII, Bath) | Bath Iron Works: 10-13 injuries per 100 workers, while the other big yards run 1.1-1.4x their peers. | 2 | 3 | 3 | 4 |
| 30 | F-007 | HMDA 2017 Black denial gap | Black applicants were denied at about 2x the White rate at every big 2017 purchase lender. | 4 | 1 | 3 | 3 |
| 31 | F-031 | NYC 2025 race money | Fix the City took $35.6M from 381 gifts. Mamdani raised $4.03M from 54,103. | 3 | 1 | 4 | 2 |
| 32 | NEW | Big water systems over the lead line | About 17 systems with 10K+ people are over the lead action level on their newest test. The Illinois cluster came from a 2025 testing change. Elgin has been over since 2021 and now reads 53 ppb. | 3 | 2 | 2 | 6 |
| 33 | F-028 | One man behind 630 UK companies | An Egyptian national born 2001 controls 630 live UK companies, none filing accounts. | 2 | 3 | 2 | 8 |
| 34 | F-004 | Novo money and Ozempic prescribing | Doctors paid only by Novo wrote 54% Ozempic, against 41% for unpaid doctors. | 3 | 2 | 2 | 5 |
| 35 | F-006 | SEC insiders as FEC donors | 5,362 corporate insiders matched to $555M of FEC giving. | 3 | 2 | 2 | 8 |
| 36 | F-008 | Co-authors of retracted papers kept NIH money | 76 co-authors of papers retracted for misconduct (ORI cases) got $187M of NIH money after the retraction. | 3 | 3 | 1 | 10 |
| 37 | F-005 | Excluded firms still getting orders | 23 firms under a government-wide ban got $800K of orders after the ban, mostly from DoD. | 1 | 3 | 3 | 6 |
| 38 | F-013 | ECHO penalty double counting | UPS reads $503M in EPA penalties because shared-case penalties repeat on every facility. | 1 | 2 | 3 | 3 |
| 39 | F-011 | FDIC orders vs deposits | Banks under FDIC orders grew deposits 51.7%, against 49.1% for the rest. | 1 | 2 | 3 | 3 |
| 40 | F-009 | Banking Committee senators' bank trades | 19% of trading senators made 34% of bank-stock trades. | 2 | 2 | 1 | 5 |
| 41 | F-023 | ATI Government Solutions after suspension | $6.8M after an SBA suspension, but it's modifications to old contracts plus a $4.6M termination settlement. | 1 | 2 | 2 | 5 |
| 42 | F-018 | ICE deaths by facility type | 37 deaths in 2022-26: too few to rank facilities. | 2 | 2 | 1 | 7 |
| 43 | F-017 | Lobbying clients vs contract winners | 995 names match, 2019-24. No angle yet. | 1 | 2 | 2 | 10 |
| 44 | F-015 | PPP loans vs SAM exclusions | Only EPA facility listings match. | 1 | 1 | 2 | 5 |
| 45 | F-012 | CFPB complaints vs FDIC-ordered banks | 2 of 30 match by name. | 1 | 1 | 1 | 10 |
| 46 | F-014 | Greenhouse-gas emitters vs ECHO | CO2e is null on about 30% of 2023 rows. | 1 | 1 | 1 | 5 |
| 47 | F-016 | MSHA controllers in FEC employer text | 1 hit. | 1 | 1 | 1 | 10 |

## The 10 new leads, before and after the skeptic

Every name is a data match, not verified against primary records.

### NARROWED

**After skeptic:** 2,776 of 16,443 high-hazard dams are rated Poor or Unsatisfactory. On 634 of them the plan field says a flat "No", and on 119 more it says "Not Required". Measured against good dams in the same state, you'd expect about 453 without a plan, so the real extra is about 300. Most of it is in NC, NM, GA, SC, TX and MO. Drop Kentucky: 90 of its 91 say "Not Required", and so do 66 of its 79 good dams.

**Skeptic's reason:**

VERDICT: NARROWED. The counts match exactly. The story on top of them does not hold as written.

**Reran it (Python door, read-only, 5 SELECTs)**
- Mart: 16,443 high-hazard dams, associated structures dropped. 2,776 rated Poor or Unsatisfactory, 2,776 distinct NID_IDs, so no duplicate loads. 753 have the plan flag False. One _SOURCE_RUN_ID. Same count in landing (16,443).
- BIA: 60 bad dams, 24 of them Unsatisfactory. Other spellings add nothing.

**What I found**

| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | blocker | **Kentucky "91 of 106" is a state-wide code, not bad dams missing plans.** 90 of the 91 say "Not Required" in the raw field; 1 says "No". Kentucky's good dams (Satisfactory or Fair) say "Not Required" on 66 of 79 and have a plan on only 15%, against 14% on its bad dams. | LIBRARY_RAW.LANDING.FED_NID_DAMS, EAP_PREPARED by condition, KY |
| 2 | real | **The flag merges three answers.** Staging sets `(upper(trim(EAP_PREPARED)) = 'YES') as has_emergency_action_plan`, so "No" and "Not Required" both become False. The 753 is 634 "No" + 119 "Not Required". The agent's no-NULLs check could never catch this, because it read the boolean, not the raw text. | C:/Code/Ripple_v6/library-onboarding/ripple_dbt/models/staging/fed_nid_dams/stg_fed_nid_dams__structures.sql (the has_emergency_action_plan line) |
| 3 | real | **The "about 95%" comparison uses Satisfactory dams only.** Satisfactory: 4,811 of 5,065 have a plan (95.0%). Fair: 4,191 of 5,113 (82.0%). The two together: 88.4%. Using each state's own good-dam rate, you'd expect 453 bad dams without a plan; there are 753. So about 40% of the 753 is just how each state reports. The bad dams are not the only ones missing plans. | Per-state good vs bad plan rates, landing |
| 4 | minor | **BIA is not part of the no-plan story.** It owns 60 bad dams, but only 4 of them have no plan. | Mart, OWNER_NAMES = 'BIA' |
| 5 | minor | **16.9% counts unrated dams in the denominator.** 3,489 high-hazard dams are unrated. Among rated dams the share is 21.4%, so 16.9% is a floor. | Mart |
| 6 | minor | **New Mexico's number is soft too.** Its 94 = 80 "No" + 14 "Not Required", and its good dams already lack a plan at 42%. Separately, 19 NM "No" rows carry a plan revision date, which contradicts the "No". | Landing, NM |
| 7 | minor | **May already be public.** AP counted poor high-hazard dams in 2019 (1,688). ASDSO, the state dam-safety officials' association, publishes plan coverage by state, as far as I know. I did not check either against primary sources. | Outside the warehouse |

**What survives**
- The 2,776 is real.
- The gap is real but smaller: bad dams lack a plan at 27.1% vs 11.6% for good dams nationally. After adjusting for state, the extra is about 300 dams, not 753.
- Extra no-plan dams over each state's baseline: NC +45, NM +33, GA +32, SC +30, TX +29, MO +19.
- Before any story: pull only the rows that say "No", and treat "Not Required" as a separate thread about state rules.

Every owner named here is a data match, not verified against primary records.

DISAGREE with the claim as written: Kentucky is a coding artifact; the comparison inflates the gap.

### NARROWED

**After skeptic:** Lower Brule Sioux Tribe (data match, not verified) is the only one of 67,777 non-state auditees whose auditor flagged going-concern doubt and material noncompliance in all 10 years, 2016-2025. No other auditee has even 7 years of both. Its federal spending did double, $16.7M to $35.7M ($246.2M total), but so did the typical tribe's. The jump is 2021 COVID money, not money that grew because of bad audits.

**Skeptic's reason:**

**Verdict: NARROWED.** The flag streak is real and rare. The "money kept growing" half is not about Lower Brule: every tribe's money grew.

**What I reran** (Python door, tag coverage-skeptic-2026-09-24; 8 statements: 4 SELECTs plus 4 session settings)

| Claim | Rerun | Status |
|---|---|---|
| One EIN, 10 years 2016-2025 | EIN 460222351, exactly 1 report per year, no duplicate loads | holds |
| Going concern 10/10 | Yes every year, no GSA_MIGRATION values | holds |
| Material noncompliance 10/10 | Yes every year | holds |
| $16.7M to $35.7M, $246.2M total | 16,657,266 to 35,668,193; the sum is 246.2M | holds |
| REDW since 2017 | Eide Bailly in 2016, REDW 2017-2025 | holds |
| 362 of 48,202 with going concern 3+ years | 362 of 48,202 | holds |
| Tribes: 13 of 827 | 16 of 898 when EINs that switch entity type are counted as tribal | minor: the definitions differ |

**Why it's rare (stronger than claimed)**
- Only 1 of 67,777 non-state EINs has both flags in 10 of 10 years. It's also the only one with both in 7+ years.
- Going concern 10/10 on its own: 5 auditees. Noncompliance 10/10 on its own: 79 (76 are local governments). The rare part is the pair.
- Tribal rates per report run 0.9-2.4% going concern and 5-9% noncompliance a year.

**Where it breaks: the money**
- Lower Brule grew 2.14x. For the 355 tribes with both a 2016 and a 2025 row, the median grew 1.77x, and 36.6% grew 2.13x or more. The doubling is normal for a tribe.
- All tribal dollars went $7.81B (2016) to $18.46B (2021). Lower Brule's own jump is also in 2021: $19.3M to $33.1M, which is COVID-era money.
- After the jump its dollars fell: $26.0M (2023), then $27.3M (2024). The "kept growing" line exists only because the two end years were picked.
- The column counts dollars the tribe spent, not what agencies awarded. There's no awards or findings table, so formula money (the boring explanation) is still not ruled out.

**Smaller gaps**
- The 2019-22 opinions list unmodified, qualified AND adverse at once, meaning different parts of the books got different opinions. It's not one adverse opinion on the whole audit.
- The 2024 filer name is "Lower Brule Sioux Tribe Governmental Services Department". The audit may cover only part of the tribe that year.
- Material weakness flips to No for 2023-25, at the switch to the new federal audit site (GSA's), where the overall weakness rate doubled. That's odd, and the report already notes it.
- Audit year 2025 is partial: 356 tribal reports, against about 700 in other years.
- Whether this is already known was not checked. The repo has no other mention of the tribe. A press search is the next step before calling it new.

**Files:** C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-0.md (lines 10, 27-34, 42); C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-0.sql (F02, F05, F06).

**Smallest fix:** keep the flag streak as the headline. Drop "while federal spending went from" as if it were the finding. Report the growth next to the median tribe's 1.77x instead.

DISAGREE, in part: the flags are unique, but the money growth is every tribe's.

### NARROWED

**After skeptic:** Illinois changed how it tests for lead in 2025. It moved 209 of its bigger systems from yearly or 3-year testing to every 6 months, and 22 went over the 15 ppb line for the first time, so the 7-town Illinois cluster comes from the new testing, not from water getting worse. Elgin is the exception: it was already over before the change (53 ppb now, over in 7 of 13 tests). Nationally, about 17 big systems (10K+ people) are over on their newest test, not 19. Newport RI and North Salt Lake UT have a newer test under the line. Data match, not verified against primary records.

**Skeptic's reason:**

VERDICT: narrowed. The count is off by about 2, and the Illinois story has a checked boring explanation.

RERUN (q1, same method as deep-2 [30])
- 19 systems, 724,514 people, 7 in Illinois. Reproduces exactly.
- One water-systems row per system and one release, so no stacked loads and the populations are clean.

HOLE 1 (real): "latest" means the period with the latest END date, and any period ending after today is dropped (deep-2.sql line 370).
- 3-year periods end later than newer 6-month ones, so the query can land on an older test.
- Newport RI (42K people): the 27.7 ppb reading was filed in 2024. A newer 2025-27 test reads 4.4. Not over.
- North Salt Lake UT (19K): the 16 ppb reading was filed in 2024. The first-half 2025 test reads 6.3. Not over.
- Kingman AZ (45K): the 110 and 60 ppb readings were re-filed into overlapping 3-year periods. Newer rows (filed 2025-05, updated 2026-05) read 0. Unclear.
- Missed: Two Rivers Utilities NC (97K), 20 ppb in a 2026-28 period.
- Dayton OH shows 0.47 "mg/L" (470 ppb), probably ppb typed as mg/L. The 1 mg/L cap can't catch typos under 1 ppb: 581 lead rows since 2015 sit at 100-1,000 ppb. None are on the 19 list, but they can inflate the 3+-periods and peer counts.
- Honest count: about 16-18 systems, roughly 0.62-0.76M people.

HOLE 2 (blocker for the Illinois angle): the agent left "Illinois changed its sampling" unchecked. I checked it (q4, q5; community systems of 3.3K+).
- 250 Illinois systems had a 6-month test in 2025. 209 of them were on yearly or 3-year testing before.
  - Rest of US: 645 of 823 were already on 6-month testing.
- Systems tested in a year: IL went from 108 in 2024 to 385 in 2025. MI stayed flat.
- Over the line: IL went from 3 at the prior test to 25, with 22 over for the first time. Rest of US went from 23 to 10.
- Median reading: IL rose from 3.2 to 4.55 ppb and 64% of systems went up. Elsewhere it was flat, and 33% went up.
- The 7 towns draw from the Fox River, Lake Michigan and wells. Different water, same jump in the same year: that points at how samples were taken, not at the pipes.
- Illinois also filed a second full-year 2025 lead row on 182 of 250 systems, median 1.2 ppb (10 systems elsewhere).
  - Example, Elgin 2025: 0 and 2.4 ppb on the full-year rows, 43 and 53 ppb on the 6-month rows.
  - The claim takes the higher 6-month row. If the full-year row is the official compliance number, the Illinois cluster disappears. Needs the EPA/state code lookup.
- 6 of the 7 Illinois towns jumped only in 2025.
  - Elgin didn't: 22.5, 21, 22.8 and 50 ppb in 2021-2024, before the change. Elgin is the real single-town lead. It is probably already known locally, since going over the lead action level requires notices to customers.

CONFIRMED
- The 370K max is copper (CU90) at KS2013505. There are 144 copper rows over 1,000.
- Elgin's 7 of 13 and Aurora's 183K people at 24 ppb reproduce.
- Aliquippa PA's latest test is from the first half of 2024, and Aliquippa is known ground (49.7 ppb back in 2020).

PARKED
- Lead has 888,760 rows and copper only 38,655. Copper looks mostly missing. Don't build on copper absence.
- 25.5% of lead rows are exactly 0, and it's unclear whether that means not detected or a placeholder.

DISAGREE with the claim as worded: Illinois cluster is a testing change; count ~17.

### NARROWED

**After skeptic:** When an inspector finds a serious defect at a water system and it never gets fixed, cases from before 2022 are still open at 19% in West Virginia, 11% on EPA-run tribal land in Region 9 and 9% in Louisiana. Other states are at 3%. The "1.7% state median" and the Region 6 and Region 10 tribal rates come from how cases get filed, not from real backlogs.

**Skeptic's reason:**

**Verdict: narrowed.** Every number in the claim reruns exactly. The comparison built on them does not hold.

**Reran and matched (8 statements, all read-only)**
- Region 9 tribal: 1,005 violations, 193 open, 19.2%
- Region 10 tribal: 379, 52 open, 13.7%
- Region 6 tribal: 173, 24 open, 13.9%
- West Virginia: 2,242, 482 open, 21.5%
- Louisiana: 710 open
- State median: 1.7% across 48 states
- Long-open list: 514 community systems, 1,594,035 people

**Findings**

| # | Severity | What breaks |
|---|---|---|
| 1 | **blocker** | **Wrong comparison base.** "Unaddressed" can only land on a violation with no end date. [s3] Nationally since 2022, 3,655 of the 3,804 Unaddressed violations are open-ended treatment-technique (TT) violations. Once a compliance period ends with no close-out, the violation lands in **Archived** instead. That covers 16,092 violations, including brand-new ones. Oklahoma: 946 of 1,029 violations from 2025 are Archived, and 48 of 48 from 2026. States with mostly limit (MCL) violations score about 0%: OK, FL, NC 0.0%; CA 0.1%. [s4] Counting open-ended TT violations only, the **state median is 7.45%, not 1.7%**. On share never resolved, the tribal regions sit in the pack: state median 16.2%, Region 9 tribal 28.9%, Texas 36.2%, California 47.7%, Louisiana 48.8%, Oklahoma 54.2%. |
| 2 | real | **The tribal range is cherry-picked.** EPA Region 8 tribal has 328 violations (more than Region 6) and is at **2.7%**. Region 7 is 5.5%, Region 5 is 8.2%, and Navajo (its own regulator) is 2.1%. |
| 3 | real | **Recent cases and late paperwork.** In Region 9, 134 of the 193 open violations began in 2025–26. Region 9 logs close-outs a median **478 days** after the fix; other states take 113 [s7]. Look at pre-2022 deficiency violations only, which leaves time for lag to clear. Share still open: other states 3.0%, **West Virginia 19.0%, Region 9 11.3%, Louisiana 8.8%**, Region 10 1.4%, Region 6 2.1%, Region 8 1.7%. Regions 10 and 6 have no backlog. |
| 4 | real | **The physical thing is an unfixed inspection defect, not contaminated water.** Violation code 45 (contaminant codes 0700/0800) makes up 168 of Region 9's 193, 369 of WV's 482 and 661 of LA's 710. [s8] Over 99% of open code-45 violations come after a site visit graded 'S' within the prior 3 years. That reads as a sanitary-survey significant deficiency; the 'S' code still needs EPA's lookup to confirm. |
| 5 | real | **The 1.59M people is mostly two known stories.** [s6] Portland alone is 666,200 people (41.8%). Portland plus Jackson MS is 53.7%, and the report itself calls both known. 324 of the 514 systems have only code-45 deficiencies open. |
| 6 | minor | West Virginia and Louisiana send letters (468 of 482 and 665 of 710 carry an informal action). Region 9 logs almost nothing (8 of 193). |
| 7 | minor | Splitting out code 5200 is justified: violation 2E under rule 351, dated 2024-10-17 almost everywhere (CA 699, FL 321, CT 312, TX 293). |

**What survives:** West Virginia, Region 9 tribal and Louisiana hold old unfixed-deficiency cases at 3 to 6 times the other-state rate. Open 2+ years: WV 218, LA 337, Region 9 48.

**Still not ruled out:** a defect fixed but never logged as closed. Test it with site visits after the violation date that no longer show an 'S' grade.

**Smallest fix**
- Re-base on code-45 or open-ended TT violations.
- Lead with the pre-2022 still-open rate.
- Drop Regions 6 and 10, and name Region 8.
- Take Portland and Jackson out of the people count.
- Say "unfixed inspection defect," not "health violation."

**Where it's wrong in the report:** C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-2.md lines 13, 42–53, 56 and 60. The queries behind it are [24] and [31] in C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-2.sql.

**My SQL:** C:/Users/wroge/AppData/Local/Temp/claude/c--Code-Ripple-v6/4be4d951-3f20-4c26-a1d6-4539a78dc789/scratchpad/sk_sdwa/s1.sql through s8.sql

DISAGREE: Ten-times gap is a filing artifact; real backlog is smaller.

### NARROWED

**After skeptic:** 19 charity-named 527s spent $195M to $202M from 2014 to mid-2026. The headline number depends on how amendment copies are dropped. The 19 are police, fire, veteran and cancer groups, plus one "United Health PAC". About three-quarters went to telemarketers and fundraising vendors, and about $0.4M went to contribution lines. The tightest tie: 11 of the 19 report 89.9-90.9% fundraising, 10 of them use the same purpose wording, and 9 of the 19 have paid BF-Telecom LLC since 2023. The Wisconsin link is weaker than claimed. It's a Regus office address that 4 groups started using in 2025-26, with 4 different records custodians. It doesn't tie together $115M. Two of the 19 have look-alike PACs registered with the FEC, so the scam-PAC press may already cover them. Every name here is a data match, not verified against primary records.

**Skeptic's reason:**

**Verdict: NARROWED.** The core cluster is real and the key number reproduces. Three supporting claims are overstated.

**Reran (8 statements, read-only, Python door)**

| Claim | Rerun | Status |
|---|---|---|
| $201.8M, 2014-2026 | $201.8M with the agent's copy-drop (same EIN + payee + date + amount). Keeping only the latest 8872 report per reporting period gives $195.0M. | holds, soft |
| 74% fundraising | 74% with the agent's copy-drop. 77% with latest-per-period. 71% counting only words like fundraising, telemarketing and caging, not "direct mail" or "phone". | holds |
| $0.2M to candidates | $0.36M. The agent summed rounded percentages. These are rows with "contribution" or "donation" in the purpose, not proven candidate payments. | minor |
| Four share a WI address, $114.7M | That address shows up only on 2025-26 reports. Both addresses are Regus offices: the groups pay "REGUS" at both. It's 3 groups at Delafield and 1 at a different Regus in Brookfield, not next door. The 4 have 4 different custodians. The $114.7M is lifetime spending; their 2025-26 spend is about $17M. The link since 2018 is a Brookfield caging firm, North American Fulfillment. It also serves real state FOP (police union) political funds (SC, MI, LA), so it doesn't prove one operator. | real |
| Nine groups at exactly 90%, BFTELECOM top payee | The 9 are the groups whose share rounds to 90%. BF-Telecom is top payee for only 7 of them. The better set: BF-Telecom is paid by 11 groups (9 of the 19, plus AMCC PAC and UCVF PAC), all starting 2023-01 or later. 11 of the 19 sit at 89.9-90.9%. 10 use "FUNDRAISING, DONOR MANAGEMENT, DATABASE SERVICES". | real |
| Outside FEC filings | FEC has a Police & Sheriffs Coalition PAC whose treasurer is Frank Pulciani, the same name as a custodian here. It also has a Veterans In Defense of Liberty PAC in Springfield MO, the same city as the 527. The known-story risk is higher than the report says. | real |

**Other checks**
- Lump rows on the 19 groups hold $11.3M raw. Examples: "ALL DISBURSEMENTS FROM 7/1-12/31/2025", "SCHED B EXPENDITURES IN PERIOD", "WITHHELD".
- Each Wisconsin group filed its second-half 2025 total twice: once as WITHHELD, once as ALL DISBURSEMENTS. The payee text differs, so the copy-drop keeps both. That's about $3.2M double-counted.
- New fact: from mid-2025 all four Wisconsin groups stopped naming who they paid. That's a real same-filer fingerprint and a stronger tie than the address.
- Triage for the whole table checks out. Latest-per-period gives $11.168B against the agent's $11.269B, and the payees are card processors and ad buyers.

**Blind spot:** keyword matching undercounts vendor spend. For example, "DATA" and "TECHNOLOGY SERVICES" payments to Residential Programs Inc don't match. I had no web access, so I couldn't check the press coverage.

**Files**
- C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-3.md, lines 46, 52 and 56
- C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-3.sql, statements [21], [28] and [30]

**Smallest fix:** rewrite the Wisconsin line as "Regus address since 2025, plus a Brookfield caging firm since 2018". Rewrite the template line as "11 groups at ~90%, 9 pay BF-Telecom". Change $0.2M to $0.36M. Add the two FEC look-alikes.

parked: the scratchpad is shared by parallel agents. My run.py was overwritten mid-task, so write inside your own subfolder.

AGREE, narrowed: cluster is real, the Wisconsin and 90%-template ties are overstated.

### NARROWED

**After skeptic:** The 2.6x-over-chance number doesn't hold up. Once you count how often the same name shows up more than once on the exclusion list, and where surnames actually live, chance predicts 46 to 50 same-state hits. The data has 54. In CA it's 15 hits against 15.6 expected. What survives is a short list of LA owners whose exclusion record is in the same line of work. Liana Karapetyan was barred in 2023 while she was the listed official of ANG Health Care, a home health agency, and since 2024-06 she has owned 100% of Direct Care HH. Kristine Arutyunyan was barred in 2024 as a hospice executive and owns Holy Light and May Light HH. Arman Danielian was barred in 2026-01 and is still listed at Vita, Valeo and Arva HH. All three are data matches, not verified against primary records.

**Skeptic's reason:**

VERDICT: narrowed. The statistical headline is broken. Three named cases are left to check against court records.

What I checked: 7 SELECT statements, Python door, tag coverage-skeptic-2026-09-24.

**Reproduced as claimed**
- 349 owner names appear somewhere on the exclusion list. 54 of those appear in the owner's own state. The report's baseline reran at 20.7.
- 12 of 941 new CA agencies have a matched owner. 54 of the 55 matched agencies are on Care Compare.
- The exclusion list is one load run, 83,816 rows, with no duplicate loads.

**Blocker: the chance baseline is too low**
- The report treats each name as one person on the list. Many names are on the list more than once. Correcting for that alone raises chance to 31.6.
- It also assumes a name is equally likely in any state. Armenian surnames sit mostly in CA and Hispanic ones in FL and TX. Using each surname's real spread across states in NPPES (the national provider registry), chance is 45.9. Using the exclusion list's own surnames, leaving out the matched first name, it's 49.9.
- Observed is 54. That's about 1 standard deviation above chance, which is noise.
- By state, observed vs expected (NPPES surnames / list surnames): CA 15 vs 15.6 / 11.9, FL 17 vs 9.0 / 15.7, TX 15 vs 12.6 / 13.2.
- The report calls the CA cluster 'the matches'. The corrected CA baseline predicts almost exactly what showed up.

**Real problems**
- '44 people' is really 44 CMS owner IDs. Anna Gasparyan is two separate owner IDs, each 100% owner of a different agency (Monarch and Safe Choice), so CMS treats them as two people. At most one of them can be the Anna Gasparyan barred in 2003. Mohamed Ahmed in OH is three owner IDs.
- The 1.3% vs 0.44% comparison uses the wrong group. The right comparisons are older CA agencies at 0.27% (6 of 2,206) and new agencies outside CA at 0.30% (2 of 665).
- Some of the gap does survive. Among owners with -YAN/-IAN surnames, new CA agencies match 8 of 746 owner IDs (1.07%) and older ones 2 of 876 (0.23%). That's about p=0.03 before correcting for how many cuts were tried, and 8 IDs is only 7 names.
- Many of the 54 are very common names. Same name in the same state in NPPES: Tam Nguyen CA 33, Jessica Smith CA 28, Maria Garcia TX 28, Jose Martinez TX 17, Juan Rodriguez FL 15, Jorge Perez FL 14.

**Minor**
- 3 of the 12 'LA-area' agencies are in Simi Valley, which is Ventura County.
- Several exclusions date from 1991-1998. Some are 1128b4 exclusions (license revoked), not fraud.
- 'The exclusion list stores no birth date' is true of the table in the warehouse. As far as I know, OIG's downloadable list does carry a birth date column. I didn't check the landing table.
- One owner role date is 2026-10-31, which is after the file was loaded.

**What survives: a second field agrees on the type of business**
- Karapetyan: the exclusion list gives her NPI as 1447482435. In NPPES that NPI is ANG Health Care Inc, a home health agency in Folsom, with LIANA KARAPETYAN as its official. The owner file lists a Liana Karapetyan as 100% owner of Direct Care HH (Pasadena, CCN 559402) from 2024-06-21. Her exclusion is dated 2023-04-20. The cities don't match.
- Arutyunyan: the exclusion list files her under hospice, business owner or executive, excluded 2024-01.
- Danielian: the exclusion list files him under drug company, business owner or executive, excluded 2026-01-20 under 1128a3. He took a 26% stake in Arva on 2025-12-04 and was still listed in the 2026-09-07 owner file.

**The boring story is already known**
- LA home health and hospice fraud rings are an old news story. Only the named listings would be new.

**Smallest fix**
- Drop the 20.8 baseline and the 2.6x line.
- Lead with the three cases where the business type matches, and pull the court records for them.

**Files**
- C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-5.md, lines 11, 21, 45, 47, 50
- C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-5.sql, statement [18] (the baseline)

DISAGREE: the 2.6x excess is surname geography. Three cases survive.

### NARROWED

**After skeptic:** This is a California family-therapist story, not a counselor story. 4,696 of CA's 4,890 opt-outs are MFTs (96%), and 185 of its 199 billers are MFTs. CA MFTs opted out at 37%. That's close to CA psychologists (32% for decisions made since 2024) and 3.5x CA social workers (11%). The 2.3x comes from pooling: high-opt-out MFTs lumped with a few counselors, measured against low-opt-out social workers lumped with psychologists.

**Skeptic's reason:**

VERDICT: narrowed. Every number reruns exactly. The frame, the ratio and one "ruled out" don't hold.

**Rerun (9 statements, Python door, tag coverage-skeptic-2026-09-24)**
- CA opt-outs: 4,696 MFT + 195 MHC = 4,891. Matches 4,890.
- CA billers with 11+ patients: 185 MFT + 14 LPC = 199. Matches.
- CA opt-out share: MHC+MFT 35.8%, psych+CSW 15.6%. Matches.
- US opt-outs per biller: 4.15 vs 0.53. Matches.
- Years line up: the latest PECOS enrollment-ID date is 2026-06-29 and the opt-out file was last updated 2026-07-13, so both are the same snapshot.
- Part B has MHC/MFT billers, which confirms it's 2024 or later.

**Findings**

| # | Severity | What | Evidence |
|---|---|---|---|
| 1 | real | It's MFTs, not counselors. CA MHC is tiny: 195 opt-outs, 893 enrolled. CA holds 70% of US MFT opt-outs (4,696 of 6,723) and 53% of MFT enrollments. "CA has 34% of the nation's opt-outs" really means "CA has most of the nation's MFTs." | skeptic query E |
| 2 | real | The 2.3x is a pooling artifact. CA, opt-outs since 2024 vs enrollments since Nov 2023, by profession: MFT 37.3%, psychologists 31.6%, MHC 17.9%, CSW 10.7%. MFT vs psychologists is only 1.2x. Nationally, counselors (10.0%) opt out less than psychologists (25.3%). | query E |
| 3 | real | CA runs high for every profession, not just the new ones. CA vs rest of US: MFT 37% vs 22%, MHC 18% vs 10%, psychologists 24% vs 16%, CSW 9% vs 7%. | query E |
| 4 | real | "Ruled out: opt-out as a first step toward enrolling" is a check that can't fail. The opt-out list and PECOS are mutually exclusive by design: 0 of 15,123 opted-out psychologists and social workers appear in PECOS at all. One snapshot can't test that hypothesis; it needs two snapshots. | query F; deep-6.md line 68 |
| 5 | real | "Hit means few people seeing seniors" overreaches. Opting out is how a therapist sees Medicare patients for cash. A high share can just mean a big senior cash-pay market. | deep-6.md line 60 |
| 6 | minor | The per-biller ratio mixes years. Opt-outs run through mid-2026 (25% of MHC+MFT opt-outs are 2025-26), but billers are 2024 only. On top of that: first-year ramp, and the file hides anyone under 11 patients. MHC alone is 2.5 per biller; MFT alone is 15.7. | query E |
| 7 | minor | The US row sums states, so providers enrolled in two states count twice. Counted by distinct NPI, the US share is 14.7% vs 10.1%, not 14.1% vs 9.5%. | deep-6.sql q17 GROUP BY ROLLUP(st) |
| 8 | minor | "Didn't leave" mostly holds. Only 10 opted-out MHC/MFT billed Part B in 2024, and 9 of them opted out in 2025 or later. Anyone who left after seeing fewer than 11 patients is invisible. | query F |

**Boring explanations still standing**
- Practice setting: MFTs and psychologists are mostly private practice, and social workers often bill through an agency.
- Association guidance drove a January 2024 filing wave: 5,093 opt-outs in one month.
- Low Medicare rates. The report itself concedes trade press has covered them.

**Smallest fix**
- Split the table by profession, CA vs the rest of the US.
- Compare decisions made since 2024 on both sides.
- Retitle the headline around MFTs.
- Downgrade the "ruled out" line to "can't test with one snapshot."

**Files**
- C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-6.md
- C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-6.sql

DISAGREE with the claim: it's MFTs versus social workers; psychologists run close to MFTs.

### NARROWED

**After skeptic:** Units whose patients mostly live in nursing homes get flagged for deaths far more than anyone else. Part of that comes from CMS's model: it under-predicts nursing-home deaths everywhere (nursing-home residents die at 1.18x expected, everyone else at 0.94x). Comparing nursing-home residents with nursing-home residents, Dialyze Direct and Concerto (31 clinics, 18 of 26 rated flagged Worse on survival) still run 1.61x expected: about 37% above nursing-home residents nationally, but only about 9% above other nursing-home-heavy units (1.48x). Home Dialysis Services is not a nursing-home operator in this data. Maryland's 9 flagged independents are all nursing-home units. The boring explanation is still open: bedside units may get the frailest residents. All names are data matches, not verified against primary records.

**Skeptic's reason:**

VERDICT: narrowed. The numbers reproduce exactly. The framing does not hold up.

RERAN (11 statements, 2 of them failed on column names; Python door; SELECT/WITH only)
- 7,557 rows, 7,557 distinct CCNs. No duplicate loads.
- Survival categories: As Expected 6,876 / Not Available 304 / Worse 214 / Better 163. Death rates run 0 to 66.4, with no sentinels. 4 clinics have a rate of exactly 0.
- Q29 matches to the digit: 46 clinics, 20 Worse, 38 rated, weighted death rate 32.27 vs 21.65, everyone else 2.27% (2.34% of the rated ones), median 1 station, other independent for-profits 33 of 421 (7.8%).
- Maryland: 9 of its 12 Worse clinics are independent for-profits. That checks out.

GAPS
| # | Severity | Finding |
|---|---|---|
| 1 | real | The "46 nursing-home operator clinics" group is contaminated. 13 Home Dialysis Services clinics (IL-based) have no nursing-home rows at all in the facility-report table (HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES, 2021-24). They run 1.08x expected with 2 of 10 rated flagged, so they look like a home PD/HHD program. Two more are DaVita and DCI home programs. The true brands are Dialyze Direct, Dialysis Direct and Concerto: 31 clinics, 18 of 26 rated flagged, 1.64x expected. |
| 2 | real | The boring explanation is partly confirmed, and the data was already in the warehouse. The facility-report table carries "All Patient Mortality (Nursing Home)" observed and expected deaths for each clinic. Nationally, nursing-home residents die at 1.179x expected; everyone else dies at 0.937x. So a unit treating only nursing-home residents starts about 25% "worse" by construction. |
| 3 | real | Like-for-like (nursing-home residents only): Dialyze Direct + Concerto 1.611x. Other independent for-profits with 50%+ nursing-home residents: 1.476x. Non-chain units with 50%+ nursing-home residents: 1.485x. DaVita 1.10-1.26x, Fresenius 1.06-1.18x. The brands carry a real excess, but it is a class effect (nursing-home-heavy units) more than a brand effect. |
| 4 | real | "Other independent for-profits still run 7.8% Worse" is mostly nursing-home units too. 21 of the 33 have 15%+ nursing-home residents, and 16 have 50%+. Among units under 15% nursing-home residents: 12 of 265 rated flagged (4.5%) at 1.02x expected, vs DaVita 2.5% and Fresenius 2.0%. |
| 5 | real | Maryland is not a separate story. 11 of its 12 independent for-profits have 53-100% nursing-home residents. The 12th is Dialyze Direct MD, whose nursing-home rows are missing, so the flag has holes. |
| 6 | minor | "At or below average" is wrong for DaVita: its death rate is 22.11 vs 21.80, and it runs 0.978x expected vs 0.968x nationally. "About average" is accurate. |
| 7 | minor | Whether this is already a known story was not checked (no web access). |

BLIND SPOTS OF MY CHECK
- The nursing-home share rests on CMS's nursing-home flag, and suppression under 11 patients hides small counts.
- Joining CCN to the facility table matched 7,403 of 7,557 clinics. State agrees on every match. The years line up: 2021-24 in both tables.
- Unmeasured frailty (bed-bound residents get dialyzed at the bedside) cannot be separated from worse care with this data.

Files: C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-4.md, C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-4.sql (Q22, Q23, Q29)

DISAGREE with the framing: real nursing-home excess, but not three brands.

### NARROWED

**After skeptic:** SpaceX's own sites ran 3.2x their industry's injury rate in 2025 (3.6x in 2024) and Bath Iron Works ran 2.7x (3.0x). Ford's plants ran 2.7x their industry pool (2.2x), but only about 1.9x GM, Toyota, Honda and Tesla head to head. The 'Ingalls 1.10x' line is really Newport News Shipbuilding. The Ingalls yard in Pascagoula isn't in either year's file. This is a year-on update of F-035 to F-037, not a new find. Data match, not verified against primary records.

**Skeptic's reason:**

VERDICT: narrowed. The core pattern holds. One label is wrong, and Ford's size depends on who you compare it to.

REPRODUCED: I reran deep-9 [14] (C:\Code\Ripple_v6\reports\coverage_2026-09-24\deep\deep-9.sql lines 148-182). Every number matches to the digit: 3.27/3.12, 2.14/2.47, 3.01/2.67, 0.84/0.81, 1.03/1.10.

FINDINGS
1. REAL - 'Ingalls' is the wrong yard. The INGALLS/HII tag (deep-9.sql line 166) catches only Newport News Shipbuilding (HII's Virginia yard, EIN 540318880, 27K workers) plus a Waco contractor. The Ingalls yard in Pascagoula is in neither year under any name. I searched '%INGALLS%', plus Pascagoula sites coded 3366xx or with 500+ workers. So 1.03x to 1.10x is Newport News, and Ingalls isn't measured at all. Fix: relabel the row in deep-9.md line 36.
2. REAL - Ford's multiple depends on the peer pool.
   - Plants only (NAICS 3361-3363): 2.18x to 2.66x. The claimed 2.47x is actually low.
   - Same sites in both years: 2.20x to 2.55x, so late filers aren't driving it.
   - Head to head in vehicle assembly (3361), 2025, cases per 100 workers: Ford 11.4, GM 6.5, Honda 6.8, Tesla 5.9, Toyota 5.2. That's 1.9x the big four and 1.75x GM.
   - GM is also a union (UAW) shop, so looser union record-keeping doesn't explain it.
   - The industry pool is pulled down by Stellantis at 1.2-1.5 on 30-40M hours. For a UAW assembler that looks under-reported or partial.
   - Say 'about 2x the big automakers', not 2.5x.
3. MINOR, and it helps the claim - SpaceX's own sites run higher than the name tag.
   - Own sites, tagged by company name: 3.58x (2024) to 3.22x (2025).
   - Tag by name, not EIN: the 2024 SpaceX rows have a blank EIN, so an EIN-only rerun drops all of 2024.
   - The name tag is diluted by ABM, PCAM and Performance Contractors rows, and by one valet crew filed twice: PCAM '2337 SPACEX VALET' and '4189 SPACEX' carry the same 1.57M hours in 2024 and the same 1.44M in 2025.
   - SpaceX's space-vehicle sites (336414) against peers present both years: 4.65x to 4.15x.
4. MINOR - Electric Boat 2025 has only 2 of the 7 General Dynamics Electric Boat sites filed in 2024; the small outposts are missing. The 2024 tag also caught Duffy Electric Boats, a California boat maker, and an Aramark café.

BATH HOLDS: one clean site, EIN 391343528. 12.70 to 11.82 against shipyard peers present both years at 4.37 to 4.42.

POOL CHECKS PASSED:
- The year column matches the table year.
- No peer site logs more cases than workers.
- No single site holds more than 25% of a pool.
- 1,017 and 1,389 exact-twin rows exist; only the PCAM twin touches these numbers.

ALREADY KNOWN: the SpaceX story is already out (Reuters, 2023); the report says so itself. I didn't check press on Ford or Bath. I didn't retest the 'deaths dead' and 'top-rate dead' calls.

QUERIES: C:\Users\wroge\AppData\Local\Temp\claude\c--Code-Ripple-v6\4be4d951-3f20-4c26-a1d6-4539a78dc789\scratchpad\b1.sql through b4.sql, run by sk.py. 9 SELECT/WITH statements plus the required ALTER SESSION pair on each of 4 connections, tag coverage-skeptic-2026-09-24. Python door only.

AGREE, narrowed: pattern holds; 'Ingalls' is Newport News; Ford nearer 2x.

### NARROWED

**After skeptic:** In Medicare's Feb-2026 hospice roster, 200 LA County hospices sit 3 or more to a building, at 53 addresses. That's 45% of LA hospices at a shared address, against 8% outside California. LA holds 14% of US hospice enrollments (846 of 6,066), not 16%. The ZIP3 cut had pulled in 31 hospices from six other counties. 'All still certified' proves nothing: every group matches the older certified list at 99%. The LA stacking is already reported. What's new: 12 San Antonio hospices with legal names running CFHC NO4 to NO22. 8 were incorporated on 2021-10-07, 6 sit in one building, and they trade under about 10 different brand names. CFHC is the only numbered-name series in the national file. Data match, not verified.

**Skeptic's reason:**

VERDICT: NARROWED. The pattern is real, but three of the headline numbers are wrong or say nothing.

WHAT I RERAN (11 statements, Python door, tag coverage-skeptic-2026-09-24)
- Reproduced: 231 rows, 231 NPIs, 231 CCNs, 59 addresses, 231 of 231 CCN matches, 206 certified 2019 or later, 0 same-suite rows.
- The certified list HEALTH__FED_CMS_HOSPICE has its own COUNTY_PARISH column. The agent used ZIP3 instead.

FINDINGS
| # | Claim | What the data says | Severity |
|---|---|---|---|
| 1 | 231 LA County hospices at 59 addresses | By Medicare's own county field: 200 at 53 addresses. The other 31 are in San Bernardino (23), Riverside (2), Ventura (3), Kern, Orange and San Diego. 18 of them are real stacks in Montclair and Upland (ZIP3 917). | real |
| 2 | LA is 16% of US enrollments (981 of 6,066) | 846 of 6,066 = 13.9% by the county field. At most 14.9% if all 60 unmatched rows were LA. | real |
| 3 | All 231 still on the certified list 'in a 2026 file' | The certified list is the older file: certification dates stop at 2025-10-15. The 2026 file is the enrollment roster itself (newest ID O20260203; I did not rerun that). The match rate is 99.2% for other LA, 98.9% for the rest of the country and 99.0% overall. So 100% is the normal rate, not a signal. | real |
| 4 | 'Each CFHC has its own ASSOCIATE_ID' | True by construction: every legal entity gets its own ID. The owner link lives in the hospice owner file, which isn't landed. | minor |
| 5 | CFHC facts | All confirmed: 12 rows, 8 incorporated on 2021-10-07, 3 on 2021-10-25, 1 blank. 6 sit at 2819 NW Loop 410, suites G, L, O, Q, R and S. NO7's address line is written '2819 NW LOOP STE G', so a strict address group splits it off. | ok |
| 6 | Missed angle | Behind the CFHC names are about 10 brands: All Faith, Bexar Hospice, Harmony, Nightingale, Willow Tree, Arms of Compassion, Genisa, Texas Heroes, Alta Vita, Ariel. A national check on legal names ending in 'NO n' or '# n' found CFHC is the only series with more than one member. Every other stem appears once, e.g. E HOSPICE GROUP OF <state> NO 1. | upgrade |
| 7 | Boring explanation | The LA stacking is already reported (LA Times, ProPublica, CMS enhanced oversight), as the agent itself says. That leaves CFHC as the only genuinely new piece. I did not check it against the news. | real |
| 8 | Addresses disagree | 23 of the 231 carry a different ZIP in the certified list. Example: enrolled at a Van Nuys stack address, certified location in Bakersfield, Riverside or San Diego. Either the hospice moved or the enrollment address isn't where it operates. | minor |

WHAT HOLDS
- LA County by the county field: 59.5% incorporated 2019 or later, and 44.7% at a shared address.
- Outside California: 27.0% and 8.0%.
- No LA suite is shared by two hospices, so this is one building, different suites.

BLIND SPOT OF THE METHOD
- The address group is an exact match on line 1 plus ZIP5. Spelling variants ('2819 NW LOOP' vs '2819 NW LOOP 410') split real stacks, so the stack counts are floors.

PARKED: 428 of LA County's 1,274 certified hospices (34%) are missing from the 2026 enrollment roster, against 7.5% elsewhere (418 of 5,578). 340 of those 428 were certified 2019 or later. That looks like the revocation wave, and it may be the bigger lead.

Files: C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-7.md, C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep/deep-7.sql

DISAGREE with the claim as written: the stacking is real, but the county proxy, the 16% and 'still certified' don't hold.

## Deep pass, all 50 tables

| table | triage | verdict | headline | boring explanation |
|---|---|---|---|---|
| ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | 8.0 | live | On tribal land where EPA is the regulator, 13.7-19.2% of health-based violations begun since 2015 are still unaddressed today. The state median is 1.7%. West Virginia is at 21.5% (482 open, 204K people), Louisiana has 710 open (456K people), and 514 community systems (1.59M people) have one open for 2+ years. | The 'no action' rate (65% on tribal land) is mostly paperwork habit. Most of those violations carry a 'compliance achieved' close-out (SOX/EOX), and states log a notice letter where EPA regions don't. So I led with the unaddressed-today rate instead. Slow data entry could still inflate that rate; not ruled out. Portland and Jackson MS are known stories. The MT0002988 severity pile was not checked (budget). |
| ENVIRONMENT__FED_NID_DAMS | 7.5 | live | 2,776 of 16,443 high-hazard dams are rated Poor or Unsatisfactory (16.9%). 753 of those have the emergency-plan flag set to False (27%), against about 95% plan coverage on Satisfactory ones. Kentucky: 91 of 106. New Mexico: 94 of 145. BIA owns 60 of the bad dams. | AP counted poor high-hazard dams in 2019 (1,688; different method, so no trend claim). The years-since-inspection angle is killed: in GA, IN and PA, good and bad dams show the same median years (9.6 vs 9.7, 7.2 vs 7.9, 5.9 vs 5.9), and those states' records are about 1,950 days old, so it is reporting lag. The plan flag has no NULLs, so 'not reported' may be folded into False; not ruled out. Federal dams are 78.4% unrated, so federal counts are floors. |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES | 7.5 | live | 19 active community water systems serving 10K+ people are over the lead action level on their latest test (2024-25), serving 724,514 people. 7 of the 19 are in Illinois, including Elgin (53 ppb, over in 7 of 13 periods) and Aurora (183K people, 24 ppb). Triage's 370K 'lead' max is copper junk. | The persistent list is the known cities; not ruled out, that is the explanation for that list. The Illinois cluster may be a change in how systems sample, not worse water; unchecked. For a tiny system, the 90th percentile of 5 samples is basically the worst tap. Big systems test every 6 months and small ones every 3 years, so period counts don't compare across sizes. Peers: small non-community systems (schools, plants) have the highest share ever over, 12.5-12.7%, against 3.6-8.6% for community systems. |
| ENVIRONMENT__FED_FRACFOCUS_REGISTRY | 6.5 | probed | 16.2% of chemical rows nationally are hidden as trade secrets. Diamondback hides 30.3% in Texas (state rate 16.2%) and has secrets in 96.7% of its 3,164 jobs. QEP (WY), Chesapeake (TX, OK, OH) and Cimarex run 10-14 points above their own states. There are no job dates at all, so no drought angle. | Trade-secret claims are legal and industry-wide, and advocacy reports have covered them. The facts line's TVD and water sums are dead: both repeat on every ingredient row (0 of 248,835 disclosures vary), the Clayton Williams max depth is 1.19B ft, and 74 jobs claim more than 40K ft. The drought angle can't be done because there are no dates. |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | 6.0 | probed | The top 1% of TRI sites (218) put out 81.6% of 2023's 2.98B lb on-site release. Metal mines put out 50.4%, and one mine, Red Dog (Teck, AK), put out 25.9% (771M lb). This is EPA's own annual headline. | Mines count moved waste rock as a release; confirmed as the reason for the ranking. Non-mining leads: hydrogen sulfide at gas plants (Dark Horse Treating, Jal NM, 73.6M lb; Targa Midway 42.0M lb) may be acid gas pumped underground and counted as a release; unchecked. Carcinogen air is topped by styrene from fiberglass boat and bathtub makers (Onyx Collection KS, 751,599 lb). Whether the sites are near people was not tested (needs a census join). |
| ENVIRONMENT__EPA_PENALTY_GAP | 7.5 | dead | Split by state, the minority gap flips: long violators in minority areas are worse off in 8 states, better off in 10, tied in 1. The 'never fined / never inspected' flags are mostly drinking-water systems and time-window effects. | Confirmed. State programs record differently: Georgia (67%/63%) and Colorado (62%/55%) lack inspection dates whatever the neighborhood. Drinking-water systems are 38,522 rows (41%), 21,634 of the 53,437 long violators and 19,994 of the 'no fine, no inspection' rows. The 12-of-12, never-fined list is mostly small-town sewage plants and mobile-home parks. A few industrial names (SK Battery America GA, Stella-Jones PA, ARI Railcar GA) are data matches, not verified. |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS | 6.0 | probed | Penalties vary 20-40x between states, but the biggest driver is what each state reports into this federal file. The clean peer number is Oklahoma refineries at $3.3K penalty per logged violation against Texas at $142K, on only 9 facilities. | Not ruled out. California districts log every notice of violation (Kern Oil: 532 cases, median $8,625). EPA-heavy states show bigger medians (OH 36.6% EPA, median $50,850 for major sources; TN $3,000). National settlements sit on one facility row: the $100.7M max is EES Coke Battery MI and $64.5M is Henry Charging ND well pads. Refinery-coded facilities include small units and nothing is weighted by plant size. |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY | 6.0 | dead | The 'states let high-priority violators ride' angle measures which states report into ICIS-Air: 558 of 8,896 HPVs from 2012-2021 (6.3%) never drew a formal action, and the state outliers are reporting gaps. | Confirmed. Ohio logged 347 formal cases to Indiana's 1,176; Louisiana refineries logged 6 violations against 85 formal cases. California holds 52% of HPVs (4,659) because its local districts log everything. The 173 open HPVs with no action include plants the file lists as permanently closed and known names (Greka Energy Cat Canyon). Michigan's 64.4% unresolved (101 HPVs, median 1,830 days to resolve) is parked, not explained. |
| ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS | 6.0 | probed | The famous $6.7B is two identical $3.35B lines under two EPA region case numbers. With BP set aside, the biggest water fines are a Texas recycler ($57M), a bankruptcy claim ($39M) and a likely typo ($30M). | Partly confirmed. BP is famous, and its two lines are 04-2010-9036 and 06-2011-4881, both on 2012-06-18, both $3,352,250,000. That looks like one settlement logged twice or split in halves; not checked against the consent decree. The 10-12% penalized shares (OK 12.2%, IL 10.0%) may mean orders are logged here and penalties land elsewhere; not ruled out. Lead: Altair Recycling Facility TX, $57.0M state civil judicial on 2025-06-06, also has open RCRA violations. Data match, not verified. |
| ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS | 6.5 | probed | Almost every hazardous-waste violation gets a fix date. Only 2,247 violations at 715 handlers from 1980-2020 are still open, out of 614K+, and 222 of those handlers still carry an EPA flag in 2026. | Partly confirmed. The open pool is tiny, and the oldest names read like abandoned or cleanup sites (Dynachem IL, Chemetco IL, US Oil Recovery TX). The 5.4% open for 2020-24 and 19.7% for 2025-26 is ordinary lag. Most violations are generator paperwork (262.A 189K rows, 262.C 113K). Still flagged in 2026: City Foundry San Antonio (open since 1995), Clean Harbors of Colfax LA, Altair Recycling TX, Santolubes SC. Data matches, not verified. |
| FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES | 7.0 | live | 19 police, fire, veteran and cancer 527s spent $201.8M from 2014 to 2026: 74% went to fundraising-type purposes, $0.2M to candidates. Four of them share a Delafield or Brookfield, WI address ($114.7M), and nine share one template (exactly 90% fundraising, BFTELECOM LLC as top payee). The triage question, who gets the $13.3B, lands on card processors and party ad buyers, which is boring. | Scam PACs are a known genre: CNN 2020, the Daily Beast's $140M network story, Jacobin 2024 and The Lever, mostly from FEC data. Telemarketing-heavy spending is legal. Not ruled out that some of these groups are already covered. The triage 'boring' is confirmed for the top payees: governors-association ad buyers and payment processors. |
| FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE | 6.5 | probed | 2024 Senate general independent spending: $675.2M backed the winning side, $516.1M backed the loser (43% of the $1,191.3M scored). WinSenate put 59% ($177.9M) on the losing side; SLF PAC put 29% there. The House can't be scored because WHO_WON stops at 2018. | The money is the famous super PACs: FF PAC $502.6M, MAGA Inc $319.3M against, WinSenate, CLF, SLF, HMP. Money flows to toss-ups, so a near 50/50 split is expected, and press scorecards exist. Holds. |
| ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS | 6.5 | probed | County density per person is big: Forest PA has 1,685 wells per 10K people, Monroe OH 1,491, Nowata OK 1,441. Venango PA holds 4,786 wells (25% of PA's). The operator angle is dead: no operator column exists. | Counts reflect how hard each state documented its wells. Appalachian orphan wells are widely reported. Not ruled out. The triage's load-duplicate explanation is ruled out: the 434-row repeats don't exist. |
| ENVIRONMENT__FED_USCG_NRC_INCIDENTS | 7.0 | probed | Peer outliers exist. CSX plus Norfolk Southern made 8.2x the NRC calls per year of UP plus BNSF in 2015-17, down to 1.8x by 2024-25. Cox Operating logged 404 calls in 2021-23 against Chevron's 283 nationwide. But the table is call headers only, with no material, amount or spill location. | These are self-reported calls, and reporting habits differ by company. CSX's 75% drop in yearly calls could be a change in who phones it in. Taylor Energy's MC-20 leak is well known. Not ruled out. The triage's 'SEQNOS 999999 sentinel' is false: SEQNOS is unique and runs 1 to 1,469,629. |
| FCT_DATASET_SIZE_HISTORY | 7.0 | probed | Data set 10's pager fell from 10,071 pages (~503.6K files) to 5,569 (~278.5K) on 2026-03-11 and held for 10 snapshots through May. But DS9 and DS11 made drops just as big that later reverted, so no drop can be called a removal from this table. | Pager parse glitches, confirmed: a '2 pages' reading appears at random on 10 of 12 pages. A site template change explains page-one counts falling by exactly one on 9 of 12 pages the week of 2026-02-03; on a multi-page list, a removed file can't shrink page one. The only file-level blip: DS6 lost one file from 2026-02-10 to 2026-03-19. |
| HEALTH__FED_CMS_HOME_HEALTH_OWNERS | 7.5 | live | 54 home health owners with 5%+ stakes share a first name, last name and state with someone on the OIG exclusion list, where chance predicts 20.8. After dropping middle-initial conflicts, 44 people are left. 54 of their 55 agencies are still on Care Compare, and 12 are LA-area agencies certified 2023-25 (12 of 941 new CA agencies, 1.3%, against 0.44% of all agencies nationally). All names are data matches, not verified against primary records. | NOT ruled out: names cluster by place (Armenian surnames in LA, Hispanic names in FL/TX), which raises chance same-state hits above the 20.8 baseline, so the true excess is under 33. City can't serve as a second check: only 9 of 141 rows agree on city, and the exclusion-list address is often a prison town (Coleman FL, Beaumont TX). Big chains owning hundreds (UnitedHealth 355, LHC 297) are legit and aren't the story. RULED OUT: the triage worry about 85.6K null CCNs. CCN is 98% filled (99,287 of 101,188). No LA/Houston owner-network cluster shows by owner ID (CA 4.9% and TX 4.0% of agencies have a 3+-agency individual owner, against 3.4% nationally, 6.4% in CO and 6.3% in OK). The hospice half of the angle can't be tested because no hospice owner file is landed. |
| HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES | 6.0 | probed | Against their own states, chains run at a median of 1.00x fire citations per home and a max of 1.95x; 22 of 301 chains sit at 1.5x or more. CareCore Health (OH, 12 homes, 1.95x, 11 of 12 homes repeat a tag all 3 cycles, 2.54x state rate), Aperion Care (IL/IN, 33 homes, 1.76x, 22 of 33 repeat, 1.83x) and Eden Senior Care (16 of 19 repeat, 2.2x) lead. It's almost all sprinkler and alarm testing (K0353, K0345), with 0-1 G+ citations per chain. | State inspection intensity is ruled out by comparing each chain with its own states. Building age is NOT ruled out: old buildings draw more K-tags. The top tags are upkeep and paperwork. The big chains sit near 1.0x (Ensign 0.80, PACS 1.15, Life Care 1.04, Genesis 1.03). Arcadia (F-021's worst chain for fines) is 1.06x, so there's no tie to F-021. |
| HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES | 7.0 | probed | In 2024, against their own states, DaVita's deaths ran 1.021x CMS expected (about 650 extra of 31,545), Fresenius 0.965x (about 1,160 fewer of 32,050), and independents were worst at 1.102x. Hospital admissions: 1.020, 0.971 and 1.047. Share of clinics significantly worse on deaths: 2.9%, 2.3% and 5.3%. | The expected counts already adjust for patient mix, so a gap of about 6% is real but small. Chain quality was covered by ProPublica in 2010. Independents are a mix of hospital-based and rural clinics. Mostly confirmed: too small and too known to lead. |
| HEALTH__FED_CMS_NADAC | 6.0 | probed | In 2024, of 308,054 consecutive price steps on same-unit generics, 127 were 2x+ up, only 20 were 3x+ up (7 drug groups, 3 of them OTC), and 542 halved. The real jumps: acetaminophen-codeine solution 30x ($0.0145 to $0.434/mL), hydrocodone-APAP solution 5.6x, naproxen DR 375 mg 4.9x, and saxagliptin 5 mg 4.2x then 4.9x ($1.35 to $6.67/tab). The 2022-23 window isn't in the warehouse. | Makers exiting and shortages (methylphenidate shows at 2x) explain most of it, and generic spikes were big news in 2014-16. The per-unit and package-size fakes are ruled out by requiring the same unit. The 2022-23 part of the angle is unresolved, not empty: those files aren't loaded. |
| HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | 6.0 | probed | High-charge hospitals bill up to 4.39x their state's median for the same DRG (Capital Health Regional NJ: 41 of 46 DRGs at 3x+), but Medicare pays them 0.83-1.24x the median. The hospitals Medicare pays 2-5x the median are public safety-net hospitals: Parkland 5.07x ($44.9M above median), JPS 3.87x, Kings County 2.82x, Jackson Memorial 2.03x ($50.6M). | This fits the data. The high-payment list is exactly the public safety-net list, which is what the teaching, disproportionate-share and outlier add-ons in the payment column predict. That isn't separable with this table, and CMS's method note wasn't re-checked. The charge gaps are the 2013 chargemaster story. |
| ECONOMICS__FED_FAC_SINGLE_AUDIT | 7.0 | live | Lower Brule Sioux Tribe (data match, not verified): going-concern doubt 10 of 10 audit years (2016-2025) and material noncompliance 10 of 10, while federal spending went from $16.7M to $35.7M ($246.2M over 10 years). | Tribal, Medicaid and school money is mostly formula money, so agencies often can't cut it over audit flags. Not ruled out, and that's the story's hinge. The top dollars in going-concern years belong to known cases: Brazos ($24.9B, a student-loan program winding down, where loan balances count as spending), Puerto Rico agencies, and NYC safety-net hospitals (Jamaica 9/9, Wyckoff 9/9). The 80% top-1% share is states, and states are dropped here. |
| CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS | 7.0 | probed | Complaints joined to recalls reproduce known scandals: Jeep fuel system had 8 fatal complaints (25 deaths) filed 13.1 years before the 2014 recall; GM Cobalt 13 fatal complaints 8.8 years early; Takata/Honda 21 fatal 14.7 years early. Nothing new at the top. | A component match is loose: an air-bag death complaint can be a bag that didn't deploy. Lincoln MKS '54 deaths' is one family filing the same 2 deaths 7 times, plus a junk row with DEATHS=40. Tesla Model S suspension's 11 fatal complaints read like one filer posting news links and junkyard listings. Only 41.2% of fatal complaints match any vehicle recall at all. Ford Explorer tires (82 fatal) is Firestone, recalled as equipment, so 'never recalled' is absence, not a finding. Ruled out as a new story. |
| CONSUMER_SAFETY__FED_NHTSA_RECALLS | 6.0 | probed | Mercedes' 28.66B units is really 9.40M. Campaign 21V058000 repeats 1,292,258 units on 18,662 rows (24.1B by itself). The real top is Ford at 94.3M units in 760 campaigns. On re-recalls, Tesla is 24% vs about 3-15% for peers. | Tesla's 24% (81 of 338) comes from four models and software recalls under one component head, and it's widely covered. Subaru is 14.9%, Honda 13.3% (Takata waves), Hyundai 3.8%, Kia 2.9%. Altec's 21 campaigns on 'AERIAL DEVICE' MY2019 is a product category, not one model. The Ford E-350 repeats come from different upfitters. |
| CONSUMER_SAFETY__FED_CPSC_NEISS | 6.0 | probed | E-bikes and mopeds (code 3215, split into 5045+5046 in 2024) went from 21.8K to 87.6K estimated ER visits, 2019 to 2023 (4.0x), while all injuries went 0.95x. Real, but CPSC publishes it. 2024-25 rises can't be trusted: weights reset in 2024 and floors jumped 1.22M in 2025. | CPSC publishes the micromobility rise itself. Not ruled out as 'already known'. Sample design is ruled in: the national total was +18% in 2024 on +7% cases, with average weight in stratum S 74.6 to 106.7 and V 16.9 to 27.6. Floors (1807) went 1.86M to 3.08M in 2025 in every stratum, which looks like a coding change. |
| ECONOMICS__FED_DOL_OSHA_INSPECTIONS | 6.5 | probed | The 'most accident and fatality inspections' list is a California list. CA holds 30,245 of 60,050 type A and M inspections since 2015; Utah is next at 2,529. Inside CA: Sierra Pacific Industries 61, Foster Farms 47, Tesla 43 (18 still open, median 486 days to close). | California uses type A (26,721) where Texas, Florida and New York use M. Likely because Cal/OSHA investigates serious-injury reports too; this table can't prove it. Big employers have more sites. Kaiser's 24 of 36 fall in 2020-21 (COVID). There's no headcount denominator (NR_IN_ESTAB is junk). Not ruled out. Next step is the OSHA 300A join inside CA. |
| HEALTH__FED_CMS_DIALYSIS | 6.5 | live | The triage premise is backwards: the two big chains are at or below average (death rate DaVita 22.11, Fresenius 21.32, all clinics 21.80). The outliers are nursing-home dialysis operators (Dialyze Direct, Concerto, Home Dialysis Services). They run 46 clinics with a median of 1 chair, and 20 of them are rated Worse than Expected on survival (20 of the 38 with a rating), against 2.3% for everyone else. Their weighted death rate is 32.27 vs 21.65. The other independent for-profits still run 7.8% Worse than Expected, and 9 of Maryland's 12 Worse-than-Expected clinics are independent for-profits. | Nursing-home residents are the sickest dialysis patients. Not ruled out: I did not check whether the CMS death-rate model adjusts for nursing-home status, and that is the first thing to read. The chains-vs-independents angle is ruled out, since the two big chains sit at or below the average. |
| HEALTH__FED_CMS_HCRIS | 7.0 | probed | Both triage angles are null in the pool. Across 81 clean switches to for-profit, the median charity change is -0.03 pts, and total charity went up, from $322.0M to $373.5M a year. For FY2022 bad debt vs charity, the median at cost is 0.52 for for-profit and 0.53 for nonprofit. One buyer stands out: at 11 hospitals whose enrollment Prime Healthcare holds, charity fell from $58.1M to $31.4M a year, -1.49 pts net of the same-state trend. Hospitals of the other 58 buyers rose 0.53 pts. The only FY2022 hospital with bad debt at cost over $20M and over 5x its charity is also enrolled under Prime: St. Mary's Regional Medical Center, Reno ($22.7M vs $2.98M). | Charity follows Medicaid expansion, and bad debt is at charges while charity is at cost. The markup artifact is ruled out: the raw bad-debt-to-charity gap (3.72 vs 2.15) vanishes at cost. Expansion is netted out for the pool with a same-state trend, but only partly for Prime (n = 11; NJ's trend fell 0.36 to 3.07 pts over those years). Prime has had press coverage before. |
| FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS | 7.0 | probed | The table can name big sellers ahead of collapses: 987 of 22,770 owner-months with $5M+ sold came before a price at least 50% lower, 4-9 months later. Candidates include Daniel Loeb in Upstart ($712M at $225, later $51), Ernest Garcia II in Carvana ($329M at $353, later $105) and Artal Group in WW ($456M at $76, later $20). But the top of that list is stock splits (Tesla, Walmart, Alphabet). The 10b5-1 plan flag exists only in a 2026-Q1 table that doesn't overlap these trades, and the FDA-recall timing test was small ($78.2M sold before recalls vs $605.8M in the control windows). | 10b5-1 plans can't be ruled out: the AFF10B5ONE checkbox is only in FINANCE__FED_SEC_EDGAR_INSIDERS (filed Jan-Mar 2026), and this table has 2 rows from 2026. Lockup expiries at the 2021 top and the 2022 crash are not ruled out either. The recall angle is ruled out as small: without Walmart it is $76.7M before vs $46.2M in the control windows, mostly Pfizer. |
| HEALTH__FED_CLINICALTRIALS | 6.5 | probed | 706 of 8,234 FDA-regulated US phase 2-4 trials (8.6%) that finished between 2017-01-18 and 2022-06-30 have no results posted as of the 2026-09-04 snapshot, covering 152,850 enrolled patients. Industry misses 9.0%, academic 8.2%, NIH 2.0%. It is a long tail: 537 sponsors, 435 of them missing exactly one. The biggest holders are Brigham and Women's (9 of 35) and UC San Diego (9 of 26). Big pharma is at 0 (BMS 0 of 101, Gilead 0 of 86). | The FDAAA TrialsTracker already publishes sponsor league tables for exactly this, and the per-sponsor counts are small. Not ruled out. Not-regulated trials (59% missing) are excluded because the law doesn't bind them. |
| HEALTH__ADDICTION_PRESCRIBERS_PAID | 6.5 | dead | Indivior paid only $170,922 in 2022 to 2,604 buprenorphine prescribers, and their Suboxone+Sublocade share barely moved (12.0% paid vs 11.1% not paid). The top 20 by maker money are Alkermes-paid psychiatrists and NPs ($41K-$134K, mostly speaker fees), with 0 Vivitrol claims for 15 of 20. The only lift is Vivitrol at 12.0% vs 5.8% among Alkermes-paid prescribers, on $2.77M of money: the known money-follows-prescribing pattern. Also, 37% of the table's $636.0M 'addiction' drug cost is pain drugs. | Volume and specialty drive both the money and the claims: paid prescribers have bigger panels (Indivior median 71 claims vs 37). Alkermes also sells antipsychotics, so its psychiatrist speaker fees are almost surely for those; the Open Payments mart has no product column to prove it. Confirmed rather than ruled out. |
| HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS | 6.0 | live | California's counselors and family therapists turned Medicare down at 2.3x the rate of its psychologists and social workers: 35.8% vs 15.6% opt-out share. 4,890 opted out; 199 billed 11+ Medicare patients in 2024. Nationally, 4.2 counselor/MFT opt-outs per 2024 biller, against 0.54 for psychologists and social workers. The triage premise was wrong: counselors didn't 'leave,' they declined to join when the benefit opened in January 2024. | Not ruled out: first-year ramp. 2024 was the first billing year, and Part B hides billers with fewer than 11 patients, so 3,458 is a floor. Also not ruled out: CA and WA have large private-pay therapy markets, and low Medicare rates are the known cause. Ruled out: opt-out as a first step toward enrolling (only 1 NPI is on both the opt-out list and PECOS), and renewal double-counting (renewals are automatic and add no rows). 99.8% of MHC/MFT opt-outs started 2024 or later; 5,114 in January 2024 alone, down to about 150-210 a month by 2026. |
| HEALTH__FED_CMS_PART_D_PRESCRIBERS | 7.0 | probed | The top opioid and antipsychotic names are volume and specialty artifacts. 292 Part D 2024 prescribers are on the OIG ban list (283 with the last name agreeing), but 291 were banned in 2024 or later, and the one earlier ban (Eduardo Miranda, Laredo TX, 2015, $7.5M of 2024 drug cost) has HAS_WAIVER = True. Non-psychiatrists wrote 78% of antipsychotic claims for patients 65+ (11.1M of 14.2M), which is a known story. | Ruled in: pain practices filed as family or internal medicine (Mackey's opioids are 79% of his claims); nursing-home doctors carry huge volumes; psych-heavy patient panels in PR, Miami and Chicago. Ruled out: rates of 100 on small denominators (ranked on counts and in-band shares, not OPIOID_PRSCRBR_RATE) and suppression junk (antipsychotic flag only '*' or blank, no non-numeric values). 'Banned later' is about 10x the base rate among the top 1,000 long-acting prescribers, but that's only 2 people. |
| HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND | 8.0 | probed | The exclusion angle is dead: $100,322 went to 14 payee lines barred before payment with the city agreeing, and $12.5M in all city-agreed ban matches, out of $135.06B. Relief tracked revenue: short-term hospitals got 7.0% to 8.8% of 2019 net patient revenue across Medicaid quintiles. One lead: Beaver Valley Hospital (Beaver UT, 25 beds) took $22.3M, 2.45x its 2019 revenue, with 40 SNF enrollments under its name. | Ruled in: the revenue formula (flat ratios) and name collisions. For LEIE persons barred before payment, the city differs on 220 of 228. Critical-access hospitals got a median 19.8% of revenue against 8.2% for short-term hospitals: the rural tranche by design. Of the 52 hospitals paid more than 50% of revenue, 33 are critical-access and only 5 have nursing homes under the same name. Match bias: systems paid under a system name miss. |
| HEALTH__FED_FDA_MAUDE | 7.0 | probed | LVADs top the death reports by design: HeartMate 3 1,748 and HVAD 1,242, in a product code where 12.6% of reports are deaths. The one sharp outlier is Nevro's Senza spinal stimulator: 168 death reports on 737 total (22.8%), against 76 on ~42,200 (0.18%) for the rest of its code. None of the 168 flag a device problem, which points at reporting practice. Dexcom has only 7 death reports, so the Dexcom angle is malfunction volume, not deaths. | Ruled in: LVAD patients die of heart failure. Spectranetics Stellarex has 147 of 158 death events before 2020: retrospective paclitaxel trial reports, known since 2019. HVAD batch-filed 98 death reports on 2021-08-20 after sales stopped. Essure's 18,838 injuries (peak April 2020, 5x its median month) are litigation-driven. Only 21 months are loaded (2020-01 to 2021-09). Open: Nevro under-reports everything but deaths, or its peers skip deaths. Spinal stimulators were widely covered in 2023. |
| HEALTH__FED_FDA_DEVICE_ENFORCEMENT | 6.0 | probed | 478 Class I recall events are still Ongoing (1,735 product rows, 199 firms). 64 have been open longer than the 4.6 years that 90% of closed Class I recalls took (median close: 733 days). 14 of the 64 are the HeartWare/Medtronic HVAD pump, which is still implanted in patients. Medline leads on ongoing Class I events (25) once its two name spellings are merged. | Ruled in: implanted devices (HVAD, pacemakers, breast implants) keep a recall 'ongoing' while patients carry them, and FDA closes the paperwork slowly. Kit assemblers like Medline multiply rows. Philips and HVAD are famous. Sensitive: 36 of the 64 started in 2021, right at the cutoff. |
| LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 | 6.5 | live | SpaceX, Ford and Bath Iron Works still ran 2.5-3x their industry peers' injury rates in 2025 (3.12x, 2.47x, 2.67x; in 2024 they were 3.27x, 2.14x, 3.01x). Electric Boat (0.81x) and Ingalls (1.10x) stayed normal. This updates F-035 to F-037; it is not a new find. The deaths and top-rate angles are dead. | Not fully ruled out. The SpaceX name tag pulls in contractors (ABM janitorial, PCAM valet, Performance Contractors) worth 39 of 478 cases and about 5.1M of 50M hours. SpaceX's own 10 sites (EIN 010627671) are 439 cases on about 44.9M hours = 1.96; the own-site peer ratio still needs a rerun. Ford's 2025 filing adds office and engineering sites (52 to 80 sites), so it needs a plants-only rerun. Thin 6-digit pools (481212) fall back to 4-digit. The deaths list is known disasters (Accurate Energetic Systems 16, UPS airline 3, U.S. Steel Clairton 2) plus typos. The top-rate list is NAICS miscodes. |
| TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY | 6.0 | probed | 13,037 tails (4.1%) and 4,319 of 29,000 jets (14.9%) sit with owner-trustees. The sanctions join found 0 confirmed hits. One lead: Aircraft Guaranty Corp Trustee (Oklahoma City) still holds 364 valid, unexpired tails and added 38 new certificates in 2024-26 (6, 18, 14) after 1 in 2021-23. Press reports tie the company to its owner's 2023 cartel-aircraft conviction; that is not verified and no warehouse list names it. | Confirmed for the big trustees: Bank of Utah 1,844, TVPX/NetJets 1,419, Wilmington Trust 623 and UMB 574 are the legal norm for leased and foreign-owned jets, and the Boston Globe covered them in 2019. For Aircraft Guaranty, not ruled out: new owners may run it, or the FAA may already have reviewed it. Southern Aircraft Consultancy re-issued 511 of 514 certificates in 2026 at a shared Casper, WY agent address, which looks like an address move. |
| OPEN_DATA__XC_WAYBACK_DOJ_EPSTEIN | 6.5 | probed | The 'quiet edits' are mostly churn: 163,012 of 173,284 fingerprint changes (94.1%) moved 50 bytes or less, and big changes hit every page on the same days. One real edit: 11 court-record pages whose address carried a plaintiff or party name (Giuffre v. Maxwell, Farmer v. Indyke x2, Bryant/Helm/Davies v. Indyke, Edwards v. Maxwell, L.M./M.J./C.L. v. Epstein, V.E. v. Nine East 71st) were renamed to name-free twins between Feb 22 and Feb 25, 2026. The old addresses answered 404 on Mar 5. | Likely: a privacy scrub. Only 2 of the 11 named addresses (Bryant, Edwards) were saved live (200 on 2026-02-22); the other 9 were only seen as 403 or 404. The pages are listing pages about 12.5K in size, not documents, and 96% of snapshots are data-set 9/10/11 page lists. |
| SCIENCE_RESEARCH__FED_NIH_REPORTER | 6.5 | probed | FY2024 NIH overhead = $9.68B on $26.90B direct (36.0 cents per dollar). The peer median among 69 orgs with $100M+ direct is 38.0 cents. Top rates: Sloan-Kettering 57.6, Scripps 49.4, Boston Children's 48.4. Top dollars: Johns Hopkins $239.8M, UCSF $219.5M, Penn $208.9M. A 15% cap would cut about $5.65B, $140.7M of it at Hopkins. That is real but already published. Parked: the overhead share rose to 37.6% in FY25 and 40.0% in FY26 (partial). | Confirmed. Negotiated rates are public, the cap fight was covered nationally, independent institutes and hospitals are known to run highest, and F-008 already used this table. The cap math uses total direct, not the modified base the real cap used, so the losses are rough. |
| POLITICS__MEMBER_PAC_MONEY | 6.0 | probed | The top 2024 outside-money members are the Senate battlegrounds: Moreno $154.8M (vs $3.1M PAC), Brown $139.7M, Casey $124.8M, McCormick $107.5M, Sheehy $82.1M. Numbers match FEC independent-expenditure lines within 4%. The blank-BIOGUIDE row ($29.3M PAC, $237.6M for, $156.8M against) is an unmatched rollup, not a person. In 2026 so far: Massie $5.66M against vs $90.7K PAC. | Confirmed. Battleground Senate races and leadership dominate (2026 PAC leaders: Guthrie $2.81M, Johnson $2.71M, Jason Smith $2.48M). The blank row matches no single candidate (Trump's lines are $134.8M / $142.2M), so it stays unresolved. |
| IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS | 7.0 | live | 231 LA County hospices sit 3 or more to a street address (59 addresses), and all 231 are still on Medicare's certified list in a 2026 file. LA holds 16% of every US hospice enrollment (981 of 6,066). New lead: 12 hospices named 'CFHC NO4' through 'CFHC NO22, INC.' in San Antonio. 8 were incorporated on 2021-10-07, 6 share one building, and each has its own ASSOCIATE_ID. Data match, not verified. | Partly ruled out. Office buildings do hold many small businesses. No two LA hospices share an exact suite (0), so this is same building, different suites. LA hospice fraud is already reported: LA Times, ProPublica, CMS enhanced oversight of new hospices in CA, NV, AZ and TX. The new parts are that it persists in a 2026 file and the San Antonio CFHC series. The facts.tsv claim of 'one NPI behind 45 enrollments' is false: max is 2 per NPI. |
| JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS | 6.0 | probed | 379 federal judges were assigned 3,650 cases naming a bank they owed money to that year (2003-2021). BofA 1,424, Chase 925, Wells 664. Most are ordinary cards and mortgages, which the recusal law does not treat as disqualifying. The narrow thread: 68 district judges with unusual loans from the bank (investment or rental property mortgages, guaranties, $250K+) on 424 cases naming it. | Mostly stands. Suits against BofA/Countrywide, Chase and Wells filled every district in 2008-15, and cases are assigned at random. Under 28 USC 455, 'financial interest' means owning part of the party; an ordinary loan is not ownership. So unlike F-001's stock, most hits are routine. It also repeats probe 95 (2026-09-05: 831 cases, 150 judges, narrower key). |
| HEALTH__PHARMA_MEAL_CAP_FINGERPRINT | 7.5 | probed | 2024: 47,607 doctor meals at exactly $125.00 and 20,666 at $124.99, against 675 at $126.00 and 192 at $123.99. $125 is a company meal limit, not a law: 28.6% of companies use it in one survey. AbbVie ranks 156th of 502 makers on bunching; it only leads on count. The real spread is between companies of the same size: AstraZeneca 11.1 meals per 1,000 just under $125, Pfizer 0.6. | Stands. The Sunshine Act has no $125 reporting line (the floor is about $13.82). $125 is a common company per-head cap. Big makers top the raw count because of sales-force size. The triage premise that AbbVie leads is rejected. |
| JUSTICE__FED_COURTLISTENER_DISCLOSURE_AGREEMENTS | 6.5 | probed | Judges with pension or payout deals from old law firms: 171 judge-firm pairs across about 160 firms. Only 26 pairs, on 42 published opinions, show that firm as counsel before the judge in the agreement years, and many of those are surname collisions. Most deals are fixed pensions with 'no control'. | Stands. Most firm agreements are fixed or closed pension plans and 401(k)s with 'no control', so the money does not ride on the firm's wins. The count is also small. Many hits are surname collisions: Andrew vs James M. Peck, Broderick in a New Hampshire state court, a different Roberts in D.D.C., William vs Robert Wilkins. |
| HEALTH__NURSING_HOME_RELIEF_BY_CHAIN | 7.0 | dead | The worst nursing-home chains did not take the most Covid relief. Per matched bed, chains under 2.5 stars got $8,193 and 3.5-star-plus chains got $10,692. The highest-fines quartile got $7,991 and the lowest got $9,129. The 'top relief per bed' decile is really a name-match-rate decile: 56% of its homes matched against 6% for the rest. | Stands. Nursing-home relief was paid by formula (per facility, per bed) plus incentive payments tied to infection and death rates, which would favor better homes. $0 means no name match: 68% of the highest-fines chains show $0 against 55% of the cleanest. Chain quality is already covered by F-021 and F-029. |
| JUSTICE__FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS | 6.5 | probed | Outside groups of bankruptcy lawyers and advisers paid for 41.0% of bankruptcy judges' trips in 2011-19 (2,525 of 6,166), against 0.7% for district and appeals judges. Delaware's Kevin Carey reported 200 trips, 22.2 a year against 3.16 for other bankruptcy judges, 25 of them paid by the Turnaround Management Association. No sponsor is tied to a case. | Speaking and teaching for ABI or TMA is permitted and routine, and the disclosures carry no dollar amounts. Not ruled out. Senechal's 75 trips paid by Robert Vogel Law Office are likely wind-down work from her former firm. Not checked. |
| JUSTICE__FED_FJC_IDB_BANKRUPTCY | 6.5 | probed | Delaware holds 46 of the 80 Chapter 11 case families with $1B+ assets filed since 2015 (57.5%), against 3.2% of all families. But 'debt discharged' is not discharge ($196.8B on 4,257 still-pending cases), and 52 of Houston's 58 big families carry under $1M in assets. The dollar venue ranking is dead, and the count version is a known story. | Venue shopping by Delaware, Houston and New Jersey is well covered. The six-snapshot double count was handled by keeping the latest snapshot. The 2.0T and 3.0T maxima weren't chased, because the dollar columns failed first. |
| JUSTICE__INTL_OPENSANCTIONS_DEFAULT | 7.0 | probed | On real sanctions programs only: 0 FAA aircraft-owner hits and 13 contract-recipient name hits, with the country agreeing on 6. Those 6 got $7.5M in contracts, almost all before they were listed. The only money after a listing: NAI Logistics B.V., 13 DoD actions, net $20,647, dated within 3 days of its 2023-12-11 Global Magnitsky listing. | Actions in the days right after a listing are likely close-out paperwork, and the listing press releases may cite these very contracts. Not checked. Name collisions account for the other 7 contract hits and 6 of the 7 PPP hits. |
| LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB | 7.0 | probed | 2024 single-employer pensions hold 108.9% of what they owe in aggregate. 77 of the 1,583 plans owing $100M+ are under 80% funded, $67.1B short in all, and the big names are 79-94% funded. 631 plans report $426.7M in unpaid minimum contributions, but the 248 in real arrears have a median of 8 people. Two mid-size outliers: EIN 822871833, 25.8% funded with $95.4M unpaid, and Transit Management of Southeast Louisiana, $79.5M unpaid. | Big shortfalls sit at big old-industry plans that are already watched: confirmed. Unpaid amounts that equal this year's minimum (201 plans, $160.9M, including NTCA's $131.2M) point to filing before the contribution deadline. |
| LABOR__FED_MSHA_ACCIDENTS | 6.5 | probed | ACNR Holdings' underground coal mines logged 11.10 recordable injuries per 100 current workers a year in 2018-24. Other big coal owners ran 2.24-8.81, and Foresight ran 12.33. Marshall County Mine rose from 80 lost-time injuries (2018) to 150 (2025), steady across the Murray and ACNR owners. But ACNR's fracture and amputation rate (1.33) is middle of the pack: its lead is sprains and strains booked as days away. | Today's headcount understates 2018-20 staffing at the post-bankruptcy owners, which inflates their rates. Not ruled out. More complete reporting looks like more harm. ACNR and Foresight already sit in F-010/B10 for violations. The fix is MSHA's quarterly employment and hours file, which isn't loaded. |

Reports and SQL: `deep/deep-0.md` to `deep/deep-9.md`.

## Triage scores below the deep cut, top 100

The other 399 tables keep their score in `stage_b.json` and in the ledger note.

| table | score | angle | boring |
|---|---|---|---|
| SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS | 6.0 | Which 'SBIR mill' firms win hundreds of small-business research awards without ever selling a product? | Repeat winning is allowed and well reported (SBIR mills); F-022 already worked the Newington address; the 1905 date is bad data. |
| EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION | 6.0 | Which colleges leave students with the most debt relative to what graduates earn? | Debt-to-earnings rankings are widely reported; for-profit and cosmetology schools lead as expected. |
| ENVIRONMENT__FED_EPA_RCRA_VIOSNC_HISTORY | 6.0 | Which hazardous-waste sites have sat in violation month after month for decades? | 96% of rows are Y because the table only lists sites with a violation; long streaks can be paperwork never closed out. |
| ENVIRONMENT__FED_EPA_NPDES_NPDES_SE_VIOLATIONS | 6.0 | Which sewage plants and factories have the most spills and one-off violations; Georgia permits GA0024147 (1.4K) and GA0039012 (1.2K) lead? | Big city sewer systems log every overflow as a separate event, and many are under consent decrees already. |
| JUSTICE__FED_COURTLISTENER_DISCLOSURE_POSITIONS | 6.0 | Federal judges sitting on boards or trusts of organizations that appear as parties in their own cases. | Most positions are family trusts, bar groups and the Federal Judges Association. F-001 already did the stock version. |
| HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS | 6.0 | Who is rolling up rural health clinics: one NPI (1316602774) sits behind 75 clinics. Is it private equity chasing the uncapped RHC payment rate? | Hospital systems legitimately run many clinics under one NPI. KY and TX lead because they are rural. |
| ENVIRONMENT__FED_EPA_ECHO | 6.0 | Which facilities keep failing inspections for years (quarters in noncompliance) and never get fined? | TOTAL_PENALTIES repeats shared-case penalties per facility (F-013) and the SNC flag is a constant; the $1.7B top is one global settlement copied onto sites. |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS | 6.0 | Which plants fail smokestack tests again and again and keep operating without a penalty? | Failures are often retests the same week; bad dates (year 0201) show dirty entry. |
| HEALTH__FED_DEA_ARCOS | 6.0 | Which distributors and pharmacies shipped per-capita pill volumes far beyond their towns, beyond the famous Kermit WV pharmacies? | The Washington Post published this exact data in 2019, and F-002 already uses it for counties. Top buyers are often hospital or long-term-care pharmacies serving many patients. |
| HOUSING__FED_HUD_MF_FIRM_COMMITMENTS | 6.0 | Which lenders and which cities drew the most federal mortgage insurance on apartments, and how much went to NYCHA PACT privatization deals? | Big NYC buildings (Co-op City, PACT) top the list because they are the biggest projects. The share per row is flat: top 1% hold only 8%. |
| HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS | 6.0 | How many rural subsidized apartments lose their affordability protection as USDA mortgages mature, and where? | The expiring-mortgage problem is known in housing-policy circles. Some dates are sentinels (1933 and 2098). |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_EVENTS_MILESTONES | 6.0 | Which water systems serving the most people have no lead pipe inventory (LSLI) or PFAS test on file, past the federal deadlines? | States report milestones late or not at all to EPA, so a missing event means the state never sent it, not that the system missed the deadline. |
| FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES | 6.0 | Which outside groups poured the most into House races they lost, or into primaries against their own party? | Super PAC spending is watched closely by OpenSecrets and the press. Totals are driven by a few presidential and Senate races. |
| FCT_LIBRARY_SNAPSHOT | 6.0 | Which of the 619 Epstein files vanished or changed after first being seen, and when? | A file 'vanishing' may be a URL rename or a crawler gap. SOURCES_OBSERVING tops out at 2. |
| POLITICS__IRS527_DIRECTORS_OFFICERS | 6.0 | The same few people and law-firm addresses run hundreds of 527s: who sits as officer on the most political groups? | Addresses like 455 Capitol Mall are compliance law firms and treasurer services; being officer of many groups is a routine service job. |
| CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS | 5.5 | Which makers had the most defect probes that closed without a recall, and how long did they stay open? | Takata air-bag probes explode row counts across every make and model; one probe covers thousands of model-years |
| ENERGY__FED_EIA861_SALES_ULT_CUST | 5.5 | Which utilities charge households the highest price per kWh, and how far above the state average? | Big utilities lead on revenue because they're big; price gaps are known (Hawaii, California) and regulated. |
| ECONOMICS__FED_IRS_AUTO_REVOCATIONS | 5.5 | Did nonprofits that lost tax-exempt status still take federal grants or PPP loans afterward? | 1.2M revocations are mostly dead small groups (alumni chapters); many were reinstated later. |
| POLITICS__FEC_COMMITTEE | 5.5 | Which treasurers run hundreds of PACs, and do those PACs raise money but spend little on candidates (scam-PAC pattern)? | Pro treasurers (Datwyler, Kilgore) are compliance firms serving many clients; scam PACs have been reported since 2019. |
| CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS | 5.5 | Which US officials, contractors or Medicare providers appear as officers of offshore entities? Join to US names in Ripple. | Name collisions are rampant (single-word trap); 'THE BEARER' rows are anonymous shares; ICIJ already published the famous names. |
| JUSTICE__FED_FHFA_SUSPENDED_COUNTERPARTIES | 5.5 | Mortgage fraudsters banned by FHFA: are any still licensed or lending, or got PPP/SBA loans after the ban? | 241 rows, mostly individuals already convicted; name matching is weak. |
| JUSTICE__RACIAL_JAIL_DISPARITY | 5.5 | Which named counties jail Black residents at 10x+ the white rate, and did that gap widen after 2015? | Vera's data, already widely covered. The 2.1M max rate is a tiny-denominator artifact, and only 57% of rows are filled. |
| HEALTH__FED_FDA_DEVICE_PMA | 5.5 | High-risk devices changed by 30-day notice (no FDA review) that were later recalled: which makers lean hardest on the no-review path? | 30-day notices are meant for routine manufacturing changes. Medtronic tops the list because it holds the most PMAs. |
| POLITICS__TX_LOBBY_FOOD_BEVERAGE | 5.5 | Which Texas officials ate the most on lobbyists' tab, and who paid? There is a $78.7K single row. | 71% of rows only give ranges; a median of $28 means mostly routine lunches. Small money. |
| ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS | 5.5 | Which gas pipeline operators leak the most gas and have repeat serious incidents? Look past PG&E's famous San Bruno blast. | This is transmission and gathering lines only, 2.0K rows. PG&E's 10 deaths are almost all San Bruno 2010, already widely covered. Big operators have more pipe. |
| ENVIRONMENT__FED_EPA_NPDES_NPDES_CS_VIOLATIONS | 5.5 | Which sewer and industrial dischargers have missed court-ordered cleanup deadlines for decades? Tennessee permits lead the list. | COMP_SCHEDULE_NMBR is a sequence number, not a count of violations, so the Tennessee sums mean nothing. Many misses are paperwork deadlines. |
| EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS | 5.5 | Which US political advertisers micro-target by age and gender, and which dark-money groups outspend candidates on Google? | Spend is given in ranges. BJP and presidential campaigns dominate on volume, and this is a public transparency report. |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_SITE_VISITS | 5.5 | Which drinking-water systems went years without the sanitary survey the rules require every 3-5 years, and how many people drink from them? | State reporting to EPA is patchy, so a missing survey can be a missing upload. The 1900 dates are placeholders. |
| SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE | 5.5 | Which institutions and journals have the most paper-mill retractions, and did their authors keep getting federal grants? | Mass journal retractions (Hindawi and others) inflate the counts. Retraction Watch already reports it, and F-008 covers retractions against NIH money. |
| JUSTICE__FED_COURTLISTENER_DISCLOSURE_SPOUSAL_INCOME | 5.5 | Judges whose spouses draw income from law firms or companies that appear before them. | Most spouse lines are 'self-employed attorney' with no firm named. The disclosure data covers 2021-23 only. |
| HEALTH__FED_HHS_OIG_LEIE | 5.5 | Banned providers still getting paid: excluded people in Medicare billing, Relief Fund, or other federal money. | F-020 already did the Open Payments cut; 90% missing NPI makes matches noisy; many are reinstated or nurses aides. |
| HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 5.5 | Which chains get cited for severe harm (scope/severity G+) repeatedly and never pay? | F-021 and F-029 already mined nursing-home chains and abuse flags; state survey intensity drives counts. |
| JUSTICE__FED_CONSOLIDATED_SCREENING_LIST | 5.5 | Blacklisted firms (Entity List, SDN) that still got US federal contracts, grants, PPP, or FDA device registration. | Name collisions; Chinese subsidiaries use different names; many listings are foreign with no US ties. |
| JUSTICE__FED_COURTLISTENER_DISCLOSURE_GIFTS | 5.5 | Which judges took the most gifts and from whom (bar groups, law firms, billionaires), and did they hear those donors' cases? | Most gifts are small bar-dinner items; ProPublica covered Supreme Court gifts heavily; 2021-23 only. |
| ECONOMICS__FED_PBGC_TRUSTEED_PENSION_PLANS | 5.5 | Which companies dumped the biggest pension plans on the federal insurer, and did those same firms keep winning federal contracts or pay executives well afterward? | The biggest trusteed plans are famous bankruptcies: airlines like United and US Airways, steelmakers like Bethlehem and LTV, and Delphi. These are well covered. The median plan has 11 people. |
| HEALTH__FED_FDA_DRUG_ENFORCEMENT | 5.5 | Which drugmakers rack up repeat Class I recalls, and do the same firms keep selling to Medicare and the VA? | Big generic and injectables makers (Hospira, Sun) recall more because they make more products. Many recalls are lot-level sterility issues. The manufacturer field is mostly empty. |
| ENERGY__FED_EIA861_RELIABILITY | 5.5 | Which utilities left customers in the dark longest in 2024? Altamaha EMC averaged 17,300 minutes, about 12 days, per customer. | The top outage numbers are almost certainly Hurricane Helene co-ops in Georgia and North Carolina. The storm is the story, not the utility. |
| FINANCE__FED_FEC_BULK_COMMITTEES | 5.5 | Scam PACs: one treasurer (Datwyler, 343 committees) and one Woodbend Dr address (204 committees) run hundreds of committees. Is that a PAC mill that raises money and spends it on itself? | Thomas Datwyler is a known compliance-service treasurer, and 1742 Woodbend Dr is likely a filing-service address. Those are legitimate vendors serving many small committees. Scam PACs have been covered but still recur. |
| HEALTH__FQHC_SITE_PEOPLE | 5.5 | Are federally excluded clinicians listing practice addresses at community health centers that run on federal grants? | This is an address match, not a staff roster, so a hospital-campus address sweeps in thousands of people. PEOPLE_AT_SITE repeats on every row (7.5K max). Known trap: 'FQHC staff is an address match.' |
| ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY | 5.5 | Which water-discharge permit holders have been in significant noncompliance quarter after quarter for years? | Violation codes are letters that need the EPA code key. Small municipal plants dominate chronic noncompliance. Known trap: the ECHO SNC flag is a constant. |
| FINANCE__SENATE_TRADES | 5.5 | Which senators traded stocks in companies before hearings or bills their committees handled, 2021-26 (beyond the 2012-20 bank finding)? | Sponsors were matched by last name only (14.8K of 15.2K rows), so senators who share a surname can be mixed up. Perdue and Tuberville are already notorious. F-009 already used this table. |
| JUSTICE__INTL_OPENSANCTIONS | 5.5 | Do sanctioned companies or people show up in US contracts, PPP loans, UK company filings or SEC filers? | 71K rows is a slice, not the full set. Single-word names collide (known trap: 8% real). About 1K crypto-wallet rows are noise. |
| POLITICS__TX_LOBBY_ENTERTAINMENT | 5.5 | Which Texas officials got the most entertainment from lobbyists, and from which industries? | Only 2.8K rows and $85K exact. Texas reports amounts as ranges, and most outings are $150 dinners. |
| HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT | 5.5 | Homebuilders' own mortgage arms (DHI, Lennar) lead FHA lending. Do their borrowers pay higher rates or buy at higher prices than borrowers at other lenders? | Builders buy down rates on new homes, so their numbers look different for known reasons. This is one month of loans. |
| JUSTICE__XC_UK_SANCTIONS_LIST | 5.5 | Shadow-fleet tankers under UK sanctions: which ones still call at ports or hold US-linked owners? | Sanctions lists are well covered. On its own this is a reference list with no money or harm counts. |
| HEALTH__FED_CMS_HOSPICE | 5.5 | How many new hospices were certified in LA County and Arizona after 2019, and how many share one address or one owner? | The LA hospice fraud surge is already a big ProPublica/LA Times story, and CMS has named it. |
| HEALTH__FED_FDA_CAERS | 5.5 | Which named supplements and cosmetics drew the most serious reports (deaths, hospital stays), and did the MoCRA law in 2022-23 change reporting? | Reports are voluntary and spike with news coverage and lawsuits (hair relaxers, kratom). Counts are not rates. |
| FINANCE__FED_SEC_13F_HOLDINGS | 5.0 | Which fund managers hold the stocks of companies members of Congress oversee, or which filers report impossible values? | $16.9 quadrillion total means value units changed in 2023 (thousands to dollars) and typos; the story is data error, not wealth |
| POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS | 5.0 | Which Canadian donors give over the legal cap, or give to multiple parties, and where does the $8.5M single line come from? | Big lines are party-to-riding transfers, not donors; name spellings split the same person |
| ENVIRONMENT__FED_EPA_NPDES_NPDES_PS_VIOLATIONS | 5.0 | Which sewer plants and factories missed Clean Water Act construction deadlines for decades without penalty? | Missed report deadlines are paperwork; municipal sewer consent decrees routinely slip |
| JUSTICE__XC_VERA_INCARCERATION_TRENDS | 5.0 | Which rural counties grew jail populations fastest per capita while crime fell, and by race? | Well-worn Vera finding already published by Vera and NYT; counties holding state or ICE detainees inflate rates |
| JUSTICE__FED_FJC_IDB_CIVIL | 5.0 | Who files the most federal civil suits (serial plaintiffs, the US government) and how often each case type ends with money? | Amounts are in thousands and capped at 9,999 (known trap), so the money columns are ceilings; top plaintiffs are common surnames and USA. |
| HEALTH__FED_VA_SUICIDE_STATE | 5.0 | Which states have the highest veteran suicide rates, and where are rates rising fastest? | Mountain West leads, tracking gun ownership and rurality; VA publishes this chart yearly; general-population comparison columns are empty. |
| ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | 5.0 | Which named power plants put out the most CO2 or NOx per megawatt-hour, and do they sit in poor or majority-Black counties? | Old coal plants are dirtiest per MWh; that is widely known and already mapped by EPA itself |
| HEALTH__FED_FDA_DEVICE_510K | 5.0 | Which cleared devices were later recalled Class I, and which 'predicate' devices spawn the most recalled descendants? | The 510k predicate loophole is well reported (ICIJ Implant Files); big makers have the most clearances and so the most recalls |
| HOUSING__FED_MAPPING_INEQUALITY | 5.0 | Do D-graded redlined neighborhoods today host more polluting plants, denied mortgages or nursing-home closures? | FIPS is blank on every row so it needs a geometry join; redlining-to-today stories have run many times |
| ENVIRONMENT__FED_NOAA_STORM_EVENTS | 5.0 | Which counties keep getting hit by deadly storms, and do federal disaster dollars follow the deaths? Heat and flood deaths may outrun tornadoes. | Deaths pile up in a few famous disasters (Joplin 2011, Katrina); 88% of injuries under a 'None' county name is a load artifact, not a place. |
| ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS | 5.0 | Which facilities report the most toxic air pollutants (e.g., ethylene oxide, benzene) next to homes, and whose emissions rose? | Big emitters are big plants; EPA's own TRI and EJScreen already publish these rankings. |
| JUSTICE__XC_RANSOMWARELIVE_VICTIMS | 5.0 | Which hospitals, school districts and local governments were posted by ransomware gangs, and did they disclose or report to HHS? | Leak-site victim lists are published by ransomware.live itself; top entries are big-name companies scraped from old lists. |
| FINANCE__FED_SENATE_EFD_PTR | 5.0 | Senators trading stocks in industries their committees oversee, 2020-2026; Tuberville and newcomer Armstrong lead volume. | Senate trading is a famous story and F-009 already did the committee angle. |
| POLITICS__TX_LOBBY_TRANSPORTATION | 5.0 | Which Texas officials took the most lobbyist-paid trips, from whom, and did the payers get bills or contracts? | Small volume; trips to conferences are routine and the TEC data is used by Texas Tribune. |
| HOUSING__FED_HUD_MF_SECTION8_CONTRACTS | 5.0 | Which private owners get HUD contract rents far above local fair market rent? The ratio reaches 472% of FMR. | High ratios are usually elderly or special-needs buildings, or mark-up-to-market renewals set by rules. F-024 already used Section 8. |
| JUSTICE__FED_FBI_CDE | 5.0 | Which states solve the smallest share of murders and violent crimes, and how far has that fallen since 1985? | Falling clearance rates are well reported nationally, and the NIBRS switch in 2021 broke state reporting coverage. |
| POLITICS__FED_EAC_EAVS | 5.0 | Which local election offices reject the most mail or provisional ballots? | Only 6.5K rows with Wisconsin heavy (1.9K), so it looks like a partial or single-cycle load. Rejection rates follow state law. |
| ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST | 5.0 | Which operators and counties use the most water per frack job, and in drought basins? | The TVD leaders (J Cleo Thompson at 2.1B feet) are typos, not deep wells. Water per well grows with lateral length, a known industry trend. |
| TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT | 5.0 | Which commercial or charter operators (FAR Part 135 and 121) have repeat accidents, and are those planes still registered and flying? | Half the rows have no operator name. Most accidents are private Part 91 flights by one-off pilots. Southwest's 77 is a small number for its fleet size. |
| ECONOMICS__INTL_GLEIF_REPEX | 5.0 | Which US-linked entities in the global company-ID register refuse to name a parent, and do they cluster at shell-registration addresses or near sanctioned names? | NATURAL_PERSONS just means a person owns it, which is true for most small firms. Each LEI appears twice by design, once for the direct parent and once for the ultimate parent. |
| TRANSPORT__FED_NTSB_AVIATION_EVENTS | 5.0 | Which operators or airports have repeat fatal accidents (tour helicopters, skydiving planes, medical flights), and are they still flying? | The ground-injury columns are 10% filled and dominated by a few big crashes, such as the 2008 Manas crash. Most events are single private planes. |
| FOREIGN_INFLUENCE__FED_FARA_BULK | 5.0 | Which US firms and ex-officials work for which foreign governments, and which principals spend the most on DC influence? | 97% of PERSON_NAME and 92% of FOREIGN_PRINCIPAL are blank because the four files do not share columns. OpenSecrets already covers FARA. |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES | 5.0 | Which states stopped inspecting major air polluters, and which big emitters went 5+ years with no full evaluation? | Inspection frequency is negotiated state by state. Year 0025 dates are typos. |
| HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY | 5.0 | People FHFA barred from mortgage business who still show up as loan officers, NMLS licensees or federal contractors. | Most are individuals already convicted of mortgage fraud; F-015 showed name matches against exclusions are thin. |
| JUSTICE__INTL_UK_SANCTIONS_LIST | 5.0 | Which UK-sanctioned people, firms or ships are not on the US list, or still hold US companies, contracts or ship calls? | UK and US lists overlap heavily; gaps usually reflect different timing, not loopholes. |
| FINANCE__FED_PCAOB_FORM_AP_FILINGS | 5.0 | Audit partners signing hundreds of public-company audits a year, or partners behind many later-restated or fraud companies. | Big fund-complex audits give one partner hundreds of funds legitimately. |
| LABOR__FED_PBGC_TRUSTEED_PLANS | 5.0 | Companies that dumped pensions on PBGC and then won federal contracts or paid executives big, or repeat dumpers by EIN. | Terminations follow bankruptcies; repeat EINs are one company with several plans. |
| HEALTH__FED_CMS_HOSPITAL_COMPARE | 5.0 | Do 1-star hospitals still pull top Medicare dollars or pay executives well? The star rating works as the outcome to join nonprofit and Medicare money against. | Low ratings track poor, safety-net patient mix. Star ratings are widely covered. 41% of hospitals have no rating. |
| ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS | 5.0 | Which states almost never find violations in their hazardous-waste inspections, compared with EPA inspecting the same kind of sites? | EPA targets its inspections at known bad actors, so its hit rate is higher by design. State inspections include routine record reviews. |
| HEALTH__FED_HRSA_SHORTAGE_AREAS | 5.0 | Which counties have been marked short of doctors for decades without the gap closing, and how much federal clinic money went there? | Rural shortage is a chronic, well-known condition. Designations persist because they unlock funding. 36K rows have a score of 0. |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | 5.0 | Where are big populations served by systems owned by private or for-profit operators, and do those systems have more violations? | A roster is a denominator. Most rows are inactive or tiny wells, and the 9M max rows are wholesalers that double count downstream systems. |
| JUSTICE__COUNTY_DOUBLE_BURDEN | 5.0 | Which counties sit in the worst tenth for both overdose deaths and jailing, and are they getting opioid settlement or treatment money? | This table is our own build and overlaps F-002 (pills vs overdoses). Rural Appalachia tops both lists for known reasons. |
| CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS | 5.0 | Which US federal contractors, insiders or donors show up as officers of offshore companies? | This is ICIJ's own data, already reported to death. Name matches are noisy: single-word matches are only 8% real. |
| POLITICS__TX_LOBBY_COVER | 5.0 | Which Texas lobbyists and clients spent the most by category over 30 years, and who spiked during key sessions? | Cover sheets are totals only. Spending follows the two-year session cycle, and Texas Municipal League types dominate. |
| INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING | 5.0 | Did DOJ quietly pull or change Epstein disclosure links between archive captures? | Page links churn with site redesigns. The Epstein file releases are heavily covered. |
| POLITICS__IRS527_8872_REPORTS | 5.0 | Which 527s take in a lot and spend it at once, or sit on money? Compare Schedule A in vs Schedule B out, per group per cycle. | These are the Schedule A/B tables rolled up again; the $13.3B matches the Schedule B table exactly. Amendments double-count periods. |
| FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS | 5.0 | Which facilities get inspected over and over with no enforcement after, and which regions barely inspect at all? | The top registry IDs (2,200 inspections) are probably multi-permit sites or stormwater programs. The 0201 date is a typo. |
| FINANCE__FED_FEC_COMMITTEES | 4.5 | Treasurers running hundreds of committees from one P.O. box, scam PAC networks | Compliance firms legitimately serve as treasurer for many committees; rows repeat per cycle (442 copies) |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES | 4.5 | Clean Air Act facilities marked in violation for years, by county and industry | Mostly small oil wells and dry cleaners; status field needs history table for duration |
| IMMIGRATION__FED_DOL_OFLC | 4.5 | Which H-1B employers file the most applications at wages below the local prevailing level, and do outsourcers dominate? | Cognizant, Infosys and Tata topping H-1B lists is a long-running, widely reported story; data is mostly 2018-19 |
| ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS | 4.5 | Which facilities got the most warning letters without ever getting a formal action or fine? | Sewage plants get routine letters for paperwork; 92% are state actions with uneven reporting |
| FCT_WAYBACK_PAGE_CHANGES | 4.5 | Which Epstein-related government pages were quietly edited or pulled (turned 404/403) and when, relative to news events? | Most changes are template tweaks, CDN errors (503) and archive fetch hiccups, not deliberate takedowns. |
| CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ADDRESSES | 4.5 | US addresses tied to offshore entities: which US cities or single buildings host the most leak-linked people? | ICIJ has mined this for years; clustering at registered-agent addresses is expected. |
| CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE | 4.5 | Mass-registration addresses and nominee directors: single UK addresses hosting thousands of companies with no accounts filed. | Formation-agent addresses legitimately host thousands; F-028 already did one Manchester version of this. |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS | 4.5 | Plants that self-certify permit deviations year after year: who admits breaking their air permit most, and are they penalized? | 57% of flags are null. Deviations are often small monitoring gaps, and reporting them is the system working. |
| PROCUREMENT__INTL_EC_SERCOP | 4.5 | Which companies won Ecuador's biggest public contracts in 2025-26, including one $4.8B contract value? | Foreign story with a small US audience. The $4.8B is likely a unit error, and contract value is only 10% filled. |
| HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER | 4.5 | Denominator: Medicare inpatient payments per hospital, which can scale charity care (F-003) or executive pay. | The biggest hospitals (NYU and friends at CCN 330101) get the most money because they are big. There is no story in the size alone. |
| FINANCE__FED_EPA_ICIS_FEC_CASE_ENFORCEMENT_CONCLUSION_FACILITIES | 4.5 | Bridge from EPA enforcement cases to facilities. It could show one case settling for thousands of sites. | Nationwide consent decrees list every site. Texas and New York lead because they have the most facilities. |
| HEALTH__FED_FDA_PURPLE_BOOK | 4.5 | Which biologics have approved biosimilars but still show high spending, suggesting the biosimilars are not being used? | Biosimilar uptake is slow for known reasons, like rebates and patents, and that is widely covered. |
| POLITICS__FED_FEC_PAC_SUMMARY | 4.5 | Which committees raise the most and spend it on overhead instead of candidates (scam PACs)? | C00401224 is ActBlue, a pass-through conduit. Big totals are the parties and conduits everyone already knows about. |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_PN_VIOLATION_ASSOC | 4.5 | Water systems that broke the rules and then also failed to tell residents; West Virginia systems 3305535/3305527/3305536 lead. | Code 03 is often a paperwork monitoring or reporting failure, not contamination. Small systems rack up counts per quarter. |
| HEALTH__FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | 4.5 | Which hospitals get paid far above peers for the same outpatient service group? | Payment is set by APC and wage index, so gaps are mostly geography; 45% of payment cells suppressed. |
| HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS | 4.5 | Home health agencies bunched at one address or registered in waves (LA County fraud hotspots). | Home health fraud in LA is a known story; shared office parks are normal. |

## Data traps from battery A

61 in `traps.tsv`: 46 empty columns, 8 constant columns, 7 nine-nines ceilings. The ones that bite:

- Google political ads creative stats: SPEND_USD empty on all 1.56M rows
- Foreign assistance: OBLIGATION_AMOUNT and DISBURSEMENT_AMOUNT empty on all 95,658 rows
- IRS 990 holds 200 rows, USAspending API 300, Grants.gov 100, EPA Envirofacts 5,000: samples, not files
- OSHA inspections NR_IN_ESTAB tops at 9,999,999,999; NHTSA complaint MILES at 9,999,999; SDWA service connections at 9,999,999
- FJC civil AMOUNT_DEMANDED and AMOUNT_RECEIVED top at 9,999: thousands-of-dollars sentinel
- Clinical trials NPI empty on all 601,694 rows
- FEC committees dim CYCLE is 2026 on every row

## Completeness skeptic: DISAGREES

Fresh-context skeptic, files only. Verdict: narrowed on "nothing beats the best", broken on "the menu is complete".

- The judge's verdict contradicts its own menu: the 527 lead (#3) and OSHA 2025 (#4) rank above F-002 (#6). Reworded: no single table beats F-032 or F-033; two beat F-002.
- Triage buried the tables behind all three tier-A findings: COURTLISTENER_FINANCIAL_DISCLOSURES 2.0 (F-001), CDC injury county 4.5 and ARCOS 6.0 never deep-queried (F-002), XWALK_HOSPITAL_CCN_EIN 1.5 (F-003). Single-table triage cannot see join stories.
- 15 of 65 tables scoring 6.0+ never got a deep pass: ARCOS, ECHO, FEC independent expenditures, IRS527_DIRECTORS_OFFICERS among them.
- 36 deep results marked probed were never ranked on the menu. Example: bankruptcy lawyers paid for 41.0% of bankruptcy judges' trips, against 0.7% for other judges.
- Battery blind spots: 168 tables with no actor column, ~180 whose actor is a bare ID code, 311 with no number column, ~75 whose lead number is not a quantity, 261 with a date column but no trend measured, 64 stubs of 300 rows or fewer.
- Below-cut tables worth a look: FARA_BULK, DOL_OFLC wages, CMS home health enrollments, COURTLISTENER gifts and spousal income, ransomware victims, FDA CAERS, FDA device PMA, PBGC trusteed plans, EPA air emissions combined, IRS527_8872_REPORTS.
- Scope: pairs 3,188 untouched, hops 2,717, place 1,548, names 348. All three tier-A findings came from those join layers.
