# PORTAL_ARC_TUCSON_OPEN_DATA_65A6CDEF8F

rows 76  columns 37  scan 5.0s

roles: amount 6, audit 2, category 22, date 1, other 5, who 2

## when

INGESTED_AT
  2026        76  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MIN_SQFT | 57 | 1 | 2.5K | 100.0K | 100.0K | 784.0K |
| MAX_SQFT | 53 | 1.5K | 5.0K | 100.0K | 100.0K | 828.4K |
| EMPNUM | 73 | 2 | 6 | 1.8K | 3.2K | 5.4K |
| SALESVOL | 72 | 695.0K | 1.80M | 100.69M | 219.69M | 559.26M |
| LATITUDE | 75 | 32.18 | 32.24 | 32.27 | 32.27 | 2.4K |
| LONGITUDE | 75 | -111.01 | -110.95 | -110.91 | -110.90 | -8.3K |

## who

CONAME by rows
         1  Small Valley Healthcare Partners
         1  Daily Hope Healthcare Services: Tolulope Green-Yesu, FNP
         1  Saif Mashaqi, MD
         1  Sairam Parthasarathy, MD
         1  Southwest Remote Medicine
         1  The University-AZ Med Ctr Surg Multispecialty Physician Ofc
         1  Arizona Telemedicine Program
         1  Southwest Kidney Institute Vascular Center, LLC
         1  Lauren Elizabeth Estep, MD
         1  Valley Fever Solutions
         1  In Home Support Service LLC
         1  Banner-University Medicine Clinic Tucson
         1  Park Avenue Health-RHBLTN
         1  Joan Louise Machamer, ACNP
         1  Health Choice
         1  Codac Health Recovery & Wellness
         1  Doctor Referrals-Tucson
         1  Sunrise Mental Health LLC
         1  Pure Health & Body Therapy
         1  Marana Health Center Inc

CONAME by dollars
       32.27        1 rows  Stillwater Moriah
       32.27        1 rows  Happy Feet Chinese Reflexology
       32.27        1 rows  Sunrise Mental Health LLC
       32.26        1 rows  Tucson Interfaith Hiv-Aid
       32.26        1 rows  Gut Instinct Wellness LLC
       32.26        1 rows  Tihan
       32.26        1 rows  Backyard Healthcare Project
       32.26        1 rows  Valor Health Services, LLC
       32.26        1 rows  Peoples Health Care Connection
       32.26        1 rows  Health Choice
       32.25        1 rows  Northwest Gastroenterology At Grant
       32.25        1 rows  In Home Support Service LLC
       32.25        1 rows  Park Avenue Health-RHBLTN
       32.25        1 rows  Higher Self Wellness
       32.24        1 rows  University-AZ Health Sciences
       32.24        1 rows  Arizona Health Sciences Center
       32.24        1 rows  Banner-University Medicine Clinic Tucson
       32.24        1 rows  Saif Mashaqi, MD
       32.24        1 rows  The University-AZ Med Ctr Surg Multispecialty Physician Ofc
       32.24        1 rows  Native American Cardiology

SRC_SHA256 by rows
        76  244f74fe8a4f502ae0c97eaaa2d5c8b27b24fa9f21c06f75909e24db04a6bb47

SRC_SHA256 by dollars
        2.4K       76 rows  244f74fe8a4f502ae0c97eaaa2d5c8b27b24fa9f21c06f75909e24db04a6

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  Arizona Telemedicine Program              2026:32.24
  Backyard Healthcare Project               2026:32.26
  Banner-University Medicine Clinic Tucson  2026:32.24
  Codac Health Recovery & Wellness          2026:32.21
  Daily Hope Healthcare Services: Tolulope  2026:32.22
  Doctor Referrals-Tucson                   2026:32.22
  Gut Instinct Wellness LLC                 2026:32.26
  Happy Feet Chinese Reflexology            2026:32.27
  Health Choice                             2026:32.26
  Higher Self Wellness                      2026:32.25
  In Home Support Service LLC               2026:32.25
  Joan Louise Machamer, ACNP                2026:32.24
  Lauren Elizabeth Estep, MD                2026:32.24
  Marana Health Center Inc                  2026:32.23
  Northwest Gastroenterology At Grant       2026:32.25
  Park Avenue Health-RHBLTN                 2026:32.25
  Peoples Health Care Connection            2026:32.26
  Pure Health & Body Therapy                2026:32.23
  Saif Mashaqi, MD                          2026:32.24
  Sairam Parthasarathy, MD                  2026:32.24
  Small Valley Healthcare Partners          2026:32.22
  Southwest Kidney Institute Vascular Cent  2026:32.22
  Southwest Remote Medicine                 2026:32.22
  Stillwater Moriah                         2026:32.27
  Sunrise Mental Health LLC                 2026:32.27
  The University-AZ Med Ctr Surg Multispec  2026:32.24
  Tihan                                     2026:32.26
  Tucson Interfaith Hiv-Aid                 2026:32.26
  Valley Fever Solutions                    2026:32.22
  Valor Health Services, LLC                2026:32.26

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  244f74fe8a4f502ae0c97eaaa2d5c8b27b24fa9f  2026:2.4K

