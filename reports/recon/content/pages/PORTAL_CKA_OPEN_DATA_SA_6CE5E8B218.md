# PORTAL_CKA_OPEN_DATA_SA_6CE5E8B218

rows 2.4K  columns 18  scan 4.9s

roles: amount 2, audit 2, category 8, date 1, id 3, who 3

## when

INGESTED_AT
  2026      2.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 2.4K | 2.06M | 2.12M | 2.17M | 2.19M | 5.15B |
| Y | 2.4K | 13.66M | 13.71M | 13.78M | 13.78M | 33.32B |

## who

MSAG_NAME by rows
        14  W PYRON AVE
        12  KENDALIA AVE
        12  SPRINGVALE DR
        12  FIVE PALMS DR
        10  SHERMAN ST
        10  W ANSLEY BLVD
        10  MCCAULEY AVE
        10  EL SENDERO
         9  W VILLARET BLVD
         9  CERALVO ST
         8  S ELLISON DR
         8  W OLMOS DR
         8  STONEWALL AVE
         8  KNIGHTS CROSS DR
         8  W MAYFIELD
         8  MENEFEE BLVD
         8  BRIGGS AVE
         8  BENRUS
         8  CHERRY RIDGE DR
         8  BURR RD

MSAG_NAME by dollars
      29.69M       14 rows  W PYRON AVE
      25.48M       12 rows  KENDALIA AVE
      25.12M       12 rows  FIVE PALMS DR
      25.00M       12 rows  SPRINGVALE DR
      21.60M       10 rows  EL SENDERO
      21.40M       10 rows  SHERMAN ST
      21.21M       10 rows  MCCAULEY AVE
      21.18M       10 rows  W ANSLEY BLVD
      19.07M        9 rows  W VILLARET BLVD
      19.02M        9 rows  CERALVO ST
      17.15M        8 rows  BURR RD
      17.07M        8 rows  E PYRON AVE
      17.03M        8 rows  E AMBER
      17.03M        8 rows  KNIGHTS CROSS DR
      17.00M        8 rows  STONEWALL AVE
      16.99M        8 rows  W OLMOS DR
      16.97M        8 rows  FITCH ST
      16.95M        8 rows  W MAYFIELD
      16.93M        8 rows  CHERRY RIDGE DR
      16.91M        8 rows  DONALDSON AVE

PROJECTNAME by rows
      2.1K  Unknown
        10  SMO25-0119
         6  SMO22-0083
         6  SMO23-0151
         6  SMO23-0146
         5  SMO25-0114
         5  SMO22-0178
         4  SMO24-0131
         4  SMO22-0175
         4  SMO24-0125
         4  SMO21-0149
         4  SMO22-0086
         4  SMO25-0048
         4  SMO22-0082
         4  SMO19-0101
         4  SMO24-0135
         4  SMO23-0153
         4  SMO25-0118
         4  SMO22-0174
         4  SMO25-0287

PROJECTNAME by dollars
       4.42B     2.1K rows  Unknown
      21.40M       10 rows  SMO25-0119
      12.90M        6 rows  SMO23-0146
      12.82M        6 rows  SMO22-0083
      12.50M        6 rows  SMO23-0151
      10.83M        5 rows  SMO25-0114
      10.60M        5 rows  SMO22-0178
       8.65M        4 rows  SMO25-0113
       8.65M        4 rows  SMO22-0174
       8.65M        4 rows  SMO22-0082
       8.63M        4 rows  SMO21-0149
       8.63M        4 rows  SMO25-0118
       8.59M        4 rows  SMO25-0287
       8.58M        4 rows  SMO24-0125
       8.54M        4 rows  SMO25-0048
       8.54M        4 rows  SMO25-0110
       8.53M        4 rows  SMO21-0148
       8.52M        4 rows  SMO22-0086
       8.52M        4 rows  SMO19-0101
       8.48M        4 rows  SMO26-0065

SRC_SHA256 by rows
      2.4K  f1b88c1cacdcf6449838bd14a254e4ba2b77645ca46ca3fd26e399ed00da5d6c

SRC_SHA256 by dollars
       5.15B     2.4K rows  f1b88c1cacdcf6449838bd14a254e4ba2b77645ca46ca3fd26e399ed00da

## who x when

MSAG_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  BENRUS                                    2026:16.81M
  BRIGGS AVE                                2026:16.87M
  BURR RD                                   2026:17.15M
  CERALVO ST                                2026:19.02M
  CHERRY RIDGE DR                           2026:16.93M
  DONALDSON AVE                             2026:16.91M
  E AMBER                                   2026:17.03M
  E PYRON AVE                               2026:17.07M
  EL SENDERO                                2026:21.60M
  FITCH ST                                  2026:16.97M
  FIVE PALMS DR                             2026:25.12M
  KENDALIA AVE                              2026:25.48M
  KNIGHTS CROSS DR                          2026:17.03M
  MCCAULEY AVE                              2026:21.21M
  MENEFEE BLVD                              2026:16.89M
  S ELLISON DR                              2026:16.56M
  SHERMAN ST                                2026:21.40M
  SPRINGVALE DR                             2026:25.00M
  STONEWALL AVE                             2026:17.00M
  W ANSLEY BLVD                             2026:21.18M
  W MAYFIELD                                2026:16.95M
  W OLMOS DR                                2026:16.99M
  W PYRON AVE                               2026:29.69M
  W VILLARET BLVD                           2026:19.07M

PROJECTNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  SMO19-0101                                2026:8.52M
  SMO21-0148                                2026:8.53M
  SMO21-0149                                2026:8.63M
  SMO22-0082                                2026:8.65M
  SMO22-0083                                2026:12.82M
  SMO22-0086                                2026:8.52M
  SMO22-0174                                2026:8.65M
  SMO22-0175                                2026:8.37M
  SMO22-0178                                2026:10.60M
  SMO23-0146                                2026:12.90M
  SMO23-0151                                2026:12.50M
  SMO23-0153                                2026:8.48M
  SMO24-0125                                2026:8.58M
  SMO24-0131                                2026:8.43M
  SMO24-0135                                2026:8.39M
  SMO25-0048                                2026:8.54M
  SMO25-0110                                2026:8.54M
  SMO25-0113                                2026:8.65M
  SMO25-0114                                2026:10.83M
  SMO25-0118                                2026:8.63M
  SMO25-0119                                2026:21.40M
  SMO25-0287                                2026:8.59M
  SMO26-0065                                2026:8.48M
  Unknown                                   2026:4.42B

## what

MATERIALTYPE: Rubber 72%, Asphalt 27%, Recycled Rubber 0%

QUANTITY: 3 58%, 1 19%, 4 10%, 5 9%, 0 2%, 2 2%, 6 0%

CONDITION: Excellent 97%, Good 3%

JURISDICTION: San Antonio 100%, Converse 0%

DISTRICT: 3 16%, 4 13%, 5 13%, 1 13%, 7 11%, 6 9%, 2 8%, 10 8%, 8 4%, 9 4%, 0 1%

MAINTENANCERESPONSIBILITY: TBD 96%, COSA - Public Works Dept 4%

STATUS: TBD 96%, Active 4%

COMMENTS: Install per SMO 25%, Streetview 1-2022 13%, Streetview 6-2024 11%, SMO 2-2026 8%, Streetview 3-2024 8%, Streetview 3-2019 8%, Speed Hump #1 6%, Speed Hump #2 6%, Streetview 5-2019 6%, Streetview 4-2019 6%, Streetview 11-2022 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.4K | 0 | 2430 13; 2429 13; 2428 13; 2427 13 |
| SH_CARTID | id | 2.4K | 0 | SH_611424 13; SH_610571 13; SH_612234 13; SH_612142 13 |
| MATERIALTYPE | category | 3 | 0 | Rubber 1.8K; Asphalt 660; Recycled Rubber 11 |
| QUANTITY | category | 7 | 0 | 3 1.4K; 1 470; 4 240; 5 229 |
| CONDITION | category | 2 | 0 | Excellent 2.4K; Good 69 |
| MSAG_NAME | who | 853 | 14 | W PYRON AVE 16; FIVE PALMS DR 15; E AMBER 14; RIM ROCK TRL 13 |
| PROJECTNAME | who | 131 | 0 | Unknown 2.1K; SMO25-0119 10; SMO22-0083 6; SMO23-0151 6 |
| JURISDICTION | category | 2 | 0 | San Antonio 2.4K; Converse 8 |
| DISTRICT | category | 11 | 0 | 3 378; 4 323; 5 309; 1 304 |
| MAINTENANCERESPONSIBILITY | category | 2 | 0 | TBD 2.3K; COSA - Public Works Dept 99 |
| STATUS | category | 2 | 0 | TBD 2.3K; Active 101 |
| COMMENTS | category | 28 | 2.4K | Install per SMO 13; Streetview 1-2022 7; Streetview 6-2024 6; SMO 2-2026 4 |
| GLOBALID | id | 2.4K | 0 | 6e60e831-3fbf-4c5d-8ec0-6 13; d5cb3eb5-42d4-4e76-b5e5-1 13; ff770a67-eb93-4766-b862-3 13; 36b725bd-1877-496f-8ad4-0 13 |
| X | amount | 2.4K | 0 | 2096007.62444213 13; 2099830.10104914 13; 2102893.71696913 13; 2077010.45508747 13 |
| Y | amount | 2.4K | 0 | 13712067.6213107 13; 13720051.7556048 13; 13727985.1350792 13; 13717138.9343307 13 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:28:23.04853 2.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | f1cf3e5f-e615-4818-accd-0 2.4K |
| SRC_SHA256 | who | 1 | 0 | f1b88c1cacdcf6449838bd14a 2.4K |
