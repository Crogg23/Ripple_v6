# PORTAL_ARC_ATLANTA_DATAATLA_F07E02DA21

rows 73  columns 36  scan 3.8s

roles: amount 6, audit 2, category 15, date 3, empty 2, other 3, who 6

## when

CREATIONDATE
  2025        73  ##############################

EDITDATE
  2025        73  ##############################

INGESTED_AT
  2026        73  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MIN_SQFT | 63 | 1 | 20.0K | 100.0K | 100.0K | 2.12M |
| MAX_SQFT | 49 | 1.5K | 20.0K | 100.0K | 100.0K | 1.65M |
| EMPNUM | 65 | 2 | 14 | 4.2K | 7.2K | 12.0K |
| SALESVOL | 63 | 224.0K | 2.48M | 950.99M | 1.58B | 2.61B |
| LATITUDE | 73 | 33.66 | 33.91 | 34.07 | 34.07 | 2.5K |
| LONGITUDE | 73 | -84.41 | -84.35 | -84.18 | -84.17 | -6.2K |

## who

CONAME by rows
         3  Northside Hospital
         2  Northside Hospital Cancer Center
         2  Piedmont Atlanta Hospital Sleep Center
         2  Winship Cancer Institute at Emory Saint Joseph's Hospital
         2  Piedmont Atlanta Hospital Outpatient Rehabilitation Services
         1  New View Wellness LLC
         1  Emory Women's Center at Emory Saint Joseph's Hospital
         1  Arthritis Center Piedmont Hospital
         1  Piedmont Atlanta Hospital Radiation Oncology Services
         1  Grady Memorial Hospital Obstetrics
         1  Children's Healthcare Hospital
         1  Nad in Georgia
         1  Piedmont Atlanta Hospital McDonnell Outpatient Surgery Ctr
         1  Walgreens Pharmacy at Piedmont Hospital
         1  Centillion Health, LLC
         1  Emory University Hospital Midtown
         1  Piedmont Atlanta Hospital Diabetes Resource Center
         1  Emory Clinic at 6300 Hospital Parkway
         1  Piedmont Atlanta Hospital Fuqua Heart Center
         1  Hospital Pharmacy

CONAME by dollars
      101.73        3 rows  Northside Hospital
       67.82        2 rows  Winship Cancer Institute at Emory Saint Joseph's Hospital
       67.82        2 rows  Northside Hospital Cancer Center
       67.62        2 rows  Piedmont Atlanta Hospital Outpatient Rehabilitation Services
       67.60        2 rows  Piedmont Atlanta Hospital Sleep Center
       34.07        1 rows  Emory Johns Creek Hospital-Pulmonology
       34.07        1 rows  Emory Vein Center at Johns Creek Hospital
       34.07        1 rows  Emory Clinic at 6300 Hospital Parkway
       34.07        1 rows  Emory Johns Creek Hospital Campus
       34.07        1 rows  Emory Johns Creek Hospital
       34.07        1 rows  Northside Hospital Radiation Oncology
       34.07        1 rows  Nad in Georgia
       34.06        1 rows  New View Wellness LLC
       34.06        1 rows  North Fulton Hospital Cancer Center
       34.06        1 rows  Pain Control Center of North Fulton Regional Hospital
       34.06        1 rows  North Fulton Hospital Pain & Spine Center
       34.06        1 rows  Centillion Health, LLC
       34.06        1 rows  North Fulton Regional Hospital-Pathology
       34.06        1 rows  Perimeter Behavioral Hospital of West Memphis
       34.05        1 rows  Emory Clinic Hospital Medicine

STATE_NAME by rows
        73  Georgia

STATE_NAME by dollars
        2.5K       73 rows  Georgia

SOURCE by rows
        73  Data Axle

SOURCE by dollars
        2.5K       73 rows  Data Axle

CREATOR by rows
        73  gpickren2

CREATOR by dollars
        2.5K       73 rows  gpickren2

## who x when

