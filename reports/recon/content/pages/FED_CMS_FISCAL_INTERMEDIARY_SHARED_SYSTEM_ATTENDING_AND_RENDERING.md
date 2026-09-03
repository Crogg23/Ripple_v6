# FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING

rows 2.05M  columns 5  scan 4.3s

roles: audit 2, date 1, id 2, who 2

## when

_INGESTED_AT
  2026     2.05M  ##############################

## who

LAST_NAME by rows
     11.2K  SMITH
     10.1K  PATEL
      8.5K  JOHNSON
      7.7K  LEE
      6.7K  MILLER
      6.4K  BROWN
      6.3K  WILLIAMS
      5.9K  JONES
      5.9K  NGUYEN
      5.0K  DAVIS
      5.0K  KIM
      4.5K  ANDERSON
      4.3K  THOMAS
      3.8K  WILSON
      3.7K  SHAH
      3.6K  MARTIN
      3.5K  TAYLOR
      3.3K  MOORE
      3.3K  KHAN
      3.2K  THOMPSON

FIRST_NAME by rows
     29.1K  MICHAEL
     24.2K  DAVID
     22.1K  JOHN
     21.2K  JENNIFER
     17.8K  ROBERT
     17.0K  JAMES
     14.8K  SARAH
     14.2K  JESSICA
     13.7K  CHRISTOPHER
     13.7K  ELIZABETH
     13.5K  MATTHEW
     13.5K  DANIEL
     13.0K  WILLIAM
     11.6K  JOSEPH
     11.6K  MARK
     10.9K  ANDREW
     10.7K  THOMAS
     10.4K  EMILY
     10.0K  AMANDA
     10.0K  RICHARD

## who x when

LAST_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  ANDERSON                                  2026:4.5K
  BROWN                                     2026:6.4K
  DAVIS                                     2026:5.0K
  JOHNSON                                   2026:8.5K
  JONES                                     2026:5.9K
  KHAN                                      2026:3.3K
  KIM                                       2026:5.0K
  LEE                                       2026:7.7K
  MARTIN                                    2026:3.6K
  MILLER                                    2026:6.7K
  MOORE                                     2026:3.3K
  NGUYEN                                    2026:5.9K
  PATEL                                     2026:10.1K
  SHAH                                      2026:3.7K
  SMITH                                     2026:11.2K
  TAYLOR                                    2026:3.5K
  THOMAS                                    2026:4.3K
  THOMPSON                                  2026:3.2K
  WILLIAMS                                  2026:6.3K
  WILSON                                    2026:3.8K

FIRST_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  AMANDA                                    2026:10.0K
  ANDREW                                    2026:10.9K
  CHRISTOPHER                               2026:13.7K
  DANIEL                                    2026:13.5K
  DAVID                                     2026:24.2K
  ELIZABETH                                 2026:13.7K
  EMILY                                     2026:10.4K
  JAMES                                     2026:17.0K
  JENNIFER                                  2026:21.2K
  JESSICA                                   2026:14.2K
  JOHN                                      2026:22.1K
  JOSEPH                                    2026:11.6K
  MARK                                      2026:11.6K
  MATTHEW                                   2026:13.5K
  MICHAEL                                   2026:29.1K
  RICHARD                                   2026:10.0K
  ROBERT                                    2026:17.8K
  SARAH                                     2026:14.8K
  THOMAS                                    2026:10.7K
  WILLIAM                                   2026:13.0K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | id | 1.99M | 0 | 1801593199 3.3K; 1669402152 3.3K; 1083443626 3.3K; 1831162759 3.3K |
| LAST_NAME | who | 397.6K | 58 | SMITH 13.9K; PATEL 12.7K; JOHNSON 9.4K; MILLER 8.4K |
| FIRST_NAME | who | 136.4K | 24 | MICHAEL 29.1K; DAVID 24.2K; JOHN 22.1K; JENNIFER 21.2K |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05 14:59:04.834 2.05M |
| _SOURCE_RUN_ID | audit id | 1.99M | 0 | c5e6a2d5-a2f5-44ec-be27-e 3.3K; 0a4d6a13-6cd0-4a0b-91aa-4 3.3K; 8035bb78-7713-4e4f-8382-7 3.3K; c66218be-9c32-47f8-9f8c-d 3.3K |
