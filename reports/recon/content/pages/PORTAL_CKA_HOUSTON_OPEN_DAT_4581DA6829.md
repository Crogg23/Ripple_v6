# PORTAL_CKA_HOUSTON_OPEN_DAT_4581DA6829

rows 447  columns 17  scan 5.3s

roles: amount 1, audit 2, category 5, date 1, other 5, who 4

## when

INGESTED_AT
  2026       447  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RFP_PRICE | 446 | 1.8K | 3.8K | 12.8K | 21.8K | 2.05M |

## who

DIMENSIONS by rows
        54  25 x 120
        29  50 x 100
        25  40 x 100
        21  50 x 120
        18  30 x 100
        18  60 x 100
        16  60 x 120
        11  60' x 170'
        11  30x100
        11  50x100
        10  25 x 110
         8  60' x 171'
         7  50 x 110
         7  80 x 100
         6  60x100
         6  100 x 100
         6  60 X 130
         6  30*100
         4  40 x 102
         4  44 x 100

DIMENSIONS by dollars
      161.2K       54 rows  25 x 120
      126.7K       21 rows  50 x 120
      115.2K       16 rows  60 x 120
      102.8K       29 rows  50 x 100
       99.5K       18 rows  60 x 100
       56.1K       11 rows  60' x 170'
       54.0K       18 rows  30 x 100
       52.5K       11 rows  50x100
       51.7K       25 rows  40 x 100
       41.0K        8 rows  60' x 171'
       38.5K        7 rows  50 x 110
       36.0K        6 rows  60x100
       33.0K       11 rows  30x100
       30.0K        6 rows  100 x 100
       30.0K        4 rows  50 x 165
       27.6K       10 rows  25 x 110
       26.6K        7 rows  80 x 100
       24.0K        3 rows  75 x 120
       22.5K        6 rows  60 X 130
       21.8K        1 rows  150 x 145.32

DEED_RESTRICTIONS by rows
        43  NO
        28  No setbacks in DR
        25  Sent for Review
        22  No setback DRs
        21  No
        15  No restrictions
        11  No Restrictions
         9  Yes
         7  YES
         6  No deed restrictions.
         6  No deed restrictions
         6  Yes setbacks in DR
         5  Front Setbacks in D/Rs-NO
         4  Setbacks in D/R'S
         4  Plat map shows a 25 feet front building line. No other restrictions.
         3  No Setbacks in DR's, Plat Map to be reviewed by P&D
         2  20 feet front & 10 feet side building lines & no alcoholic beverages
         2  30 feet front & 4 feet side building lines; street corner lots 12 feet
         2  30 ft front & 12 ft side building line. No alcohol sales or dance hall
         2  20 ft front, 6 ft side & 10 ft side st. building lines

DEED_RESTRICTIONS by dollars
      171.1K       43 rows  NO
      115.2K       28 rows  No setbacks in DR
      100.7K       22 rows  No setback DRs
       99.0K       25 rows  Sent for Review
       85.8K       21 rows  No
       82.8K       15 rows  No restrictions
       52.9K        9 rows  Yes
       45.9K        6 rows  Yes setbacks in DR
       40.0K       11 rows  No Restrictions
       28.8K        4 rows  Plat map shows a 25 feet front building line. No other restr
       28.5K        6 rows  No deed restrictions
       26.9K        7 rows  YES
       24.4K        6 rows  No deed restrictions.
       20.8K        5 rows  Front Setbacks in D/Rs-NO
       16.4K        4 rows  Setbacks in D/R'S
       15.0K        1 rows  20 foot front & 5 foot side building line; however garages m
       12.2K        2 rows  30 ft front & 12 ft side building line. No alcohol sales or 
       11.8K        1 rows  20 ft front, 5 ft side & 15 ft side street building lines
       10.9K        1 rows  20 foot front & 10 feet side street building line
       10.3K        2 rows  30 feet front & 4 feet side building lines; street corner lo

