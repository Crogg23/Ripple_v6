# PORTAL_ARC_ATLANTA_DATAATLA_7D3C4A9739

rows 57  columns 36  scan 4.4s

roles: amount 6, audit 2, category 13, date 3, empty 2, other 5, who 6

## when

CREATIONDATE
  2025        57  ##############################

EDITDATE
  2025        57  ##############################

INGESTED_AT
  2026        57  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MIN_SQFT | 39 | 1 | 5.0K | 77.2K | 100.0K | 576.5K |
| MAX_SQFT | 38 | 1.5K | 10.0K | 100.0K | 100.0K | 1.06M |
| EMPNUM | 56 | 2 | 8 | 96.65 | 150 | 782 |
| SALESVOL | 54 | 254.0K | 1.47M | 20.45M | 33.45M | 148.53M |
| LATITUDE | 57 | 33.53 | 33.83 | 34.08 | 34.09 | 1.9K |
| LONGITUDE | 57 | -84.66 | -84.37 | -84.17 | -84.16 | -4.8K |

## who

CONAME by rows
         1  Exclusive Women's Health Care
         1  Peachtree Health & Rehab
         1  Workit Health Mi PLLC
         1  Nile Women's Health Care
         1  GKM Healthcare Clinic
         1  Winton Chiropractic Health Clinic
         1  Mindbodysoul Mental Health & Family Practice LLC
         1  Atlanta Health & Rehab
         1  Women's Health Specialist of North Atlanta
         1  Four Winds Health
         1  Women's Health Ctr-North
         1  Northside Behavioral Health
         1  Georgia Health Clinics, LLC
         1  Viewfi Health Penn, P C
         1  Department of Health Service
         1  Ageless Men's Health
         1  United Health & Behavioral
         1  Alpha Omega Health Center of Roswell
         1  Palmetto Health Council Inc
         1  Health Service Center Inc

CONAME by dollars
       34.09        1 rows  Legacy Health Care
       34.08        1 rows  Complete Health Diagnostics
       34.06        1 rows  Health Choice Urgent Care-Roswell
       34.06        1 rows  North Fulton Health Care
       34.06        1 rows  Skyn Clinic
       34.06        1 rows  Active Life Health of Alpharetta PLLC
       34.06        1 rows  Women's Health Ctr-North
       34.06        1 rows  Northside Behavioral Health
       34.05        1 rows  Georgia Health Clinics, LLC
       34.05        1 rows  Health Whole Body
       34.05        1 rows  Restore Health Group
       34.05        1 rows  Pars Health Clinic LLC
       34.05        1 rows  Women's Health Specialist of North Atlanta
       34.04        1 rows  Nile Women's Health Care
       34.04        1 rows  Health Service Center Inc
       34.04        1 rows  Alpha Omega Health Center of Roswell
       34.04        1 rows  GKM Healthcare Clinic
       34.03        1 rows  Pinnacle Health Services
       33.99        1 rows  Four Winds Health
       33.99        1 rows  Winton Chiropractic Health Clinic

STATE_NAME by rows
        57  Georgia

STATE_NAME by dollars
        1.9K       57 rows  Georgia

SOURCE by rows
        57  Data Axle

SOURCE by dollars
        1.9K       57 rows  Data Axle

CREATOR by rows
        57  gpickren2

CREATOR by dollars
        1.9K       57 rows  gpickren2

## who x when

