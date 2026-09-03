# PORTAL_CKA_WESTERN_PENNSYLV_F37C7E01BF

rows 215  columns 26  scan 5.3s

roles: amount 6, audit 2, category 5, date 3, other 7, who 4

## when

LAST_EDITED_DATE
  2023       215  ##############################

CREATED_DATE
  2023       215  ##############################

INGESTED_AT
  2026       215  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENG | 196 | 24.32 | 1.4K | 77.3K | 123.3K | 894.4K |
| SQFT | 214 | 46.58 | 64.7K | 18.59M | 27.77M | 169.40M |
| DPW_AC | 214 | 0 | 1.49 | 426.78 | 637.41 | 3.9K |
| ACREAGE | 214 | 0 | 1.49 | 426.78 | 637.41 | 3.9K |
| SHAPE__AREA | 215 | 7.50 | 10.3K | 2.98M | 4.45M | 27.20M |
| SHAPE__LENGTH | 215 | 9.74 | 511.98 | 31.9K | 49.4K | 438.9K |

## who

ORIGPKNAME by rows
         1  Cowley Playground
         1  Fort Pitt Playground
         1  Southside Riverfront Park
         1  Fineview Field
         1  Niagara Parklet
         1  West Penn Park
         1  Mellon Square Park
         1  Negley Run Blvd
         1  Sheraden Monument
         1  Curto Park
         1  Fairhaven Park
         1  McGonigle Playground
         1  Arlington Playground
         1  Able Long Parklet
         1  Zulema Passive Area
         1  Liberty Avenue Island
         1  Point State Park
         1  Stratmore Parklet
         1  Granville Parklet
         1  Spring Hill Playground

ORIGPKNAME by dollars
       4.45M        1 rows  Hays Woods
       4.24M        1 rows  Frick Park
       3.04M        1 rows  Schenley Park
       2.65M        1 rows  Highland Park
       1.81M        1 rows  Riverview Park
       1.20M        1 rows  Duquesne Heights Greenway
      974.4K        1 rows  Hazelwood Park
      560.8K        1 rows  Seldom Seen Park
      544.0K        1 rows  McKinley Park
      429.5K        1 rows  East Common Park
      400.6K        1 rows  Southside Park
      391.5K        1 rows  Brookline Memorial Park
      374.3K        1 rows  Moore Park
      357.2K        1 rows  Sheraden Park
      319.6K        1 rows  Mt. Washington Park
      275.3K        1 rows  Fairhaven Park
      233.0K        1 rows  Bigelow Park
      227.7K        1 rows  Mellon Park
      224.5K        1 rows  Grandview Park
      217.1K        1 rows  Brighton Heights Park

LAST_EDITED_USER by rows
       215  pgh.dcp.allisot

LAST_EDITED_USER by dollars
      27.20M      215 rows  pgh.dcp.allisot

CREATED_USER by rows
       215  pgh.dcp.allisot

CREATED_USER by dollars
      27.20M      215 rows  pgh.dcp.allisot

SRC_SHA256 by rows
       215  9b9fc74eddd28bb5ac2d1dd45616d74265b8838caf38a4d1e4dad0150fcd14aa

SRC_SHA256 by dollars
      27.20M      215 rows  9b9fc74eddd28bb5ac2d1dd45616d74265b8838caf38a4d1e4dad0150fcd

## who x when

ORIGPKNAME by LAST_EDITED_DATE, dollars = SHAPE__AREA
  Able Long Parklet                         2023:11.6K
  Arlington Playground                      2023:29.4K
  Cowley Playground                         2023:29.6K
  Curto Park                                2023:50.5K
  Duquesne Heights Greenway                 2023:1.20M
  East Common Park                          2023:429.5K
  Fairhaven Park                            2023:275.3K
  Fineview Field                            2023:18.5K
  Fort Pitt Playground                      2023:66.4K
  Frick Park                                2023:4.24M
  Granville Parklet                         2023:3.6K
  Hays Woods                                2023:4.45M
  Hazelwood Park                            2023:974.4K
  Highland Park                             2023:2.65M
  Liberty Avenue Island                     2023:8.1K
  McGonigle Playground                      2023:36.3K
  McKinley Park                             2023:544.0K
  Mellon Square Park                        2023:9.8K
  Negley Run Blvd                           2023:6.2K
  Niagara Parklet                           2023:1.6K
  Point State Park                          2023:201.4K
  Riverview Park                            2023:1.81M
  Schenley Park                             2023:3.04M
  Seldom Seen Park                          2023:560.8K
  Sheraden Monument                         2023:1.0K
  Southside Riverfront Park                 2023:98.3K
  Spring Hill Playground                    2023:44.9K
  Stratmore Parklet                         2023:3.7K
  West Penn Park                            2023:157.7K
  Zulema Passive Area                       2023:5.1K

