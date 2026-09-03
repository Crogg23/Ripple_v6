# PORTAL_ARC_LA_COUNTY_OPEN_D_58A85AED74

rows 2  columns 16  scan 2.3s

roles: audit 2, category 11, date 1, empty 1, other 1, who 1

## when

INGESTED_AT
  2026         2  ##############################

## who

SRC_SHA256 by rows
         2  e2f72a14dbd42f9fdcd8aaf9e62864259129acbc922800599651c103fa6df9ef

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  e2f72a14dbd42f9fdcd8aaf9e62864259129acbc  2026:2

## what

SCC: 7.13.58 50%, 7.33.107 50%

BUSINESS_NAME: Providence St Joseph Med 50%, Sonus Sf0010 50%

CENTER_NAME: Providence Saint Joseph Nicu 50%, SONUS NORTHRIDGE 50%

ADDRESS_LINE_1: Buena Vista Alameda Street 50%, Unknown 50%

CITY: Burbank 50%, Unknown 50%

ZIP_CODE: 91505-4809 50%, 0 50%

PHONE: (818) 734-9124 100%

NPI: 1336173269 50%, 1760783344 50%

SCC_TYPE: Community Neonatal Intensive C 50%, Communication Disorders Center 50%

FAMILY_FRIENDLY_SCC_TYPE: NICU and HRIF Center 50%, Hearing Center (ages 5 and up) 50%

FID: 2 50%, 1 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SCC | category | 2 | 0 | 7.13.58 1; 7.33.107 1 |
| BUSINESS_NAME | category | 2 | 0 | Providence St Joseph Med 1; Sonus Sf0010 1 |
| CENTER_NAME | category | 2 | 0 | Providence Saint Joseph N 1; SONUS NORTHRIDGE 1 |
| ADDRESS_LINE_1 | category | 2 | 0 | Buena Vista Alameda Stree 1; Unknown 1 |
| ADDRESS_LINE_2 | empty | 1 | 2 |  |
| CITY | category | 2 | 0 | Burbank 1; Unknown 1 |
| STATE | other | 1 | 0 | CA 2 |
| ZIP_CODE | category | 2 | 0 | 91505-4809 1; 0 1 |
| PHONE | category | 2 | 1 | (818) 734-9124 1 |
| NPI | category | 2 | 0 | 1336173269 1; 1760783344 1 |
| SCC_TYPE | category | 2 | 0 | Community Neonatal Intens 1; Communication Disorders C 1 |
| FAMILY_FRIENDLY_SCC_TYPE | category | 2 | 0 | NICU and HRIF Center 1; Hearing Center (ages 5 an 1 |
| FID | category | 2 | 0 | 2 1; 1 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:30:14.64827 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | 639de7c1-0043-46e8-8813-d 2 |
| SRC_SHA256 | who | 1 | 0 | e2f72a14dbd42f9fdcd8aaf9e 2 |
