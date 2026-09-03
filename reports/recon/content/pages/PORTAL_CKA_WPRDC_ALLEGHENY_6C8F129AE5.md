# PORTAL_CKA_WPRDC_ALLEGHENY_6C8F129AE5

rows 1.0K  columns 38  scan 4.9s

roles: amount 2, audit 2, category 18, date 2, empty 6, id 5, who 4

## when

LAST_EDI_1
  2018      1.0K  ##############################

INGESTED_AT
  2026      1.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 1.0K | 40.38 | 40.44 | 40.47 | 40.49 | 41.5K |
| LONGITUDE | 1.0K | -80.04 | -79.97 | -79.92 | -79.90 | -82.0K |

## who

LOCATION by rows
        59  PENN AVE
        46  E CARSON ST
        43  CENTRE AVE
        36  FORBES AVE
        34  LIBERTY AVE
        34  MURRAY AVE
        29  BUTLER ST
        21  BROOKLINE BLVD
        21  SCHENLEY DR
        18  5TH AVE
        17  BAUM BLVD
        15  BROWNSVILLE RD
        14  W GENERAL ROBINSON ST
        12  WESTERN AVE
        12  BLVD OF ALLIES
        11  FIFTH AVE
        10  FEDERAL ST
        10  PENN AVE.
        10  BIGELOW BLVD
         9  GRANDVIEW AVE

LOCATION by dollars
        2.4K       59 rows  PENN AVE
        1.9K       46 rows  E CARSON ST
        1.7K       43 rows  CENTRE AVE
        1.5K       36 rows  FORBES AVE
        1.4K       34 rows  LIBERTY AVE
        1.4K       34 rows  MURRAY AVE
        1.2K       29 rows  BUTLER ST
      849.24       21 rows  SCHENLEY DR
      848.24       21 rows  BROOKLINE BLVD
      727.92       18 rows  5TH AVE
      687.81       17 rows  BAUM BLVD
      605.95       15 rows  BROWNSVILLE RD
      566.30       14 rows  W GENERAL ROBINSON ST
      485.40       12 rows  WESTERN AVE
      485.28       12 rows  BLVD OF ALLIES
      444.91       11 rows  FIFTH AVE
      404.66       10 rows  PENN AVE.
      404.55       10 rows  FEDERAL ST
      404.48       10 rows  BIGELOW BLVD
      364.07        9 rows  CEDAR AVE

NODE by rows
       101  SOUTHSIDE
        91  NORTHSIDE
        68  BLOOMFIELD
        60  OAKLAND3
        57  EASTLIB
        57  DOWNTOWN2
        51  STRIPDIST
        49  UPTOWN2
        46  SQ.HILL1
        44  OAKLAND4
        42  SHADYSIDE2
        41  DOWNTOWN1
        38  NORTHSHORE
        38  OAKLAND2
        31  OAKLAND1
        29  LAWRENCEV
        21  BROOKLINE
        17  MT.WASH
        12  UPTOWN1
        10  SHADYSIDE1

NODE by dollars
        4.1K      101 rows  SOUTHSIDE
        3.7K       91 rows  NORTHSIDE
        2.8K       68 rows  BLOOMFIELD
        2.4K       60 rows  OAKLAND3
        2.3K       57 rows  EASTLIB
        2.3K       57 rows  DOWNTOWN2
        2.1K       51 rows  STRIPDIST
        2.0K       49 rows  UPTOWN2
        1.9K       46 rows  SQ.HILL1
        1.8K       44 rows  OAKLAND4
        1.7K       42 rows  SHADYSIDE2
        1.7K       41 rows  DOWNTOWN1
        1.5K       38 rows  NORTHSHORE
        1.5K       38 rows  OAKLAND2
        1.3K       31 rows  OAKLAND1
        1.2K       29 rows  LAWRENCEV
      848.24       21 rows  BROOKLINE
      687.36       17 rows  MT.WASH
      485.28       12 rows  UPTOWN1
      404.50       10 rows  SHADYSIDE1

TERMINAL_S by rows
      1.0K  Active

TERMINAL_S by dollars
       41.5K     1.0K rows  Active

SRC_SHA256 by rows
      1.0K  bdd953b057dbd69a120c9fa39b7855a0f506996022e7cb855285925c8c26a43f

