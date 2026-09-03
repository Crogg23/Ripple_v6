# PORTAL_ARC_LA_COUNTY_OPEN_D_83F0BA30FB

rows 5  columns 15  scan 2.1s

roles: audit 2, category 10, date 1, empty 1, other 1, who 1

## when

INGESTED_AT
  2026         5  ##############################

## who

SRC_SHA256 by rows
         5  362d096693adb4d41279e2d743526263aceca5b9eeb4c416e264944cdd4044d7

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  362d096693adb4d41279e2d743526263aceca5b9  2026:5

## what

NPI: 1356339543 20%, 1689732885 20%, 1457321317 20%, 1194876821 20%, 1003133695 20%

LEGAL_NAME: Willits Hospital Inc 20%, Sutter Bay Hospitals 20%, Palomar Health 20%, Oroville Hospital 20%, Mountain View Child Care Inc 20%

BUSINESS_NAME: Frank R Howard Memorial Hosp 20%, Calif Pacific Med Ctr 20%, Palomar Health Downtown Camp 20%, Oroville Hospital 20%, Totally Kids Rehabilitation 20%

FACILITY_TYPE: Limited 40%, Tertiary 20%, Pediatric Community 20%, Special 20%

COUNTY: Mendocino 20%, San Francisco 20%, San Diego 20%, Butte 20%, San Bernardino 20%

ADDRESS_LINE_1: 1 Marcela Drive 20%, Clay Buchanan Street 20%, 2185 Citracado Parkway 20%, 2767 Olive Highway 20%, 1720 Mountain View Avenue 20%

CITY: Willits 20%, San Francisco 20%, Escondido 20%, Oroville 20%, Loma Linda 20%

ZIP_CODE: 95490-5769 20%, 94115 20%, 92025-4159 20%, 95966-6118 20%, 92354-1727 20%

PHONE: (707) 459-6801 20%, (415) 600-1400 20%, (760) 739-3000 20%, (916) 533-8500 20%, (909) 796-6915 20%

FID: 5 20%, 4 20%, 3 20%, 2 20%, 1 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | category | 5 | 0 | 1356339543 1; 1689732885 1; 1457321317 1; 1194876821 1 |
| LEGAL_NAME | category | 5 | 0 | Willits Hospital Inc 1; Sutter Bay Hospitals 1; Palomar Health 1; Oroville Hospital 1 |
| BUSINESS_NAME | category | 5 | 0 | Frank R Howard Memorial H 1; Calif Pacific Med Ctr 1; Palomar Health Downtown C 1; Oroville Hospital 1 |
| FACILITY_TYPE | category | 4 | 0 | Limited 2; Tertiary 1; Pediatric Community 1; Special 1 |
| COUNTY | category | 5 | 0 | Mendocino 1; San Francisco 1; San Diego 1; Butte 1 |
| ADDRESS_LINE_1 | category | 5 | 0 | 1 Marcela Drive 1; Clay Buchanan Street 1; 2185 Citracado Parkway 1; 2767 Olive Highway 1 |
| ADDRESS_LINE_2 | empty | 1 | 5 |  |
| CITY | category | 5 | 0 | Willits 1; San Francisco 1; Escondido 1; Oroville 1 |
| STATE | other | 1 | 0 | CA 5 |
| ZIP_CODE | category | 5 | 0 | 95490-5769 1; 94115 1; 92025-4159 1; 95966-6118 1 |
| PHONE | category | 5 | 0 | (707) 459-6801 1; (415) 600-1400 1; (760) 739-3000 1; (916) 533-8500 1 |
| FID | category | 5 | 0 | 5 1; 4 1; 3 1; 2 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:30:36.95099 5 |
| SOURCE_RUN_ID | audit | 1 | 0 | 49271ef5-1220-4942-a631-f 5 |
| SRC_SHA256 | who | 1 | 0 | 362d096693adb4d41279e2d74 5 |
