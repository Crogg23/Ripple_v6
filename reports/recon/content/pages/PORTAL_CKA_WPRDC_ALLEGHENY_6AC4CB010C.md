# PORTAL_CKA_WPRDC_ALLEGHENY_6AC4CB010C

rows 45  columns 6  scan 1.7s

roles: audit 2, category 3, date 1, who 1

## when

INGESTED_AT
  2026        45  ##############################

## who

SRC_SHA256 by rows
        45  afc2e50d73fc3f2c848bab150473bbdd040a0cd563abe00b878543a7e19ce3f8

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date
  afc2e50d73fc3f2c848bab150473bbdd040a0cd5  2026:45

## what

OBJECTID: 45 8%, 44 8%, 43 8%, 42 8%, 41 8%, 40 8%, 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%

SCHOOLD: Woodland Hills 8%, Wilkinsburg 8%, West Mifflin Area 8%, West Jefferson Hills 8%, West Allegheny 8%, Upper St. Clair Area 8%, Sto-Rox 8%, Steel Valley 8%, South Park 8%, South Fayette Township 8%, South Allegheny 8%, Shaler Area 8%

GEOMETRY: POLYGON ((597760.8593881390988 8%, POLYGON ((596835.8115665906807 8%, POLYGON ((594756.4983978235395 8%, POLYGON ((588490.3902801636140 8%, POLYGON ((565890.8598783345660 8%, POLYGON ((580174.2726102954475 8%, POLYGON ((578044.4301294364267 8%, POLYGON ((594650.4606656837277 8%, POLYGON ((586187.4753790646791 8%, POLYGON ((570538.0537964485120 8%, POLYGON ((595981.7577205239795 8%, POLYGON ((586426.3014055222738 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 45 | 0 | 45 1; 44 1; 43 1; 42 1 |
| SCHOOLD | category | 45 | 0 | Woodland Hills 1; Wilkinsburg 1; West Mifflin Area 1; West Jefferson Hills 1 |
| GEOMETRY | category | 45 | 0 | POLYGON ((597760.85938813 1; POLYGON ((596835.81156659 1; POLYGON ((594756.49839782 1; POLYGON ((588490.39028016 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:21:52.67502 45 |
| SOURCE_RUN_ID | audit | 1 | 0 | a645e97e-980b-497e-8d0c-a 45 |
| SRC_SHA256 | who | 1 | 0 | afc2e50d73fc3f2c848bab150 45 |
