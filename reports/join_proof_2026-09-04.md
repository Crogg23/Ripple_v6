# Proof the joins pay: three cross-source tests, 2026-09-04

Chris's ask, verbatim: "prove to me that my data warehouse was worth all this build by actually
finding something interesting that we can only do because of the joins and modeling of it"

All queries through the Python door, LIBRARY_RAW.LANDING, run 2026-09-04. Both CMS tables are program year 2024.

## Finding 1 — pharma money and prescribing move together, inside the same specialty
Join: FED_CMS_OPEN_PAYMENTS (15.35M payments, $2.65B, PY2024) × FED_CMS_PART_D_PRESCRIBERS (1.42M prescribers, $288B, 2024) on NPI.
Filter: individual prescribers with 100+ claims. Physician-type recipients only.

Whole population, by pharma dollars received:
| band | prescribers | brand share | cost per claim | opioid rate |
|---|---|---|---|---|
| none | 388,888 | 16.6% | $141 | 5.99 |
| <$100 | 154,690 | 14.8% | $158 | 7.35 |
| $100–1k | 265,601 | 17.6% | $224 | 6.34 |
| $1k–10k | 104,833 | 19.2% | $403 | 6.45 |
| $10k–100k | 14,784 | 24.3% | $890 | 8.53 |
| $100k+ | 2,431 | 25.7% | $1,047 | 7.83 |

Within specialty, none vs $10k+ received. Mean and median cost per claim:
| specialty | n none | n big | mean none | mean big | median none | median big | brand none | brand big |
|---|---|---|---|---|---|---|---|---|
| Nurse Practitioner | 79,028 | 869 | $119 | $1,052 | $60 | $435 | 12.7% | 24.0% |
| Internal Medicine | 52,036 | 782 | $136 | $1,152 | $79 | $378 | 14.9% | 29.3% |
| Family Practice | 53,125 | 320 | $82 | $267 | $76 | $122 | 12.4% | 19.9% |
| Physician Assistant | 41,398 | 457 | $87 | $819 | — | — | 11.2% | 19.5% |
| Psychiatry | 10,486 | 422 | $100 | $294 | — | — | 5.7% | 11.5% |
| Optometry | 3,785 | 159 | $108 | $751 | — | — | 33.7% | 54.3% |
| Cardiology | 3,163 | 928 | $237 | $580 | — | — | 17.6% | 22.7% |

What was checked: sum of Open Payments dollars per NPI, joined to Part D cost and brand claims per NPI.
What a hit means: prescribers paid $10k+ by manufacturers write 7x costlier scripts than unpaid peers of the same type.
What a miss would mean: flat cost across bands. It is not flat in any of 12 specialties.
Caveat: correlation. Specialty label is coarse; an oncology NP is still "Nurse Practitioner". Sub-specialty control is the next cut.
Why only the join: Open Payments has no prescribing. Part D has no payments. NPI is the only bridge.

## Finding 2 — 22 debarred firms got 99 paid contract actions while debarred
Join: FED_SAM_EXCLUSIONS_FULL_R2 (firms with a UEI) × FED_USASPENDING_CONTRACTS_FULL_R2 on UEI.
Filter: action date between exclusion active date and termination date, obligation > 0.
Result: 22 vendors, 99 actions, $1,858,825, 2011–2026.
Top: QUANTELL INC $402,659 DoD 2014–15; Monbo Group $359,607 DoD 2023; A&S Skill Machinist $150,474, 18 DLA actions 2023–25.
Colour: Glenn Defense Marine Asia, the Fat Leonard company, got 2 Navy actions for $18,258 six days after exclusion.
Caveat: some actions are de-obligation reversals or contract closeouts on pre-existing awards; each needs a read.
Why only the join: SAM never sees the money. USAspending never sees the ban.

## Finding 3 — TRAP, not a finding: "revoked nonprofits still funded"
Join: FED_IRS_AUTO_REVOCATIONS × FED_FAC_SINGLE_AUDIT (EIN→UEI bridge) × FED_USASPENDING_ASSISTANCE_FULL.
Result: 223 orgs, $13.4B after revocation. Top: Metropolitan Transportation Authority $11.8B, Standing Rock Sioux Tribe, Peoria Housing Authority.
Why it's a trap: governments and tribes get auto-revoked because they never had to file a 990. Revocation means nothing for them.
Real version needs a filter: exclude government units, tribes, housing authorities, then re-run. Not done today.

## Cost
Nine queries, largest scanned 93M contract rows and 15M payment rows. No prior run of this pattern in the query log to price against.

## Skeptic verdict, same day
- 7x is the best row, not the rule. Range is 1.6x Family Practice to 7.25x NP by median.
- Brand share moves 12.7%→24%; that cannot make a 7x gap. Drug mix is the lead explanation. Makers pay who already writes biologics.
- ProPublica Dollars for Docs published Open Payments × Part D years ago. "Only the join" is true; "only this warehouse" is not.
- Finding 2: UEI did not exist before April 2022. The 2011–2015 matches ride a backfilled DUNS→UEI map, unvalidated. Mods on pre-existing awards are lawful.
- "Not flat in any of 12 specialties" was written from the mean table; medians shown for 3 only.
Both verdicts go to Chris.
