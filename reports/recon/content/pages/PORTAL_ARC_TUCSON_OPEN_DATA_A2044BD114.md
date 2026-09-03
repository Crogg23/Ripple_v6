# PORTAL_ARC_TUCSON_OPEN_DATA_A2044BD114

rows 1.9K  columns 27  scan 5.0s

roles: amount 2, audit 2, category 7, date 1, id 2, other 3, who 11

## when

INGESTED_AT
  2026      1.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SALESVOL | 1.6K | 34.0K | 1.00M | 18.95M | 66.55M | 3.50B |
| EMPNUM | 1.8K | 1 | 7 | 200 | 3.2K | 37.5K |

## who

CONAME by rows
        25  Walgreens
        16  CVS Pharmacy
        12  Walmart Pharmacy
        12  Fry's Food Pharmacy
         8  Safeway Pharmacy
         8  Sonora Quest Laboratories
         7  Genoa Healthcare LLC
         7  Arizona Community Physicians
         7  La Frontera Center Inc
         6  Carbon Health Primary Care of Florida PA
         6  Athletico Physical Therapy
         6  Nationwide Vision
         6  ATI Physical Therapy
         5  GNC
         5  Carondelet Medical Group
         5  Hanger Clinic
         5  Lab Corp
         5  NextCare Urgent Care
         5  MinuteClinic
         4  University Medical Center

CONAME by dollars
        3.2K        1 rows  Banner-University Medical Center Tucson
        3.0K        1 rows  TMC HealthCare
        1.4K        1 rows  Carondelet St Joseph's Hospital
        1.2K        1 rows  Carondalet St Mary's Hospital
         784        1 rows  Banner-University Medical Center South
         750        1 rows  El Rio Foundation Inc
         542       25 rows  Walgreens
         400        1 rows  Radiology Ltd
         398        1 rows  Devon Gables Health Care Center
         285        1 rows  Tabula Rasa Healthcare, Inc
         279        1 rows  Tucson Orthopaedic Institute
         250        1 rows  Forum at Tucson A Mariott Senior Living Community
         211        3 rows  Southern Arizona Urgent Care
         210        3 rows  El Rio Community Health Center
         209        7 rows  La Frontera Center Inc
         201       12 rows  Fry's Food Pharmacy
         200        1 rows  Sapphire of Tucson
         200        1 rows  Pima Medical Institute-Online
         200        1 rows  Banner-University Medical Center Tucson Cafeteria
         200        1 rows  Sam's Club

HQNAME by rows
      1.5K  nan
        25  Walgreens Boots Alliance, Inc
        17  CVS Pharmacy, Inc
        13  Fry's Food Stores
        12  Walmart U.S. Division
        10  Banner Health
        10  Carondelet Health Network
         9  Sonora Quest Laboratories
         9  Genoa Healthcare, LLC
         9  Carondelet Medical Group
         8  Safeway Inc
         7  DaVita Inc
         7  Carbon Health
         6  Nationwide Vision Center, Inc
         6  Athletico Physical Therapy
         6  ATI Physical Therapy, Inc
         5  Hanger Prosthetics & Orthotics Inc
         5  Laboratory Corporation of America
         5  Next Care Urgent Care
         5  MinuteClinic LLC

HQNAME by dollars
       23.0K     1.5K rows  nan
        4.1K       10 rows  Banner Health
        2.7K        3 rows  Tenet Healthcare Corporation
         542       25 rows  Walgreens Boots Alliance, Inc
         285        1 rows  Tabula Rasa HealthCare, Inc
         256        5 rows  University Of Arizona
         252       10 rows  Carondelet Health Network
         250        1 rows  AlerisLife, Inc
         230        2 rows  Encompass Health Corporation
         219        9 rows  Carondelet Medical Group
         215       13 rows  Fry's Food Stores
         211        3 rows  Sam's Club Division
         200        1 rows  Home Instead, Inc
         200        2 rows  Costco Wholesale Corporation
         200        1 rows  Senior Resource Group LLC
         199        1 rows  UHS of Delaware Inc
         194        7 rows  DaVita Inc
         188       17 rows  CVS Pharmacy, Inc
         170        1 rows  The Ensign Group, Inc
         140        1 rows  YMCA of the USA

STATE_NAME by rows
      1.9K  Arizona

STATE_NAME by dollars
       37.5K     1.9K rows  Arizona

