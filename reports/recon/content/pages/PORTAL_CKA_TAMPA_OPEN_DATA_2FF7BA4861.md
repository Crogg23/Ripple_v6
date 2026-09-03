# PORTAL_CKA_TAMPA_OPEN_DATA_2FF7BA4861

rows 150  columns 13  scan 4.3s

roles: amount 1, audit 2, category 4, date 2, other 2, who 3

## when

DATE
  2021       143  ##############################
  2024         5  #
  2025         2  

INGESTED_AT
  2026       150  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 150 | 0 | 1.3K | 8.6K | 10.3K | 289.6K |

## who

C_ORGANIZATION by rows
       150  Fire Rescue (Fire Rescue)

C_ORGANIZATION by dollars
      289.6K      150 rows  Fire Rescue (Fire Rescue)

TYPEDATA by rows
       150  Period

TYPEDATA by dollars
      289.6K      150 rows  Period

SRC_SHA256 by rows
       150  0c3694c9bff9a4235674dc5721e26611a0233c35f01e5f7c1def740240e24bed

SRC_SHA256 by dollars
      289.6K      150 rows  0c3694c9bff9a4235674dc5721e26611a0233c35f01e5f7c1def740240e2

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Fire Rescue (Fire Rescue)                 2021:269.4K 2024:12.1K 2025:8.2K

TYPEDATA by DATE, dollars = VALUE
  Period                                    2021:269.4K 2024:12.1K 2025:8.2K

## what

CHARTNAME: Rescues Per Year 28%, Medical Calls by Year 24%, Fire Calls by Year 24%, Working Fires per Location 24%

DESCRIPTION: Fire Rescue; Rescues Per Year 28%, Fire; Medical Calls by Year 24%, Fire; Fire Calls 24%, Fire; Working Fires per Locati 24%

CATEGORY: Drew Park / West Tampa 8%, Unnamed 8%, Ybor City 8%, Westshore to Central Business  8%, Tampa Palms 8%, Tampa Heights 8%, Port Tampa / Interbay 8%, Palmetto Beach / Grant Park 8%, Old Seminole Heights 8%, Northeast Tampa / Rowlett Park 8%, New Tampa - North 8%, Lowry Park 8%

PERIOD: 2024 50%, 2023 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 152 | 0 | 17167 1; 17166 1; 13567 1; 13566 1 |
| C_ORGANIZATION | who | 1 | 0 | Fire Rescue (Fire Rescue) 150 |
| CHARTNAME | category | 4 | 0 | Rescues Per Year 42; Medical Calls by Year 36; Fire Calls by Year 36; Working Fires per Locatio 36 |
| DESCRIPTION | category | 4 | 0 | Fire Rescue; Rescues Per  42; Fire; Medical Calls by Ye 36; Fire; Fire Calls 36; Fire; Working Fires per L 36 |
| CATEGORY | category | 41 | 0 | Drew Park / West Tampa 6; Unnamed 6; Ybor City 6; Westshore to Central Busi 6 |
| SUMMARY | other | 1 | 0 | Total 150 |
| TYPEDATA | who | 1 | 0 | Period 150 |
| DATE | date | 7 | 0 | 2021-04-29T00:00:00 120; 2021-04-27T00:00:00 23; 2024-06-11T10:24:00 2; 2024-06-11T00:00:00 2 |
| PERIOD | category | 2 | 0 | 2024 75; 2023 75 |
| VALUE | amount | 132 | 0 | 14 4; 8 4; 0 3; 17 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:16:24.04203 150 |
| SOURCE_RUN_ID | audit | 1 | 0 | fd9c21fb-9af7-4b54-b0ad-6 150 |
| SRC_SHA256 | who | 1 | 0 | 0c3694c9bff9a4235674dc572 150 |
