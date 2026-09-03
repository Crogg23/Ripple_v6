# PORTAL_CKA_CALIFORNIA_OPEN_6611464444

rows 770  columns 23  scan 4.2s

roles: amount 3, audit 2, category 9, date 1, other 6, who 3

## when

INGESTED_AT
  2026       770  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 770 | 0 | 39.32 | 42 | 42 | 30.1K |
| LONGITUDE | 770 | -124.28 | -121.79 | -118.24 | 0 | -93.5K |
| ELEV | 770 | -7.38 | 149 | 5.2K | 5.5K | 473.8K |

## who

STNAME by rows
         1  Ryer Island (RD 501) Well 99-8 screen 9-14 ft bgs
         1  Old River at Tracy Barrier well 1W screen 86-106 ft bgs
         1  Banta-Carbona ID GSA MW-204 mid-deep screen 790-800 ft
         1  Old River at Tracy Barrier well 4 screen 10-20 ft bgs
         1  Delta Island Consumptive Use-McCormackWilliamson-ND13MA
         1  Byron-Bethany ID GSA MW-201 mid-shallow screen 495-505
         1  Delta Island Consumptive Use-Tyler Island-ND39MB-100ff
         1  Prospect Island Well 9A screen 11.2-21.2 ft bgs
         1  Delta Island Consumptive Use-Staten Island-ND23MB-100ff
         1  Ryer Island (RD 501) Well 99-1 screen 33-38 ft bgs
         1  CVWD G9
         1  Prospect Island Well 10A screen 18-28 ft bgs
         1  Ryer Island (RD 501) Well 99-11 screen 53-58 ft bgs
         1  Prospect Island Well 5A screen 27.9-37.9 ft bgs
         1  Byron-Bethany ID GSA MW-202 mid-deep screen 405-415 ft
         1  Grant Line Canal Barrier well 2 screen 15-25 ft bgs
         1  Prospect Island Well 1A screen 13.1-23.1 ft bgs
         1  North San Joaquin WCD first shallow screen 160-190 ft b
         1  Byron-Bethany ID GSA MW-201 shallow screen 250-260 ft b
         1  Upper Roberts Island Well 1C screen 35-40 ft bgs

STNAME by dollars
          42        1 rows  MOD_13R003M screen interval unknown
          42        1 rows  SIS_18J001M screen interval 1260 to 1540 bgs
          42        1 rows  SIS_14M001M screen interval 36 to 127 bgs
          42        1 rows  SIS_16M001M screen interval 1053 to 1537 bgs
          42        1 rows  SIS_13K001M screen interval 935 to 1557 bgs
          42        1 rows  MOD_14R001M screen interval 814 to 1537 bgs
          42        1 rows  SIS_15K001M screen interval 1212 to 1433 bgs
          42        1 rows  MOD_16P001M screen interval 823 to 2108 bgs
          42        1 rows  SIS_16P003M screen interval less than 1200 bgs
       41.98        1 rows  MOD_26D001M screen interval 1250 to 1802 bgs
       41.97        1 rows  SIS_30F002M screen interval 260 to 700 bgs
       41.97        1 rows  SIS_30F001M screen interval 25 to 142 bgs
       41.97        1 rows  MOD_25Q001M screen interval 5 to 110 bgs
       41.97        1 rows  SIS_30L001M screen interval less than 50 bgs
       41.96        1 rows  MOD_36A002M screen interval 428 to 528 bgs
       41.96        1 rows  SIS_35C001M screen interval 2561 to 2761 bgs
       41.89        1 rows  SIS_27D004M screen interval 80 to 100 ft bgs
       41.89        1 rows  SIS_27D002M screen interval 790 to 850 ft bgs
       41.89        1 rows  SIS_27D001M screen interval 1080 to 1090 ft bgs
       41.89        1 rows  SIS_27D003M screen interval 185 to 215 ft bgs

WELL_NAME by rows
        26  Screen: Unknown
         4  Screen: 30-50 ft
         3  Screen: 55-65 ft
         2  Screen: 800-820 ft
         2  Screen: 550-570 ft
         2  Screen: 60-70 ft
         2  Screen: 130-180 ft
         2  Screen: 680-750 ft
         2  Screen: 490-510 ft
         2  Screen: 940-960 ft
         2  Screen: 140-150 ft
         2  Screen: 140-180 ft
         2  Screen: 520-530 ft
         2  Screen: 50-60 ft
         2  Screen: 470-480 ft
         2  Screen: 45-55 ft
         1  OVHV MW-3 Deep
         1  ND48MB
         1  ND48MA
         1  ND45

