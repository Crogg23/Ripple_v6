# PORTAL_CKA_WPRDC_ALLEGHENY_B542229640

rows 10  columns 26  scan 4.7s

roles: amount 7, audit 2, category 10, date 4, empty 1, who 3

## when

CREATED_DATE
  2024        10  ##############################

DATE_RESOL
  1981         1  ###############
  1983         1  ###############
  1985         1  ###############
  2006         1  ###############
  2010         2  ##############################
  2011         2  ##############################
  2012         2  ##############################

LAST_EDITED_DATE
  2024        10  ##############################

INGESTED_AT
  2026        10  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 10 | 136.5K | 917.6K | 2.05M | 2.06M | 10.03M |
| SHAPE__LENGTH | 10 | 5.0K | 17.5K | 30.3K | 30.4K | 170.6K |
| ACRES | 10 | 3.13 | 21.07 | 46.97 | 47.39 | 230.32 |
| PERIMETER | 10 | 3.8K | 23.5K | 54.6K | 55.2K | 258.8K |
| PGHDB_SDE_GREENWAYSCARTEGRAPH_A | 10 | 222.6K | 917.6K | 2.05M | 2.06M | 10.03M |
| SHAPE_LENG | 9 | 721.50 | 22.6K | 40.4K | 41.2K | 193.6K |

## who

CREATED_USER by rows
        10  pgh.dcp.allisot

CREATED_USER by dollars
      10.03M       10 rows  pgh.dcp.allisot

LAST_EDITED_USER by rows
        10  pgh.dcp.allisot

LAST_EDITED_USER by dollars
      10.03M       10 rows  pgh.dcp.allisot

SRC_SHA256 by rows
        10  ae44b826917a0ea8b8edbb9fd13b51c701c4509ceea38dfca550df8d0e61be72

SRC_SHA256 by dollars
      10.03M       10 rows  ae44b826917a0ea8b8edbb9fd13b51c701c4509ceea38dfca550df8d0e61

## who x when

CREATED_USER by DATE_RESOL, dollars = SHAPE__AREA
  pgh.dcp.allisot                           1981:2.06M 1983:136.5K 1985:1.86M 2006:1.20M 2010:1.34M 2011:1.87M 2012:1.56M

LAST_EDITED_USER by DATE_RESOL, dollars = SHAPE__AREA
  pgh.dcp.allisot                           1981:2.06M 1983:136.5K 1985:1.86M 2006:1.20M 2010:1.34M 2011:1.87M 2012:1.56M

## what

GLOBALID: 9c850136-c3be-44ce-b6fd-3ee33e 10%, e2aaed34-f270-465a-ad6f-ae9e58 10%, 06f4d641-d412-4b3f-b550-9f278a 10%, 41ba5a47-88fe-4b97-b290-c226a2 10%, dcc77b23-546c-4e40-92be-00e89e 10%, 083d1e3d-a3d0-4778-8628-0096b7 10%, d4c590a8-e941-41ae-b080-68650e 10%, b366bcff-9300-4e9a-8947-cd3cbb 10%, 894febed-7f74-4568-9cef-7f7240 10%, 802f3428-5628-4087-b158-be05e7 10%

OBJECTID_1: 10 10%, 9 10%, 8 10%, 7 10%, 6 10%, 5 10%, 4 10%, 3 10%, 2 10%, 1 10%

DPWDIV: 3 30%, 1 30%, 5 20%, 2 10%, 0 10%

GREENWAY: 0 44%, 3 11%, 7 11%, 5 11%, 6 11%, 4 11%

GREENWAY_I: 2 10%, 1 10%, 10 10%, 9 10%, 8 10%, 11 10%, 7 10%, 12 10%, 6 10%, 4 10%

LABEL: Hazelwood Greenway 10%, Spring Hill / Spring Garden Gr 10%, Oakcliffe Greenway 10%, Allegheny River Greenway 10%, Observatory Hill Hollows Green 10%, Bigelow Greenway 10%, Perry South Greenway 10%, Nine Mile Run Greenway 10%, Moore Greenway 10%, Beechview - Seldom Seen Greenw 10%

NAME: Hazelwood 10%, Spring Hill Spring Garden 10%, Oakcliffe 10%, Allegheny River 10%, Observatory Hill Hollows 10%, Bigelow 10%, Perry South 10%, Nine Mile Run 10%, Moore 10%, Beechview Seldom Seen 10%

