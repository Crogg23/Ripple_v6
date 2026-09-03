# FED_USGS_WBD_HUC8

rows 2.5K  columns 19  scan 4.3s

roles: amount 4, audit 2, category 3, date 2, empty 1, id 3, other 2, who 2

## errors
  LOADDATE: 001065 (22023): SQL compilation error:
Function TRY_CAST cannot be used with arguments of types FLOAT and NUMBER(20,0)

## when

HUC8
  1801        22  #############
  1802        28  ################
  1803        10  ######
  1804        13  ########
  1805         6  ###
  1806        12  #######
  1807        16  #########
  1808         3  ##
  1809        11  ######
  1810         5  ###
  1901        52  ##############################
  1902        21  ############
  1903        25  ##############
  1905        18  ##########
  1906        21  ############
  1907        26  ###############
  1908        27  ################
  1909        19  ###########
  2001         1  #
  2002         1  #
  2003         1  #
  2004         1  #
  2005         1  #
  2006         1  #
  2007         1  #
  2008         2  #
  2009        10  ######

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AREAACRES | 2.4K | 24.4K | 865.3K | 4.94M | 20.99M | 2.78B |
| AREASQKM | 2.4K | 98.77 | 3.5K | 20.0K | 84.9K | 11.25M |
| SHAPE_LENGTH | 2.5K | 39.1K | 578.0K | 2.67M | 7.33M | 1.72B |
| SHAPE_AREA | 2.5K | 121.77M | 5.99B | 99.84B | 265.84B | 26992.36B |

## who

NAME by rows
         8  Black
         7  Beaver
         6  Salt
         6  Willow
         5  Vermilion
         5  Big Sandy
         5  Little
         4  Buffalo
         4  Lower White
         4  Rock
         4  St. Marys
         4  Muddy
         4  Snake
         4  Spring
         4  Elk
         4  Pine
         3  White
         3  Upper White
         3  Cedar
         3  Blackwater

NAME by dollars
       7.33M        1 rows  Icy Strait-Chatham Strait
       6.48M        1 rows  Lake Superior
       6.36M        1 rows  Lake Huron
       5.29M        1 rows  Western Aleutian Islands
       4.71M        8 rows  Black
       3.91M        1 rows  Ikpikpuk River
       3.85M        1 rows  Kuskokwim Delta
       3.72M        1 rows  Utukok River
       3.59M        1 rows  Shelikof Strait
       3.54M        1 rows  Lake Michigan
       3.48M        7 rows  Beaver
       3.46M        1 rows  Lower Colville River
       3.43M        1 rows  Meade River
       3.16M        1 rows  Porcupine Flats-Porcupine River
       3.07M        1 rows  Charley River-Yukon River
       3.04M        1 rows  Nordenskiold River-Yukon River
       3.01M        1 rows  Lower Pelly River
       2.99M        5 rows  Big Sandy
       2.96M        1 rows  Upper Colville River
       2.92M        1 rows  Bell River-Porcupine River

SRC_SHA256 by rows
      2.5K  2bbbd8e20e157f1985d98abe81a588302c3ed046353fd57b5f8aa50956d0e71f

SRC_SHA256 by dollars
       1.72B     2.5K rows  2bbbd8e20e157f1985d98abe81a588302c3ed046353fd57b5f8aa50956d0

## who x when

NAME by HUC8, dollars = SHAPE_LENGTH
  Icy Strait-Chatham Strait                 1901:7.33M
  Ikpikpuk River                            1906:3.91M
  Kuskokwim Delta                           1903:3.85M
  Lower Colville River                      1906:3.46M
  Shelikof Strait                           1902:3.59M
  Utukok River                              1906:3.72M
  Western Aleutian Islands                  1903:5.29M

SRC_SHA256 by HUC8, dollars = SHAPE_LENGTH
  2bbbd8e20e157f1985d98abe81a588302c3ed046  1801:10.90M 1802:13.07M 1803:5.55M 1804:7.16M 1805:2.53M 1806:5.99M 1807:6.07M 1808:1.70M 1809:8.06M 1810:3.60M 1901:56.12M 1902:39.44M 1903:46.79M 1905:34.60M 1906:52.20M 1907:47.90M 1908:52.15M 1909:33.39M 2001:524.2K 2002:265.4K 2003:91.8K 2004:121.8K 2005:197.4K 2006:245.2K 2007:198.3K 2008:161.6K 2009:684.4K

## what

