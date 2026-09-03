# PORTAL_SOC_CHICAGO_DATA_POR_1719DAE821

rows 2.0K  columns 29  scan 5.5s

roles: amount 3, audit 2, category 7, date 2, other 9, who 7

## when

VIOLATION_DATE
  2023       100  ####
  2024       828  ##############################
  2025       792  #############################
  2026       280  ##########

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 2.0K | 41.66 | 41.90 | 42 | 42.02 | 83.8K |
| LONGITUDE | 2.0K | -87.84 | -87.68 | -87.55 | -87.53 | -175.4K |
| FINE_AMOUNT | 1.8K | 0 | 750 | 10.0K | 30.0K | 2.19M |

## who

STREET_NAME by rows
        79  GRAND
        79  ASHLAND
        67  WESTERN
        42  ARCHER
        40  BELMONT
        36  PULASKI
        32  CICERO
        30  DAMEN
        28  CALIFORNIA
        27  HALSTED
        26  DIVISION
        23  ROOSEVELT
        22  CERMAK
        22  LAWRENCE
        21  KEDZIE
        21  NORTH
        20  MILWAUKEE
        20  PAULINA
        20  OGDEN
        19  IRVING PARK

STREET_NAME by dollars
      122.3K       79 rows  GRAND
       88.2K       67 rows  WESTERN
       74.0K       11 rows  STATE
       64.4K       79 rows  ASHLAND
       61.0K        7 rows  INDIANA
       42.5K       42 rows  ARCHER
       40.0K       11 rows  66TH
       38.2K       12 rows  ELSTON
       30.8K       20 rows  OGDEN
       30.4K       36 rows  PULASKI
       30.0K        3 rows  21ST
       29.0K        8 rows  KENMORE
       28.1K       40 rows  BELMONT
       27.8K       14 rows  LINCOLN
       27.0K       26 rows  DIVISION
       26.0K        9 rows  ONTARIO
       25.4K       27 rows  HALSTED
       25.1K       32 rows  CICERO
       22.5K       19 rows  IRVING PARK
       22.4K       28 rows  CALIFORNIA

RESPONDENT by rows
        30  EZMB LLC
        21  BUILDER LUXURY INC
        17  Speedway, LLC
        15  Reekop Corp.
        14  Gas N Go, Inc.
        12  Bachula Development, Inc.
        12  CARLOS GROUP INC
        12  PRECISION EXCAVATION LLC
        11  Renaissance Properties-IL, LLC
        11  Siddiqui, Khalid
        10  HPG Holding, Inc.
        10  AZ SPE, LLC
        10  7-Eleven, Inc.
         9  MAT Asphalt, LLC.
         9  LONGFORD CONSTRUCTION INC.
         8  3820 S. Archer Corp.
         8  * ALL CONCRETE CONTRACTORS INC
         8  2525 W Taylor LLC
         8  MODERN MASONRY LLC
         8  Vivify Construction, LLC

RESPONDENT by dollars
       60.5K       15 rows  Reekop Corp.
       60.0K        6 rows  CHATHAM HOUSING PORTFOLIO 91 LLC
       40.0K       11 rows  Renaissance Properties-IL, LLC
       35.0K        2 rows  S.E. State Street Chicago LLC
       35.0K        2 rows  ALLEN, HARVEY
       30.0K        1 rows  Midtown Athletic Club Chicago
       30.0K        3 rows  TRIPLETT, CHRISTOPHER
       22.0K        8 rows  2525 W Taylor LLC
       21.0K        4 rows  JONES DRILLING, LLC
       20.0K        2 rows  4040 Ogden LLC 4040 Ogden LLC
       18.0K        4 rows  COMMONWEALTH EDISON COMPANY
       17.3K       12 rows  PRECISION EXCAVATION LLC
       16.6K       12 rows  CARLOS GROUP INC
       16.5K        4 rows  JSL Building Restoration Group Inc.
       16.0K        3 rows  MIDWEST PRESSURE WASHING AND RESTORATION INC
       15.2K        4 rows  SHORTY RELL AUTO LLC
       15.0K        2 rows  GREEN ERA 83RD STREET LLC
       15.0K        6 rows  B & K  Concrete 1 Inc.
       15.0K        4 rows  J.GILL & CO. MASONRY
       14.8K       30 rows  EZMB LLC

