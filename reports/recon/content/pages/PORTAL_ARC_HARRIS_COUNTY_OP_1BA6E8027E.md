# PORTAL_ARC_HARRIS_COUNTY_OP_1BA6E8027E

rows 27  columns 22  scan 3.2s

roles: amount 4, audit 2, category 14, date 1, empty 1, who 1

## when

INGESTED_AT
  2026        27  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SITE_LATITUDE | 26 | 29.61 | 29.63 | 29.82 | 29.82 | 771.45 |
| SITE_LONGITUDE | 26 | -95.64 | -95.07 | -95.05 | -95.05 | -2.5K |
| TOTAL_EMISSIONS | 26 | 0.60 | 64.80 | 3.9K | 4.6K | 14.7K |
| SUM_EMISSION | 12 | 0.60 | 125.70 | 4.4K | 4.6K | 11.1K |

## who

SRC_SHA256 by rows
        27  f1305b7b928356b63977fab6a0dbf77a6eaf31c8ef25835a637d37e49d8cb397

SRC_SHA256 by dollars
       14.7K       27 rows  f1305b7b928356b63977fab6a0dbf77a6eaf31c8ef25835a637d37e49d8c

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTAL_EMISSIONS
  f1305b7b928356b63977fab6a0dbf77a6eaf31c8  2026:14.7K

## what

OBJECTID: 27 8%, 26 8%, 25 8%, 24 8%, 23 8%, 22 8%, 21 8%, 20 8%, 19 8%, 18 8%, 17 8%, 16 8%

ADDRESS: 9502 BAYPORT BLVD 24%, 5761 UNDERWOOD RD 20%, 2502 SHELDON RD 12%, 9801 BAY AREA BLVD 8%, 13300 BAY AREA BLVD 8%, nan 4%, 3333 HWY 6 SOUTH 4%, 11002 CHOATE RD 4%, 407 W BRENTWOOD 4%, 2759 INDEPENDENCE PARKWAY S 4%, 9502 B BAYPORT BLVD B 4%, 2027 BATTLEGROUND RD 4%

CITY: PASADENA 59%, CHANNELVIEW 15%, LA PORTE 11%, HOUSTON 7%, nan 4%, DEER PARK 4%

COUNTY: Harris 96%, nan 4%

SITE_NAME: CLEAR LAKE PLANT 20%, BAYPORT EO PLANT 20%, CHANNELVIEW PLANT 12%, BAYPORT PLANT 12%, OXITENO PASADENA PLANT 8%, nan 4%, SHELL TECHNOLOGY CENTER HOUSTO 4%, ROGER W POWELL PLANT 4%, EAGLE RAILCAR CHANNELVIEW FACI 4%, DEER PARK FACILITY 4%, CLEAR LAKE 4%, CLEAN HARBORS DEER PARK 4%

NAICS_DESCRIPTION: Petrochemical Manufacturing 67%, Surface Active Agent Manufactu 11%, Solid Waste Landfill 7%, nan 4%, All Other Support Activities f 4%, All Other Miscellaneous Chemic 4%, All Other Support Services 4%

COMPANY_NAME: CELANESE LTD 20%, EQUISTAR CHEMICALS LP 20%, LYONDELL CHEMICAL COMPANY 12%, nan 8%, OXITENO USA LLC 8%, ROHM AND HAAS CHEMICALS LLC 8%, SHELL CHEMICAL LP 4%, E R CARPENTER LP 4%, EAGLE RAILCAR SERVICES-CHANNEL 4%, VOPAK LOGISTICS SERVICES USA I 4%, ARKEMA INC 4%, CLEAN HARBORS DEER PARK LLC 4%

POLLUTANT_DESC: Ethylene Oxide 96%, nan 4%

EMISSIONS_UOM: LB 96%, nan 4%

EMISSION_COMMENT: nan 85%, 2020 facility-reported TRI emi 7%, AirToxScreen SLT Review change 4%, EPA calculated Commercial Ster 4%

POLLUTANT_TYPE_S: HAP 96%, nan 4%

