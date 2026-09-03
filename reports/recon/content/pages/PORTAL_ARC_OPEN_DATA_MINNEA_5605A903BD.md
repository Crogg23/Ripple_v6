# PORTAL_ARC_OPEN_DATA_MINNEA_5605A903BD

rows 39  columns 37  scan 5.3s

roles: amount 5, audit 2, category 27, date 3, who 1

## when

SOURCEDATE
  2010        20  ##############################
  2012         1  ##
  2014         1  ##
  2016         4  ######
  2017         3  ####
  2019         2  ###
  2020         4  ######
  2021         3  ####

VAL_DATE
  2010         8  ##############
  2016         2  ####
  2017         1  ##
  2018         4  #######
  2019         3  #####
  2020        17  ##############################
  2021         1  ##
  2022         2  ####

INGESTED_AT
  2026        39  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| POPULATION | 38 | 11 | 201.50 | 837.60 | 882 | 9.2K |
| LATITUDE | 38 | 44.90 | 44.96 | 45.04 | 45.05 | 1.7K |
| LONGITUDE | 38 | -93.32 | -93.25 | -93.18 | -93.17 | -3.5K |
| ENROLLMENT | 38 | 10 | 187 | 786.19 | 828 | 8.5K |
| FT_TEACHER | 38 | 0 | 13 | 51.78 | 54 | 653 |

## who

SRC_SHA256 by rows
        39  544337d8241665880c50c5f72cc1a566aee3024d4e84a44ab34d3e8bed56add1

SRC_SHA256 by dollars
        9.2K       39 rows  544337d8241665880c50c5f72cc1a566aee3024d4e84a44ab34d3e8bed56

## who x when

SRC_SHA256 by VAL_DATE, dollars = POPULATION
  544337d8241665880c50c5f72cc1a566aee3024d  2010:1.6K 2016:555 2017:318 2018:1.5K 2019:580 2020:4.3K 2021:103 2022:307

## what

OBJECTID_1: 39 8%, 38 8%, 37 8%, 36 8%, 35 8%, 34 8%, 33 8%, 32 8%, 31 8%, 30 8%, 29 8%, 28 8%

OBJECTID: nan 8%, 105340.0 8%, 102672.0 8%, 102203.0 8%, 100035.0 8%, 96221.0 8%, 96218.0 8%, 94867.0 8%, 86586.0 8%, 84601.0 8%, 79421.0 8%, 77719.0 8%

NCESID: nan 8%, 270019005280 8%, 270011705279 8%, 270029903733 8%, 270033505203 8%, 270035404849 8%, 270028804862 8%, 270022004420 8%, 270035004097 8%, 270027803617 8%, 270019003143 8%, 270033504554 8%

NAME: nan 8%, FRIENDSHIP ACADEMY OF ARTS - I 8%, BANAADIR SECONDARY 8%, LINCOLN INTERNATIONAL SCHOOL 8%, HENNEPIN MIDDLE SCHOOL 8%, NEW CITY SCHOOL 8%, HIAWATHA COLLEGIATE HIGH SCHOO 8%, AURORA MIDDLE SCHOOL 8%, AUGSBURG FAIRVIEW ACADEMY 8%, SOUTHSIDE FAMILY CHARTER SCHOO 8%, FRIENDSHIP ACDMY OF FINE ARTS  8%, HENNEPIN ELEMENTARY SCHOOL 8%

ADDRESS: nan 8%, 3320 E. 41ST ST 8%, 1201 BRYANT AVE N 8%, 2520 MINNEHAHA AVE 8%, 5011 S 31ST AVE 8%, 1500 6TH STREET NE 8%, 3500 E 28TH STREET 8%, 2103 E 26TH ST 8%, 2504 COLUMBUS AVE 8%, 4500 CLINTON AVE S 8%, 2600 E 38TH ST 8%, 2123 CLINTON AVE S 8%

CITY: MINNEAPOLIS 97%, nan 3%

STATE: MN 97%, nan 3%

