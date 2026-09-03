# PORTAL_CKA_ANALYZE_BOSTON_75AFC07272

rows 13  columns 11  scan 3.1s

roles: amount 2, audit 2, category 5, date 1, empty 1, who 1

## when

INGESTED_AT
  2026        13  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 13 | 0.11 | 0.19 | 0.38 | 0.39 | 2.58 |
| SHAPE_AREA | 13 | 0 | 0 | 0 | 0 | 0 |

## who

SRC_SHA256 by rows
        13  af70deb3bbeb50ebcc7b4d5a8fdcfa1862f8b662366ae3b591689f472bba2e77

SRC_SHA256 by dollars
        2.58       13 rows  af70deb3bbeb50ebcc7b4d5a8fdcfa1862f8b662366ae3b591689f472bba

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  af70deb3bbeb50ebcc7b4d5a8fdcfa1862f8b662  2026:2.58

## what

PWD: 2-02 8%, 2-08 8%, 3-07 8%, 3-03 8%, 1-10A 8%, 1-10B 8%, 1-1C 8%, 3-05 8%, 2-04 8%, 1-1B 8%, 1-1A 8%, 1-09 8%

NAME: Jamaica Plain/Roslindale 8%, Hyde Park 8%, South Dorchester 8%, North Dorchester 8%, Kenmore/Fenway/Mission Hill 8%, Roxbury 8%, Back Bay/South End/Downtown 8%, South Boston 8%, Allston/Brighton 8%, Beacon Hill/West End/North End 8%, Charlestown 8%, East Boston 8%

COMBO: 2-02: Jamaica Plain/Roslindale 8%, 2-08: Hyde Park 8%, 3-07:  South Dorchester 8%, 3-03:  North Dorchester 8%, 1-10A: Kenmore/Fenway/Mission  8%, 1-10A:  Roxbury 8%, 1-1C: Back Bay/South End/Downt 8%, 3-05:  South Boston 8%, 2-04:  Allston/Brighton 8%, 1-1B:  Beacon Hill/West End/No 8%, 1-1A:  Charlestown 8%, 1-09:  East Boston 8%

DIST: 02 8%, 08 8%, 07 8%, 03 8%, 10A 8%, 10B 8%, 1C 8%, 05 8%, 04 8%, 1B 8%, 1A 8%, 09 8%

GLOBALID: {7F8A0170-4740-494F-87CF-FBEC6 8%, {847BC7E0-290F-46FF-8863-7F075 8%, {D8B0E94B-AC9A-466E-B893-51F06 8%, {7A43B73B-4218-470C-A0C9-6AC68 8%, {8FE77D37-5A58-4E36-B196-858A8 8%, {DEE792FD-3482-40FE-93E5-38A52 8%, {7432E84B-46AA-4116-BFE3-459AB 8%, {2283E388-EEE0-4EDA-882B-BA615 8%, {3796B0A9-5BCA-4731-8A59-BBAC7 8%, {E4426049-38A5-4F67-A16F-D42E0 8%, {B30B164E-8F12-4046-B986-C3BDD 8%, {2A03BBF2-9034-4D11-AC16-F8A50 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PWD | category | 13 | 0 | 2-02 1; 2-08 1; 3-07 1; 3-03 1 |
| NAME | category | 13 | 0 | Jamaica Plain/Roslindale 1; Hyde Park 1; South Dorchester 1; North Dorchester 1 |
| COMBO | category | 13 | 0 | 2-02: Jamaica Plain/Rosli 1; 2-08: Hyde Park 1; 3-07:  South Dorchester 1; 3-03:  North Dorchester 1 |
| DIST | category | 13 | 0 | 02 1; 08 1; 07 1; 03 1 |
| GLOBALID | category | 13 | 0 | {7F8A0170-4740-494F-87CF- 1; {847BC7E0-290F-46FF-8863- 1; {D8B0E94B-AC9A-466E-B893- 1; {7A43B73B-4218-470C-A0C9- 1 |
| SHAPE_LENGTH | amount | 13 | 0 | 0.179035216562901 1; 0.210046062876571 1; 0.268765644361145 1; 0.182563021503363 1 |
| SHAPE_AREA | amount | 13 | 0 | 0.001569404872082 1; 0.001400347144670 1; 0.001558898811396 1; 0.001050874985919 1 |
| SHAPE_WKT | empty | 1 | 13 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:14:43.64933 13 |
| SOURCE_RUN_ID | audit | 1 | 0 | 7270067c-4c73-4a5c-82cd-6 13 |
| SRC_SHA256 | who | 1 | 0 | af70deb3bbeb50ebcc7b4d5a8 13 |
