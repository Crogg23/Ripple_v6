# FED_EIA860_1_UTILITY

rows 6.6K  columns 14  scan 3.2s

roles: audit 2, category 1, date 1, id 1, other 5, state 1, who 4

## when

_INGESTED_AT
  2026      6.6K  ##############################

## who

UTILITY_NAME by rows
         2  Domtar Industries Inc
         2  ExxonMobil Oil Corp
         2  State Farm Mutual Auto Ins Co
         2  Cascade Solar LLC
         2  International Paper Co
         2  Formosa Plastics Corp
         2  Cleveland Cliffs
         2  Domtar Paper Company LLC
         2  Merck & Co Inc
         2  Dow Chemical Co
         2  Boise White Paper LLC
         1  Nutrien US LLC
         1  City of Beaver City - (NE)
         1  City of Alexandria - (LA)
         1  Duke Energy Progress - (NC)
         1  Boltonville Hydro Associates
         1  City of Carmi - (IL)
         1  American Bituminous Power LP
         1  OLS Energy-Agnews Inc.
         1  City of Cambridge - (NE)

_SRC_FILE by rows
      6.6K  1___Utility_Y2024.xlsx

STREET_ADDRESS by rows
       233  700 Universe Blvd
       122  700 Universe Blvd.
       105  130 Roberts Street
        70  222 2nd Ave South Suite 1900
        69  575 Fifth Ave., 35th Fl.
        66  101 Summer Street, 2nd Floor
        56  222 2nd Ave. South, Suite 1900
        54  333 Washington Street
        48  100 California St Suite 400
        46  P.O. Box 3827
        39  100 Brickstone Square, Suite 3
        36  1310 Point Street, 8th Floor
        36  4900 S. Scottsdale Road, Suite
        35  800 Gessner Road
        33  804 Carnegie Center
        32  101 Summer Street
        28  200 Liberty Street, 14 Floor
        27  17200 N. Perimeter Drive, Suit
        27  44 Montgomery Street
        27  125 High Street, 17th Floor Hi

CITY by rows
       397  Juno Beach
       371  New York
       273  Houston
       247  Boston
       174  San Francisco
       144  Nashville
       115  Asheville
       108  Scottsdale
        93  Chicago
        84  Arlington
        69  Austin
        67  Baltimore
        57  Jersey City
        54  San Diego
        51  Schenectady
        49  Princeton
        43  Denver
        43  Charlotte
        40  Andover
        37  Annapolis

## who x when

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  American Bituminous Power LP              2026:1
  Boise White Paper LLC                     2026:2
  Boltonville Hydro Associates              2026:1
  Cascade Solar LLC                         2026:2
  City of Alexandria - (LA)                 2026:1
  City of Beaver City - (NE)                2026:1
  City of Cambridge - (NE)                  2026:1
  City of Carmi - (IL)                      2026:1
  Cleveland Cliffs                          2026:2
  Domtar Industries Inc                     2026:2
  Domtar Paper Company LLC                  2026:2
  Dow Chemical Co                           2026:2
  Duke Energy Progress - (NC)               2026:1
  ExxonMobil Oil Corp                       2026:2
  Formosa Plastics Corp                     2026:2
  International Paper Co                    2026:2
  Merck & Co Inc                            2026:2
  Nutrien US LLC                            2026:1
  OLS Energy-Agnews Inc.                    2026:1
  State Farm Mutual Auto Ins Co             2026:2

_SRC_FILE by _INGESTED_AT  LOAD STAMP, not an event date
  1___Utility_Y2024.xlsx                    2026:6.6K

## where

STATE: CA 821, NY 641, TX 599, FL 535, MA 423, NC 236, NJ 213, IL 196, MN 192, CT 172, MD 168, VA 164

## what

ENTITY_TYPE: Q 70%, M 9%, IND 7%, COM 5%, I 3%, C 2%, P 1%, S 1%, F 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| UTILITY_ID | id | 6.6K | 0 | 67250 34; 67239 34; 67238 34; 67237 34 |
| UTILITY_NAME | who | 6.7K | 0 | Helion Energy, Inc. 34; Eagles Solar II, LLC 34; Eagles Solar I, LLC 34; Appleseed Solar, LLC 34 |
| STREET_ADDRESS | who | 3.8K | 2 | 700 Universe Blvd 234; 700 Universe Blvd. 123; 130 Roberts Street 117; 222 2nd Ave South Suite 1 92 |
| CITY | who | 1.8K | 0 | Juno Beach 398; New York 374; Houston 273; Boston 248 |
| STATE | state | 57 | 8 | CA 821; NY 641; TX 599; FL 535 |
| ZIP | other | 2.6K | 0 | 33408 395; 37201 148; 10017 145; 2110 144 |
| OWNER_OF_PLANTS_REPORTED_ON_FORM | other | 1 | 656 | Y 6.0K |
| OPERATOR_OF_PLANTS_REPORTED_ON_FORM | other | 1 | 3.8K | Y 2.9K |
| ASSET_MANAGER_OF_PLANTS_REPORTED_ON_FORM | other | 1 | 4.8K | Y 1.9K |
| OTHER_RELATIONSHIPS_WITH_PLANTS_REPORTED_ON_FORM | other | 1 | 6.5K | Y 96 |
| ENTITY_TYPE | category | 9 | 0 | Q 4.7K; M 613; IND 480; COM 334 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:37:34.98079 6.6K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 30e6e27a-c93e-4172-b32a-d 6.6K |
| _SRC_FILE | who | 1 | 0 | 1___Utility_Y2024.xlsx 6.6K |
