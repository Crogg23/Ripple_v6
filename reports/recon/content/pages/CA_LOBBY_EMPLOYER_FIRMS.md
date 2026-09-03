# CA_LOBBY_EMPLOYER_FIRMS

rows 524  columns 8  scan 1.9s

roles: audit 2, category 1, empty 1, other 1, who 3

## who

FIRM_NAME by rows
        18  HEIM, NOACK, KELLY & SPAHNN
        16  NIELSEN, MERKSAMER, PARRINELLO, MUELLER & NAYLOR LLP
        12  SLOAT HIGGINS JENSEN & ASSOCIATES
        12  KAHL/POWNALL ADVOCATES
        11  GOVERNMENTAL ADVOCATES, INC.
        11  ROSE & KINDEL, INC.
        10  PLATINUM ADVISORS LLC
         9  PILLSBURY WINTHROP LLP
         8  WILKE, FLEURY, HOFFELT, GOULD & BIRNEY, LLP
         8  ADVOCATION, INC.
         7  ROBINSON & ASSOCIATES, INC., RICHARD
         7  CWB CONSULTING
         7  LARSON & ASSOCIATES, GEORGE H.
         7  HYDE, MILLER, OWEN & TROST
         7  TREAT, PAULA
         7  SPENCER ROBERTS & ASSOCIATES, INC.
         6  SMITH, KEMPTON & WATTS
         6  HIESTAND, APC, FRED J.
         6  MINNEHAN AND ASSOCIATES, CHRISTINE
         6  LUCAS ADVOCATES

EMPLOYER_ID by rows
        12  1146796
        12  1146836
        11  1146888
        11  1146844
         9  1146774
         8  1146822
         8  1146901
         8  1146864
         8  1146802
         8  1147080
         7  1146905
         7  1147061
         7  1147194
         6  1146780
         6  1146830
         6  1146941
         6  1146793
         6  1147198
         6  1147009
         6  1146855

SRC_SHA256 by rows
       524  338e7f8e21abd9df8cd5f33e221f896ad318924067807988fa37657c3d9e7476

## what

SESSION_ID: 1999 39%, 2001 35%, 1995 14%, 1997 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| EMPLOYER_ID | who | 176 | 0 | 1146836 12; 1146796 12; 1146888 11; 1146844 11 |
| FIRM_ID | other | 133 | 0 | 1147249 18; 1147313 17; 1147749 17; 1147293 14 |
| FIRM_NAME | who | 166 | 0 | HEIM, NOACK, KELLY & SPAH 18; NIELSEN, MERKSAMER, PARRI 16; KAHL/POWNALL ADVOCATES 12; SLOAT HIGGINS JENSEN & AS 12 |
| SESSION_ID | category | 4 | 0 | 1999 205; 2001 185; 1995 74; 1997 60 |
| TERMINATION_DT | empty | 1 | 524 |  |
| INGESTED_AT | audit | 1 | 0 | 1785965860163961 524 |
| SOURCE_RUN_ID | audit | 1 | 0 | 665accd6-b5eb-4499-aff8-b 524 |
| SRC_SHA256 | who | 1 | 0 | 338e7f8e21abd9df8cd5f33e2 524 |
