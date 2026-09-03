# FED_USASPENDING_TOPTIER_AGENCIES

rows 111  columns 16  scan 4.7s

roles: amount 3, audit 2, other 6, who 5

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| OUTLAY_AMOUNT | 111 | 0 | 44.46M | 1267.06B | 1666.77B | 5970.27B |
| OBLIGATED_AMOUNT | 111 | 0 | 65.18M | 1269.13B | 1840.83B | 6420.53B |
| BUDGET_AUTHORITY_AMOUNT | 111 | -9.77B | 211.11M | 2538.92B | 3379.35B | 12793.16B |

## who

AGENCY_NAME by rows
         1  United States Court of Appeals for Veterans Claims
         1  African Development Foundation
         1  Department of Justice
         1  400 Years of African-American History Commission
         1  National Endowment for the Arts
         1  Advisory Council on Historic Preservation
         1  American Battle Monuments Commission
         1  Department of Labor
         1  Corporation for National and Community Service
         1  Environmental Protection Agency
         1  United States Trade and Development Agency
         1  Marine Mammal Commission
         1  Department of Education
         1  National Credit Union Administration
         1  Armed Forces Retirement Home
         1  Administrative Conference of the U.S.
         1  National Labor Relations Board
         1  Occupational Safety and Health Review Commission
         1  District of Columbia Courts
         1  Department of the Treasury

AGENCY_NAME by dollars
    1666.77B        1 rows  Department of Health and Human Services
    1291.27B        1 rows  Department of the Treasury
    1049.19B        1 rows  Social Security Administration
     893.60B        1 rows  Department of Defense
     255.92B        1 rows  Department of Veterans Affairs
     142.88B        1 rows  Department of Agriculture
     127.35B        1 rows  Office of Personnel Management
      89.02B        1 rows  Department of Homeland Security
      79.62B        1 rows  Department of Education
      73.82B        1 rows  Department of Transportation
      50.10B        1 rows  Department of Housing and Urban Development
      40.30B        1 rows  Department of Labor
      38.96B        1 rows  Department of Energy
      33.49B        1 rows  Department of Justice
      23.71B        1 rows  Department of State
      20.74B        1 rows  Department of the Interior
      16.57B        1 rows  Corps of Engineers - Civil Works
      14.81B        1 rows  National Aeronautics and Space Administration
      12.43B        1 rows  Department of Commerce
      10.23B        1 rows  Railroad Retirement Board

AGENCY_SLUG by rows
         1  us-international-development-finance-corporation
         1  armed-forces-retirement-home
         1  environmental-protection-agency
         1  export-import-bank-of-the-united-states
         1  barry-goldwater-scholarship-and-excellence-in-education-foundation
         1  federal-financial-institutions-examination-council
         1  federal-maritime-commission
         1  peace-corps
         1  inter-american-foundation
         1  public-buildings-reform-board
         1  small-business-administration
         1  federal-communications-commission
         1  morris-k-udall-and-stewart-l-udall-foundation
         1  national-transportation-safety-board
         1  commission-of-fine-arts
         1  advisory-council-on-historic-preservation
         1  international-trade-commission
         1  committee-for-purchase-from-people-who-are-blind-or-severely-disabled
         1  department-of-education
         1  department-of-defense

AGENCY_SLUG by dollars
    1666.77B        1 rows  department-of-health-and-human-services
    1291.27B        1 rows  department-of-the-treasury
    1049.19B        1 rows  social-security-administration
     893.60B        1 rows  department-of-defense
     255.92B        1 rows  department-of-veterans-affairs
     142.88B        1 rows  department-of-agriculture
     127.35B        1 rows  office-of-personnel-management
      89.02B        1 rows  department-of-homeland-security
      79.62B        1 rows  department-of-education
      73.82B        1 rows  department-of-transportation
      50.10B        1 rows  department-of-housing-and-urban-development
      40.30B        1 rows  department-of-labor
      38.96B        1 rows  department-of-energy
      33.49B        1 rows  department-of-justice
      23.71B        1 rows  department-of-state
      20.74B        1 rows  department-of-the-interior
      16.57B        1 rows  corps-of-engineers-civil-works
      14.81B        1 rows  national-aeronautics-and-space-administration
      12.43B        1 rows  department-of-commerce
      10.23B        1 rows  railroad-retirement-board

