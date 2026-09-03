# PORTAL_ARC_TUCSON_OPEN_DATA_78DF4DC45F

rows 1.0K  columns 27  scan 4.0s

roles: amount 2, audit 2, category 7, date 1, empty 1, id 2, other 5, who 8

## when

INGESTED_AT
  2026      1.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SALESVOL | 549 | 17.0K | 296.0K | 15.60M | 64.08M | 722.42M |
| EMPNUM | 1.0K | 1 | 6 | 200 | 600 | 19.3K |

## who

CONAME by rows
         9  La Frontera Center Inc
         6  Arizona Mentor
         6  Goodwill Donation Center
         5  ATI Physical Therapy
         5  La Petite Academy
         4  Danville Services
         4  Community Options Inc
         3  Fairmount Assisted Living
         3  Blake Foundation
         3  Danville Services of AZ LLC
         3  Casa De Los Ninos
         3  Lutheran Social Service
         3  American Red Cross
         3  Pima Prevention Partnership
         3  Boys & Girls Club of Tucson
         3  Goodwill
         2  Sherwood Village Assisted Living & Memory Care
         2  RISE Services Inc
         2  Habitat For Humanity
         2  Employment Security Appeals

CONAME by dollars
         618        3 rows  Blake Foundation
         508        2 rows  Ppep Inc
         500        1 rows  Developmental Disabilities
         400        1 rows  Headstart
         398        1 rows  Devon Gables Health Care Center
         300        1 rows  Beacon Group
         275        1 rows  Goodwill Industries of Southern Arizona, Inc
         250        1 rows  Forum at Tucson A Mariott Senior Living Community
         240        9 rows  La Frontera Center Inc
         213        4 rows  Community Options Inc
         205        2 rows  Gap Ministries
         200        1 rows  Handmaker
         200        1 rows  Pima County One-Stop Career
         200        1 rows  Villa Hermosa
         200        1 rows  Home Instead
         199        1 rows  Tucson Jewish Community Center Inc
         190        1 rows  Encompass Health Rehabilitation Institute of Tucson
         190        2 rows  Desert Horizons Communities
         170        1 rows  Park Avenue Health & Rehab
         162        1 rows  Community Bridges

HQNAME by rows
       866  nan
         9  Goodwill Industries of Southern Arizona, Inc
         7  Arizona Mentor
         7  YMCA of the USA
         6  Learning Care Group Inc
         5  Boys & Girls Clubs of America
         5  ATI Physical Therapy, Inc
         5  Easterseals Blake Foundation
         4  Danville Services-Arizona LLC
         4  The American National Red Cross
         3  Brookdale Senior Living Inc
         3  United Way Worldwide
         3  Lutheran Services in America
         3  KinderCare Learning Center LLC
         3  The American Legion Department of Arizona
         3  The Salvation Army Arizona
         2  Goodwill Industries International Inc
         2  Habitat For Humanity International
         2  Big Brothers Big Sisters of America
         2  Labor Systems

HQNAME by dollars
       15.3K      866 rows  nan
         417        7 rows  YMCA of the USA
         275        2 rows  Goodwill Industries International Inc
         250        1 rows  AlerisLife, Inc
         200        1 rows  Senior Resource Group LLC
         200        1 rows  Home Instead, Inc
         190        1 rows  Encompass Health Corporation
         183        3 rows  United Way Worldwide
         170        1 rows  The Ensign Group, Inc
         158        5 rows  Easterseals Blake Foundation
         120        3 rows  Lutheran Services in America
         114        6 rows  Learning Care Group Inc
         108        2 rows  Atria Senior Living, Inc
         107        2 rows  US Parole Commission
         100        1 rows  Economic Security Department
          83        3 rows  Brookdale Senior Living Inc
          80        2 rows  Caring Senior Service
          65        1 rows  BrightStar Franchising, LLC
          64        9 rows  Goodwill Industries of Southern Arizona, Inc
          60        1 rows  Children's Learning Adventure USA LLC

STATE_NAME by rows
      1.0K  Arizona

STATE_NAME by dollars
       19.3K     1.0K rows  Arizona