## what

ADDR: N Campbell Ave 38%, E Fort Lowell Rd 11%, E Broadway Blvd 6%, N 1st Ave 6%, W Saint Marys Rd 6%, N Bonita Ave 6%, E Congress St 4%, S 6 Th Ave 4%, N Tucson Blvd 4%, S Euclid Ave 4%, E Speedway Blvd 4%, N Silverbell Rd 4%

CITY: Tucson 99%, nan 1%

STATE_NAME: Arizona 99%, nan 1%

STATE: AZ 99%, nan 1%

ZIP: 85719 42%, 85701 12%, 85745 12%, 85724 11%, 85705 9%, 85716 8%, 85723 3%, nan 1%, 85711 1%, 85713 1%

NAICS: 62199921 52%, 62211003 9%, 62199962 9%, 62199952 7%, 62211002 4%, 62199901 4%, 62211001 4%, 62199907 3%, 62199926 3%, nan 1%, 62199963 1%, 62199935 1%

NAICS_ALL: 62199921 49%, 62199962 11%, 62211003 9%, 62199952 8%, 62211001 6%, 62199907 4%, 62199926 4%, nan 2%, 62199921, 99999005 2%, 62211002, 62211003, 62231004 2%, 62199901, 81311021, 81331908 2%, 62199901 2%

SIC: 809907 52%, 806201 9%, 809974 9%, 809921 7%, 806202 4%, 809933 4%, 806203 4%, 809948 3%, 809909 3%, nan 1%, 809975 1%, 809951 1%

SIC_ALL: 809907 49%, 809974 11%, 806201 9%, 809921 8%, 806203 6%, 809948 4%, 809909 4%, nan 2%, 809907, 999966 2%, 806202, 806201, 806904 2%, 809933, 866110, 839998 2%, 809933 2%

INDUSTRY_DESC: Health Services 49%, Sleep Disorders-Diagnostic/Tre 11%, Medical Centers 9%, Wellness Programs 8%, Emergency Medical & Surgical S 6%, Medical Emergency Training 4%, Holistic Health Services 4%, nan 2%, Health Services, Federal Gover 2%, Hospitals, Medical Centers, Go 2%, Aids Information & Testing, Re 2%, Aids Information & Testing 2%

AFFILIATE: nan 100%

BRAND: nan 100%

HQNAME: Banner-University Medical Cent 17%, Banner Health 17%, nan 8%, US Department of Veterans Affa 8%, Tucson VA Medical Center 8%, Carondalet St Mary's Hospital 8%, University Of Arizona 8%, CSL Plasma Inc 8%, Tenet Healthcare Corporation 8%, Arizona Urology Specialists, P 8%

LOC_CONF: Very High 96%, High 3%, nan 1%

NAICS_SECT: Health Care & Social Assistanc 99%, nan 1%

PLACETYPE: Independent 82%, Branch 11%, Headquarters 7%, nan 1%

SQFOOTAGE: 2500 - 4999 29%, 1500 - 2499 19%, 10000 - 19999 14%, 5000 - 9999 9%, 20000 - 39999 9%, 100000+ 7%, 1 - 1499 7%, 40000 - 99999 5%, nan 2%

SOURCE: Data Axle 99%, nan 1%

CREATIONDATE: 1742236997000.0 99%, nan 1%

CREATOR: ehammon1_cotgis 99%, nan 1%

EDITDATE: 1742236997000.0 99%, nan 1%