SRC_SHA256 by dollars
       41.5K     1.0K rows  bdd953b057dbd69a120c9fa39b7855a0f506996022e7cb855285925c8c26

## who x when

LOCATION by LAST_EDI_1, dollars = LATITUDE
  5TH AVE                                   2018:727.92
  BAUM BLVD                                 2018:687.81
  BIGELOW BLVD                              2018:404.48
  BLVD OF ALLIES                            2018:485.28
  BROOKLINE BLVD                            2018:807.84
  BROWNSVILLE RD                            2018:605.95
  BUTLER ST                                 2018:1.2K
  CEDAR AVE                                 2018:364.07
  CENTRE AVE                                2018:1.7K
  E CARSON ST                               2018:1.9K
  FEDERAL ST                                2018:404.55
  FIFTH AVE                                 2018:404.47
  FORBES AVE                                2018:1.5K
  GRANDVIEW AVE                             2018:363.92
  LIBERTY AVE                               2018:1.4K
  MURRAY AVE                                2018:1.4K
  PENN AVE                                  2018:2.4K
  PENN AVE.                                 2018:404.66
  SCHENLEY DR                               2018:849.24
  W GENERAL ROBINSON ST                     2018:566.30
  WESTERN AVE                               2018:485.40

NODE by LAST_EDI_1, dollars = LATITUDE
  BLOOMFIELD                                2018:2.8K
  BROOKLINE                                 2018:807.84
  DOWNTOWN1                                 2018:1.7K
  DOWNTOWN2                                 2018:2.3K
  EASTLIB                                   2018:2.3K
  LAWRENCEV                                 2018:1.2K
  MT.WASH                                   2018:687.36
  NORTHSHORE                                2018:1.5K
  NORTHSIDE                                 2018:3.7K
  OAKLAND1                                  2018:1.3K
  OAKLAND2                                  2018:1.5K
  OAKLAND3                                  2018:2.4K
  OAKLAND4                                  2018:1.8K
  SHADYSIDE1                                2018:404.50
  SHADYSIDE2                                2018:1.7K
  SOUTHSIDE                                 2018:4.0K
  SQ.HILL1                                  2018:1.9K
  STRIPDIST                                 2018:2.1K
  UPTOWN1                                   2018:485.28
  UPTOWN2                                   2018:1.9K

## what

DATE1: Mon - Sat 89%, Mon - Thurs 11%

DATE2: Fri - Sat 100%

LAST_EDITE: SDE 100%

LOT: Lot 98%, LOT 2%

MAXHOURS: No Max 45%, 2 Hours 39%, 4 Hours 10%, 10 Hours 5%, 3 Hours 2%

NODE_1: SouthSide 13%, Northside 12%, Bloomfield 9%, Uptown 9%, SquirellHill 9%, ShadySide 8%, Oakland 3 8%, East Liberty 7%, Downtown 2 7%, Strip District 7%, Oakland 4 6%, Downtown 1 6%

RATE: $1.50 Per Hour 50%, $3 Per Hour 18%, $4 Per Hour 10%, $2 Per Hour 8%, $3.00 Per Hour 5%, $1 Per Hour 3%, $2.00 Per Hour 3%, Dynamic 3%, $1.00 Per Hour 2%

RATE2: $2.50 Per Hour 100%

RATETIMEA: ~ 8AM - 2PM 100%

RATETIMEB: ~ 2PM - 6PM 100%

RESTDATES: Mon - Fri 93%, Fri - Sat 7%

RESTRICTIO: M-F, 7AM-9AM, 4PM-6PM 70%, M-F, 7AM-9AM 20%, M-F, 4PM-6PM 4%, M-F, 3PM-6PM 2%, M-F, 7AM-9AM, 3PM-6PM 2%, M-F, 7-10AM 1%

RESTTIME1: 7AM - 9AM 86%, 10PM - 2AM 5%, 4PM - 6PM 4%, 3PM - 6PM 2%, 6PM - 4AM 1%, 7AM - 10AM 1%

RESTTIME2: 4PM - 6PM 97%, 3PM - 6PM 3%

SIM_NUMBER: 9223372036854775807 100%, 0 0%

SPECIALEV: No 95%, Yes 5%

TIME1: ~ 8AM - 6PM 94%, ~ 8AM - 10PM 6%

