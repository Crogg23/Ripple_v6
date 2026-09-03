# PORTAL_ARC_KENTUCKY_OPEN_GI_23E8E1668C

rows 2.0K  columns 35  scan 3.7s

roles: amount 2, audit 2, category 4, date 2, id 6, other 8, who 12

## when

MODDATE
  2021      1.5K  ##############################
  2022       484  ##########

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 2.0K | 36.53 | 38.06 | 39.09 | 39.12 | 75.8K |
| LONGITUDE | 2.0K | -89.22 | -85.51 | -82.62 | -82.42 | -170.9K |

## who

COMPANYNAM by rows
        13  Humana Inc
        11  Irving Materials Inc
         8  Xerox
         6  Bluegrass Materials Company LLC
         6  International Paper
         5  Berry Plastics Corporation
         3  H T Hackney
         3  Bluegrass Supply Chain Services
         3  Clariant Corporation
         3  BPM Lumber LLC
         3  Airgas Inc
         3  Florida Tile, Inc.
         3  Freedom Metals Inc
         3  Carhartt Inc
         3  Hitachi Automotive Systems Americas Inc
         3  ABF Freight System Inc
         2  Corvac Composites LLC
         2  Fruit of the Loom
         2  DecoArt Inc
         2  Ford Motor Company

COMPANYNAM by dollars
      496.78       13 rows  Humana Inc
      414.84       11 rows  Irving Materials Inc
      303.01        8 rows  Xerox
      228.57        6 rows  International Paper
      222.35        6 rows  Bluegrass Materials Company LLC
      187.76        5 rows  Berry Plastics Corporation
      114.63        3 rows  Clariant Corporation
      114.15        3 rows  Florida Tile, Inc.
      113.98        3 rows  Freedom Metals Inc
      113.31        3 rows  ABF Freight System Inc
         113        3 rows  Hitachi Automotive Systems Americas Inc
      112.95        3 rows  H T Hackney
      112.56        3 rows  Airgas Inc
      112.42        3 rows  Carhartt Inc
      111.42        3 rows  BPM Lumber LLC
      111.04        3 rows  Bluegrass Supply Chain Services
       78.06        2 rows  Forge Lumber
       77.89        2 rows  Duro Bag Manufacturing Company
       77.31        2 rows  Gusher Pumps
       77.23        2 rows  Expeditors International of Washington Inc

FACILITYNA by rows
        13  Humana Inc
        11  Irving Materials Inc
         9  Conduent
         6  Berry Global Inc.
         6  International Paper
         6  Bluegrass Materials Company LLC
         4  Lee Building Products
         4  Beam Suntory
         3  Essity
         3  Carhartt Inc
         3  ABF Freight System Inc
         3  Gusher Pumps
         3  Leggett & Platt Inc
         3  H T Hackney
         3  Clariant Corporation
         3  LSC Communications
         3  Freedom Metals Inc
         3  BPM Lumber LLC
         2  Florida Tile Inc
         2  Amazon.com KYDC LLC

FACILITYNA by dollars
      496.78       13 rows  Humana Inc
      414.84       11 rows  Irving Materials Inc
      341.01        9 rows  Conduent
      228.57        6 rows  International Paper
      224.52        6 rows  Berry Global Inc.
      222.35        6 rows  Bluegrass Materials Company LLC
      152.13        4 rows  Beam Suntory
      149.53        4 rows  Lee Building Products
      116.01        3 rows  Gusher Pumps
      114.63        3 rows  Clariant Corporation
      113.98        3 rows  Freedom Metals Inc
      113.77        3 rows  Leggett & Platt Inc
      113.31        3 rows  ABF Freight System Inc
      112.95        3 rows  H T Hackney
      112.73        3 rows  LSC Communications
      112.47        3 rows  Essity
      112.42        3 rows  Carhartt Inc
      111.42        3 rows  BPM Lumber LLC
       78.06        2 rows  Forge Lumber
       78.06        2 rows  Auto Vehicle Parts, LLC

MAIN_NAICS by rows
       121  551114
        88  493110
        50  332710
        41  323111
        40  336390
        35  511110
        33  326199
        30  332322
        30  327320
        30  312140
        29  212312
        29  321113
        27  332312
        26  541511
        23  321920
        23  484121
        23  518210
        21  333514
        19  811310
        18  561422

