# PORTAL_CKA_CALIFORNIA_OPEN_1424436F0D

rows 10.0K  columns 14  scan 4.0s

roles: amount 1, audit 2, category 6, date 1, id 1, other 1, who 3

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 10.0K | -62.13M | 0 | 26.81M | 614.59M | 16.15B |

## who

ENTITY_NAME by rows
        63  Access Services for Los Angeles County CTSA - Specialized Service
        62  Alameda - Specialized Service
        56  Arcata
        50  Alameda-Contra Costa Transit District
        50  Arvin
        47  Corcoran
        45  Gold Coast Transit District
        45  Exeter
        44  Amador Transit
        44  Madera
        44  Eastern Contra Costa County Transit Authority - Specialized Service
        44  Palos Verdes Peninsula Transportation Authority
        44  Butte Regional Transit - Specialized Service
        44  Calaveras County
        44  North Coast Railroad Authority
        44  Montebello - Specialized Service
        44  Downey - Specialized Service
        44  Los Angeles County Metropolitan Transportation Authority - Specialized
        44  Morro Bay
        44  Los Angeles - Specialized Service

ENTITY_NAME by dollars
       5.07B       44 rows  Los Angeles County Metropolitan Transportation Authority
       1.35B       50 rows  Alameda-Contra Costa Transit District
       1.06B       22 rows  San Francisco
       1.01B       22 rows  San Francisco Bay Area Rapid Transit District
     514.77M       22 rows  Santa Clara Valley Transportation Authority
     501.27M       63 rows  Access Services for Los Angeles County CTSA - Specialized Se
     475.91M       44 rows  Orange County Transportation Authority
     463.96M       44 rows  Peninsula Corridor Joint Powers Board
     360.41M       22 rows  Southern California Regional Rail Authority
     306.94M       44 rows  Golden Gate Bridge Highway and Transportation District
     244.89M       44 rows  Foothill Transit
     221.18M       22 rows  Sacramento Regional Transit System
     219.62M       44 rows  North County Transit District
     213.65M       44 rows  Long Beach Public Transportation Company
     202.14M       44 rows  Los Angeles
     195.92M       44 rows  Omnitrans
     180.38M       44 rows  Los Angeles County Metropolitan Transportation Authority - S
     164.51M       44 rows  Orange County Transportation Authority - Specialized Service
     161.12M       22 rows  San Diego Trolley Inc.
     155.38M       22 rows  San Mateo County Transit District

CITY_STATE by rows
       198  Los Angeles, CA
       176  Eureka, CA
       176  San Francisco, CA
       176  Bakersfield, CA
       176  Fresno, CA
       154  Stockton, CA
       138  Oakland, CA
       132  Ukiah, CA
       132  Oceanside, CA
       110  Petaluma, CA
       110  San Luis Obispo, CA
       110  Auburn, CA
       110  Modesto, CA
        91  Chico, CA
        88  Clovis, CA
        88  Lompoc, CA
        88  Downey, CA
        88  Banning, CA
        88  Folsom, CA
        88  Norwalk, CA

CITY_STATE by dollars
       5.84B      198 rows  Los Angeles, CA
       2.46B      138 rows  Oakland, CA
       1.45B      176 rows  San Francisco, CA
     640.42M       88 rows  Orange, CA
     636.25M       88 rows  San Carlos, CA
     536.12M       44 rows  San Jose, CA
     501.27M       63 rows  El Monte, CA
     405.79M       66 rows  San Diego, CA
     276.74M       88 rows  Sacramento, CA
     244.89M       44 rows  West Covina, CA
     244.76M      132 rows  Oceanside, CA
     229.01M       88 rows  San Bernardino, CA
     215.47M       88 rows  Long Beach, CA
     164.28M      154 rows  Stockton, CA
     142.40M      176 rows  Fresno, CA
     108.33M       88 rows  Monterey, CA
     100.22M       44 rows  Santa Monica, CA
      98.38M       66 rows  Riverside, CA
      94.21M      176 rows  Bakersfield, CA
      87.13M       88 rows  Concord, CA

SRC_SHA256 by rows
     10.0K  6bed5e29b9ff8028623cf4656251390766735ffc784fa951f01a9a5b939f94fe

SRC_SHA256 by dollars
      16.15B    10.0K rows  6bed5e29b9ff8028623cf4656251390766735ffc784fa951f01a9a5b939f

## who x when

ENTITY_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = VALUE
  Access Services for Los Angeles County C  2026:501.27M
  Alameda - Specialized Service             2026:1.79M
  Alameda-Contra Costa Transit District     2026:1.35B
  Amador Transit                            2026:4.17M
  Arcata                                    2026:3.58M
  Arvin                                     2026:2.10M
  Butte Regional Transit - Specialized Ser  2026:6.85M
  Calaveras County                          2026:1.33M
  Corcoran                                  2026:2.12M
  Downey - Specialized Service              2026:6.65M
  Eastern Contra Costa County Transit Auth  2026:7.49M
  Exeter                                    2026:-337
  Foothill Transit                          2026:244.89M
  Gold Coast Transit District               2026:53.95M
  Golden Gate Bridge Highway and Transport  2026:306.94M
  Los Angeles - Specialized Service         2026:24.74M
  Los Angeles County Metropolitan Transpor  2026:5.07B
  Los Angeles County Metropolitan Transpor  2026:180.38M
  Madera                                    2026:3.64M
  Montebello - Specialized Service          2026:885.5K
  Morro Bay                                 2026:782.4K
  North Coast Railroad Authority            2026:4.36M
  Orange County Transportation Authority    2026:475.91M
  Palos Verdes Peninsula Transportation Au  2026:5.28M
  Peninsula Corridor Joint Powers Board     2026:463.96M
  Sacramento Regional Transit System        2026:221.18M
  San Francisco                             2026:1.06B
  San Francisco Bay Area Rapid Transit Dis  2026:1.01B
  Santa Clara Valley Transportation Author  2026:514.77M
  Southern California Regional Rail Author  2026:360.41M

