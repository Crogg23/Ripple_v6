# Sweep 2026-09-24 — sweep2-a (singles, 25 rows)

**Result:** 5 live, 13 probed, 7 dead, 0 untouched.
**Budget:** 72 SELECT/WITH statements out of 120. Each connection also ran one `ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS`. Queries are in `sweep2-a.sql`.
Nothing was written to the warehouse.

## Every row

| Row | Status | The number that mattered |
|---|---|---|
| CORPORATE_REGISTRY__FED_IRS_EO_BMF | probed | top 1% hold 84% of $11.0T assets; median 0 (454K null + 826K zero) |
| ECONOMICS__FED_IRS_BMF | dead | a near-copy of EO_BMF: same top 10, older snapshot |
| EDUCATION__FED_SENATE_LDA_FILINGS | probed | the 24 filings at $5M+ are junk (PhRMA $140M in one quarter; "Loc Nation" $20M x11) |
| HEALTH__FED_CMS_NURSING_HOME | **live** | Bria: 11 of 15 homes abuse-flagged (73% vs 10% nationally) |
| HEALTH__FED_NURSINGHOME411 | probed | Dec 2025 snapshot; confirms Bria; CHOW flag has 55 'Y' here |
| JUSTICE__…_NON_INVESTMENT_INCOME | dead | INCOME_AMOUNT blank on 99.3% of rows |
| JUSTICE__FED_COURTLISTENER_JUDGES | dead | FTM money on only 409 of 16,191 |
| POLITICS__FED_CONGRESS_LEGISLATORS | dead | reference table; N_TERMS is stored as text |
| POLITICS__MEMBER_CROSSWALK | dead | reference table; 13 presidents have no BIOGUIDE |
| ECONOMICS__FED_SBA_PPP | probed | only the $150K+ file; 749 loans at the $10M cap; "NEW APPLICATION" placeholder name |
| TRANSPORT__FED_FRA_CASUALTIES | **live** | trespasser deaths up from 664 (2017) to 838 (2025); Brightline had 41 deaths in 2024 |
| HEALTH__FED_CMS_QPP_EXPERIENCE | probed | 14% of individual reporters took the max −9% cut vs 0.2% of group rows |
| IMMIGRATION__FED_ICE_DETAINERS | **live** | share convicted when the detainer is written: 42.5% (FY23) down to 16.4% (FY26) |
| JUSTICE__FED_COURTLISTENER_DOCKETS | dead | VIEW_COUNT is web traffic; 2029 dates are junk |
| NYC_CFB 2021 | probed | McGuire $10.0M with no match; outside spenders (IS) mixed into the file |
| HEALTH__FED_CMS_PARTD_PRESCRIBERS | probed | top prescriber is $44.7M of Shingrix: a pharmacy standing order |
| NYC_CFB 2025 | **live** | Fix the City $35.6M from 381 gifts vs Mamdani $4.0M from 54,440 |
| CFPB_COMPLAINTS | probed | the 3 credit bureaus = 78% of complaints; each doubled from 2024 to 2025 |
| UK_COMPANIES_HOUSE_PSC | **live** | one man born 1996 is the controlling person on 1,602 active companies |
| CMS_OPEN_PAYMENTS (PY2024) | probed | the top payment is a $91.1M "Acquisitions" buyout on one row |
| CMS_OPEN_PAYMENTS_2022 | probed | Coric $133.7M and Love $98.9M, both acquisitions |
| CMS_OPEN_PAYMENTS_2023 | probed | top recipients are royalty holders; top 1% get 74% |
| COURTLISTENER_CITATIONS | dead | DATE_CREATED is the load date; VOLUME 9999 is a stand-in value |
| NYC_CFB 2001 | probed | CONTRIBUTION_DATE is null on every row |
| NYC_CFB 2009 | probed | Bloomberg is $108.4M of the $150.6M total |

## Top three live rows

