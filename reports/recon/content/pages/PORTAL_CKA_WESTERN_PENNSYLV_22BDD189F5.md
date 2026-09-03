# PORTAL_CKA_WESTERN_PENNSYLV_22BDD189F5

rows 20  columns 15  scan 4.0s

roles: amount 2, audit 2, category 7, date 3, other 1, who 1

## when

CREATED_DATE
  2017         1  ###############
  2019         1  ###############
  2020         2  ##############################
  2021         2  ##############################

LAST_EDITED_DATE
  2019         1  ##
  2020        14  ##############################
  2021         2  ####

INGESTED_AT
  2026        20  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 20 | 15.0K | 891.4K | 21.85M | 25.98M | 50.39M |
| SHAPE__LENGTH | 20 | 611.19 | 5.4K | 54.3K | 62.5K | 194.0K |

## who

SRC_SHA256 by rows
        20  2295c2a7ecc6dd1e79035b831f6bcd2498d064129348f8d0f1e9011731c23091

SRC_SHA256 by dollars
      50.39M       20 rows  2295c2a7ecc6dd1e79035b831f6bcd2498d064129348f8d0f1e9011731c2

## who x when

SRC_SHA256 by LAST_EDITED_DATE, dollars = SHAPE__AREA
  2295c2a7ecc6dd1e79035b831f6bcd2498d06412  2019:54.9K 2020:20.59M 2021:1.42M

## what

GLOBALID: 38b0d6e8-ce3e-40d6-84b9-47ce35 8%, fa64bfa4-2981-4991-b23d-9f29fc 8%, ec522246-b392-4f8b-8f90-ab95a0 8%, 00840db1-314b-4c75-bcd6-506373 8%, 6c5cd294-65b5-4ad7-bc71-fcfa0a 8%, 8235b491-b6b4-48e0-9166-37990d 8%, 474715ba-07bb-4370-9b88-837542 8%, 5b5dcfc3-0b99-44a1-b4a6-860714 8%, fa1f7ff4-b81e-4517-9042-939753 8%, d689f242-1772-456f-82c7-5bad69 8%, 300e722f-1acf-4b52-85ca-6bf5f8 8%, a998ea12-1f3a-45c7-8e07-705b67 8%

OBJECTID: 38 8%, 31 8%, 24 8%, 17 8%, 16 8%, 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%

CREATED_USER: SDE 100%

GUIDELINE_LINK: https://apps.pittsburghpa.gov/ 17%, https://apps.pittsburghpa.gov/ 8%, https://apps.pittsburghpa.gov/ 8%, https://apps.pittsburghpa.gov/ 8%, https://apps.pittsburghpa.gov/ 8%, https://apps.pittsburghpa.gov/ 8%, https://apps.pittsburghpa.gov/ 8%, https://apps.pittsburghpa.gov/ 8%, https://apps.pittsburghpa.gov/ 8%, https://apps.pittsburghpa.gov/ 8%, https://apps.pittsburghpa.gov/ 8%

HISTORIC_NAME: Mexican War Street (Original) 8%, Beth Abraham Cemetery 8%, Frick Park 8%, Allegheny Commons Park 8%, Allegheny West 8%, Alpha Terrace 8%, Deutschtown 8%, East Carson Street 8%, Manchester 8%, Mellon Park 8%, Shrine of the Blessed Mother 8%, Market Square 8%

LAST_EDITED_USER: SDE 100%

GEOMETRY: POLYGON ((583975.6092722447356 8%, MULTIPOLYGON (((585775.4715908 8%, MULTIPOLYGON (((593489.1067640 8%, POLYGON ((584560.8601810904219 8%, POLYGON ((583188.4228824435267 8%, POLYGON ((591349.3801653959089 8%, MULTIPOLYGON (((584704.7661656 8%, POLYGON ((586017.5401190950069 8%, POLYGON ((582343.8007626577746 8%, MULTIPOLYGON (((591905.9010950 8%, MULTIPOLYGON (((588428.7217365 8%, POLYGON ((584708.7519554370082 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GLOBALID | category | 20 | 0 | 38b0d6e8-ce3e-40d6-84b9-4 1; fa64bfa4-2981-4991-b23d-9 1; ec522246-b392-4f8b-8f90-a 1; 00840db1-314b-4c75-bcd6-5 1 |
| OBJECTID | category | 20 | 0 | 38 1; 31 1; 24 1; 17 1 |
| SHAPE__AREA | amount | 20 | 0 | 1006606.16137695 1; 776255.373321533 1; 25981167.2052612 1; 2776014.37249756 1 |
| SHAPE__LENGTH | amount | 20 | 0 | 4214.90178148314 1; 5650.20421814917 1; 62538.8911663592 1; 14500.2826135719 1 |
| CREATED_DATE | date | 6 | 14 | 2020-08-10T17:35:23 2; 2021-07-27T16:33:37 1; 2021-03-23T18:45:24 1; 2017-08-21T14:44:00 1 |
| CREATED_USER | category | 2 | 14 | SDE 6 |
| GUIDELINE_LINK | category | 13 | 7 | https://apps.pittsburghpa 2; https://apps.pittsburghpa 1; https://apps.pittsburghpa 1; https://apps.pittsburghpa 1 |
| HISTORIC_NAME | category | 20 | 0 | Mexican War Street (Origi 1; Beth Abraham Cemetery 1; Frick Park 1; Allegheny Commons Park 1 |
| LAST_EDITED_DATE | date | 17 | 3 | 2020-09-25T15:04:57 2; 2020-09-25T15:05:43 1; 2020-09-25T15:04:04 1; 2020-09-25T15:04:16 1 |
| LAST_EDITED_USER | category | 2 | 3 | SDE 17 |
| TYPE | other | 1 | 0 | CHD 20 |
| GEOMETRY | category | 20 | 0 | POLYGON ((583975.60927224 1; MULTIPOLYGON (((585775.47 1; MULTIPOLYGON (((593489.10 1; POLYGON ((584560.86018109 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:16:08.07779 20 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4f183137-e718-4559-b350-4 20 |
| SRC_SHA256 | who | 1 | 0 | 2295c2a7ecc6dd1e79035b831 20 |