EDITOR: ehammon1_cotgis 99%, nan 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 76 | 0 | 76 1; 75 1; 74 1; 73 1 |
| CONAME | who | 77 | 0 | MHBCRC 1; Willow Springs Behavioral 1; Wellness Center USA, Inc 1; Valor Health Services, LL 1 |
| ADDR | category | 41 | 0 | N Campbell Ave 18; E Fort Lowell Rd 5; E Broadway Blvd 3; N 1st Ave 3 |
| CITY | category | 2 | 0 | Tucson 75; nan 1 |
| STATE_NAME | category | 2 | 0 | Arizona 75; nan 1 |
| STATE | category | 2 | 0 | AZ 75; nan 1 |
| ZIP | category | 10 | 0 | 85719 32; 85701 9; 85745 9; 85724 8 |
| ZIP4 | other | 56 | 3 | 4330 9; 0002 6; 0001 3; 2750 3 |
| NAICS | category | 19 | 0 | 62199921 36; 62211003 6; 62199962 6; 62199952 5 |
| NAICS_ALL | category | 34 | 0 | 62199921 26; 62199962 6; 62211003 5; 62199952 4 |
| SIC | category | 19 | 0 | 809907 36; 806201 6; 809974 6; 809921 5 |
| SIC_ALL | category | 35 | 0 | 809907 26; 809974 6; 806201 5; 809921 4 |
| INDUSTRY_DESC | category | 34 | 0 | Health Services 26; Sleep Disorders-Diagnosti 6; Medical Centers 5; Wellness Programs 4 |
| AFFILIATE | category | 2 | 75 | nan 1 |
| BRAND | category | 2 | 75 | nan 1 |
| HQNAME | category | 11 | 64 | Banner-University Medical 2; Banner Health 2; nan 1; US Department of Veterans 1 |
| LOC_CONF | category | 3 | 0 | Very High 73; High 2; nan 1 |
| NAICS_SECT | category | 2 | 0 | Health Care & Social Assi 75; nan 1 |
| PLACETYPE | category | 4 | 0 | Independent 62; Branch 8; Headquarters 5; nan 1 |
| SQFOOTAGE | category | 10 | 18 | 2500 - 4999 17; 1500 - 2499 11; 10000 - 19999 8; 5000 - 9999 5 |
| MIN_SQFT | amount | 9 | 0 | nan 19; 2500.0 17; 1500.0 11; 10000.0 8 |
| MAX_SQFT | amount | 8 | 0 | nan 23; 4999.0 17; 2499.0 11; 19999.0 8 |
| EMPNUM | amount | 27 | 0 | 3.0 13; 5.0 11; 2.0 6; 6.0 5 |
| SALESVOL | amount | 31 | 0 | 1042000.0 12; 1737000.0 10; 695000.0 7; 3820000.0 5 |
| SOURCE | category | 2 | 0 | Data Axle 75; nan 1 |
| ESRI_PID | other | 77 | 0 | nan 1; c9016191d22d390b1ebf9e36f 1; c4368186e91d9b5b5d63f3e61 1; 78a0310168add675cd12f082c 1 |
| DESC | other | 77 | 0 | nan 1; Willow Springs Behavioral 1; Wellness Center USA, Inc, 1; Valor Health Services, LL 1 |
| LATITUDE | amount | 58 | 0 | 32.24183399982495 9; 32.240494313920266 4; 32.24049400011885 3; 32.226586000351354 3 |
| LONGITUDE | amount | 58 | 0 | -110.94724200037646 9; -110.94608379978565 4; -110.94608400010999 3; -110.98532300011681 3 |
| CREATIONDATE | category | 2 | 0 | 1742236997000.0 75; nan 1 |
| CREATOR | category | 2 | 0 | ehammon1_cotgis 75; nan 1 |
| EDITDATE | category | 2 | 0 | 1742236997000.0 75; nan 1 |
| EDITOR | category | 2 | 0 | ehammon1_cotgis 75; nan 1 |
| GEOMETRY | other | 58 | 0 | {"type": "Point", "coordi 9; {"type": "Point", "coordi 4; {"type": "Point", "coordi 3; {"type": "Point", "coordi 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:18:48.53142 76 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3c4503cf-64c5-45e1-aeeb-f 76 |
| SRC_SHA256 | who | 1 | 0 | 244f74fe8a4f502ae0c97eaaa 76 |
