# PORTAL_CKA_ANALYZE_BOSTON_F5E467A238

rows 87  columns 19  scan 3.6s

roles: amount 2, audit 2, category 5, date 1, empty 1, other 6, who 3

## when

INGESTED_AT
  2026        87  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POINT_X | 87 | -71.17 | -71.08 | -71.02 | -71 | -6.2K |
| POINT_Y | 87 | 42.24 | 42.32 | 42.38 | 42.38 | 3.7K |

## who

NAME by rows
         1  Saint Joseph Preparatory High School
         1  The Advent School
         1  The Winsor School
         1  Elizabeth Seton Academy
         1  Roxbury Latin School
         1  Julie's Family Learning Program
         1  Excel Academy Charter High School
         1  Catholic Memorial
         1  MATCH Charter Public High School
         1  Roxbury Prep - Lucy Stone
         1  Youth Build Boston
         1  St Theresa Elementary
         1  The Learning Project
         1  St John Elementary
         1  The Newman School
         1  Codman Academy Charter Public School
         1  The Kingsley Montessori School
         1  Bridge Boston Charter School (K1-1)
         1  Shaloh House Jewish Day School
         1  St Mary Of Czestochowa

NAME by dollars
         -71        1 rows  Excel Academy Charter School - Orient Heights
      -71.02        1 rows  Excel Academy Charter School - East Boston
      -71.02        1 rows  Edward Brooke Charter School - East Boston
      -71.03        1 rows  South Boston Catholic Academy
      -71.04        1 rows  Excel Academy Charter High School
      -71.04        1 rows  St Peter Academy
      -71.04        1 rows  E Boston Central Catholic
      -71.05        1 rows  Pope John Paul II Academy (Neponset)
      -71.05        1 rows  Cristo Rey Boston High School
      -71.05        1 rows  Boston Collegiate Charter School (Lower School)
      -71.05        1 rows  Julie's Family Learning Program
      -71.05        1 rows  St Brendan Elementary
      -71.05        1 rows  Notre Dame Montessori
      -71.05        1 rows  Neighborhood House Charter School
      -71.05        1 rows  Seaport Campus School
      -71.05        1 rows  St John Elementary
      -71.05        1 rows  Boston College High
      -71.06        1 rows  Bridge Boston Charter School (2-4)
      -71.06        1 rows  Dorchester Collegiate Academy
      -71.06        1 rows  Boston Collegiate Charter School (Middle and High School)

TOWN by rows
        87  BOSTON

TOWN by dollars
       -6.2K       87 rows  BOSTON

SRC_SHA256 by rows
        87  a136de9a348e96edf73f04db7989106363fee540e13e33df2cccffbfaa6e56bc