LOCATION by rows
        16  {"type": "Point", "coordinates": [-87.54990714092, 41.702655500159]}
        15  {"type": "Point", "coordinates": [-87.694027653206, 41.893399135959]}
        14  {"type": "Point", "coordinates": [-87.666979759294, 41.890867764994]}
        12  {"type": "Point", "coordinates": [-87.668516238401, 41.858037820234]}
        11  {"type": "Point", "coordinates": [-87.587464002435, 41.774350568144]}
        10  {"type": "Point", "coordinates": [-87.694952467868, 41.830402822602]}
        10  {"type": "Point", "coordinates": [-87.677022207376, 41.822972765727]}
         9  {"type": "Point", "coordinates": [-87.721829523349, 41.742285829664]}
         9  {"type": "Point", "coordinates": [-87.716513742832, 41.913715390359]}
         9  {"type": "Point", "coordinates": [-87.698772968018, 41.828299038872]}
         8  {"type": "Point", "coordinates": [-87.646036776674, 41.912141069499]}
         8  {"type": "Point", "coordinates": [-87.688674523894, 41.869200486233]}
         8  {"type": "Point", "coordinates": [-87.700850731312, 41.954612444082]}
         8  {"type": "Point", "coordinates": [-87.663396255502, 41.954077915128]}
         8  {"type": "Point", "coordinates": [-87.625362024568, 41.893426146708]}
         8  {"type": "Point", "coordinates": [-87.688135035871, 41.824112853701]}
         8  {"type": "Point", "coordinates": [-87.666340663907, 41.870386161123]}
         8  {"type": "Point", "coordinates": [-87.75412735364, 41.967837901096]}
         7  {"type": "Point", "coordinates": [-87.731032251518, 41.848745776337]}
         7  {"type": "Point", "coordinates": [-87.709327105003, 41.899500583242]}

