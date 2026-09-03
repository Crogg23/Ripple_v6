# FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS

rows 7.2K  columns 5  scan 3.7s

roles: audit 2, date 1, id 2, who 2

## when

_INGESTED_AT
  2026      7.2K  ##############################

## who

LAST_NAME by rows
        52  PATEL
        41  SMITH
        37  NGUYEN
        23  WILLIAMS
        23  LEE
        22  KIM
        21  SHAH
        19  MOORE
        19  BROWN
        17  KHAN
        17  CHEN
        15  DAVIS
        15  TAYLOR
        14  PEREZ
        14  JOHNSON
        14  RODRIGUEZ
        13  WILSON
        13  SINGH
        13  WONG
        12  WHITE

FIRST_NAME by rows
        82  MICHAEL
        70  JOHN
        56  DAVID
        54  MATTHEW
        53  JAMES
        52  ANDREW
        49  ROBERT
        49  DANIEL
        47  WILLIAM
        46  SARAH
        46  JOSEPH
        40  JOSHUA
        36  CHRISTOPHER
        36  ERIC
        35  RYAN
        34  JENNIFER
        33  JESSICA
        31  LAUREN
        30  JACOB
        29  JONATHAN

## who x when

LAST_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  BROWN                                     2026:19
  CHEN                                      2026:17
  DAVIS                                     2026:15
  JOHNSON                                   2026:14
  KHAN                                      2026:17
  KIM                                       2026:22
  LEE                                       2026:23
  MOORE                                     2026:19
  NGUYEN                                    2026:37
  PATEL                                     2026:52
  PEREZ                                     2026:14
  RODRIGUEZ                                 2026:14
  SHAH                                      2026:21
  SINGH                                     2026:13
  SMITH                                     2026:41
  TAYLOR                                    2026:15
  WHITE                                     2026:12
  WILLIAMS                                  2026:23
  WILSON                                    2026:13
  WONG                                      2026:13

FIRST_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  ANDREW                                    2026:52
  CHRISTOPHER                               2026:36
  DANIEL                                    2026:49
  DAVID                                     2026:56
  ERIC                                      2026:36
  JACOB                                     2026:30
  JAMES                                     2026:53
  JENNIFER                                  2026:34
  JESSICA                                   2026:33
  JOHN                                      2026:70
  JONATHAN                                  2026:29
  JOSEPH                                    2026:46
  JOSHUA                                    2026:40
  LAUREN                                    2026:31
  MATTHEW                                   2026:54
  MICHAEL                                   2026:82
  ROBERT                                    2026:49
  RYAN                                      2026:35
  SARAH                                     2026:46
  WILLIAM                                   2026:47

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | id | 7.4K | 0 | 1477172195 37; 1619559861 37; 1386586246 37; 1457563751 37 |
| LAST_NAME | who | 5.5K | 0 | PATEL 75; SMITH 70; NGUYEN 58; WILLIAMS 56 |
| FIRST_NAME | who | 3.2K | 4 | MICHAEL 83; JOHN 70; DAVID 57; JAMES 55 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-26 12:06:55.600 7.2K |
| _SOURCE_RUN_ID | audit id | 7.1K | 0 | 7fd86796-93ec-449b-9f48-5 37; 0b0da8b9-436d-49c0-8a6e-c 37; 06c221b3-35b0-47c9-ae53-8 37; 8c68ba81-d491-4440-86c1-1 37 |
