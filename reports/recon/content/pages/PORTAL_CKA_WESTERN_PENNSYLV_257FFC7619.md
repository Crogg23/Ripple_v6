# PORTAL_CKA_WESTERN_PENNSYLV_257FFC7619

rows 9  columns 11  scan 3.2s

roles: amount 2, audit 2, category 6, date 1, who 1

## when

INGESTED_AT
  2026         9  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 9 | 70.96M | 169.17M | 286.50M | 286.88M | 1.63B |
| SHAPE__LENGTH | 9 | 49.1K | 112.7K | 179.4K | 182.2K | 988.5K |

## who

SRC_SHA256 by rows
         9  383e5cc8377d883a0c69e7388bea198e3ac8f2bdd87c60ad650e3104eded2546

SRC_SHA256 by dollars
       1.63B        9 rows  383e5cc8377d883a0c69e7388bea198e3ac8f2bdd87c60ad650e3104eded

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  383e5cc8377d883a0c69e7388bea198e3ac8f2bd  2026:1.63B

## what

DIST_ID: 3 11%, 4 11%, 6 11%, 7 11%, 2 11%, 5 11%, 1 11%, 9 11%, 8 11%

DIST_NAME: D3 11%, D4 11%, D6 11%, D7 11%, D2 11%, D5 11%, D1 11%, D9 11%, D8 11%

GLOBALID: 969e060c-5bb8-4a3c-8a0c-dd6e8b 11%, bf965136-b8bf-415e-8c2d-85dad1 11%, daadce40-ad0f-4203-9d5a-44704e 11%, 3caaaf3f-fa45-49bb-aad7-7c3696 11%, e1f0a146-aab4-43e8-8cb8-e65574 11%, 4ae56b1e-00ad-47ed-b565-9731bb 11%, 514b047b-3c42-49a1-b531-94b277 11%, 2c9a7a6c-6d3e-4325-9b6c-585dc2 11%, b1e74475-ec1b-405b-9db4-301724 11%

OBJECTID: 72 11%, 65 11%, 48 11%, 46 11%, 43 11%, 40 11%, 30 11%, 21 11%, 20 11%

OBJECTID_1: 9 11%, 8 11%, 7 11%, 6 11%, 5 11%, 4 11%, 3 11%, 2 11%, 1 11%

GEOMETRY: POLYGON ((588821.5260505487676 11%, POLYGON ((583009.0125179910100 11%, POLYGON ((583731.6343997502699 11%, POLYGON ((592600.5412786400411 11%, POLYGON ((581299.4936243777628 11%, POLYGON ((589838.7271098417695 11%, POLYGON ((583829.5361689486308 11%, POLYGON ((594527.5901556966127 11%, POLYGON ((591454.9600904092658 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DIST_ID | category | 9 | 0 | 3 1; 4 1; 6 1; 7 1 |
| DIST_NAME | category | 9 | 0 | D3 1; D4 1; D6 1; D7 1 |
| GLOBALID | category | 9 | 0 | 969e060c-5bb8-4a3c-8a0c-d 1; bf965136-b8bf-415e-8c2d-8 1; daadce40-ad0f-4203-9d5a-4 1; 3caaaf3f-fa45-49bb-aad7-7 1 |
| OBJECTID | category | 9 | 0 | 72 1; 65 1; 48 1; 46 1 |
| OBJECTID_1 | category | 9 | 0 | 9 1; 8 1; 7 1; 6 1 |
| SHAPE__AREA | amount | 9 | 0 | 136640859.737671 1; 169173446.411377 1; 156443221.786041 1; 143906756.97229 1 |
| SHAPE__LENGTH | amount | 9 | 0 | 80946.006680445 1; 86951.0782096829 1; 119972.461353237 1; 86553.8772906552 1 |
| GEOMETRY | category | 9 | 0 | POLYGON ((588821.52605054 1; POLYGON ((583009.01251799 1; POLYGON ((583731.63439975 1; POLYGON ((592600.54127864 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:12:09.78789 9 |
| SOURCE_RUN_ID | audit | 1 | 0 | 044f8bf3-e8e8-45e5-a291-6 9 |
| SRC_SHA256 | who | 1 | 0 | 383e5cc8377d883a0c69e7388 9 |
