# PORTAL_SOC_UTAH_OPEN_DATA_P_598C279750

rows 34  columns 30  scan 3.8s

roles: amount 4, audit 2, category 21, date 1, other 2, who 1

## when

INGESTED_AT
  2026        34  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SUBSIDY_VALUE | 34 | 494 | 4.05M | 111.80M | 125.00M | 687.36M |
| MEGADEAL_CONTRIBUTION | 34 | 0 | 0 | 83.75M | 125.00M | 125.00M |
| SUBSIDY_VALUE_ADJUSTED_FOR_MEGADEAL | 34 | 0 | 2.48M | 111.80M | 125.00M | 602.36M |
| WAGE_DATA | 9 | 23.80M | 389.49M | 1.71B | 1.71B | 6.16B |

## who

SRC_SHA256 by rows
        34  9c6dfdd23c852670d57d6ed072953eaa91b480d16c7eccdfa058eac178c8cfc5

SRC_SHA256 by dollars
     687.36M       34 rows  9c6dfdd23c852670d57d6ed072953eaa91b480d16c7eccdfa058eac178c8

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SUBSIDY_VALUE
  9c6dfdd23c852670d57d6ed072953eaa91b480d1  2026:687.36M

## what

COMPANY: Procter & Gamble 18%, ATK Aerospace Structures 14%, eBay 14%, IM Flash Technologies 11%, Royal Bank of Scotland 7%, ATK Aerospace Systems 7%, Oracle 7%, Goldman Sachs 7%, ITT Pro Services 4%, ATK Launch Systems 4%, ITT Corporation 4%, Adobe Systems Inc. 4%

PARENT_COMPANY: Orbital ATK 29%, Procter & Gamble 15%, Micron Technology 15%, eBay 12%, ITT Corporation 6%, Royal Bank of Scotland 6%, Oracle 6%, Goldman Sachs 6%, Adobe Systems 3%, SolarWinds 3%

COUNTY: nan 82%, Salt Lake 9%, Davis 3%, Box Elder 3%, Utah 3%

YEAR: 2009 24%, 2011 24%, 2010 21%, 2008 12%, 2014 6%, 2013 6%, 2012 3%, 2007 3%, 1995 3%

PROGRAM_NAME: Economic Development Tax Incre 53%, Custom Fit Training Program 41%, multiple 6%

AWARDING_AGENCY: Governor's Office of Economic  56%, Utah College of Applied Techno 41%, multiple 3%

TYPE_OF_SUBSIDY: tax credit/rebate 53%, training reimbursement 41%, MEGADEAL 6%

NUMBER_OF_JOBS_OR_TRAINING_SLOTS: 200 21%, 192 7%, 40 7%, 1 7%, 260 7%, 802 7%, 50 7%, 1185 7%, 397 7%, 351 7%, 2200 7%, 2707 7%

SOURCE_OF_DATA: direct from agency; not on web 41%, http://business.utah.gov/site- 12%, agency provided spreadsheet ve 12%, http://business.utah.gov/GOED/ 12%, agency provided spreadsheet ve 9%, agency provided spreadsheet ve 6%, http://business.utah.gov/site- 3%, The subsidy amount and the job 3%, The subsidy value came from: J 3%

NOTES: Subsidy value is amount spent  41%,  year is fiscal year  26%,  Year is fiscal year.  15%, Year is fiscal year. Subsidy v 6%, Year is fiscal year. Jobs figu 6%, The state awarded up to $85 mi 3%, The original subsidy package a 3%

SUBSIDY_SOURCE: state 97%, multiple 3%

