# FED_CMS_ORDER_AND_REFERRING

rows 2.02M  columns 10  scan 4.8s

roles: audit 2, category 5, date 1, id 2, who 2

## when

_INGESTED_AT
  2026     2.02M  ##############################

## who

LAST_NAME by rows
     10.9K  SMITH
     10.2K  PATEL
      8.3K  JOHNSON
      7.7K  LEE
      6.4K  MILLER
      6.3K  WILLIAMS
      6.2K  BROWN
      5.9K  NGUYEN
      5.8K  JONES
      5.0K  KIM
      4.8K  DAVIS
      4.3K  ANDERSON
      4.2K  THOMAS
      3.8K  SHAH
      3.7K  WILSON
      3.5K  MARTIN
      3.4K  TAYLOR
      3.4K  KHAN
      3.2K  MOORE
      3.2K  THOMPSON

FIRST_NAME by rows
     28.0K  MICHAEL
     23.6K  DAVID
     21.6K  JOHN
     20.7K  JENNIFER
     17.4K  ROBERT
     16.5K  JAMES
     14.7K  SARAH
     13.9K  JESSICA
     13.6K  ELIZABETH
     13.0K  DANIEL
     12.9K  CHRISTOPHER
     12.8K  MATTHEW
     12.8K  WILLIAM
     11.2K  MARK
     11.2K  JOSEPH
     10.5K  ANDREW
     10.5K  THOMAS
     10.2K  EMILY
      9.9K  RICHARD
      9.8K  AMANDA

## who x when

LAST_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  ANDERSON                                  2026:4.3K
  BROWN                                     2026:6.2K
  DAVIS                                     2026:4.8K
  JOHNSON                                   2026:8.3K
  JONES                                     2026:5.8K
  KHAN                                      2026:3.4K
  KIM                                       2026:5.0K
  LEE                                       2026:7.7K
  MARTIN                                    2026:3.5K
  MILLER                                    2026:6.4K
  MOORE                                     2026:3.2K
  NGUYEN                                    2026:5.9K
  PATEL                                     2026:10.2K
  SHAH                                      2026:3.8K
  SMITH                                     2026:10.9K
  TAYLOR                                    2026:3.4K
  THOMAS                                    2026:4.2K
  THOMPSON                                  2026:3.2K
  WILLIAMS                                  2026:6.3K
  WILSON                                    2026:3.7K

FIRST_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  AMANDA                                    2026:9.8K
  ANDREW                                    2026:10.5K
  CHRISTOPHER                               2026:12.9K
  DANIEL                                    2026:13.0K
  DAVID                                     2026:23.6K
  ELIZABETH                                 2026:13.6K
  EMILY                                     2026:10.2K
  JAMES                                     2026:16.5K
  JENNIFER                                  2026:20.7K
  JESSICA                                   2026:13.9K
  JOHN                                      2026:21.6K
  JOSEPH                                    2026:11.2K
  MARK                                      2026:11.2K
  MATTHEW                                   2026:12.8K
  MICHAEL                                   2026:28.0K
  RICHARD                                   2026:9.9K
  ROBERT                                    2026:17.4K
  SARAH                                     2026:14.7K
  THOMAS                                    2026:10.5K
  WILLIAM                                   2026:12.8K

## what

PARTB: Y 96%, N 4%

DME: Y 100%, N 0%

HHA: Y 84%, N 16%

PMD: Y 80%, N 20%

HOSPICE: Y 57%, N 43%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | id | 1.99M | 0 | 1962084368 3.2K; 1407295389 3.2K; 1932060308 3.2K; 1154315257 3.2K |
| LAST_NAME | who | 396.8K | 57 | PATEL 12.8K; SMITH 12.8K; JOHNSON 9.2K; MILLER 8.3K |
| FIRST_NAME | who | 137.8K | 26 | MICHAEL 28.0K; DAVID 23.6K; JOHN 21.6K; JENNIFER 20.7K |
| PARTB | category | 2 | 0 | Y 1.93M; N 87.2K |
| DME | category | 2 | 0 | Y 2.02M; N 4 |
| HHA | category | 2 | 0 | Y 1.69M; N 328.7K |
| PMD | category | 2 | 0 | Y 1.61M; N 413.1K |
| HOSPICE | category | 2 | 0 | Y 1.14M; N 878.0K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05 15:05:23.110 2.02M |
| _SOURCE_RUN_ID | audit id | 1.98M | 0 | 1e0c094c-ce91-4b5f-bb81-c 3.2K; 2c465df6-29c5-4c27-9eb0-a 3.2K; 5c4d9ef8-4b33-4ff3-9d13-2 3.2K; 08e147b0-e7cb-420b-8d21-1 3.2K |
