# PORTAL_ARC_LA_COUNTY_OPEN_D_6DF63A4983

rows 187  columns 16  scan 2.5s

roles: audit 2, category 3, date 1, other 7, state 1, who 3

## when

INGESTED_AT
  2026       187  ##############################

## who

BUSINESS_NAME by rows
         9  Kaiser Foundation Hosp
         4  Kaiser Foundation Hospital
         1  National Rehab Ctr
         1  Sierra Vista Regional
         1  California Hospital Medical
         1  Sutter Solano Medical
         1  San Antonio Community Ho
         1  Adventist Medical Hanford
         1  Scripps Mercy Hospital Chula
         1  Northern Inyo Hospital
         1  El Camino Hosp
         1  Comm Hosp of San Bernardino
         1  Calif Pacific Med Ctr
         1  Saint Agnes Medical Center
         1  Washington Hospital
         1  John Muir Medical Center
         1  Adventist Health Bakersfield
         1  Providence Cedars-Sinai
         1  Simi Valley Hosp Hlth
         1  Centinela Hosp Med Ctr

LEGAL_NAME by rows
        10  Dignity Health
        10  Kaiser Foundation Hosp
         5  Sutter Bay Hospitals
         4  Kaiser Foundation Hospitals
         4  Sutter Valley Hospitals
         3  Providence Health System
         3  Kaiser Foundation Hospital
         3  Dignity Community Care
         3  Scripps Health
         2  Emanate Health Medical
         2  Los Robles Hospital
         2  Fresno Community Hospital
         2  Kaiser Foundation
         2  Sharp Memorial Hosp
         2  Doctors Medical Center of
         2  St Joseph Health Northern
         1  Santa Ynez Valley
         1  Cha Hollywood Medical
         1  Central California
         1  Tri City Hospital

SRC_SHA256 by rows
       187  7f55000fc2f685ba820fd46cadd20f97d03e21d667d3f75c3d493fe72cdfc5e1

## who x when

BUSINESS_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Adventist Health Bakersfield              2026:1
  Adventist Medical Hanford                 2026:1
  Calif Pacific Med Ctr                     2026:1
  California Hospital Medical               2026:1
  Centinela Hosp Med Ctr                    2026:1
  Comm Hosp of San Bernardino               2026:1
  El Camino Hosp                            2026:1
  John Muir Medical Center                  2026:1
  Kaiser Foundation Hosp                    2026:9
  Kaiser Foundation Hospital                2026:4
  National Rehab Ctr                        2026:1
  Northern Inyo Hospital                    2026:1
  Providence Cedars-Sinai                   2026:1
  Saint Agnes Medical Center                2026:1
  San Antonio Community Ho                  2026:1
  Scripps Mercy Hospital Chula              2026:1
  Sierra Vista Regional                     2026:1
  Simi Valley Hosp Hlth                     2026:1
  Sutter Solano Medical                     2026:1
  Washington Hospital                       2026:1

LEGAL_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Central California                        2026:1
  Cha Hollywood Medical                     2026:1
  Dignity Community Care                    2026:3
  Dignity Health                            2026:10
  Doctors Medical Center of                 2026:2
  Emanate Health Medical                    2026:2
  Fresno Community Hospital                 2026:2
  Kaiser Foundation                         2026:2
  Kaiser Foundation Hosp                    2026:10
  Kaiser Foundation Hospital                2026:3
  Kaiser Foundation Hospitals               2026:4
  Los Robles Hospital                       2026:2
  Providence Health System                  2026:3
  Santa Ynez Valley                         2026:1
  Scripps Health                            2026:3
  Sharp Memorial Hosp                       2026:2
  St Joseph Health Northern                 2026:2
  Sutter Bay Hospitals                      2026:5
  Sutter Valley Hospitals                   2026:4
  Tri City Hospital                         2026:1

## where

STATE: CA 183, NV 2, OR 2

## what

FACILITY_TYPE: Pediatric Community 29%, Limited 18%, Special 16%, General Community (over 14 wit 13%, Tertiary 12%, Standard 11%, Long 1%

COUNTY: Los Angeles 37%, San Diego 10%, Orange 8%, San Bernardino 7%, San Francisco 6%, Santa Clara 6%, Alameda 6%, Sacramento 6%, Kern 5%, Ventura 5%, Monterey 3%, Riverside 3%

ADDRESS_LINE_2: nan 97%, P.O. Box 7937 1%, PO Box 819 1%, PO Box 1029 1%, De Las Pulgas 1%, 5th Fl 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | other | 181 | 0 | 1407839921 2; 1659359446 2; 1538157508 1; 1649213000 1 |
| LEGAL_NAME | who | 145 | 0 | Kaiser Foundation Hosp 10; Dignity Health 10; Sutter Bay Hospitals 5; Kaiser Foundation Hospita 4 |
| BUSINESS_NAME | who | 175 | 0 | Kaiser Foundation Hosp 9; Kaiser Foundation Hospita 4; Adventist Health Bakersfi 1; San Francisco Gen Hosp 1 |
| FACILITY_TYPE | category | 7 | 0 | Pediatric Community 54; Limited 34; Special 30; General Community (over 1 25 |
| COUNTY | category | 46 | 0 | Los Angeles 47; San Diego 12; Orange 10; San Bernardino 9 |
| ADDRESS_LINE_1 | other | 186 | 0 | 2615 Chester Avenue 1; 1001 Potrero Avenue 1; 1805 Medical Center Drive 1; 999 San Bernardino Road 1 |
| ADDRESS_LINE_2 | category | 6 | 0 | nan 182; P.O. Box 7937 1; PO Box 819 1; PO Box 1029 1 |
| CITY | other | 123 | 0 | Los Angeles 13; San Francisco 7; San Diego 6; Sacramento 6 |
| STATE | state | 3 | 0 | CA 183; NV 2; OR 2 |
| ZIP_CODE | other | 185 | 0 | 90242-3456 2; 93301-2006 1; 94110-3518 1; 92411-1217 1 |
| PHONE | other | 177 | 0 | (702) 855-1022 5; nan 4; (415) 438-5500 3; (562) 401-7022 2 |
| FID | other | 188 | 0 | 187 1; 186 1; 185 1; 184 1 |
| GEOMETRY | other | 183 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:32:41.54121 187 |
| SOURCE_RUN_ID | audit | 1 | 0 | 50c620b1-f1de-454d-b792-9 187 |
| SRC_SHA256 | who | 1 | 0 | 7f55000fc2f685ba820fd46ca 187 |
