# PORTAL_SOC_TEXAS_OPEN_DATA_D83872D208

rows 239  columns 15  scan 5.4s

roles: amount 3, audit 2, category 2, date 2, other 4, who 3

## when

ORDER_DATE
  2015         9  ########
  2016        32  ###########################
  2017        22  ##################
  2018        36  ##############################
  2019        24  ####################
  2020        21  ##################
  2021        23  ###################
  2022        23  ###################
  2023        16  #############
  2024        22  ##################
  2025        11  #########

INGESTED_AT
  2026       239  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAYABLE_AMOUNT | 239 | 0 | 45.0K | 7.93M | 75.00M | 192.43M |
| ATTORNEY_FEES | 239 | 0 | 7.5K | 705.5K | 10.00M | 18.65M |
| COURT_COSTS | 239 | 0 | 0 | 3.1K | 17.0K | 36.4K |

## who

RESPONDENT_NAME by rows
         4  TEXAS RAIN HOLDING COMPANY, INC.
         3  *BURNETT, SHEA BROCK
         2  SUBURBAN UTILITY CO
         2  NORMAN BARNETT
         2  MAGELLAN TERMINALS HOLDINGS, L.P.
         2  Exxon Mobil Corporation
         1  BLACK, YOLANDA *
         1  GRAVES TIRE SERVICE *
         1  ATC WEST TEXAS, LLC *
         1  VAN DER HORST U.S.A. CORPORATION
         1  GEORGE W. JACKSON
         1  Seng Phet Souimaniphanh
         1  KARISHMA PROPERTIES, INC.
         1  CITY OF CORPUS CHRISTI
         1  J&S Water Company, L.L.C.
         1  PLANT MAINTENANCE SERVICES, L.L.C. *
         1  JASANI, AMEER ALI
         1  PASADENA REFINING SYSTEM, INC *
         1  GINEZ, RIGOBERTO *
         1  DOLORES A. LUKE

RESPONDENT_NAME by dollars
      75.00M        1 rows  *Audi of America, LLC
      57.01M        1 rows  *POLSTON, DAVID
      10.00M        1 rows  KMCO, LLC
       4.55M        1 rows  RESEARCH LABORATORIES, INC.
       3.00M        1 rows  PARKER SQUARE BANK *
       2.92M        2 rows  Exxon Mobil Corporation
       2.50M        1 rows  Houston Refining LP
       2.20M        1 rows  CITY OF HOUSTON
       2.00M        1 rows  The Dow Chemical Company
       2.00M        1 rows  Arkema Inc.
       1.60M        1 rows  ExxonMobil Oil Corporation
       1.49M        1 rows  E. I. DU PONT DE NEMOURS AND COMPANY
       1.45M        1 rows  Equistar Chemicals, LP
       1.30M        1 rows  TotalEnergies Petrochemicals & Refining USA, Inc.
       1.14M        1 rows  CITY OF CORPUS CHRISTI
       1.12M        1 rows  COMMERCIAL METALS COMPANY *
       1.10M        1 rows  PASADENA REFINING SYSTEM, INC.
       1.02M        1 rows  LyondellBasell Acetyls, LLC
       1.00M        1 rows  Pasadena Refining System, Inc.
      938.0K        2 rows  MAGELLAN TERMINALS HOLDINGS, L.P.

COUNTY by rows
        72  HARRIS
        14  ECTOR
        10  *MULTIPLE
         9  BEXAR
         6  TRAVIS
         6  HIDALGO
         6  DALLAS
         6  JEFFERSON
         5  BRAZORIA
         3  NOLAN
         3  HUNT
         3  LUBBOCK
         3  NUECES
         3  TOM GREEN
         3  WISE
         3  HOPKINS
         3  EL PASO
         2  GRAYSON
         2  SMITH
         2  MCLENNAN