SUBDIVISION by rows
        82  HIGHLAND ADDITION
        58  HIGHLAND HEIGHTS
        30  TRINITY GARDENS SEC 2
        24  LINCOLN CITY SEC 3
        19  LIBERTY ROAD MANOR SEC 14
        13  LIBERTY ROAD MANOR SEC 6
        13  BLUE BONNET ESTATES
        12  SUNNYSIDE COURTS
        11  ROSEWOOD ESTATES SEC 02
        11  WASHINGTON HEIGHTS ANNEX SEC 1
        11  RUBERFIELD
        11  CARVER ESTATES
        10  HOLLEMAN
         9  ROSEWOOD ESTATES
         7  SETTEGAST HEIGHTS U/R
         6  LIBERTY TERRACE
         6  ABST 1281 J M SWISHER
         6  SUNNYSIDE PLACE
         5  VIOLA
         4  EAGLE

SUBDIVISION by dollars
      338.1K       82 rows  HIGHLAND ADDITION
      255.1K       58 rows  HIGHLAND HEIGHTS
      181.4K       24 rows  LINCOLN CITY SEC 3
      150.6K       30 rows  TRINITY GARDENS SEC 2
       95.2K       13 rows  BLUE BONNET ESTATES
       68.5K       12 rows  SUNNYSIDE COURTS
       59.8K       11 rows  CARVER ESTATES
       55.8K       11 rows  RUBERFIELD
       42.4K       11 rows  WASHINGTON HEIGHTS ANNEX SEC 1
       42.3K       13 rows  LIBERTY ROAD MANOR SEC 6
       41.9K       19 rows  LIBERTY ROAD MANOR SEC 14
       41.2K       11 rows  ROSEWOOD ESTATES SEC 02
       33.8K        9 rows  ROSEWOOD ESTATES
       33.4K       10 rows  HOLLEMAN
       31.6K        6 rows  SUNNYSIDE PLACE
       30.2K        4 rows  WASHINGTON HEIGHTS ANNEX SEC 2
       27.4K        6 rows  LIBERTY TERRACE
       26.8K        2 rows  BROOKHAVEN R/P
       26.3K        6 rows  ABST 1281 J M SWISHER
       24.0K        4 rows  TRINITY GARDENS SEC 3

SRC_SHA256 by rows
       447  ec9b1555aeac0ead3765f2e46493ceff9a41b14af095dec6fe83f1498c974a82

SRC_SHA256 by dollars
       2.05M      447 rows  ec9b1555aeac0ead3765f2e46493ceff9a41b14af095dec6fe83f1498c97

## who x when

DIMENSIONS by INGESTED_AT  LOAD STAMP, not an event date, dollars = RFP_PRICE
  100 x 100                                 2026:30.0K
  150 x 145.32                              2026:21.8K
  25 x 110                                  2026:27.6K
  25 x 120                                  2026:161.2K
  30 x 100                                  2026:54.0K
  30*100                                    2026:18.0K
  30x100                                    2026:33.0K
  40 x 100                                  2026:51.7K
  40 x 102                                  2026:8.2K
  44 x 100                                  2026:17.6K
  50 x 100                                  2026:102.8K
  50 x 110                                  2026:38.5K
  50 x 120                                  2026:126.7K
  50 x 165                                  2026:30.0K
  50x100                                    2026:52.5K
  60 X 130                                  2026:22.5K
  60 x 100                                  2026:99.5K
  60 x 120                                  2026:115.2K
  60' x 170'                                2026:56.1K
  60' x 171'                                2026:41.0K
  60x100                                    2026:36.0K
  75 x 120                                  2026:24.0K
  80 x 100                                  2026:26.6K

