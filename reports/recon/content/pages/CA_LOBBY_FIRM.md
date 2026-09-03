# CA_LOBBY_FIRM

rows 256  columns 21  scan 3.3s

roles: amount 12, audit 2, category 1, other 4, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CURRENT_QTR_AMT | 256 | 0 | 0 | 107.0K | 194.1K | 1.46M |
| SESSION_TOTAL_AMT | 256 | 0 | 93.1K | 2.51M | 3.39M | 88.55M |
| YR_1_YTD_AMT | 256 | 0 | 0 | 0 | 318.8K | 318.8K |
| YR_2_YTD_AMT | 256 | 0 | 93.1K | 2.51M | 3.39M | 88.24M |
| QTR_1 | 256 | 0 | 0 | 0 | 79.7K | 79.7K |
| QTR_2 | 256 | 0 | 0 | 0 | 79.7K | 79.7K |

## who

FIRM_NAME by rows
         1  MILLIGAN, PAMELA K. 
         1  U.S. ADVOCACY 
         1  SALAZAR-HOBSON, LAW OFFICES OF ANTONIO 
         1  BOBBURT 
         1  REISNER, DONALD J. 
         1  LYNCH & ASSOCIATES 
         1  CAPITOL STRATEGIES GROUP, INC. 
         1  HELMSIN YARWOOD & ASSOCIATES 
         1  FITZHARRIS & ASSOCIATES 
         1  LELAND AND ASSOCIATES 
         1  A-K ASSOCIATES INC. 
         1  SCHOOL SERVICES OF CALIFORNIA, INC. 
         1  HEIM, NOACK, KELLY & SPAHNN 
         1  MAYER, BROWN & PLATT 
         1  BROWN AND ASSOCIATES, MARC 
         1  FOX, GOVERNMENT RELATIONS, ROBERT 
         1  TURNER, LAW OFFICES OF PREM HUNJI 
         1  MC DONOUGH, HOLLAND & ALLEN 
         1  ROSS, ROBERT E. 
         1  SANDFORD, INC., H. B. 

FIRM_NAME by dollars
      194.1K        1 rows  CARTER LOBBYING FIRM, ART 
      115.8K        1 rows  BROAD, LAW OFFICES OF BARRY 
      112.2K        1 rows  WAGERMAN ASSOCIATES, INC. 
      102.7K        1 rows  MC CALLUM GROUP, PATRICK 
       96.9K        1 rows  GOVERNMENT AFFAIRS CONSULTING 
       96.2K        1 rows  JEA & ASSOCIATES 
       89.9K        1 rows  OMI GOVERNMENT RELATIONS 
       82.6K        1 rows  CRISCIONE, JOE V. 
       68.5K        1 rows  YARYAN, LAW OFFICES OF TIMOTHY 
       68.0K        1 rows  INSTITUTE FOR GOVERNMENT AFFAIRS & PUBLIC POLICY, LLC, THE 
       63.3K        1 rows  PRICE CONSULTING 
       60.7K        1 rows  LOVELL, LAW OFFICES OF JOHN 
       53.7K        1 rows  MC HUGH & ASSOCIATES 
       39.8K        1 rows  DOWDEN AND ASSOCIATES, HR 
       37.8K        1 rows  CAMPBELL - GOVERNMENTAL ACCESS 
       35.3K        1 rows  CLINE COMPANY, ROBERT C. 
       31.3K        1 rows  DCK ADVOCATES, INC. 
       25.4K        1 rows  WALSH AND ASSOCIATES, DANNY 
       21.5K        1 rows  HALL CONSULTING, JOAN 
       20.5K        1 rows  NEWHART & ASSOCIATES, CHARLOTTE MAXWELL 

SRC_SHA256 by rows
       256  a48dd5e06824fc12153928a3e045b7228196b5c44f329058d0f568718cb23f72

SRC_SHA256 by dollars
       1.46M      256 rows  a48dd5e06824fc12153928a3e045b7228196b5c44f329058d0f568718cb2

## what

CONTRIBUTOR_ID: 0 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIRM_ID | other | 253 | 0 | 1147642 2; 1147479 2; 1147554 2; 1147450 2 |
| SESSION_ID | other | 1 | 0 | 2001 256 |
| FIRM_NAME | who | 256 | 0 | ADVOCACY GROUP, THE  2; LIND & ASSOCIATES, ALLAN  2; GOVERNMENT AFFAIRS CONSUL 2; HELMSIN YARWOOD & ASSOCIA 2 |
| CURRENT_QTR_AMT | amount | 25 | 0 | 0 232; 96896.03 1; 60748 1; 7725 1 |
| SESSION_TOTAL_AMT | amount | 241 | 0 | 0 15; 180450 2; 113517.48 2; 172001.06 2 |
| CONTRIBUTOR_ID | category | 2 | 3 | 0 253 |
| SESSION_YR_1 | other | 1 | 0 | 2001 256 |
| SESSION_YR_2 | other | 1 | 0 | 2002 256 |
| YR_1_YTD_AMT | amount | 2 | 0 | 0 255; 318769.40 1 |
| YR_2_YTD_AMT | amount | 241 | 0 | 0 15; 180450 2; 113517.48 2; 172001.06 2 |
| QTR_1 | amount | 2 | 0 | 0 255; 79692.35 1 |
| QTR_2 | amount | 2 | 0 | 0 255; 79692.35 1 |
| QTR_3 | amount | 2 | 0 | 0 255; 79692.35 1 |
| QTR_4 | amount | 2 | 0 | 0 255; 79692.35 1 |
| QTR_5 | amount | 78 | 0 | 0 178; 328571.26 1; 149877.25 1; 129450.01 1 |
| QTR_6 | amount | 85 | 0 | 0 173; 370633.32 1; 164927.84 1; 101882.16 1 |
| QTR_7 | amount | 224 | 0 | 0 26; 82350 2; 62011.74 2; 83634.65 2 |
| QTR_8 | amount | 223 | 0 | 0 29; 98100 2; 51505.74 2; 88366.41 2 |
| INGESTED_AT | audit | 1 | 0 | 1785965869624240 256 |
| SOURCE_RUN_ID | audit | 1 | 0 | 172b179f-42e8-4d20-9b97-1 256 |
| SRC_SHA256 | who | 1 | 0 | a48dd5e06824fc12153928a3e 256 |
