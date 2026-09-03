# PORTAL_CKA_WPRDC_ALLEGHENY_2169858E8A

rows 368  columns 18  scan 4.8s

roles: audit 2, category 4, date 3, other 6, who 4

## when

CREATIONDATE
  2019       347  ##############################
  2020         1  
  2021         2  
  2022         4  
  2023         4  
  2024        10  #

EDITDATE
  2019       212  ##############################
  2020         1  
  2021         7  #
  2022        24  ###
  2023        83  ############
  2024        36  #####
  2025         5  #

INGESTED_AT
  2026       368  ##############################

## who

LOCALNAME by rows
         6  Haymaker
         5  Service Rd
         4  Brownsville
         4  Ridge
         3  Fifth
         3  Middle
         3  Entrance
         3  Cliff Mine
         3  Bethel Church
         3  Glenfield
         3  Dorseyville
         3  Old Campbells Run
         3  Wall
         3  Mccoy
         2  Stroschein
         2  Center
         2  Hemlock
         2  Vanadium
         2  Babcock
         2  Homestead-Duquesne

LEGALNAME by rows
         5  Ridge
         5  Service Rd
         5  Brownsville
         4  Evergreen
         4  Dravosburg Bridge Ramp
         4  Coal Valley
         4  Homestead - Duquesne
         4  Campbells Run
         4  Haymaker
         3  Glenfield
         3  Kittanning & Dorseyville
         3  Blackburn
         3  Middle
         3  Babcock
         3  Mccoy
         3  Crane Ave
         3  Whitehall
         3  McKees Rocks / Steubenville
         3  Entrance
         3  Painters Run

FACILITYID by rows
         3  81507
         2  81504
         2  99006
         2  73440
         2  31420
         2  29899
         2  73798
         2  80401
         2  17155
         2  47020
         2  80616
         1  69779
         1  69747
         1  70600
         1  69727
         1  68967
         1  68213
         1  16956
         1  33349
         1  81608

SRC_SHA256 by rows
       368  596026e5ece96841a245ad16bc85383ab9acd00e5840292c6c1f4b0615c67b5a

## who x when

LOCALNAME by EDITDATE
  Babcock                                   2019:1 2024:1
  Bethel Church                             2023:3
  Brownsville                               2019:1 2021:1 2023:1 2024:1
  Center                                    2019:2
  Cliff Mine                                2019:2 2023:1
  Dorseyville                               2019:3
  Entrance                                  2019:3
  Fifth                                     2019:3
  Glenfield                                 2024:3
  Haymaker                                  2019:4 2023:2
  Hemlock                                   2019:2
  Homestead-Duquesne                        2019:2
  Mccoy                                     2019:1 2023:2
  Middle                                    2019:3
  Old Campbells Run                         2019:2 2024:1
  Ridge                                     2019:3 2023:1
  Service Rd                                2019:3 2025:2
  Stroschein                                2019:2
  Vanadium                                  2022:1 2023:1
  Wall                                      2019:1 2023:2

LEGALNAME by EDITDATE
  Babcock                                   2019:2 2024:1
  Blackburn                                 2022:2 2023:1
  Brownsville                               2019:1 2021:1 2023:2 2024:1
  Campbells Run                             2019:1 2023:2 2024:1
  Coal Valley                               2023:3 2024:1
  Crane Ave                                 2022:2 2023:1
  Dravosburg Bridge Ramp                    2019:4
  Entrance                                  2019:3
  Evergreen                                 2019:4
  Glenfield                                 2024:3
  Haymaker                                  2019:2 2023:2
  Homestead - Duquesne                      2019:4
  Kittanning & Dorseyville                  2019:3
  McKees Rocks / Steubenville               2019:1 2023:2
  Mccoy                                     2019:1 2023:2
  Middle                                    2019:3
  Painters Run                              2019:3
  Ridge                                     2019:2 2023:2 2024:1
  Service Rd                                2019:3 2025:2
  Whitehall                                 2019:2 2021:1

## what

CREATOR: eligthomas 95%, steven.finnegan@alleghenycount 4%, SFinneganAC 1%, RSanderAC 1%

DEPARTMENT: DPW 79%, Parks 21%

EDITOR: eligthomas 57%, steven.finnegan@alleghenycount 19%, SFinneganAC 17%, GISHelp 2%, RSanderAC 2%, MSimoneauxAC 1%, OMallAC 1%

TYPE: Rd 69%, Dr 15%, Ave 7%, Blvd 3%, St 2%, Ln 2%, Loop 1%, Ramp 1%, Pike 1%, Ext 1%, ROAD 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CREATIONDATE | date | 22 | 0 | 2019-10-03T15:36:17 346; 2022-10-05T12:35:20 2; 2024-04-12T11:34:35 1; 2024-02-12T19:05:54 1 |
| CREATOR | category | 5 | 1 | eligthomas 350; steven.finnegan@allegheny 13; SFinneganAC 2; RSanderAC 2 |
| DEPARTMENT | category | 2 | 0 | DPW 289; Parks 79 |
| EDITDATE | date | 124 | 0 | 2019-10-03T15:36:17 210; 2024-01-22T13:19:07 13; 2024-02-12T19:10:03 3; 2024-01-17T14:34:00 3 |
| EDITOR | category | 8 | 2 | eligthomas 210; steven.finnegan@allegheny 70; SFinneganAC 62; GISHelp 9 |
| FACILITYID | who | 339 | 18 | 81507 3; 81504 3; 80616 3; 47020 3 |
| GLOBALID | other | 370 | 0 | e4aac4f8-8fda-40f4-ae66-4 2; f76f5efc-96cb-4dc8-980f-8 2; 36c44908-ac57-4231-a9c2-8 2; cc9f79cf-3224-44a9-a0cb-6 2 |
| LEGACYID | other | 288 | 78 |   1170-00 3;   1329-00 2;   1135-01 2;   1135-03 2 |
| LEGALNAME | who | 276 | 0 | Brownsville 5; Ridge 5; Service Rd 5; Glenfield 4 |
| LOCALNAME | who | 306 | 0 | Haymaker 6; Service Rd 5; Glenfield 4; Ridge 4 |
| OBJECTID_1 | other | 368 | 0 | 620 2; 618 2; 617 2; 615 2 |
| ROUTEID | other | 360 | 0 | 1329-00 2; 1135-01 2; 1135-03 2; 1135-02 2 |
| ROUTENO | other | 372 | 0 | 132900 2; 113501 2; 113503 2; 113502 2 |
| TYPE | category | 17 | 46 | Rd 220; Dr 46; Ave 22; Blvd 9 |
| GEOMETRY | other | 371 | 0 | LINESTRING (570402.222130 2; LINESTRING (573932.679641 2; LINESTRING (573843.442742 2; LINESTRING (574502.543038 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:40:35.27251 368 |
| SOURCE_RUN_ID | audit | 1 | 0 | 847ca088-0358-4e0e-888d-e 368 |
| SRC_SHA256 | who | 1 | 0 | 596026e5ece96841a245ad16b 368 |
