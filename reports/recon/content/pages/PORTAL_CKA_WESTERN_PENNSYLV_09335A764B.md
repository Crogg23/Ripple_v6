# PORTAL_CKA_WESTERN_PENNSYLV_09335A764B

rows 10.0K  columns 12  scan 3.8s

roles: audit 2, category 2, date 3, other 3, who 3

## when

START_DATE
  2026     10.0K  ##############################

END_DATE
  2026     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## who

END_STATION_NAME by rows
       490  O'Hara St & University Place
       442  S Bouquet Ave & Sennott St
       431  Forbes Ave at TCS Hall (CMU Campus)
       373  N Dithridge St & Centre Ave
       369  Atwood St & Bates St
       347  Ivy St & Walnut St
       342  S 27th St & Sidney St. (Southside Works)
       342  Centre Ave & S Millvale Ave
       330  Zulema St & Coltart Ave
       321  Schenley Dr & Schenley Dr Ext
       317  Boulevard of the Allies & Parkview Ave
       286  Coltart Ave & Forbes Ave
       272  North Shore Trail & Fort Duquesne Bridge
       272  Penn Ave & 7th St
       262  Fifth Ave & S Bouquet St
       244  S Negley Ave & Centre Ave
       226  Liberty Ave & Stanwix St
       201  Ellsworth Ave & N Neville St
       195  Shady Ave & Ellsworth Ave
       187  Forbes Ave & Market Square

START_STATION_NAME by rows
       470  O'Hara St & University Place
       453  S Bouquet Ave & Sennott St
       419  N Dithridge St & Centre Ave
       402  Forbes Ave at TCS Hall (CMU Campus)
       366  Atwood St & Bates St
       355  Ivy St & Walnut St
       344  Centre Ave & S Millvale Ave
       329  Boulevard of the Allies & Parkview Ave
       318  S 27th St & Sidney St. (Southside Works)
       318  Schenley Dr & Schenley Dr Ext
       314  Coltart Ave & Forbes Ave
       309  Zulema St & Coltart Ave
       278  Penn Ave & 7th St
       274  Fifth Ave & S Bouquet St
       254  North Shore Trail & Fort Duquesne Bridge
       242  Ellsworth Ave & N Neville St
       228  S Negley Ave & Centre Ave
       222  Liberty Ave & Stanwix St
       213  Forbes Ave & Market Square
       193  Shady Ave & Ellsworth Ave

SRC_SHA256 by rows
     10.0K  f5cb0489978f08459f62a0aeca621d2ecd9d6d63cf697577f98647e6af353411

## who x when

END_STATION_NAME by START_DATE
  Atwood St & Bates St                      2026:369
  Boulevard of the Allies & Parkview Ave    2026:317
  Centre Ave & S Millvale Ave               2026:342
  Coltart Ave & Forbes Ave                  2026:286
  Ellsworth Ave & N Neville St              2026:201
  Fifth Ave & S Bouquet St                  2026:262
  Forbes Ave & Market Square                2026:187
  Forbes Ave at TCS Hall (CMU Campus)       2026:431
  Ivy St & Walnut St                        2026:347
  Liberty Ave & Stanwix St                  2026:226
  N Dithridge St & Centre Ave               2026:373
  North Shore Trail & Fort Duquesne Bridge  2026:272
  O'Hara St & University Place              2026:490
  Penn Ave & 7th St                         2026:272
  S 27th St & Sidney St. (Southside Works)  2026:342
  S Bouquet Ave & Sennott St                2026:442
  S Negley Ave & Centre Ave                 2026:244
  Schenley Dr & Schenley Dr Ext             2026:321
  Shady Ave & Ellsworth Ave                 2026:195
  Zulema St & Coltart Ave                   2026:330

START_STATION_NAME by START_DATE
  Atwood St & Bates St                      2026:366
  Boulevard of the Allies & Parkview Ave    2026:329
  Centre Ave & S Millvale Ave               2026:344
  Coltart Ave & Forbes Ave                  2026:314
  Ellsworth Ave & N Neville St              2026:242
  Fifth Ave & S Bouquet St                  2026:274
  Forbes Ave & Market Square                2026:213
  Forbes Ave at TCS Hall (CMU Campus)       2026:402
  Ivy St & Walnut St                        2026:355
  Liberty Ave & Stanwix St                  2026:222
  N Dithridge St & Centre Ave               2026:419
  North Shore Trail & Fort Duquesne Bridge  2026:254
  O'Hara St & University Place              2026:470
  Penn Ave & 7th St                         2026:278
  S 27th St & Sidney St. (Southside Works)  2026:318
  S Bouquet Ave & Sennott St                2026:453
  S Negley Ave & Centre Ave                 2026:228
  Schenley Dr & Schenley Dr Ext             2026:318
  Shady Ave & Ellsworth Ave                 2026:193
  Zulema St & Coltart Ave                   2026:309

## what

CLOSED_STATUS: NORMAL 89%, GRACE_PERIOD 11%, FORCED_CLOSED 0%, TERMINATED 0%

RIDER_TYPE: MEMBER 80%, CASUAL 20%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CLOSED_STATUS | category | 4 | 0 | NORMAL 8.9K; GRACE_PERIOD 1.1K; FORCED_CLOSED 29; TERMINATED 2 |
| DURATION | other | 2.5K | 0 | 25 278; 24 153; 21 132; 26 122 |
| START_STATION_ID | other | 60 | 0 | 12 470; 13 453; 34 419; 59 402 |
| START_DATE | date | 9.9K | 0 | 2026-05-26 09:11:45 51; 2026-05-26 09:15:20 51; 2026-05-26 10:15:20 51; 2026-05-26 11:19:39 51 |
| START_STATION_NAME | who | 60 | 0 | O'Hara St & University Pl 470; S Bouquet Ave & Sennott S 453; N Dithridge St & Centre A 419; Forbes Ave at TCS Hall (C 402 |
| END_DATE | date | 9.9K | 0 | 2026-05-26 11:40:52 51; 2026-05-26 11:45:28 51; 2026-05-26 09:17:21 50; 2026-05-26 09:24:54 50 |
| END_STATION_ID | other | 61 | 1 | 12 490; 13 442; 59 431; 34 373 |
| END_STATION_NAME | who | 61 | 1 | O'Hara St & University Pl 490; S Bouquet Ave & Sennott S 442; Forbes Ave at TCS Hall (C 431; N Dithridge St & Centre A 373 |
| RIDER_TYPE | category | 2 | 0 | MEMBER 8.0K; CASUAL 2.0K |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:48:04.49144 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | e7d29f45-5e29-4482-b025-1 10.0K |
| SRC_SHA256 | who | 1 | 0 | f5cb0489978f08459f62a0aec 10.0K |
