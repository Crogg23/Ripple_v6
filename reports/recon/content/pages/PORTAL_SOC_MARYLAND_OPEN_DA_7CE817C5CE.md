# PORTAL_SOC_MARYLAND_OPEN_DA_7CE817C5CE

rows 64  columns 17  scan 3.2s

roles: audit 2, category 3, date 1, other 6, who 6

## when

INGESTED_AT
  2026        64  ##############################

## who

FACILITY_NAME by rows
         1  MERCY MEDICAL CENTER INC
         1  WESTERN MARYLAND CENTER
         1  ADVENTIST HEALTHCARE BEHAVIORAL HEALTH & WELLNESS
         1  ADVENTIST HEALTHCARE WASHINGTON ADVENTIST HOSPITAL
         1  GARRETT COUNTY MEMORIAL HOSPITAL
         1  THOMAS B FINAN CENTER
         1  DEER'S HEAD CENTER
         1  EASTERN SHORE HOSPITAL CENTER
         1  UNIVERSITY OF MARYLAND ST JOSEPH MEDICAL CENTER
         1  SPRING GROVE HOSPITAL CENTER
         1  SAINT LUKE INSTITUTE
         1  CLIFTON T PERKINS HOSPITAL CENTER
         1  UNIVERSITY OF M D UPPER CHESAPEAKE MEDICAL CENTER
         1  MEDSTAR HARBOR HOSPITAL
         1  JOHNS HOPKINS HOSPITAL, THE
         1  CARROLL HOSPITAL CENTER
         1  CALVERT MEMORIAL HOSPITAL
         1  MERITUS MEDICAL CENTER
         1  MEDSTAR SOUTHERN MARYLAND HOSPITAL CENTER
         1  KENNEDY KRIEGER INSTITUTE

FACILITY_CONTACT by rows
         3  KENNETH KOZEL
         2  BRADLEY CHAMBERS
         2  CHRISTINE WRAY
         2  LYLE SHELDON
         2  MOHAN SUNTHA
         1  ISHMAEL GAMA
         1  JOSEPH ROSS
         1  THOMAS KLEINHANZL
         1  VICTORIA BAYLESS
         1  AMY PERRY
         1  STEVEN SNELGROVE
         1  KEVIN YOUNG
         1  CHERYL HEILMAN
         1  REDONDA MILLER
         1  DOUG RYDER
         1  NEIL MOORE
         1  HARSH TRIVEDI
         1  BRIAN WHITE
         1  BARRY EISENBERG
         1  MARY BETH WAIDE

FACILITY_ADDRESS by rows
         1  315 DEER'S HEAD HOSPITAL ROAD
         1  2001 MEDICAL PARKWAY
         1  301 SAINT PAUL PLACE
         1  6701 NORTH  CHARLES STREET
         1  5401 OLD COURT ROAD
         1  1500 PENNSYLVANIA AVENUE
         1  3001 SOUTH  HANOVER STREET
         1  8118 GOOD LUCK ROAD
         1  500 UPPER CHESAPEAKE DRIVE
         1  11711 LIVINGSTON ROAD
         1  251 NORTH  FOURTH STREET
         1  8450 DORSEY RUN ROAD
         1  13215  BROOK LANE DRIVE
         1  7300 VAN DUSEN ROAD
         1  900 CATON AVENUE
         1  9901 MEDICAL CENTER DRIVE
         1  5 GARRETT AVENUE
         1  220 TILGHMAN ROAD
         1  400 WEST SEVENTH ST
         1  301 HOSPITAL DRIVE

FACILITY_PHONE by rows
         2  (443) 643-3303
         1  (410) 778-7668
         1  (443) 481-1307
         1  (410) 724-3001
         1  (410) 402-7455
         1  (301) 618-2000
         1  (410) 362-3000
         1  (240) 313-9500
         1  (301) 891-5651
         1  (410) 601-5131
         1  (410) 970-7000
         1  (301) 733-0330
         1  (410) 595-1967
         1  (410) 337-1000
         1  (240) 964-8001
         1  (301) 896-2576
         1  (410) 448-6701
         1  (240) 826-6517
         1  (240) 864-6005
         1  (410) 328-8667

## who x when

FACILITY_NAME by INGESTED_AT  LOAD STAMP, not an event date
  ADVENTIST HEALTHCARE BEHAVIORAL HEALTH &  2026:1
  ADVENTIST HEALTHCARE WASHINGTON ADVENTIS  2026:1
  CALVERT MEMORIAL HOSPITAL                 2026:1
  CARROLL HOSPITAL CENTER                   2026:1
  CLIFTON T PERKINS HOSPITAL CENTER         2026:1
  DEER'S HEAD CENTER                        2026:1
  EASTERN SHORE HOSPITAL CENTER             2026:1
  GARRETT COUNTY MEMORIAL HOSPITAL          2026:1
  JOHNS HOPKINS HOSPITAL, THE               2026:1
  KENNEDY KRIEGER INSTITUTE                 2026:1
  MEDSTAR HARBOR HOSPITAL                   2026:1
  MEDSTAR SOUTHERN MARYLAND HOSPITAL CENTE  2026:1
  MERCY MEDICAL CENTER INC                  2026:1
  MERITUS MEDICAL CENTER                    2026:1
  SAINT LUKE INSTITUTE                      2026:1
  SPRING GROVE HOSPITAL CENTER              2026:1
  THOMAS B FINAN CENTER                     2026:1
  UNIVERSITY OF M D UPPER CHESAPEAKE MEDIC  2026:1
  UNIVERSITY OF MARYLAND ST JOSEPH MEDICAL  2026:1
  WESTERN MARYLAND CENTER                   2026:1

