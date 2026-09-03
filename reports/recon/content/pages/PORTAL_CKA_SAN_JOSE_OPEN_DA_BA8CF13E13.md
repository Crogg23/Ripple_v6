# PORTAL_CKA_SAN_JOSE_OPEN_DA_BA8CF13E13

rows 67  columns 23  scan 4.8s

roles: amount 5, audit 2, category 10, date 1, other 4, who 2

## when

INGESTED_AT
  2026        67  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 67 | 6.14M | 6.15M | 6.18M | 6.18M | 412.36M |
| Y | 67 | 1.91M | 1.95M | 1.98M | 1.98M | 130.85M |
| INVERTELEV | 14 | -5.53 | 61 | 288.60 | 311.10 | 1.1K |
| FLOORELEV | 2 | 74.90 | 74.90 | 74.90 | 74.90 | 149.80 |
| RIMELEV | 10 | 15.92 | 103.78 | 301.14 | 315 | 1.1K |

## who

FACILITYID by rows
         1  90011
         1  42109
         1  81849
         1  72666
         1  90028
         1  42096
         1  37172
         1  28604
         1  41867
         1  1207
         1  75151
         1  42093
         1  90010
         1  90026
         1  36739
         1  71281
         1  42902
         1  28526
         1  41891
         1  41909

FACILITYID by dollars
       6.18M        1 rows  17932
       6.18M        1 rows  17471
       6.18M        1 rows  17872
       6.17M        1 rows  41840
       6.17M        1 rows  90024
       6.17M        1 rows  50130
       6.17M        1 rows  28318
       6.16M        1 rows  28600
       6.16M        1 rows  43527
       6.16M        1 rows  28594
       6.16M        1 rows  29273
       6.16M        1 rows  28604
       6.16M        1 rows  41909
       6.16M        1 rows  28526
       6.16M        1 rows  43842
       6.16M        1 rows  90020
       6.16M        1 rows  27700
       6.16M        1 rows  41867
       6.16M        1 rows  41869
       6.16M        1 rows  28492

SRC_SHA256 by rows
        67  210710de6dfb0ea0199a0bfc15105574f2252f48f4c645ad13adb71e77829263

SRC_SHA256 by dollars
     412.36M       67 rows  210710de6dfb0ea0199a0bfc15105574f2252f48f4c645ad13adb71e7782

## who x when

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  1207                                      2026:6.15M
  17471                                     2026:6.18M
  17872                                     2026:6.18M
  17932                                     2026:6.18M
  28318                                     2026:6.17M
  28526                                     2026:6.16M
  28594                                     2026:6.16M
  28600                                     2026:6.16M
  28604                                     2026:6.16M
  36739                                     2026:6.15M
  37172                                     2026:6.15M
  41840                                     2026:6.17M
  41867                                     2026:6.16M
  41891                                     2026:6.16M
  41909                                     2026:6.16M
  42093                                     2026:6.14M
  42096                                     2026:6.14M
  42109                                     2026:6.14M
  42902                                     2026:6.15M
  43527                                     2026:6.16M
  50130                                     2026:6.17M
  71281                                     2026:6.14M
  72666                                     2026:6.15M
  75151                                     2026:6.15M
  81849                                     2026:6.16M
  90010                                     2026:6.16M
  90011                                     2026:6.16M
  90024                                     2026:6.17M
  90026                                     2026:6.15M
  90028                                     2026:6.15M

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  210710de6dfb0ea0199a0bfc15105574f2252f48  2026:412.36M

## what

MATERIAL: RCP 76%, UNK 19%, ZZZ 1%, OTH 1%, VCP 1%

STRUCTTYPE: JC 93%, OC 4%, GS 1%, DP 1%

NAME: Zanker Soil Bed Filter 33%, Canoas Ferrous Chloride Inject 33%, Canoas Soil Bed Filter 33%

INSTALLYEAR: 2022 25%, 1995 12%, 1962 12%, 1994 12%, 1969 12%, 2019 12%, 1986 12%

