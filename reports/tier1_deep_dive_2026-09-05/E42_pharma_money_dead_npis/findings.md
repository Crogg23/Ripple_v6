# E42 — Is drug industry money still being sent to switched-off NPIs?

Deep dive, 2026-09-05. Python door only. Scripts: `queries.py`, `queries2.py`; log: `queries.log`; page: `story.html`.

**Short version:** yes, $4,187,435 in PY2024, and the first pass reproduces to the cent.
But it is not drug money and it is mostly not "still being sent." It is device-maker royalties that never stopped,
to eight surgeons whose NPIs were switched off between 2014 and 2023, plus one $50k practice acquisition. One person in the ten
is different: an optometrist paid $538k for speaking and consulting after his NPI went dark. The other 1,315 NPIs split $252k, mostly lunches.

---

## What was checked

| Step | What | Result |
|---|---|---|
| Cohort | NPPES rows with a deactivation date and no reactivation date | 346,179 NPIs (18,423 more were deactivated then reactivated) |
| Rebuild | Open Payments PY2024 rolled up per NPI per day first, then joined, payment date strictly after deactivation | **1,325 NPIs, $4,187,435.11, 2,729 transfers; 1,224 paid 90+ days after** — matches the first pass exactly |
| Top 10 | per-NPI after-deactivation total, ranked | $3,935,240 = 94.0% of the money |
| Nature | for the ten and for the rest | ten: royalty $3,347,030 (9 NPIs carry some royalty; 8 are royalty-only), speaking $451,125 + consulting $87,000 (1 NPI), acquisition $50,000 (1 NPI), food $85 |
| Dates | deactivation vs first and last 2024 dollar, for each of the ten | gap 84 days to 3,520 days; 8 of 10 over a year, 6 of 10 over four years |
| Prior years | same ten in the PY2023 and PY2022 files | all ten paid in at least one prior year by the same payers; 8 of 10 in both |
| Reactivated? | NPI_REACTIVATION_DATE, REPLACEMENT_NPI on the ten | null and blank on all ten |
| New NPI? | live type-1 NPPES row, same first + last name + state | 2 of 10 have one, both in the wrong specialty (dentist; gastro/OB-GYN/paediatric dentist) |
| Reason? | NPI_DEACTIVATION_REASON_CODE | blank on all ten and on all 346,179 |
| Reason proxies | OIG LEIE, SAM exclusions, Part B 2024 billing | 0 of 10 on any of the three |
| Reactivated window | NPIs deactivated then reactivated, paid inside the window | 35 NPIs, 65 transfers, $14,666 — nothing |

## The ten

| # | Name | State, specialty | Deactivated | First 2024 $ | Gap | Payer | Nature | PY2024 $ | PY2023 $ | PY2022 $ |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Spetzler | AZ, neurosurgery | 2018-11-07 | 2024-01-25 | 5.2 y | Stryker | royalty | 1,791,118 | 1,795,003 | 1,972,468 |
| 2 | Geller | CA, optometrist | 2023-02-10 | 2024-02-19 | 1.0 y | J&J Vision Care | **speaking + consulting** | 538,153 | 1,091,200 | 840,290 |
| 3 | Fenlin | PA, orthopaedics | 2014-06-06 | 2024-01-25 | 9.6 y | Stryker | royalty | 536,693 | 712,481 | 1,154,803 |
| 4 | Mast | NV, orthopaedics | 2019-05-28 | 2024-02-09 | 4.7 y | DePuy Synthes | royalty | 365,269 | 395,181 | 424,557 |
| 5 | Morrison | GA, neurosurgery | 2019-10-07 | 2024-02-08 | 4.3 y | Stryker | royalty | 356,375 | 333,091 | 354,899 |
| 6 | Duran | MT, cardiothoracic | 2017-08-30 | 2024-01-23 | 6.4 y | Medtronic | royalty | 91,523 | 89,912 | 88,872 |
| 7 | Hill | MS, orthopaedics | 2019-12-13 | 2024-02-08 | 4.2 y | Globus, Stryker, Alphatec | royalty | 82,472 | 30,146 | 31,033 |
| 8 | Ruiz | FL, oral surgery | 2023-11-01 | 2024-01-24 | 84 d | KLS-Martin | royalty (+$56 AZ lunches) | 64,404 | 223,240 | 153,333 |
| 9 | Reddy | AZ, retina | 2022-09-20 | 2024-01-30 | 1.4 y | US Retina, Bausch & Lomb | **acquisition $50k** + royalty | 62,786 | — | 41,899 |
| 10 | Goldstein | NJ, podiatry | 2014-07-29 | 2024-02-14 | 9.5 y | Cook | royalty | 46,447 | 42,512 | — |

Prior-year dollars are the whole year's payments to that NPI, not date-tested, because 2023 and 2022 are context here, not the claim.

## What a hit means

