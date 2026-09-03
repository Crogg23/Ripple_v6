# PORTAL_CKA_OKLAHOMA_OPEN_DA_042A7F3ED2

rows 10.0K  columns 15  scan 3.7s

roles: amount 1, audit 2, category 2, date 2, other 4, who 5

## when

PO_DATE
  2025      3.1K  ##############
  2026      6.9K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | 0 | 6.9K | 2.99M | 78.74M | 2.04B |

## who

BUSINESS_UNIT_NAME by rows
      2.5K  Department of Transportation
      1.2K  Department of Corrections
       637  Mental Health & Subst Abuse Sv
       433  Dept of Environmental Quality
       413  State Bureau of Investigation
       373  Mgmt and Enterprise Services
       369  Department of Veterans Affairs
       290  Attorney General
       211  District Attorneys Council
       196  Department of Agriculture
       193  Oklahoma Military Department
       165  Office of Juvenile Affairs
       146  Council on Law Enfc Ed & Trng
       121  Dept of Rehabilitation Service
       100  Comm on Children and Youth
        97  Department of Commerce
        93  Energy Resources Board
        84  Department of Labor
        84  Secretary of State
        82  Narc & Dangerous Drugs Control

BUSINESS_UNIT_NAME by dollars
       1.13B     2.5K rows  Department of Transportation
     273.73M     1.2K rows  Department of Corrections
      96.17M        8 rows  OSU Medical Authority
      80.24M      637 rows  Mental Health & Subst Abuse Sv
      59.45M      290 rows  Attorney General
      51.69M      165 rows  Office of Juvenile Affairs
      34.69M      373 rows  Mgmt and Enterprise Services
      34.09M       51 rows  OK DEP AEROSPACE & AERONAUTICS
      31.07M       11 rows  Department of Health
      27.79M      433 rows  Dept of Environmental Quality
      26.78M       82 rows  Narc & Dangerous Drugs Control
      25.94M       46 rows  Tobacco Settlement Endmt Trust
      15.53M       65 rows  Oklahoma Lottery Commission
      14.34M      369 rows  Department of Veterans Affairs
      13.95M      413 rows  State Bureau of Investigation
      13.81M      211 rows  District Attorneys Council
      13.09M      193 rows  Oklahoma Military Department
      12.24M        8 rows  Capitol Improvement Authority
       8.65M      196 rows  Department of Agriculture
       7.25M       45 rows  Health Care Workforce Trng Com

VENDOR by rows
       729  OFFICE OF MANAGEMENT & ENTERPRISE SVCS
       452  OKLAHOMA DEPARTMENT OF CORRECTIONS
       271  STANDLEY SYSTEMS LLC
       264  AUTHORITY ORDER-PCARD
       224  DELL MARKETING LP
       215  SHI INTERNATIONAL CORP
       200  AUTHORITY ORDER VENDOR
       191  DELL FINANCIAL SERVICES LLC
       158  ORION SECURITY SOLUTIONS LLC
       123  SYSCO CORPORATION
       120  ACTION SAFETY SUPPLY CO LLC
       111  CARAHSOFT TECHNOLOGY CORP
        92  THERMO FISHER SCIENTIFIC INC
        88  SOUTH CENTRAL INDUSTRIES INC
        80  COMDATA INC
        79  ANIXTER INC
        75  GALLS LLC
        70  AT&T ENTERPRISES LLC
        69  CENTRAL SALT LLC
        66  STAPLES INC

