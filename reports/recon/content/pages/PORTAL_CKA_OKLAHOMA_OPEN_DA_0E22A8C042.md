# PORTAL_CKA_OKLAHOMA_OPEN_DA_0E22A8C042

rows 10.0K  columns 15  scan 4.4s

roles: amount 1, audit 2, category 2, date 2, other 4, who 5

## when

PO_DATE
  2025      7.8K  ##############################
  2026      2.2K  ########

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 9.8K | 0 | 8.2K | 3.18M | 78.74M | 2.21B |

## who

BUSINESS_UNIT_NAME by rows
      2.3K  Department of Transportation
       961  Department of Corrections
       919  Mental Health & Subst Abuse Sv
       466  Dept of Environmental Quality
       422  Department of Veterans Affairs
       407  Mgmt and Enterprise Services
       377  Oklahoma Military Department
       330  State Bureau of Investigation
       313  Attorney General
       297  Department of Agriculture
       241  Tourism and Recreation Dept.
       186  OK DEP AEROSPACE & AERONAUTICS
       172  Department of Education
       169  District Attorneys Council
       161  Energy Resources Board
       148  Department of Commerce
       141  Office of Juvenile Affairs
       109  Okla Space Industry Devel Auth
       106  Alcoholic Bev Laws Enforce
       102  Council on Law Enfc Ed & Trng

BUSINESS_UNIT_NAME by dollars
       1.14B     2.3K rows  Department of Transportation
     382.21M      919 rows  Mental Health & Subst Abuse Sv
     192.17M      407 rows  Mgmt and Enterprise Services
      63.38M      313 rows  Attorney General
      62.40M      186 rows  OK DEP AEROSPACE & AERONAUTICS
      54.76M      141 rows  Office of Juvenile Affairs
      52.93M       10 rows  OSU Medical Authority
      30.28M      297 rows  Department of Agriculture
      27.99M      466 rows  Dept of Environmental Quality
      25.55M      109 rows  Okla Space Industry Devel Auth
      22.20M      422 rows  Department of Veterans Affairs
      19.38M      961 rows  Department of Corrections
      14.36M      169 rows  District Attorneys Council
      12.55M       91 rows  OK Medical Marijuana Authority
      10.40M       50 rows  Oklahoma Lottery Commission
       9.34M       45 rows  Historical Society
       7.57M      330 rows  State Bureau of Investigation
       7.51M       50 rows  JD McCarty Center
       7.48M       36 rows  Insurance Department
       7.34M      161 rows  Energy Resources Board

VENDOR by rows
       679  OFFICE OF MANAGEMENT & ENTERPRISE SVCS
       400  OKLAHOMA DEPARTMENT OF CORRECTIONS
       394  DELL FINANCIAL SERVICES LLC
       331  STANDLEY SYSTEMS LLC
       253  AUTHORITY ORDER VENDOR
       213  DELL MARKETING LP
       177  SHI INTERNATIONAL CORP
       164  MENTAL HEALTH AND SUBSTANCE ABUSE SERV
       149  ORION SECURITY SOLUTIONS LLC
       137  CENTRAL SALT LLC
       136  SOUTH CENTRAL INDUSTRIES INC
       129  W W GRAINGER INC
       110  THERMO FISHER SCIENTIFIC INC
       108  COMDATA INC
        79  CARAHSOFT TECHNOLOGY CORP
        79  AUTHORITY ORDER-PCARD
        77  ACTION SAFETY SUPPLY CO LLC
        75  SYNERGY DATACOM SUPPLY INC
        74  STAPLES INC
        73  GALLS LLC