LOCATION by dollars
       60.5K       15 rows  {"type": "Point", "coordinates": [-87.694027653206, 41.89339
       60.0K        6 rows  {"type": "Point", "coordinates": [-87.620443437835, 41.77279
       40.0K       11 rows  {"type": "Point", "coordinates": [-87.587464002435, 41.77435
       35.0K        2 rows  {"type": "Point", "coordinates": [-87.625276997877, 41.78397
       35.0K        2 rows  {"type": "Point", "coordinates": [-87.625280001564, 41.78408
       30.0K        3 rows  {"type": "Point", "coordinates": [-87.675989908287, 41.85298
       30.0K        1 rows  {"type": "Point", "coordinates": [-87.678439541114, 41.92572
       22.0K        8 rows  {"type": "Point", "coordinates": [-87.688674523894, 41.86920
       21.0K        8 rows  {"type": "Point", "coordinates": [-87.625362024568, 41.89342
       20.0K        2 rows  {"type": "Point", "coordinates": [-87.726240494513, 41.85068
       18.0K        4 rows  {"type": "Point", "coordinates": [-87.68712340928, 41.901090
       16.0K        3 rows  {"type": "Point", "coordinates": [-87.656749646096, 41.98336
       15.2K        4 rows  {"type": "Point", "coordinates": [-87.742733711349, 41.88527
       15.0K        4 rows  {"type": "Point", "coordinates": [-87.647173638458, 41.88303
       15.0K        2 rows  {"type": "Point", "coordinates": [-87.640764981413, 41.74354
       14.9K        6 rows  {"type": "Point", "coordinates": [-87.647423583714, 41.90353
       14.5K        9 rows  {"type": "Point", "coordinates": [-87.698772968018, 41.82829
       13.5K        4 rows  {"type": "Point", "coordinates": [-87.686777991004, 41.84645
       13.0K        9 rows  {"type": "Point", "coordinates": [-87.716513742832, 41.91371
       12.0K        2 rows  {"type": "Point", "coordinates": [-87.683479190448, 41.79969

CASE_TYPE by rows
      2.0K  Administration Hearing

CASE_TYPE by dollars
       2.19M     2.0K rows  Administration Hearing

## who x when

STREET_NAME by VIOLATION_DATE, dollars = FINE_AMOUNT
  21ST                                      2025:30.0K
  66TH                                      2024:40.0K
  ARCHER                                    2023:3.2K 2024:24.1K 2025:13.2K 2026:2.0K
  ASHLAND                                   2023:5.5K 2024:25.5K 2025:30.8K 2026:2.6K
  BELMONT                                   2024:16.4K 2025:10.0K 2026:1.7K
  CALIFORNIA                                2023:2.2K 2024:9.2K 2025:9.5K 2026:1.5K
  CERMAK                                    2023:750 2024:8.8K 2025:4.8K 2026:2.2K
  CICERO                                    2023:2 2024:14.9K 2025:8.4K 2026:1.7K
  DAMEN                                     2024:9.5K 2025:5.5K 2026:2.2K
  DIVISION                                  2024:10.2K 2025:16.8K 2026:0
  ELSTON                                    2024:3.5K 2025:34.8K 2026:1
  GRAND                                     2023:6.0K 2024:28.1K 2025:86.8K 2026:1.5K
  HALSTED                                   2023:750 2024:15.2K 2025:7.2K 2026:2.2K
  INDIANA                                   2024:61.0K
  IRVING PARK                               2024:9.2K 2025:12.5K 2026:750
  KEDZIE                                    2024:17.5K 2025:1.5K 2026:1.0K
  KENMORE                                   2024:3.0K 2025:26.0K
  LAWRENCE                                  2024:4.2K 2025:5.8K 2026:1.5K
  LINCOLN                                   2024:3.5K 2025:24.3K
  MILWAUKEE                                 2024:14.4K 2025:6.0K 2026:2
  NORTH                                     2024:13.6K 2025:3.4K 2026:1.0K
  OGDEN                                     2023:1.0K 2024:6.0K 2025:22.8K 2026:1.0K
  ONTARIO                                   2024:26.0K 2026:0
  PAULINA                                   2024:5.0K 2025:9.3K 2026:850
  PULASKI                                   2023:10.0K 2024:12.1K 2025:3.9K 2026:4.5K
  ROOSEVELT                                 2023:1.5K 2024:4.6K 2025:7.3K 2026:400
  STATE                                     2024:4.0K 2025:70.0K
  WESTERN                                   2023:1.5K 2024:25.7K 2025:61.0K 2026:5

RESPONDENT by VIOLATION_DATE, dollars = FINE_AMOUNT
  * ALL CONCRETE CONTRACTORS INC            2024:9.6K 2025:3.0K
  2525 W Taylor LLC                         2024:22.0K
  3820 S. Archer Corp.                      2023:1.5K 2024:4.0K 2025:750
  4040 Ogden LLC 4040 Ogden LLC             2025:20.0K
  7-Eleven, Inc.                            2024:4.8K 2025:2.0K 2026:1.5K
  ALLEN, HARVEY                             2025:35.0K
  AZ SPE, LLC                               2024:2.5K 2025:3.0K
  BUILDER LUXURY INC                        2024:2.2K 2025:0 2026:7.7K
  Bachula Development, Inc.                 2023:2.0K 2024:9.0K
  CARLOS GROUP INC                          2024:8.3K 2025:8.2K 2026:0
  CHATHAM HOUSING PORTFOLIO 91 LLC          2024:60.0K
  COMMONWEALTH EDISON COMPANY               2025:18.0K
  EZMB LLC                                  2023:3.8K 2024:10.2K 2025:800
  Gas N Go, Inc.                            2024:4.0K 2025:5.0K 2026:0
  HPG Holding, Inc.                         2024:3.8K 2025:2.8K
  JONES DRILLING, LLC                       2024:21.0K
  JSL Building Restoration Group Inc.       2024:16.5K
  LONGFORD CONSTRUCTION INC.                2024:2.2K 2026:0
  MAT Asphalt, LLC.                         2023:1.0K 2024:5.1K 2025:4.0K
  MIDWEST PRESSURE WASHING AND RESTORATION  2025:16.0K
  MODERN MASONRY LLC                        2026:0
  Midtown Athletic Club Chicago             2025:30.0K
  PRECISION EXCAVATION LLC                  2025:16.4K 2026:840
  Reekop Corp.                              2025:60.5K
  Renaissance Properties-IL, LLC            2024:40.0K
  S.E. State Street Chicago LLC             2025:35.0K
  Siddiqui, Khalid                          2024:5.0K 2025:6.0K
  Speedway, LLC                             2024:4.8K 2025:6.3K 2026:750
  TRIPLETT, CHRISTOPHER                     2025:30.0K
  Vivify Construction, LLC                  2024:4.5K

## what

DIRECTION: W 42%, N 33%, S 21%, E 5%

STREET_TYPE: AVE 60%, ST 27%, RD 6%, BLVD 2%, PL 2%, nan 1%, HWY 0%, DR 0%, PKWY 0%, CT 0%, TER 0%

CASE_STATUS: Closed 85%, Open 15%

COMMENT: INSPECTOR:417325; 28%, INSPECTOR:417337; 15%, INSPECTOR:249349; 12%, INSPECTOR:437489; 9%, INSPECTOR:443615; 8%, INSPECTOR:3308; 7%, INSPECTOR:451826; 6%, INSPECTOR:379542; 5%, INSPECTOR:431068; 4%, INSPECTOR:10937; 4%, INSPECTOR:13776; 2%, INSPECTOR:425726; 1%

COMPUTED_REGION_43WA_7QMU: 41 12%, 18 12%, 40 12%, 46 9%, 11 9%, 23 9%, 1 8%, 26 8%, 49 7%, 20 5%, 47 5%, 45 5%

DISPOSITION: LIABPLEA 49%, DEFAULT 15%, nan 14%, NONSUIT 11%, LIABLE 7%, LIABCONT 2%, NOTLIAB 1%

STREET_NUMBER_TO: nan 100%, 5107 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CASE_NUMBER | other | 1.2K | 0 | ENVCTY29376 13; ENVCTY29062 13; ENVCTY29431 13; ENVCTY28306 12 |
| ADDRESS | who | 893 | 0 | 2666 W GRAND AVE 18; 3033 E 106TH ST 16; 1534 E 66TH PL 16; 2501 W TAYLOR ST 15 |
| STREET_NUMBER_FROM | other | 795 | 0 | 1533 18; 2666 17; 4243 16; 3033 16 |
| DIRECTION | category | 4 | 0 | W 838; N 651; S 415; E 96 |
| STREET_NAME | who | 323 | 0 | ASHLAND 79; GRAND 79; WESTERN 67; ARCHER 42 |
| STREET_TYPE | category | 11 | 0 | AVE 1.2K; ST 542; RD 127; BLVD 40 |
| TICKET_NO | other | 981 | 0 | nan 591; E000040299 8; E000039753 8; E000039660 8 |
| RESPONDENT | who | 899 | 0 | EZMB LLC 32; BUILDER LUXURY INC 21; Bachula Development, Inc. 17; Speedway, LLC 17 |
| CASE_TYPE | who | 1 | 0 | Administration Hearing 2.0K |
| VIOLATION_DATE | date | 504 | 0 | 2024-02-16T00:00:00.000 21; 2024-02-09T00:00:00.000 20; 2023-12-11T00:00:00.000 19; 2023-11-08T00:00:00.000 17 |
| CODE_VIOLATION | other | 99 | 0 | 11-4-765(2)(b) Full Descr 232; 11-4-765(2)(c) Full Descr 220; 4-108-350(A)(2) Full Desc 182; 4-108-355(B) Full Descrip 130 |
| CASE_STATUS | category | 2 | 0 | Closed 1.7K; Open 297 |
| COMMENT | category | 46 | 0 | INSPECTOR:417325; 535; INSPECTOR:417337; 288; INSPECTOR:249349; 228; INSPECTOR:437489; 164 |
| DATA_SOURCE | who | 1 | 0 | DEPT. OF PUBLIC HEALTH 2.0K |
| LATITUDE | amount | 904 | 0 | 41.893399135959164 18; 41.70265550015945 16; 41.7743505681442 16; 41.86920048623289 15 |
| LONGITUDE | amount | 889 | 0 | -87.69402765320562 18; -87.5499071409203 16; -87.58746400243531 16; -87.68867452389381 15 |
| LOCATION | who | 879 | 0 | {"type": "Point", "coordi 18; {"type": "Point", "coordi 16; {"type": "Point", "coordi 16; {"type": "Point", "coordi 15 |
| COMPUTED_REGION_VRXF_VC4K | other | 71 | 0 | 25 210; 23 114; 46 98; 29 98 |
| COMPUTED_REGION_6MKV_F3DW | other | 54 | 0 | 21538 156; 22535 128; 14920 116; 21184 114 |
| COMPUTED_REGION_BDYS_3D7I | other | 424 | 0 | 174 30; 545 25; 37 20; 485 20 |
| COMPUTED_REGION_43WA_7QMU | category | 49 | 0 | 41 133; 18 124; 40 123; 46 94 |
| COMPUTED_REGION_RPCA_8UM6 | other | 55 | 0 | 39 148; 1 125; 28 118; 43 106 |
| FINE_AMOUNT | amount | 45 | 0 | 1000 419; 750 372; 0 366; nan 168 |
| DOCKET_NO | other | 995 | 0 | nan 279; 24DE000086 12; 24DE000080 11; 24DE000014 11 |
| DISPOSITION | category | 7 | 0 | LIABPLEA 986; DEFAULT 302; nan 289; NONSUIT 220 |
| STREET_NUMBER_TO | category | 2 | 0 | nan 2.0K; 5107 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:07:56.22413 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 33fe734e-ee4f-4a42-ade6-6 2.0K |
| SRC_SHA256 | who | 1 | 0 | 9b8e90fadcb47bb62793e218d 2.0K |
