# PORTAL_ARC_HARRIS_COUNTY_OP_3CFE4113ED

rows 2  columns 30  scan 3.6s

roles: amount 2, audit 2, category 9, date 3, other 6, who 9

## when

SOURCEDATE
  2021         2  ##############################

VAL_DATE
  2020         2  ##############################

INGESTED_AT
  2026         2  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 2 | 29.79 | 29.79 | 29.79 | 29.79 | 59.58 |
| LONGITUDE | 2 | -95.18 | -95.18 | -95.18 | -95.18 | -190.36 |

## who

NAICS_DESC by rows
         2  CHILD DAY CARE CENTERS

NAICS_DESC by dollars
       59.58        2 rows  CHILD DAY CARE CENTERS

SOURCE by rows
         2  http://www.dfps.state.tx.us/child_care/search_texas_child_care/ppfacil

SOURCE by dollars
       59.58        2 rows  http://www.dfps.state.tx.us/child_care/search_texas_child_ca

VAL_METHOD by rows
         2  IMAGERY/OTHER

VAL_METHOD by dollars
       59.58        2 rows  IMAGERY/OTHER

WEBSITE by rows
         2  NOT AVAILABLE

WEBSITE by dollars
       59.58        2 rows  NOT AVAILABLE

## who x when

NAICS_DESC by VAL_DATE, dollars = LATITUDE
  CHILD DAY CARE CENTERS                    2020:59.58

SOURCE by VAL_DATE, dollars = LATITUDE
  http://www.dfps.state.tx.us/child_care/s  2020:59.58

## what

OBJECTID_1: 2 50%, 1 50%

ID: 0060777015 50%, 0091677015 50%

NAME: KIDZTOWN 50%, ANNOINTED CHRISTIAN CHILDCARE 50%

ADDRESS: 13829 LONGVIEW ST 50%, 13837 LONGVIEW ST 50%

TELEPHONE: (713) 455-3500 50%, (713) 330-3112 50%

TYPE: CENTER BASED 50%, RELIGIOUS FACILITY 50%

POPULATION: 99 50%, 68 50%

OBJECTID: 114979 50%, 111171 50%

GEOMETRY: {"type": "Point", "coordinates 50%, {"type": "Point", "coordinates 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | category | 2 | 0 | 2 1; 1 1 |
| ID | category | 2 | 0 | 0060777015 1; 0091677015 1 |
| NAME | category | 2 | 0 | KIDZTOWN 1; ANNOINTED CHRISTIAN CHILD 1 |
| ADDRESS | category | 2 | 0 | 13829 LONGVIEW ST 1; 13837 LONGVIEW ST 1 |
| CITY | who | 1 | 0 | HOUSTON 2 |
| STATE | other | 1 | 0 | TX 2 |
| ZIP | other | 1 | 0 | 77015 2 |
| ZIP4 | who | 1 | 0 | NOT AVAILABLE 2 |
| TELEPHONE | category | 2 | 0 | (713) 455-3500 1; (713) 330-3112 1 |
| TYPE | category | 2 | 0 | CENTER BASED 1; RELIGIOUS FACILITY 1 |
| STATUS | other | 1 | 0 | OPEN 2 |
| POPULATION | category | 2 | 0 | 99 1; 68 1 |
| COUNTY | who | 1 | 0 | HARRIS 2 |
| COUNTYFIPS | other | 1 | 0 | 48201 2 |
| COUNTRY | other | 1 | 0 | USA 2 |
| LATITUDE | amount | 2 | 0 | 29.78609 1; 29.78596 1 |
| LONGITUDE | amount | 2 | 0 | -95.17958 1; -95.17895 1 |
| NAICS_CODE | other | 1 | 0 | 624410 2 |
| NAICS_DESC | who | 1 | 0 | CHILD DAY CARE CENTERS 2 |
| SOURCE | who | 1 | 0 | http://www.dfps.state.tx. 2 |
| SOURCEDATE | date | 1 | 0 | 1633564800000 2 |
| VAL_METHOD | who | 1 | 0 | IMAGERY/OTHER 2 |
| VAL_DATE | date | 1 | 0 | 1589155200000 2 |
| WEBSITE | who | 1 | 0 | NOT AVAILABLE 2 |
| ST_SUBTYPE | who | 1 | 0 | LICENSED CENTER - CHILD C 2 |
| OBJECTID | category | 2 | 0 | 114979 1; 111171 1 |
| GEOMETRY | category | 2 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:11:55.50948 2 |
| SOURCE_RUN_ID | audit | 1 | 0 | 6fb6eb4a-94da-4253-bae0-c 2 |
| SRC_SHA256 | who | 1 | 0 | a5bd749ec7aeb7f295317c6d0 2 |
