# FED_EIA861_UTILITY_DATA

rows 1.7K  columns 35  scan 2.9s

roles: audit 2, category 28, date 1, id 1, other 1, state 1, who 2

## when

_INGESTED_AT
  2026      1.7K  ##############################

## who

UTILITY_NAME by rows
         3  Withheld
         1  City of Batavia - (IL)
         1  Big Sandy Rural Elec Coop Corp
         1  PowerSouth Energy Cooperative
         1  Alaska Village Elec Coop, Inc
         1  City of Bluffton - (IN)
         1  Bonneville Power Administration
         1  City of Azusa
         1  Baltimore Gas & Electric Co
         1  Entergy Arkansas LLC
         1  Benton County
         1  Beauregard Electric Coop, Inc
         1  Central Maine Power Co
         1  Alcorn County Elec Power Assn
         1  Village of Baraga - (MI)
         1  City of Andalusia
         1  Cedarburg Light & Water Comm
         1  City of Benton - (KY)
         1  Arkansas River Power Authority
         1  Austin Energy

_SRC_FILE by rows
      1.7K  Utility_Data_2024.xlsx

## who x when

UTILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  Alaska Village Elec Coop, Inc             2026:1
  Alcorn County Elec Power Assn             2026:1
  Arkansas River Power Authority            2026:1
  Austin Energy                             2026:1
  Baltimore Gas & Electric Co               2026:1
  Beauregard Electric Coop, Inc             2026:1
  Benton County                             2026:1
  Big Sandy Rural Elec Coop Corp            2026:1
  Bonneville Power Administration           2026:1
  Cedarburg Light & Water Comm              2026:1
  Central Maine Power Co                    2026:1
  City of Andalusia                         2026:1
  City of Azusa                             2026:1
  City of Batavia - (IL)                    2026:1
  City of Benton - (KY)                     2026:1
  City of Bluffton - (IN)                   2026:1
  Entergy Arkansas LLC                      2026:1
  PowerSouth Energy Cooperative             2026:1
  Village of Baraga - (MI)                  2026:1
  Withheld                                  2026:3

_SRC_FILE by _INGESTED_AT  LOAD STAMP, not an event date
  Utility_Data_2024.xlsx                    2026:1.7K

## where

STATE: TX 207, CA 84, TN 82, NY 72, WI 70, NC 64, GA 62, OH 57, MN 52, MO 51, AL 47, IN 46

## what

OWNERSHIP_TYPE: Cooperative 35%, Municipal 27%, Retail Power Marketer 15%, Investor Owned 10%, Political Subdivision 5%, Wholesale Power Marketer 2%, Transmission 2%, Community Choice Aggregator 2%, State 1%, Municipal Mktg Authority 1%, Behind the Meter 1%, Federal 0%

NERC_REGION: SERC 32%, WECC 16%, RFC 15%, MRO 11%, SPP 7%, TRE 6%, NPCC 6%, MISO 4%, FRCC 2%, AK 1%, ERCOT 0%, HI 0%

TRE: Y 69%, N 31%

FRCC: Y 72%, N 28%

MRO: Y 88%, N 12%

NPCC: Y 84%, N 16%

RFC: Y 68%, N 32%

SERC: Y 95%, N 5%

SPP: Y 69%, N 31%

WECC: Y 93%, N 7%

CAISO: Y 82%, N 18%

ERCOT: Y 90%, N 10%

PJM: Y 92%, N 8%

NYISO: Y 92%, N 8%

SPP_1: Y 86%, N 14%

MISO: Y 90%, N 10%

ISONE: Y 88%, N 12%

OTHER: Y 84%, N 16%

GENERATION: Y 82%, N 18%

TRANSMISSION: Y 73%, N 27%

BUYING_TRANSMISSION: Y 90%, N 10%

DISTRIBUTION: Y 99%, N 1%

BUYING_DISTRIBUTION: Y 60%, N 40%

WHOLESALE_MARKETING: Y 90%, N 10%

RETAIL_MARKETING: Y 87%, N 13%

BUNDLED: Y 75%, N 25%

ALT_FUEL_VEHICLE: Y 52%, N 48%

ALT_FUEL_VEHICLE_2: Y 88%, N 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATA_YEAR | other | 1 | 0 | 2024 1.7K |
| UTILITY_NUMBER | id | 1.7K | 0 | 88888 11; 67251 9; 67122 9; 67113 9 |
| UTILITY_NAME | who | 1.7K | 0 | Withheld 11; GridLiance Heartland LLC 9; Selfserve Energy Corp. 9; Morongo Transmission LLC 9 |
| STATE | state | 52 | 1 | TX 207; CA 84; TN 82; NY 72 |
| OWNERSHIP_TYPE | category | 12 | 0 | Cooperative 602; Municipal 458; Retail Power Marketer 250; Investor Owned 163 |
| NERC_REGION | category | 18 | 315 | SERC 441; WECC 217; RFC 206; MRO 154 |
| TRE | category | 2 | 1.5K | Y 130; N 58 |
| FRCC | category | 2 | 1.7K | Y 31; N 12 |
| MRO | category | 2 | 1.5K | Y 214; N 29 |
| NPCC | category | 2 | 1.6K | Y 97; N 19 |
| RFC | category | 2 | 1.4K | Y 234; N 112 |
| SERC | category | 2 | 1.2K | Y 458; N 25 |
| SPP | category | 2 | 1.5K | Y 129; N 57 |
| WECC | category | 2 | 1.4K | Y 259; N 19 |
| CAISO | category | 2 | 1.6K | Y 100; N 22 |
| ERCOT | category | 2 | 1.5K | Y 167; N 18 |
| PJM | category | 2 | 1.4K | Y 291; N 26 |
| NYISO | category | 2 | 1.6K | Y 112; N 10 |
| SPP_1 | category | 2 | 1.5K | Y 184; N 30 |
| MISO | category | 2 | 1.3K | Y 327; N 38 |
| ISONE | category | 2 | 1.6K | Y 133; N 18 |
| OTHER | category | 2 | 1.3K | Y 322; N 63 |
| GENERATION | category | 2 | 1.2K | Y 411; N 90 |
| TRANSMISSION | category | 2 | 1.2K | Y 377; N 141 |
| BUYING_TRANSMISSION | category | 2 | 1.2K | Y 405; N 47 |
| DISTRIBUTION | category | 2 | 483 | Y 1.2K; N 17 |
| BUYING_DISTRIBUTION | category | 2 | 1.6K | Y 65; N 44 |
| WHOLESALE_MARKETING | category | 2 | 1.3K | Y 328; N 36 |
| RETAIL_MARKETING | category | 2 | 1.3K | Y 357; N 53 |
| BUNDLED | category | 2 | 1.4K | Y 196; N 65 |
| ALT_FUEL_VEHICLE | category | 2 | 734 | Y 499; N 468 |
| ALT_FUEL_VEHICLE_2 | category | 2 | 1.1K | Y 500; N 71 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:38:44.00085 1.7K |
| _SOURCE_RUN_ID | audit | 1 | 0 | e3041a5f-83b5-459a-bbbe-2 1.7K |
| _SRC_FILE | who | 1 | 0 | Utility_Data_2024.xlsx 1.7K |
