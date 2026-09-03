# PORTAL_ARC_LA_COUNTY_OPEN_D_E034245E05

rows 8  columns 17  scan 2.1s

roles: audit 2, category 13, date 1, other 1, who 1

## when

INGESTED_AT
  2026         8  ##############################

## who

SRC_SHA256 by rows
         8  0d4dc62318db594c16df4c71bb6a7c16f28e9f1bbd508ab37fe51222d0c0f682

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  0d4dc62318db594c16df4c71bb6a7c16f28e9f1b  2026:8

## what

SCC: 7.09.30A 12%, 7.37.20 12%, 7.35.77 12%, 7.05.20 12%, 7.05.45 12%, 7.33.107 12%, 7.13.58 12%, 7.35.53 12%

CENTER_NAME: UC Irvine Medical Center 38%, UCSF Benioff Children's Hospit 12%, Totally Kids Rehabilitation Ho 12%, SONUS NORTHRIDGE 12%, Providence Saint Joseph Nicu 12%, Connect Hearing Santa Rosa 12%

SCC_TYPE: Communication Disorders Center 25%, Rehabilitation Center 25%, Metabolic Center 12%, HRIF - Regional 12%, Communication Disorders Center 12%, Community Neonatal Intensive C 12%

COUNTY: Orange 38%, Los Angeles 25%, Alameda 12%, San Bernardino 12%, Sonoma 12%

NPI: 0 25%, 1003961251 12%, 1669437075 12%, 1003133695 12%, 1760783344 12%, 1336173269 12%, 1265700942 12%

PROVIDER_NAME: Univ of Calif Irvine 25%, Childrens Hosp Med Ctr 12%, University Head Neck Surge 12%, Mountain View Child Care Inc 12%, Serendipity Hearing Inc 12%, Providence St Joseph Med 12%, Connect Hearing, Inc 12%

BUSINESS_NAME: Univ of Calif Irvine 25%, Children's Hosp Med Cent 12%, Regents of The University of 12%, Totally Kids Rehabilitation 12%, Sonus Sf0010 12%, Providence St Joseph Med 12%, Newport Audiology Centers 12%

ADDRESS_LINE_1: 101 City Dr S 38%, 51ST And Grove Street 12%, 1720 Mountain View Avenue 12%, Unknown 12%, Buena Vista Alameda Street 12%, 4725 B Hoen Avenue 12%

ADDRESS_LINE_2: Building 25 50%, Suite B 50%

CITY: Orange 38%, Oakland 12%, Loma Linda 12%, Unknown 12%, Burbank 12%, Santa Rosa 12%

ZIP_CODE: 92868-3201 38%, 94609 12%, 92354-1727 12%, 0 12%, 91505-4809 12%, 95405-9405 12%

PHONE: (714) 456-6011 29%, (510) 428-3885x5724 14%, (714) 456-7890 14%, (909) 796-6915 14%, (818) 734-9124 14%, (707) 542-1154 14%

FID: 8 12%, 7 12%, 6 12%, 5 12%, 4 12%, 3 12%, 2 12%, 1 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SCC | category | 8 | 0 | 7.09.30A 1; 7.37.20 1; 7.35.77 1; 7.05.20 1 |
| CENTER_NAME | category | 6 | 0 | UC Irvine Medical Center 3; UCSF Benioff Children's H 1; Totally Kids Rehabilitati 1; SONUS NORTHRIDGE 1 |
| SCC_TYPE | category | 6 | 0 | Communication Disorders C 2; Rehabilitation Center 2; Metabolic Center 1; HRIF - Regional 1 |
| COUNTY | category | 5 | 0 | Orange 3; Los Angeles 2; Alameda 1; San Bernardino 1 |
| NPI | category | 7 | 0 | 0 2; 1003961251 1; 1669437075 1; 1003133695 1 |
| PROVIDER_NAME | category | 7 | 0 | Univ of Calif Irvine 2; Childrens Hosp Med Ctr 1; University Head Neck Surg 1; Mountain View Child Care  1 |
| BUSINESS_NAME | category | 7 | 0 | Univ of Calif Irvine 2; Children's Hosp Med Cent 1; Regents of The University 1; Totally Kids Rehabilitati 1 |
| ADDRESS_LINE_1 | category | 6 | 0 | 101 City Dr S 3; 51ST And Grove Street 1; 1720 Mountain View Avenue 1; Unknown 1 |
| ADDRESS_LINE_2 | category | 3 | 6 | Building 25 1; Suite B 1 |
| CITY | category | 6 | 0 | Orange 3; Oakland 1; Loma Linda 1; Unknown 1 |
| STATE | other | 1 | 0 | CA 8 |
| ZIP_CODE | category | 6 | 0 | 92868-3201 3; 94609 1; 92354-1727 1; 0 1 |
| PHONE | category | 7 | 1 | (714) 456-6011 2; (510) 428-3885x5724 1; (714) 456-7890 1; (909) 796-6915 1 |
| FID | category | 8 | 0 | 8 1; 7 1; 6 1; 5 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:30:43.13103 8 |
| SOURCE_RUN_ID | audit | 1 | 0 | 1be32d57-641f-42c2-8dde-6 8 |
| SRC_SHA256 | who | 1 | 0 | 0d4dc62318db594c16df4c71b 8 |
