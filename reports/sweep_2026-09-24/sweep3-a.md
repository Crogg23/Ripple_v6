# Sweep 3, agent A: 30 singles rows

**Tally:** 2 live, 16 probed, 10 dead, 2 skip. **40 warehouse statements** (budget 120). All SQL is in `sweep3-a.sql`.

## Every row

| Row | Status | The number that mattered |
|---|---|---|
| NYC CFB 2013 contributions | dead | Self-funders top the list: Catsimatidis $10.8M, Spitzer $10.7M. 0 of 104K matched donors got more than the match cap |
| SAM exclusions | probed | 1,412 UEIs on 3+ rows. FIGG Group (the FIU bridge firm) has 9 FHWA rows. Every row is "Active" |
| IRS 527 Schedule A | probed | $13.58B total. **$1.47B (10.8%) sits in lump rows**, not in named donors |
| Part B by provider and service | **live** | Skin substitutes: $4.62B across 1,153 billers. Jeng $146.6M; Kapadia $91.8M on 28 patients |
| UN sanctions list | dead | GENDER is blank on 950 of 1,011 rows |
| NAAG multistate settlements | dead | OTHER_SETTLEMENT_AMOUNT is filled on 21 of 882 rows. The tobacco settlement (MSA) is $206B of the $377.9B total |
| FAERS demographics | dead | **DEATH_DT is blank on all 5.81M rows** |
| CourtListener positions | dead | VOTES_YES_PERCENT is filled on 4 of 51,290 rows |
| Form 5500 | dead | FORM_YEAR is blank on every row, and asset totals are empty. The top plan is NEA's, with 2.64M participants |
| Part B by provider | probed | $152.2B allowed. The top 1% of providers get 34% of it. The top individual is Jeng, $154.5M |
| CMS Medicare provider | skip | A copy of Part B by provider: same 1,296,739 NPIs, same dollar total |
| Nursing home penalties | probed | $459M in fines. $4,587 repeats 636 times. The top home is Chicago Ridge SNF, IL, at $883K |
| GovInfo bill cosponsors | probed | Chip Roy was original cosponsor on 521 consecutive bills, all withdrawn the same day |
| Senate stock watcher | probed | The file stops in 2020. Perdue made 2,597 of the 8,350 trades |
| CMS home health | probed | Only 25 agencies spend 1.5x the national episode cost or more. The top is 2.17x |
| OSHA case detail 2023 | probed | 282 deaths. Amazon has the most cases, 38,132. Employee counts go up to 172M |
| Hospital officer pay | probed | The same executive's total pay repeats on every related return |
| CourtListener judge races | dead | A link table with coded race IDs |
| DOL OLMS union reports | probed | Some columns are shifted: TERMINATE_FLAG holds first names |
| OSHA case detail 2024 | probed | 201 deaths. USPS has 24 deaths across 2023-24 |
| FDIC failed banks | dead | SVB, First Republic and IndyMac top the losses. Known history |
| EPA RCRA enforcements | probed | $1.19B proposed penalties, $1.50B final. Dates start in year 0999 |
| DME by referring provider | probed | 78% of rows carry the suppressed flag. Luckette (NV) is the top referrer at $22.2M |
| DME by supplier | **live** | Sunshine Senior Solutions: $1.10B on 8 codes, about $10K per patient |
| HUD public housing authorities | probed | North Little Rock got $4.4M for 110 units with 0 occupied. The median is $3,044 per unit |
| CourtListener courts | dead | DATE_LAST_PACER_CONTACT is blank on all 3,361 rows |
| UCDP conflict events | probed | CODE_STATUS is 'Clear' on every row. One Ethiopia 2022 row holds 121,848 deaths |
| OSHA case detail 2025 | probed | 130 deaths. Target has the most cases, 9,287 |
| Bill cosponsors | skip | A copy of the GovInfo table for the 118th-119th Congress |
| FJC judges | dead | 614 of 4,067 judges are women (15%). The same judges as the copy sweep-a flagged |

## The top three