METASOURCEID: {511D2AC8-11BA-45FC-AB98-F69D6 96%, {223F29BD-DAF9-49D8-8E62-D18F7 1%, {B162ADA7-C152-4BAA-A9BA-9BC69 1%, {0F5CF5FB-6B4F-41E3-84E9-F5C22 0%, {2F42D1FB-7624-4C17-A5F6-ECFEE 0%, {39295707-BC3E-4C8E-A346-7A744 0%, {74113E96-0C19-4C43-98B2-8975F 0%, {A9DB8B60-5A4A-4FFC-8BE7-FA64F 0%, {83C0E336-A7DC-4A77-8B32-0D3D2 0%, {902F57E0-530B-4676-9815-0A999 0%, {F2BDADD4-674B-4FE2-850D-CDE80 0%, {B94603DB-170B-4C99-9284-74833 0%

SOURCEDATADESC: Watershed Boundary Dataset (WB 97%, National Hydro Network (NHN) W 3%, 3D Elevation Product 1/3 Arc-s 0%, Pierce 2020  0%, USGS 3DEP

NAIP Imagery 2020 0%, 3DEP IFSAR 5-meter DEM 0%, National Hydro Network Work Un 0%, Digital Raster Graphic [QUAD I 0%, Watershed Boundary Dataset 0%

SOURCEORIGINATOR: Natural Resources and Conserva 96%, Government of Canada; Natural  3%, U.S. Geological Survey 1%, Natural Resource Canada 1%, Pierce County Washington, Wash 0%, British Columbia 0%, Instituto Nacional de Estadist 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.4K | 0 | 2456 13; 2455 13; 2454 13; 2453 13 |
| TNMID | id | 2.5K | 0 | {11AA202E-FD40-4016-A9F9- 13; {D63D8B76-A97E-4235-81FE- 13; {CDC8477F-CD47-41E7-9549- 13; {A3DD555F-0651-495A-A56F- 13 |
| METASOURCEID | category | 36 | 27 | {511D2AC8-11BA-45FC-AB98- 2.3K; {223F29BD-DAF9-49D8-8E62- 34; {B162ADA7-C152-4BAA-A9BA- 27; {0F5CF5FB-6B4F-41E3-84E9- 7 |
| SOURCEDATADESC | category | 9 | 61 | Watershed Boundary Datase 2.3K; National Hydro Network (N 62; 3D Elevation Product 1/3  5; Pierce 2020  3 |
| SOURCEORIGINATOR | category | 7 | 30 | Natural Resources and Con 2.3K; Government of Canada; Nat 62; U.S. Geological Survey 21; Natural Resource Canada 18 |
| SOURCEFEATUREID | empty | 0 | 2.5K |  |
| LOADDATE | date | 99 | 1 | 1723803860000 2.3K; 1728568419000 11; 1727793672000 11; 1727793673000 10 |
| REFERENCEGNIS_IDS | other | 2.0K | 107 | 1618946 15; 1416405 14; 1416412 14; 970226 14 |
| AREAACRES | amount | 2.4K | 7 | 995247.69 13; 798418.79 13; 825063.09 13; 643399.16 13 |
| AREASQKM | amount | 2.5K | 11 | 4027.63 13; 3231.09 13; 3338.91 13; 2603.75 13 |
| STATES | other | 256 | 1 | TX 143; AK 130; CN 116; CA 105 |
| HUC8 | date | 2.5K | 0 | 19010308 13; 19010307 13; 19010306 13; 19010224 13 |
| NAME | who | 2.3K | 0 | Nakina River 13; Inklin River 13; Sheslay River 13; Lower Stikine River 13 |
| GLOBALID | id | 2.5K | 0 | {3259E4E5-7D35-4B7F-AC35- 13; {3F4E375C-27A3-43A3-981E- 13; {41C0520A-89EC-4DE2-8E23- 13; {5745D604-18E8-4D7D-A28C- 13 |
| SHAPE_LENGTH | amount | 2.5K | 0 | 995798.267076387 13; 861730.295936207 13; 801185.607045945 13; 855068.739808598 13 |
| SHAPE_AREA | amount | 2.4K | 0 | 15267120875.0209 13; 11924318147.9966 13; 12042349738.2804 13; 9090558502.14831 13 |
| INGESTED_AT | audit | 1 | 0 | 1786153381186418 2.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 9c70c879-5856-4e48-8503-6 2.5K |
| SRC_SHA256 | who | 1 | 0 | 2bbbd8e20e157f1985d98abe8 2.5K |