SOURCEYEAR: MAGE 57%, ABPL 29%, APPL 14%

PLANCRT: UNK 86%, CPMS4880 5%, HD89012 3%, PP1096 2%, 3-10278C 2%, 3-05966 2%, 862074 2%

PLANMOD: CPMS6008 100%

NOTES: Precast Concrete Junction Box 15%, Repaired 4880-33(CPMS5804) in  15%, UIF: CPMS4880 8%, HD72257; HD103639; HD104392: C 8%, HD103639; HD104392: Rehabilita 8%, HD103639;  8%, HD95929: Added missing junctio 8%, CPMS10085: Remove Rungs & Reha 8%, 1175-36 8%, Not a manhole accesspoint. CIP 8%, Drop Connection 8%

PLANREF: HD104392 50%, CPMS5983 17%, HD95929 17%, CPMS10085 17%

CREATIONDATE: 1900/01/01 00:00:00+00 97%, 2025/01/27 22:39:54+00 1%, 2025/01/27 22:33:23+00 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 67 | 0 | 6163326.22987475 1; 6162202.48015374 1; 6154105.209931 1; 6154113.98025467 1 |
| Y | amount | 68 | 0 | 1941208.46009207 1; 1940624.37005289 1; 1956496.08010732 1; 1956480.93217173 1 |
| OBJECTID | other | 68 | 0 | 4079 1; 4078 1; 3278 1; 2877 1 |
| FACILITYID | who | 66 | 0 | 28604 1; 28526 1; 90028 1; 90027 1 |
| INTID | other | 66 | 0 | 1000321 1; 1000320 1; 90030 1; 90027 1 |
| INVERTELEV | amount | 14 | 53 | 87.39 2; 89.43 1; 39.64 1; 39.25 1 |
| MATERIAL | category | 5 | 0 | RCP 51; UNK 13; ZZZ 1; OTH 1 |
| STRUCTTYPE | category | 4 | 0 | JC 62; OC 3; GS 1; DP 1 |
| NAME | category | 4 | 64 | Zanker Soil Bed Filter 1; Canoas Ferrous Chloride I 1; Canoas Soil Bed Filter 1 |
| OWNEDBY | other | 1 | 0 | SJ 67 |
| INSTALLYEAR | category | 8 | 59 | 2022 2; 1995 1; 1962 1; 1994 1 |
| SOURCEYEAR | category | 4 | 53 | MAGE 8; ABPL 4; APPL 2 |
| PLANCRT | category | 8 | 3 | UNK 55; CPMS4880 3; HD89012 2; PP1096 1 |
| PLANMOD | category | 2 | 65 | CPMS6008 2 |
| LASTUPDATE | other | 58 | 0 | 2006/04/28 14:04:26+00 5; 2006/04/28 14:01:35+00 3; 2006/04/28 13:56:40+00 3; 2006/04/28 13:50:18+00 2 |
| NOTES | category | 12 | 54 | Precast Concrete Junction 2; Repaired 4880-33(CPMS5804 2; UIF: CPMS4880 1; HD72257; HD103639; HD1043 1 |
| FLOORELEV | amount | 2 | 65 | 74.9 2 |
| RIMELEV | amount | 10 | 57 | 104.49 2; 104.73 1; 103.07 1; 161 1 |
| PLANREF | category | 5 | 61 | HD104392 3; CPMS5983 1; HD95929 1; CPMS10085 1 |
| CREATIONDATE | category | 3 | 0 | 1900/01/01 00:00:00+00 65; 2025/01/27 22:39:54+00 1; 2025/01/27 22:33:23+00 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:13:13.42936 67 |
| SOURCE_RUN_ID | audit | 1 | 0 | acce3318-cbe2-416e-b4a4-9 67 |
| SRC_SHA256 | who | 1 | 0 | 210710de6dfb0ea0199a0bfc1 67 |
