# FED_FRACFOCUS_WATER_SOURCE

rows 23.7K  columns 12  scan 4.3s

roles: amount 1, audit 2, category 2, date 1, id 1, other 2, who 4

## when

_INGESTED_AT
  2026     23.7K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PERCENT | 23.7K | 0 | 100 | 100 | 100 | 2.02M |

## who

WELLNAME by rows
         6  MNCL 31and6-16-13HC 002-ALT
         4  BATTLESHIP 707H
         4  KOLACHE G 9HD
         4  BATTLESHIP 708H
         4  SANISH BAY W 5293 34-1 5T
         4  SANISH BAY W 5293 34-1 6B
         4  BATTLESHIP 805H
         4  QUINT ASPER STATE UNIT 4H
         4  MCGARY-TUDOR WEST 4H
         3  Callas 6H
         3  Callas 7H
         3  Stone House 3H
         3  Falls CIty West 2H
         3  Callas 8H
         3  Falls City West 3H
         3  Bowser 4H
         3  Bowser 3H
         3  Callas 5H
         3  Wildcat 10MH
         3  Wildcat 9MH

WELLNAME by dollars
         300        3 rows  Washington 1-16
         300        3 rows  Waddell TR E #3700
         300        3 rows  Forty Niner Ridge Unit #035H
         300        3 rows  Truist 1-18H
         200        2 rows  Steelhead 54-2 Unit 2301H
         200        2 rows  Annie Oakley AB 4231A 5B
         200        2 rows  KEENE 14-35TFH
         200        2 rows  UTL 1110D 1109H
         200        2 rows  Waggoner Grayback 161
         200        2 rows  Jocye 1-3
         200        2 rows  Schooner 8
         200        2 rows  Texas #1
         200        2 rows  Striped Bass GY CEN 10H
         200        2 rows  LOE FED COM 504H
         200        2 rows  Slagle-Fallon A 2R
         200        2 rows  Waddell TR E 3700
         200        2 rows  Forty Niner Ridge Unit #052H
         200        2 rows  ROULETTE 804H
         200        2 rows  Kibbe
         200        2 rows  ROULETTE 802H

OPERATORNAME by rows
      1.9K  Diamondback E&P LLC
      1.2K  MEWBOURNE OIL COMPANY
      1.0K  ConocoPhillips Company/Burlington Resources
       977  COG Operating LLC
       791  Chevron USA Inc.
       680  Continental Resources, Inc
       667  Apache Corporation
       544  XTO Energy/ExxonMobil
       540  Cimarex Energy Co.
       533  Blackbeard Operating
       522  Hess Corporation
       497  Matador Production Company
       377  SM Energy
       373  Marathon Oil
       342  BPX Operating Company
       325  Magnolia Oil & Gas LLC
       301  Noble Energy, Inc.
       283  Ascent Resources - Utica, LLC
       282  Expand Operating LLC
       242  PDC Energy

OPERATORNAME by dollars
      136.3K     1.9K rows  Diamondback E&P LLC
       99.5K     1.0K rows  ConocoPhillips Company/Burlington Resources
       84.1K     1.2K rows  MEWBOURNE OIL COMPANY
       72.9K      791 rows  Chevron USA Inc.
       71.4K      977 rows  COG Operating LLC
       59.5K      680 rows  Continental Resources, Inc
       52.3K      540 rows  Cimarex Energy Co.
       51.3K      544 rows  XTO Energy/ExxonMobil
       46.5K      667 rows  Apache Corporation
       39.0K      497 rows  Matador Production Company
       37.8K      533 rows  Blackbeard Operating
       34.4K      522 rows  Hess Corporation
       34.1K      342 rows  BPX Operating Company
       33.4K      373 rows  Marathon Oil
       33.0K      377 rows  SM Energy
       32.5K      325 rows  Magnolia Oil & Gas LLC
       26.5K      301 rows  Noble Energy, Inc.
       22.1K      242 rows  PDC Energy
       20.7K      282 rows  Expand Operating LLC
       20.2K      202 rows  Javelin Energy Partners Management LLC

COUNTYNAME by rows
      2.0K  Eddy
      1.3K  Martin
      1.3K  Lea
      1.1K  Midland
      1.1K  Weld
       906  Reeves
       697  Upton
       574  Karnes
       567  McKenzie
       521  Williams
       518  Crane
       512  Culberson
       493  Howard
       448  DeWitt
       398  Loving
       371  Ward
       360  Mountrail
       332  Webb
       320  Reagan
       314  Harrison

COUNTYNAME by dollars
      157.6K     2.0K rows  Eddy
      107.9K     1.3K rows  Lea
       99.8K     1.1K rows  Weld
       98.0K     1.3K rows  Martin
       80.3K     1.1K rows  Midland
       74.2K      906 rows  Reeves
       57.8K      697 rows  Upton
       57.1K      574 rows  Karnes
       47.6K      512 rows  Culberson
       44.8K      448 rows  DeWitt
       44.5K      567 rows  McKenzie
       43.4K      493 rows  Howard
       38.6K      521 rows  Williams
       38.0K      518 rows  Crane
       33.1K      332 rows  Webb
       31.2K      398 rows  Loving
       29.7K      371 rows  Ward
       28.7K      293 rows  Live Oak
       27.9K      320 rows  Reagan
       27.4K      274 rows  Dimmit

_SRC_FILE by rows
     23.7K  WaterSource_1.csv