LOCATION_1: nan 59%, {"latitude": "40.52505", "long 9%, {"latitude": "40.653066", "lon 6%, {"latitude": "40.387876", "lon 6%, {"latitude": "40.758478", "lon 6%, {"latitude": "41.022072", "lon 6%, {"latitude": "40.562242", "lon 3%, {"latitude": "44.151166", "lon 3%, {"latitude": "40.610919", "lon 3%

COMPUTED_REGION_9Z68_3KQ5: nan 59%, 3176 26%, 3182 6%, 3183 6%, 2688 3%

WAGE_DATA_TYPE: nan 74%, payroll 26%

INVESTMENT_DATA: nan 62%, 540000000 6%, 6270000 3%, 436000000 3%, 6142500 3%, 260000000 3%, 81000000 3%, 2642908 3%, 50000000 3%, 51000000 3%, 20200000 3%, 250000000 3%

COMPUTED_REGION_5D9V_6BUI: nan 68%, 26 26%, 5 6%

COMPUTED_REGION_QMWN_IMPY: nan 68%, 224 9%, 247 6%, 198 6%, 220 6%, 181 3%, 245 3%

COMPUTED_REGION_JDNU_JMST: nan 68%, 51 9%, 298 6%, 287 6%, 70 6%, 53 3%, 296 3%

COMPUTED_REGION_MFUY_BEE2: nan 68%, 23 9%, 21 6%, 22 6%, 30 6%, 19 6%

COMPUTED_REGION_2FPW_SWV9: nan 68%, 42 9%, 63 6%, 44 6%, 24 6%, 34 3%, 60 3%

PROJECT_DESCRIPTION: nan 94%, distribution center 3%, computer chip plant 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COMPANY | category | 18 | 0 | Procter & Gamble 5; ATK Aerospace Structures 4; eBay 4; IM Flash Technologies 3 |
| PARENT_COMPANY | category | 10 | 0 | Orbital ATK 10; Procter & Gamble 5; Micron Technology 5; eBay 4 |
| LOCATION | other | 1 | 0 | Utah 34 |
| COUNTY | category | 5 | 0 | nan 28; Salt Lake 3; Davis 1; Box Elder 1 |
| YEAR | category | 9 | 0 | 2009 8; 2011 8; 2010 7; 2008 4 |
| SUBSIDY_VALUE | amount | 33 | 0 | 85000000 2; 16483 1; 11073 1; 494 1 |
| MEGADEAL_CONTRIBUTION | amount | 2 | 0 | 0 33; 125000000 1 |
| SUBSIDY_VALUE_ADJUSTED_FOR_MEGADEAL | amount | 34 | 0 | 16483 1; 11073 1; 494 1; 8607261 1 |
| PROGRAM_NAME | category | 3 | 0 | Economic Development Tax  18; Custom Fit Training Progr 14; multiple 2 |
| AWARDING_AGENCY | category | 3 | 0 | Governor's Office of Econ 19; Utah College of Applied T 14; multiple 1 |
| TYPE_OF_SUBSIDY | category | 3 | 0 | tax credit/rebate 18; training reimbursement 14; MEGADEAL 2 |
| NUMBER_OF_JOBS_OR_TRAINING_SLOTS | category | 32 | 0 | 200 3; 192 1; 40 1; 1 1 |
| SOURCE_OF_DATA | category | 9 | 0 | direct from agency; not o 14; http://business.utah.gov/ 4; agency provided spreadshe 4; http://business.utah.gov/ 4 |
| NOTES | category | 7 | 0 | Subsidy value is amount s 14;  year is fiscal year  9;  Year is fiscal year.  5; Year is fiscal year. Subs 2 |
| SUBSIDY_SOURCE | category | 2 | 0 | state 33; multiple 1 |
| LOAN_VALUE | other | 1 | 0 | 0 34 |
| LOCATION_1 | category | 9 | 0 | nan 20; {"latitude": "40.52505",  3; {"latitude": "40.653066", 2; {"latitude": "40.387876", 2 |
| COMPUTED_REGION_9Z68_3KQ5 | category | 5 | 0 | nan 20; 3176 9; 3182 2; 3183 2 |
| WAGE_DATA | amount | 10 | 0 | nan 25; 389488515 1; 23799980 1; 1278000000 1 |
| WAGE_DATA_TYPE | category | 2 | 0 | nan 25; payroll 9 |
| INVESTMENT_DATA | category | 14 | 0 | nan 20; 540000000 2; 6270000 1; 436000000 1 |
| COMPUTED_REGION_5D9V_6BUI | category | 3 | 0 | nan 23; 26 9; 5 2 |
| COMPUTED_REGION_QMWN_IMPY | category | 7 | 0 | nan 23; 224 3; 247 2; 198 2 |
| COMPUTED_REGION_JDNU_JMST | category | 7 | 0 | nan 23; 51 3; 298 2; 287 2 |
| COMPUTED_REGION_MFUY_BEE2 | category | 6 | 0 | nan 23; 23 3; 21 2; 22 2 |
| COMPUTED_REGION_2FPW_SWV9 | category | 7 | 0 | nan 23; 42 3; 63 2; 44 2 |
| PROJECT_DESCRIPTION | category | 3 | 0 | nan 32; distribution center 1; computer chip plant 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:41:11.07436 34 |
| SOURCE_RUN_ID | audit | 1 | 0 | ad97766c-853a-4fa1-9610-f 34 |
| SRC_SHA256 | who | 1 | 0 | 9c6dfdd23c852670d57d6ed07 34 |