- **Eight royalties, one acquisition.** Reddy's $62,786 is a $50,000 practice buy-out from US Retina plus $12,786 of Bausch & Lomb royalty, so eight of the ten are pure royalty streams. A royalty is passive income on a patented implant. It keeps paying after the surgeon stops operating,
  and it is paid to a person or their estate, not to an NPI. Open Payments still has to tag it to a covered recipient, and
  the manufacturer's recipient record keeps the old NPI forever because nothing refreshes it. Spetzler's stream is flat at
  $1.8M to $2.0M a year across three files, five to six years after deactivation. That is a retired surgeon's royalty, filed
  correctly by the company and never re-keyed by anyone.
- **One speaker.** Geller is the row that does not fit. Speaking and consulting are services performed in the year.
  J&J Vision Care paid him $451k to speak and $87k to consult in 2024 with an NPI that went dark in February 2023.
  His profile still carries a CA licence in the supplement, so the reporting itself is legal; the NPI is just gone.
  Benign read: left clinical practice, dropped the NPI, kept the industry work. Either way, this is the one of the ten
  where "still being sent" is literally true.
- **The tail.** 1,078 of 1,325 NPIs got under $100; 1,246 NPIs took 2,503 meals worth $82,211. 116 NPIs were paid a
  decade or more after deactivation, for $9,190. That is stale recipient-matching in Open Payments, not people.

## What a miss would have meant

A zero after the date test would have said CMS scrubs Open Payments against NPPES. It does not. Part B does: the first
pass found 1 NPI deactivated before 2024 with a Part B 2024 row, and none of the ten here bill Part B.

## What a skeptic would attack

1. **"Dead" is not in the data.** Reason code is blank on 346,179 of 346,179. None of the ten is excluded or on SAM. The
   warehouse cannot say retired, dead, merged or revoked. Answer: the report says deactivated, and the royalty pattern plus
   zero Part B billing is consistent with retirement, nothing more.
2. **Is the deactivation date itself right?** One NPPES snapshot, no second source of provider status. Answer: the same
   test ran on three Open Payments vintages with the same shape, and the ten all have multi-year streams, so a single
   bad date would not produce this.
3. **Did they re-enrol under a new NPI?** REPLACEMENT_NPI is blank by construction on deactivated rows. Answer: a
   name + state search of live type-1 rows finds a same-name NPI for only two of the ten, in the wrong specialty.
   Not proof, but the obvious rescue fails.
4. **Is $4.19M the right headline?** No. It reads like a spread and it is five people and one speaker. The per-NPI median
   is $28. Answer: headline carries the concentration.
5. **Who says these are the people named?** All 1,325 deactivated NPPES rows carry a blank ENTITY_TYPE_CODE, blank name,
   blank taxonomy and blank state. Every identity, specialty and state in this report comes from Open Payments alone;
   NPPES contributes only the NPI and the deactivation date. A wrong NPI keyed by a manufacturer would put the wrong name
   on this table with nothing in NPPES to catch it. The profile supplement repeats the same NPI, so it is not a second source.
6. **"Drug industry money."** The hunch title says drug. The head of the money is device makers (Stryker, DePuy,
   Medtronic, Globus, Alphatec, KLS-Martin, Cook, Bausch & Lomb); the drug companies are the $82k of lunches.

## Traps met

- The Open Payments mart (`HEALTH__FED_CMS_OPEN_PAYMENTS`, 22 columns) does not carry
  `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID`, so the quadrillion-dollar id-as-money trap cannot fire
  there; `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS` is the only money column and it is typed FLOAT. Landing still has the trap.
- The NPPES mart mixes blank conventions on one row: dates are NULL (`NPI_REACTIVATION_DATE is null` works) while text
  columns on the same stripped row are empty strings (`ENTITY_TYPE_CODE = ''`, not null). Test each column by its type.
- `HEALTH__FED_HHS_OIG_LEIE` renames every landing column: LASTNAME to LAST_NAME, EXCLTYPE to EXCLUSION_TYPE,
  EXCLDATE to EXCLUSION_DATE, and adds WAS_REINSTATED and NPI_IS_REAL. Landing names throw in the mart.
- `DATE_OF_PAYMENT` in the PY2024 mart parses with `try_to_date(x,'MM/DD/YYYY')` on 100% of rows, but the 73 year-2
  rows (36 NPIs, min 0002-11-30) survive into the mart; min(DATE_OF_PAYMENT) is unusable. Harmless here: a year-2 date
  sorts before every deactivation date, so it can only shrink the after-deactivation count.

## The answer

Industry money is still booked to switched-off NPIs, $4.19M of it in PY2024, but the money is eight device royalty
streams to surgeons that predate the deactivation and never stopped, one $50k practice acquisition, plus one optometrist paid $538k for services with a
dark NPI. Nothing was reactivated, replaced or excluded. The drug-company share is $82k of lunches to 1,246 NPIs.

STATUS: confirmed but reframed
HEADLINE: $4,187,435 of PY2024 industry money went to 1,325 switched-off NPIs, 94% of it to 10 people — eight device royalties that ran the same in 2022 and 2023, one practice acquisition, one optometrist paid $538k for speaking and consulting a year after his NPI went dark; none reactivated, none excluded, none billing Part B.
