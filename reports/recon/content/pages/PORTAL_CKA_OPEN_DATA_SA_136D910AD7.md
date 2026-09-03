# PORTAL_CKA_OPEN_DATA_SA_136D910AD7

rows 4  columns 9  scan 3.6s

roles: amount 2, audit 2, category 4, date 1, who 1

## when

INGESTED_AT
  2026         4  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 4 | 10.18M | 10.18M | 10.18M | 10.18M | 40.71M |
| SHAPE__LENGTH | 4 | 11.3K | 11.3K | 11.3K | 11.3K | 45.2K |

## who

SRC_SHA256 by rows
         4  c5063b703b2934c33c7605e06885caff236b27a5cdf42b6bd429b69b1f06a52e

SRC_SHA256 by dollars
      40.71M        4 rows  c5063b703b2934c33c7605e06885caff236b27a5cdf42b6bd429b69b1f06

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE__AREA
  c5063b703b2934c33c7605e06885caff236b27a5  2026:40.71M

## what

OBJECTID: 4 25%, 3 25%, 2 25%, 1 25%

ADDRESS: 10040 ESPADA RD 
TX 25%, 9101 GRAF RD 
TX 25%, 6539 SAN JOSE DR 
TX 25%, MISSION RD 
TX 25%

MISSIONNAME: MISSION ESPADA 25%, MISSION SAN JUAN 25%, MISSION SAN JOSE 25%, MISSION CONCEPCION 25%

MPOD: MPOD-4 25%, MPOD-3 25%, MPOD-2 25%, MPOD-1 25%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 4 | 0 | 4 1; 3 1; 2 1; 1 1 |
| ADDRESS | category | 4 | 0 | 10040 ESPADA RD 
TX 1; 9101 GRAF RD 
TX 1; 6539 SAN JOSE DR 
TX 1; MISSION RD 
TX 1 |
| MISSIONNAME | category | 4 | 0 | MISSION ESPADA 1; MISSION SAN JUAN 1; MISSION SAN JOSE 1; MISSION CONCEPCION 1 |
| MPOD | category | 4 | 0 | MPOD-4 1; MPOD-3 1; MPOD-2 1; MPOD-1 1 |
| SHAPE__AREA | amount | 4 | 0 | 10176462.3691406 1; 10176462.2949219 1; 10176462.4082031 1; 10176462.328125 1 |
| SHAPE__LENGTH | amount | 4 | 0 | 11308.9718371297 1; 11308.9718018443 1; 11308.9717614757 1; 11308.9718153775 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:09:11.64582 4 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4c766c65-25e4-47ac-92c4-0 4 |
| SRC_SHA256 | who | 1 | 0 | c5063b703b2934c33c7605e06 4 |
