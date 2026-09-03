# PORTAL_CKA_IRELAND_NATIONAL_8B963015F5

rows 1.4K  columns 11  scan 2.5s

roles: amount 1, audit 2, category 7, date 1, who 1

## when

INGESTED_AT
  2026      1.4K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 1.1K | -6.95M | 90.4K | 75.21M | 108.19M | 6.24B |

## who

SRC_SHA256 by rows
      1.4K  8afc4767f9af68418ce142abe5e81def46ef3ac6df3122c13de63e51635a6a56

SRC_SHA256 by dollars
       6.24B     1.4K rows  8afc4767f9af68418ce142abe5e81def46ef3ac6df3122c13de63e51635a

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = VALUE
  8afc4767f9af68418ce142abe5e81def46ef3ac6  2026:6.24B

## what

YEAR: 2022 21%, 2023 20%, 2021 20%, 2020 20%, 2019 19%

FISHING_TECH: TM 17%, FPO 16%, DTS 16%, DRB 16%, DFN 16%, HOK 9%, TBB 7%, INACTIVE 2%

GEAR: Pelagic trawlers 17%, Vessels using pots and/or trap 16%, Demersal trawlers and/or demer 16%, Dredgers 16%, Drift and/or fixed netters 16%, Vessels using hooks 9%, Beam trawlers 7%, NA 2%

VESSEL_LENGTH: VL2440 20%, VL1012 20%, VL1218 19%, VL1824 19%, VL0010 18%, VL40XX 3%

VESSEL_LENGTH_2: Vessel between 24 meters and 4 20%, Vessel between 10 meters and 1 20%, Vessel between 12 meters and 1 19%, Vessel between 18 meters and 2 19%, Vessel between 0 meters and 10 18%, Vessel greater than 40 meters  3%

VARIABLE_NAME: Number of vessels 13%, Total costs 11%, Net profit 11%, Total income 11%, Gross Value Added 11%, Gross value of landings 11%, Engaged crew 11%, Energy costs 11%, Days at sea 11%

UNIT: euro 65%, number 24%, day 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 5 | 0 | 2022 285; 2023 276; 2021 275; 2020 275 |
| FISHING_TECH | category | 8 | 0 | TM 234; FPO 225; DTS 225; DRB 225 |
| GEAR | category | 8 | 0 | Pelagic trawlers 234; Vessels using pots and/or 225; Demersal trawlers and/or  225; Dredgers 225 |
| VESSEL_LENGTH | category | 6 | 0 | VL2440 275; VL1012 275; VL1218 266; VL1824 265 |
| VESSEL_LENGTH_2 | category | 6 | 0 | Vessel between 24 meters  275; Vessel between 10 meters  275; Vessel between 12 meters  266; Vessel between 18 meters  265 |
| VARIABLE_NAME | category | 9 | 0 | Number of vessels 176; Total costs 150; Net profit 150; Total income 150 |
| VALUE | amount | 874 | 0 | NA 275; 0 87; 1 19; 2 17 |
| UNIT | category | 3 | 0 | euro 900; number 326; day 150 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:25:55.40174 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9172a297-21d0-46e2-804f-7 1.4K |
| SRC_SHA256 | who | 1 | 0 | 8afc4767f9af68418ce142abe 1.4K |