ZIP: 55406 17%, 55407 14%, 55411 11%, 55404 11%, 55413 9%, 55414 9%, 55417 6%, 55419 6%, 55403 6%, 55418 6%, nan 3%, 55405 3%

ZIP4: 8888 69%, nan 3%, 4102 3%, 5111 3%, 3022 3%, 2650 3%, 2039 3%, 3223 3%, 4527 3%, 1609 3%, 4802 3%, 1529 3%

TELEPHONE: (612) 879-6703 12%, (612) 843-5050 12%, (612) 455-4004 12%, (612) 588-1449 12%, nan 6%, (612) 326-7200 6%, (612) 872-8690 6%, (612) 623-3309 6%, (612) 200-9590 6%, (612) 333-1614 6%, (612) 872-8322 6%, (612) 668-2680 6%

TYPE: 1 92%, nan 3%, 2 3%, 4 3%

STATUS: 1 92%, 3 5%, nan 3%

COUNTY: HENNEPIN 95%, nan 3%, RAMSEY 3%

COUNTYFIPS: 27053 95%, nan 3%, 27123 3%

COUNTRY: USA 97%, nan 3%

NAICS_CODE: 611110 97%, nan 3%

NAICS_DESC: ELEMENTARY AND SECONDARY SCHOO 97%, nan 3%

SOURCE: nan 8%, http://nces.ed.gov/GLOBALLOCAT 8%, http://nces.ed.gov/GLOBALLOCAT 8%, http://nces.ed.gov/GLOBALLOCAT 8%, http://nces.ed.gov/GLOBALLOCAT 8%, http://nces.ed.gov/GLOBALLOCAT 8%, http://nces.ed.gov/GLOBALLOCAT 8%, http://nces.ed.gov/GLOBALLOCAT 8%, http://nces.ed.gov/GLOBALLOCAT 8%, http://nces.ed.gov/GLOBALLOCAT 8%, http://nces.ed.gov/GLOBALLOCAT 8%, http://nces.ed.gov/GLOBALLOCAT 8%

VAL_METHOD: IMAGERY/OTHER 77%, IMAGERY 21%, nan 3%

WEBSITE: http://www.friendshipacademy.o 11%, http://www.hennepinschools.org 11%, http://www.hiawathaacademies.o 11%, http://www.mpls.k12.mn.us/ 11%, http://www.mnic.org/ 11%, http://www.mtcs.org/ 11%, nan 6%, NOT AVAILABLE 6%, http://www.lincolnihs.org 6%, http://www.newcitycharterschoo 6%, http://www.auroracharterschool 6%, http://www.afa.tc 6%

LEVEL: ELEMENTARY 56%, HIGH 28%, MIDDLE 11%, nan 3%, OTHER 3%

ST_GRADE: KG 44%, 09 23%, PK 13%, 05 8%, 06 5%, nan 3%, 02 3%, 07 3%

END_GRADE: 08 36%, 12 31%, 04 10%, 06 8%, KG 5%, nan 3%, 01 3%, 05 3%, 07 3%

DISTRICTID: 2700117 17%, 2700288 17%, 2700190 9%, 2700335 9%, 2721240 9%, 2700341 9%, 2700446 9%, nan 4%, 2700299 4%, 2700354 4%, 2700220 4%, 2700350 4%

SHELTER_ID: NOT AVAILABLE 97%, nan 3%

