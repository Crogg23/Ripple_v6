# PORTAL_CKA_SAN_JOSE_OPEN_DA_2ED954C361

rows 297  columns 13  scan 3.6s

roles: amount 2, audit 2, category 3, date 1, other 3, who 3

## when

INGESTED_AT
  2026       297  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 297 | 5.8K | 14.9K | 97.0K | 210.0K | 5.73M |
| SHAPE_AREA | 297 | 1.68M | 10.00M | 216.55M | 620.78M | 6.38B |

## who

NAME by rows
         2  Guadalupe
         2  Commercial
         1  Sierramont
         1  Welch Park
         1  Quimby Oak
         1  North Berryessa
         1  The Willows
         1  Houge Parker
         1  Hayes
         1  South University
         1  Blackford
         1  Wooster and East Ct and West Ct
         1  Checkers
         1  Cherry
         1  Burbank
         1  Davis and Roeder
         1  Mitty
         1  Naglee
         1  Virginia and Martha
         1  Roundtable

NAME by dollars
      210.0K        1 rows  Alviso
      122.9K        1 rows  Santa Teresa Hills
      122.2K        1 rows  Coyote Creek
       95.9K        1 rows  East Foothills
       92.7K        1 rows  Fowler Creek
       78.4K        1 rows  Mount Pleasant Foothills
       78.1K        1 rows  Los Alamitos Creek
       74.1K        1 rows  Quicksilver
       72.9K        1 rows  Shady Oaks and Basking Ridge
       71.4K        1 rows  Silver Creek Country Club
       63.6K        1 rows  Sierra Vista Hills
       61.6K        1 rows  Suncrest
       54.8K        1 rows  The Villages
       54.2K        1 rows  Trimble Business Area
       53.4K        1 rows  Almaden Guadalupe Park
       46.7K        1 rows  Tasman and Zanker
       41.3K        1 rows  Coyote Creek North
       39.5K        1 rows  Evergreen Valley High
       36.9K        1 rows  Orchard
       35.0K        1 rows  Airport

FACILITYID by rows
         1  37
         1  5
         1  63
         1  69
         1  47
         1  92
         1  106
         1  143
         1  113
         1  147
         1  221
         1  187
         1  132
         1  74
         1  31
         1  2
         1  192
         1  48
         1  50
         1  33

FACILITYID by dollars
      210.0K        1 rows  119
      122.9K        1 rows  220
      122.2K        1 rows  293
       95.9K        1 rows  289
       92.7K        1 rows  149
       78.4K        1 rows  290
       78.1K        1 rows  215
       74.1K        1 rows  219
       72.9K        1 rows  292
       71.4K        1 rows  150
       63.6K        1 rows  134
       61.6K        1 rows  136
       54.8K        1 rows  152
       54.2K        1 rows  120
       53.4K        1 rows  281
       46.7K        1 rows  122
       41.3K        1 rows  261
       39.5K        1 rows  53
       36.9K        1 rows  143
       35.0K        1 rows  123

SRC_SHA256 by rows
       297  1989266c54689411c09d03541898251526a0f8f7df5a91e87eb30f9921d169ca

