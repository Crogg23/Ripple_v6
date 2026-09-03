# PORTAL_ARC_LA_COUNTY_OPEN_D_501C20229C

rows 1.2K  columns 19  scan 3.7s

roles: audit 2, category 2, date 1, id 4, other 3, who 8

## when

INGESTED_AT
  2026      1.2K  ##############################

## who

USER_BUSINESS_NAME by rows
        30  RALPHS GROCERY CO
        18  SMART & FINAL STORES LLC
        12  TRADER JOE'S CO
         9  THE VONS COMPANIES INC
         8  NUMERO UNO ACQUISITIONS LLC
         7  SUPER CENTER CONCEPTS INC
         7  MRS GOOCHS NATURAL FOOD MARKETS INC
         5  BERBERIAN ENTERPRISES INC
         5  MOTHERS NUTRITIONAL CENTER INC
         4  NORTHGATE GONZALEZ LLC
         4  GELSON'S MARKETS
         4  7-ELEVEN, INC.
         3  H H & S ENTERPRISES INC
         3  SF MARKETS LLC
         3  AHMED H IBRAHIM
         3  R & S SHARMA INC
         2  JIKU BARUA
         2  RIGOBERTO GONZALEZ
         2  JORGE ALBERTO RAMOS
         2  JOSE LUIS RODRIGUEZ

USER_DBA_NAME by rows
       236  nan
         8  NUMERO UNO MARKET
         4  SUPERIOR GROCERS
         4  WHOLE FOODS MARKET
         3  BIG APPLE
         3  QUICKMART
         2  WASHINGTON MINI MARKET
         2  COOKBOOK MARKET
         2  MINI MARKET LA BENDICION
         2  EL RANCHITO MARKET
         2  LIVING WATER
         2  ANGELICA'S MARKET
         2  EL RANCHO MARKET
         2  SUPER A FOODS
         2  TOYIN MINI MARKET
         2  HOLLYWOOD BAZAAR
         2  RE GROCERY
         2  MAMBA MART
         2  DAILY FOOD MARKET
         2  PETER PAN MARKET

USER_NAICS by rows
      1.2K  445100

USER_MAILING_ADDRESS by rows
       644  nan
        60  POST OFFICE BOX #219088
        29  POST OFFICE BOX #54143
        16  POST OFFICE BOX #512377
        12  POST OFFICE BOX #8000
         9  POST OFFICE BOX #29096
         8  6701 WILSON AVENUE
         7  POST OFFICE BOX #684786
         6  13635 FREEWAY DRIVE
         5  1201 N MAGNOLIA AVENUE
         5  15510   CARMENITA ROAD
         5  5315 SANTA MONICA BLVD
         3  POST OFFICE BOX #512256
         2  17132 GARD AVENUE
         2  3115   WABASH AVENUE
         2  201 W UNIVERSITY AVENUE
         2  23622   CALABASAS ROAD   SUITE #331
         2  915 E 230TH STREET
         2  3464 ATWATER AVENUE
         2  15510 CARMENITA ROAD

## who x when

USER_BUSINESS_NAME by INGESTED_AT  LOAD STAMP, not an event date
  7-ELEVEN, INC.                            2026:4
  AHMED H IBRAHIM                           2026:3
  BERBERIAN ENTERPRISES INC                 2026:5
  GELSON'S MARKETS                          2026:4
  H H & S ENTERPRISES INC                   2026:3
  JIKU BARUA                                2026:2
  JORGE ALBERTO RAMOS                       2026:2
  JOSE LUIS RODRIGUEZ                       2026:2
  MOTHERS NUTRITIONAL CENTER INC            2026:5
  MRS GOOCHS NATURAL FOOD MARKETS INC       2026:7
  NORTHGATE GONZALEZ LLC                    2026:4
  NUMERO UNO ACQUISITIONS LLC               2026:8
  R & S SHARMA INC                          2026:3
  RALPHS GROCERY CO                         2026:30
  RIGOBERTO GONZALEZ                        2026:2
  SF MARKETS LLC                            2026:3
  SMART & FINAL STORES LLC                  2026:18
  SUPER CENTER CONCEPTS INC                 2026:7
  THE VONS COMPANIES INC                    2026:9
  TRADER JOE'S CO                           2026:12

