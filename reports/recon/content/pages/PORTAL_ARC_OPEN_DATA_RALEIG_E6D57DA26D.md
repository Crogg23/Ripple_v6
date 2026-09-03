# PORTAL_ARC_OPEN_DATA_RALEIG_E6D57DA26D

rows 334  columns 13  scan 2.6s

roles: amount 1, audit 2, category 8, date 1, other 1, who 1

## when

INGESTED_AT
  2026       334  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| FIRMS | 172 | 1 | 216.50 | 23.6K | 26.4K | 316.2K |

## who

SRC_SHA256 by rows
       334  0026687bbf25181830efba54fd4e430f250103ce28cb8247b301ea0602a3f742

SRC_SHA256 by dollars
      316.2K      334 rows  0026687bbf25181830efba54fd4e430f250103ce28cb8247b301ea0602a3

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = FIRMS
  0026687bbf25181830efba54fd4e430f250103ce  2026:316.2K

## what

NAICS_CODE: Total for all sectors 63%, Other services (except public  3%, Accommodation and food service 3%, Arts, entertainment, and recre 3%, Health care and social assista 3%, Educational services 3%, Administrative and support and 3%, Professional, scientific, and  3%, Finance and insurance (662) 3%, Information 3%, Transportation and warehousing 3%, Retail trade 3%

SEX: nan 88%, Equally male/female 3%, Male 3%, Female 3%, Unclassifiable 3%

ETHNICITY: nan 90%, Non-Hispanic 3%, Hispanic 3%, Unclassifiable 3%, Equally Hispanic/non-Hispanic 2%

RACE: nan 77%, Nonminority 3%, Minority 3%, Asian 3%, White 3%, American Indian and Alaska Nat 3%, Unclassifiable 3%, Black or African American 2%, Equally minority/nonminority 2%, Native Hawaiian and Other Paci 1%

VETERAN: nan 89%, Nonveteran 3%, Veteran 3%, Equally veteran/nonveteran 3%, Unclassifiable 3%

EMPLOYMENT_SIZE: 1 to 4 employees 12%, no employees 11%, 500 employees or more 11%, 5 to 9 employees 10%, 20 to 49 employees 10%, 100 to 249 employees 10%, 10 to 19 employees 10%, 250 to 499 employees 10%, 50 to 99 employees 9%, Firms with less than 500 emplo 5%

YEAR: 1 12%, 0 11%, 8 11%, 2 10%, 4 10%, 6 10%, 3 10%, 7 10%, 5 9%, 9 5%

SITENAME: CBSA: Raleigh-Cary, NC Metropo 99%, For total 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 332 | 0 | 373 2; 372 2; 371 2; 370 2 |
| NAICS_CODE | category | 22 | 0 | Total for all sectors 172; Other services (except pu 9; Accommodation and food se 9; Arts, entertainment, and  9 |
| SEX | category | 4 | 0 | nan 295; Equally male/female 10; Male 10; Female 10 |
| ETHNICITY | category | 5 | 0 | nan 299; Non-Hispanic 10; Hispanic 10; Unclassifiable 9 |
| RACE | category | 10 | 0 | nan 257; Nonminority 10; Minority 10; Asian 10 |
| VETERAN | category | 5 | 0 | nan 296; Nonveteran 10; Veteran 10; Equally veteran/nonvetera 9 |
| EMPLOYMENT_SIZE | category | 10 | 0 | 1 to 4 employees 40; no employees 38; 500 employees or more 37; 5 to 9 employees 35 |
| YEAR | category | 10 | 0 | 1 40; 0 38; 8 37; 2 35 |
| FIRMS | amount | 135 | 0 | nan 162; 2.0 11; 3.0 7; 1.0 6 |
| SITENAME | category | 2 | 0 | CBSA: Raleigh-Cary, NC Me 332; For total 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:22:27.77323 334 |
| SOURCE_RUN_ID | audit | 1 | 0 | 9451de88-f6e0-4a06-adde-4 334 |
| SRC_SHA256 | who | 1 | 0 | 0026687bbf25181830efba54f 334 |