SRC_SHA256 by dollars
       5.73M      297 rows  1989266c54689411c09d03541898251526a0f8f7df5a91e87eb30f9921d1

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Alviso                                    2026:210.0K
  Blackford                                 2026:20.3K
  Burbank                                   2026:12.0K
  Checkers                                  2026:13.9K
  Cherry                                    2026:19.3K
  Commercial                                2026:34.6K
  Coyote Creek                              2026:122.2K
  Davis and Roeder                          2026:12.2K
  East Foothills                            2026:95.9K
  Fowler Creek                              2026:92.7K
  Guadalupe                                 2026:20.1K
  Hayes                                     2026:14.1K
  Houge Parker                              2026:15.9K
  Los Alamitos Creek                        2026:78.1K
  Mitty                                     2026:11.9K
  Mount Pleasant Foothills                  2026:78.4K
  Naglee                                    2026:15.1K
  North Berryessa                           2026:26.9K
  Quicksilver                               2026:74.1K
  Quimby Oak                                2026:17.5K
  Roundtable                                2026:12.4K
  Santa Teresa Hills                        2026:122.9K
  Shady Oaks and Basking Ridge              2026:72.9K
  Sierramont                                2026:8.5K
  Silver Creek Country Club                 2026:71.4K
  South University                          2026:11.2K
  The Willows                               2026:16.8K
  Virginia and Martha                       2026:13.2K
  Welch Park                                2026:19.7K
  Wooster and East Ct and West Ct           2026:9.5K

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  106                                       2026:9.5K
  113                                       2026:11.9K
  119                                       2026:210.0K
  132                                       2026:12.4K
  143                                       2026:36.9K
  147                                       2026:18.8K
  149                                       2026:92.7K
  150                                       2026:71.4K
  187                                       2026:14.9K
  192                                       2026:13.0K
  2                                         2026:10.4K
  215                                       2026:78.1K
  219                                       2026:74.1K
  220                                       2026:122.9K
  221                                       2026:19.5K
  289                                       2026:95.9K
  290                                       2026:78.4K
  292                                       2026:72.9K
  293                                       2026:122.2K
  31                                        2026:16.7K
  33                                        2026:11.3K
  37                                        2026:11.2K
  47                                        2026:12.4K
  48                                        2026:12.2K
  5                                         2026:10.6K
  50                                        2026:9.7K
  63                                        2026:30.0K
  69                                        2026:16.4K
  74                                        2026:15.4K
  92                                        2026:13.7K

## what

SOURCE: Census Blockgroup 66%, Fill in 20%, Neighborhood Assn 14%

LASTUPDATE: 2022/05/26 14:56:42+00 38%, 2022/05/26 14:56:43+00 35%, 2022/05/26 14:56:44+00 21%, 2022/05/26 14:56:41+00 5%, 2022/07/19 19:01:33+00 0%, 2022/07/19 19:01:25+00 0%, 2024/04/24 21:24:23+00 0%, 2024/04/24 21:20:28+00 0%

NOTES: was Coyote Creek 14%, was East Foothills 14%, was Little Portugal 14%, was North 1st 14%, was Canoas Creek 14%, was Alum Rock Hills 14%, was Technology 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 296 | 0 | 297 2; 296 2; 295 2; 294 2 |
| FACILITYID | who | 296 | 0 | 297 2; 296 2; 295 2; 294 2 |
| INTID | other | 296 | 0 | 297 2; 296 2; 295 2; 294 2 |
| NAME | who | 291 | 0 | Guadalupe 3; Foxchase and Oakridge 2; Westfield Oakridge 2; Magic Sands Mobile Homes 2 |
| SOURCE | category | 4 | 183 | Census Blockgroup 75; Fill in 23; Neighborhood Assn 16 |
| LASTUPDATE | category | 8 | 0 | 2022/05/26 14:56:42+00 112; 2022/05/26 14:56:43+00 103; 2022/05/26 14:56:44+00 62; 2022/05/26 14:56:41+00 16 |
| NOTES | category | 8 | 290 | was Coyote Creek 1; was East Foothills 1; was Little Portugal 1; was North 1st 1 |
| ENTERPRISEID | other | 294 | 0 | REF-NEIG-0000000297 2; REF-NEIG-0000000296 2; REF-NEIG-0000000295 2; REF-NEIG-0000000294 2 |
| SHAPE_LENGTH | amount | 292 | 0 | 14203.8319149237 2; 11380.9085401254 2; 9281.38061629234 2; 9031.79173434468 2 |
| SHAPE_AREA | amount | 302 | 0 | 9144803.90050408 2; 6216529.88088921 2; 4940265.20189433 2; 3988640.66808749 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:38:53.25216 297 |
| SOURCE_RUN_ID | audit | 1 | 0 | a57c30b2-5dfa-4ddc-8620-1 297 |
| SRC_SHA256 | who | 1 | 0 | 1989266c54689411c09d03541 297 |
