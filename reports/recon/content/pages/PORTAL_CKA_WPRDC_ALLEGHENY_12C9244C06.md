# PORTAL_CKA_WPRDC_ALLEGHENY_12C9244C06

rows 410  columns 35  scan 4.3s

roles: amount 2, audit 2, category 21, date 1, empty 1, other 6, who 3

## when

INGESTED_AT
  2026       410  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 410 | -8.94M | -8.90M | -8.88M | -8.87M | -3.65B |
| Y | 410 | 4.90M | 4.93M | 4.96M | 4.96M | 2.02B |

## who

SCHOOL_NAME by rows
         3  Kinder Care Learning Center
         2  William Penn El Sch
         2  Goddard School
         2  Central El Sch
         1  Crafton El Sch
         1  Penn Hills El Sch
         1  North Allegheny HS
         1  Pittsburgh Langley K-8
         1  Allegheny IU 3- Pathfinder
         1  Bellevue El Sch
         1  Montour El Sch
         1  Elizabeth Forward SHS
         1  East Union Intrmd Sch
         1  Clara Barton El Sch
         1  Deer Lakes HS
         1  Jefferson El Sch
         1  Penn Hills SHS
         1  Baldwin SHS
         1  East Allegheny JSHS
         1  Jefferson MS

SCHOOL_NAME by dollars
      -8.87M        1 rows  Plum MS
      -8.87M        1 rows  Harvest Baptist Academy
      -8.88M        1 rows  Allegheny IU 3- Sunrise
      -8.88M        1 rows  St Joseph High School
      -8.88M        1 rows  Highlands SHS
      -8.88M        1 rows  Highlands MS
      -8.88M        1 rows  University Park El Sch
      -8.88M        1 rows  Greater Works Christian School
      -8.88M        1 rows  Highlands Early Childhood Center
      -8.88M        1 rows  Spectrum CS
      -8.88M        1 rows  Learning Tree
      -8.88M        1 rows  Ramsey El Sch
      -8.88M        1 rows  Forbes Road CTC
      -8.88M        1 rows  Gateway SHS
      -8.88M        1 rows  Holiday Park Intermediate Sch
      -8.88M        1 rows  Dr Cleveland Stewart Jr El Sch
      -8.88M        1 rows  Pivik El Sch
      -8.88M        1 rows  Highlands El Sch
      -8.88M        1 rows  O'Block El Sch
      -8.88M        1 rows  Gateway MS

LEA_AUN by rows
        53  102027451
        11  103026852
        10  103026402
         8  103021252
         7  103028302
         7  103026343
         6  103023912
         6  103021003
         6  103026902
         6  103024102
         6  103023153
         6  103029203
         5  103027503
         5  103029403
         5  103025002
         5  103029902
         5  103029553
         5  103024603
         4  103027753
         4  103021752

LEA_AUN by dollars
      -8.87M        1 rows  207652255
      -8.88M        1 rows  203026785
      -8.88M        1 rows  203022945
      -8.88M        1 rows  103023410
      -8.88M        1 rows  300025414
      -8.88M        1 rows  103023807
      -8.88M        1 rows  203029188
      -8.88M        1 rows  203025785
      -8.88M        1 rows  203026685
      -8.88M        1 rows  103024162
      -8.88M        1 rows  303022278
      -8.88M        1 rows  303020076
      -8.88M        1 rows  102023030
      -8.88M        1 rows  203021385
      -8.88M        1 rows  203020255
      -8.88M        1 rows  103028425
      -8.88M        1 rows  203024715
      -8.88M        1 rows  115220003
      -8.88M        1 rows  103020005
      -8.89M        1 rows  203025485

SRC_SHA256 by rows
       410  43a77abe3c1b1f5af8c219d02e3bc5a0d23fdba528acb59bf32ae08fe9a8abe1

SRC_SHA256 by dollars
      -3.65B      410 rows  43a77abe3c1b1f5af8c219d02e3bc5a0d23fdba528acb59bf32ae08fe9a8

## who x when

