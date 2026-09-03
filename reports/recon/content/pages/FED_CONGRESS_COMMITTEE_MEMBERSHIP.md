# FED_CONGRESS_COMMITTEE_MEMBERSHIP

rows 3.9K  columns 11  scan 2.2s

roles: audit 2, category 4, who 5

## who

MEMBER_NAME by rows
        22  Jeanne Shaheen
        22  Deb Fischer
        20  John Boozman
        20  Jack Reed
        19  Christopher A. Coons
        19  Roger F. Wicker
        19  Gary C. Peters
        18  Brian Schatz
        18  Shelley Moore Capito
        18  Katie Boyd Britt
        18  Jeff Merkley
        18  Patty Murray
        18  Mike Rounds
        18  Amy Klobuchar
        17  John Kennedy
        17  Jerry Moran
        17  Jon Husted
        17  John Cornyn
        17  Ted Cruz
        17  Bill Hagerty

COMMITTEE_NAME by rows
        66  House Committee on Transportation and Infrastructure
        62  House Committee on Appropriations
        57  House Committee on Armed Services
        54  House Committee on Energy and Commerce
        53  House Committee on Financial Services
        53  House Committee on Agriculture
        51  House Committee on Transportation and Infrastructure -- Highways and T
        50  House Committee on Foreign Affairs
        47  House Committee on Oversight and Government Reform
        45  House Committee on Ways and Means
        45  House Committee on Natural Resources
        42  House Committee on the Judiciary
        39  House Committee on Transportation and Infrastructure -- Aviation
        39  House Committee on Science, Space, and Technology
        37  House Committee on the Budget
        36  House Committee on Education and Workforce
        31  House Committee on Transportation and Infrastructure -- Water Resource
        31  House Committee on Homeland Security
        30  House Committee on Energy and Commerce -- Health
        30  House Committee on Transportation and Infrastructure -- Railroads, Pip

BIOGUIDE by rows
        22  S001181
        22  F000463
        20  R000122
        20  B001236
        19  P000595
        19  C001088
        19  W000437
        18  K000367
        18  S001194
        18  R000605
        18  M001176
        18  C001047
        18  M001111
        18  B001319
        17  M001244
        17  H000601
        17  C001098
        17  C001056
        17  P000145
        17  H001104

COMMITTEE_CODE by rows
        66  HSPW
        62  HSAP
        57  HSAS
        54  HSIF
        53  HSAG
        53  HSBA
        51  HSPW12
        50  HSFA
        47  HSGO
        45  HSII
        45  HSWM
        42  HSJU
        39  HSSY
        39  HSPW05
        37  HSBU
        36  HSED
        31  HSHM
        31  HSPW02
        30  HSPW14
        30  HSIF03

## what

IS_SUBCOMMITTEE: True 66%, False 34%

PARTY: majority 56%, minority 44%

RANK: 1 13%, 2 13%, 3 13%, 4 13%, 5 11%, 6 9%, 7 7%, 8 6%, 9 5%, 10 4%, 11 3%, 12 2%

TITLE: Ranking Member 36%, Chairman 23%, Ex Officio 19%, Chair 13%, Vice Chair 6%, Vice Chairman 2%, Chairwoman 1%, Vice Chairwoman 0%, Cochairman 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COMMITTEE_CODE | who | 224 | 0 | HSPW 66; HSAP 62; HSAS 57; HSIF 54 |
| COMMITTEE_NAME | who | 228 | 0 | House Committee on Transp 66; House Committee on Approp 62; House Committee on Armed  57; House Committee on Energy 54 |
| IS_SUBCOMMITTEE | category | 2 | 0 | True 2.5K; False 1.3K |
| BIOGUIDE | who | 533 | 0 | J000304 22; F000246 22; S001189 22; M000194 22 |
| MEMBER_NAME | who | 530 | 0 | Ronny Jackson 22; Pat Fallon 22; Austin Scott 22; Nancy Mace 22 |
| PARTY | category | 2 | 0 | majority 2.2K; minority 1.7K |
| RANK | category | 35 | 0 | 1 455; 2 451; 3 448; 4 427 |
| TITLE | category | 10 | 3.3K | Ranking Member 217; Chairman 143; Ex Officio 118; Chair 79 |
| _INGESTED_AT | audit | 1 | 0 | 1782874830640269 3.9K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 7a91b1de-6ec3-4ef7-8049-0 3.9K |
| _SRC_SHA256 | who | 1 | 0 | c7693b813aff8c012f749dd54 3.9K |
