# CA_LOBBY_FIRM_LOBBYIST

rows 577  columns 9  scan 3.1s

roles: audit 2, other 3, who 4

## who

LOBBYIST_FIRST_NAME by rows
         4  DAVID
         4  RICHARD A.
         4  MICHAEL J.
         4  WILLIAM E.
         3  ROBERT W.
         3  THOMAS E.
         3  JOHN R.
         3  JOHN P.
         3  ROBERT J.
         3  MICHAEL B.
         3  RICHARD
         2  JAMES W.
         2  BOB
         2  JAMES D.
         2  MICHAEL R.
         2  PETER M.
         2  ALAN L.
         2  CHARLES L.
         2  PAMELA K.
         2  JOHN C.

LOBBYIST_LAST_NAME by rows
         5  ROSS
         5  BROWN
         4  GARCIA
         4  FLANIGAN
         3  HUNTER
         3  MILLER
         3  LARSON
         3  HARRIS
         3  GOVENAR
         2  ENGLISH
         2  TOBE
         2  ANDERSON
         2  LIVINGSTON
         2  THOMAS
         2  WHITE
         2  SIMONELLI
         2  OCHOA
         2  EDWARDS
         2  THOMPSON
         2  NALDOZA

FIRM_NAME by rows
        12  KAHL/POWNALL ADVOCATES
         8  LIVINGSTON & MATTESICH LAW CORPORATION
         8  SCHOOL SERVICES OF CALIFORNIA, INC.
         8  GOVERNMENTAL ADVOCATES, INC.
         7  ROSE & KINDEL, INC.
         7  PLATINUM ADVISORS LLC
         6  NIELSEN, MERKSAMER, PARRINELLO, MUELLER & NAYLOR LLP
         6  HEIM, NOACK, KELLY & SPAHNN
         6  CARPENTER SNODGRASS & ASSOCIATES
         6  WILSON GROUP, THE
         6  FLANIGAN LAW FIRM, THE
         6  MURDOCH, WALRATH  & HOLMES
         6  NOSSAMAN, GUTHNER, KNOX & ELLIOTT, LLP
         6  STEFFES, FOLEY & LARDNER, INC. 
         5  GUALCO GROUP, THE
         5  READ & ASSOCIATES, AARON
         5  PILLSBURY WINTHROP LLP
         5  ROBINSON & ASSOCIATES, INC., RICHARD
         5  PUBLIC POLICY ADVOCATES, LLC
         5  LANG, HANSEN, O'MALLEY AND MILLER GOVERNMENTAL RELATIONS

SRC_SHA256 by rows
       577  0ca1dc33bc1b239dab186fa7ae2457253c64f1a1c251436583497eeef558091d

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LOBBYIST_ID | other | 572 | 0 | 1149031 3; 1148769 3; 1148597 3; 1149514 3 |
| FIRM_ID | other | 336 | 0 | 1147235 12; 1147320 8; 1147293 8; 1147252 8 |
| LOBBYIST_LAST_NAME | who | 504 | 0 | ROSS 5; BROWN 5; FLANIGAN 4; GREENE 4 |
| LOBBYIST_FIRST_NAME | who | 512 | 0 | MICHAEL J. 5; RICHARD A. 5; THOMAS E. 4; ERNEST E. 4 |
| FIRM_NAME | who | 340 | 0 | KAHL/POWNALL ADVOCATES 12; SCHOOL SERVICES OF CALIFO 8; GOVERNMENTAL ADVOCATES, I 8; LIVINGSTON & MATTESICH LA 8 |
| SESSION_ID | other | 1 | 0 | 2001 577 |
| INGESTED_AT | audit | 1 | 0 | 1785965880679767 577 |
| SOURCE_RUN_ID | audit | 1 | 0 | a9e37c80-7b0e-4a08-87b1-d 577 |
| SRC_SHA256 | who | 1 | 0 | 0ca1dc33bc1b239dab186fa7a 577 |
