# PORTAL_CKA_CALIFORNIA_OPEN_41B8625438

rows 11  columns 23  scan 2.6s

roles: amount 3, audit 2, category 15, date 1, empty 1, other 1, who 1

## when

INGESTED_AT
  2026        11  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 11 | 38.65 | 39.37 | 39.75 | 39.76 | 432.19 |
| LONGITUDE | 11 | -122.11 | -121.91 | -121.55 | -121.54 | -1.3K |
| ELEV | 11 | 27 | 70 | 185.27 | 189.30 | 939.01 |

## who

SRC_SHA256 by rows
        11  3019d1b931ea7ee2ed99a35554b412ce2318b661c3d85ed204231f68132076d5

SRC_SHA256 by dollars
      432.19       11 rows  3019d1b931ea7ee2ed99a35554b412ce2318b661c3d85ed204231f681320

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  3019d1b931ea7ee2ed99a35554b412ce2318b661  2026:432.19

## what

STATION: 22N02W15C002M 9%, 21N02W33M001M 9%, 20N01E18L001M 9%, 19N02W08Q001M 9%, 19N01E35B002M 9%, 18N01E35L001M 9%, 17N02W09H002M 9%, 16N02W05B001M 9%, 11N04E04N005M 9%, 11N01E24Q008M 9%, 09N03E08C004M 9%

SITE_CODE: 397634N1220771W001 11%, 396299N1221007W001 11%, 395771N1219082W001 11%, 395157N1221122W001 11%, 394634N1218278W001 11%, 393678N1218288W001 11%, 393417N1220838W001 11%, 392753N1221057W001 11%, 386464N1216675W004 11%

STNAME: GLE_15C002M screen interval 75 9%, GLE_33M001M screen interval 86 9%, BUT_18L001M screen interval 76 9%, GLE_08Q001M screen interval 85 9%, BUT_35B002M screen interval 93 9%, BUT_35L001M screen interval 81 9%, COL_09H002M screen interval 77 9%, COL_05B001M screen interval 73 9%, Sutter Land Subsidence Extenso 9%, Zamora Land Subsidence Extenso 9%, Conaway Extensometer screen 53 9%

WELL_NAME: Screen: 759-780 ft 9%, Screen: 869-890 ft 9%, Screen: 767-894 ft 9%, Screen: 856-876 ft 9%, Screen: 930-950 ft 9%, Screen: 816-836 ft 9%, Screen: 779-800 ft 9%, Screen: 730-750 ft 9%, SUT Ext 9%, ZAM Ext 9%, CON Ext and P4 deep 9%

POSACC: Unknown 73%, Survey, 1m 18%, GPS, 10m 9%

ELEVACC: Unknown 73%, EST.CONTOUR <2M. 18%, R.L. AT SURFACE 9%

COUNTY_NAME: Glenn 27%, Butte 27%, Colusa 18%, Yolo 18%, Sutter 9%

BASIN_CODE: 5-021.52 44%, 5-021.70 33%, 5-021.51 11%, 5-021.67 11%

BASIN_NAME: Colusa 44%, Butte 33%, Corning 11%, Yolo 11%

WELL_DEPTH: 825 11%, 929 11%, 940 11%, 910 11%, 980 11%, 840 11%, 806 11%, 797 11%, 545 11%

WELL_USE: Observation 100%

WELL_TYPE: Part of a nested/multi-complet 89%, Single Well 11%

WCR_NO: WCR2003-009798 11%, WCR2002-009790 11%, WCR1999-008135 11%, WCR2004-009692 11%, WCR2003-009257 11%, 726837 11%, WCR2003-009204 11%, WCR2003-009690 11%, WCR1991-012780 11%

WDL: https://wdl.water.ca.gov/Stati 9%, https://wdl.water.ca.gov/Stati 9%, https://wdl.water.ca.gov/Stati 9%, https://wdl.water.ca.gov/Stati 9%, https://wdl.water.ca.gov/Stati 9%, https://wdl.water.ca.gov/Stati 9%, https://wdl.water.ca.gov/Stati 9%, https://wdl.water.ca.gov/Stati 9%, https://wdl.water.ca.gov/Stati 9%, https://wdl.water.ca.gov/Stati 9%, https://wdl.water.ca.gov/Stati 9%

COMMENT: 11N04E04N005M is the extensome 33%, 11N01E24Q008M is the extensome 33%, 09N03E08C004M is the extensome 33%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATION | category | 11 | 0 | 22N02W15C002M 1; 21N02W33M001M 1; 20N01E18L001M 1; 19N02W08Q001M 1 |
| SITE_CODE | category | 10 | 2 | 397634N1220771W001 1; 396299N1221007W001 1; 395771N1219082W001 1; 395157N1221122W001 1 |
| STNAME | category | 11 | 0 | GLE_15C002M screen interv 1; GLE_33M001M screen interv 1; BUT_18L001M screen interv 1; GLE_08Q001M screen interv 1 |
| WELL_NAME | category | 11 | 0 | Screen: 759-780 ft 1; Screen: 869-890 ft 1; Screen: 767-894 ft 1; Screen: 856-876 ft 1 |
| LATITUDE | amount | 11 | 0 | 39.763431 1; 39.629906 1; 39.577074 1; 39.5157 1 |
| LONGITUDE | amount | 11 | 0 | -122.077156 1; -122.100662 1; -121.908207 1; -122.112233 1 |
| LLDATUM | other | 1 | 0 | NAD83 11 |
| POSACC | category | 3 | 0 | Unknown 8; Survey, 1m 2; GPS, 10m 1 |
| ELEV | amount | 11 | 0 | 189.3 1; 149.0 1; 107.35 1; 108.36 1 |
| ELEVDATUM | empty | 1 | 11 |  |
| ELEVACC | category | 3 | 0 | Unknown 8; EST.CONTOUR <2M. 2; R.L. AT SURFACE 1 |
| COUNTY_NAME | category | 5 | 0 | Glenn 3; Butte 3; Colusa 2; Yolo 2 |
| BASIN_CODE | category | 5 | 2 | 5-021.52 4; 5-021.70 3; 5-021.51 1; 5-021.67 1 |
| BASIN_NAME | category | 5 | 2 | Colusa 4; Butte 3; Corning 1; Yolo 1 |
| WELL_DEPTH | category | 10 | 2 | 825 1; 929 1; 940 1; 910 1 |
| WELL_USE | category | 2 | 2 | Observation 9 |
| WELL_TYPE | category | 3 | 2 | Part of a nested/multi-co 8; Single Well 1 |
| WCR_NO | category | 10 | 2 | WCR2003-009798 1; WCR2002-009790 1; WCR1999-008135 1; WCR2004-009692 1 |
| WDL | category | 11 | 0 | https://wdl.water.ca.gov/ 1; https://wdl.water.ca.gov/ 1; https://wdl.water.ca.gov/ 1; https://wdl.water.ca.gov/ 1 |
| COMMENT | category | 4 | 8 | 11N04E04N005M is the exte 1; 11N01E24Q008M is the exte 1; 09N03E08C004M is the exte 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:13:14.34312 11 |
| SOURCE_RUN_ID | audit | 1 | 0 | 60b0a840-507b-4b2a-b6a1-5 11 |
| SRC_SHA256 | who | 1 | 0 | 3019d1b931ea7ee2ed99a3555 11 |
