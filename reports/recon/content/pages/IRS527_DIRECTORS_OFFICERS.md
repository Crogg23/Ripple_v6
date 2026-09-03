# IRS527_DIRECTORS_OFFICERS

rows 189.6K  columns 15  scan 3.2s

roles: audit 2, id 1, other 3, state 1, who 8

## who

ENTITY_NAME by rows
       547  Shawnda Deane
       492  Noreen A Fenner
       458  Ashlee N. Titus
       403  Nancy H. Watkins
       351  Thomas W. Hiltachk
       301  Noreen Fenner
       287  J. Richard Eichman
       276  Kinde Durkee
       266  Mark Herron
       262  David Ramba
       258  Laura Ann Stephen
       253  Kim Bailes
       246  Denise Lewis
       237  Stephanie D Sanchez
       217  Rita Copeland
       212  Brian T. Hildreth
       208  Robert I. Watkins
       204  Stacy Owens
       203  C. April Boling
       188  Noreen A. Fenner

ORG_NAME by rows
      1.5K  PSEA-PACE for State Elections
       734  Hospital and Healthsystem Assoc  of PA Political Action Comm HAPAC
       725  TX State Teachers Association PAC
       634  Associated General Contractors of Texas PAC
       590  OREGON EDUC ASSOCIATION PEOPLE FOR IMPROVEMENT OF EDUCATION
       462  Standing Committee on Political Education, CaLabor
       449  Peace Officers Research Assn of CA Statewide IE Comm
       377  Republican State Leadership Committee - RSLC
       369  Verizon Communications Inc. Good Government Club - PA
       364  Million More Voters, Sponsored by the CA Labor Federation, AFL-CIO
       361  San Bernardino County SEBA PAC
       353  Service Employees International Union Local 521 Candidate PAC
       353  WA State Council of Fire Fighters Segregated Fund
       351  SEIU California State Council Political Committee
       336  Peace Officers Research Association of California PAC
       330  Californians Allied for Patient Protection Political Action Committee
       329  Service Employees Intl. Union Local 521 Independent Expenditure Comm
       313  SEIU California State Council Small Contributor Committee
       309  Florida Phosphate Political Committee Inc
       306  PORAC Official Law Enforcement Voter Guide

ENTITY_ADDR1 by rows
      1.4K  455 Capitol Mall, Suite 600
      1.3K  400 N. 3rd Street, Box 1724
      1.2K  1103 Hays Street
       911  610 S. Boulevard
       753  527 East Park Avenue
       727  2302 Zanker Road
       616  4010 Truxel Road
       607  1787 Tribute Road, Suite K
       600  828 West Washington Blvd.
       571  1001 K Street, Suite 200
       482  2940 Advantage Way
       400  1700 Tribute Road, Suite 201
       397  8489 Cabin Hill Road
       339  1201 F Street NW
       327  P. O. Box 11309
       325  2724 West 8th Street 
       322  4004 Kearny Mesa Road
       314  1069 Adams Street SE
       298  1127 11th Street
       294  5429 Madison Avenue

ENTITY_TITLE by rows
     39.0K  Treasurer
     14.6K  Director
      8.2K  Candidate
      8.2K  President
      7.9K  Chairman
      6.6K  Board Member
      5.1K  Secretary
      4.7K  Vice President
      4.5K  Assistant Treasurer
      4.4K  Chair
      4.0K  TREASURER
      3.5K  Chairperson
      2.7K  Principal Officer
      2.4K  Deputy Treasurer
      2.2K  Trustee
      1.8K  Officer
      1.4K  Campaign Manager
      1.4K  Executive Director
      1.0K  Owner
      1.0K  Committee Member

## where

ENTITY_STATE: CA 46.6K, FL 19.4K, TX 11.9K, PA 8.2K, DC 6.6K, NY 6.5K, IL 5.6K, WA 5.5K, OH 4.4K, VA 4.4K, MI 4.3K, NJ 4.1K

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FORM_ID_NUMBER | other | 77.8K | 0 | 9773100 1.0K; 9773503 1.0K; 9773502 1.0K; 9766956 977 |
| DIRECTOR_ID | id | 193.1K | 0 | 281691 948; 281690 948; 281689 948; 281688 948 |
| ORG_NAME | who | 59.9K | 0 | PSEA-PACE for State Elect 1.6K; Service Employees Interna 1.0K; Standing Committee on Pol 1.0K; Associated Republicans of 998 |
| EIN | other | 58.2K | 0 | 232116856 1.6K; 260124577 1.0K; 770686907 1.0K; 232125904 1.0K |
| ENTITY_NAME | who | 110.5K | 74 | Noreen A Fenner 1.1K; Kim Bailes 1.0K; Noreen Fenner 987; Ashlee N. Titus 962 |
| ENTITY_TITLE | who | 11.3K | 133 | Treasurer 39.0K; Director 14.6K; Candidate 8.2K; President 8.2K |
| ENTITY_ADDR1 | who | 81.3K | 67 | 1103 Hays Street 1.7K; 455 Capitol Mall, Suite 6 1.6K; 527 East Park Avenue 1.6K; 400 N. 3rd Street, Box 17 1.6K |
| ENTITY_ADDR2 | who | 8.8K | 155.2K | Suite 200 629; Suite 400 624; Suite 300 595; Suite 100 453 |
| ENTITY_CITY | who | 12.8K | 57 | Sacramento 12.8K; Tallahassee 6.2K; Washington 6.1K; Los Angeles 3.4K |
| ENTITY_STATE | state | 57 | 7 | CA 46.6K; FL 19.4K; TX 11.9K; PA 8.2K |
| ENTITY_ZIP | who | 17.2K | 7 | 95814 8.1K; 32301 3.9K; 95834 1.7K; 20005 1.7K |
| ENTITY_ZIP_EXT | who | 6.5K | 160.9K | 1724 1.4K; 2220 480; 9790 246; 1701 210 |
| INGESTED_AT | audit | 1 | 0 | 1785966302628518 189.6K |
| SOURCE_RUN_ID | audit | 1 | 0 | 6adb3591-78a6-4d79-b776-1 189.6K |
| SRC_SHA256 | other | 1 | 0 | f1dcece4f64ae78155e82e845 189.6K |
