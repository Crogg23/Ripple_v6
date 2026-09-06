# Hunch 15 — Are banned companies still getting paid on disaster-relief contracts?

**Short answer: no.** The $169M is real arithmetic on the wrong question. Line up the ban date against the award date and the money inside a ban window is **$15,328 gross, -$403,238 net** (the government was clawing back, not paying).

## What was checked

| Step | What | Number |
|---|---|---|
| Exclusion list | `PROCUREMENT__FED_SAM_EXCLUSIONS` | 168,328 records; 35,197 firms/entities; 38,427 distinct UEIs; 159,074 open-ended ("Indefinite") |
| Contracts | `FED_USASPENDING_CONTRACTS_FULL_R2` | 93,153,424 transactions, 2006-10-01 to 2026-08-22, 582,657 UEIs |
| Disaster slice | FEMA as awarding sub-agency, OR a disaster keyword in the description (hurricane, wildfire, flood, debris removal, FEMA, emergency management...) | 210,751 FEMA rows + ~110K keyword rows |
| Match | recipient UEI = exclusion UEI, or CAGE = CAGE, or exact upper-cased name; entities only, no individuals | 349 transactions, 61 recipients (56 by ID, 5 by name only) |
| Timing | action date between exclusion ACTIVATION_DATE and TERMINATION_DATE (open-ended when Indefinite) | **20 transactions, 7 recipients** |

A SAM exclusion is the federal do-not-hire list. UEI is the government's company ID (replaced DUNS). CAGE is the older DoD supplier code. "Obligation" is money the agency committed on a transaction; negative means it took money back.

## Rebuilding the first pass a different way

Tried nine variants (`repro.json`). Exact hit:
**26 companies, $169,247,003 = FEMA only, UEI join, sum of CURRENT_TOTAL_VALUE_OF_AWARD once per award, no dates.**

That is the award *ceiling*, not spend. Same 26 companies on FEDERAL_ACTION_OBLIGATION: **$22.1M**. All disaster agencies, 56 companies: **$41.1M**.

$155,982,000 of the $169M (92%) is one award, CONT_AWD_70FB7018C00000001: Tribute Contracting's Hurricane Maria meals deal — $156M obligated Oct 2017, $155.7M de-obligated by Jan 2019, net $255K. Excluded 2025-03-26.

## The timing check the first pass skipped

- 54 of 61 recipients: every disaster award ended **before** the exclusion started. Typical gap: years. Blackhawk Ventures last award 2012, banned 2021. N-Powell last award 2014, banned 2015. Intellipeak and Worldwide Equipment banned August 2026, last awards 2022 and March 2026.
- 7 recipients have a transaction on or after ban start. 20 transactions:
  - 14 are de-obligations or $0 closeouts (JS SDVO -$273K, Prescient -$77K, Anderson -$63K, TAK, Investment Mgmt Enterprise).
  - 2 are Universal Medical Inc, 2007-08 VA apron purchases ($3,096), matched by **name only** to a 1998 HHS/OPM exclusion on a firm with a different UEI. Same-name collision, not a hit.
  - **4 are real:** Anderson Court Reporting LLC, excluded by Department of Labor 2024-07-19; one FEMA purchase order for court transcripts, 70FA4024P00000053, awarded 2024-08-29 ($6,190) and modified 2024-09-25 ($6,043). $12,232 total. A transcription vendor, not disaster work.

## What a hit means / what a miss means

- Hit would mean: a company got new disaster money while on the list. That happened once, $12K, transcripts.
- Miss means: the exclusion list is doing its job on the money that matters, or the ban came after the failure (Tribute is the clean example: the ban is the consequence of the contract, not evidence of paying a banned firm).

## What a skeptic would attack, and the answer

1. **"Your disaster slice is too narrow."** Keyword slice is deliberately wide (catches Army "emergency response" work). The FEMA sub-agency slice alone reproduces the first pass exactly, so the narrowing did not lose the 26.
2. **"UEI join misses renamed shells."** Added CAGE and exact-name joins; they add 5 recipients and $2.6M, all pre-ban. Fuzzy-name matching is a different hunch (affiliate evasion) and the surname/generic-name traps apply.
3. **"Termination date null means the ban ended."** No: TERMINATION_DATE_RAW is 'Indefinite' on 159,074 of the null rows; treated as open-ended, which *widens* the window and still finds nothing.
4. **"You used the earliest activation across multiple records."** Yes, that is the widest possible window per company (5,937 UEIs have 2+ records). Still nothing.
5. **"Action date is not payment date."** Obligation is the commitment; outlays are not in this table. A banned company could still receive outlays on pre-ban obligations, and that is legal — exclusions bar *new* awards, not performance on existing contracts.
6. **"Parent-UEI evasion: a banned parent contracting through a child."** Skeptic tested it: 1 transaction, $0.
7. **"UEI coverage in the exclusion list is spotty."** Skeptic tested it: 97% of entity exclusions carry a UEI.
8. **"The keyword slice misses rows with blank descriptions."** Skeptic tested it: TRANSACTION_DESCRIPTION is non-null on every row.
9. **"Only 2006 onward."** Exclusions from the 1990s (5,758 activations in 2000 alone) with pre-2006 contracts are invisible. Not fixable in this data; does not affect the "still getting paid" question.

## Traps found

- `FED_USASPENDING_CONTRACTS_FULL_R2` columns are **UPPERCASE**, unlike the older USAspending landings. `select "recipient_uei"` fails; bare `RECIPIENT_UEI` works. The 2026-08-31 lowercase trap does not apply to R2.
- `CURRENT_TOTAL_VALUE_OF_AWARD` changes per transaction (Tribute, CONT_AWD_70FB7018C00000001: $255K, $155.98M, $70M, $5.255M, $255K on five rows of one award; the first-pass method took the $155.98M max). Summing it per transaction gives $457M; max per award gives $223M; neither is money moved. Use FEDERAL_ACTION_OBLIGATION for dollars that moved.
- `ACTIVATION_DATE` has sentinels: 1908-04-20, 2084, 2099-12-30. 11,016 rows null.
- Exclusion `CAGE_CODE` is populated on only 392 of 168,328 rows; a CAGE-only join would find almost nothing and prove nothing.

STATUS: dead
HEADLINE: 26 banned companies, $169M in "disaster contracts" shrinks to $12,232 (one court-transcript vendor) once award dates are checked against ban dates; net money inside ban windows is -$403K of clawbacks.
