# PORTAL_ARC_OPEN_DATA_DC_56C4F04CF0

rows 9  columns 68  scan 5.3s

roles: amount 11, audit 2, category 31, date 4, empty 3, other 16, who 2

## when

REPORTDATE
  2020         4  ##############################
  2021         1  ########
  2022         1  ########
  2023         2  ###############
  2024         1  ########

FROMDATE
  2020         4  ##############################
  2021         1  ########
  2022         1  ########
  2023         2  ###############
  2024         1  ########

LASTUPDATEDATE
  2020         4  ##############################
  2021         1  ########
  2024         4  ##############################

INGESTED_AT
  2026         9  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MEASURE | 9 | 201 | 1.1K | 4.7K | 4.9K | 16.5K |
| OFFSET | 9 | 0.07 | 17.71 | 32.73 | 32.92 | 159.05 |
| LATITUDE | 9 | 38.84 | 38.85 | 38.87 | 38.87 | 349.68 |
| LONGITUDE | 9 | -77 | -77 | -76.98 | -76.98 | -692.97 |
| XCOORD | 9 | 399.6K | 400.3K | 401.5K | 401.6K | 3.60M |
| YCOORD | 9 | 130.6K | 131.1K | 133.1K | 133.2K | 1.18M |

## who

WARD by rows
         9  Ward 8

WARD by dollars
       16.5K        9 rows  Ward 8

SRC_SHA256 by rows
         9  6a96b76c708e9ec12370468e3e3041ef36e8813b93529e64bac77074c5c4a6c6

SRC_SHA256 by dollars
       16.5K        9 rows  6a96b76c708e9ec12370468e3e3041ef36e8813b93529e64bac77074c5c4

## who x when

WARD by REPORTDATE, dollars = MEASURE
  Ward 8                                    2020:8.9K 2021:742.03 2022:2.6K 2023:3.1K 2024:1.1K

SRC_SHA256 by REPORTDATE, dollars = MEASURE
  6a96b76c708e9ec12370468e3e3041ef36e8813b  2020:8.9K 2021:742.03 2022:2.6K 2023:3.1K 2024:1.1K

## what

OBJECTID: 9 11%, 8 11%, 7 11%, 6 11%, 5 11%, 4 11%, 3 11%, 2 11%, 1 11%

CRIMEID: 55329652222 11%, 49231901407 11%, 42702249304 11%, 38901849122 11%, 28672934 11%, 28510879 11%, 28500630 11%, 28361582 11%, 28277667 11%

CCN: 24053376 11%, 23061847 11%, 23024175 11%, 22179472 11%, 21015268 11%, 20121331 11%, 20116457 11%, 20052220 11%, 20002554 11%

ROUTEID: 13059452 22%, 13009362 22%, 15081252A 11%, 14076422 11%, 13058542 11%, 13083422 11%, 15081252 11%

ADDRESS: 2200 SOUTH CAPITOL STREET SE 11%, ROBBINS ROAD SW
WASHINGTON, 11%, 2735 MARTIN LUTHER KING JR AVE 11%, 2737 MARTIN LUTHER KING JR AVE 11%, OAKWOOD ST SE & MALCOLM X AVE  11%, SUITLAND PKWY EAST OF STANTON  11%, 2700 SOUTH CAPITOL STREET SE 11%, 634 ALABAMA AVENUE SE 11%, 13TH STREET SE & ALABAMA AVENU 11%

EVENTID: nan 44%, f7895ea7-de29-4791-98b6-263d3a 11%, 427db5a8-92f7-426a-9824-d66444 11%, 9e5bc266-c180-475f-a7db-ccf923 11%, 45e84ef0-de41-47d9-ba9e-6e99b7 11%, cd04ef17-d4fc-4d02-b409-13665a 11%