SCHOOL_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  Allegheny IU 3- Pathfinder                2026:-8.91M
  Allegheny IU 3- Sunrise                   2026:-8.88M
  Baldwin SHS                               2026:-8.90M
  Bellevue El Sch                           2026:-8.91M
  Central El Sch                            2026:-17.78M
  Clara Barton El Sch                       2026:-8.90M
  Crafton El Sch                            2026:-8.91M
  Deer Lakes HS                             2026:-8.89M
  East Allegheny JSHS                       2026:-8.88M
  East Union Intrmd Sch                     2026:-8.89M
  Elizabeth Forward SHS                     2026:-8.89M
  Goddard School                            2026:-17.83M
  Greater Works Christian School            2026:-8.88M
  Harvest Baptist Academy                   2026:-8.87M
  Highlands Early Childhood Center          2026:-8.88M
  Highlands MS                              2026:-8.88M
  Highlands SHS                             2026:-8.88M
  Jefferson El Sch                          2026:-8.91M
  Jefferson MS                              2026:-8.91M
  Kinder Care Learning Center               2026:-26.75M
  Montour El Sch                            2026:-8.92M
  North Allegheny HS                        2026:-8.91M
  Penn Hills El Sch                         2026:-8.88M
  Penn Hills SHS                            2026:-8.88M
  Pittsburgh Langley K-8                    2026:-8.91M
  Plum MS                                   2026:-8.87M
  Spectrum CS                               2026:-8.88M
  St Joseph High School                     2026:-8.88M
  University Park El Sch                    2026:-8.88M
  William Penn El Sch                       2026:-17.80M

LEA_AUN by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  102027451                                 2026:-471.86M
  103021003                                 2026:-53.44M
  103021252                                 2026:-71.28M
  103021752                                 2026:-35.67M
  103023153                                 2026:-53.35M
  103023410                                 2026:-8.88M
  103023807                                 2026:-8.88M
  103023912                                 2026:-53.34M
  103024102                                 2026:-53.27M
  103024162                                 2026:-8.88M
  103024603                                 2026:-44.48M
  103025002                                 2026:-44.51M
  103026343                                 2026:-62.45M
  103026402                                 2026:-89.03M
  103026852                                 2026:-98.00M
  103026902                                 2026:-53.47M
  103027503                                 2026:-44.46M
  103027753                                 2026:-35.67M
  103028302                                 2026:-62.33M
  103029203                                 2026:-53.49M
  103029403                                 2026:-44.64M
  103029553                                 2026:-44.50M
  103029902                                 2026:-44.45M
  203022945                                 2026:-8.88M
  203025785                                 2026:-8.88M
  203026685                                 2026:-8.88M
  203026785                                 2026:-8.88M
  203029188                                 2026:-8.88M
  207652255                                 2026:-8.87M
  300025414                                 2026:-8.88M

## what

LEA_AIU_DESCRIPTION: Allegheny IU3 75%, Pittsburgh-Mt. Oliver IU2 25%

LEA_INST_NAME: City of Pittsburgh 43%, Gateway 6%, Mt. Lebanon 6%, North Allegheny 6%, Pine-Richland 5%, Fox Chapel Area 5%, Bethel Park 5%, Woodland Hills 4%, Hampton Township 4%, Moon Area 4%, North Hills 4%, McKeesport Area 4%

CITY: Pittsburgh 68%, Monroeville 5%, Allison Park 4%, McKeesport 4%, Sewickley 3%, Gibsonia 3%, Wexford 3%, Bethel Park 3%, West Mifflin 2%, Moon Township 2%, Bridgeville 2%, Glenshaw 2%

GRADE_LIST: K,1,2,3,4,5 21%, 9,10,11,12 16%, K,1,2,3,4,5,6,7,8 16%, 6,7,8 9%, K 9%, K,1,2,3,4,5,6,7,8,9,10,11,12 7%, K,1,2,3,4 7%, K,1,2,3,4,5,6 4%, 7,8,9,10,11,12 3%, K,1,2,3 3%, K,1,2 3%, 6,7,8,9,10,11,12 2%

ELEMENTARY: 1 86%, 0 14%

SECONDARY: 0 70%, 1 30%

GRADE_K: 1 59%, 0 41%

GRADE_1: 1 56%, 0 44%

GRADE_2: 1 56%, 0 44%

GRADE_3: 1 57%, 0 43%

GRADE_4: 1 56%, 0 44%

GRADE_5: 1 52%, 0 48%

GRADE_6: 0 58%, 1 42%

GRADE_7: 0 60%, 1 40%

GRADE_8: 0 60%, 1 40%

GRADE_9: 0 72%, 1 28%