VENDOR by dollars
     247.62M       10 rows  ARAMARK CORRECTIONAL SERVICES LLC
     169.77M       11 rows  SHERWOOD CONSTRUCTION CO INC
     108.31M        5 rows  ROBINSON CONSTRUCTION LLC
      56.51M       55 rows  OKLAHOMA STATE UNIVERSITY
      52.49M        2 rows  DUIT CONSTRUCTION COMPANY INC
      51.28M        8 rows  BECCO CONTRACTORS INC
      49.46M        4 rows  OKLAHOMA STATE UNIVERSITY MEDICAL CENTER
      46.26M       50 rows  OFFICE OF JUVENILE AFFAIRS
      44.03M        5 rows  C3 CONSTRUCTION INC
      42.66M        5 rows  SILVER STAR CONSTRUCTION CO INC
      37.51M       15 rows  HASKELL LEMON GROUP LLC
      36.84M      200 rows  AUTHORITY ORDER VENDOR
      35.95M        8 rows  OKLAHOMA HEALTH CARE AUTHORITY
      33.34M        7 rows  J&R CONSTRUCTORS GROUP
      31.03M        5 rows  OVERLAND CORPORATION
      30.89M        1 rows  OSU MEDICAL AUTHORITY
      29.22M       15 rows  THE CUMMINS CONSTRUCTION COMPANY INC
      27.80M        4 rows  MANHATTAN ROAD & BRIDGE COMPANY
      26.56M       30 rows  BOARD OF REGENTS OF THE UNIV OF OK HSC
      20.32M      729 rows  OFFICE OF MANAGEMENT & ENTERPRISE SVCS

BUSINESS_UNIT by rows
      2.5K  34500
      1.2K  13100
       637  45200
       433  29200
       413  30800
       373  09000
       369  65000
       290  04900
       211  22000
       196  04000
       193  02500
       165  40000
       146  41500
       121  80500
       100  12700
        97  16000
        93  35900
        84  40500
        84  62500
        82  47700

BUSINESS_UNIT by dollars
       1.13B     2.5K rows  34500
     273.73M     1.2K rows  13100
      96.17M        8 rows  77500
      80.24M      637 rows  45200
      59.45M      290 rows  04900
      51.69M      165 rows  40000
      34.69M      373 rows  09000
      34.09M       51 rows  06000
      31.07M       11 rows  34000
      27.79M      433 rows  29200
      26.78M       82 rows  47700
      25.94M       46 rows  09200
      15.53M       65 rows  43500
      14.34M      369 rows  65000
      13.95M      413 rows  30800
      13.81M      211 rows  22000
      13.09M      193 rows  02500
      12.24M        8 rows  10500
       8.65M      196 rows  04000
       7.25M       45 rows  61900

DESC by rows
       628  SERVICE: Highway Engineering Services
       254  GRANT:Federal Funding to Subdivisions; Federal Grants that pass throug
       230  ROADWAY: Road construction services
        88  SERVICE:Environmental Remediation Services. Furnish All Labor, Materia
        79  General Laboratory Supplies
        77  GRANT:Funding to Subdivisions; Grants that pass through State Agency t
        66  AUTHORITY ORDER: Purchase Card
        61  SW0776-Traffic Striping
        58  GRANT: pass-thru funding for Forestry Cost-Share assistance grants.
        57  ENGINEERING SRVS: Right of way utility specialist contracts
        52  Dell Laptop Lease
        49  Laptop Computer Lease
        49  SW0699 Herbicide, Fertilizer, and Related Chemicals
        47  Network Cable and Accessories
        46  Class "A" Sand
        45  AUTHORITY ORDER: Emergency Purchases (Small Dollar) less than the Comp
        44  Opioid Abatement Grant
        37  EASEMENT: Right of way
        36  LAPTOP
        35  FUEL SRVC: Allowable charges