### 1. Mail-order medical supplies: $10K-16K per patient (DME by supplier, live)
- **What I checked:** total allowed per supplier = average allowed × services, summed over each supplier's codes. Then the top six suppliers' three biggest codes, with patients.
- **Number:**
  - **Sunshine Senior Solutions** (Delray Beach, FL): $1.10B on 8 codes. That's $513M for alginate dressings (A6197) and $430M for intermittent catheters (A4353), across about 42-48K patients, about $10K each.
  - **Almaz Med Supply** (Woodside, NY): $604M. Its catheters come to **$16.6K per patient**.
  - **JL Webb DME** (Bowling Green, KY): catheters at $9.6K per patient.
- **A hit means:** a few suppliers with huge volume on two codes that are known for fraud. That's the catheter and dressing pattern CMS flagged.
- **A miss means:** the same suppliers turn out to be big national mail-order shops, with per-patient costs in line with peers on the same code.
- **The boring explanation:** mail-order volume. Also, the average-times-services math can overshoot when rows mix rentals. Next step: compare with the same code's median supplier per patient, and check the data year.

### 2. Skin substitutes billed by individual clinicians (Part B by provider and service, live)
- **What I checked:** HCPCS codes Q4100-Q4399, allowed amount = average × services, summed per NPI.
- **Number:** $4.62B across 1,153 billers. The top 20 get $1.13B (24%).
  - **Aaron Jeng** (internist, CA): $146.6M. $110M of it is one product, Q4205, and his biggest code covers 403 patients.
  - **Ravi Kapadia** (CA): $91.8M on at most 28 patients, **about $3.3M each**.
  - Nurse practitioners in FL, NV and AZ fill much of the top 15.
- **A hit means:** per-patient graft areas that no real wound needs.
- **A miss means:** the big billers are wound-care centers with legitimately huge caseloads.
- **The boring explanation:** CMS priced some grafts above $1,500 per cm², so a few big wounds can cost a lot. But $3.3M per patient is past that. DOJ's 2025 takedowns already hit this area, so check the news before claiming it.

### 3. Chip Roy's 521 withdrawn cosponsorships (GovInfo cosponsors, probed)
- **What I checked:** withdrawn cosponsorships by member.
- **Number:** Roy has 521 withdrawals. The next member has 5. All 521 are consecutive bills from HR1844 on. He is marked as original cosponsor on every one, and every one was withdrawn on 2023-05-18.
- **A hit would mean** a real mass sign-on and pull-back. **A miss means** a clerk mistake that was fixed.
- **The boring explanation:** almost certainly the clerk mistake. Anyone counting withdrawals or "most cosponsorships" needs to know it's there.

## New data traps
- **IRS 527 Schedule A has lump rows.** 10,443 rows ("Aggregate below threshold", "Sum of Transactions", "TOTAL SCHEDULE A CONTRIBUTIONS") hold $1.47B. That's 97.6% of American Police Officers Alliance's money and 34.5% of ActBlue Non-Federal's. Ranking by donor name breaks.
- **FAERS DEMO `DEATH_DT` is blank on all 5.81M rows.** Country is spelled two ways, "UNITED STATES" and "US".
- **OSHA ITA `ANNUAL_AVERAGE_EMPLOYEES` has typos.** 41 rows in 2023 and 150 in 2024 claim 1M or more employees; the top is 172,307,584. Per-worker rates need a cap.
- **Hospital officer pay repeats `TOTAL_COMPENSATION`.** It repeats on every return where a person is listed: Lloyd Dean's $35.5M appears 3 times, Howard Kern's $11.4M 5 times. Sums count the same pay more than once.
- **DOL OLMS has column-shifted rows.** TERMINATE_FLAG holds first names on about 100 rows. SHORTAGE_AMOUNT is above 0 on only 78 rows, and all of them are shifted address rows.
- **Copies:** CMS_MEDICARE_PROVIDER is the same table as ..._BY_PROVIDER. POLITICS__BILL_COSPONSORS is GovInfo cosponsors for the 118th-119th Congress.
- **Constant or empty columns:** UCDP `CODE_STATUS` is always 'Clear'. CourtListener `VOTES_YES_PERCENT` is filled on 4 rows. Form 5500 `FORM_YEAR` is empty. UN sanctions `GENDER` is 94% blank.

## Statement count
40 of 120.