SRC_SHA256 by dollars
       -6.2K       87 rows  a136de9a348e96edf73f04db7989106363fee540e13e33df2cccffbfaa6e

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  Boston Collegiate Charter School (Lower   2026:-71.05
  Bridge Boston Charter School (K1-1)       2026:-71.09
  Catholic Memorial                         2026:-71.17
  Codman Academy Charter Public School      2026:-71.07
  Cristo Rey Boston High School             2026:-71.05
  E Boston Central Catholic                 2026:-71.04
  Edward Brooke Charter School - East Bost  2026:-71.02
  Elizabeth Seton Academy                   2026:-71.07
  Excel Academy Charter High School         2026:-71.04
  Excel Academy Charter School - East Bost  2026:-71.02
  Excel Academy Charter School - Orient He  2026:-71
  Julie's Family Learning Program           2026:-71.05
  MATCH Charter Public High School          2026:-71.12
  Pope John Paul II Academy (Neponset)      2026:-71.05
  Roxbury Latin School                      2026:-71.16
  Roxbury Prep - Lucy Stone                 2026:-71.07
  Saint Joseph Preparatory High School      2026:-71.14
  Shaloh House Jewish Day School            2026:-71.15
  South Boston Catholic Academy             2026:-71.03
  St Brendan Elementary                     2026:-71.05
  St John Elementary                        2026:-71.05
  St Mary Of Czestochowa                    2026:-71.06
  St Peter Academy                          2026:-71.04
  St Theresa Elementary                     2026:-71.16
  The Advent School                         2026:-71.07
  The Kingsley Montessori School            2026:-71.08
  The Learning Project                      2026:-71.08
  The Newman School                         2026:-71.08
  The Winsor School                         2026:-71.11
  Youth Build Boston                        2026:-71.09

TOWN by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  BOSTON                                    2026:-6.2K

## what

TOWN_MAIL: Dorchester 27%, Boston 17%, Roxbury 9%, Jamaica Plain 9%, South Boston 6%, Brighton 6%, Hyde Park 6%, Mattapan 5%, East Boston 5%, West Roxbury 5%, Roslindale 3%, Charlestown 2%

ZIP: 02124 18%, 02125 11%, 02130 11%, 02119 9%, 02136 9%, 02127 8%, 02135 8%, 02126 6%, 02215 6%, 02132 6%, 02128 5%, 02121 5%

FAX: -- 69%, 617-652-7461 5%, 617-254-8909 5%, 617-445-9153 5%, 617-427-4529 2%, 617-242-0016 2%, 617-822-7527 2%, 617-275-5760 2%, 857-203-9666 2%, 617-983-0332 2%, 617-232-7925 2%

GRADES: PK,K,1,2,3,4,5,6,7,8 30%, 9,10,11,12 23%, 5,6,7,8 11%, 6,7,8 7%, PK,K,1,2,3,4,5,6 5%, 5,6,7,8,9,10,11,12 5%, K,1,2,3,4,5,6,7,8 5%, K,1,2,3,4,5,6 5%, PK,K,1,2,3,4,5,6,7,8,9,10,11,1 4%, 7,8,9,10,11,12 4%, PK, K 2%

TYPE: PRI 57%, CHA 36%, SPE 6%, COP 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | empty | 1 | 87 |  |
| SCHID | other | 84 | 3 | 8337 1; 8642 1; 8662 1; 5303 1 |
| NAME | who | 87 | 0 | St Patrick Elementary 1; Notre Dame Montessori 1; Julie's Family Learning P 1; Good Shepherd School 1 |
| ADDRESS | other | 88 | 0 | 131 Mt. Pleasant Ave 1; 265 Mt. Vernon Street 1; 133 Dorchester Street 1; 20 Winthrop Street 1 |
| TOWN_MAIL | category | 13 | 0 | Dorchester 23; Boston 15; Roxbury 8; Jamaica Plain 8 |
| TOWN | who | 1 | 0 | BOSTON 87 |
| STATE | other | 1 | 0 | MA 87 |
| ZIP | category | 23 | 0 | 02124 12; 02125 7; 02130 7; 02119 6 |
| PRINCIPAL | other | 73 | 11 | Dana Lehman 3; Mary Lanata 2; Emily Hepler 2; Robert Monahan 1 |
| PHONE | other | 75 | 7 | 617-265-0019 4; -- 2; 617-238-7300 2; 617-427-3881 1 |
| FAX | category | 49 | 8 | -- 29; 617-652-7461 2; 617-254-8909 2; 617-445-9153 2 |
| GRADES | category | 34 | 8 | PK,K,1,2,3,4,5,6,7,8 17; 9,10,11,12 13; 5,6,7,8 6; 6,7,8 4 |
| TYPE | category | 4 | 0 | PRI 50; CHA 31; SPE 5; COP 1 |
| SHAPE_WKT | other | 86 | 0 | POINT (-71.07622175799997 1; POINT (-71.04625812699998 1; POINT (-71.04723225299994 1; POINT (-71.06158977699993 1 |
| POINT_X | amount | 87 | 0 | -71.076221757999974 1; -71.046258126999987 1; -71.047232252999947 1; -71.061589776999938 1 |
| POINT_Y | amount | 88 | 0 | 42.324911816000053 1; 42.318792696000060 1; 42.334927784000058 1; 42.373785101000067 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:30:18.96362 87 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0b0585ac-e940-4436-be65-a 87 |
| SRC_SHA256 | who | 1 | 0 | a136de9a348e96edf73f04db7 87 |
