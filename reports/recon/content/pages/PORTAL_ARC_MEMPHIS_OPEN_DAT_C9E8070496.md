# PORTAL_ARC_MEMPHIS_OPEN_DAT_C9E8070496

rows 1.0K  columns 23  scan 3.5s

roles: amount 4, audit 2, category 6, date 3, id 4, other 3, who 2

## when

CREATED_DA
  2020         8  #################
  2021        11  ########################
  2022        14  ##############################
  2023        12  ##########################
  2024         3  ######
  2025        14  ##############################

LAST_EDI_1
  2021        10  
  2023      1.0K  ##############################
  2024         2  
  2025        16  

INGESTED_AT
  2026      1.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_STAR | 1.0K | 3.0K | 179.5K | 14.94M | 235.79M | 1.38B |
| SHAPE_STLE | 1.0K | 221.30 | 2.0K | 25.9K | 262.3K | 3.82M |
| SHAPE__AREA | 1.0K | 3.0K | 179.5K | 14.94M | 235.79M | 1.38B |
| SHAPE__LENGTH | 1.0K | 221.30 | 2.0K | 25.9K | 262.3K | 3.82M |

## who

RULINGDATE by rows
       375  nan
         7  1012867200000.0
         7  1196640000000.0
         6  632448000000.0
         6  1083628800000.0
         5  872467200000.0
         5  931737600000.0
         5  633052800000.0
         5  712281600000.0
         5  833846400000.0
         5  734659200000.0
         5  626400000000.0
         5  839289600000.0
         4  1136246400000.0
         4  1070323200000.0
         4  590112000000.0
         4  844128000000.0
         4  697766400000.0
         4  627609600000.0
         4  749174400000.0

RULINGDATE by dollars
     406.64M      375 rows  nan
     237.70M        3 rows  597974400000.0
     170.57M        3 rows  1631145600000.0
      41.23M        1 rows  1162857600000.0
      22.73M        1 rows  735264000000.0
      15.38M        1 rows  967420800000.0
      15.26M        2 rows  824774400000.0
      12.62M        5 rows  633052800000.0
      11.02M        1 rows  610675200000.0
      10.45M        1 rows  775872000000.0
       9.21M        3 rows  937872000000.0
       9.00M        2 rows  1589414400000.0
       8.50M        1 rows  1206662400000.0
       8.17M        1 rows  1120953600000.0
       7.76M        2 rows  756432000000.0
       7.11M        4 rows  827193600000.0
       6.97M        1 rows  1158192000000.0
       6.88M        2 rows  752803200000.0
       6.62M        5 rows  626400000000.0
       6.55M        2 rows  945648000000.0

SRC_SHA256 by rows
      1.0K  0dc3975fb6b18729c822d5e0fdac5d478f0adbcec7e44a483cc375626742380f

SRC_SHA256 by dollars
       1.38B     1.0K rows  0dc3975fb6b18729c822d5e0fdac5d478f0adbcec7e44a483cc375626742

## who x when

RULINGDATE by CREATED_DA, dollars = SHAPE_STAR
  1589414400000.0                           2020:8.80M
  1631145600000.0                           2021:170.57M
  nan                                       2020:1.77M 2021:30.3K 2023:5.40M 2024:72.0K

SRC_SHA256 by CREATED_DA, dollars = SHAPE_STAR
  0dc3975fb6b18729c822d5e0fdac5d478f0adbce  2020:16.19M 2021:173.91M 2022:8.72M 2023:5.42M 2024:439.4K 2025:4.76M

## what

CASETYPE: Z 100%, SCB 0%

YEAR: 1986 12%, 1988 10%, 1997 9%, 2000 9%, 1989 9%, 1996 9%, 2001 8%, 2004 7%, 1998 7%, 1999 7%, 2005 7%, 1995 7%

CASE_RULIN: 0 94%, 2 3%, 1 1%, 12 0%, 9 0%, 4 0%, 3 0%, 8 0%