TIME2: ~ 8AM - 12AM 92%, ~ 8AM - 10PM 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | id | 1.0K | 0 | 1035 6; 1034 6; 1033 6; 1032 6 |
| CREATED_DA | empty | 1 | 1.0K |  |
| CREATED_DATE | empty | 1 | 1.0K |  |
| CREATED_US | empty | 1 | 1.0K |  |
| CREATED_USER | empty | 1 | 1.0K |  |
| DATE1 | category | 3 | 6 | Mon - Sat 912; Mon - Thurs 108 |
| DATE2 | category | 2 | 918 | Fri - Sat 108 |
| LAST_EDI_1 | date | 3 | 6 | 2018-04-19T00:00:00+00:00 1.0K; 2018-04-20T00:00:00+00:00 7 |
| LAST_EDITE | category | 2 | 6 | SDE 1.0K |
| LAST_EDITED_DATE | empty | 1 | 1.0K |  |
| LAST_EDITED_USER | empty | 1 | 1.0K |  |
| LATITUDE | amount | 1.0K | 0 | 40.44555299 6; 40.39580224 6; 40.42826154 6; 40.41108826 6 |
| LOCATION | who | 234 | 0 | PENN AVE 59; E CARSON ST 46; CENTRE AVE 43; FORBES AVE 36 |
| LONGITUDE | amount | 1.0K | 0 | -80.01315039 6; -80.02297084 6; -79.97638643 6; -79.99013945 6 |
| LOT | category | 3 | 967 | Lot 58; LOT 1 |
| MAXHOURS | category | 6 | 6 | No Max 455; 2 Hours 400; 4 Hours 102; 10 Hours 47 |
| NODE | who | 62 | 0 | SOUTHSIDE 101; NORTHSIDE 91; BLOOMFIELD 68; OAKLAND3 60 |
| NODE_1 | category | 30 | 6 | SouthSide 100; Northside 94; Bloomfield 71; Uptown 69 |
| OBJECTID | id | 1.0K | 0 | 0 9; 304 6; 303 6; 302 6 |
| RATE | category | 10 | 4 | $1.50 Per Hour 510; $3 Per Hour 181; $4 Per Hour 98; $2 Per Hour 77 |
| RATE2 | category | 2 | 1.0K | $2.50 Per Hour 10 |
| RATETIMEA | category | 2 | 1.0K | ~ 8AM - 2PM 10 |
| RATETIMEB | category | 2 | 1.0K | ~ 2PM - 6PM 10 |
| RESTDATES | category | 3 | 934 | Mon - Fri 86; Fri - Sat 6 |
| RESTRICTIO | category | 7 | 935 | M-F, 7AM-9AM, 4PM-6PM 64; M-F, 7AM-9AM 18; M-F, 4PM-6PM 4; M-F, 3PM-6PM 2 |
| RESTTIME1 | category | 7 | 934 | 7AM - 9AM 79; 10PM - 2AM 5; 4PM - 6PM 4; 3PM - 6PM 2 |
| RESTTIME2 | category | 3 | 962 | 4PM - 6PM 62; 3PM - 6PM 2 |
| SERIAL_NUM | id | 1.0K | 0 | B0010X01816 6; B0010X00858 6; B0010X00725 6; B0010P00519 6 |
| SIM_NUMBER | category | 2 | 0 | 9223372036854775807 1.0K; 0 5 |
| SPECIALEV | category | 3 | 6 | No 964; Yes 56 |
| TERMINAL_I | id | 1.0K | 0 | 422021-NSHORE0403 6; 419001-BROOKL0502 6; 415344-S21ST0002 6; 427006-BVILLE0504 6 |
| TERMINAL_S | who | 1 | 0 | Active 1.0K |
| TIME1 | category | 3 | 6 | ~ 8AM - 6PM 955; ~ 8AM - 10PM 65 |
| TIME2 | category | 3 | 918 | ~ 8AM - 12AM 99; ~ 8AM - 10PM 9 |
| GEOMETRY | id | 1.0K | 0 | POINT (583687.51147623639 6; POINT (582915.75995460397 6; POINT (586827.50184693525 6; POINT (585682.67153834050 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:48:57.69299 1.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 2f70a140-6da5-4e1e-8808-e 1.0K |
| SRC_SHA256 | who | 1 | 0 | bdd953b057dbd69a120c9fa39 1.0K |
