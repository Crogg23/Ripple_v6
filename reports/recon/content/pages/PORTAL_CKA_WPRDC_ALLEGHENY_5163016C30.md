# PORTAL_CKA_WPRDC_ALLEGHENY_5163016C30

rows 306  columns 21  scan 2.9s

roles: audit 2, category 8, date 1, other 7, who 4

## when

INGESTED_AT
  2026       306  ##############################

## who

INST_NAME by rows
         9  Kinder Care Learning Center
         4  Goddard School
         2  Eden Christian Academy
         2  Imani Christian Academy
         2  Yeshiva Achei Tmimim Schools
         2  Valley Special Needs
         2  Auberle Semi-Ind Living Prog
         2  Carnegie Mellon University Childrens School
         2  Crafton Childrens Corner
         2  Huntington Learning Center
         2  Learning Tree
         1  Assumption School
         1  Auberle
         1  Central Catholic
         1  St Edmunds Academy
         1  Bradley School
         1  Sonshine Christian Center
         1  St Anthony School Programs at St Mary
         1  Rhema Christian School
         1  Royal Oak Nursery School & Kdg

LAST_NAME by rows
         6  George
         2  Militzer
         2  Powers
         2  Smith
         2  Montgomery
         2  Westbrooks-Martin
         2  Stubenbort
         2  Styche
         2  Rosenfeld
         2  Roberts
         2  Trettel
         2  Niels
         2  Hancock
         2  Townsend
         1  Rosi
         1  Brink
         1  Quattrone
         1  Nicotra
         1  Barrett
         1  Correll

FIRST_NAME by rows
         6  Lisa
         5  Linda
         4  William
         4  Jennifer
         3  Karen
         3  Elizabeth
         3  Donna
         3  Amy
         3  Cynthia
         3  Deborah
         3  Michele
         3  Gary
         2  Keisha
         2  Ronald
         2  John
         2  Barbara
         2  Janet
         2  Jessica
         2  Sharon
         2  Carol

SRC_SHA256 by rows
       306  a3516daca07acd883c1317f7a8490c5f6334239fe147c541bc8fe3b56d6e4117

## who x when

INST_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Assumption School                         2026:1
  Auberle                                   2026:1
  Auberle Semi-Ind Living Prog              2026:2
  Bradley School                            2026:1
  Carnegie Mellon University Childrens Sch  2026:2
  Central Catholic                          2026:1
  Crafton Childrens Corner                  2026:2
  Eden Christian Academy                    2026:2
  Goddard School                            2026:4
  Huntington Learning Center                2026:2
  Imani Christian Academy                   2026:2
  Kinder Care Learning Center               2026:9
  Learning Tree                             2026:2
  Rhema Christian School                    2026:1
  Royal Oak Nursery School & Kdg            2026:1
  Sonshine Christian Center                 2026:1
  St Anthony School Programs at St Mary     2026:1
  St Edmunds Academy                        2026:1
  Valley Special Needs                      2026:2
  Yeshiva Achei Tmimim Schools              2026:2

LAST_NAME by INGESTED_AT  LOAD STAMP, not an event date
  Barrett                                   2026:1
  Brink                                     2026:1
  Correll                                   2026:1
  George                                    2026:6
  Hancock                                   2026:2
  Militzer                                  2026:2
  Montgomery                                2026:2
  Nicotra                                   2026:1
  Niels                                     2026:2
  Powers                                    2026:2
  Quattrone                                 2026:1
  Roberts                                   2026:2
  Rosenfeld                                 2026:2
  Rosi                                      2026:1
  Smith                                     2026:2
  Stubenbort                                2026:2
  Styche                                    2026:2
  Townsend                                  2026:2
  Trettel                                   2026:2
  Westbrooks-Martin                         2026:2

## what

CATEGORY: Nonpublic, Non-Licensed School 36%, Other Private, Non-Licensed En 36%, Licensed, Private Academic Sch 24%, Approved Private School 5%

IU: Allegheny IU 3 77%, Pittsburgh-Mt Oliver IU 2 23%

LOCATION_CITY: Pittsburgh 74%, Wexford 5%, Monroeville 3%, Sewickley 3%, Mc Keesport 2%, Gibsonia 2%, Allison Park 2%, Munhall 2%, Glenshaw 2%, Bridgeville 2%, Bethel Park 2%, West Mifflin 2%

LOCATION_STATE: PA 99%, Pa 1%

TITLE: Principal 55%, Director 44%, Executive Director 1%

SALUTATION: Ms 56%, Mr 16%, Mrs 16%, Sr 7%, Dr 2%, Rabbi 1%, Miss 1%, Br 1%, Pr 1%

MIDDLE_INIT: L 25%, J 14%, M 12%, A 10%, B 8%, E 7%, C 5%, K 5%, N 5%, S 4%, R 4%

ADMIN_PHO_1: 225 50%, 370 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | other | 305 | 0 | 306 2; 305 2; 304 2; 303 2 |
| AU_NUMBER | other | 298 | 0 | 300029890 2; 300029998 2; 300028780 2; 300029960 2 |
| INST_NAME | who | 285 | 0 | Kinder Care Learning Cent 9; Goddard School 4; Yeshiva Achei Tmimim Scho 3; Valley Special Needs 3 |
| CATEGORY | category | 4 | 0 | Nonpublic, Non-Licensed S 110; Other Private, Non-Licens 109; Licensed, Private Academi 73; Approved Private School 14 |
| IU | category | 3 | 1 | Allegheny IU 3 235; Pittsburgh-Mt Oliver IU 2 70 |
| PHONE_NUMBER | other | 222 | 71 | (724)940-9020 6; (412)422-7300 3; (412)741-1800 3; (412)255-1293 2 |
| LOCATION_ADDRESS | other | 292 | 0 | 900 Agnew Rd 3; 305 Wood Street 2; 7921 Frankstown Ave 2; 2281 Rochester Rd 2 |
| LOCATION_CITY | category | 41 | 0 | Pittsburgh 192; Wexford 12; Monroeville 9; Sewickley 8 |
| LOCATION_STATE | category | 2 | 0 | PA 304; Pa 2 |
| LOCATION_ZIP_CODE | other | 62 | 0 | 15221 20; 15213 14; 15206 14; 15090 12 |
| LOCATION_1 | other | 159 | 0 | 0 141; 1402 3; 1458 2; 1304 2 |
| TITLE | category | 4 | 107 | Principal 110; Director 88; Executive Director 1 |
| SALUTATION | category | 10 | 154 | Ms 85; Mr 24; Mrs 24; Sr 11 |
| FIRST_NAME | who | 146 | 107 | Lisa 6; Linda 5; William 4; Jennifer 4 |
| MIDDLE_INIT | category | 18 | 224 | L 18; J 10; M 9; A 7 |
| LAST_NAME | who | 181 | 107 | George 6; Rosenfeld 2; Niels 2; Townsend 2 |
| ADMIN_PHONE | other | 83 | 217 | (412)341-3256 2; (412)321-6995 2; (412)751-4250 2; (412)224-3552 2 |
| ADMIN_PHO_1 | category | 3 | 304 | 225 1; 370 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:39:14.05563 306 |
| SOURCE_RUN_ID | audit | 1 | 0 | d3048b92-8c70-4b22-bea7-7 306 |
| SRC_SHA256 | who | 1 | 0 | a3516daca07acd883c1317f7a 306 |
