# PORTAL_ARC_LA_COUNTY_OPEN_D_18EE361084

rows 126  columns 34  scan 4.1s

roles: amount 1, audit 2, category 17, date 1, empty 1, other 9, who 4

## when

INGESTED_AT
  2026       126  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCORE | 126 | 93.59 | 100 | 100 | 100 | 12.6K |

## who

CONAME by rows
         1  ST COLUMBKILLE SCHOOL
         1  61ST STREET ELEMENTARY SCHOOL
         1  BIRDIELEE V BRIGHT ELEMENTARY
         1  NATIVITY SCHOOL
         1  PARK HUERTA PRIMARY CTR
         1  CROWN PREPARATORY ACADEMY
         1  SIXTY-SIXTH STREET EARLY EDU
         1  JUST BEGINNING
         1  RICHARD MERKIN MIDDLE SCHOOL
         1  DESERT SANDS CHARTER HIGH SCH
         1  ACCELERATED CHARTER ELEMENTARY
         1  SANTEE EDUCATIONAL COMPLEX
         1  NORMANDIE CHRISTIAN SCHOOL
         1  MARY'S TENDER LOVIN CARE
         1  ASCOT AVE ELEMENTARY SCHOOL
         1  LILLIAN STREET ELEMENTARY SCH
         1  FRIDA KAHLO CONTINUATION HIGH
         1  DR MAYA ANGELOU HIGH SCHOOL
         1  WADSWORTH AVENUE ELEMENTARY
         1  49TH STREET ELEMENTARY SCHOOL

CONAME by dollars
         100        1 rows  CROWN PREPARATORY ACADEMY
         100        1 rows  CARVER MIDDLE SCHOOL
         100        1 rows  HOOPER AVE ELEMENTARY SCHOOL
         100        1 rows  JOHN MACK ELEMENTARY SCHOOL
         100        1 rows  CENTER FOR ADVANCED LEARNING
         100        1 rows  ANIMO RALPH BUNCHE CHARTER
         100        1 rows  GREATER EBENEZER ACADEMY
         100        1 rows  JEFFERSON HIGH SCHOOL
         100        1 rows  MANUAL ARTS SR HIGH SCHOOL
         100        1 rows  BILAL LEARNING CTR
         100        1 rows  TWENTIETH STREET ELEMENTARY
         100        1 rows  CALIFORNIA COLLEGIATE CHARTER
         100        1 rows  NORWOOD STREET ELEMENTARY SCH
         100        1 rows  COUNTY KIDS PLACE KINDERCARE
         100        1 rows  MARTIN LUTHER KING ELEMENTARY
         100        1 rows  NEVIN AVENUE ELEMENTARY
         100        1 rows  DR JULIAN NAVA LEARNING ACAD
         100        1 rows  WILLIAM JEFFERSON CLINTON
         100        1 rows  HOLMES AVE ELEMENTARY SCHOOL
         100        1 rows  TWENTY-FOURTH ST ELEMENTARY

STATE_NAME by rows
       126  California

STATE_NAME by dollars
       12.6K      126 rows  California

SOURCE by rows
       126  INFOGROUP

SOURCE by dollars
       12.6K      126 rows  INFOGROUP

SRC_SHA256 by rows
       126  3f5d1532b33e9fa9003a6b0868eb3156786be6ea282d2bdc42c2b3e88546fc51

SRC_SHA256 by dollars
       12.6K      126 rows  3f5d1532b33e9fa9003a6b0868eb3156786be6ea282d2bdc42c2b3e88546

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  49TH STREET ELEMENTARY SCHOOL             2026:100
  61ST STREET ELEMENTARY SCHOOL             2026:100
  ACCELERATED CHARTER ELEMENTARY            2026:100
  ANIMO RALPH BUNCHE CHARTER                2026:100
  ASCOT AVE ELEMENTARY SCHOOL               2026:100
  BILAL LEARNING CTR                        2026:100
  BIRDIELEE V BRIGHT ELEMENTARY             2026:100
  CARVER MIDDLE SCHOOL                      2026:100
  CENTER FOR ADVANCED LEARNING              2026:100
  CROWN PREPARATORY ACADEMY                 2026:100
  DESERT SANDS CHARTER HIGH SCH             2026:100
  DR MAYA ANGELOU HIGH SCHOOL               2026:100
  FRIDA KAHLO CONTINUATION HIGH             2026:100
  GREATER EBENEZER ACADEMY                  2026:100
  HOOPER AVE ELEMENTARY SCHOOL              2026:100
  JEFFERSON HIGH SCHOOL                     2026:100
  JOHN MACK ELEMENTARY SCHOOL               2026:100
  JUST BEGINNING                            2026:100
  LILLIAN STREET ELEMENTARY SCH             2026:100
  MANUAL ARTS SR HIGH SCHOOL                2026:100
  MARY'S TENDER LOVIN CARE                  2026:100
  NATIVITY SCHOOL                           2026:100
  NORMANDIE CHRISTIAN SCHOOL                2026:100
  PARK HUERTA PRIMARY CTR                   2026:100
  RICHARD MERKIN MIDDLE SCHOOL              2026:100
  SANTEE EDUCATIONAL COMPLEX                2026:100
  SIXTY-SIXTH STREET EARLY EDU              2026:100
  ST COLUMBKILLE SCHOOL                     2026:100
  TWENTIETH STREET ELEMENTARY               2026:100
  WADSWORTH AVENUE ELEMENTARY               2026:100