GRADE_10: 0 70%, 1 30%

GRADE_11: 0 71%, 1 29%

GRADE_12: 0 71%, 1 29%

SCHOOL_CATEGORY: SD 59%, PS 33%, CS 6%, OCCCTC 1%, IU 1%, Cyber CS 0%

SCHOOL_CATEGORY_DESCRIPTION: Public School 60%, Private School 33%, Charter School 6%, CTC 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 392 | 0 | -8896601.31 3; -8898420.9554 3; -8897029.0862 3; -8911275.3073 3 |
| Y | amount | 398 | 0 | 4930613.0313 3; 4914813.1984 3; 4932528.9736 3; 4915796.9265 3 |
| OBJECTID | other | 408 | 0 | 411 3; 410 3; 409 3; 408 3 |
| LEA_AUN | who | 210 | 0 | 102027451 53; 103026852 11; 103026402 10; 103021252 8 |
| LEA_AIU_DESCRIPTION | category | 2 | 0 | Allegheny IU3 308; Pittsburgh-Mt. Oliver IU2 102 |
| LEA_INST_NAME | category | 43 | 0 | City of Pittsburgh 107; Gateway 16; Mt. Lebanon 16; North Allegheny 16 |
| SCHOOL_NAME | who | 402 | 0 | Kinder Care Learning Cent 4; Day School 3; Easter Seals of Western a 3; DePaul Institute 3 |
| CITY | category | 49 | 0 | Pittsburgh 220; Monroeville 15; Allison Park 12; McKeesport 12 |
| STATE | other | 1 | 0 | PA 410 |
| ZIPCODE | other | 77 | 0 | 15237 16; 15206 14; 15146 14; 15108 14 |
| FULL_ADDRESS | other | 397 | 0 | 1405 Shady Avenue, Pittsb 3; 2000 Clairton Road, West  3; 6202 Alder Street, Pittsb 3; 134 E Elizabeth Street, P 3 |
| GRADE_LIST | category | 44 | 0 | K,1,2,3,4,5 72; 9,10,11,12 55; K,1,2,3,4,5,6,7,8 54; 6,7,8 30 |
| ELEMENTARY | category | 2 | 0 | 1 351; 0 59 |
| SECONDARY | category | 2 | 0 | 0 288; 1 122 |
| GRADE_K | category | 2 | 0 | 1 243; 0 167 |
| GRADE_1 | category | 2 | 0 | 1 231; 0 179 |
| GRADE_2 | category | 2 | 0 | 1 231; 0 179 |
| GRADE_3 | category | 2 | 0 | 1 232; 0 178 |
| GRADE_4 | category | 2 | 0 | 1 230; 0 180 |
| GRADE_5 | category | 2 | 0 | 1 213; 0 197 |
| GRADE_6 | category | 2 | 0 | 0 236; 1 174 |
| GRADE_7 | category | 2 | 0 | 0 245; 1 165 |
| GRADE_8 | category | 2 | 0 | 0 245; 1 165 |
| GRADE_9 | category | 2 | 0 | 0 294; 1 116 |
| GRADE_10 | category | 2 | 0 | 0 288; 1 122 |
| GRADE_11 | category | 2 | 0 | 0 290; 1 120 |
| GRADE_12 | category | 2 | 0 | 0 290; 1 120 |
| CYBER_SCHOOL | empty | 1 | 410 |  |
| LAST_EDIT_DATE | other | 404 | 0 | 2025/11/12 19:36:22.713+0 3; 2025/11/10 20:03:27.030+0 3; 2025/11/10 20:03:26.713+0 3; 2025/11/13 20:57:39.458+0 3 |
| SCHOOL_CATEGORY | category | 6 | 0 | SD 241; PS 137; CS 23; OCCCTC 5 |
| SCHOOL_CATEGORY_DESCRIPTION | category | 4 | 0 | Public School 244; Private School 137; Charter School 24; CTC 5 |
| ADDRESS | other | 391 | 0 | 1405 Shady Avenue 3; 2000 Clairton Road 3; 6202 Alder Street 3; 134 E Elizabeth Street 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:41:21.41929 410 |
| SOURCE_RUN_ID | audit | 1 | 0 | f9a94553-94ff-4d5f-889e-e 410 |
| SRC_SHA256 | who | 1 | 0 | 43a77abe3c1b1f5af8c219d02 410 |