DESC by dollars
     841.32M      230 rows  ROADWAY: Road construction services
     247.62M       10 rows  Food Management Services
     153.25M      628 rows  SERVICE: Highway Engineering Services
      48.12M        1 rows  Support of educational and operational activities at the OSU
      44.93M      254 rows  GRANT:Federal Funding to Subdivisions; Federal Grants that p
      33.29M       34 rows  SERVICE: Airport Runway Construction
      30.89M        1 rows  REIMBURSEMENT FOR CONSTRUCTION OF NEW TULSA PSYCHIATRIC CARE
      30.00M        1 rows  Reimbursement for cost of construction of hospital expansion
      21.70M        1 rows  Payroll Encumbrance
      18.36M        1 rows  Enhanced Tier Payment System (ETPS)(19601/3003199)
      17.55M       44 rows  Opioid Abatement Grant
      17.30M       30 rows  Domestic Violence and Sexual Assault Services Contract
      15.00M        1 rows  Hold for Next Generation
      13.09M        1 rows  FY26/27: 04/03/26-10/30/26 - Year 1 of 5 - Provide funding f
      13.09M        1 rows  FY26/27: 04/03/26-10/30/26 - Year 1 of 5 - Provide funding f
       9.23M        1 rows  2010 Principal
       8.46M        1 rows  FEDERAL PASS-THRU FUNDING
       8.37M       33 rows  PASS THRU FUND:  Agency mission related projects exempted fr
       8.00M        1 rows  FY26 Level 1 Trauma- State match funds provided to OHCA to f
       7.07M       57 rows  ENGINEERING SRVS: Right of way utility specialist contracts

## who x when

BUSINESS_UNIT_NAME by PO_DATE, dollars = AMOUNT
  Attorney General                          2025:51.61M 2026:7.84M
  Capitol Improvement Authority             2026:12.24M
  Comm on Children and Youth                2025:312.4K 2026:1.66M
  Council on Law Enfc Ed & Trng             2025:433.3K 2026:1.69M
  Department of Agriculture                 2025:3.55M 2026:5.11M
  Department of Commerce                    2025:32.0K 2026:68.4K
  Department of Corrections                 2025:6.86M 2026:266.87M
  Department of Health                      2025:466.85 2026:31.07M
  Department of Labor                       2026:741.5K
  Department of Transportation              2025:201.80M 2026:925.95M
  Department of Veterans Affairs            2025:5.02M 2026:9.32M
  Dept of Environmental Quality             2025:10.40M 2026:17.39M
  Dept of Rehabilitation Service            2025:1.62M 2026:3.94M
  District Attorneys Council                2025:8.67M 2026:5.15M
  Energy Resources Board                    2025:942.5K 2026:1.89M
  Health Care Workforce Trng Com            2025:43.1K 2026:7.21M
  Mental Health & Subst Abuse Sv            2025:50.72M 2026:29.51M
  Mgmt and Enterprise Services              2025:13.27M 2026:21.42M
  Narc & Dangerous Drugs Control            2025:291.3K 2026:26.49M
  OK DEP AEROSPACE & AERONAUTICS            2025:17.65M 2026:16.44M
  OSU Medical Authority                     2026:96.17M
  Office of Juvenile Affairs                2025:48.65M 2026:3.05M
  Oklahoma Lottery Commission               2025:151.3K 2026:15.38M
  Oklahoma Military Department              2025:262.3K 2026:12.82M
  Secretary of State                        2025:108.5K 2026:679.4K
  State Bureau of Investigation             2025:1.77M 2026:12.18M
  Tobacco Settlement Endmt Trust            2025:798.1K 2026:25.14M

