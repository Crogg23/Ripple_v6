# CA_LOBBY_FIRM_EMPLOYER

rows 170  columns 14  scan 5.1s

roles: amount 2, audit 2, category 4, date 2, empty 1, other 1, who 2

## when

RPT_START
  2001       170  ##############################

RPT_END
  2001       170  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PER_TOTAL | 170 | 0 | 7.1K | 52.2K | 60.0K | 1.46M |
| CUM_TOTAL | 170 | 0 | 12.9K | 93.5K | 123.0K | 2.86M |

## who

EMPLOYER_NAME by rows
         2  ENGINEERS AND SCIENTISTS OF CALIFORNIA LOCAL 20 IFPTE AFL-CIO & CLC
         1  BLUE SHIELD OF CALIFORNIA
         1  Auerbach
         1  United Transportation Services INC
         1  ASSOCIATION OF CALIFORNIA CARE OPERATORS INC
         1  CALIFORNIA FEDERATION OF TEACHERS
         1  Knowaste L.L.C.
         1  STUART & ASSOCIATES
         1  F.A.I.R. Faculty Attempting to Improve Retirement
         1  CALIFORNIA REFUSE REMOVAL COUNCIL SOUTHERN DISTRICT
         1  California Association of County Treasurers and Tax Collectors
         1  Educational Testing Service
         1  CALIFORNIA COALITION OF AGENCIES SERVING THE DEAF
         1  Camp Ph.D
         1  Los Angeles County Probation Department Union AFSCME Local 685
         1  Will Rogers Polo Club
         1  SONOMA COUNTY WATER AGENCY
         1  California Governmental Affairs Council of the ASSE
         1  Riley & Reiner
         1  BROWN & WILLIAMSON TOBACCO CORPORATION

EMPLOYER_NAME by dollars
       60.0K        1 rows  BLUE SHIELD OF CALIFORNIA
       54.6K        1 rows  Los Angeles Community College District
       51.2K        1 rows  CALIFORNIA SPA AND POOL INDUSTRY EDUCATION COUNCIL
       32.7K        1 rows  CALIFORNIA STATE PIPE TRADES COUNCIL
       30.5K        1 rows  California Association of Health Underwriters
       30.4K        1 rows  California Association of Insurance and Financial Advisors
       25.7K        1 rows  FOREST PRODUCTS INDUSTRY NATIONAL LABOR MANAGEMENT COMMITTEE
       22.6K        1 rows  CALIFORNIA STATE ASSOCIATION OF ELECTRICAL WORKERS
       22.3K        1 rows  CALIFORNIA FINANCIAL SERVICES ASSOCIATION
       21.5K        1 rows  American College of Obstetricians and Gynecologists District
       20.9K        1 rows  Law Offices of John Lovell
       20.2K        1 rows  BROWN & WILLIAMSON TOBACCO CORPORATION
       19.7K        1 rows  Northern California Power Agency
       19.6K        1 rows  CALIFORNIA TEAMSTERS PUBLIC AFFAIRS COUNCIL
       19.5K        1 rows  County Alcohol and Drug Program Administrators' Assoc. of CA
       19.2K        1 rows  MONTEREY COUNTY OF
       18.8K        1 rows  Association for Los Angeles Deputy Sheriffs
       17.2K        1 rows  INTERNATIONAL BROTHERHOOD OF ELECTRICAL WORKERS LOCAL 1245
       16.2K        1 rows  San Joaquin County
       15.5K        1 rows  CALIFORNIA CORRECTIONAL PEACE OFFICERS ASSOCIATION

SRC_SHA256 by rows
       170  7749f80767c91b69fbcd0f50343b47e15f5cbcd8b1af35146b3b5ed5ee8c6ebd

SRC_SHA256 by dollars
       1.46M      170 rows  7749f80767c91b69fbcd0f50343b47e15f5cbcd8b1af35146b3b5ed5ee8c

## who x when