STATE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCORE
  California                                2026:12.6K

## what

CITY: LOS ANGELES 99%, HUNTINGTON PARK 1%

ZIP: 90011 30%, 90007 17%, 90037 16%, 90044 7%, 90018 6%, 90062 6%, 90003 5%, 90001 5%, 90089 3%, 90015 2%, 90255 1%, 90058 1%

NAICS: 61111007 88%, 62441006 12%

SIC: 821103 88%, 835102 12%

SALESVOL: 0 88%, 190 2%, 423 2%, 634 2%, 275 1%, 296 1%, 169 1%, 212 1%, 85 1%, 64 1%, 148 1%, 486 1%

HDBRCH: 2 100%

ULTNUM: 000000000 99%, 597899889 1%

FRNCOD: EKN 39%, E 13%, JN 6%, 0 6%, NS 6%, EJKP 6%, EKN0 5%, J 5%, JNS0 4%, S 4%, EKP 4%

ISCODE: D 54%, C 23%, A 18%, B 5%

SQFTCODE: 8 33%, 7 25%, 4 10%, 5 9%, 6 8%, 1 6%, 3 6%, 2 4%

LOC_NAME: PointAddress 79%, StreetAddress 17%, Subaddress 2%, PostalExt 1%

HALFMILETOMCDONALDS: No 64%, Yes 36%

THREEQUARTERMILETOMCDONALDS: Yes 69%, No 31%

ONEMILETOMCDONALDS: Yes 84%, No 16%

HALFMILETMOBILE: No 83%, Yes 17%

THREEQUARTERMILETMOBILE: No 67%, Yes 33%

ONEMILETMOBILE: No 52%, Yes 48%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 128 | 0 | 184 1; 183 1; 179 1; 178 1 |
| LOCNUM | other | 127 | 0 | 891455636 1; 891452260 1; 746632198 1; 746348613 1 |
| CONAME | who | 125 | 0 | ACCELERATED SCHOOL 1; TRINITY STREET SCHOOL 1; METRO CHARTER CORP 1; SIXTY FIRST STREET ELEMEN 1 |
| STREET | other | 85 | 0 | S FIGUEROA ST 5; S VERMONT AVE 5; S NORMANDIE AVE 5; S MAIN ST 4 |
| CITY | category | 2 | 0 | LOS ANGELES 125; HUNTINGTON PARK 1 |
| STATE | other | 1 | 0 | CA 126 |
| STATE_NAME | who | 1 | 0 | California 126 |
| ZIP | category | 13 | 0 | 90011 38; 90007 21; 90037 20; 90044 9 |
| ZIP4 | other | 116 | 2 | 1022 2; 2635 2; 1096 2; 2202 2 |
| NAICS | category | 2 | 0 | 61111007 111; 62441006 15 |
| SIC | category | 2 | 0 | 821103 111; 835102 15 |
| SALESVOL | category | 12 | 0 | 0 111; 190 3; 423 2; 634 2 |
| HDBRCH | category | 2 | 125 | 2 1 |
| ULTNUM | category | 2 | 0 | 000000000 125; 597899889 1 |
| PUBPRV | empty | 1 | 126 |  |
| EMPNUM | other | 53 | 0 | 9 17; 150 8; 20 6; 25 6 |
| FRNCOD | category | 28 | 27 | EKN 30; E 10; JN 5; 0 5 |
| ISCODE | category | 5 | 87 | D 21; C 9; A 7; B 2 |
| SQFTCODE | category | 8 | 0 | 8 41; 7 32; 4 12; 5 11 |
| LOC_NAME | category | 4 | 0 | PointAddress 100; StreetAddress 22; Subaddress 3; PostalExt 1 |
| STATUS | other | 1 | 0 | M 126 |
| SCORE | amount | 4 | 0 | 100.0 122; 98.59375 2; 93.59375 1; 98.859375 1 |
| SOURCE | who | 1 | 0 | INFOGROUP 126 |
| REC_TYPE | other | 1 | 0 | 0 126 |
| HALFMILETOMCDONALDS | category | 2 | 0 | No 81; Yes 45 |
| THREEQUARTERMILETOMCDONALDS | category | 2 | 0 | Yes 87; No 39 |
| ONEMILETOMCDONALDS | category | 2 | 0 | Yes 106; No 20 |
| HALFMILETMOBILE | category | 2 | 0 | No 105; Yes 21 |
| THREEQUARTERMILETMOBILE | category | 2 | 0 | No 85; Yes 41 |
| ONEMILETMOBILE | category | 2 | 0 | No 66; Yes 60 |
| GEOMETRY | other | 118 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:20:16.28591 126 |
| SOURCE_RUN_ID | audit | 1 | 0 | 8c705152-b600-4046-93c1-0 126 |
| SRC_SHA256 | who | 1 | 0 | 3f5d1532b33e9fa9003a6b086 126 |