MAIN_NAICS by dollars
        4.6K      121 rows  551114
        3.3K       88 rows  493110
        1.9K       50 rows  332710
        1.6K       41 rows  323111
        1.5K       40 rows  336390
        1.3K       35 rows  511110
        1.2K       33 rows  326199
        1.1K       30 rows  312140
        1.1K       30 rows  327320
        1.1K       30 rows  332322
        1.1K       29 rows  212312
        1.1K       29 rows  321113
        1.0K       27 rows  332312
      991.04       26 rows  541511
      875.50       23 rows  518210
      872.19       23 rows  484121
      860.15       23 rows  321920
      795.35       21 rows  333514
      714.47       19 rows  811310
      686.90       18 rows  561110

NAICS6 by rows
       121  551114
        88  493110
        50  332710
        41  323111
        40  336390
        35  511110
        33  326199
        30  312140
        30  327320
        30  332322
        29  212312
        29  321113
        27  332312
        26  541511
        23  484121
        23  518210
        23  321920
        21  333514
        19  811310
        18  561422

NAICS6 by dollars
        4.6K      121 rows  551114
        3.3K       88 rows  493110
        1.9K       50 rows  332710
        1.6K       41 rows  323111
        1.5K       40 rows  336390
        1.3K       35 rows  511110
        1.2K       33 rows  326199
        1.1K       30 rows  312140
        1.1K       30 rows  327320
        1.1K       30 rows  332322
        1.1K       29 rows  212312
        1.1K       29 rows  321113
        1.0K       27 rows  332312
      991.04       26 rows  541511
      875.50       23 rows  518210
      872.19       23 rows  484121
      860.15       23 rows  321920
      795.35       21 rows  333514
      714.47       19 rows  811310
      686.90       18 rows  561110

## who x when

COMPANYNAM by MODDATE, dollars = LATITUDE
  ABF Freight System Inc                    2021:37.01 2022:76.30
  Airgas Inc                                2022:112.56
  BPM Lumber LLC                            2021:111.42
  Berry Plastics Corporation                2021:113.47 2022:74.29
  Bluegrass Materials Company LLC           2021:110.76 2022:111.59
  Bluegrass Supply Chain Services           2021:74.01 2022:37.03
  Carhartt Inc                              2021:112.42
  Clariant Corporation                      2021:114.63
  Corvac Composites LLC                     2021:74.43
  DecoArt Inc                               2021:75.65
  Duro Bag Manufacturing Company            2021:77.89
  Expeditors International of Washington I  2021:77.23
  Florida Tile, Inc.                        2021:114.15
  Ford Motor Company                        2021:76.44
  Forge Lumber                              2021:78.06
  Freedom Metals Inc                        2021:113.98
  Fruit of the Loom                         2021:73.96
  Gusher Pumps                              2021:77.31
  H T Hackney                               2021:74.65 2022:38.30
  Hitachi Automotive Systems Americas Inc   2021:113
  Humana Inc                                2021:496.78
  International Paper                       2021:191.64 2022:36.93
  Irving Materials Inc                      2021:339.29 2022:75.55
  Xerox                                     2021:266.15 2022:36.86

FACILITYNA by MODDATE, dollars = LATITUDE
  ABF Freight System Inc                    2021:37.01 2022:76.30
  Amazon.com KYDC LLC                       2021:75.96
  Auto Vehicle Parts, LLC                   2021:39.03 2022:39.03
  BPM Lumber LLC                            2021:111.42
  Beam Suntory                              2021:114.20 2022:37.93
  Berry Global Inc.                         2021:150.23 2022:74.29
  Bluegrass Materials Company LLC           2021:110.76 2022:111.59
  Carhartt Inc                              2021:112.42
  Clariant Corporation                      2021:114.63
  Conduent                                  2021:304.15 2022:36.86
  Essity                                    2021:75.43 2022:37.04
  Florida Tile Inc                          2021:76.14
  Forge Lumber                              2021:78.06
  Freedom Metals Inc                        2021:113.98
  Gusher Pumps                              2021:116.01
  H T Hackney                               2021:74.65 2022:38.30
  Humana Inc                                2021:496.78
  International Paper                       2021:191.64 2022:36.93
  Irving Materials Inc                      2021:339.29 2022:75.55
  LSC Communications                        2021:37.01 2022:75.72
  Lee Building Products                     2021:112.58 2022:36.95
  Leggett & Platt Inc                       2021:113.77

## what

MFG: 1 68%, 0 32%

NAICSCODE5: 561910 15%, 551114 15%, 339950 10%, 336350 10%, 541512 10%, 333514 10%, 332710 10%, 445210 5%, 323113 5%, 326111 5%, 722320 5%

