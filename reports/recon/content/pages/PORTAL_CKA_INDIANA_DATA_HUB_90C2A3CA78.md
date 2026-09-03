# PORTAL_CKA_INDIANA_DATA_HUB_90C2A3CA78

rows 784  columns 6  scan 2.9s

roles: audit 2, category 1, date 1, other 1, who 2

## when

INGESTED_AT
  2026       784  ##############################

## who

COUNTY by rows
        38  Marion
        27  Allen
        27  Lake
        20  St. Joseph
        14  Henry
        14  Kosciusko
        14  Spencer
        14  Vigo
        14  Madison
        13  Clark
        13  Tippecanoe
        13  Hamilton
        12  Delaware
        12  Harrison
        11  Monroe
        11  Hendricks
        11  Gibson
        11  Clay
        11  Wayne
        11  Grant

SRC_SHA256 by rows
       784  6446cf4487b54437e07f094dbc7588da7d85bf56af984c0a02854225c6f3cdab

## who x when

COUNTY by INGESTED_AT  LOAD STAMP, not an event date
  Allen                                     2026:27
  Clark                                     2026:13
  Clay                                      2026:11
  Delaware                                  2026:12
  Gibson                                    2026:11
  Grant                                     2026:11
  Hamilton                                  2026:13
  Harrison                                  2026:12
  Hendricks                                 2026:11
  Henry                                     2026:14
  Kosciusko                                 2026:14
  Lake                                      2026:27
  Madison                                   2026:14
  Marion                                    2026:38
  Monroe                                    2026:11
  Spencer                                   2026:14
  St. Joseph                                2026:20
  Tippecanoe                                2026:13
  Vigo                                      2026:14
  Wayne                                     2026:11

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  6446cf4487b54437e07f094dbc7588da7d85bf56  2026:784

## what

OTP_DRIVE_TIME_IN_MINUTES: 15-30 36%, 0-15 31%, 30-45 24%, 45-60 7%, 60-90 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COUNTY | who | 93 | 0 | Marion 38; Allen 27; Lake 27; St. Joseph 20 |
| ZCTA | other | 763 | 0 | 47951 4; 47713 4; 47280 4; 47401 4 |
| OTP_DRIVE_TIME_IN_MINUTES | category | 5 | 0 | 15-30 284; 0-15 245; 30-45 191; 45-60 52 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:46:59.00595 784 |
| SOURCE_RUN_ID | audit | 1 | 0 | c08b9a82-5ddf-4c11-87da-2 784 |
| SRC_SHA256 | who | 1 | 0 | 6446cf4487b54437e07f094db 784 |