LAST_EDITED_USER by LAST_EDITED_DATE, dollars = SHAPE__AREA
  pgh.dcp.allisot                           2023:27.20M

## what

TYPE: NP 51%, BTF 19%, CP 11%, RP 9%, SU 6%, RVR 3%, SCH 1%, OTR 0%

MAINTENANCERESPONSIBILITY: Parks - Riverview 19%, Parks - Emerald 15%, Parks - McKinley 15%, Parks - Highland 12%, Parks - Schenley 11%, Parks - Frick 11%, 3rd Division 8%, 2nd Division 5%, 5th Division 1%, 6th Division 1%, State 0%, 1st Division 0%

SECTOR: 12 13%, 4 12%, 10 9%, 5 9%, 16 8%, 7 8%, 6 8%, 2 7%, 13 7%, 11 6%, 14 6%, 9 6%

DIVNAME: Riverview 23%, Emerald 19%, McKinley 18%, Highland 14%, Schenley 14%, Frick 12%, Northeast 1%

FINAL_CAT: Neighborhood Park 51%, Beautification Site 19%, Community Park 11%, Regional Park 9%, Special Use Park 6%, Riverfront Park 3%, Public School 1%, Other 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ORIGPKNAME | who | 200 | 14 | Joe Natoli Playground 2; Homewood Playground 2; Hazelwood Park 1; Bigelow Park 1 |
| TYPE | category | 9 | 1 | NP 109; BTF 41; CP 23; RP 19 |
| UPDATEPKNM | other | 215 | 0 | Niagara Park 2; Joe Natoli Park 2; Homewood Park 2; Hazelwood Park 2 |
| MAINTENANCERESPONSIBILITY | category | 14 | 0 | Parks - Riverview 41; Parks - Emerald 32; Parks - McKinley 32; Parks - Highland 25 |
| SHAPE_LENG | amount | 197 | 19 | 2027.25345377 1; 1360.90801945 1; 2752.13027248 1; 107319.676945 1 |
| SECTOR | category | 17 | 1 | 12 23; 4 22; 10 17; 5 17 |
| SQFT | amount | 215 | 1 | 235805.69596935 2; 185956.14072439 2; 6072921.4986122 2; 2457.02344516 2 |
| OBJECTID_1 | other | 215 | 0 | 1819 2; 1818 2; 1417 2; 1416 2 |
| LAST_EDITED_USER | who | 1 | 0 | pgh.dcp.allisot 215 |
| DIVNAME | category | 8 | 39 | Riverview 40; Emerald 33; McKinley 32; Highland 24 |
| CREATED_USER | who | 1 | 0 | pgh.dcp.allisot 215 |
| FINAL_CAT | category | 9 | 1 | Neighborhood Park 109; Beautification Site 41; Community Park 23; Regional Park 19 |
| GLOBALID_1 | other | 217 | 0 | f93b81eb-e816-4da6-8231-e 2; e621f3c0-b885-47fb-a472-a 2; 91054892-42c7-43db-ba9d-6 2; b6756676-f977-4ffe-a2b9-c 2 |
| LAST_EDITED_DATE | date | 1 | 0 | 2023-08-02T14:10:28.845Z 215 |
| OBJECTID | other | 212 | 1 | 95 2; 90 2; 414429 2; 219 2 |
| ALTERNTNAM | other | 196 | 14 | Emerald View Regional Par 7; Joe Natoli Park 1; Homewood Park 1; Hazelwood Park 1 |
| DPW_AC | amount | 217 | 1 | 5.41337555544003 2; 4.26898265728162 2; 139.415651753199 2; 5.64057225270754E-02 2 |
| ACREAGE | amount | 218 | 1 | 5.41337556 2; 4.26898266 2; 139.41565175 2; 0.05640572 2 |
| SHAPE__AREA | amount | 215 | 0 | 1590.73046875 2; 37912.6328125 2; 29871.64453125 2; 974365.86328125 2 |
| GLOBALID | other | 193 | 23 | bc75545d-28e9-4c68-b1fd-4 1; 9296bb5e-10ce-4bb7-a855-5 1; 50baa3f0-758b-4bbb-98d6-3 1; c9e4bd66-e2b3-4f4a-b49b-a 1 |
| CREATED_DATE | date | 1 | 0 | 2023-08-02T14:10:28.845Z 215 |
| SHAPE__LENGTH | amount | 211 | 0 | 159.64691586806254 2; 812.7995146423968 2; 735.0430062632247 2; 20984.954802862707 2 |
| DATASPATIAL_WKB | other | 212 | 0 | \x00000000030000000100000 2; \x00000000030000000100000 2; \x00000000030000000100000 2; \x00000000060000001100000 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:37:09.35213 215 |
| SOURCE_RUN_ID | audit | 1 | 0 | cddb9ad2-c86d-485b-ae81-0 215 |
| SRC_SHA256 | who | 1 | 0 | 9b9fc74eddd28bb5ac2d1dd45 215 |