MAR_ADDRESS: 2200 SOUTH CAPITOL STREET SE 11%, nan 11%, 2735 MARTIN LUTHER KING JR AVE 11%, 2737 MARTIN LUTHER KING JR AVE 11%, 542 OAKWOOD STREET SE 11%, 3076 STANTON ROAD SE 11%, 2700 SOUTH CAPITOL STREET SE 11%, 634 ALABAMA AVENUE SE 11%, 3200 13TH STREET SE 11%

MINORINJURIES_DRIVER: 0 78%, 2 11%, 1 11%

UNKNOWNINJURIES_DRIVER: 0 78%, 1 22%

FATAL_DRIVER: 1 56%, 0 44%

FATAL_PEDESTRIAN: 0 78%, 1 22%

SPEEDING_INVOLVED: 0 89%, 1 11%

NEARESTINTROUTEID: 0 22%, 13026862 22%, 13083422 11%, 13066232 11%, 36003242 11%, 13074552 11%, 58022422 11%

NEARESTINTSTREETNAME: CYPRESS ST SE 22%, SUITLAND PKWY SE 11%, nan 11%, OAKWOOD ST SE 11%, 0 Intersecting RouteID Not Fou 11%, Ramp-36003242 11%, RANDLE PL SE 11%, Driveway-58022422 11%

INTAPPROACHDIRECTION: East 33%, South 33%, West 22%, Southwest 11%

LOCATIONERROR: nan 78%, Blockkey ERROR. 03300859084ed9 11%, Intersecting Route ERROR.  0 I 11%

MPDGEOX: nan 67%, 399651.01 11%, 400279.96 11%, 400997.95 11%

MPDGEOY: nan 67%, 132304.44 11%, 130634.46 11%, 130763.46 11%

FATALPASSENGER: 0 67%, 1 22%, 3 11%

MAJORINJURIESPASSENGER: 0 89%, 2 11%

MINORINJURIESPASSENGER: 0 89%, 2 11%

MAR_ID: 309941 11%, 309678 11%, 44949 11%, 44965 11%, 8889 11%, 287476 11%, 302058 11%, 2446 11%, 278343 11%

BLOCKKEY: 21a59e20c4bdfe116aa182155ee65c 22%, 03300859084ed9b7131f867f75874c 11%, 1b1312f639e8a4488bcd9119e01c06 11%, 9ece7a08f9b6114c3b49a7bc32a319 11%, 888c6a6773081be98e763abdff81df 11%, 6a3cc56f4a587b1afa38ccdaef2069 11%, 03a7382e594bc394ef0e44c9adb75e 11%, afcb366fc5da216d0d8be130517a28 11%

SUBBLOCKKEY: 935084732d740631f381c230bb7e9c 22%, 358c641a9b5be1869da345abd0a594 11%, bba26ab5cc8aaa322b2b4867223af6 11%, 9ece7a08f9b6114c3b49a7bc32a319 11%, 6551ef3fc0344eb8f16d7a920f2702 11%, 1e30c8c1ecb0d6ab059909eaf42028 11%, 03a7382e594bc394ef0e44c9adb75e 11%, 04dcf3bc7d8e5077205f4d6487c108 11%

CORRIDORID: nan 22%, 13059452_1 22%, Blockkey Not Found on Corridor 22%, 13058542_1 11%, 13083422_1 11%, 13009362_1 11%

NEARESTINTKEY: 0 22%, 8649b5868fbfd89b9e507306b43ae4 22%, 30c42884acfe1183be08659c152675 11%, 9d608b5c38c0cf92c26de6ffed7760 11%, 5af0381ecb6816d8d904fe13cec816 11%, d124769cadd7594e5a9292a6e1e57a 11%, f29033d82e8d0eadcf77a1e4ca24c0 11%

MAJORINJURIESOTHER: nan 56%, 0.0 44%

MINORINJURIESOTHER: nan 56%, 0.0 44%

UNKNOWNINJURIESOTHER: nan 56%, 0.0 44%

FATALOTHER: nan 56%, 0.0 44%