COUNTY by dollars
     108.78M       72 rows  HARRIS
      57.11M        2 rows  COLORADO
       3.26M        6 rows  JEFFERSON
       3.00M        1 rows  WICHITA
       2.98M       10 rows  *MULTIPLE
       2.00M        5 rows  BRAZORIA
       1.78M        3 rows  NUECES
       1.48M       14 rows  ECTOR
       1.37M        9 rows  BEXAR
       1.05M        2 rows  SMITH
      652.7K        6 rows  DALLAS
      553.6K        3 rows  EL PASO
      498.9K        3 rows  HUNT
      490.7K        6 rows  HIDALGO
      475.0K        1 rows  CALHOUN
      473.8K        1 rows  HARDIN
      446.8K        3 rows  WISE
      445.9K        2 rows  CHAMBERS
      384.7K        2 rows  MONTGOMERY
      367.2K        1 rows  FORT BEND

SRC_SHA256 by rows
       239  ca440ba119d62b53a95282b8fd587868cabf4f82454099bb244a5f63ac8317ba

SRC_SHA256 by dollars
     192.43M      239 rows  ca440ba119d62b53a95282b8fd587868cabf4f82454099bb244a5f63ac83

## who x when

RESPONDENT_NAME by ORDER_DATE, dollars = PAYABLE_AMOUNT
  *Audi of America, LLC                     2024:75.00M
  *BURNETT, SHEA BROCK                      2024:0 2025:0
  *POLSTON, DAVID                           2025:57.01M
  ATC WEST TEXAS, LLC *                     2019:20.0K
  Arkema Inc.                               2024:2.00M
  BLACK, YOLANDA *                          2018:38.3K
  CITY OF CORPUS CHRISTI                    2021:1.14M
  CITY OF HOUSTON                           2021:2.20M
  DOLORES A. LUKE                           2019:473.8K
  Exxon Mobil Corporation                   2023:755.0K 2024:2.17M
  ExxonMobil Oil Corporation                2023:1.60M
  GEORGE W. JACKSON                         2021:53.2K
  GINEZ, RIGOBERTO *                        2021:5.0K
  GRAVES TIRE SERVICE *                     2020:135.6K
  Houston Refining LP                       2023:2.50M
  J&S Water Company, L.L.C.                 2024:70.0K
  JASANI, AMEER ALI                         2018:29.0K
  KARISHMA PROPERTIES, INC.                 2019:6.0K
  KMCO, LLC                                 2020:10.00M
  MAGELLAN TERMINALS HOLDINGS, L.P.         2022:938.0K
  NORMAN BARNETT                            2016:136.5K 2021:131.2K
  PARKER SQUARE BANK *                      2021:3.00M
  PASADENA REFINING SYSTEM, INC *           2018:195.0K
  PLANT MAINTENANCE SERVICES, L.L.C. *      2021:30.0K
  RESEARCH LABORATORIES, INC.               2025:4.55M
  SUBURBAN UTILITY CO                       2016:125.0K 2022:247.2K
  Seng Phet Souimaniphanh                   2023:198.7K
  TEXAS RAIN HOLDING COMPANY, INC.          2019:15.2K 2020:345.4K
  The Dow Chemical Company                  2025:2.00M
  VAN DER HORST U.S.A. CORPORATION          2018:120.8K

