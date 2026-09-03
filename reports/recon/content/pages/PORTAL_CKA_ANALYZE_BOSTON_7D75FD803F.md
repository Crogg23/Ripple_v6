# PORTAL_CKA_ANALYZE_BOSTON_7D75FD803F

rows 134  columns 18  scan 3.7s

roles: amount 2, audit 2, category 5, date 1, other 6, who 3

## when

INGESTED_AT
  2026       134  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POINT_X | 134 | -71.17 | -71.08 | -71.02 | -71 | -9.5K |
| POINT_Y | 134 | 42.23 | 42.32 | 42.39 | 42.39 | 5.7K |

## who

SCH_NAME by rows
         2  Eliot K-8
         2  Kennedy Health Careers Academy
         1  Madison Park High
         1  Adams Elementary
         1  Higginson/Lewis K-8
         1  Mozart Elementary
         1  Mather Elementary
         1  McKinley Prep High Sch
         1  Newcomers Academy
         1  Another Course to College
         1  Lyon, Mary 9-12
         1  Boston Green Academy
         1  East Boston High
         1  Lyon K-8
         1  Comm Acad Sci Health
         1  Murphy K-8
         1  McCormack Middle
         1  Russell Elementary
         1  Curley Upper (6-8)
         1  Snowden International

SCH_NAME by dollars
         -71        1 rows  Guild Elementary
      -71.01        1 rows  Bradley Elementary
      -71.03        1 rows  Otis Elementary
      -71.03        1 rows  Perry K-8
      -71.03        1 rows  East Boston High
      -71.03        1 rows  East Boston EEC
      -71.03        1 rows  Adams Elementary
      -71.03        1 rows  McKay K-8
      -71.03        1 rows  Kennedy Patrick Elem
      -71.04        1 rows  Tynan Elementary
      -71.04        1 rows  McCormack Middle
      -71.04        1 rows  Umana/ Alighieri K-8
      -71.04        1 rows  Dever Elementary
      -71.04        1 rows  O'Donnell Elementary
      -71.04        1 rows  Alighieri Montessori
      -71.04        1 rows  Excel High
      -71.05        1 rows  UP Academy
      -71.05        1 rows  Perkins Elementary
      -71.05        1 rows  Murphy K-8
      -71.05        1 rows  Condon Elementary

BLDG_NAME by rows
         2  Dorchester Ed. Bldg #1 - Main
         2  West Roxbury Ed. Bldg
         2  Mckinley Mackey Bldg
         2  Cleveland Bldg
         2  Hyde Park EC
         2  Taft Bldg
         2  Gavin Bldg
         2  Agassiz Building
         2  Thompson Bldg
         2  Jackson Mann Bldg
         2  Burke High School Bldg
         2  Hennigan Bldg
         1  Mozart Bldg
         1  Church Street Bldg
         1  Winship Bldg
         1  Tobin Bldg
         1  Everett Bldg
         1  Manning Bldg
         1  Mildred Avenue Bldg
         1  Marshall Bldg

BLDG_NAME by dollars
         -71        1 rows  Guild Bldg
      -71.01        1 rows  Bradley Bldg


      -71.03        1 rows  Adams Bldg
      -71.03        1 rows  Kennedy, P Bldg
      -71.03        1 rows  Otis Bldg
      -71.03        1 rows  East Boston High Bldg
      -71.03        1 rows  East Boston Eec Bldg
      -71.03        1 rows  Mckay Bldg
      -71.03        1 rows  Perry Bldg
      -71.04        1 rows  Umana / Barnes Bldg
      -71.04        1 rows  Alighieri Bldg
      -71.04        1 rows  Dever Bldg
      -71.04        1 rows  Tynan Bldg
      -71.04        1 rows  Odonnell Bldg
      -71.04        1 rows  Mccormack Bldg
      -71.04        1 rows  South Boston Ed. Bldg
      -71.05        1 rows  Perkins Bldg
      -71.05        1 rows  Eliot Bldg
      -71.05        1 rows  Murphy Bldg
      -71.05        1 rows  Kenny Bldg

SRC_SHA256 by rows
       134  098c7be97f716e272739b386d6f4c50e6320a3fa30b9a9b308e162acb996843b

SRC_SHA256 by dollars
       -9.5K      134 rows  098c7be97f716e272739b386d6f4c50e6320a3fa30b9a9b308e162acb996

## who x when

SCH_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  Adams Elementary                          2026:-71.03
  Another Course to College                 2026:-71.15
  Boston Green Academy                      2026:-71.15
  Bradley Elementary                        2026:-71.01
  Comm Acad Sci Health                      2026:-71.06
  Curley Upper (6-8)                        2026:-71.11
  Dever Elementary                          2026:-71.04
  East Boston EEC                           2026:-71.03
  East Boston High                          2026:-71.03
  Eliot K-8                                 2026:-142.11
  Guild Elementary                          2026:-71
  Higginson/Lewis K-8                       2026:-71.09
  Kennedy Health Careers Academy            2026:-142.20
  Kennedy Patrick Elem                      2026:-71.03
  Lyon K-8                                  2026:-71.16
  Lyon, Mary 9-12                           2026:-71.16
  Madison Park High                         2026:-71.09
  Mather Elementary                         2026:-71.06
  McCormack Middle                          2026:-71.04
  McKay K-8                                 2026:-71.03
  McKinley Prep High Sch                    2026:-71.10
  Mozart Elementary                         2026:-71.14
  Murphy K-8                                2026:-71.05
  Newcomers Academy                         2026:-71.08
  Otis Elementary                           2026:-71.03
  Perry K-8                                 2026:-71.03
  Russell Elementary                        2026:-71.06
  Snowden International                     2026:-71.08
  Tynan Elementary                          2026:-71.04
  Umana/ Alighieri K-8                      2026:-71.04

