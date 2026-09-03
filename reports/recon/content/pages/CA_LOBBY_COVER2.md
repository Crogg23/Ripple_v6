# CA_LOBBY_COVER2

rows 206.5K  columns 16  scan 3.0s

roles: audit 2, category 6, other 4, who 4

## who

ENTY_NAML by rows
       851  Smith
       712  Brown
       676  Ross
       671  Harris
       665  Gonzalez
       493  Johnson
       443  Lee
       442  Rodriguez
       428  Kim
       404  Sanchez
       403  Baker
       396  White
       391  ROSS
       376  Gonsalves
       372  Hernandez
       366  MILLER
       364  Miller
       361  Martinez
       355  Cooper
       353  SMITH

ENTY_NAMF by rows
      2.8K  Michael
      2.1K  David
      1.9K  John
      1.7K  Robert
      1.5K  James
      1.3K  Jennifer
      1.2K  Daniel
      1.1K  Mark
      1.1K  William
      1.0K  Christopher
      1.0K  Matthew
       998  Richard
       893  Andrew
       881  Thomas
       863  Scott
       843  Elizabeth
       839  Peter
       771  Kevin
       722  JOHN
       698  Jason

ENTY_TITLE by rows
     11.2K  Lobbyist
      8.5K  Managing Director
      5.7K  Legislative Advocate
      4.1K  Partner
      4.1K  Vice President
      4.0K  LOBBYIST
      3.1K  Director
      2.8K  LEGISLATIVE ADVOCATE
      2.8K  President
      2.7K  Principal
      2.7K  Executive Director
      2.2K  Owner
      1.8K  Legislative Representative
      1.3K  MANAGING DIRECTOR
      1.3K  Policy Advocate
      1.3K  Senior Vice President
       886  Senior Managing Director
       825  Associate Director
       816  Legislative Director
       795  Associate

ENTITY_ID by rows
       211  1273641
       205  1283112
       196  L00655
       193  L23395
       184  L20427
       179  L25424
       178  1258189
       177  1236630
       172  1273640
       164  L23262
       163  L25869
       162  L22691
       161  L00339
       160  L25431
       160  L25358
       160  L00445
       160  L25564
       160  L24784
       159  L25785
       158  L22264

## what

AMEND_ID: 0 81%, 1 15%, 2 3%, 3 1%, 4 0%, 5 0%, 6 0%, 10 0%, 9 0%, 8 0%, 7 0%

ENTITY_CD: EMP 72%, OWN 12%, PTN 11%, OFF 5%

ENTY_NAMS: Jr. 42%, II 19%, Sr. 12%, JR. 7%, Esq. 7%, III 6%, IV 3%, Esq.  2%, Jr 1%, Ph.D. 1%

ENTY_NAMT: Mr. 58%, Ms. 27%, MR. 4%, Mrs. 4%, MS. 2%, CEO 1%, Mr 1%, Ms 1%, owner 1%, MR.  1%, Principle 0%

FORM_TYPE: F635 56%, F625 44%

LINE_ITEM: 1 49%, 2 21%, 3 11%, 4 6%, 5 4%, 6 3%, 7 2%, 8 1%, 9 1%, 10 1%, 11 1%, 12 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AMEND_ID | category | 11 | 0 | 0 166.9K; 1 31.0K; 2 6.3K; 3 1.6K |
| ENTITY_CD | category | 4 | 0 | EMP 148.8K; OWN 24.7K; PTN 23.6K; OFF 9.5K |
| ENTITY_ID | who | 4.4K | 90.1K | 1284537 590; 1395203 587; 1294115 587; 1362013 587 |
| ENTY_NAMF | who | 4.9K | 1.6K | Michael 2.8K; David 2.1K; John 2.0K; Robert 1.7K |
| ENTY_NAML | who | 7.7K | 994 | Wilson 1.0K; Edgar 1.0K; Reeb 1.0K; FERNANDEZ 1.0K |
| ENTY_NAMS | category | 26 | 205.7K | Jr. 310; II 137; Sr. 89; JR. 51 |
| ENTY_NAMT | category | 47 | 196.3K | Mr. 5.8K; Ms. 2.7K; MR. 386; Mrs. 355 |
| ENTY_TITLE | who | 3.6K | 73.1K | Lobbyist 11.2K; Managing Director 8.5K; Legislative Advocate 5.7K; Partner 4.1K |
| FILING_ID | other | 84.3K | 0 | 3091141 1.1K; 3143877 1.1K; 3099778 1.1K; 3136290 1.1K |
| FORM_TYPE | category | 2 | 0 | F635 115.2K; F625 91.3K |
| LINE_ITEM | category | 35 | 0 | 1 100.8K; 2 41.9K; 3 22.0K; 4 13.0K |
| REC_TYPE | other | 1 | 0 | CVR2 206.5K |
| TRAN_ID | other | 21.6K | 0 | 1 52.4K; 2 21.3K; 3 10.2K; 4 5.3K |
| INGESTED_AT | audit | 1 | 0 | 1785965815640576 206.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | bf6268e6-fb22-41e4-aa3a-b 206.5K |
| SRC_SHA256 | other | 1 | 0 | b027a4b2ff1aa35106f1a8021 206.5K |