_SRC_FILE by dollars
       2.02M    23.7K rows  WaterSource_1.csv

## who x when

WELLNAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = PERCENT
  Annie Oakley AB 4231A 5B                  2026:200
  BATTLESHIP 707H                           2026:200
  BATTLESHIP 708H                           2026:200
  BATTLESHIP 805H                           2026:200
  Bowser 3H                                 2026:100
  Bowser 4H                                 2026:100
  Callas 5H                                 2026:100
  Callas 6H                                 2026:100
  Callas 7H                                 2026:100
  Callas 8H                                 2026:100
  Falls CIty West 2H                        2026:100
  Falls City West 3H                        2026:100
  Forty Niner Ridge Unit #035H              2026:300
  Jocye 1-3                                 2026:200
  KEENE 14-35TFH                            2026:200
  KOLACHE G 9HD                             2026:200
  MCGARY-TUDOR WEST 4H                      2026:200
  MNCL 31and6-16-13HC 002-ALT               2026:0
  QUINT ASPER STATE UNIT 4H                 2026:200
  SANISH BAY W 5293 34-1 5T                 2026:200
  SANISH BAY W 5293 34-1 6B                 2026:200
  Steelhead 54-2 Unit 2301H                 2026:200
  Stone House 3H                            2026:100
  Truist 1-18H                              2026:300
  UTL 1110D 1109H                           2026:200
  Waddell TR E #3700                        2026:300
  Waggoner Grayback 161                     2026:200
  Washington 1-16                           2026:300
  Wildcat 10MH                              2026:100
  Wildcat 9MH                               2026:100

OPERATORNAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = PERCENT
  Apache Corporation                        2026:46.5K
  Ascent Resources - Utica, LLC             2026:14.3K
  BPX Operating Company                     2026:34.1K
  Blackbeard Operating                      2026:37.8K
  COG Operating LLC                         2026:71.4K
  Chevron USA Inc.                          2026:72.9K
  Cimarex Energy Co.                        2026:52.3K
  ConocoPhillips Company/Burlington Resour  2026:99.5K
  Continental Resources, Inc                2026:59.5K
  Diamondback E&P LLC                       2026:136.3K
  Expand Operating LLC                      2026:20.7K
  Hess Corporation                          2026:34.4K
  Javelin Energy Partners Management LLC    2026:20.2K
  MEWBOURNE OIL COMPANY                     2026:84.1K
  Magnolia Oil & Gas LLC                    2026:32.5K
  Marathon Oil                              2026:33.4K
  Matador Production Company                2026:39.0K
  Noble Energy, Inc.                        2026:26.5K
  PDC Energy                                2026:22.1K
  SM Energy                                 2026:33.0K
  XTO Energy/ExxonMobil                     2026:51.3K

## what

STATENAME: Texas 53%, New Mexico 15%, North Dakota 8%, Colorado 7%, Oklahoma 5%, Pennsylvania 4%, Ohio 3%, West Virginia 2%, Louisiana 2%, Wyoming 1%, Utah 1%, Montana 0%

DESCRIPTION: Groundwater, < 1000TDS 35%, Produced Water 33%, Surface Water, < 1000TDS 14%, Groundwater, > 1000TDS 11%, Other, > 1000TDS 2%, Surface Water, > 1000TDS 2%, Other, < 1000TDS 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| WATERSOURCEID | id | 23.8K | 0 | 696c7f54-106f-460e-8624-1 119; 24610fbb-6136-462c-97c6-6 119; 2c80e55f-6111-4678-9109-9 119; d7049b9a-1f9a-4fcc-b218-c 119 |
| DISCLOSUREID | other | 20.6K | 0 | 52d7871d-25ff-4e4d-bd9e-f 120; a842f50e-ee46-4c0e-ae8e-f 120; a66d00fb-c187-4f1d-aec6-f 120; 4e848eab-8c29-4824-8ed7-f 120 |
| APINUMBER | other | 20.2K | 0 | 33105059890000 120; 42389412360000 120; 33053065040000 120; 42317466640000 120 |
| STATENAME | category | 19 | 0 | Texas 12.5K; New Mexico 3.5K; North Dakota 1.8K; Colorado 1.6K |
| COUNTYNAME | who | 286 | 0 | Eddy 2.0K; Martin 1.3K; Lea 1.3K; Midland 1.1K |
| OPERATORNAME | who | 577 | 0 | Diamondback E&P LLC 1.9K; MEWBOURNE OIL COMPANY 1.2K; ConocoPhillips Company/Bu 1.0K; COG Operating LLC 977 |
| WELLNAME | who | 19.7K | 0 | TI-STATE-158-95-3635H-4 120; MARMACONDA STATE 2-5-14-1 120; BB-SIVERTSON-LN- 151-95-1 120; SUNCLOUD 48 1 B 5WB 120 |
| DESCRIPTION | category | 7 | 0 | Groundwater, < 1000TDS 8.4K; Produced Water 8.0K; Surface Water, < 1000TDS 3.4K; Groundwater, > 1000TDS 2.6K |
| PERCENT | amount | 2.0K | 0 | 100.00 16.9K; 50.00 405; 0.00 249; 90.00 206 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05T21:36:25.63617 23.7K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 093fbe44-ace4-44cd-aa1e-a 23.7K |
| _SRC_FILE | who | 1 | 0 | WaterSource_1.csv 23.7K |
