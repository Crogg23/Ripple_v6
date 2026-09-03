# PORTAL_CKA_SAN_JOSE_OPEN_DA_9E83620979

rows 62  columns 15  scan 4.0s

roles: amount 3, audit 2, category 4, date 1, empty 2, other 2, who 2

## when

INGESTED_AT
  2026        62  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AREAAC | 62 | 310.05 | 1.7K | 229.5K | 374.7K | 829.8K |
| SHAPE_LENGTH | 62 | 15.3K | 55.3K | 1.07M | 1.20M | 7.66M |
| SHAPE_AREA | 62 | 13.51M | 76.03M | 10.00B | 16.32B | 36.15B |

## who

FACILITYID by rows
         1  52
         1  8
         1  23
         1  28
         1  49
         1  39
         1  54
         1  31
         1  40
         1  32
         1  48
         1  1
         1  13
         1  62
         1  41
         1  7
         1  6
         1  59
         1  27
         1  15

FACILITYID by dollars
      374.7K        1 rows  8
      136.7K        1 rows  7
       56.7K        1 rows  27
       55.6K        1 rows  43
       33.6K        1 rows  60
       23.2K        1 rows  59
       13.4K        1 rows  58
       13.2K        1 rows  42
       12.3K        1 rows  41
       10.7K        1 rows  57
        9.9K        1 rows  56
        8.5K        1 rows  40
        8.1K        1 rows  55
        5.0K        1 rows  39
        3.6K        1 rows  54
        3.5K        1 rows  26
        3.3K        1 rows  53
        2.9K        1 rows  25
        2.8K        1 rows  24
        2.8K        1 rows  52

SRC_SHA256 by rows
        62  a54cb1f1854907a929e1270303773299d85b24eae353e35d0922c0458df66a01

SRC_SHA256 by dollars
      829.8K       62 rows  a54cb1f1854907a929e1270303773299d85b24eae353e35d0922c0458df6

## who x when

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREAAC
  1                                         2026:310.05
  13                                        2026:789.63
  15                                        2026:940.80
  23                                        2026:2.6K
  25                                        2026:2.9K
  26                                        2026:3.5K
  27                                        2026:56.7K
  28                                        2026:479.94
  31                                        2026:654.30
  32                                        2026:1.0K
  39                                        2026:5.0K
  40                                        2026:8.5K
  41                                        2026:12.3K
  42                                        2026:13.2K
  43                                        2026:55.6K
  48                                        2026:1.0K
  49                                        2026:1.1K
  52                                        2026:2.8K
  53                                        2026:3.3K
  54                                        2026:3.6K
  55                                        2026:8.1K
  56                                        2026:9.9K
  57                                        2026:10.7K
  58                                        2026:13.4K
  59                                        2026:23.2K
  6                                         2026:2.1K
  60                                        2026:33.6K
  62                                        2026:1.8K
  7                                         2026:136.7K
  8                                         2026:374.7K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREAAC
  a54cb1f1854907a929e1270303773299d85b24ea  2026:829.8K

## what

SOILTYPE: Silt Loam 31%, Clay Loam 27%, Clay 26%, Loam 13%, Sandy Clay 3%

COUNTUSDASITES: 25 31%, 36 27%, 40 26%, 13 13%, 2 3%

MINHSG: D 56%, B 44%

MINUSDA: Loam or Silt Loam 31%, Clay Loam 27%, Clay Loam or Silty Clay Loam-C 26%, Fine Sandy Loam-Gravelly Loam- 13%, Very Gravelly Clay 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 62 | 0 | 62 1; 61 1; 60 1; 59 1 |
| FACILITYID | who | 62 | 0 | 60 1; 59 1; 58 1; 57 1 |
| INTID | other | 62 | 0 | 60 1; 59 1; 58 1; 57 1 |
| SOILTYPE | category | 5 | 0 | Silt Loam 19; Clay Loam 17; Clay 16; Loam 8 |
| COUNTUSDASITES | category | 5 | 0 | 25 19; 36 17; 40 16; 13 8 |
| MINHSG | category | 2 | 0 | D 35; B 27 |
| MINUSDA | category | 5 | 0 | Loam or Silt Loam 19; Clay Loam 17; Clay Loam or Silty Clay L 16; Fine Sandy Loam-Gravelly  8 |
| AREAAC | amount | 62 | 0 | 33630.89 1; 23184.84 1; 13374.18 1; 10663.77 1 |
| LASTUPDATE | empty | 1 | 62 |  |
| NOTES | empty | 1 | 62 |  |
| SHAPE_LENGTH | amount | 62 | 0 | 609310.07633653 1; 197530.991474142 1; 236291.648121055 1; 188573.601117772 1 |
| SHAPE_AREA | amount | 61 | 0 | 1464791711.09549 1; 1009920029.9608 1; 582575710.954976 1; 464511044.773922 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:28:53.96600 62 |
| SOURCE_RUN_ID | audit | 1 | 0 | a3be4a11-8b6b-4f16-9ef1-5 62 |
| SRC_SHA256 | who | 1 | 0 | a54cb1f1854907a929e127030 62 |