### 1. ICE detainers: fewer of the people held have convictions
- **What was checked:** DETAINER_PREPARED_CRIMINALITY, the criminality code ICE records when it writes the detainer, grouped by fiscal year. Duplicate-likely rows were removed and each person counted once per year.
- **Numbers:**

  | FY | Persons | Convicted | Pending charges | Other immigration violator |
  |---|---|---|---|---|
  | 2023 | 91,217 | 42.5% | 54.5% | 3.0% |
  | 2024 | 105,780 | 39.6% | 57.5% | 2.9% |
  | 2025 | 165,506 | 28.1% | 66.5% | 5.4% |
  | 2026 | 83,111 | 16.4% | 71.2% | 12.5% |

- **Hit means:** a policy shift toward detainers on people with no conviction, and the code is set when the detainer is written, so a later conviction can't make old years look better.
- **Miss would mean:** the codes were redefined or backfilled.
- **Boring explanation:** coding practice changed. Also, FY26 has no rows from April to June 2026 (only 4 stray rows after March). Treat FY26 as partial.

### 2. UK Companies House PSC: mass nominee names
- **What was checked:** active individual controlling persons (PSCs), counted by distinct company per name and birth year.
- **Numbers:**
  - "Mr Mohammed Ayyaz" (born 1996): 1,602 companies, plus 618 more as "Dr Mohammed Ayyaz".
  - Peter Valaitis (born 1950): 1,279.
  - Michael Gleissner: 1,013, all notified on 51 days in 2016–17.
  - Gabrielle Southern (born 1996): 759 companies, notified inside 17 days in 2016.
  - An Egyptian national born 2001: 631 companies, 2022–26.
  - Another named person: 568 companies with postcode '00000'.
- **Hit means:** formation factories or stolen identities, a known Companies House abuse pattern.
- **Miss would mean:** the same name and birth year belongs to different people. That is unlikely at 600+ companies.
- **Boring explanation:** legitimate formation agents and shelf-company sellers. Gleissner is a known bulk registrant.

### 3. CMS nursing homes: Bria Health Services
- **What was checked:** the ABUSE_ICON rate by chain for chains with 10+ homes, in both snapshots (May 2026 and Dec 2025).
- **Numbers:**
  - Bria: 11 of 15 homes flagged, 73%. Nationally: 1,482 of 14,700, 10%.
  - Bria's average rating is 1.27 stars and its fines total $5.1M.
  - The flag held on the same homes across both snapshots.
  - Next chains: Evercare 8 of 11, Saba 7 of 11, Arcadia 12 of 22.
- **Hit means:** a chain-level abuse pattern concentrated in the Metro East St. Louis area of Illinois (Cahokia, Belleville, Alton).
- **Miss would mean:** the flag came from one inspection wave.
- **Boring explanation:** one aggressive state survey office. Illinois inspection intensity would need comparing.

The other live rows are FRA trespasser deaths and NYC 2025 outside money. Both are real numbers but known stories.

## New data traps
- **QPP ALLOWED_CHARGES is the group's total, repeated on every clinician row.** One value sits on 5,357 rows, and the column sums to $17.3 trillion. Any per-NPI ranking or "dollars under penalty" figure is inflated. Use rows where PARTICIPATION_OPTION = 'Individual' for per-clinician money.
- **COURTLISTENER non-investment income:** INCOME_AMOUNT is blank on 15,188 of 15,302 rows.
- **CONGRESS_LEGISLATORS:**
  - N_TERMS is stored as text, so MAX returns 9 instead of 30.
  - LEGISLATOR_SET is blank on every row.
  - FEC_IDS is blank on 11,237 rows.
  - The member crosswalk has correct values.
- **NYC CFB 2001:** CONTRIBUTION_DATE is null on all 193,741 rows.
- **Open Payments:** teaching-hospital rows hold NPI as an empty string, not null. `COALESCE(NPI, ...)` puts all of them into one fake recipient, about $0.7–1.1B a year.
- **LDA INCOME:** amended filings (types 2A, 1A…) repeat the original's total. Summing across filing types double counts.
- **PPP table:** this is the $150K-and-up extract only (99.6% of rows are $150K or more). It can't show bunching under $150K. BORROWER_NAME 'NEW APPLICATION' is a placeholder.
- **IRS_BMF (ECONOMICS)** duplicates EO_BMF (CORPORATE_REGISTRY) as an older snapshot.
- **The CHOW-flag trap applies only to CMS_NURSING_HOME.** NURSINGHOME411's PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS has 55 'Y'.