CURRENT_TOTAL_BUDGET_AUTHORITY_AMOUNT by rows
       111  13397064591776.7

CURRENT_TOTAL_BUDGET_AUTHORITY_AMOUNT by dollars
    5970.27B      111 rows  13397064591776.7

AGENCY_ID by rows
         1  1067
         1  1205
         1  862
         1  11
         1  1166
         1  655
         1  1516
         1  1147
         1  1163
         1  1418
         1  766
         1  1426
         1  1162
         1  695
         1  95
         1  1416
         1  1129
         1  1141
         1  561
         1  882

AGENCY_ID by dollars
    1666.77B        1 rows  806
    1291.27B        1 rows  456
    1049.19B        1 rows  539
     893.60B        1 rows  1173
     255.92B        1 rows  561
     142.88B        1 rows  95
     127.35B        1 rows  503
      89.02B        1 rows  766
      79.62B        1 rows  1068
      73.82B        1 rows  731
      50.10B        1 rows  882
      40.30B        1 rows  267
      38.96B        1 rows  930
      33.49B        1 rows  252
      23.71B        1 rows  315
      20.74B        1 rows  209
      16.57B        1 rows  1205
      14.81B        1 rows  862
      12.43B        1 rows  183
      10.23B        1 rows  693

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AGENCY_ID | who | 113 | 0 | 1418 1; 90 1; 1169 1; 1162 1 |
| TOPTIER_CODE | other | 113 | 0 | 519 1; 1133 1; 345 1; 510 1 |
| ABBREVIATION | other | 109 | 0 | VEF 1; USTDA 1; CAVC 1; CSB 1 |
| AGENCY_NAME | who | 106 | 0 | Vietnam Education Foundat 1; United States Trade and D 1; United States Court of Ap 1; United States Chemical Sa 1 |
| CONGRESSIONAL_JUSTIFICATION_URL | other | 99 | 13 | https://www.ustda.gov/cj 1; https://www.uscourts.cavc 1; https://www.csb.gov/cj 1; https://www.usich.gov/cj 1 |
| ACTIVE_FY | other | 1 | 0 | 2026 111 |
| ACTIVE_FQ | other | 1 | 0 | 3 111 |
| OUTLAY_AMOUNT | amount | 98 | 0 | 0.0 13; 31890820.95 1; 26917018.0 1; 7518756.17 1 |
| OBLIGATED_AMOUNT | amount | 100 | 0 | 0.0 13; 42530730.61 1; 29982124.37 1; 6653751.27 1 |
| BUDGET_AUTHORITY_AMOUNT | amount | 101 | 0 | 0.0 11; 226783239.95 1; 133139926.4 1; 19824884.77 1 |
| CURRENT_TOTAL_BUDGET_AUTHORITY_AMOUNT | who | 1 | 0 | 13397064591776.7 111 |
| PERCENTAGE_OF_TOTAL_BUDGET_AUTHORITY | other | 100 | 0 | 0.0 11; 1.6927830600234817e-05 1; 9.937992422737375e-06 1; 1.4797931766462322e-06 1 |
| AGENCY_SLUG | who | 110 | 0 | vietnam-education-foundat 1; united-states-trade-and-d 1; united-states-court-of-ap 1; united-states-chemical-sa 1 |
| _INGESTED_AT | audit | 1 | 0 | 1781647214225021 111 |
| _SOURCE_RUN_ID | audit | 1 | 0 | ac11c9cb-b0ea-4d25-a102-6 111 |
| _SRC_SHA256 | who | 1 | 0 | d8f46b615d63d6749f663575b 111 |