WELL_NAME by dollars
        1.0K       26 rows  Screen: Unknown
      159.70        4 rows  Screen: 30-50 ft
      119.03        3 rows  Screen: 55-65 ft
       80.23        2 rows  Screen: 680-750 ft
       80.03        2 rows  Screen: 140-180 ft
       79.62        2 rows  Screen: 550-570 ft
       79.60        2 rows  Screen: 940-960 ft
       79.55        2 rows  Screen: 60-70 ft
       79.42        2 rows  Screen: 800-820 ft
       79.37        2 rows  Screen: 50-60 ft
       79.28        2 rows  Screen: 470-480 ft
       79.18        2 rows  Screen: 520-530 ft
       79.16        2 rows  Screen: 130-180 ft
       79.14        2 rows  Screen: 140-150 ft
       79.07        2 rows  Screen: 490-510 ft
       78.82        2 rows  Screen: 45-55 ft
          42        1 rows  Screen: 1212-1433 ft
          42        1 rows  Screen: 1053-1537 ft
          42        1 rows  Screen: 814-1537 ft
          42        1 rows  Screen: 823-2108 ft

SRC_SHA256 by rows
       770  5c1405e820a9d9286b8bc66963a37e7bf24c7b3fcecab040a8c3942a7a382337

SRC_SHA256 by dollars
       30.1K      770 rows  5c1405e820a9d9286b8bc66963a37e7bf24c7b3fcecab040a8c3942a7a38

## who x when

STNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  Banta-Carbona ID GSA MW-204 mid-deep scr  2026:37.64
  Byron-Bethany ID GSA MW-201 mid-shallow   2026:37.78
  Byron-Bethany ID GSA MW-201 shallow scre  2026:37.78
  Byron-Bethany ID GSA MW-202 mid-deep scr  2026:37.80
  CVWD G9                                   2026:33.69
  Delta Island Consumptive Use-McCormackWi  2026:38.24
  Delta Island Consumptive Use-Staten Isla  2026:38.20
  Delta Island Consumptive Use-Tyler Islan  2026:38.20
  Grant Line Canal Barrier well 2 screen 1  2026:37.82
  MOD_13R003M screen interval unknown       2026:42
  MOD_14R001M screen interval 814 to 1537   2026:42
  MOD_16P001M screen interval 823 to 2108   2026:42
  MOD_26D001M screen interval 1250 to 1802  2026:41.98
  North San Joaquin WCD first shallow scre  2026:38.23
  Old River at Tracy Barrier well 1W scree  2026:37.81
  Old River at Tracy Barrier well 4 screen  2026:37.81
  Prospect Island Well 10A screen 18-28 ft  2026:38.26
  Prospect Island Well 1A screen 13.1-23.1  2026:38.25
  Prospect Island Well 5A screen 27.9-37.9  2026:38.29
  Prospect Island Well 9A screen 11.2-21.2  2026:38.27
  Ryer Island (RD 501) Well 99-1 screen 33  2026:38.27
  Ryer Island (RD 501) Well 99-11 screen 5  2026:38.27
  Ryer Island (RD 501) Well 99-8 screen 9-  2026:38.28
  SIS_13K001M screen interval 935 to 1557   2026:42
  SIS_14M001M screen interval 36 to 127 bg  2026:42
  SIS_15K001M screen interval 1212 to 1433  2026:42
  SIS_16M001M screen interval 1053 to 1537  2026:42
  SIS_16P003M screen interval less than 12  2026:42
  SIS_18J001M screen interval 1260 to 1540  2026:42
  Upper Roberts Island Well 1C screen 35-4  2026:37.81

WELL_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  ND45                                      2026:38.17
  ND48MA                                    2026:38.15
  ND48MB                                    2026:38.15
  OVHV MW-3 Deep                            2026:37.61
  Screen: 1053-1537 ft                      2026:42
  Screen: 1212-1433 ft                      2026:42
  Screen: 130-180 ft                        2026:79.16
  Screen: 140-150 ft                        2026:79.14
  Screen: 140-180 ft                        2026:80.03
  Screen: 30-50 ft                          2026:159.70
  Screen: 45-55 ft                          2026:78.82
  Screen: 470-480 ft                        2026:79.28
  Screen: 490-510 ft                        2026:79.07
  Screen: 50-60 ft                          2026:79.37
  Screen: 520-530 ft                        2026:79.18
  Screen: 55-65 ft                          2026:119.03
  Screen: 550-570 ft                        2026:79.62
  Screen: 60-70 ft                          2026:79.55
  Screen: 680-750 ft                        2026:80.23
  Screen: 800-820 ft                        2026:79.42
  Screen: 814-1537 ft                       2026:42
  Screen: 823-2108 ft                       2026:42
  Screen: 940-960 ft                        2026:79.60
  Screen: Unknown                           2026:1.0K

## what

