# PORTAL_CKA_SAN_JOSE_OPEN_DA_CF566B299B

rows 4.2K  columns 15  scan 4.0s

roles: amount 2, audit 2, category 6, date 1, empty 1, id 2, who 2

## when

INGESTED_AT
  2026      4.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 4.2K | 22.35 | 3.7K | 155.6K | 14.95M | 89.93M |
| SHAPE_AREA | 4.2K | 2.52 | 393.5K | 38.13M | 4.32B | 22.54B |

## who

FACILITYID by rows
         1  95
         1  7
         1  89
         1  24
         1  3
         1  109
         1  110
         1  68
         1  119
         1  47
         1  153
         1  174
         1  134
         1  90
         1  14
         1  2
         1  149
         1  20
         1  88
         1  31

FACILITYID by dollars
      14.95M        1 rows  1854
       7.56M        1 rows  2723
       5.58M        1 rows  1489
       4.23M        1 rows  4161
       4.11M        1 rows  1783
       3.81M        1 rows  114
       3.22M        1 rows  4146
       2.80M        1 rows  3698
       1.87M        1 rows  3835
       1.49M        1 rows  4196
       1.03M        1 rows  220
       1.00M        1 rows  2223
      589.2K        1 rows  249
      469.5K        1 rows  3567
      424.9K        1 rows  149
      418.1K        1 rows  340
      381.1K        1 rows  597
      366.8K        1 rows  3577
      346.5K        1 rows  1246
      319.6K        1 rows  329

SRC_SHA256 by rows
      4.2K  439c1307b1070374cb948e37b1fece26853a069e9a3f41000edd2467ae24670a

SRC_SHA256 by dollars
      89.93M     4.2K rows  439c1307b1070374cb948e37b1fece26853a069e9a3f41000edd2467ae24

## who x when

FACILITYID by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  109                                       2026:3.3K
  110                                       2026:4.4K
  114                                       2026:3.81M
  119                                       2026:13.8K
  134                                       2026:4.6K
  14                                        2026:10.7K
  1489                                      2026:5.58M
  149                                       2026:424.9K
  153                                       2026:8.4K
  174                                       2026:40.2K
  1783                                      2026:4.11M
  1854                                      2026:14.95M
  2                                         2026:3.8K
  20                                        2026:3.9K
  24                                        2026:3.3K
  2723                                      2026:7.56M
  3                                         2026:4.0K
  31                                        2026:2.6K
  3698                                      2026:2.80M
  3835                                      2026:1.87M
  4146                                      2026:3.22M
  4161                                      2026:4.23M
  4196                                      2026:1.49M
  47                                        2026:3.2K
  68                                        2026:2.5K
  7                                         2026:4.8K
  88                                        2026:3.7K
  89                                        2026:2.7K
  90                                        2026:2.1K
  95                                        2026:3.4K

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  439c1307b1070374cb948e37b1fece26853a069e  2026:89.93M

## what

LANDCOVER: California Annual Grassland 24%, Pond 18%, Northern Coastal Scrub / Diabl 12%, Coast Live Oak Forest and Wood 9%, Mixed Riparian Forest and Wood 9%, Golf Courses / Urban Parks 7%, Urban - Suburban 4%, Serpentine Rock Outcrop / Barr 3%, Seasonal Wetland 3%, Rock Outcrop 3%, Agriculture developed / Covere 3%, Orchard 2%

NATURALCOVER: Grasslands 30%, Open Water (Aquatic) 17%, Chaparral & Northern Coastal S 12%, Developed 12%, Oak Woodland 11%, Riparian Forest and Scrub 9%, Irrigated Agriculture 6%, Wetland 3%, Conifer Woodland 1%

VEGTYPE: 1 24%, 26 18%, 3 12%, 18 9%, 16 9%, 47 7%, 43 4%, 41 3%, 37 3%, 42 3%, 36 3%, 31 2%

LANDCOVERID: 10 24%, 70 18%, 22 12%, 33 9%, 42 9%, 92 7%, 90 4%, 12 3%, 61 3%, 14 3%, 83 3%, 80 2%

NATURALCOVERID: 1 30%, 7 17%, 2 12%, 9 12%, 3 11%, 4 9%, 8 6%, 6 3%, 5 1%

LASTUPDATE: 2013/06/28 11:50:19+00 14%, 2013/06/28 11:50:20+00 14%, 2013/06/28 11:50:14+00 14%, 2013/06/28 11:50:18+00 13%, 2013/06/28 11:50:17+00 11%, 2013/06/28 11:50:13+00 11%, 2013/06/28 11:50:15+00 8%, 2013/06/28 11:50:12+00 8%, 2013/06/28 11:50:11+00 4%, 2013/06/28 11:50:21+00 2%, 2013/06/28 11:50:16+00 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 4.2K | 0 | 4196 21; 4195 21; 4194 21; 4193 21 |
| FACILITYID | who | 4.2K | 0 | 4150 21; 4149 21; 4148 21; 4147 21 |
| INTID | id | 4.2K | 0 | 4150 21; 4149 21; 4148 21; 4147 21 |
| LANDCOVER | category | 35 | 0 | California Annual Grassla 976; Pond 732; Northern Coastal Scrub /  499; Coast Live Oak Forest and 381 |
| NATURALCOVER | category | 9 | 0 | Grasslands 1.2K; Open Water (Aquatic) 733; Chaparral & Northern Coas 512; Developed 483 |
| VEGTYPE | category | 35 | 0 | 1 976; 26 732; 3 499; 18 381 |
| LANDCOVERID | category | 35 | 0 | 10 976; 70 732; 22 499; 33 381 |
| NATURALCOVERID | category | 9 | 0 | 1 1.2K; 7 733; 2 512; 9 483 |
| LASTUPDATE | category | 11 | 0 | 2013/06/28 11:50:19+00 600; 2013/06/28 11:50:20+00 599; 2013/06/28 11:50:14+00 580; 2013/06/28 11:50:18+00 533 |
| NOTES | empty | 1 | 4.2K |  |
| SHAPE_LENGTH | amount | 4.2K | 0 | 5211.93121649071 21; 1228.98979418563 21; 5721.55117556665 21; 1228.08463427474 21 |
| SHAPE_AREA | amount | 4.1K | 0 | 944146.616175105 21; 95381.0398000171 21; 1886808.73126588 21; 89865.9799873507 21 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:07:03.92312 4.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 54dadc6f-c998-4a58-b2e5-b 4.2K |
| SRC_SHA256 | who | 1 | 0 | 439c1307b1070374cb948e37b 4.2K |