NAICSCODE6: 332999 17%, 312120 17%, 541511 17%, 332710 11%, 325510 6%, 334510 6%, 332994 6%, 326199 6%, 611513 6%, 424120 6%, 541330 6%

FPOTMFGASP: 0 97%, 1 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID_1 | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| COMPANYID | who | 2.0K | 0 | 001t0000003smMm 10; 001t0000003skpL 10; 001t0000003sikm 10; 001t0000003sn4o 10 |
| COUNTY | who | 112 | 0 | Jefferson 470; Fayette 153; Boone 117; Kenton 67 |
| FACILITYNA | who | 1.8K | 0 | Humana Inc 20; Irving Materials Inc 18; Lee Building Products 13; International Paper 13 |
| ADDRESS | id | 2.0K | 0 | 4564 US HWY 60 W, Lewispo 10; 840 Licking Pike, Wilder, 10; 2400 Arbor Tech Drive, He 10; 112 Walter Jetton Blvd, P 10 |
| PRODUCTSSE | other | 1.9K | 1 | Newspaper publishing 16; Ready-mixed concrete 14; Headquarters 13; Crushed limestone 13 |
| EMPLOYEES | other | 321 | 0 | 15 58; 10 48; 8 47; 20 46 |
| YREST | other | 150 | 0 | 1999 60; 0 48; 1988 44; 1989 44 |
| LATITUDE | amount | 1.9K | 0 | 38.979277 11; 37.929445 10; 39.034386 10; 39.065278 10 |
| LONGITUDE | amount | 2.0K | 0 | -84.58955 11; -86.827635 10; -84.484404 10; -84.632534 10 |
| IMPORTKBIF | id | 2.0K | 0 | 0 14; 6393 10; 95 10; 264318100 10 |
| COMPANYNAM | who | 1.9K | 0 | Humana Inc 20; Irving Materials Inc 18; International Paper 13; Louisville Fire Brick Wor 11 |
| PHONE | id | 1.9K | 17 | (502) 580-1000 17; 270-898-7392 11; 270-295-3955 10; 859-441-7400 10 |
| WEBSITE | other | 1.6K | 182 | www.irvmat.com 19; www.humana.com 19; www.leebp.com 12; www.internationalpaper.co 12 |
| BYPRODUCTS | other | 182 | 1.8K | Recycled paper 2; Blocks filled in forms fo 2; Dried Grains 2; chips ,sawdust, bark 1 |
| MODDATE | date | 132 | 0 | 1639353600000 769; 1641254400000 133; 1634083200000 123; 1640131200000 118 |
| MFG | category | 2 | 0 | 1 1.4K; 0 646 |
| NAICSCODE1 | who | 410 | 0 | 551114 121; 493110 88; 332710 50; 323111 41 |
| NAICSCODE2 | who | 306 | 1.2K | 493110 52; 551114 38; 326199 21; 811310 19 |
| NAICSCODE3 | who | 148 | 1.7K | 493110 21; 551114 17; 811310 8; 541614 7 |
| NAICSCODE4 | other | 76 | 1.9K | 333514 4; 493110 4; 332710 4; 551114 4 |
| NAICSCODE5 | category | 35 | 2.0K | 561910 3; 551114 3; 339950 2; 336350 2 |
| NAICSCODE6 | category | 36 | 2.0K | 332999 3; 312120 3; 541511 3; 332710 2 |
| MAIN_NAICS | who | 410 | 0 | 551114 121; 493110 88; 332710 50; 323111 41 |
| NAICS6 | who | 410 | 0 | 551114 121; 493110 88; 332710 50; 323111 41 |
| NAICSNATLI | who | 404 | 0 | Corporate, Subsidiary, an 121; General Warehousing and S 88; Machine Shops 50; Commercial Printing (exce 41 |
| NAICSNAT_1 | who | 404 | 0 | Managing Offices 121; General Warehousing and S 88; Machine Shops 50; Commercial Printing (exce 41 |
| FPOTMFGASP | category | 2 | 0 | 0 1.9K; 1 54 |
| YRRMVD | other | 1 | 0 | 0 2.0K |
| ESRI_OID | other | 395 | 0 | 847 121; 696 88; 347 50; 237 41 |
| GEOMETRY | id | 2.0K | 0 | {"type": "Point", "coordi 11; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:33:29.19869 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 444cd4d0-748c-4a3a-b566-8 2.0K |
| SRC_SHA256 | who | 1 | 0 | 775f24c1574ad5acbaa268005 2.0K |
