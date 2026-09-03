# PORTAL_CKA_SAN_JOSE_OPEN_DA_4006091422

rows 8  columns 18  scan 2.9s

roles: amount 3, audit 2, category 11, date 1, empty 1, who 1

## when

INGESTED_AT
  2026         8  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCHOOLDISTAREA | 8 | 30.36 | 79.18 | 276.97 | 287.31 | 813.73 |
| SHAPE_LENGTH | 8 | 210.7K | 381.5K | 532.8K | 539.6K | 3.04M |
| SHAPE_AREA | 8 | 846.30M | 2.21B | 7.72B | 8.01B | 22.68B |

## who

SRC_SHA256 by rows
         8  4f680bc29b75018822da0d5c2c7236499b4bb897ee707c68e35980f41dbc0ce0

SRC_SHA256 by dollars
      813.73        8 rows  4f680bc29b75018822da0d5c2c7236499b4bb897ee707c68e35980f41dbc

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCHOOLDISTAREA
  4f680bc29b75018822da0d5c2c7236499b4bb897  2026:813.73

## what

OBJECTID: 166 12%, 165 12%, 164 12%, 163 12%, 148 12%, 147 12%, 146 12%, 145 12%

FACILITYID: 137 12%, 134 12%, 133 12%, 135 12%, 165 12%, 184 12%, 152 12%, 148 12%

INTID: 137 12%, 134 12%, 133 12%, 135 12%, 165 12%, 184 12%, 152 12%, 148 12%

SCHOOLDISTRICTID: 10 12%, 7 12%, 5 12%, 13 12%, 20 12%, 21 12%, 16 12%, 14 12%

SCHOOLDISTRICTNAME: Los Gatos-Saratoga Joint Union 12%, East Side Union High School Di 12%, Campbell Union High School Dis 12%, Fremont Union High School Dist 12%, San Jose Unified School Distri 12%, Santa Clara Unified School Dis 12%, Morgan Hill Unified School Dis 12%, Milpitas Unified School Distri 12%

DISTRICTTYPE: Secondary 50%, Unified 50%

AGENCYURL: www.lgsuhsd.org 12%, www.esuhsd.org 12%, www.cuhsd.org 12%, www.fuhsd.org 12%, www.sjusd.org 12%, www.santaclarausd.org 12%, www.mhusd.org 12%, www.musd.org 12%

PHONE: 408-354-2520 12%, 408-347-5000 12%, 408-371-0960 12%, 408-522-2200 12%, 408-535-6000 12%, 408-423-2000 12%, 408-201-6023 12%, 408-635-2600 12%

EMAIL: clinstrom@lgsuhsd.org 12%, funkc@esuhsd.org 12%, malaimo@cuhsd.org 12%, polly_bove@fuhsd.org 12%, nalbarran@sjusd.org 12%, skemp@scusd.net 12%, betandos@mhusd.org 12%, nrodriguez@musd.org 12%

LASTUPDATE: 2022/05/04 17:50:05+00 75%, 2022/05/04 17:49:58+00 12%, 2022/03/05 00:33:38+00 12%

ENTERPRISEID: PLN-SCHD-0000000137 12%, PLN-SCHD-0000000134 12%, PLN-SCHD-0000000133 12%, PLN-SCHD-0000000135 12%, PLN-SCHD-0000000165 12%, PLN-SCHD-0000000184 12%, PLN-SCHD-0000000152 12%, PLN-SCHD-0000000148 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 8 | 0 | 166 1; 165 1; 164 1; 163 1 |
| FACILITYID | category | 8 | 0 | 137 1; 134 1; 133 1; 135 1 |
| INTID | category | 8 | 0 | 137 1; 134 1; 133 1; 135 1 |
| SCHOOLDISTRICTID | category | 8 | 0 | 10 1; 7 1; 5 1; 13 1 |
| SCHOOLDISTRICTNAME | category | 8 | 0 | Los Gatos-Saratoga Joint  1; East Side Union High Scho 1; Campbell Union High Schoo 1; Fremont Union High School 1 |
| DISTRICTTYPE | category | 2 | 0 | Secondary 4; Unified 4 |
| SCHOOLDISTAREA | amount | 8 | 0 | 103.41 1; 139.65 1; 30.36 1; 54.95 1 |
| AGENCYURL | category | 8 | 0 | www.lgsuhsd.org 1; www.esuhsd.org 1; www.cuhsd.org 1; www.fuhsd.org 1 |
| PHONE | category | 8 | 0 | 408-354-2520 1; 408-347-5000 1; 408-371-0960 1; 408-522-2200 1 |
| EMAIL | category | 8 | 0 | clinstrom@lgsuhsd.org 1; funkc@esuhsd.org 1; malaimo@cuhsd.org 1; polly_bove@fuhsd.org 1 |
| LASTUPDATE | category | 3 | 0 | 2022/05/04 17:50:05+00 6; 2022/05/04 17:49:58+00 1; 2022/03/05 00:33:38+00 1 |
| NOTES | empty | 1 | 8 |  |
| ENTERPRISEID | category | 8 | 0 | PLN-SCHD-0000000137 1; PLN-SCHD-0000000134 1; PLN-SCHD-0000000133 1; PLN-SCHD-0000000135 1 |
| SHAPE_LENGTH | amount | 8 | 0 | 431839.39116596 1; 441837.25926786 1; 210708.561249346 1; 362362.736004989 1 |
| SHAPE_AREA | amount | 8 | 0 | 2882336423.16376 1; 3892846794.83456 1; 846304990.687328 1; 1531409524.30296 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:11:53.07971 8 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2955e968-1241-4f75-b019-e 8 |
| SRC_SHA256 | who | 1 | 0 | 4f680bc29b75018822da0d5c2 8 |
