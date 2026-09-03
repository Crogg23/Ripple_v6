# PORTAL_CKA_VIRGINIA_OPEN_DA_3E67A117FB

rows 9.5K  columns 10  scan 3.4s

roles: amount 1, audit 2, category 1, date 2, other 3, who 2

## when

REPORT_DATE
  2024      9.5K  ##############################

INGESTED_AT
  2026      9.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_CASES | 9.5K | 519 | 8.6K | 143.9K | 293.7K | 185.04M |

## who

LOCALITY by rows
        84  Charlotte
        80  Buckingham
        80  Stafford
        80  Lunenburg
        78  Suffolk
        78  Franklin City
        78  Arlington
        78  Frederick
        77  Clarke
        77  Surry
        77  Hanover
        77  Fairfax
        77  Highland
        77  Craig
        76  Powhatan
        76  Grayson
        76  Lee
        76  Halifax
        76  Wise
        76  Richmond County

LOCALITY by dollars
      22.11M       77 rows  Fairfax
       9.93M       70 rows  Prince William
       9.13M       71 rows  Virginia Beach
       7.73M       74 rows  Henrico
       7.56M       68 rows  Chesterfield
       7.46M       68 rows  Loudoun
       5.53M       78 rows  Arlington
       5.30M       74 rows  Chesapeake
       4.76M       72 rows  Richmond City
       4.44M       75 rows  Norfolk
       4.13M       73 rows  Newport News
       3.85M       80 rows  Stafford
       3.43M       70 rows  Alexandria
       3.28M       75 rows  Hampton
       2.82M       71 rows  Spotsylvania
       2.49M       77 rows  Hanover
       2.31M       78 rows  Frederick
       2.30M       72 rows  Roanoke County
       2.30M       72 rows  Roanoke City
       2.11M       78 rows  Suffolk

SRC_SHA256 by rows
      9.5K  16973891083f4339b2fe445d45612dfbe5726734199fa86505a41dfd163b7d17

SRC_SHA256 by dollars
     185.04M     9.5K rows  16973891083f4339b2fe445d45612dfbe5726734199fa86505a41dfd163b

## who x when

LOCALITY by REPORT_DATE, dollars = TOTAL_CASES
  Alexandria                                2024:3.43M
  Arlington                                 2024:5.53M
  Buckingham                                2024:439.5K
  Charlotte                                 2024:330.8K
  Chesapeake                                2024:5.30M
  Chesterfield                              2024:7.56M
  Clarke                                    2024:307.6K
  Craig                                     2024:123.6K
  Fairfax                                   2024:22.11M
  Franklin City                             2024:224.3K
  Frederick                                 2024:2.31M
  Grayson                                   2024:488.5K
  Halifax                                   2024:829.2K
  Hanover                                   2024:2.49M
  Henrico                                   2024:7.73M
  Highland                                  2024:40.5K
  Lee                                       2024:750.9K
  Loudoun                                   2024:7.46M
  Lunenburg                                 2024:310.6K
  Newport News                              2024:4.13M
  Norfolk                                   2024:4.44M
  Powhatan                                  2024:535.4K
  Prince William                            2024:9.93M
  Richmond City                             2024:4.76M
  Richmond County                           2024:249.3K
  Stafford                                  2024:3.85M
  Suffolk                                   2024:2.11M
  Surry                                     2024:124.5K
  Virginia Beach                            2024:9.13M
  Wise                                      2024:1.25M

SRC_SHA256 by REPORT_DATE, dollars = TOTAL_CASES
  16973891083f4339b2fe445d45612dfbe5726734  2024:185.04M

## what

VDH_HEALTH_DISTRICT: Three Rivers 12%, Central Shenandoah 12%, Crater 10%, Mount Rogers 10%, Piedmont 9%, Lord Fairfax 7%, Blue Ridge 7%, Alleghany 7%, Rappahannock 6%, Rappahannock Rapidan 6%, Peninsula 6%, Central Virginia 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORT_DATE | date | 142 | 0 | 2024-05-05 133; 2024-05-02 133; 2024-05-03 133; 2024-05-01 133 |
| FIPS | other | 134 | 0 | 51037 84; 51111 80; 51029 80; 51179 80 |
| LOCALITY | who | 132 | 0 | Charlotte 84; Lunenburg 80; Buckingham 80; Stafford 80 |
| VDH_HEALTH_DISTRICT | category | 34 | 0 | Three Rivers 717; Central Shenandoah 695; Crater 576; Mount Rogers 565 |
| TOTAL_CASES | amount | 5.9K | 0 | 524 57; 1214 56; 1490 51; 5152 50 |
| HOSPITALIZATIONS | other | 890 | 0 | 43 130; 44 124; 54 114; 85 102 |
| DEATHS | other | 279 | 0 | 55 352; 32 248; 115 215; 47 157 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:46:09.36548 9.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4b9d8aac-b178-4309-bae4-a 9.5K |
| SRC_SHA256 | who | 1 | 0 | 16973891083f4339b2fe445d4 9.5K |