FACILITY_CONTACT by INGESTED_AT  LOAD STAMP, not an event date
  AMY PERRY                                 2026:1
  BARRY EISENBERG                           2026:1
  BRADLEY CHAMBERS                          2026:2
  BRIAN WHITE                               2026:1
  CHERYL HEILMAN                            2026:1
  CHRISTINE WRAY                            2026:2
  DOUG RYDER                                2026:1
  HARSH TRIVEDI                             2026:1
  ISHMAEL GAMA                              2026:1
  JOSEPH ROSS                               2026:1
  KENNETH KOZEL                             2026:3
  KEVIN YOUNG                               2026:1
  LYLE SHELDON                              2026:2
  MARY BETH WAIDE                           2026:1
  MOHAN SUNTHA                              2026:2
  NEIL MOORE                                2026:1
  REDONDA MILLER                            2026:1
  STEVEN SNELGROVE                          2026:1
  THOMAS KLEINHANZL                         2026:1
  VICTORIA BAYLESS                          2026:1

## what

COUNTY: BALTIMORE CITY 28%, MONTGOMERY COUNTY 15%, BALTIMORE COUNTY 11%, PRINCE GEORGE'S COUNTY 11%, DORCHESTER COUNTY 6%, WICOMICO COUNTY 6%, WASHINGTON COUNTY 6%, HARFORD COUNTY 4%, HOWARD COUNTY 4%, CARROLL COUNTY 4%, ALLEGANY COUNTY 4%, ANNE ARUNDEL COUNTY 4%

FACILITY_CITY: BALTIMORE 46%, CAMBRIDGE 8%, SALISBURY 8%, ROCKVILLE 8%, HAGERSTOWN 8%, SILVER SPRING 5%, CUMBERLAND 5%, BEL AIR 3%, RANDALLSTOWN 3%, GERMANTOWN 3%, COLUMBIA 3%, TOWSON 3%

TYPE: Acute, General and Special Hos 75%, Psychiatric Hospital 16%, Children Hospital 3%, Rehabilitation Hospital 3%, Geriatric Care Hospital 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| THE_GEOM | other | 65 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| OBJECTID | other | 63 | 0 | 81 1; 79 1; 96 1; 100 1 |
| COUNTY | category | 22 | 0 | BALTIMORE CITY 15; MONTGOMERY COUNTY 8; BALTIMORE COUNTY 6; PRINCE GEORGE'S COUNTY 6 |
| FACILITY_NAME | who | 63 | 0 | UNIVERSITY OF MARYLAND ME 1; SINAI HOSPITAL OF BALTIMO 1; EASTERN SHORE HOSPITAL CE 1; UNIVERSITY OF M D UPPER C 1 |
| FACILITY_ADDRESS | who | 63 | 0 | 22 SOUTH  GREENE STREET 1; 2401 WEST BELVEDERE AVENU 1; POST OFFICE BOX 800 1; 500 UPPER CHESAPEAKE DRIV 1 |
| FACILITY_CITY | category | 37 | 0 | BALTIMORE 18; CAMBRIDGE 3; SALISBURY 3; ROCKVILLE 3 |
| FACILITY_STATE | other | 1 | 0 | MD 64 |
| FACILITY_ZIP | who | 53 | 0 | 21613 3; 21204 3; 20850 3; 21742 3 |
| FACILITY_PHONE | who | 63 | 0 | (443) 643-3303 2; (410) 328-8667 1; (410) 601-5131 1; (410) 221-2525 1 |
| FACILITY_CONTACT | who | 57 | 0 | KENNETH KOZEL 3; MOHAN SUNTHA 2; LYLE SHELDON 2; BRADLEY CHAMBERS 2 |
| LICENSE_CAPACITY | other | 58 | 0 | nan 3; 192 2; 87 2; 232 2 |
| LICENSE_INFO | other | 57 | 0 | Licensed from: 06/17/2016 4; Licensed from: 12/18/2015 3; Licensed from: 10/25/2014 2; Licensed from: 05/07/2016 2 |
| CCN | other | 61 | 0 | nan 4; 210002 1; 210012 1; 214002 1 |
| TYPE | category | 5 | 0 | Acute, General and Specia 48; Psychiatric Hospital 10; Children Hospital 2; Rehabilitation Hospital 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:43:23.83496 64 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0041cab7-ba2a-4825-8e27-b 64 |
| SRC_SHA256 | who | 1 | 0 | 2414c8dc6f8d7a8a19afdd17e 64 |