NAICS by rows
       127  81331908
        87  62419012
        66  62441003
        58  62331206
        44  62441006
        36  62411004
        25  62419011
        25  62411006
        21  62431009
        21  62221001
        18  62161001
        16  61111007
        14  62399007
        14  81311008
        14  62431008
        12  62133003
        11  81331103
        11  81331904
        11  81391002
         9  54172006

NAICS by dollars
        2.3K       87 rows  62419012
        1.9K      127 rows  81331908
        1.4K       58 rows  62331206
         859       66 rows  62441003
         799       44 rows  62441006
         717       21 rows  62431009
         687        9 rows  54172006
         641       16 rows  61111007
         605       21 rows  62221001
         541       18 rows  62161001
         534       25 rows  62411006
         517        2 rows  92313004
         404        2 rows  62441004
         350        9 rows  45951040
         300        1 rows  33441902
         278       11 rows  81331103
         233       25 rows  62419011
         206        2 rows  62331204
         203        2 rows  62431002
         200        1 rows  62331103

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = EMPNUM
  ATI Physical Therapy                      2026:29
  American Red Cross                        2026:6
  Arizona Mentor                            2026:46
  Beacon Group                              2026:300
  Blake Foundation                          2026:618
  Boys & Girls Club of Tucson               2026:30
  Casa De Los Ninos                         2026:37
  Community Options Inc                     2026:213
  Danville Services                         2026:25
  Danville Services of AZ LLC               2026:30
  Developmental Disabilities                2026:500
  Devon Gables Health Care Center           2026:398
  Employment Security Appeals               2026:28
  Fairmount Assisted Living                 2026:45
  Forum at Tucson A Mariott Senior Living   2026:250
  Gap Ministries                            2026:205
  Goodwill                                  2026:36
  Goodwill Donation Center                  2026:28
  Goodwill Industries of Southern Arizona,  2026:275
  Habitat For Humanity                      2026:47
  Handmaker                                 2026:200
  Headstart                                 2026:400
  La Frontera Center Inc                    2026:240
  La Petite Academy                         2026:95
  Lutheran Social Service                   2026:120
  Pima County One-Stop Career               2026:200
  Pima Prevention Partnership               2026:51
  Ppep Inc                                  2026:508
  RISE Services Inc                         2026:7
  Sherwood Village Assisted Living & Memor  2026:65

HQNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = EMPNUM
  ATI Physical Therapy, Inc                 2026:29
  AlerisLife, Inc                           2026:250
  Arizona Mentor                            2026:46
  Atria Senior Living, Inc                  2026:108
  Big Brothers Big Sisters of America       2026:36
  Boys & Girls Clubs of America             2026:48
  BrightStar Franchising, LLC               2026:65
  Brookdale Senior Living Inc               2026:83
  Caring Senior Service                     2026:80
  Danville Services-Arizona LLC             2026:29
  Easterseals Blake Foundation              2026:158
  Economic Security Department              2026:100
  Encompass Health Corporation              2026:190
  Goodwill Industries International Inc     2026:275
  Goodwill Industries of Southern Arizona,  2026:64
  Habitat For Humanity International        2026:47
  Home Instead, Inc                         2026:200
  KinderCare Learning Center LLC            2026:49
  Labor Systems                             2026:4
  Learning Care Group Inc                   2026:114
  Lutheran Services in America              2026:120
  Senior Resource Group LLC                 2026:200
  The American Legion Department of Arizon  2026:12
  The American National Red Cross           2026:24
  The Ensign Group, Inc                     2026:170
  The Salvation Army Arizona                2026:30
  US Parole Commission                      2026:107
  United Way Worldwide                      2026:183
  YMCA of the USA                           2026:417
  nan                                       2026:15.3K

## what

CITY: Tucson 98%, South Tucson 1%, Pima 0%

ZIP: 85712 16%, 85711 14%, 85705 12%, 85719 11%, 85710 10%, 85716 10%, 85701 8%, 85745 4%, 85713 4%, 85715 4%, 85706 3%, 85718 3%

PLACETYPE: Independent 84%, Branch 15%, Headquarters 1%, Kiosk 0%