VENDOR by dollars
     330.03M      253 rows  AUTHORITY ORDER VENDOR
     200.33M       22 rows  OKLAHOMA HEALTH CARE AUTHORITY
     144.77M      164 rows  MENTAL HEALTH AND SUBSTANCE ABUSE SERV
     114.01M        9 rows  ROBINSON CONSTRUCTION LLC
      76.42M        1 rows  DUIT CONSTRUCTION COMPANY INC
      59.17M        8 rows  C3 CONSTRUCTION INC
      52.42M       16 rows  THE CUMMINS CONSTRUCTION COMPANY INC
      45.95M       49 rows  OFFICE OF JUVENILE AFFAIRS
      38.78M        5 rows  OVERLAND CORPORATION
      37.11M       17 rows  OSU-CENTER FOR HEALTH SCIENCES
      35.34M       27 rows  CAPITOL IMPROVEMENT AUTHORITY
      34.94M        4 rows  SHERWOOD CONSTRUCTION CO INC
      30.89M        1 rows  OSU MEDICAL AUTHORITY
      29.71M       55 rows  OKLAHOMA STATE UNIVERSITY
      25.92M      679 rows  OFFICE OF MANAGEMENT & ENTERPRISE SVCS
      25.11M        6 rows  BECCO CONTRACTORS INC
      24.82M       33 rows  OK DEPT OF AEROSPACE AND AERONAUTICS
      22.69M        2 rows  ALLEN CONTRACTING INC
      15.75M        2 rows  RUDY CONSTRUCTION CO
      15.67M       10 rows  BUILT RIGHT CONSTRUCTION LLC

BUSINESS_UNIT by rows
      2.3K  34500
       961  13100
       919  45200
       466  29200
       422  65000
       407  9000
       377  2500
       330  30800
       313  4900
       297  4000
       241  56600
       186  6000
       172  26500
       169  22000
       161  35900
       148  16000
       141  40000
       109  34600
       106  3000
       102  41500

BUSINESS_UNIT by dollars
       1.14B     2.3K rows  34500
     382.21M      919 rows  45200
     192.17M      407 rows  9000
      63.38M      313 rows  4900
      62.40M      186 rows  6000
      54.76M      141 rows  40000
      52.93M       10 rows  77500
      30.28M      297 rows  4000
      27.99M      466 rows  29200
      25.55M      109 rows  34600
      22.20M      422 rows  65000
      19.38M      961 rows  13100
      14.36M      169 rows  22000
      12.55M       91 rows  45500
      10.40M       50 rows  43500
       9.34M       45 rows  35000
       7.57M      330 rows  30800
       7.51M       50 rows  67000
       7.48M       36 rows  38500
       7.34M      161 rows  35900