CITY_STATE by INGESTED_AT  LOAD STAMP, not an event date, dollars = VALUE
  Auburn, CA                                2026:34.56M
  Bakersfield, CA                           2026:94.21M
  Banning, CA                               2026:4.02M
  Chico, CA                                 2026:22.15M
  Clovis, CA                                2026:12.85M
  Downey, CA                                2026:9.64M
  El Monte, CA                              2026:501.27M
  Eureka, CA                                2026:19.49M
  Folsom, CA                                2026:6.39M
  Fresno, CA                                2026:142.40M
  Lompoc, CA                                2026:5.35M
  Long Beach, CA                            2026:215.47M
  Los Angeles, CA                           2026:5.84B
  Modesto, CA                               2026:54.54M
  Monterey, CA                              2026:108.33M
  Norwalk, CA                               2026:31.63M
  Oakland, CA                               2026:2.46B
  Oceanside, CA                             2026:244.76M
  Orange, CA                                2026:640.42M
  Petaluma, CA                              2026:60.92M
  Sacramento, CA                            2026:276.74M
  San Bernardino, CA                        2026:229.01M
  San Carlos, CA                            2026:636.25M
  San Diego, CA                             2026:405.79M
  San Francisco, CA                         2026:1.45B
  San Jose, CA                              2026:536.12M
  San Luis Obispo, CA                       2026:22.36M
  Stockton, CA                              2026:164.28M
  Ukiah, CA                                 2026:17.73M
  West Covina, CA                           2026:244.89M

## what

FISCAL_YEAR: 2018 61%, 2019 38%, 2017 0%, 2007 0%, 2024 0%, 2006 0%, 2025 0%

TYPE: Expenditures 99%, Expenses 1%

FORM_TABLE: Statement of Revenues, Expense 99%, TO_INCOME_STAT_OPEXP 1%

CATEGORY: Operating Expenses 68%, Nonoperating Expenses 32%

SUBCATEGORY: Materials and Supplies 19%, Labor 19%, Depreciation 6%, Services 6%, Capital Leases 6%, Other Nonoperating Expenses 6%, Loss on Disposal of Capital As 6%, Voluntary Nonexchange Transact 6%, Related Parties Lease Agreemen 6%, Operating Lease Expenses 6%, Interest Expense 6%, Other Operating Expenses 6%

LINE_DESCRIPTION: Services 8%, Fringe Benefits 8%, Other Salaries and Wages 8%, Fuel and Lubricants 8%, Operators Salaries and Wages 8%, Tires and Tubes 8%, Interest Expense 8%, Purchased Transportation 8%, Amortization of Intangibles 8%, Taxes 8%, Utilities 8%, Other Materials and Supplies 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ENTITY_NAME | who | 292 | 0 | Plumas County 66; Pleasanton - Specialized  66; Placer County 66; Pismo Beach - Specialized 66 |
| FISCAL_YEAR | category | 7 | 0 | 2018 6.1K; 2019 3.8K; 2017 42; 2007 41 |
| TYPE | category | 2 | 0 | Expenditures 9.9K; Expenses 90 |
| FORM_TABLE | category | 2 | 0 | Statement of Revenues, Ex 9.9K; TO_INCOME_STAT_OPEXP 90 |
| CATEGORY | category | 2 | 0 | Operating Expenses 6.8K; Nonoperating Expenses 3.2K |
| SUBCATEGORY | category | 18 | 0 | Materials and Supplies 1.4K; Labor 1.4K; Depreciation 463; Services 452 |
| LINE_DESCRIPTION | category | 28 | 0 | Services 459; Fringe Benefits 459; Other Salaries and Wages 458; Fuel and Lubricants 457 |
| VALUE | amount | 3.9K | 0 | 0 6.1K; 436130 20; 119553 20; 342930 20 |
| CITY_STATE | who | 164 | 0 | Los Angeles, CA 198; Bakersfield, CA 176; Eureka, CA 176; San Francisco, CA 176 |
| ZIP_CODE | other | 205 | 0 | 93721 176; 95482 132; 95501 132; 95603 110 |
| ROW_NUMBER | id | 9.8K | 0 | 201911141018 50; 201911141019 50; 201911141020 50; 201911141021 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:04:45.27250 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | acc417e1-f22a-42bf-a709-3 10.0K |
| SRC_SHA256 | who | 1 | 0 | 6bed5e29b9ff8028623cf4656 10.0K |