CONAME by CREATIONDATE, dollars = LATITUDE
  Active Life Health of Alpharetta PLLC     2025:34.06
  Ageless Men's Health                      2025:33.83
  Alpha Omega Health Center of Roswell      2025:34.04
  Atlanta Health & Rehab                    2025:33.66
  Complete Health Diagnostics               2025:34.08
  Department of Health Service              2025:33.75
  Exclusive Women's Health Care             2025:33.73
  Four Winds Health                         2025:33.99
  GKM Healthcare Clinic                     2025:34.04
  Georgia Health Clinics, LLC               2025:34.05
  Health Choice Urgent Care-Roswell         2025:34.06
  Health Service Center Inc                 2025:34.04
  Health Whole Body                         2025:34.05
  Legacy Health Care                        2025:34.09
  Mindbodysoul Mental Health & Family Prac  2025:33.78
  Nile Women's Health Care                  2025:34.04
  North Fulton Health Care                  2025:34.06
  Northside Behavioral Health               2025:34.06
  Palmetto Health Council Inc               2025:33.53
  Pars Health Clinic LLC                    2025:34.05
  Peachtree Health & Rehab                  2025:33.92
  Pinnacle Health Services                  2025:34.03
  Restore Health Group                      2025:34.05
  Skyn Clinic                               2025:34.06
  United Health & Behavioral                2025:33.74
  Viewfi Health Penn, P C                   2025:33.85
  Winton Chiropractic Health Clinic         2025:33.99
  Women's Health Ctr-North                  2025:34.06
  Women's Health Specialist of North Atlan  2025:34.05
  Workit Health Mi PLLC                     2025:33.91

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2025:1.9K

## what

ADDR: Piedmont Rd NE 16%, W Peachtree St NW 12%, Holcomb Bridge Rd 12%, Roswell Rd 8%, Crabapple Rd 8%, Donald Lee Hollowell Pkwy NW 8%, Mansell Rd 8%, Georgia Ave SE 8%, Hospital Blvd 8%, W Crossville Rd 4%, Peachtree Dunwoody Rd 4%, Old National Hwy 4%

CITY: Atlanta 54%, Roswell 23%, Alpharetta 9%, Sandy Springs 5%, College Park 4%, Johns Creek 4%, Palmetto 2%

ZIP: 30076 22%, 30075 10%, 30308 10%, 30328 8%, 30312 8%, 30309 8%, 30318 8%, 30305 8%, 30315 5%, 30097 5%, 30314 5%, 30022 5%

NAICS: 62111129 77%, 62199921 16%, 62149306 4%, 62142002 2%, 62211003 2%

NAICS_ALL: 62111129 42%, 62199921 18%, 62111129, 62111107 9%, 62111129, 62199921 9%, 62111129, 62111107, 62131002 7%, 62149306, 62111129 2%, 62142002, 62221001, 62111129,  2%, 62149306, 62111107 2%, 62211003 2%, 62199921, 62111129 2%, 62111129, 62199921, 62131002,  2%, 62111129, 62111107, 62199918,  2%

SIC: 801104 77%, 809907 16%, 809320 4%, 809305 2%, 806201 2%

SIC_ALL: 801104 42%, 809907 18%, 801104, 801101 9%, 801104, 809907 9%, 801104, 801101, 804101 7%, 809320, 801104 2%, 809305, 806301, 801104, 801101 2%, 809320, 801101 2%, 806201 2%, 809907, 801104 2%, 801104, 809907, 804101, 729917 2%, 801104, 801101, 809906, 839998 2%

INDUSTRY_DESC: Clinics 42%, Health Services 18%, Clinics, Physicians & Surgeons 9%, Clinics, Health Services 9%, Clinics, Physicians & Surgeons 7%, Urgent Medical Care Centers an 2%, Outpatient Mental Health & Sub 2%, Urgent Medical Care Centers an 2%, Medical Centers 2%, Health Services, Clinics 2%, Clinics, Health Services, Chir 2%, Clinics, Physicians & Surgeons 2%

HQNAME: Premise Health 20%, Grady Health System 20%, Spelman College 20%, Oak Street Health, Inc 20%, Everside Health 20%

LOC_CONF: Very High 88%, High 12%

PLACETYPE: Independent 91%, Branch 9%

SQFOOTAGE: 2500 - 4999 26%, 20000 - 39999 23%, 5000 - 9999 15%, 40000 - 99999 13%, 10000 - 19999 10%, 1 - 1499 8%, 1500 - 2499 3%, 100000+ 3%