GEOMETRY: {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%, {"type": "Point", "coordinates 11%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 9 | 0 | 9 1; 8 1; 7 1; 6 1 |
| CRIMEID | category | 9 | 0 | 55329652222 1; 49231901407 1; 42702249304 1; 38901849122 1 |
| CCN | category | 9 | 0 | 24053376 1; 23061847 1; 23024175 1; 22179472 1 |
| REPORTDATE | date | 9 | 0 | 1712721120000 1; 1682044020000 1; 1676336940000 1; 1670644800000 1 |
| ROUTEID | category | 7 | 0 | 13059452 2; 13009362 2; 15081252A 1; 14076422 1 |
| MEASURE | amount | 9 | 0 | 1132.58 1; 503.89 1; 2604.35 1; 2613.05 1 |
| OFFSET | amount | 9 | 0 | 32.92 1; 30.580000000000002 1; 28.57 1; 24.09 1 |
| STREETSEGID | empty | 1 | 9 |  |
| ROADWAYSEGID | empty | 1 | 9 |  |
| FROMDATE | date | 9 | 0 | 1712741160000 1; 1682191620000 1; 1676763960000 1; 1670805360000 1 |
| TODATE | empty | 1 | 9 |  |
| ADDRESS | category | 9 | 0 | 2200 SOUTH CAPITOL STREET 1; ROBBINS ROAD SW
WASHINGTO 1; 2735 MARTIN LUTHER KING J 1; 2737 MARTIN LUTHER KING J 1 |
| LATITUDE | amount | 9 | 0 | 38.865142999999996 1; 38.866212 1; 38.84731 1; 38.847165 1 |
| LONGITUDE | amount | 9 | 0 | -77.002561 1; -77.004393 1; -76.996662 1; -76.996048 1 |
| XCOORD | amount | 9 | 0 | 399777.713 1; 399618.728 1; 400289.76 1; 400343.106 1 |
| YCOORD | amount | 9 | 0 | 133035.873 1; 133154.531 1; 131056.247 1; 131040.218 1 |
| WARD | who | 1 | 0 | Ward 8 9 |
| EVENTID | category | 6 | 0 | nan 4; f7895ea7-de29-4791-98b6-2 1; 427db5a8-92f7-426a-9824-d 1; 9e5bc266-c180-475f-a7db-c 1 |
| MAR_ADDRESS | category | 9 | 0 | 2200 SOUTH CAPITOL STREET 1; nan 1; 2735 MARTIN LUTHER KING J 1; 2737 MARTIN LUTHER KING J 1 |
| MAR_SCORE | other | 1 | 0 | 200 9 |
| MAJORINJURIES_BICYCLIST | other | 1 | 0 | 0 9 |
| MINORINJURIES_BICYCLIST | other | 1 | 0 | 0 9 |
| UNKNOWNINJURIES_BICYCLIST | other | 1 | 0 | 0 9 |
| FATAL_BICYCLIST | other | 1 | 0 | 0 9 |
| MAJORINJURIES_DRIVER | other | 1 | 0 | 0 9 |
| MINORINJURIES_DRIVER | category | 3 | 0 | 0 7; 2 1; 1 1 |
| UNKNOWNINJURIES_DRIVER | category | 2 | 0 | 0 7; 1 2 |
| FATAL_DRIVER | category | 2 | 0 | 1 5; 0 4 |
| MAJORINJURIES_PEDESTRIAN | other | 1 | 0 | 0 9 |
| MINORINJURIES_PEDESTRIAN | other | 1 | 0 | 0 9 |
| UNKNOWNINJURIES_PEDESTRIAN | other | 1 | 0 | 0 9 |
| FATAL_PEDESTRIAN | category | 2 | 0 | 0 7; 1 2 |
| TOTAL_VEHICLES | amount | 3 | 0 | 1 5; 2 3; 5 1 |
| TOTAL_BICYCLES | other | 1 | 0 | 0 9 |
| TOTAL_PEDESTRIANS | amount | 2 | 0 | 0 7; 1 2 |
| PEDESTRIANSIMPAIRED | other | 1 | 0 | 0 9 |
| BICYCLISTSIMPAIRED | other | 1 | 0 | 0 9 |
| DRIVERSIMPAIRED | other | 1 | 0 | 0 9 |
| TOTAL_TAXIS | other | 1 | 0 | 0 9 |
| TOTAL_GOVERNMENT | other | 1 | 0 | 0 9 |
| SPEEDING_INVOLVED | category | 2 | 0 | 0 8; 1 1 |
| NEARESTINTROUTEID | category | 7 | 0 | 0 2; 13026862 2; 13083422 1; 13066232 1 |
| NEARESTINTSTREETNAME | category | 8 | 0 | CYPRESS ST SE 2; SUITLAND PKWY SE 1; nan 1; OAKWOOD ST SE 1 |
| OFFINTERSECTION | amount | 8 | 0 | 0.0 2; 84.75 1; 31.32 1; 40.0 1 |
| INTAPPROACHDIRECTION | category | 4 | 0 | East 3; South 3; West 2; Southwest 1 |
| LOCATIONERROR | category | 3 | 0 | nan 7; Blockkey ERROR. 033008590 1; Intersecting Route ERROR. 1 |
| LASTUPDATEDATE | date | 9 | 0 | 1719460290000 1; 1719440861000 1; 1719437579000 1; 1719434196000 1 |
| MPDLATITUDE | amount | 9 | 0 | 38.865148 1; 38.866198 1; 38.847265 1; 38.847190999999995 1 |
| MPDLONGITUDE | amount | 9 | 0 | -77.00218199999999 1; -77.004359 1; -76.996365 1; -76.99632299999999 1 |
| MPDGEOX | category | 4 | 0 | nan 6; 399651.01 1; 400279.96 1; 400997.95 1 |
| MPDGEOY | category | 4 | 0 | nan 6; 132304.44 1; 130634.46 1; 130763.46 1 |
| FATALPASSENGER | category | 3 | 0 | 0 6; 1 2; 3 1 |
| MAJORINJURIESPASSENGER | category | 2 | 0 | 0 8; 2 1 |
| MINORINJURIESPASSENGER | category | 2 | 0 | 0 8; 2 1 |
| UNKNOWNINJURIESPASSENGER | other | 1 | 0 | 0 9 |
| MAR_ID | category | 9 | 0 | 309941 1; 309678 1; 44949 1; 44965 1 |
| BLOCKKEY | category | 8 | 0 | 21a59e20c4bdfe116aa182155 2; 03300859084ed9b7131f867f7 1; 1b1312f639e8a4488bcd9119e 1; 9ece7a08f9b6114c3b49a7bc3 1 |
| SUBBLOCKKEY | category | 8 | 0 | 935084732d740631f381c230b 2; 358c641a9b5be1869da345abd 1; bba26ab5cc8aaa322b2b48672 1; 9ece7a08f9b6114c3b49a7bc3 1 |
| CORRIDORID | category | 6 | 0 | nan 2; 13059452_1 2; Blockkey Not Found on Cor 2; 13058542_1 1 |
| NEARESTINTKEY | category | 7 | 0 | 0 2; 8649b5868fbfd89b9e507306b 2; 30c42884acfe1183be08659c1 1; 9d608b5c38c0cf92c26de6ffe 1 |
| MAJORINJURIESOTHER | category | 2 | 0 | nan 5; 0.0 4 |
| MINORINJURIESOTHER | category | 2 | 0 | nan 5; 0.0 4 |
| UNKNOWNINJURIESOTHER | category | 2 | 0 | nan 5; 0.0 4 |
| FATALOTHER | category | 2 | 0 | nan 5; 0.0 4 |
| GEOMETRY | category | 9 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:30:54.04266 9 |
| SOURCE_RUN_ID | audit | 1 | 0 | 34059ff1-f586-4205-9a97-2 9 |
| SRC_SHA256 | who | 1 | 0 | 6a96b76c708e9ec12370468e3 9 |
