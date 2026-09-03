# PORTAL_CKA_ANALYZE_BOSTON_F059843BA0

rows 7.0K  columns 46  scan 5.8s

roles: amount 5, audit 2, category 14, date 2, empty 15, id 1, other 6, who 2

## when

INSTALLED_ON
  2017      7.0K  ##############################

INGESTED_AT
  2026      7.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LONGITUDE | 7.0K | -71.15 | -71.07 | -71.04 | -71.04 | -494.2K |
| LATITUDE | 7.0K | 42.33 | 42.35 | 42.37 | 42.38 | 294.5K |
| BASE_RATE | 7.0K | 0.25 | 0.25 | 0.25 | 2 | 1.7K |
| POINT_X | 7.0K | -71.15 | -71.07 | -71.04 | -71.04 | -494.2K |
| POINT_Y | 7.0K | 42.33 | 42.35 | 42.37 | 42.38 | 294.5K |

## who

STREET by rows
       721  COMMONWEALTH AV
       482  BEACON ST
       243  TREMONT ST
       221  HARRISON AV
       219  WASHINGTON ST
       175  BAY STATE RD
       174  CHARLES ST
       151  HUNTINGTON AV
       146  BERKELEY ST
       143  D STREET
       135  SUMMER ST
       131  BOYLSTON ST
       108  COLUMBUS AV
       102  STUART ST
        96  ALBANY ST
        89  CLARENDON ST
        87  CAMBRIDGE ST
        82  DARTMOUTH ST
        77  CHESTNUT HILL AV
        76  BROOKLINE AV

STREET by dollars
      -71.05        1 rows  CONGRESS ST D-A
      -71.05        1 rows  BROAD ST C-S
      -71.05        1 rows  BROAD ST S-F
      -71.05        1 rows  BROAD ST S-W
      -71.05        1 rows  BROAD ST C-M
      -71.05        1 rows  BROAD ST F-W
      -71.05        1 rows  BROAD ST F-C
      -71.06        1 rows  LOMASNEY WY N-S
      -71.06        1 rows  STANIFORD ST O-C
      -71.06        1 rows  TREMONT ST TP-W
      -71.06        1 rows  STANIFORD ST L-O
      -71.06        1 rows  TREMONT ST W-TP
      -71.07        1 rows  BERKELEY ST ST J-B
      -71.07        1 rows  BERKELEY ST B-N
      -71.08        1 rows  DARTMOUTH ST B-N
      -71.09        1 rows  BOYLSTON ST ST C-D
      -71.09        1 rows  BOYLSTON ST M-H
     -142.10        2 rows  BROAD ST M-C
     -142.10        2 rows  BROAD ST
     -142.12        2 rows  TREMONT ST W-A

SRC_SHA256 by rows
      7.0K  c6ae8bb8f38eb545a3790cae21ae9b3cbc271cf217bfa7e971dddb36bc599a1f

SRC_SHA256 by dollars
     -494.2K     7.0K rows  c6ae8bb8f38eb545a3790cae21ae9b3cbc271cf217bfa7e971dddb36bc59

## who x when

STREET by INSTALLED_ON, dollars = LONGITUDE
  ALBANY ST                                 2017:-6.8K
  BAY STATE RD                              2017:-12.4K
  BEACON ST                                 2017:-34.3K
  BERKELEY ST                               2017:-10.4K
  BOYLSTON ST                               2017:-9.3K
  BROAD ST C-M                              2017:-71.05
  BROAD ST C-S                              2017:-71.05
  BROAD ST F-C                              2017:-71.05
  BROAD ST F-W                              2017:-71.05
  BROAD ST S-F                              2017:-71.05
  BROAD ST S-W                              2017:-71.05
  BROOKLINE AV                              2017:-5.4K
  CAMBRIDGE ST                              2017:-6.2K
  CHARLES ST                                2017:-12.4K
  CHESTNUT HILL AV                          2017:-5.5K
  CLARENDON ST                              2017:-6.3K
  COLUMBUS AV                               2017:-7.7K
  COMMONWEALTH AV                           2017:-51.3K
  CONGRESS ST D-A                           2017:-71.05
  D STREET                                  2017:-10.2K
  DARTMOUTH ST                              2017:-5.8K
  HARRISON AV                               2017:-15.7K
  HUNTINGTON AV                             2017:-10.7K
  LOMASNEY WY N-S                           2017:-71.06
  STANIFORD ST O-C                          2017:-71.06
  STUART ST                                 2017:-7.2K
  SUMMER ST                                 2017:-9.6K
  TREMONT ST                                2017:-17.3K
  TREMONT ST TP-W                           2017:-71.06
  WASHINGTON ST                             2017:-15.6K

