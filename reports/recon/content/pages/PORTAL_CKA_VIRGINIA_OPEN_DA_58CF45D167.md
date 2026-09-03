# PORTAL_CKA_VIRGINIA_OPEN_DA_58CF45D167

rows 78  columns 11  scan 3.2s

roles: amount 2, audit 2, category 4, date 1, other 2, who 1

## when

INGESTED_AT
  2026        78  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 78 | 36.58 | 37.34 | 39.11 | 39.19 | 2.9K |
| LONGITUDE | 78 | -82.75 | -77.53 | -75.99 | -75.86 | -6.1K |

## who

SRC_SHA256 by rows
        78  772dfcf0a1187f12dc67143b1a14ab5bf78e5659ef46d4b54c4db4cc03625f31

SRC_SHA256 by dollars
        2.9K       78 rows  772dfcf0a1187f12dc67143b1a14ab5bf78e5659ef46d4b54c4db4cc0362

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  772dfcf0a1187f12dc67143b1a14ab5bf78e5659  2026:2.9K

## what

BED_SIZE_CATEGORY: Less than 100 Beds 37%, Greater than 200 Beds 36%, Between 101-200 Beds 27%

HOSPITAL_SYSTEM: HCA 19%, Sentara Healthcare 16%, Bon Secours Mercy Health 15%, Ballad Health 9%, Inova 7%, LifePoint Health 6%, UVA Health System 6%, Riverside 6%, Centra Health 6%, Carilion Clinic 6%, VCU Health 4%

MEDICAL_SCHOOL_AFFILIATION: Yes 78%, No 22%

VDH_HEALTH_PLANNING_REGION: Southwest 28%, Central 21%, Eastern 21%, Northwest 17%, Northern 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| HOSPITAL | other | 77 | 0 | Wythe County Community Ho 1; Winchester Medical Center 1; Warren Memorial Hospital 1; Virginia Hospital Center 1 |
| FULL_ADDRESS | other | 79 | 0 | 600 West Ridge Road Wythe 1; 1840 Amherst Street Winch 1; 1000 N Shenandoah Avenue  1; 1701 N George Mason Drive 1 |
| BED_SIZE_CATEGORY | category | 3 | 0 | Less than 100 Beds 29; Greater than 200 Beds 28; Between 101-200 Beds 21 |
| HOSPITAL_SYSTEM | category | 15 | 4 | HCA 13; Sentara Healthcare 11; Bon Secours Mercy Health 10; Ballad Health 6 |
| MEDICAL_SCHOOL_AFFILIATION | category | 2 | 0 | Yes 61; No 17 |
| VDH_HEALTH_PLANNING_REGION | category | 5 | 0 | Southwest 22; Central 16; Eastern 16; Northwest 13 |
| LATITUDE | amount | 79 | 0 | 36.95453722 1; 39.19127082 1; 38.93598319 1; 38.88960239 1 |
| LONGITUDE | amount | 79 | 0 | -81.09720817 1; -78.19660677 1; -78.15198103 1; -77.12816858 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:29:51.19330 78 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3d79fa28-0ade-41d2-b3c5-3 78 |
| SRC_SHA256 | who | 1 | 0 | 772dfcf0a1187f12dc67143b1 78 |