EMPLOYER_NAME by RPT_START, dollars = PER_TOTAL
  ASSOCIATION OF CALIFORNIA CARE OPERATORS  2001:2.9K
  American College of Obstetricians and Gy  2001:21.5K
  Auerbach                                  2001:750
  BLUE SHIELD OF CALIFORNIA                 2001:60.0K
  BROWN & WILLIAMSON TOBACCO CORPORATION    2001:20.2K
  CALIFORNIA COALITION OF AGENCIES SERVING  2001:9.0K
  CALIFORNIA FEDERATION OF TEACHERS         2001:9.0K
  CALIFORNIA FINANCIAL SERVICES ASSOCIATIO  2001:22.3K
  CALIFORNIA REFUSE REMOVAL COUNCIL SOUTHE  2001:13.1K
  CALIFORNIA SPA AND POOL INDUSTRY EDUCATI  2001:51.2K
  CALIFORNIA STATE ASSOCIATION OF ELECTRIC  2001:22.6K
  CALIFORNIA STATE PIPE TRADES COUNCIL      2001:32.7K
  California Association of County Treasur  2001:12.6K
  California Association of Health Underwr  2001:30.5K
  California Association of Insurance and   2001:30.4K
  California Governmental Affairs Council   2001:0
  Camp Ph.D                                 2001:4.0K
  ENGINEERS AND SCIENTISTS OF CALIFORNIA L  2001:9.0K
  Educational Testing Service               2001:9.0K
  F.A.I.R. Faculty Attempting to Improve R  2001:1.4K
  FOREST PRODUCTS INDUSTRY NATIONAL LABOR   2001:25.7K
  Knowaste L.L.C.                           2001:0
  Law Offices of John Lovell                2001:20.9K
  Los Angeles Community College District    2001:54.6K
  Los Angeles County Probation Department   2001:12.6K
  Riley & Reiner                            2001:0
  SONOMA COUNTY WATER AGENCY                2001:11.2K
  STUART & ASSOCIATES                       2001:15.0K
  United Transportation Services INC        2001:500
  Will Rogers Polo Club                     2001:0

SRC_SHA256 by RPT_START, dollars = PER_TOTAL
  7749f80767c91b69fbcd0f50343b47e15f5cbcd8  2001:1.46M

## what

FIRM_ID: 1147251 14%, 1231516 10%, 1147504 9%, 1147322 9%, 1147329 9%, 1147720 8%, 1147401 8%, 1147546 8%, 1147554 7%, 1147451 7%, 1147402 5%, 1147413 5%

FILING_ID: 767722 14%, 767982 10%, 767547 9%, 767589 9%, 768155 9%, 768138 8%, 767937 8%, 768146 8%, 766410 7%, 767627 7%, 765369 5%, 768049 5%

FILING_SEQUENCE: 0 91%, 1 9%

FIRM_NAME: CARTER LOBBYING FIRM, ART 14%, MC HUGH & ASSOCIATES 10%, BROAD, LAW OFFICES OF BARRY 9%, WAGERMAN ASSOCIATES, INC. 9%, CLINE COMPANY, ROBERT C. 9%, MC CALLUM GROUP, PATRICK 8%, JEA & ASSOCIATES 8%, PRICE CONSULTING 8%, GOVERNMENT AFFAIRS CONSULTING 7%, LOVELL, LAW OFFICES OF JOHN 7%, YARYAN, LAW OFFICES OF TIMOTHY 5%, WALSH AND ASSOCIATES, DANNY 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIRM_ID | category | 24 | 0 | 1147251 18; 1231516 13; 1147504 12; 1147322 12 |
| FILING_ID | category | 24 | 0 | 767722 18; 767982 13; 767547 12; 767589 12 |
| FILING_SEQUENCE | category | 2 | 0 | 0 155; 1 15 |
| FIRM_NAME | category | 24 | 0 | CARTER LOBBYING FIRM, ART 18; MC HUGH & ASSOCIATES 13; BROAD, LAW OFFICES OF BAR 12; WAGERMAN ASSOCIATES, INC. 12 |
| EMPLOYER_NAME | who | 170 | 0 | ENGINEERS AND SCIENTISTS  2; Los Angeles Community Col 1; Glendale Community Colleg 1; F.A.I.R. Faculty Attempti 1 |
| RPT_START | date | 1 | 0 | 4/1/2001 12:00:00 AM 170 |
| RPT_END | date | 1 | 0 | 6/30/2001 12:00:00 AM 170 |
| PER_TOTAL | amount | 124 | 0 | 0 21; 9000 7; 6000 5; 7500 5 |
| CUM_TOTAL | amount | 132 | 0 | 0 20; 15000 5; 12000 3; 3000 3 |
| LBY_ACTVTY | other | 127 | 25 | SB 27x SB 28x SB 8x SB 23 7; Subcontract client for Ac 5; No Activity This Quarter 4; AB 1016;  AB 5;  AB 145;  2 |
| EXT_LBY_ACTVTY | empty | 1 | 170 |  |
| INGESTED_AT | audit | 1 | 0 | 1785965875142453 170 |
| SOURCE_RUN_ID | audit | 1 | 0 | 43a35cd8-62ae-45f3-a065-7 170 |
| SRC_SHA256 | who | 1 | 0 | 7749f80767c91b69fbcd0f503 170 |
