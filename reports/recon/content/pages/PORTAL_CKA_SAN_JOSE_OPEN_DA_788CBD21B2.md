# PORTAL_CKA_SAN_JOSE_OPEN_DA_788CBD21B2

rows 1.7K  columns 11  scan 4.0s

roles: amount 2, audit 2, category 2, date 1, empty 1, id 2, who 2

## when

INGESTED_AT
  2026      1.7K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 1.7K | 5.26 | 5.9K | 161.2K | 1.05M | 24.02M |
| SHAPE_AREA | 1.7K | 0.64 | 699.6K | 46.04M | 300.33M | 5.34B |

## who

FACILITYID by rows
         1  104
         1  24
         1  47
         1  49
         1  142
         1  54
         1  57
         1  69
         1  32
         1  73
         1  105
         1  74
         1  94
         1  67
         1  26
         1  16
         1  84
         1  39
         1  45
         1  40

FACILITYID by dollars
       1.05M        1 rows  85
      588.1K        1 rows  112
      538.0K        1 rows  1183
      319.6K        1 rows  185
      316.1K        1 rows  23
      297.2K        1 rows  1015
      272.9K        1 rows  192
      269.3K        1 rows  1317
      250.7K        1 rows  280
      230.4K        1 rows  989
      210.2K        1 rows  1149
      209.1K        1 rows  312
      205.1K        1 rows  34
      188.8K        1 rows  1010
      169.0K        1 rows  701
      167.3K        1 rows  988
      163.3K        1 rows  456
      159.1K        1 rows  155
      153.8K        1 rows  1089
      148.3K        1 rows  114

SRC_SHA256 by rows
      1.7K  557d737ad25b09adf76c1406c88c235d6494fd21c7ee27e720d4c7ed0e914cb2

SRC_SHA256 by dollars
      24.02M     1.7K rows  557d737ad25b09adf76c1406c88c235d6494fd21c7ee27e720d4c7ed0e91

## who x when

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  1015                                      2026:297.2K
  104                                       2026:26.4K
  105                                       2026:3.5K
  112                                       2026:588.1K
  1183                                      2026:538.0K
  1317                                      2026:269.3K
  142                                       2026:385.98
  16                                        2026:14.0K
  185                                       2026:319.6K
  192                                       2026:272.9K
  23                                        2026:316.1K
  24                                        2026:54.9K
  26                                        2026:13.3K
  280                                       2026:250.7K
  32                                        2026:8.9K
  39                                        2026:123.2K
  40                                        2026:3.8K
  45                                        2026:6.9K
  47                                        2026:10.2K
  49                                        2026:6.5K
  54                                        2026:4.5K
  57                                        2026:12.8K
  67                                        2026:3.9K
  69                                        2026:7.9K
  73                                        2026:3.9K
  74                                        2026:5.4K
  84                                        2026:7.5K
  85                                        2026:1.05M
  94                                        2026:1.8K
  989                                       2026:230.4K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  557d737ad25b09adf76c1406c88c235d6494fd21  2026:24.02M

## what

OVERWINTERINGHABITAT: Yes 51%, Potential 49%

LASTUPDATE: 2013/06/28 11:50:24+00 70%, 2013/06/28 11:50:23+00 22%, 2013/06/28 11:50:22+00 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.7K | 0 | 1703 9; 1702 9; 1701 9; 1700 9 |
| FACILITYID | who | 1.7K | 0 | 1361 9; 1360 9; 1359 9; 1358 9 |
| INTID | id | 1.7K | 0 | 1361 9; 1360 9; 1359 9; 1358 9 |
| OVERWINTERINGHABITAT | category | 2 | 0 | Yes 876; Potential 825 |
| LASTUPDATE | category | 3 | 0 | 2013/06/28 11:50:24+00 1.2K; 2013/06/28 11:50:23+00 382; 2013/06/28 11:50:22+00 127 |
| NOTES | empty | 1 | 1.7K |  |
| SHAPE_LENGTH | amount | 1.7K | 0 | 201.665406563842 9; 7390.28609385022 9; 8811.50472024621 9; 7715.76788223661 9 |
| SHAPE_AREA | amount | 1.7K | 0 | 109.341754010226 9; 1487967.98560812 9; 3542174.16931848 9; 167891.389738964 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:55:55.67790 1.7K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0cca1f7d-ef7a-4281-bbae-8 1.7K |
| SRC_SHA256 | who | 1 | 0 | 557d737ad25b09adf76c1406c 1.7K |