SRC_SHA256 by INSTALLED_ON, dollars = LONGITUDE
  c6ae8bb8f38eb545a3790cae21ae9b3cbc271cf2  2017:-494.2K

## what

VENDOR: IPS 98%, Parkeon 2%

PAY_POLICY: 08:00AM-08:00PM MON-SAT $0.25  40%, 08:00AM-06:00PM MON-SAT $0.25  39%, 08:00AM-06:00PM MON-SAT $0.25  12%, 08:00AM-06:00PM MON-FRI $0.25  4%, 08:00AM-08:00PM MON-SAT $0.25  1%, 10:00AM-06:00PM MON-SAT $0.25  1%, 08:00AM-04:00PM MON-FRI $0.25  1%, 08:00AM-08:00PM MON-SAT $0.25  1%, 08:00AM-08:00PM SAT $0.25 120, 1%, 09:00AM-05:00PM MON-SAT $0.25  0%, 08:00AM-06:00PM SAT $0.25 120, 0%, 11:00AM-08:00PM MON-SAT $0.25  0%

PARK_NO_PAY: 00:00AM-24:00AM SUN, 00:00AM-0 51%, 00:00AM-24:00AM SUN, 00:00AM-0 42%, 00:00AM-24:00AM SUN, 00:00AM-0 4%, 00:00AM-24:00AM SUN, 00:00AM-1 1%, 00:00AM-24:00AM SUN, 00:00AM-0 1%, 00:00AM-24:00AM SUN, 00:00AM-0 1%, 00:00AM-24:00AM SUN, 00:00AM-0 0%, 00:00AM-24:00AM SUN, 00:00AM-0 0%, 00:00AM-24:00AM SUN, 00:00AM-1 0%, 00:00AM-24:00AM SUN, 00:00AM-0 0%, 00:00AM-24:00AM SUN, 00:00AM-0 0%, 00:00AM-24:00AM SUN, 00:00AM-0 0%

TOW_AWAY: 04:00PM-06:00PM MON-FRI 100%

DIR: W 26%, S 25%, N 25%, E 24%, s 0%

LOCK: 1 100%, 0 0%

TRAVEL_DIRECTION: S 100%

NUMBEROFSPACES: 1 100%

METER_TYPE: SINGLE-SPACE 98%, MULTI-SPACE STALL 2%

HAS_SENSOR: NO 100%

G_DISTRICT: DISTRICT 0 100%, DISTRICT 1 0%

G_SUBZONE: 0DD 11%, 0DF 10%, 0DA 9%, 0AD 9%, 0KE 8%, 0FB 8%, 0BD 8%, 0ED 8%, 0EE 7%, 0KB 7%, 0FE 7%, 0CD 7%

METER_STATE: ACTIVE 100%