SIC_ALL by rows
       209  801101
       142  802101
        69  809907
        56  801104
        40  804101
        38  808201
        37  801104,801101
        29  591205,801132
        29  804918
        25  805908
        25  804913
        22  806201
        21  806301
        20  591205,533101,549904,591202,591203,594710,599992,738401,801132
        18  809921
        17  801101,801104
        17  804201
        13  807101
        12  591205,533101,549904,591202,591203,594710,599992,738401,801132,804939
        12  591205,549904,801132

SIC_ALL by dollars
        3.2K        1 rows  806202,806201,806203,999966
        3.0K        1 rows  806202,805101,806203
        2.1K      209 rows  801101
        1.4K        1 rows  806202,806203,806301
        1.3K        2 rows  806202,806203
        1.1K      142 rows  802101
         784        2 rows  806202,806201,806203
         750        1 rows  801104,723119,801101,802101,873303
         670       56 rows  801104
         530       29 rows  591205,801132
         521       37 rows  801104,801101
         447       20 rows  591205,533101,549904,591202,591203,594710,599992,738401,8011
         423       69 rows  809907
         400        1 rows  801101,807129,999966
         398        1 rows  836105,805101,805902,805904,809907,999966
         394       17 rows  801101,801104
         387       38 rows  808201
         386       25 rows  805908
         374        6 rows  809907,999966
         322       22 rows  806201

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = EMPNUM
  ATI Physical Therapy                      2026:31
  Arizona Community Physicians              2026:119
  Athletico Physical Therapy                2026:32
  Banner-University Medical Center South    2026:784
  Banner-University Medical Center Tucson   2026:3.2K
  CVS Pharmacy                              2026:163
  Carbon Health Primary Care of Florida PA  2026:47
  Carondalet St Mary's Hospital             2026:1.2K
  Carondelet Medical Group                  2026:106
  Carondelet St Joseph's Hospital           2026:1.4K
  Devon Gables Health Care Center           2026:398
  El Rio Foundation Inc                     2026:750
  Fry's Food Pharmacy                       2026:201
  GNC                                       2026:15
  Genoa Healthcare LLC                      2026:90
  Hanger Clinic                             2026:26
  La Frontera Center Inc                    2026:209
  Lab Corp                                  2026:16
  MinuteClinic                              2026:40
  Nationwide Vision                         2026:37
  NextCare Urgent Care                      2026:64
  Radiology Ltd                             2026:400
  Safeway Pharmacy                          2026:83
  Sonora Quest Laboratories                 2026:38
  TMC HealthCare                            2026:3.0K
  Tabula Rasa Healthcare, Inc               2026:285
  Tucson Orthopaedic Institute              2026:279
  University Medical Center                 2026:65
  Walgreens                                 2026:542
  Walmart Pharmacy                          2026:106

HQNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = EMPNUM
  ATI Physical Therapy, Inc                 2026:31
  AlerisLife, Inc                           2026:250
  Athletico Physical Therapy                2026:32
  Banner Health                             2026:4.1K
  CVS Pharmacy, Inc                         2026:188
  Carbon Health                             2026:52
  Carondelet Health Network                 2026:252
  Carondelet Medical Group                  2026:219
  Costco Wholesale Corporation              2026:200
  DaVita Inc                                2026:194
  Encompass Health Corporation              2026:230
  Fry's Food Stores                         2026:215
  Genoa Healthcare, LLC                     2026:103
  Hanger Prosthetics & Orthotics Inc        2026:26
  Home Instead, Inc                         2026:200
  Laboratory Corporation of America         2026:16
  MinuteClinic LLC                          2026:40
  Nationwide Vision Center, Inc             2026:37
  Next Care Urgent Care                     2026:64
  Safeway Inc                               2026:83
  Sam's Club Division                       2026:211
  Senior Resource Group LLC                 2026:200
  Sonora Quest Laboratories                 2026:43
  Tabula Rasa HealthCare, Inc               2026:285
  Tenet Healthcare Corporation              2026:2.7K
  UHS of Delaware Inc                       2026:199
  University Of Arizona                     2026:256
  Walgreens Boots Alliance, Inc             2026:542
  Walmart U.S. Division                     2026:106
  nan                                       2026:23.0K

## what

CITY: Tucson 99%, South Tucson 1%, Davis Monthan Afb 0%, Tucscon 0%

