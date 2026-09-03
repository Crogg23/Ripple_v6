# FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS

rows 6.9K  columns 5  scan 4.0s

roles: audit 2, date 1, id 2, who 2

## when

_INGESTED_AT
  2026      6.9K  ##############################

## who

LAST_NAME by rows
        53  JOHNSON
        46  SMITH
        42  WILLIAMS
        34  JONES
        33  THOMAS
        31  MILLER
        24  DAVIS
        22  BROWN
        21  WHITE
        20  GONZALEZ
        20  RODRIGUEZ
        19  MOORE
        18  LEE
        17  TAYLOR
        17  WRIGHT
        16  MARTINEZ
        16  LEWIS
        16  PATEL
        15  GREEN
        15  WILSON

FIRST_NAME by rows
        89  JENNIFER
        70  JESSICA
        70  SARAH
        60  ELIZABETH
        56  AMANDA
        52  MELISSA
        50  EMILY
        49  ASHLEY
        46  MARY
        46  LAUREN
        44  NICOLE
        40  MEGAN
        39  STEPHANIE
        39  LISA
        38  KIMBERLY
        38  HEATHER
        37  MICHELLE
        37  SARA
        37  REBECCA
        36  KATHERINE

## who x when

LAST_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  BROWN                                     2026:22
  DAVIS                                     2026:24
  GONZALEZ                                  2026:20
  GREEN                                     2026:15
  JOHNSON                                   2026:53
  JONES                                     2026:34
  LEE                                       2026:18
  LEWIS                                     2026:16
  MARTINEZ                                  2026:16
  MILLER                                    2026:31
  MOORE                                     2026:19
  PATEL                                     2026:16
  RODRIGUEZ                                 2026:20
  SMITH                                     2026:46
  TAYLOR                                    2026:17
  THOMAS                                    2026:33
  WHITE                                     2026:21
  WILLIAMS                                  2026:42
  WILSON                                    2026:15
  WRIGHT                                    2026:17

FIRST_NAME by _INGESTED_AT  LOAD STAMP, not an event date
  AMANDA                                    2026:56
  ASHLEY                                    2026:49
  ELIZABETH                                 2026:60
  EMILY                                     2026:50
  HEATHER                                   2026:38
  JENNIFER                                  2026:89
  JESSICA                                   2026:70
  KATHERINE                                 2026:36
  KIMBERLY                                  2026:38
  LAUREN                                    2026:46
  LISA                                      2026:39
  MARY                                      2026:46
  MEGAN                                     2026:40
  MELISSA                                   2026:52
  MICHELLE                                  2026:37
  NICOLE                                    2026:44
  REBECCA                                   2026:37
  SARA                                      2026:37
  SARAH                                     2026:70
  STEPHANIE                                 2026:39

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NPI | id | 6.9K | 0 | 1619121571 35; 1851006621 35; 1831670736 35; 1447707658 35 |
| LAST_NAME | who | 5.0K | 0 | WILLIAMS 73; SMITH 73; JOHNSON 67; THOMAS 62 |
| FIRST_NAME | who | 2.6K | 1 | JENNIFER 89; SARAH 70; JESSICA 70; ELIZABETH 60 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-26 12:06:50.634 6.9K |
| _SOURCE_RUN_ID | audit id | 6.9K | 0 | b091da62-58ed-4ca7-8296-b 35; ec16ecea-57a2-414d-8773-d 35; dd8a58a6-f942-4836-a5cb-5 35; f8066967-a726-417c-947e-9 35 |