USER_DBA_NAME by INGESTED_AT  LOAD STAMP, not an event date
  ANGELICA'S MARKET                         2026:2
  BIG APPLE                                 2026:3
  COOKBOOK MARKET                           2026:2
  DAILY FOOD MARKET                         2026:2
  EL RANCHITO MARKET                        2026:2
  EL RANCHO MARKET                          2026:2
  HOLLYWOOD BAZAAR                          2026:2
  LIVING WATER                              2026:2
  MAMBA MART                                2026:2
  MINI MARKET LA BENDICION                  2026:2
  NUMERO UNO MARKET                         2026:8
  PETER PAN MARKET                          2026:2
  QUICKMART                                 2026:3
  RE GROCERY                                2026:2
  SUPER A FOODS                             2026:2
  SUPERIOR GROCERS                          2026:4
  TOYIN MINI MARKET                         2026:2
  WASHINGTON MINI MARKET                    2026:2
  WHOLE FOODS MARKET                        2026:4
  nan                                       2026:236

## what

LOC_NAME: CAMS_POINTS 84%, CAMS_STREETS 16%, Nationwide_Geo 1%

USER_COUNCIL_DISTRICT: 9 20%, 14 14%, 8 13%, 10 12%, 1 11%, 13 10%, 5 7%, 0 5%, 11 4%, 15 2%, 4 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.2K | 0 | 1247 7; 1246 7; 1245 7; 1244 7 |
| LOC_NAME | category | 3 | 0 | CAMS_POINTS 1.0K; CAMS_STREETS 194; Nationwide_Geo 8 |
| USER_LOCATION_ACCOUNT | id | 1.3K | 0 | 0000554496-0021-4 7; 0003282894-0001-5 7; 0000032242-0005-5 7; 0003317288-0001-8 7 |
| USER_BUSINESS_NAME | who | 1.1K | 0 | RALPHS GROCERY CO 30; SMART & FINAL STORES LLC 18; TRADER JOE'S CO 13; THE VONS COMPANIES INC 10 |
| USER_DBA_NAME | who | 974 | 0 | nan 236; NUMERO UNO MARKET 8; TRADER JOE'S #250 6; TIMOS MARKET 6 |
| USER_STREET_ADDRESS | id | 1.2K | 0 | 3131 S HOOVER STREET   SU 7; 3608 W SLAUSON AVENUE 7; 8137 S VERMONT AVENUE #33 7; 3612 W SLAUSON AVENUE 7 |
| USER_CITY | who | 1 | 0 | LOS ANGELES 1.2K |
| USER_ZIP_CODE | other | 1.1K | 0 | 90043-2900 8; 90089-8500 7; 90044-3535 7; 90019-5201 7 |
| USER_LOCATION_DESCRIPTION | id | 1.2K | 0 | 3131 HOOVER 90089-8500 7; 3608 SLAUSON 90043 7; 8137 VERMONT 90044-3535 7; 3612 SLAUSON 90043-2900 7 |
| USER_MAILING_ADDRESS | who | 424 | 0 | nan 644; POST OFFICE BOX #219088 60; POST OFFICE BOX #54143 29; POST OFFICE BOX #512377 16 |
| USER_MAILING_CITY | who | 71 | 0 | nan 645; LOS ANGELES 384; DALLAS 62; SANTA FE SPRINGS 13 |
| USER_MAILING_ZIP_CODE | other | 415 | 0 | nan 644; 75221-9088 60; 90054-0143 29; 90051-0377 16 |
| USER_NAICS | who | 1 | 0 | 445100 1.2K |
| USER_PRIMARY_NAICS_DESCRIPTION | who | 1 | 0 | Grocery stores (including 1.2K |
| USER_COUNCIL_DISTRICT | category | 11 | 0 | 9 255; 14 174; 8 168; 10 148 |
| GEOMETRY | other | 1.2K | 0 | {"type": "Point", "coordi 7; {"type": "Point", "coordi 7; {"type": "Point", "coordi 7; {"type": "Point", "coordi 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:30:44.30702 1.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 50f3654c-790b-4d71-949f-1 1.2K |
| SRC_SHA256 | who | 1 | 0 | 6d2929cfb7281eb21a36c4743 1.2K |