BLDG_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = POINT_X
  Adams Bldg                                2026:-71.03
  Agassiz Building                          2026:-142.22
  Bradley Bldg

                            2026:-71.01
  Burke High School Bldg                    2026:-142.16
  Church Street Bldg                        2026:-71.07
  Cleveland Bldg                            2026:-142.12
  Dorchester Ed. Bldg #1 - Main             2026:-142.16
  East Boston Eec Bldg                      2026:-71.03
  East Boston High Bldg                     2026:-71.03
  Everett Bldg                              2026:-71.06
  Gavin Bldg                                2026:-142.10
  Guild Bldg                                2026:-71
  Hennigan Bldg                             2026:-142.22
  Hyde Park EC                              2026:-142.24
  Jackson Mann Bldg                         2026:-142.28
  Kennedy, P Bldg                           2026:-71.03
  Manning Bldg                              2026:-71.13
  Marshall Bldg                             2026:-71.07
  Mckay Bldg                                2026:-71.03
  Mckinley Mackey Bldg                      2026:-142.14
  Mildred Avenue Bldg                       2026:-71.09
  Mozart Bldg                               2026:-71.14
  Otis Bldg                                 2026:-71.03
  Perry Bldg                                2026:-71.03
  Taft Bldg                                 2026:-142.30
  Thompson Bldg                             2026:-142.16
  Tobin Bldg                                2026:-71.10
  Umana / Barnes Bldg                       2026:-71.04
  West Roxbury Ed. Bldg                     2026:-142.34
  Winship Bldg                              2026:-71.16

## what

CITY: Dorchester 22%, Roxbury 14%, Boston 12%, Jamaica Plain 9%, East Boston 8%, Brighton 6%, South Boston 5%, West Roxbury 5%, Roslindale 5%, Hyde Park 5%, Mattapan 5%, Charlestown 3%

ZIPCODE: 02119 13%, 02128 11%, 02130 11%, 02124 10%, 02121 8%, 02135 8%, 02127 7%, 02132 7%, 02131 7%, 02122 6%, 02136 6%, 02126 6%

SCH_TYPE: ES 31%, K-8 26%, HS 16%, Special 9%, 6/7-12 5%, MS 4%, K-12 4%, ELC 4%

SHARED: Shared 100%

COMPLEX: West Roxbury EC 50%, S. Boston EC 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BLDG_ID | other | 119 | 0 | 150.000000000000000 2; 139.000000000000000 2; 65.000000000000000 2; 0.000000000000000 2 |
| BLDG_NAME | who | 123 | 0 | Burke High School Bldg 2; Taft Bldg 2; Cleveland Bldg 2; Hyde Park EC 2 |
| ADDRESS | other | 123 | 0 | 60 Washington Street 2; 20 Warren Street 2; 11 Charles Street 2; 655 Metropolitan Ave 2 |
| CITY | category | 13 | 0 | Dorchester 29; Roxbury 18; Boston 16; Jamaica Plain 12 |
| ZIPCODE | category | 23 | 0 | 02119 13; 02128 11; 02130 11; 02124 10 |
| CSP_SCH_ID | other | 129 | 0 | 4381.000000000000000 2; 1440.000000000000000 2; 1260.000000000000000 1; 1470.000000000000000 1 |
| SCH_ID | other | 128 | 0 | 4381.000000000000000 2; 1440.000000000000000 2; 4272.000000000000000 2; 1260.000000000000000 1 |
| SCH_NAME | who | 132 | 0 | Eliot K-8 2; Kennedy Health Careers Ac 2; Dearborn Middle School 1; Boston Green Academy 1 |
| SCH_LABEL | other | 131 | 0 | Eliot K-8 2; Kennedy HCA 2; Dearborn MS 1; Boston Green Academy 1 |
| SCH_TYPE | category | 8 | 0 | ES 42; K-8 35; HS 21; Special 12 |
| SHARED | category | 2 | 112 | Shared 22 |
| COMPLEX | category | 3 | 132 | West Roxbury EC 1; S. Boston EC 1 |
| SHAPE_WKT | other | 130 | 0 | POINT (-71.07679086299998 2; POINT (-71.13769999999993 2; POINT (-71.17433999999997 2; POINT (-71.08091000099995 2 |
| POINT_X | amount | 126 | 0 | -71.076790862999985 2; -71.137699999999938 2; -71.174339999999972 2; -71.080910000999950 2 |
| POINT_Y | amount | 124 | 0 | 42.287783495000042 2; 42.352050000000077 2; 42.282259999000075 2; 42.281410000000051 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:34:31.95006 134 |
| SOURCE_RUN_ID | audit | 1 | 0 | 25d0a1cc-aed6-45cf-b399-c 134 |
| SRC_SHA256 | who | 1 | 0 | 098c7be97f716e272739b386d 134 |