ZIP: 85712 26%, 85711 13%, 85710 11%, 85719 9%, 85716 7%, 85715 7%, 85705 7%, 85745 7%, 85713 3%, 85714 3%, 85747 3%, 85718 3%

PLACETYPE: Independent 80%, Branch 19%, Headquarters 1%

SQFOOTAGE: 2,500 - 4,999 21%, 1 - 1,499 14%, 1,500 - 2,499 14%, 5,000 - 9,999 14%, 10,000 - 19,999 11%, 40,000 - 99,999 7%, nan 7%, 20,000 - 39,999 7%, 100,000+ 4%

AFFILIATE: nan 100%, American Red Cross 0%, YMCA 0%, Health Mart Pharmacy 0%, Vision Source 0%

BRAND: nan 100%, Blue Cross-Blue Shield,Cigna,P 0%, Nationwide Ins Co 0%

LOC_CONF: Very High 98%, High 2%, Low 0%, Medium 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.8K | 0 | 1889 10; 1888 10; 1887 10; 1886 10 |
| ESRI_PID | id | 1.9K | 0 | 28671fc2739fa2924302a0030 10; c857e4060de2671e3905e8d15 10; 78a95a24855af12a55051c50a 10; 89356b27ec37f2f86422e4f61 10 |
| CONAME | who | 1.7K | 0 | Walgreens 25; CVS Pharmacy 16; Carbon Health Primary Car 14; Walmart Pharmacy 13 |
| STREET | who | 253 | 0 | East Broadway Boulevard 122; East Grant Road 115; North Campbell Avenue 86; North Wilmot Road 81 |
| CITY | category | 4 | 0 | Tucson 1.9K; South Tucson 13; Davis Monthan Afb 4; Tucscon 1 |
| STATE | other | 1 | 0 | AZ 1.9K |
| STATE_NAME | who | 1 | 0 | Arizona 1.9K |
| ZIP | category | 28 | 0 | 85712 431; 85711 213; 85710 182; 85719 154 |
| ZIP4 | other | 1.1K | 0 | nan 50; 0001 17; 2119 16; 1256 15 |
| NAICS_ALL | who | 787 | 0 | 62111107 209; 62121003 142; 62199921 69; 62149301 56 |
| NAICS | who | 207 | 0 | 62111107 318; 62121003 192; 62149301 189; 62199921 102 |
| SIC_ALL | who | 805 | 0 | 801101 209; 802101 142; 809907 69; 801104 56 |
| SIC | who | 209 | 0 | 801101 318; 802101 192; 801104 189; 809907 102 |
| SALESVOL | amount | 403 | 0 | nan 257; 1500000.0 84; 1737000.0 76; 938000.0 68 |
| EMPNUM | amount | 91 | 0 | 5.0 229; 4.0 160; 6.0 160; 8.0 144 |
| PLACETYPE | category | 3 | 0 | Independent 1.5K; Branch 367; Headquarters 16 |
| HQNAME | who | 154 | 0 | nan 1.5K; Walgreens Boots Alliance, 25; CVS Pharmacy, Inc 17; Fry's Food Stores 13 |
| SQFOOTAGE | category | 9 | 0 | 2,500 - 4,999 398; 1 - 1,499 271; 1,500 - 2,499 265; 5,000 - 9,999 262 |
| AFFILIATE | category | 5 | 0 | nan 1.9K; American Red Cross 2; YMCA 1; Health Mart Pharmacy 1 |
| BRAND | category | 3 | 0 | nan 1.9K; Blue Cross-Blue Shield,Ci 1; Nationwide Ins Co 1 |
| PROFSPEC | who | 183 | 0 | nan 1.4K; General Dentistry 94; Internal Medicine 17; Pediatrics 16 |
| LOC_CONF | category | 4 | 0 | Very High 1.8K; High 30; Low 7; Medium 5 |
| SOURCE | who | 1 | 0 | Data Axle 1.9K |
| GEOMETRY | other | 1.1K | 0 | {"type": "Point", "coordi 18; {"type": "Point", "coordi 17; {"type": "Point", "coordi 16; {"type": "Point", "coordi 15 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:31:32.30419 1.9K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4ba583b0-5f96-4a51-872f-7 1.9K |
| SRC_SHA256 | who | 1 | 0 | e56bfdc51cb1e2dcc9f75041a 1.9K |
