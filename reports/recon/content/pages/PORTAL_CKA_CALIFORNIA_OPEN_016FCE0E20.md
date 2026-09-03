# PORTAL_CKA_CALIFORNIA_OPEN_016FCE0E20

rows 353  columns 7  scan 3.3s

roles: audit 2, category 1, date 1, other 2, who 2

## when

INGESTED_AT
  2026       353  ##############################

## who

FARM_NAME by rows
         1  ROCKING CHAIR FARM MARKETS
         1  BURNS BLOSSOM FARM LLC
         1  BRIGHT FARM
         1  BEE IN MY BONNET
         1  TWIN GIRLS FARMS
         1  BORBA FARMS
         1  BELLACIENDA
         1  CHARLOTTE'S PERENNIAL GARDENS
         1  CKL PRODUCE
         1  PIERCE FAMILY FARM
         1  HAPPY GOAT FARM
         1  WILDER WITCH FARMS
         1  LETICIA'S FARMS
         1  ESPINOSA FARMS
         1  COVERING GROUND FARMS
         1  UPCOUNTRY FARMS
         1  MP FAMILY FARM
         1  LUNA FARM
         1  B. VANG FARM
         1  C & J AG SERVICES

SRC_SHA256 by rows
       353  bd53721369e7c5321da66506736987aeb50e9cc0b9a759123d3a9a6d71a3e0cc

## who x when

FARM_NAME by INGESTED_AT  LOAD STAMP, not an event date
  B. VANG FARM                              2026:1
  BEE IN MY BONNET                          2026:1
  BELLACIENDA                               2026:1
  BORBA FARMS                               2026:1
  BRIGHT FARM                               2026:1
  BURNS BLOSSOM FARM LLC                    2026:1
  C & J AG SERVICES                         2026:1
  CHARLOTTE'S PERENNIAL GARDENS             2026:1
  CKL PRODUCE                               2026:1
  COVERING GROUND FARMS                     2026:1
  ESPINOSA FARMS                            2026:1
  HAPPY GOAT FARM                           2026:1
  LETICIA'S FARMS                           2026:1
  LUNA FARM                                 2026:1
  MP FAMILY FARM                            2026:1
  PIERCE FAMILY FARM                        2026:1
  ROCKING CHAIR FARM MARKETS                2026:1
  TWIN GIRLS FARMS                          2026:1
  UPCOUNTRY FARMS                           2026:1
  WILDER WITCH FARMS                        2026:1

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  bd53721369e7c5321da66506736987aeb50e9cc0  2026:353

## what

COUNTY: Fresno 17%, Humboldt 17%, Riverside 12%, Ventura 8%, Tulare 7%, Los Angeles 7%, San Diego 6%, Mendocino 6%, Santa Cruz 5%, Merced 5%, Siskiyou 4%, Sonoma 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COUNTY | category | 46 | 0 | Fresno 39; Humboldt 37; Riverside 28; Ventura 18 |
| FARM_NAME | who | 354 | 0 | XIONG FAMILY FARM 2; SALLE ORCHARDS 2; PEARSON ORCHARD 2; MUSHROOM ADVENTURES 2 |
| CERTIFIED_PRODUCER_1 | other | 353 | 0 | Victor Hernandez 3; Cindy Xiong 2; Nicole Salle 2; Joan Lewis 2 |
| CERTIFIED_PRODUCER_2 | other | 163 | 191 | Billie Jean Salle 1; John Pearson 1; Kremena Dancheva 1; Andrew Walker 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:19:11.26783 353 |
| SOURCE_RUN_ID | audit | 1 | 0 | 5a7ba3c2-3b3e-4842-9f25-4 353 |
| SRC_SHA256 | who | 1 | 0 | bd53721369e7c5321da665067 353 |
