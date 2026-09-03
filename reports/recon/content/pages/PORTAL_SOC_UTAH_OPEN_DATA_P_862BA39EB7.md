# PORTAL_SOC_UTAH_OPEN_DATA_P_862BA39EB7

rows 17  columns 20  scan 3.8s

roles: amount 2, audit 2, category 12, date 1, other 1, who 3

## when

INGESTED_AT
  2026        17  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 17 | -113.78 | -113.55 | -112.99 | -112.99 | -1.9K |
| Y | 17 | 37 | 37.12 | 37.20 | 37.20 | 630.71 |

## who

SITEDESC by rows
        17  TRI Facilities

SITEDESC by dollars
       -1.9K       17 rows  TRI Facilities

FAC_CNTY by rows
        17  WASHINGTON

FAC_CNTY by dollars
       -1.9K       17 rows  WASHINGTON

SRC_SHA256 by rows
        17  bd1e1caa02b3f057642fe4bee2b0e07c5b5a76ba8428fbc11795e27415182e33

SRC_SHA256 by dollars
       -1.9K       17 rows  bd1e1caa02b3f057642fe4bee2b0e07c5b5a76ba8428fbc11795e2741518

## who x when

SITEDESC by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  TRI Facilities                            2026:-1.9K

FAC_CNTY by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  WASHINGTON                                2026:-1.9K

## what