SPACE_STATE: ACTIVE 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| METER_ID | other | 126 | 6.8K | 450703 1; 450702 1; 450701 1; 450700 1 |
| VENDOR | category | 3 | 1 | IPS 6.8K; Parkeon 124 |
| PAY_POLICY | category | 29 | 2 | 08:00AM-08:00PM MON-SAT $ 2.7K; 08:00AM-06:00PM MON-SAT $ 2.7K; 08:00AM-06:00PM MON-SAT $ 855; 08:00AM-06:00PM MON-FRI $ 253 |
| PRE_PAY | empty | 1 | 7.0K |  |
| PARK_NO_PAY | category | 21 | 2 | 00:00AM-24:00AM SUN, 00:0 3.5K; 00:00AM-24:00AM SUN, 00:0 2.9K; 00:00AM-24:00AM SUN, 00:0 253; 00:00AM-24:00AM SUN, 00:0 52 |
| GREEN_DOME | empty | 1 | 7.0K |  |
| TOW_AWAY | category | 2 | 6.9K | 04:00PM-06:00PM MON-FRI 54 |
| STREET_CLEANING | empty | 1 | 7.0K |  |
| DIR | category | 6 | 3 | W 1.8K; S 1.7K; N 1.7K; E 1.7K |
| BLK_NO | other | 280 | 1 | COMM 311; MASS 227; CHAR 206; BEAC 169 |
| STREET | who | 190 | 1 | COMMONWEALTH AV 721; BEACON ST 482; TREMONT ST 243; HARRISON AV 221 |
| LOCK | category | 3 | 1 | 1 6.9K; 0 14 |
| LOCK_2 | empty | 1 | 7.0K |  |
| LONGITUDE | amount | 6.7K | 1 | -71.111529000000004 35; -71.111643000000001 35; -71.111756999999997 35; -71.111870999999994 35 |
| LATITUDE | amount | 5.8K | 1 | 42.348014999999997 36; 42.348000999999996 36; 42.348007000000003 36; 42.348013000000002 36 |
| TRAVEL_DIRECTION | category | 2 | 7.0K | S 2 |
| FROM_INTERSECTION | empty | 1 | 7.0K |  |
| TO_INTERSECTION | empty | 1 | 7.0K |  |
| SPACE_NUMBER | other | 125 | 6.8K | 703 1; 702 1; 701 1; 700 1 |
| NUMBEROFSPACES | category | 2 | 1 | 1 7.0K |
| METER_TYPE | category | 3 | 1 | SINGLE-SPACE 6.8K; MULTI-SPACE STALL 124 |
| HAS_SENSOR | category | 2 | 1 | NO 7.0K |
| G_DISTRICT | category | 3 | 15 | DISTRICT 0 6.9K; DISTRICT 1 12 |
| G_PASSPORT_ZONES | other | 585 | 6.4K | 833 3; 869 3; 868 3; 867 3 |
| G_PM_ZONE | other | 188 | 6.8K | 862 1; 850 1; 849 1; 817 1 |
| G_SUBZONE | category | 46 | 15 | 0DD 282; 0DF 268; 0DA 241; 0AD 224 |
| G_ZONE | other | 52 | 15 | DD 271; DF 268; DA 241; KE 224 |
| BASE_RATE | amount | 6 | 3 | 0.250000000000000 6.9K; 0.260000000000000 2; 1.250000000000000 1; 0.500000000000000 1 |
| POLE_MOUNT | empty | 1 | 7.0K |  |
| YOKE | empty | 1 | 7.0K |  |
| HOUSING_TYPE | empty | 1 | 7.0K |  |
| HOUSING_MANUFACTURER | empty | 1 | 7.0K |  |
| SIDEWALKGE | empty | 1 | 7.0K |  |
| COIN_SLOTLE | empty | 1 | 7.0K |  |
| METER_CONDITION | empty | 1 | 7.0K |  |
| PERMIT_RATE | empty | 1 | 7.0K |  |
| INSTALLED_ON | date | 3 | 1 | 4/1/2017 1:00:00 AM 6.7K; 1/1/2017 12:00:00 AM 264 |
| PURCHASED_DATE | empty | 1 | 7.0K |  |
| METER_STATE | category | 2 | 1 | ACTIVE 7.0K |
| SPACE_STATE | category | 2 | 1 | ACTIVE 7.0K |
| SHAPE_WKT | id | 7.0K | 0 | POINT EMPTY 35; POINT (-71.11152899999996 35; POINT (-71.11164299999995 35; POINT (-71.11175699899996 35 |
| POINT_X | amount | 6.6K | 1 | -71.111528999999962 35; -71.111642999999958 35; -71.111756998999965 35; -71.111870999999951 35 |
| POINT_Y | amount | 5.7K | 1 | 42.348015000000032 36; 42.348001000000068 36; 42.348007000000052 36; 42.348013000000037 36 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:12:01.37556 7.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9fe95e07-4c75-4e06-822e-4 7.0K |
| SRC_SHA256 | who | 1 | 0 | c6ae8bb8f38eb545a3790cae2 7.0K |
