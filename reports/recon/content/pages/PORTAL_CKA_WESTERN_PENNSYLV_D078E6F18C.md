# PORTAL_CKA_WESTERN_PENNSYLV_D078E6F18C

rows 1.3K  columns 16  scan 3.4s

roles: audit 2, category 3, date 1, id 3, other 3, who 5

## when

INGESTED_AT
  2026      1.3K  ##############################

## who

USER_LOCATION_NAME by rows
         8  PLEASANT HILLS COMMUNITY PRESBY CHURCH
         6  BURCHFIELD SCH - UPPER LEVEL GYM
         5  MARKHAM ELEMENTARY SCHOOL
         5  KINGSLEY HOUSE COMMUNITY RM 
         5  FOSTER SCHOOL
         5  BALDWIN COMMUNITY UNITED METHODIST CHURCH
         5  CHRIST LUTHERAN CHURCH
         5  JULIA WARD HOWE ELEMENTARY SCHOOL
         5  LINCOLN ELEMENTARY SCHOOL
         4  JEWISH COMMUNITY CENTER - LEVINSON HALL SIDE B
         4  BALDWIN HIGH SCHOOL - GYM HALLWAY
         4  FAIRVIEW VOLUNTEER FIRE DEPT.
         4  MYRTLE ELEMENTARY SCHOOL CAFETERIA
         4  ST ALBERT THE GREAT
         4  FORT COUCH MIDDLE SCHOOL GYM
         4  QUAKER VALLEY MIDDLE SCHOOL
         4  BANKSVILLE POOL - FIRST FLOOR
         4  NEW PENN HILLS HIGH SCHOOL
         4  SHALER ELEMENTARY SCHOOL - AUDITORIUM LOBBY
         4  OAK HILL MANAGEMENT OFFICE

USER_MUNICIPALITY by rows
       402  PITTSBURGH
        50  PENN HILLS
        38  MT LEBANON
        34  SHALER
        33  ROSS
        32  MCKEESPORT
        28  BETHEL PARK
        25  MONROEVILLE
        21  WEST MIFFLIN
        21  MCCANDLESS
        21  PLUM
        18  UPPER ST CLAIR
        18  BALDWIN BORO
        18  SCOTT
        17  WILKINSBURG
        16  MOON
        16  WHITEHALL
        13  HAMPTON
        13  SOUTH PARK
        13  N VERSAILLES

USER_ADDRESS by rows
         8  199 OLD CLAIRTON RD.
         6  1500 BURCHFIELD RD
         6  12 MONONGAHELA AVE
         5  700 VERMONT AVE.
         5  6435 FRANKSTOWN AVENUE
         5  515 FORT COUCH RD.
         5  2 RALSTON PL.
         5  400 BROADMOOR AVE.
         5  5001 BAPTIST RD.
         5  165 CRESCENT DRIVE
         4  280 BURROWS ST
         4  745 NORTH NEGLEY AVE
         4  1290 MIFFLIN RD
         4  5151 MCANNULTY RD.
         4  5145 WEXFORD RUN RD.
         4  1960 EDEN PARK BLVD
         4  5738 FORBES AVE
         4  3198 SCHIECK STREET
         4  1500 BOYCE RD.
         4  1 VETERANS WAY

USER_CITY by rows
       401  PITTSBURGH
        45  PENN HILLS
        38  MT LEBANON
        34  SHALER
        33  ROSS
        32  MCKEESPORT
        28  BETHEL PARK
        24  MONROEVILLE
        21  MCCANDLESS
        21  PLUM
        21  WEST MIFFLIN
        18  BALDWIN BORO
        18  UPPER ST CLAIR
        18  SCOTT
        17  WILKINSBURG
        16  WHITEHALL
        13  HAMPTON
        13  SOUTH PARK
        13  NORTH VERSAILLES
        13  CLAIRTON

## who x when