CONAME by CREATIONDATE, dollars = LATITUDE
  Arthritis Center Piedmont Hospital        2025:33.81
  Centillion Health, LLC                    2025:34.06
  Children's Healthcare Hospital            2025:33.91
  Emory Clinic at 6300 Hospital Parkway     2025:34.07
  Emory Johns Creek Hospital                2025:34.07
  Emory Johns Creek Hospital Campus         2025:34.07
  Emory Johns Creek Hospital-Pulmonology    2025:34.07
  Emory University Hospital Midtown         2025:33.77
  Emory Vein Center at Johns Creek Hospita  2025:34.07
  Emory Women's Center at Emory Saint Jose  2025:33.91
  Grady Memorial Hospital Obstetrics        2025:33.75
  Hospital Pharmacy                         2025:33.75
  Nad in Georgia                            2025:34.07
  New View Wellness LLC                     2025:34.06
  North Fulton Hospital Cancer Center       2025:34.06
  North Fulton Hospital Pain & Spine Cente  2025:34.06
  North Fulton Regional Hospital-Pathology  2025:34.06
  Northside Hospital                        2025:101.73
  Northside Hospital Cancer Center          2025:67.82
  Northside Hospital Radiation Oncology     2025:34.07
  Pain Control Center of North Fulton Regi  2025:34.06
  Perimeter Behavioral Hospital of West Me  2025:34.06
  Piedmont Atlanta Hospital Diabetes Resou  2025:33.81
  Piedmont Atlanta Hospital Fuqua Heart Ce  2025:33.81
  Piedmont Atlanta Hospital McDonnell Outp  2025:33.81
  Piedmont Atlanta Hospital Outpatient Reh  2025:67.62
  Piedmont Atlanta Hospital Radiation Onco  2025:33.80
  Piedmont Atlanta Hospital Sleep Center    2025:67.60
  Walgreens Pharmacy at Piedmont Hospital   2025:33.81
  Winship Cancer Institute at Emory Saint   2025:67.82

STATE_NAME by CREATIONDATE, dollars = LATITUDE
  Georgia                                   2025:2.5K

## what

ADDR: Peachtree Dunwoody Rd 27%, Peachtree Rd NW 16%, Johnson Ferry Rd 15%, Hospital Pkwy 9%, Jesse Hill Jr Dr SE 7%, Hospital Blvd 7%, Peachtree St NE 5%, Peachtree Rd NE 5%, Peachtree Road Nw 77 2%, Howell Mill Rd NW 2%, Northwinds Pkwy 2%, Collier Rd NW 2%

CITY: Atlanta 77%, Roswell 8%, Johns Creek 8%, Alpharetta 4%, Duluth 1%, Sandy Springs 1%

ZIP: 30342 31%, 30309 25%, 30097 10%, 30303 7%, 30308 7%, 30076 6%, 30328 6%, 30009 3%, 30075 3%, 30318 1%, 30005 1%, 30354 1%

ZIP4: 1281 25%, 1731 9%, 1476 9%, 1611 9%, 1605 9%, 1701 6%, 2247 6%, 4789 6%, 1549 6%, 5911 6%, 3050 6%

NAICS: 62111129 25%, 62211002 19%, 62111107 18%, 62199921 12%, 62231005 7%, 62221001 5%, 45611009 5%, 62221002 5%, 62149305 1%, 62211003 1%

NAICS_ALL: 62111129 21%, 62199921 14%, 62111107 14%, 62111129, 62111107 7%, 62111129, 62211003 7%, 62221001 7%, 45611009 7%, 62231005 7%, 62211002, 62211001 7%, 62221002 5%, 62111107, 62111129 2%, 62231005, 62111107 2%

SIC: 801104 25%, 806202 19%, 801101 18%, 809907 12%, 806906 7%, 806301 5%, 591205 5%, 806398 5%, 809308 1%, 806201 1%

SIC_ALL: 801104 21%, 809907 14%, 801101 14%, 801104, 801101 7%, 801104, 806201 7%, 806301 7%, 591205 7%, 806906 7%, 806202, 806203 7%, 806398 5%, 801101, 801104 2%, 806906, 801101 2%

INDUSTRY_DESC: Clinics 21%, Health Services 14%, Physicians & Surgeons 14%, Clinics, Physicians & Surgeons 7%, Clinics, Medical Centers 7%, Mental Health Services 7%, Pharmacies 7%, Cancer Treatment Centers 7%, Hospitals, Emergency Medical & 7%, Psychiatric & Substance Abuse  5%, Physicians & Surgeons, Clinics 2%, Cancer Treatment Centers, Phys 2%

HQNAME: Piedmont Atlanta 32%, Emory Saint Joseph's Hospital 18%, Emory Healthcare Network 15%, Children's Healthcare of Atlan 9%, Emory Johns Creek Hospital 6%, Emory University Hospital Midt 6%, St Joseph's Hospital 3%, Walgreen Co 3%, Select Medical Corporation 3%, Children's Healthcare of Atlan 3%, Piedmont Healthcare 3%

LOC_CONF: Very High 95%, High 3%, Low 1%, Medium 1%

PLACETYPE: Independent 49%, Branch 37%, Headquarters 14%

SQFOOTAGE: 100000+ 22%, 20000 - 39999 17%, 40000 - 99999 16%, 2500 - 4999 14%, 1 - 1499 13%, 10000 - 19999 11%, 1500 - 2499 5%, 5000 - 9999 2%

DESC: CONAME, Atlanta, Georgia 77%, CONAME, Roswell, Georgia 8%, CONAME, Johns Creek, Georgia 8%, CONAME, Alpharetta, Georgia 4%, CONAME, Duluth, Georgia 1%, CONAME, Sandy Springs, Georgia 1%