DESC by rows
       567  SERVICE: Highway Engineering Services
       221  ROADWAY: Road construction services
       202  GRANT:Federal Funding to Subdivisions; Federal Grants that pass throug
       117  GRANT:Funding to Subdivisions; Grants that pass through State Agency t
       111  GRANT:Aviation Education Grants
       107  SERVICE:Environmental Remediation Services. Furnish All Labor, Materia
        73  GRANT: pass-thru funding for Forestry Cost-Share assistance grants.
        71  General Laboratory Supplies
        67  SERVICE: Airport Runway Construction
        65  FUEL SRVC: Allowable charges
        62  ENGINEERING SRVS: Right of way utility specialist contracts
        60  Laptop Computer Lease
        60  REQ 2650014020 - Dell Precision 3480 - SoonerStart
        54  AUTHORITY ORDER: Purchase Card
        54  SW0699 Herbicide, Fertilizer, and Related Chemicals
        47  Network Cable and Accessories
        47  Class "A" Sand
        44  PACT FUNDS
        44  SERVICE:Mapping Services, Digitized (see 0962-52 for Standard Mapping 
        44  Opioid Abatement Grant

DESC by dollars
     626.20M      221 rows  ROADWAY: Road construction services
     126.74M      567 rows  SERVICE: Highway Engineering Services
     106.29M       24 rows  AUTHORITY ORDER: Emergency Purchases (Small Dollar) less tha
      94.65M       10 rows  .
      65.66M        1 rows  88 Payroll Encumbrance
      62.82M        1 rows  CCBHC Demonstration
      61.04M       67 rows  SERVICE: Airport Runway Construction
      60.07M      202 rows  GRANT:Federal Funding to Subdivisions; Federal Grants that p
      50.00M       44 rows  PACT FUNDS
      45.72M        1 rows  Outpatient Behavioral Health - TXIX
      30.89M        1 rows  REIMBURSEMENT FOR CONSTRUCTION OF NEW TULSA PSYCHIATRIC CARE
      28.93M        1 rows  Pass through of GME appropriations from Legislature
      25.45M        1 rows  Inpatient Behavioral Health - TXIX
      19.42M        1 rows  Payroll 200212/19601
      18.36M        1 rows  Enhanced Tier Payment System (ETPS)(19601/3003199)
      17.55M       44 rows  Opioid Abatement Grant
      17.30M       30 rows  Domestic Violence and Sexual Assault Services Contract
      16.00M        1 rows  10 Payroll Encumbrance
      15.85M        1 rows  2002011/19601
      15.30M        1 rows  Outpatient Behavioral Health – CHP

## who x when

BUSINESS_UNIT_NAME by PO_DATE, dollars = AMOUNT
  Alcoholic Bev Laws Enforce                2025:1.38M 2026:785.3K
  Attorney General                          2025:56.10M 2026:7.28M
  Council on Law Enfc Ed & Trng             2025:885.8K 2026:103.3K
  Department of Agriculture                 2025:26.22M 2026:4.06M
  Department of Commerce                    2025:2.65M 2026:12.8K
  Department of Corrections                 2025:12.20M 2026:7.18M
  Department of Education                   2025:1.94M 2026:99.7K
  Department of Transportation              2025:885.07M 2026:253.35M
  Department of Veterans Affairs            2025:21.97M 2026:230.9K
  Dept of Environmental Quality             2025:14.66M 2026:13.33M
  District Attorneys Council                2025:11.27M 2026:3.10M
  Energy Resources Board                    2025:6.53M 2026:815.6K
  Historical Society                        2025:4.32M 2026:5.02M
  Insurance Department                      2025:7.12M 2026:358.1K
  JD McCarty Center                         2025:7.51M 2026:100
  Mental Health & Subst Abuse Sv            2025:360.00M 2026:22.21M
  Mgmt and Enterprise Services              2025:189.36M 2026:2.81M
  OK DEP AEROSPACE & AERONAUTICS            2025:58.98M 2026:3.42M
  OK Medical Marijuana Authority            2025:12.29M 2026:266.2K
  OSU Medical Authority                     2025:44.93M 2026:8.00M
  Office of Juvenile Affairs                2025:54.70M 2026:64.7K
  Okla Space Industry Devel Auth            2025:25.55M 2026:5.0K
  Oklahoma Lottery Commission               2025:260.8K 2026:10.14M
  Oklahoma Military Department              2025:4.87M 2026:683.5K
  State Bureau of Investigation             2025:4.52M 2026:3.05M
  Tourism and Recreation Dept.              2025:2.23M 2026:39

VENDOR by PO_DATE, dollars = AMOUNT
  ACTION SAFETY SUPPLY CO LLC               2025:2.64M 2026:10.14M
  AUTHORITY ORDER VENDOR                    2025:324.90M 2026:5.13M
  AUTHORITY ORDER-PCARD                     2025:1.04M 2026:239.3K
  C3 CONSTRUCTION INC                       2025:59.17M
  CAPITOL IMPROVEMENT AUTHORITY             2025:34.07M 2026:1.27M
  CARAHSOFT TECHNOLOGY CORP                 2025:3.77M 2026:848.1K
  CENTRAL SALT LLC                          2025:3.54M
  COMDATA INC                               2025:4.06M 2026:145.6K
  DELL FINANCIAL SERVICES LLC               2025:1.64M 2026:655.0K
  DELL MARKETING LP                         2025:414.3K 2026:740.3K
  DUIT CONSTRUCTION COMPANY INC             2025:76.42M
  GALLS LLC                                 2025:155.0K 2026:3.7K
  MENTAL HEALTH AND SUBSTANCE ABUSE SERV    2025:144.74M 2026:33.6K
  OFFICE OF JUVENILE AFFAIRS                2025:45.95M
  OFFICE OF MANAGEMENT & ENTERPRISE SVCS    2025:23.84M 2026:2.09M
  OKLAHOMA DEPARTMENT OF CORRECTIONS        2025:1.10M 2026:208.7K
  OKLAHOMA HEALTH CARE AUTHORITY            2025:173.61M 2026:26.71M
  ORION SECURITY SOLUTIONS LLC              2025:213.7K 2026:26.6K
  OSU-CENTER FOR HEALTH SCIENCES            2025:37.07M 2026:40.9K
  OVERLAND CORPORATION                      2025:38.78M
  ROBINSON CONSTRUCTION LLC                 2025:8.34M 2026:105.67M
  SHERWOOD CONSTRUCTION CO INC              2025:10.37M 2026:24.57M
  SHI INTERNATIONAL CORP                    2025:3.24M 2026:648.7K
  SOUTH CENTRAL INDUSTRIES INC              2025:490.2K 2026:125.80
  STANDLEY SYSTEMS LLC                      2025:98.5K 2026:143.9K
  STAPLES INC                               2025:8.4K 2026:32.7K
  SYNERGY DATACOM SUPPLY INC                2025:133.4K 2026:8.5K
  THE CUMMINS CONSTRUCTION COMPANY INC      2025:52.42M
  THERMO FISHER SCIENTIFIC INC              2025:793.4K 2026:660.4K
  W W GRAINGER INC                          2025:343.5K 2026:21.9K

## what

ORIGIN: EXC 55%, OSF 21%, AGY 13%, CHG 11%, CP 0%, LSG 0%

PO_TYPE: RLSE 30%, ITRL 23%, IAGY 20%, SUBR 9%, DOT 9%, AO 3%, ITAG 2%, OMKT 2%, PYE 1%, PCAO 1%, UTIL 1%, GSAV 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BUSINESS_UNIT | who | 104 | 0 | 34500 2.3K; 13100 961; 45200 919; 29200 466 |
| BUSINESS_UNIT_NAME | who | 104 | 0 | Department of Transportat 2.3K; Department of Corrections 961; Mental Health & Subst Abu 919; Dept of Environmental Qua 466 |
| PO_ID | other | 5.7K | 0 | 4529069685 128; 4529069586 107; 259008574 91; 2929026476 71 |
| LINE_NBR | other | 101 | 0 | 1 5.7K; 2 1.2K; 3 639; 4 453 |
| VENDOR | who | 1.4K | 0 | OFFICE OF MANAGEMENT & EN 679; OKLAHOMA DEPARTMENT OF CO 400; DELL FINANCIAL SERVICES L 394; STANDLEY SYSTEMS LLC 331 |
| DESC | who | 5.5K | 0 | SERVICE: Highway Engineer 567; ROADWAY: Road constructio 223; GRANT:Federal Funding to  203; GRANT:Aviation Education  134 |
| AMOUNT | amount | 6.1K | 223 | 5000 119; 25000 110; 10000 106; 1000 104 |
| PO_DATE | date | 177 | 0 | 2025-08-13T00:00:00 235; 2025-09-23T00:00:00 194; 2025-08-24T00:00:00 187; 2025-07-15T00:00:00 164 |
| PO_DATE_EXCEL | other | 179 | 0 | 45880 235; 45921 194; 45891 187; 45851 164 |
| ORIGIN | category | 6 | 0 | EXC 5.5K; OSF 2.1K; AGY 1.3K; CHG 1.1K |
| PO_TYPE | category | 18 | 0 | RLSE 2.9K; ITRL 2.3K; IAGY 2.0K; SUBR 907 |
| FLAGGED_AS_DIRECT_PO | other | 1 | 0 | No 10.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:43:25.41487 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 58e85b5e-4774-4355-bb49-5 10.0K |
| SRC_SHA256 | who | 1 | 0 | 3ac9973f926643dfe3abf16b2 10.0K |
