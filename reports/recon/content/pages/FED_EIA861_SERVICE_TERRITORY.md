# FED_EIA861_SERVICE_TERRITORY

rows 11.8K  columns 9  scan 2.8s

roles: audit 2, date 1, other 3, state 1, who 3

## when

_INGESTED_AT
  2026     11.8K  ##############################

## who

ABBEVILLE by rows
       111  Washington
        92  Franklin
        89  Lincoln
        88  Jackson
        81  Jefferson
        77  Madison
        74  Clay
        70  Montgomery
        69  Monroe
        66  Marion
        62  Grant
        60  Union
        59  Marshall
        55  Wayne
        54  Polk
        52  Clark
        52  Greene
        51  Crawford
        50  Douglas
        50  Johnson

_SRC_FILE by rows
     11.8K  Service_Territory_2024.xlsx

CITY_OF_ABBEVILLE_SC by rows
       259  WAPA-- Western Area Power Administration
       155  Georgia Power Co
       129  Virginia Electric & Power Co
        99  Oncor Electric Delivery Company LLC
        90  PacifiCorp
        84  Interstate Power and Light Co
        83  Bonneville Power Administration
        83  Kentucky Utilities Co
        81  Ameren Illinois Company
        75  Otter Tail Power Co
        71  Duke Energy Indiana, LLC
        71  Entergy Arkansas LLC
        69  Duke Energy Progress - (NC)
        67  Northern States Power Co - Minnesota
        65  Oklahoma Gas & Electric Co
        65  Union Electric Co - (MO)
        63  Duke Energy Carolinas, LLC
        60  Consumers Energy Co - (MI)
        60  Entergy Louisiana LLC
        60  MidAmerican Energy Co

## who x when

ABBEVILLE by _INGESTED_AT  LOAD STAMP, not an event date
  Clark                                     2026:52
  Clay                                      2026:74
  Crawford                                  2026:51
  Douglas                                   2026:50
  Franklin                                  2026:92
  Grant                                     2026:62
  Greene                                    2026:52
  Jackson                                   2026:88
  Jefferson                                 2026:81
  Johnson                                   2026:50
  Lincoln                                   2026:89
  Madison                                   2026:77
  Marion                                    2026:66
  Marshall                                  2026:59
  Monroe                                    2026:69
  Montgomery                                2026:70
  Polk                                      2026:54
  Union                                     2026:60
  Washington                                2026:111
  Wayne                                     2026:55

_SRC_FILE by _INGESTED_AT  LOAD STAMP, not an event date
  Service_Territory_2024.xlsx               2026:11.8K

## where

SC: TX 978, IA 600, GA 572, MN 505, MO 494, KS 460, IN 455, OH 435, NE 409, NC 395, KY 375, WI 370

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| C_2024 | other | 1 | 0 | 2024 11.8K |
| C_34 | other | 2.9K | 0 | 27000 302; 19876 167; 7140 165; 44372 144 |
| CITY_OF_ABBEVILLE_SC | who | 2.9K | 0 | WAPA-- Western Area Power 302; Virginia Electric & Power 167; Georgia Power Co 165; Oncor Electric Delivery C 144 |
| Y | other | 1 | 8.9K | Y 2.9K |
| SC | state | 51 | 0 | TX 978; IA 600; GA 572; MN 505 |
| ABBEVILLE | who | 1.9K | 0 | Washington 111; Franklin 92; Lincoln 89; Jackson 88 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:37.39542 11.8K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 74fd7d77-eba3-4f29-bbef-b 11.8K |
| _SRC_FILE | who | 1 | 0 | Service_Territory_2024.xl 11.8K |