GEOMETRY: {"type": "Point", "coordinates 22%, {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 5%, {"type": "Point", "coordinates 5%, {"type": "Point", "coordinates 5%, {"type": "Point", "coordinates 5%, {"type": "Point", "coordinates 5%, {"type": "Point", "coordinates 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 73 | 0 | 73 1; 72 1; 71 1; 70 1 |
| CONAME | who | 68 | 0 | Northside Hospital 3; Winship Cancer Institute  2; Piedmont Atlanta Hospital 2; Piedmont Atlanta Hospital 2 |
| ADDR | category | 30 | 0 | Peachtree Dunwoody Rd 15; Peachtree Rd NW 9; Johnson Ferry Rd 8; Hospital Pkwy 5 |
| CITY | category | 6 | 0 | Atlanta 56; Roswell 6; Johns Creek 6; Alpharetta 3 |
| STATE_NAME | who | 1 | 0 | Georgia 73 |
| STATE | other | 1 | 0 | GA 73 |
| ZIP | category | 13 | 0 | 30342 22; 30309 18; 30097 7; 30303 5 |
| ZIP4 | category | 47 | 6 | 1281 8; 1731 3; 1476 3; 1611 3 |
| NAICS | category | 10 | 0 | 62111129 18; 62211002 14; 62111107 13; 62199921 9 |
| NAICS_ALL | category | 42 | 0 | 62111129 9; 62199921 6; 62111107 6; 62111129, 62111107 3 |
| SIC | category | 10 | 0 | 801104 18; 806202 14; 801101 13; 809907 9 |
| SIC_ALL | category | 42 | 0 | 801104 9; 809907 6; 801101 6; 801104, 801101 3 |
| INDUSTRY_DESC | category | 42 | 0 | Clinics 9; Health Services 6; Physicians & Surgeons 6; Clinics, Physicians & Sur 3 |
| AFFILIATE | empty | 1 | 73 |  |
| BRAND | empty | 1 | 73 |  |
| HQNAME | category | 14 | 37 | Piedmont Atlanta 11; Emory Saint Joseph's Hosp 6; Emory Healthcare Network 5; Children's Healthcare of  3 |
| LOC_CONF | category | 4 | 0 | Very High 69; High 2; Low 1; Medium 1 |
| PLACETYPE | category | 3 | 0 | Independent 36; Branch 27; Headquarters 10 |
| SQFOOTAGE | category | 9 | 10 | 100000+ 14; 20000 - 39999 11; 40000 - 99999 10; 2500 - 4999 9 |
| MIN_SQFT | amount | 9 | 0 | 100000.0 14; 20000.0 11; nan 10; 40000.0 10 |
| MAX_SQFT | amount | 8 | 0 | nan 24; 39999.0 11; 99999.0 10; 4999.0 9 |
| EMPNUM | amount | 34 | 0 | nan 8; 15.0 7; 8.0 4; 5.0 4 |
| SALESVOL | amount | 51 | 0 | nan 10; 447000.0 3; 4015000.0 3; 1116000.0 2 |
| SOURCE | who | 1 | 0 | Data Axle 73 |
| ESRI_PID | other | 73 | 0 | 87f9b96d398b01504b5e904a8 1; af1ef2babdbcad4a6ccc8ea9b 1; a04a09c769805fc82527c6bb6 1; 82704d791a30531d2178402d6 1 |
| DESC | category | 6 | 0 | CONAME, Atlanta, Georgia 56; CONAME, Roswell, Georgia 6; CONAME, Johns Creek, Geor 6; CONAME, Alpharetta, Georg 3 |
| LATITUDE | amount | 48 | 0 | 33.80998999980422 8; 33.910486000072254 5; 33.76895100019894 3; 33.808856000373005 3 |
| LONGITUDE | amount | 47 | 0 | -84.39584799976178 8; -84.3502330004134 5; -84.3495930001808 3; -84.38628800004909 3 |
| CREATIONDATE | date | 1 | 0 | 1738179783477 73 |
| CREATOR | who | 1 | 0 | gpickren2 73 |
| EDITDATE | date | 1 | 0 | 1738179783477 73 |
| EDITOR | who | 1 | 0 | gpickren2 73 |
| GEOMETRY | category | 48 | 0 | {"type": "Point", "coordi 8; {"type": "Point", "coordi 5; {"type": "Point", "coordi 3; {"type": "Point", "coordi 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:18:36.51454 73 |
| SOURCE_RUN_ID | audit | 1 | 0 | e076ea74-9880-48e5-b6a0-6 73 |
| SRC_SHA256 | who | 1 | 0 | 4f40e9fd0c2cfb3aa6743e2ff 73 |