SQFOOTAGE: 2,500 - 4,999 24%, 1,500 - 2,499 21%, 5,000 - 9,999 13%, 1 - 1,499 13%, 10,000 - 19,999 8%, 20,000 - 39,999 8%, 40,000 - 99,999 7%, 100,000+ 4%, nan 3%

AFFILIATE: nan 97%, YMCA 1%, Boys & Girls Club 0%, United Way 0%, American Red Cross 0%, American Legion 0%, Habitat For Humanity 0%, VFW 0%, Eagles (FOE) 0%

PROFSPEC: nan 99%, Psychiatry 0%, Neurology,Psychiatry 0%, General Practice,Family Practi 0%, Pediatrics,Psychiatry 0%, Internal Medicine 0%, Estate Planning 0%, Certified Public Accounting 0%, Oncology,Surgery 0%, Obstetrics & Gynecology 0%

LOC_CONF: Very High 97%, High 3%, Low 0%, Medium 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.0K | 0 | 1024 6; 1023 6; 1022 6; 1021 6 |
| ESRI_PID | id | 1.0K | 0 | cb08f5b7c8c33863dc5f3c9a2 6; c857e4060de2671e3905e8d15 6; 267403833f01608363fc46968 6; ada6ce9a3777fea89d58f9322 6 |
| CONAME | who | 939 | 0 | Goodwill Donation Center 9; La Frontera Center Inc 9; La Petite Academy 8; Community Options Inc 7 |
| STREET | who | 329 | 0 | East Broadway Boulevard 78; East Speedway Boulevard 37; East Grant Road 33; East Fort Lowell Road 27 |
| CITY | category | 3 | 0 | Tucson 1.0K; South Tucson 15; Pima 1 |
| STATE | other | 1 | 0 | AZ 1.0K |
| STATE_NAME | who | 1 | 0 | Arizona 1.0K |
| ZIP | category | 25 | 0 | 85712 145; 85711 132; 85705 116; 85719 106 |
| ZIP4 | other | 780 | 0 | nan 37; 6106 9; 3119 8; 3558 7 |
| NAICS_ALL | other | 655 | 0 | 81331908 46; 62441003 43; 62331206 29; 62419012 28 |
| NAICS | who | 211 | 0 | 81331908 127; 62419012 87; 62441003 66; 62331206 58 |
| SIC_ALL | other | 665 | 0 | 839998 46; 835101 43; 836105 29; 832218 28 |
| SIC | who | 211 | 0 | 839998 127; 832218 87; 835101 66; 836105 58 |
| SALESVOL | amount | 226 | 0 | nan 475; 197000.0 39; 296000.0 29; 247000.0 28 |
| EMPNUM | amount | 81 | 0 | 4.0 122; 5.0 92; 2.0 83; 3.0 81 |
| PLACETYPE | category | 4 | 0 | Independent 863; Branch 154; Headquarters 6; Kiosk 1 |
| HQNAME | who | 91 | 0 | nan 866; Goodwill Industries of So 9; Arizona Mentor 7; YMCA of the USA 7 |
| SQFOOTAGE | category | 9 | 0 | 2,500 - 4,999 241; 1,500 - 2,499 215; 5,000 - 9,999 137; 1 - 1,499 130 |
| AFFILIATE | category | 9 | 0 | nan 998; YMCA 7; Boys & Girls Club 5; United Way 3 |
| BRAND | empty | 1 | 1.0K |  |
| PROFSPEC | category | 10 | 0 | nan 1.0K; Psychiatry 3; Neurology,Psychiatry 2; General Practice,Family P 1 |
| LOC_CONF | category | 4 | 0 | Very High 993; High 26; Low 4; Medium 1 |
| SOURCE | who | 1 | 0 | Data Axle 1.0K |
| GEOMETRY | other | 832 | 0 | {"type": "Point", "coordi 10; {"type": "Point", "coordi 8; {"type": "Point", "coordi 7; {"type": "Point", "coordi 7 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:30:05.35488 1.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 63cd5b2c-40d8-4c2d-be0c-0 1.0K |
| SRC_SHA256 | who | 1 | 0 | d2a10bd7035431f93b7c63c7c 1.0K |