NHOOD: Hazelwood 14%, South Oakland 14%, Perry North 14%, Perry South 14%, Squirrel Hill South 14%, Brookline 14%, Beechview 14%

OBJECTID: 0 44%, 25 11%, 2 11%, 24771 11%, 47 11%, 23 11%

GEOMETRY: MULTIPOLYGON (((589078.5488811 10%, MULTIPOLYGON (((585487.6906984 10%, MULTIPOLYGON (((588022.8476323 10%, MULTIPOLYGON (((590332.0609118 10%, MULTIPOLYGON (((582751.7944469 10%, MULTIPOLYGON (((588440.8260195 10%, MULTIPOLYGON (((583443.9012710 10%, MULTIPOLYGON (((591818.8951621 10%, MULTIPOLYGON (((583705.4335143 10%, MULTIPOLYGON (((583483.7826836 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GLOBALID | category | 10 | 0 | 9c850136-c3be-44ce-b6fd-3 1; e2aaed34-f270-465a-ad6f-a 1; 06f4d641-d412-4b3f-b550-9 1; 41ba5a47-88fe-4b97-b290-c 1 |
| OBJECTID_1 | category | 10 | 0 | 10 1; 9 1; 8 1; 7 1 |
| SHAPE__AREA | amount | 10 | 0 | 136469.013916016 1; 2064315.58428955 1; 222644.743835449 1; 1647238.92077637 1 |
| SHAPE__LENGTH | amount | 10 | 0 | 5013.7389417684 1; 19303.1856461039 1; 6349.6060176117 1; 28843.9895794838 1 |
| ACRES | amount | 10 | 0 | 3.13288494 1; 47.38997541 1; 5.11119956 1; 37.81540224 1 |
| CARTID | empty | 1 | 10 |  |
| CREATED_DATE | date | 1 | 0 | 2024-04-10T16:46:41 10 |
| CREATED_USER | who | 1 | 0 | pgh.dcp.allisot 10 |
| DATE_RESOL | date | 9 | 0 | 2012-05-11 2; 1983-03-28 1; 1981-06-29 1; 2011-04-06 1 |
| DPWDIV | category | 5 | 0 | 3 3; 1 3; 5 2; 2 1 |
| GREENWAY | category | 7 | 1 | 0 4; 3 1; 7 1; 5 1 |
| GREENWAY_I | category | 10 | 0 | 2 1; 1 1; 10 1; 9 1 |
| LABEL | category | 10 | 0 | Hazelwood Greenway 1; Spring Hill / Spring Gard 1; Oakcliffe Greenway 1; Allegheny River Greenway 1 |
| LAST_EDITED_DATE | date | 1 | 0 | 2024-04-10T16:46:41 10 |
| LAST_EDITED_USER | who | 1 | 0 | pgh.dcp.allisot 10 |
| NAME | category | 10 | 0 | Hazelwood 1; Spring Hill Spring Garden 1; Oakcliffe 1; Allegheny River 1 |
| NHOOD | category | 8 | 3 | Hazelwood 1; South Oakland 1; Perry North 1; Perry South 1 |
| OBJECTID | category | 7 | 1 | 0 4; 25 1; 2 1; 24771 1 |
| PERIMETER | amount | 10 | 0 | 48166.9375 1; 21532.10546875 1; 6321.64794922 1; 24508.02734375 1 |
| PGHDB_SDE_GREENWAYSCARTEGRAPH_A | amount | 10 | 0 | 256683.32226773 1; 2064315.58483373 1; 222644.74347781 1; 1523837.6436447 1 |
| SHAPE_LENG | amount | 10 | 1 | 41209.8857304 1; 21532.104694 1; 6321.64819273 1; 24508.0271153 1 |
| SQMILES | amount | 10 | 0 | 0.00489513 1; 0.07404743 1; 0.00798631 1; 0.05908657 1 |
| GEOMETRY | category | 10 | 0 | MULTIPOLYGON (((589078.54 1; MULTIPOLYGON (((585487.69 1; MULTIPOLYGON (((588022.84 1; MULTIPOLYGON (((590332.06 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:12:26.03679 10 |
| SOURCE_RUN_ID | audit | 1 | 0 | 37875334-4407-4a22-8843-3 10 |
| SRC_SHA256 | who | 1 | 0 | ae44b826917a0ea8b8edbb9fd 10 |