DESC: CONAME, Atlanta, Georgia 54%, CONAME, Roswell, Georgia 23%, CONAME, Alpharetta, Georgia 9%, CONAME, Sandy Springs, Georgia 5%, CONAME, College Park, Georgia 4%, CONAME, Johns Creek, Georgia 4%, CONAME, Palmetto, Georgia 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 57 | 0 | 57 1; 56 1; 55 1; 54 1 |
| CONAME | who | 56 | 0 | Health Choice Urgent Care 1; The Amen Clinics 1; Swift Health Urgent Care  1; Southside Medical Ctr Sch 1 |
| ADDR | category | 44 | 0 | Piedmont Rd NE 4; W Peachtree St NW 3; Holcomb Bridge Rd 3; Roswell Rd 2 |
| CITY | category | 7 | 0 | Atlanta 31; Roswell 13; Alpharetta 5; Sandy Springs 3 |
| STATE_NAME | who | 1 | 0 | Georgia 57 |
| STATE | other | 1 | 0 | GA 57 |
| ZIP | category | 27 | 0 | 30076 9; 30075 4; 30308 4; 30328 3 |
| ZIP4 | other | 53 | 3 | 3000 2; 7525 1; 7156 1; 3244 1 |
| NAICS | category | 5 | 0 | 62111129 44; 62199921 9; 62149306 2; 62142002 1 |
| NAICS_ALL | category | 24 | 0 | 62111129 19; 62199921 8; 62111129, 62111107 4; 62111129, 62199921 4 |
| SIC | category | 5 | 0 | 801104 44; 809907 9; 809320 2; 809305 1 |
| SIC_ALL | category | 24 | 0 | 801104 19; 809907 8; 801104, 801101 4; 801104, 809907 4 |
| INDUSTRY_DESC | category | 24 | 0 | Clinics 19; Health Services 8; Clinics, Physicians & Sur 4; Clinics, Health Services 4 |
| AFFILIATE | empty | 1 | 57 |  |
| BRAND | empty | 1 | 57 |  |
| HQNAME | category | 6 | 52 | Premise Health 1; Grady Health System 1; Spelman College 1; Oak Street Health, Inc 1 |
| LOC_CONF | category | 2 | 0 | Very High 50; High 7 |
| PLACETYPE | category | 2 | 0 | Independent 52; Branch 5 |
| SQFOOTAGE | category | 9 | 18 | 2500 - 4999 10; 20000 - 39999 9; 5000 - 9999 6; 40000 - 99999 5 |
| MIN_SQFT | amount | 9 | 0 | nan 18; 2500.0 10; 20000.0 9; 5000.0 6 |
| MAX_SQFT | amount | 8 | 0 | nan 19; 4999.0 10; 39999.0 9; 9999.0 6 |
| EMPNUM | amount | 23 | 0 | 4.0 7; 6.0 6; 14.0 5; 8.0 5 |
| SALESVOL | amount | 27 | 0 | 893000.0 6; 1339000.0 5; 3123000.0 4; 1116000.0 4 |
| SOURCE | who | 1 | 0 | Data Axle 57 |
| ESRI_PID | other | 55 | 0 | d42be43c546d75236878928e4 1; a5d099552a58a15efb6e7e5d3 1; 8111775ff491e2a2d3830958c 1; 5b38b381115b1a6a98d7ee36c 1 |
| DESC | category | 7 | 0 | CONAME, Atlanta, Georgia 31; CONAME, Roswell, Georgia 13; CONAME, Alpharetta, Georg 5; CONAME, Sandy Springs, Ge 3 |
| LATITUDE | amount | 55 | 0 | 33.73708599970598 2; 34.057990999878335 1; 33.9159539998675 1; 33.613915999828585 1 |
| LONGITUDE | amount | 56 | 0 | -84.37940499964606 2; -84.38188400038555 1; -84.35062300040072 1; -84.47297300041369 1 |
| CREATIONDATE | date | 1 | 0 | 1738179790916 57 |
| CREATOR | who | 1 | 0 | gpickren2 57 |
| EDITDATE | date | 1 | 0 | 1738179790916 57 |
| EDITOR | who | 1 | 0 | gpickren2 57 |
| GEOMETRY | other | 56 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:17:34.49143 57 |
| SOURCE_RUN_ID | audit | 1 | 0 | 48c67a0f-6b84-4927-b446-1 57 |
| SRC_SHA256 | who | 1 | 0 | 4142bd84fb65a15a3ae24c07d 57 |