ADDRESS: 2300 FRAYSER BOULEVARD 13%, 5516 RAINES RD 13%, TCHULAHOMA 13%, 3535 CENTRAL AVE 13%, 2572 PARK AVE 7%, 3230 US HIGHWAY 51 7%, W/ SIDE OF SWINNEA RD; 1400 N  7%, 1389 FAIRFAX ST 7%, 1351 WILLIAMS AVE 7%, 1260 DEXTER LN 7%, 3343 WINCHESTER RD 7%

CREATED_US: BROOKS 42%, SDE 24%, HOLYFIELD 24%, SHARKEY 6%, DIXON 3%

LAST_EDITE: HOLYFIELD 98%, SDE 2%, SHARKEY 0%, DIXON 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | id | 1.0K | 0 | 1049 6; 1048 6; 1047 6; 1046 6 |
| CASETYPE | category | 2 | 0 | Z 1.0K; SCB 1 |
| YEAR | category | 41 | 13 | 1986 66; 1988 56; 1997 52; 2000 51 |
| CASENUM | other | 217 | 11 | 104 19; 108 18; 112 18; 102 17 |
| DOCKET | id | 1.0K | 0 | Z 1990-149 7; Z 2025- 004 6; Z 2024- 006 6; Z 2024- 008 6 |
| ATLAS_GRID | other | 140 | 29 | 2030 64; 2545 37; 1850 34; 1955 31 |
| CASE_RULIN | category | 8 | 0 | 0 986; 2 30; 1 14; 12 4 |
| RULINGDATE | who | 443 | 0 | nan 375; 872467200000.0 7; 734659200000.0 7; 1012867200000.0 7 |
| COMMENTS | other | 51 | 998 | R8 to EMP 2; APPOVED 1; HOLD FOR ONE MONTH 1; Converted to PD95-325 1 |
| ADDRESS | category | 50 | 996 | 2300 FRAYSER BOULEVARD 2; 5516 RAINES RD 2; TCHULAHOMA 2; 3535 CENTRAL AVE 2 |
| CREATED_US | category | 6 | 987 | BROOKS 26; SDE 15; HOLYFIELD 15; SHARKEY 4 |
| CREATED_DA | date | 39 | 0 | nan 987; 1756339200000.0 4; 1607990400000.0 4; 1627516800000.0 4 |
| LAST_EDITE | category | 5 | 3 | HOLYFIELD 1.0K; SDE 16; SHARKEY 4; DIXON 1 |
| LAST_EDI_1 | date | 12 | 0 | 1686182400000.0 1.0K; 1631750400000.0 10; 1756339200000.0 8; 1755820800000.0 5 |
| GLOBALID | id | 1.1K | 0 | {41B2438D-1ED7-4817-8324- 6; {6F5CE648-E539-488A-85A6- 6; {4F5CDC6C-E901-405A-8D88- 6; {4BC9C19A-AB61-44A3-BAD8- 6 |
| SHAPE_STAR | amount | 1.1K | 0 | 266273.338382 6; 164383.516168 6; 1656528.22005 6; 4735.54656767 6 |
| SHAPE_STLE | amount | 1.0K | 0 | 2430.29996886 6; 1641.48710144 6; 6173.73979113 6; 326.389023996 6 |
| SHAPE__AREA | amount | 1.1K | 0 | 266273.33837890625 6; 164383.51626586914 6; 1656528.2200622559 6; 4735.546539306641 6 |
| SHAPE__LENGTH | amount | 1.0K | 0 | 2430.2999688609866 6; 1641.4871014387281 6; 6173.739791117153 6; 326.38902396188575 6 |
| GEOMETRY | id | 1.0K | 0 | {"type": "Polygon", "coor 6; {"type": "Polygon", "coor 6; {"type": "Polygon", "coor 6; {"type": "Polygon", "coor 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:52:10.35868 1.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 45c8cda6-3431-4847-b67a-4 1.0K |
| SRC_SHA256 | who | 1 | 0 | 0dc3975fb6b18729c822d5e0f 1.0K |