THE_GEOM: {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 14%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%, {"type": "Point", "coordinates 7%

OBJECTID: 1 8%, 10 8%, 9 8%, 5 8%, 16 8%, 2 8%, 11 8%, 14 8%, 8 8%, 17 8%, 6 8%, 13 8%

DERRID: 84770STGRG1301E 8%, 84770QRSKT516NI 8%, 8477WTHMSP845NI 8%, 84780HNSNP99S1E 8%, 84780SRNSN411SL 8%, 84790CBNTC188N3 8%, 84784BRNTW689NS 8%, 84737PCMRC210NH 8%, 8479WSNRCC1825E 8%, 8479WDNFDS131EC 8%, 84770HYCCK845NI 8%, 84770STKRP1843E 8%

CIMID: 490000006821 8%, Pending4910 8%, NEW6977 8%, Pending5807 8%, Pending5090 8%, Pending4953 8%, Pending4934 8%, Pending5010 8%, NEW6550 8%, NEW9422 8%, Pending5808 8%, Pending5004 8%

MAPLABEL: TRI Facilities - 84770STGRG130 8%, TRI Facilities - 84770QRSKT516 8%, TRI Facilities - 8477WTHMSP845 8%, TRI Facilities - 84780HNSNP99S 8%, TRI Facilities - 84780SRNSN411 8%, TRI Facilities - 84790CBNTC188 8%, TRI Facilities - 84784BRNTW689 8%, TRI Facilities - 84737PCMRC210 8%, TRI Facilities - 8479WSNRCC182 8%, TRI Facilities - 8479WDNFDS131 8%, TRI Facilities - 84770HYCCK845 8%, TRI Facilities - 84770STKRP184 8%

FAC_CITY: SAINT GEORGE 65%, WASHINGTON 12%, HILDALE 12%, HURRICANE 6%, SPRINGDALE 6%

FAC_ADDRES: 1301 EAST 700 NORTH 8%, 516 NORTH INDUSTRIAL ROAD 8%, 845 N INDUSTRIAL RD 8%, 990 S 100 E 8%, 411 S LANDFIELD RD 8%, 188 NORTH 3050 EAST 8%, 689 NORTH STATE STREET 8%, 210 North Highway 91 8%, 1825 EAST 3860 SOUTH 8%, 1310 E COMMERCE DR 8%, 845 N. INDUSTRIAL ROAD 8%, 1843 E 4150 South 8%

FAC_NAME: ST. GEORGE STEEL FABRICATION,  8%, AQUARIUS KITCHEN AND BATH 8%, THOMAS PETROLEUM LLC ST GEORGE 8%, HANSON PIPE and PRECAST INC WA 8%, SORENSON READY MIX CONCRETE 8%, CABINETEC 8%, BRENTWOOD INDUSTRIES INC. 8%, PACE AMERICAN OF UTAH 8%, SUNROC CORPORATION - FORT PIER 8%, DEAN FOODS ICE CREAM 8%, HAYCOCK PETROLEUM SAINT GEORGE 8%, STAKER and PARSON COMPANIES FT 8%

FAC_ZIP: 84770 35%, 84790 29%, 84780 12%, 84784 12%, 84737 6%, 84767 6%

ST_KEY: 5196 8%, 5119 8%, 7072 8%, 5398 8%, 5383 8%, 5221 8%, 5160 8%, 5281 8%, 6637 8%, 9527 8%, 5402 8%, 5275 8%

SIC_DESC: nan 82%, Petroleum Bulk Terminals 6%, Food 6%, Petroleum 6%

POSS_CHEM: nan 82%, POLYCYCLIC AROMATIC COMPOUNDS, 6%, Ammonia, NITRIC ACID 6%, LEAD, NITRATE COMPOUNDS, BENZO 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| THE_GEOM | category | 15 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| OBJECTID | category | 17 | 0 | 1 1; 10 1; 9 1; 5 1 |
| DERRID | category | 17 | 0 | 84770STGRG1301E 1; 84770QRSKT516NI 1; 8477WTHMSP845NI 1; 84780HNSNP99S1E 1 |
| CIMID | category | 17 | 0 | 490000006821 1; Pending4910 1; NEW6977 1; Pending5807 1 |
| MAPLABEL | category | 17 | 0 | TRI Facilities - 84770STG 1; TRI Facilities - 84770QRS 1; TRI Facilities - 8477WTHM 1; TRI Facilities - 84780HNS 1 |
| X | amount | 15 | 0 | -113.60646773 2; -113.57781073 2; -113.55544202 1; -113.56000532 1 |
| Y | amount | 15 | 0 | 37.18543772 2; 37.04186296 2; 37.11951139 1; 37.1167353 1 |
| FAC_CITY | category | 5 | 0 | SAINT GEORGE 11; WASHINGTON 2; HILDALE 2; HURRICANE 1 |
| FAC_ADDRES | category | 17 | 0 | 1301 EAST 700 NORTH 1; 516 NORTH INDUSTRIAL ROAD 1; 845 N INDUSTRIAL RD 1; 990 S 100 E 1 |
| FAC_NAME | category | 17 | 0 | ST. GEORGE STEEL FABRICAT 1; AQUARIUS KITCHEN AND BATH 1; THOMAS PETROLEUM LLC ST G 1; HANSON PIPE and PRECAST I 1 |
| SITEDESC | who | 1 | 0 | TRI Facilities 17 |
| FAC_ZIP | category | 6 | 0 | 84770 6; 84790 5; 84780 2; 84784 2 |
| FAC_STATE | other | 1 | 0 | UT 17 |
| ST_KEY | category | 17 | 0 | 5196 1; 5119 1; 7072 1; 5398 1 |
| FAC_CNTY | who | 1 | 0 | WASHINGTON 17 |
| SIC_DESC | category | 4 | 0 | nan 14; Petroleum Bulk Terminals 1; Food 1; Petroleum 1 |
| POSS_CHEM | category | 4 | 0 | nan 14; POLYCYCLIC AROMATIC COMPO 1; Ammonia, NITRIC ACID 1; LEAD, NITRATE COMPOUNDS,  1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:41:55.44201 17 |
| SOURCE_RUN_ID | audit | 1 | 0 | 90e8c03d-7cb3-4f83-9a44-a 17 |
| SRC_SHA256 | who | 1 | 0 | bd1e1caa02b3f057642fe4bee 17 |