LLDATUM: NAD83 91%, WGS84 9%

POSACC: Survey, 1m 39%, GPS, 10m 32%, Unknown 29%

ELEVDATUM: NAVD88 100%

ELEVACC: R.L. AT SURFACE 47%, Unknown 33%, R.L. AT W.L.M.PT. 13%, EST.CONTOUR <2M. 2%, EST.CONTOUR 2-4M. 2%, OTHER 2%, EST.CONTOUR 4-8M. 1%

COUNTY_NAME: Glenn 17%, Tehama 14%, Yolo 12%, Butte 11%, San Joaquin 10%, Sutter 8%, Colusa 6%, Solano 5%, Shasta 5%, Siskiyou 5%, Modoc 4%, Plumas 2%

BASIN_CODE: 5-021.52 22%, 5-021.67 13%, 5-021.51 9%, 5-021.70 9%, 5-021.56 8%, 5-021.66 7%, 5-022.15 7%, 5-021.57 7%, 5-021.62 6%, 5-022.01 4%, 5-006.03 4%, 5-021.64 4%

BASIN_NAME: Colusa 21%, Yolo 13%, Corning 9%, Butte 9%, Los Molinos 8%, Solano 7%, Tracy 7%, Vina 7%, Sutter 6%, Big Valley 5%, Eastern San Joaquin 4%, Anderson 4%

WELL_USE: Observation 89%, Irrigation 6%, Residential 2%, Unknown 2%, Other 0%, Stockwatering 0%, Industrial 0%

WELL_TYPE: Part of a nested/multi-complet 65%, Single Well 33%, Unknown 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATION | other | 771 | 0 | FHM4 4; 48N05E36A002M 4; 48N05E26D001M 4; 48N05E25Q001M 4 |
| SITE_CODE | other | 760 | 5 | 419614N1213411W001 4; 419762N1213727W001 4; 419657N1213438W001 4; 419962N1214106W001 4 |
| STNAME | who | 750 | 0 | Fitzhugh Meadows 4 4; MOD_36A002M screen interv 4; MOD_26D001M screen interv 4; MOD_25Q001M screen interv 4 |
| WELL_NAME | who | 728 | 0 | Screen: Unknown 27; Screen: 30-50 ft 6; Screen: 680-750 ft 5; Screen: 55-65 ft 5 |
| LATITUDE | amount | 461 | 0 | 41.89439222 7; 41.550591 7; 40.392931 7; 40.187439 7 |
| LONGITUDE | amount | 460 | 0 | -122.294453 7; -122.198787 7; -121.9748336 6; -122.544563 6 |
| LLDATUM | category | 3 | 16 | NAD83 687; WGS84 67 |
| POSACC | category | 3 | 0 | Survey, 1m 301; GPS, 10m 248; Unknown 221 |
| ELEV | amount | 462 | 0 | 0.0 13; 457.84 7; 33.0 7; 451.48 6 |
| ELEVDATUM | category | 2 | 482 | NAVD88 288 |
| ELEVACC | category | 7 | 0 | R.L. AT SURFACE 365; Unknown 252; R.L. AT W.L.M.PT. 102; EST.CONTOUR <2M. 16 |
| COUNTY_NAME | category | 32 | 0 | Glenn 110; Tehama 89; Yolo 75; Butte 72 |
| BASIN_CODE | category | 50 | 18 | 5-021.52 115; 5-021.67 72; 5-021.51 47; 5-021.70 47 |
| BASIN_NAME | category | 49 | 18 | Colusa 115; Yolo 72; Corning 47; Butte 47 |
| WELL_DEPTH | other | 383 | 21 | 100 16; 160 13; 50 12; 25 12 |
| WELL_USE | category | 8 | 6 | Observation 679; Irrigation 46; Residential 19; Unknown 13 |
| WELL_TYPE | category | 4 | 6 | Part of a nested/multi-co 498; Single Well 252; Unknown 14 |
| WCR_NO | other | 340 | 160 | WCR2010-008159 6; WCR2023-007525 6; WCR2007-007867 6; WCR2021-015610 6 |
| WDL | other | 776 | 0 | https://wdl.water.ca.gov/ 4; https://wdl.water.ca.gov/ 4; https://wdl.water.ca.gov/ 4; https://wdl.water.ca.gov/ 4 |
| COMMENT | other | 221 | 494 | TSS Site, Part of multi-c 38; Voluntary Community Data  5; 2022-12-23 Coordinates ar 5; Part of nested well 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:46:52.98064 770 |
| SOURCE_RUN_ID | audit | 1 | 0 | 24f92d90-c5b2-4c76-ac3c-7 770 |
| SRC_SHA256 | who | 1 | 0 | 5c1405e820a9d9286b8bc6696 770 |