DISPLAYNAME: Hiawatha Northrop 15%, MTS Secondary 8%, Friendship Intermidate 8%, Banaadir Seccondary 8%, Lincoln Intl 8%, Hennepin Middle 8%, New City 8%, Hiawatha Kingfield 8%, Aurora 8%, Augsburg Fairview 8%, Southside Family 8%, Friendship Primary 8%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | category | 39 | 0 | 39 1; 38 1; 37 1; 36 1 |
| OBJECTID | category | 39 | 0 | nan 1; 105340.0 1; 102672.0 1; 102203.0 1 |
| NCESID | category | 39 | 0 | nan 1; 270019005280 1; 270011705279 1; 270029903733 1 |
| NAME | category | 38 | 0 | nan 1; FRIENDSHIP ACADEMY OF ART 1; BANAADIR SECONDARY 1; LINCOLN INTERNATIONAL SCH 1 |
| ADDRESS | category | 39 | 0 | nan 1; 3320 E. 41ST ST 1; 1201 BRYANT AVE N 1; 2520 MINNEHAHA AVE 1 |
| CITY | category | 2 | 0 | MINNEAPOLIS 38; nan 1 |
| STATE | category | 2 | 0 | MN 38; nan 1 |
| ZIP | category | 16 | 0 | 55406 6; 55407 5; 55411 4; 55404 4 |
| ZIP4 | category | 16 | 0 | 8888 24; nan 1; 4102 1; 5111 1 |
| TELEPHONE | category | 35 | 0 | (612) 879-6703 2; (612) 843-5050 2; (612) 455-4004 2; (612) 588-1449 2 |
| TYPE | category | 4 | 0 | 1 36; nan 1; 2 1; 4 1 |
| STATUS | category | 3 | 0 | 1 36; 3 2; nan 1 |
| POPULATION | amount | 39 | 0 | nan 1; 206.0 1; 101.0 1; 138.0 1 |
| COUNTY | category | 3 | 0 | HENNEPIN 37; nan 1; RAMSEY 1 |
| COUNTYFIPS | category | 3 | 0 | 27053 37; nan 1; 27123 1 |
| COUNTRY | category | 2 | 0 | USA 38; nan 1 |
| LATITUDE | amount | 39 | 0 | nan 1; 44.92910296400004 1; 44.99081282800006 1; 44.95633229600003 1 |
| LONGITUDE | amount | 39 | 0 | nan 1; -93.22353619799998 1; -93.29161842699995 1; -93.24037797099999 1 |
| NAICS_CODE | category | 2 | 0 | 611110 38; nan 1 |
| NAICS_DESC | category | 2 | 0 | ELEMENTARY AND SECONDARY  38; nan 1 |
| SOURCE | category | 39 | 0 | nan 1; http://nces.ed.gov/GLOBAL 1; http://nces.ed.gov/GLOBAL 1; http://nces.ed.gov/GLOBAL 1 |
| SOURCEDATE | date | 9 | 0 | 1264723200000.0 20; 1580947200000.0 4; 1451952000000.0 4; 1615939200000.0 3 |
| VAL_METHOD | category | 3 | 0 | IMAGERY/OTHER 30; IMAGERY 8; nan 1 |
| VAL_DATE | date | 24 | 0 | 1268870400000.0 5; 1581984000000.0 4; 1517529600000.0 3; 1268784000000.0 3 |
| WEBSITE | category | 33 | 0 | http://www.friendshipacad 2; http://www.hennepinschool 2; http://www.hiawathaacadem 2; http://www.mpls.k12.mn.us 2 |
| LEVEL | category | 6 | 3 | ELEMENTARY 20; HIGH 10; MIDDLE 4; nan 1 |
| ENROLLMENT | amount | 38 | 0 | 322.0 2; nan 1; 203.0 1; 90.0 1 |
| ST_GRADE | category | 8 | 0 | KG 17; 09 9; PK 5; 05 3 |
| END_GRADE | category | 9 | 0 | 08 14; 12 12; 04 4; 06 3 |
| DISTRICTID | category | 28 | 0 | 2700117 4; 2700288 4; 2700190 2; 2700335 2 |
| FT_TEACHER | amount | 27 | 0 | 11.0 4; 10.0 4; 13.0 2; 23.0 2 |
| SHELTER_ID | category | 2 | 0 | NOT AVAILABLE 38; nan 1 |
| DISPLAYNAME | category | 38 | 0 | Hiawatha Northrop 2; MTS Secondary 1; Friendship Intermidate 1; Banaadir Seccondary 1 |
| GEOMETRY | category | 39 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:16:53.57162 39 |
| SOURCE_RUN_ID | audit | 1 | 0 | b5b4494e-2cd1-41a3-b90b-8 39 |
| SRC_SHA256 | who | 1 | 0 | 544337d8241665880c50c5f72 39 |
