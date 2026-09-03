# PORTAL_CKA_ANALYZE_BOSTON_899BB82358

rows 572  columns 13  scan 4.0s

roles: amount 5, audit 2, category 1, date 1, other 3, who 2

## when

INGESTED_AT
  2026       572  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 572 | 42.25 | 42.36 | 42.52 | 42.53 | 24.2K |
| LONGITUDE | 572 | -71.25 | -71.09 | -70.89 | 71.04 | -40.5K |
| TOTAL_DOCKS | 572 | 9 | 17 | 35 | 53 | 10.0K |
| POINT_X | 572 | -71.25 | -71.09 | -70.89 | 71.04 | -40.5K |
| POINT_Y | 572 | 42.25 | 42.36 | 42.52 | 42.53 | 24.2K |

## who

NAME by rows
         1  Bowdoin St at Quincy St
         1  Brighton Mills - 370 Western Ave
         1  Marion St at White St
         1  Brookline Village - Station Street at MBTA
         1  Washington St at Peters Park
         1  MIT Stata Center at Vassar St / Main St
         1  Lafayette Square at Mass Ave / Main St / Columbia St
         1  Fresh Pond Reservation
         1  Porter Square Station
         1  Kennedy-Longfellow School 158 Spring St
         1  W Broadway at D St
         1  Discovery Park - 30 Acorn Park Drive
         1  Lesley University
         1  The Eddy - New St at Sumner St
         1  Bennington St at Constitution Beach
         1  Railroad Lot and Minuteman Bikeway
         1  Government Center - Cambridge St at Court St
         1  Blossom St at Charles St
         1  Tremont St at E Berkeley St
         1  Lansdowne T Stop

NAME by dollars
          53        1 rows  MIT Vassar St
          47        1 rows  South Station - 700 Atlantic Ave
          40        1 rows  Forest Hills
          37        1 rows  Nashua Street at Red Auerbach Way
          35        1 rows  MIT Stata Center at Vassar St / Main St
          35        1 rows  West End Park
          35        1 rows  Government Center - Cambridge St at Court St
          33        1 rows  Copley Square - Dartmouth St at Boylston St
          33        1 rows  Maverick Square - Lewis Mall
          32        1 rows  Boston Public Market - Surface Rd at Sudbury St
          32        1 rows  Stadium Rd at Western Ave
          32        1 rows  Nashua Street at Red Auerbach Way [Extension]
          31        1 rows  Arch St at Franklin St
          31        1 rows  JFK/UMass T Stop
          31        1 rows  Boylston St at Arlington St
          28        1 rows  Park Street T Stop - Tremont St at Park St
          27        1 rows  Washington St at Rutland St
          27        1 rows  84 Cambridgepark Dr
          27        1 rows  Lansdowne T Stop
          27        1 rows  Packard's Corner - Commonwealth Ave at Brighton Ave

SRC_SHA256 by rows
       572  efe91253a301a1864d247234555a3f35ac7a082ea0ffb778aeeb46707d0531e0

SRC_SHA256 by dollars
       10.0K      572 rows  efe91253a301a1864d247234555a3f35ac7a082ea0ffb778aeeb46707d05

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_DOCKS
  Bennington St at Constitution Beach       2026:17
  Blossom St at Charles St                  2026:15
  Boston Public Market - Surface Rd at Sud  2026:32
  Bowdoin St at Quincy St                   2026:15
  Brighton Mills - 370 Western Ave          2026:15
  Brookline Village - Station Street at MB  2026:19
  Copley Square - Dartmouth St at Boylston  2026:33
  Discovery Park - 30 Acorn Park Drive      2026:23
  Forest Hills                              2026:40
  Fresh Pond Reservation                    2026:17
  Government Center - Cambridge St at Cour  2026:35
  Kennedy-Longfellow School 158 Spring St   2026:19
  Lafayette Square at Mass Ave / Main St /  2026:15
  Lansdowne T Stop                          2026:27
  Lesley University                         2026:15
  MIT Stata Center at Vassar St / Main St   2026:35
  MIT Vassar St                             2026:53
  Marion St at White St                     2026:19
  Maverick Square - Lewis Mall              2026:33
  Nashua Street at Red Auerbach Way         2026:37
  Nashua Street at Red Auerbach Way [Exten  2026:32
  Porter Square Station                     2026:19
  Railroad Lot and Minuteman Bikeway        2026:11
  South Station - 700 Atlantic Ave          2026:47
  Stadium Rd at Western Ave                 2026:32
  The Eddy - New St at Sumner St            2026:15
  Tremont St at E Berkeley St               2026:19
  W Broadway at D St                        2026:23
  Washington St at Peters Park              2026:19
  West End Park                             2026:35

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_DOCKS
  efe91253a301a1864d247234555a3f35ac7a082e  2026:10.0K

## what

DISTRICT: Boston 57%, Cambridge 16%, Somerville 7%, Salem 3%, Newton 3%, Medford 3%, Everett 2%, Brookline 2%, Arlington 2%, Watertown 2%, Revere 1%, Malden 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NUMBER | other | 568 | 0 | S32052 3; S32019 3; S32018 3; S32017 3 |
| NAME | who | 569 | 0 | Somerville Hospital 3; Grove St at Community Pat 3; Assembly Square T 3; East Somerville Library ( 3 |
| LATITUDE | amount | 568 | 0 | 42.377369999999999 4; 42.390413000000002 3; 42.396386810000003 3; 42.392232839999998 3 |
| LONGITUDE | amount | 568 | 0 | -71.066770000000005 4; -71.108570999999998 3; -71.120113059999994 3; -71.077466009999995 3 |
| DISTRICT | category | 13 | 0 | Boston 324; Cambridge 92; Somerville 38; Salem 18 |
| PUBLIC | other | 1 | 0 | Yes 572 |
| TOTAL_DOCKS | amount | 27 | 0 | 19 175; 15 160; 11 74; 23 33 |
| SHAPE_WKT | other | 569 | 0 | POINT (-71.06676999999996 4; POINT (-71.10857099999998 3; POINT (-71.12011305999993 3; POINT (-71.07746600999996 3 |
| POINT_X | amount | 564 | 0 | -71.066769999999963 4; -71.108570999999984 3; -71.120113059999937 3; -71.077466009999966 3 |
| POINT_Y | amount | 564 | 0 | 42.377370000000042 4; 42.390413000000081 3; 42.396386810000081 3; 42.392232840000077 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:43:04.19816 572 |
| SOURCE_RUN_ID | audit | 1 | 0 | 24ffefd6-971c-40bb-91b7-3 572 |
| SRC_SHA256 | who | 1 | 0 | efe91253a301a1864d2472345 572 |