COUNTY by ORDER_DATE, dollars = PAYABLE_AMOUNT
  *MULTIPLE                                 2016:136.5K 2019:0 2020:227.6K 2021:2.55M 2022:60.2K
  BEXAR                                     2018:680.9K 2019:55.2K 2020:16.5K 2021:298.6K 2024:314.6K
  BRAZORIA                                  2016:2.3K 2017:1.9K 2025:2.00M
  CALHOUN                                   2024:475.0K
  CHAMBERS                                  2018:435.0K 2021:10.8K
  COLORADO                                  2025:57.11M
  DALLAS                                    2016:21.0K 2018:253.6K 2019:329.5K 2020:0 2024:48.6K
  ECTOR                                     2015:0 2016:44.9K 2017:1.2K 2018:1.14M 2019:20.0K 2020:246.7K 2021:30.0K
  EL PASO                                   2017:73.0K 2019:185.6K 2022:295.0K
  FORT BEND                                 2018:367.2K
  GRAYSON                                   2015:0 2016:113.3K
  HARDIN                                    2019:473.8K
  HARRIS                                    2015:191.7K 2016:478.4K 2017:23.8K 2018:1.00M 2019:522.8K 2020:11.92M 2021:230.0K 2022:2.06M 2023:5.36M 2024:82.42M 2025:4.58M
  HIDALGO                                   2016:13.7K 2018:472.0K 2021:5.0K
  HOPKINS                                   2017:86.4K
  HUNT                                      2017:200.0K 2018:131.0K 2020:167.8K
  JEFFERSON                                 2015:23.6K 2018:15.8K 2022:324.9K 2023:2.90M
  LUBBOCK                                   2018:186.5K 2020:29.8K 2021:53.2K
  MCLENNAN                                  2017:117.3K 2019:10.0K
  MONTGOMERY                                2021:354.7K 2022:30.0K
  NOLAN                                     2024:0 2025:0
  NUECES                                    2018:61.0K 2021:1.14M 2022:588.0K
  SMITH                                     2019:814.6K 2023:231.7K
  TOM GREEN                                 2016:54.8K 2022:22.1K
  TRAVIS                                    2015:10.8K 2016:35.2K 2019:10.5K 2024:34.0K
  WICHITA                                   2021:3.00M
  WISE                                      2016:189.4K 2020:58.7K 2023:198.7K

## what

PROGRAM: MUNICIPAL SOLID WASTE 21%, AIR QUALITY 19%, MULTI-MEDIA 15%, PUBLIC WATER SUPPLY 14%, PETROLEUM STORAGE TANKS 12%, WATER QUALITY 11%, INDUSTRIAL AND HAZARDOUS WASTE 5%, DISTRICTS 2%, EMERGENCY RESPONSE 0%, DAM SAFETY 0%, DRY CLEANERS 0%

PENALTY_DEFERRED: 0 95%, 9900000 0%, 100000 0%, 40000 0%, 5663 0%, 7500 0%, 12000 0%, 10000 0%, 12500 0%, 8640 0%, 20000 0%, 170350 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PROGRAM | category | 11 | 0 | MUNICIPAL SOLID WASTE 51; AIR QUALITY 45; MULTI-MEDIA 37; PUBLIC WATER SUPPLY 33 |
| CASE_NO | other | 222 | 0 | 60270 4; 57465 3; 59656 3; 49998 3 |
| DISTRICT_COURT_DOCKET_NO | other | 234 | 0 | D-1-GN-24-000114 4; DC-18-18651 3; D-1-GN-19-002002 3; 2023-57660 2 |
| RESPONDENT_NAME | who | 231 | 0 | *BURNETT, SHEA BROCK 4; TEXAS RAIN HOLDING COMPAN 4; *LEUNG, ADA WING 2; *Craft-Turney Water Suppl 2 |
| TCEQ_ID | other | 152 | 0 | ZBA001A 56; 0 19; nan 10; 1010111 2 |
| COUNTY | who | 83 | 0 | HARRIS 72; ECTOR 14; *MULTIPLE 10; BEXAR 9 |
| ORDER_DATE | date | 224 | 0 | 2025-04-02T00:00:00.000 3; 2024-12-12T00:00:00.000 3; 2025-06-06T00:00:00.000 3; 2016-05-23T00:00:00.000 3 |
| PENALTY_ASSESSED | other | 193 | 0 | 0 13; 30000 6; 50000 4; 5000 4 |
| PENALTY_DEFERRED | category | 13 | 0 | 0 227; 9900000 1; 100000 1; 40000 1 |
| PAYABLE_AMOUNT | amount | 191 | 0 | 0 14; 10000 5; 30000 5; 5000 4 |
| ATTORNEY_FEES | amount | 129 | 0 | 0 18; 5000 16; 10000 10; 3000 9 |
| COURT_COSTS | amount | 18 | 0 | 0 219; 3115 2; 275 2; 365 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:08:46.98804 239 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6453b3c4-2a13-4d94-a85c-7 239 |
| SRC_SHA256 | who | 1 | 0 | ca440ba119d62b53a95282b8f 239 |