USER_LOCATION_NAME by INGESTED_AT  LOAD STAMP, not an event date
  BALDWIN COMMUNITY UNITED METHODIST CHURC  2026:5
  BALDWIN HIGH SCHOOL - GYM HALLWAY         2026:4
  BANKSVILLE POOL - FIRST FLOOR             2026:4
  BURCHFIELD SCH - UPPER LEVEL GYM          2026:6
  CHRIST LUTHERAN CHURCH                    2026:5
  FAIRVIEW VOLUNTEER FIRE DEPT.             2026:4
  FORT COUCH MIDDLE SCHOOL GYM              2026:4
  FOSTER SCHOOL                             2026:5
  JEWISH COMMUNITY CENTER - LEVINSON HALL   2026:4
  JULIA WARD HOWE ELEMENTARY SCHOOL         2026:5
  KINGSLEY HOUSE COMMUNITY RM               2026:5
  LINCOLN ELEMENTARY SCHOOL                 2026:5
  MARKHAM ELEMENTARY SCHOOL                 2026:5
  MYRTLE ELEMENTARY SCHOOL CAFETERIA        2026:4
  NEW PENN HILLS HIGH SCHOOL                2026:4
  OAK HILL MANAGEMENT OFFICE                2026:4
  PLEASANT HILLS COMMUNITY PRESBY CHURCH    2026:8
  QUAKER VALLEY MIDDLE SCHOOL               2026:4
  SHALER ELEMENTARY SCHOOL - AUDITORIUM LO  2026:4
  ST ALBERT THE GREAT                       2026:4

USER_MUNICIPALITY by INGESTED_AT  LOAD STAMP, not an event date
  BALDWIN BORO                              2026:18
  BETHEL PARK                               2026:28
  HAMPTON                                   2026:13
  MCCANDLESS                                2026:21
  MCKEESPORT                                2026:32
  MONROEVILLE                               2026:25
  MOON                                      2026:16
  MT LEBANON                                2026:38
  N VERSAILLES                              2026:13
  PENN HILLS                                2026:50
  PITTSBURGH                                2026:402
  PLUM                                      2026:21
  ROSS                                      2026:33
  SCOTT                                     2026:18
  SHALER                                    2026:34
  SOUTH PARK                                2026:13
  UPPER ST CLAIR                            2026:18
  WEST MIFFLIN                              2026:21
  WHITEHALL                                 2026:16
  WILKINSBURG                               2026:17

## what

USER_D: 1 22%, 2 20%, 3 14%, 4 10%, 5 7%, 6 6%, 7 5%, 0 4%, 8 4%, 9 3%, 10 3%, 11 2%

USER_STATE: PA 100%

USER_W: 0 39%, 1 10%, 3 9%, 2 9%, 4 7%, 5 6%, 7 5%, 14 4%, 6 4%, 19 4%, 8 3%, 9 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.3K | 0 | 1327 7; 1326 7; 1325 7; 1324 7 |
| USER_ADDRESS | who | 788 | 0 | 199 OLD CLAIRTON RD. 12; 1500 BURCHFIELD RD 11; 809 CENTER ST 10; 5001 BAPTIST RD. 10 |
| USER_CITY | who | 133 | 10 | PITTSBURGH 401; PENN HILLS 45; MT LEBANON 38; SHALER 34 |
| USER_D | category | 42 | 0 | 1 259; 2 236; 3 163; 4 111 |
| USER_LOCATION_NAME | who | 810 | 0 | PLEASANT HILLS COMMUNITY  12; BURCHFIELD SCH - UPPER LE 11; BALDWIN COMMUNITY UNITED  10; PITTSBURGH URBAN CHRISTIA 9 |
| USER_MUNI | other | 128 | 0 | 188 402; 185 50; 173 38; 202 34 |
| USER_MUNICIPALITY | who | 130 | 0 | PITTSBURGH 402; PENN HILLS 50; MT LEBANON 38; SHALER 34 |
| USER_MWD | id | 1.3K | 0 | 1720016 7; 1720014 7; 1720015 7; 1580009 7 |
| USER_PS_NUM | id | 1.3K | 0 | 424 7; 422 7; 423 7; 296 7 |
| USER_STATE | category | 2 | 17 | PA 1.3K |
| USER_W | category | 33 | 0 | 0 423; 1 103; 3 96; 2 94 |
| USER_ZIPCODE | other | 98 | 21 | 15235 42; 15206 41; 15210 39; 15236 38 |
| GEOMETRY | other | 954 | 0 | POINT (589489.75454538408 11; POINT (584918.34328657842 10; POINT (579426.26934112375 10; POINT (596946.30054286227 9 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:53:12.36767 1.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4e27bc25-7dc2-47d0-8ee4-2 1.3K |
| SRC_SHA256 | who | 1 | 0 | 9a5754e57c6cab36714e7f969 1.3K |