DEED_RESTRICTIONS by INGESTED_AT  LOAD STAMP, not an event date, dollars = RFP_PRICE
  20 feet front & 10 feet side building li  2026:8.9K
  20 foot front & 10 feet side street buil  2026:10.9K
  20 foot front & 5 foot side building lin  2026:15.0K
  20 ft front, 5 ft side & 15 ft side stre  2026:11.8K
  20 ft front, 6 ft side & 10 ft side st.   2026:7.5K
  30 feet front & 4 feet side building lin  2026:10.3K
  30 ft front & 12 ft side building line.   2026:12.2K
  Front Setbacks in D/Rs-NO                 2026:20.8K
  NO                                        2026:171.1K
  No                                        2026:85.8K
  No Restrictions                           2026:40.0K
  No Setbacks in DR's, Plat Map to be revi  2026:8.0K
  No deed restrictions                      2026:28.5K
  No deed restrictions.                     2026:24.4K
  No restrictions                           2026:82.8K
  No setback DRs                            2026:100.7K
  No setbacks in DR                         2026:115.2K
  Plat map shows a 25 feet front building   2026:28.8K
  Sent for Review                           2026:99.0K
  Setbacks in D/R'S                         2026:16.4K
  YES                                       2026:26.9K
  Yes                                       2026:52.9K
  Yes setbacks in DR                        2026:45.9K

## what

HOPE_AREA: Acres Home 45%, Settegast 19%, Sunnyside 15%, Trinity/Houston Gardens 13%, Fifth Ward 6%, Independence Heights 1%, Third Ward 0%, Magnolia 0%, Denver Harbor 0%

ZIPCODE: 77028 31%, 77088 29%, 77091 17%, 77051 13%, 77026 4%, 77016 2%, 77020 2%, 77018 1%, 77004 0%, 77012 0%

LOT_USE_DESCRIPTION: Single-Family 80%, May Subdivide into 2 Single-Fa 17%, May Subdivide into 3 Single-Fa 2%, Possible Urban Garden Location 0%, Single-Family; Must Send Plans 0%, May Subdivide into 6 Single-Fa 0%

KEYMAP: 455T 17%, 412S 14%, 412Y 11%, 533Y 11%, 412T 11%, 455P 8%, 412X 6%, 454L 5%, 412W 5%, 412Q 4%, 454Q 4%, 411V 3%

NONE: Details 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| HOPE_AREA | category | 10 | 1 | Acres Home 201; Settegast 83; Sunnyside 67; Trinity/Houston Gardens 60 |
| HCAD | other | 444 | 0 | Count = 446 3; #0660250080817 3; #0660250080791 3; #0660250080814 3 |
| COH | other | 434 | 1 | 5488 3; 3718 3; 3723 3; 3732 3 |
| ADDRESS | other | 269 | 1 | 0 SUNNYHILL RD 17; 0 COHN 13; 0 SPARTA AVE 11; 0 HOFFMAN 10 |
| ZIPCODE | category | 11 | 9 | 77028 134; 77088 127; 77091 74; 77051 59 |
| SUBDIVISION | who | 76 | 0 | HIGHLAND ADDITION 82; HIGHLAND HEIGHTS 58; TRINITY GARDENS SEC 2 30; LINCOLN CITY SEC 3 24 |
| LEGAL_DESCRIPTION | other | 420 | 1 | TR 817A BLK 8 3; LT 791 BLK 8 3; LT 814 BLK 8 3; LT 691 BLK 2 3 |
| DEED_RESTRICTIONS | who | 80 | 165 | NO 43; No setbacks in DR 28; Sent for Review 25; No setback DRs 22 |
| LOT_USE_DESCRIPTION | category | 7 | 12 | Single-Family 349; May Subdivide into 2 Sing 72; May Subdivide into 3 Sing 10; Possible Urban Garden Loc 2 |
| KEYMAP | category | 42 | 1 | 455T 55; 412S 48; 412Y 38; 533Y 37 |
| DIMENSIONS | who | 161 | 1 | 25 x 120 54; 50 x 100 29; 40 x 100 25; 50 x 120 21 |
| RFP_PRICE | amount | 89 | 1 | 3000 85; 6000 42; 5000 39; 3750 37 |
| LAND_SQFT | other | 112 | 1 | 3000 84; 5000 47; 6000 39; 7200 18 |
| NONE | category | 2 | 1 | Details 446 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:42:12.14443 447 |
| SOURCE_RUN_ID | audit | 1 | 0 | 35f83134-6414-44a0-87ec-1 447 |
| SRC_SHA256 | who | 1 | 0 | ec9b1555aeac0ead3765f2e46 447 |
