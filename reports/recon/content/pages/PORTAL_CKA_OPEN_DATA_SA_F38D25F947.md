# PORTAL_CKA_OPEN_DATA_SA_F38D25F947

rows 53  columns 9  scan 3.7s

roles: amount 2, audit 2, category 1, date 2, other 1, who 2

## when

CREATED_DATE
  2025        53  ##############################

INGESTED_AT
  2026        53  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 53 | 0 | 0 | 0.01 | 0.01 | 0.03 |
| SHAPE__LENGTH | 53 | 0.09 | 0.26 | 1.27 | 1.41 | 18.63 |

## who

NAME by rows
         1  FS37
         1  FS13
         1  FS04
         1  FS43
         1  FS06
         1  FS51
         1  FS02
         1  FS34
         1  FS29
         1  FS17
         1  FS52
         1  FS39
         1  FS46
         1  FS03
         1  FS48
         1  FS07
         1  FS15
         1  FS10
         1  FS45
         1  FS53

NAME by dollars
        0.01        1 rows  FS50
        0.01        1 rows  FS45
        0.01        1 rows  FS53
           0        1 rows  FS26
           0        1 rows  FS01
           0        1 rows  FS06
           0        1 rows  FS38
           0        1 rows  FS48
           0        1 rows  FS13
           0        1 rows  FS35
           0        1 rows  FS41
           0        1 rows  FS52
           0        1 rows  FS31
           0        1 rows  FS47
           0        1 rows  FS46
           0        1 rows  FS44
           0        1 rows  FS22
           0        1 rows  FS30
           0        1 rows  FS54
           0        1 rows  FS42

SRC_SHA256 by rows
        53  cbf881eea98ab6fce11ca60df3b52582bd39f24a3e339c5de5a3b9e6bea50f81

SRC_SHA256 by dollars
        0.03       53 rows  cbf881eea98ab6fce11ca60df3b52582bd39f24a3e339c5de5a3b9e6bea5

## who x when

NAME by CREATED_DATE, dollars = SHAPE__AREA
  FS01                                      2025:0
  FS02                                      2025:0
  FS03                                      2025:0
  FS04                                      2025:0
  FS06                                      2025:0
  FS07                                      2025:0
  FS10                                      2025:0
  FS13                                      2025:0
  FS15                                      2025:0
  FS17                                      2025:0
  FS22                                      2025:0
  FS26                                      2025:0
  FS29                                      2025:0
  FS31                                      2025:0
  FS34                                      2025:0
  FS35                                      2025:0
  FS37                                      2025:0
  FS38                                      2025:0
  FS39                                      2025:0
  FS41                                      2025:0
  FS43                                      2025:0
  FS44                                      2025:0
  FS45                                      2025:0.01
  FS46                                      2025:0
  FS47                                      2025:0
  FS48                                      2025:0
  FS50                                      2025:0.01
  FS51                                      2025:0
  FS52                                      2025:0
  FS53                                      2025:0.01

SRC_SHA256 by CREATED_DATE, dollars = SHAPE__AREA
  cbf881eea98ab6fce11ca60df3b52582bd39f24a  2025:0.03

## what

PLANNING_ZONES: 7 13%, 8 13%, 1 13%, 2 13%, 6 13%, 5 11%, 3 11%, 4 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 53 | 0 | 53 1; 52 1; 51 1; 50 1 |
| NAME | who | 53 | 0 | FS43 1; FS33 1; FS05 1; FS19 1 |
| PLANNING_ZONES | category | 8 | 0 | 7 7; 8 7; 1 7; 2 7 |
| CREATED_DATE | date | 1 | 0 | 11/13/2025 4:34:56 PM 53 |
| SHAPE__AREA | amount | 53 | 0 | 0.00331235331145763 1; 0.00192899542344094 1; 0.000773013537582301 1; 0.00134983076281969 1 |
| SHAPE__LENGTH | amount | 53 | 0 | 0.563018016706757 1; 0.282459953125894 1; 0.206088001235152 1; 0.197043211392879 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:28:08.91849 53 |
| SOURCE_RUN_ID | audit | 1 | 0 | a39c6d45-48a2-4e27-8638-2 53 |
| SRC_SHA256 | who | 1 | 0 | cbf881eea98ab6fce11ca60df 53 |