VENDOR by PO_DATE, dollars = AMOUNT
  ACTION SAFETY SUPPLY CO LLC               2025:1.67M 2026:16.69M
  ANIXTER INC                               2025:13.5K 2026:24.6K
  ARAMARK CORRECTIONAL SERVICES LLC         2026:247.62M
  AT&T ENTERPRISES LLC                      2026:999.9K
  AUTHORITY ORDER VENDOR                    2025:866.9K 2026:35.97M
  AUTHORITY ORDER-PCARD                     2025:87.6K 2026:17.04M
  BECCO CONTRACTORS INC                     2025:1.11M 2026:50.17M
  C3 CONSTRUCTION INC                       2025:31.34M 2026:12.69M
  CARAHSOFT TECHNOLOGY CORP                 2025:2.91M 2026:2.41M
  CENTRAL SALT LLC                          2025:2.05M
  COMDATA INC                               2025:325.3K 2026:3.26M
  DELL FINANCIAL SERVICES LLC               2025:341.5K 2026:1.39M
  DELL MARKETING LP                         2025:191.1K 2026:1.40M
  DUIT CONSTRUCTION COMPANY INC             2026:52.49M
  GALLS LLC                                 2025:10.5K 2026:15.5K
  OFFICE OF JUVENILE AFFAIRS                2025:45.95M 2026:313.4K
  OFFICE OF MANAGEMENT & ENTERPRISE SVCS    2025:4.68M 2026:15.63M
  OKLAHOMA DEPARTMENT OF CORRECTIONS        2025:415.1K 2026:2.14M
  OKLAHOMA STATE UNIVERSITY                 2025:12.31M 2026:44.20M
  OKLAHOMA STATE UNIVERSITY MEDICAL CENTER  2025:174.3K 2026:49.29M
  ORION SECURITY SOLUTIONS LLC              2025:118.6K 2026:161.6K
  ROBINSON CONSTRUCTION LLC                 2026:108.31M
  SHERWOOD CONSTRUCTION CO INC              2026:169.77M
  SHI INTERNATIONAL CORP                    2025:2.23M 2026:2.43M
  SILVER STAR CONSTRUCTION CO INC           2026:42.66M
  SOUTH CENTRAL INDUSTRIES INC              2025:2.5K 2026:446.3K
  STANDLEY SYSTEMS LLC                      2025:25.5K 2026:720.2K
  STAPLES INC                               2025:1.2K 2026:111.2K
  SYSCO CORPORATION                         2026:8.30M
  THERMO FISHER SCIENTIFIC INC              2025:275.6K 2026:1.13M

## what

ORIGIN: EXC 58%, OSF 23%, AGY 10%, CHG 8%, CP 1%

PO_TYPE: RLSE 29%, ITRL 23%, IAGY 20%, DOT 9%, SUBR 8%, PCAO 3%, AO 2%, ITAG 1%, GSAV 1%, UTIL 1%, OMKT 1%, PYE 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESS_UNIT | who | 109 | 0 | 34500 2.5K; 13100 1.2K; 45200 637; 29200 433 |
| BUSINESS_UNIT_NAME | who | 109 | 0 | Department of Transportat 2.5K; Department of Corrections 1.2K; Mental Health & Subst Abu 637; Dept of Environmental Qua 433 |
| PO_ID | other | 5.8K | 0 | 4529069744 91; 4159004943 85; 3459085792 75; 2929026627 72 |
| LINE_NBR | other | 62 | 0 | 1 5.9K; 2 1.3K; 3 681; 4 463 |
| VENDOR | who | 1.3K | 0 | OFFICE OF MANAGEMENT & EN 729; OKLAHOMA DEPARTMENT OF CO 452; STANDLEY SYSTEMS LLC 271; AUTHORITY ORDER-PCARD 264 |
| DESC | who | 5.3K | 0 | SERVICE: Highway Engineer 628; GRANT:Federal Funding to  257; ROADWAY: Road constructio 230; GRANT: pass-thru funding  93 |
| AMOUNT | amount | 6.1K | 0 | 5000 130; 1000 118; 10000 103; 25000 86 |
| PO_DATE | date | 177 | 0 | 2026-05-06 00:00:00 190; 2026-05-18 00:00:00 176; 2026-05-14 00:00:00 135; 2026-01-12 00:00:00 127 |
| PO_DATE_EXCEL | other | 179 | 0 | 46146 190; 46158 176; 46154 135; 46032 127 |
| ORIGIN | category | 5 | 0 | EXC 5.8K; OSF 2.3K; AGY 1.0K; CHG 754 |
| PO_TYPE | category | 15 | 0 | RLSE 2.9K; ITRL 2.3K; IAGY 2.0K; DOT 938 |
| FLAGGED_AS_DIRECT_PO | other | 1 | 0 | No 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:42:29.49532 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4d249f6c-cc22-4bc9-9da4-7 10.0K |
| SRC_SHA256 | who | 1 | 0 | 82c1c384a54e9339723a36fc3 10.0K |