CALCULATION_METHOD: Engineering Judgment 37%, USEPA Emission Factor (no Cont 30%, Material Balance 15%, Stack Test (no Control Efficie 7%, nan 4%, Other Emission Factor (no Cont 4%, Continuous Emission Monitoring 4%

TRI_FACILITY_ID: nan 26%, 77507HCHST9502B 19%, 7750WSLVYS5761U&77507QSTRC5761 19%, 77530RCCHM2502S 11%, 77571RHMND13300 7%, 77507CRPNT11002 4%, 77507DWCHM952BB 4%, 77536SFTYK2027B 4%, 7750WCLRNT952BA 4%, 77507PTRLT13200 4%

GEOMETRY: {"type": "Point", "coordinates 21%, {"type": "Point", "coordinates 21%, {"type": "Point", "coordinates 12%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, nan 4%, {"type": "Point", "coordinates 4%, {"type": "Point", "coordinates 4%, {"type": "Point", "coordinates 4%, {"type": "Point", "coordinates 4%, {"type": "Point", "coordinates 4%, {"type": "Point", "coordinates 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 27 | 0 | 27 1; 26 1; 25 1; 24 1 |
| ADDRESS | category | 14 | 0 | 9502 BAYPORT BLVD 6; 5761 UNDERWOOD RD 5; 2502 SHELDON RD 3; 9801 BAY AREA BLVD 2 |
| CALC_DATA_YEAR | empty | 1 | 27 |  |
| CITY | category | 6 | 0 | PASADENA 16; CHANNELVIEW 4; LA PORTE 3; HOUSTON 2 |
| COUNTY | category | 2 | 0 | Harris 26; nan 1 |
| SITE_NAME | category | 14 | 0 | CLEAR LAKE PLANT 5; BAYPORT EO PLANT 5; CHANNELVIEW PLANT 3; BAYPORT PLANT 3 |
| NAICS_DESCRIPTION | category | 7 | 0 | Petrochemical Manufacturi 18; Surface Active Agent Manu 3; Solid Waste Landfill 2; nan 1 |
| COMPANY_NAME | category | 14 | 0 | CELANESE LTD 5; EQUISTAR CHEMICALS LP 5; LYONDELL CHEMICAL COMPANY 3; nan 2 |
| POLLUTANT_DESC | category | 2 | 0 | Ethylene Oxide 26; nan 1 |
| EMISSIONS_UOM | category | 2 | 0 | LB 26; nan 1 |
| EMISSION_COMMENT | category | 4 | 0 | nan 23; 2020 facility-reported TR 2; AirToxScreen SLT Review c 1; EPA calculated Commercial 1 |
| POLLUTANT_TYPE_S | category | 2 | 0 | HAP 26; nan 1 |
| CALCULATION_METHOD | category | 7 | 0 | Engineering Judgment 10; USEPA Emission Factor (no 8; Material Balance 4; Stack Test (no Control Ef 2 |
| TRI_FACILITY_ID | category | 10 | 0 | nan 7; 77507HCHST9502B 5; 7750WSLVYS5761U&77507QSTR 5; 77530RCCHM2502S 3 |
| SITE_LATITUDE | amount | 15 | 0 | 29.625819 5; 29.6294 5; 29.816654 3; 29.608792 2 |
| SITE_LONGITUDE | amount | 15 | 0 | -95.061592 5; -95.0806 5; -95.107603 3; -95.061022 2 |
| TOTAL_EMISSIONS | amount | 27 | 0 | nan 1; 501.8 1; 1.4 1; 66.0 1 |
| SUM_EMISSION | amount | 13 | 0 | nan 15; 501.8 1; 1.4 1; 72.6 1 |
| GEOMETRY | category | 15 | 0 | {"type": "Point", "coordi 5; {"type": "Point", "coordi 5; {"type": "Point", "coordi 3; {"type": "Point", "coordi 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:15:16.62595 27 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0164b673-a4a8-4c02-a891-2 27 |
| SRC_SHA256 | who | 1 | 0 | f1305b7b928356b63977fab6a 27 |
