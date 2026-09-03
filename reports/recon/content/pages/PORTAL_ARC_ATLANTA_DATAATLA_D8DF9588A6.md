# PORTAL_ARC_ATLANTA_DATAATLA_D8DF9588A6

rows 15  columns 22  scan 3.2s

roles: amount 3, audit 2, category 11, date 4, other 2, who 1

## when

FINAL_UPDA
  2008         1  ###############
  2009         1  ###############
  2013         1  ###############
  2014         1  ###############
  2018         2  ##############################
  2020         1  ###############

CREATED_DATE
  2018        14  ##############################
  2020         1  ##

LAST_EDITED_DATE
  2021        15  ##############################

INGESTED_AT
  2026        15  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| ACRES | 15 | 0.70 | 6.38 | 209.77 | 235.75 | 381.71 |
| SHAPE__AREA | 15 | 30.7K | 278.1K | 9.14M | 10.27M | 16.63M |
| SHAPE__LENGTH | 15 | 974.54 | 2.5K | 65.6K | 74.2K | 120.5K |

## who

SRC_SHA256 by rows
        15  c4ef245dcafc3df064ff4bc5142d04bea3b2349355795fa5f67665971378d853

SRC_SHA256 by dollars
      381.71       15 rows  c4ef245dcafc3df064ff4bc5142d04bea3b2349355795fa5f67665971378

## who x when

SRC_SHA256 by CREATED_DATE, dollars = ACRES
  c4ef245dcafc3df064ff4bc5142d04bea3b23493  2018:370.78 2020:10.93

## what

OBJECTID: 15 8%, 14 8%, 13 8%, 12 8%, 11 8%, 10 8%, 9 8%, 8 8%, 7 8%, 6 8%, 5 8%, 4 8%

FROM_ZONE: I2 53%, I-2 20%, I1, I2 7%, VARIOUS 7%, PDMU 7%, I1 7%

TO_ZONE: MR-4A 20%, MR-4A-C 20%, PD-MU 13%, MRC-3 7%, SPI-23 7%, MR-5B 7%, MR-2-C 7%, MR-4B 7%, O-I 7%, MRC-3-C 7%

DOCKET_NO: Z-06-135 8%, Z-12-002 8%, Z-06-139 8%, Z-07-102 8%, Z-20-028 8%, Z-08-039 8%, Z-08-063 8%, Z-08-077 8%, Z-07-105 8%, Z-13-052 8%, Z-17-083 8%, Z-07-016 8%

STATUS: COMPLETE 47%, nan 33%, FILED 13%, APPROVED 7%

STATUS_SUBTYPE: 2 73%, 4 27%

ORDINANCE: nan 40%, 12-O-0157 7%, 07-O-0149 7%, 08-O-0524 7%, 08-O-1767 7%, 14-O-1043 7%, 18-O-1008 7%, 07-O-0599 7%, 18-O-1289 7%, 06-O-0577 7%

ORDHYPERLINK: nan 40%, https://aimewebapp.blob.core.w 7%, https://aimewebapp.blob.core.w 7%, https://aimewebapp.blob.core.w 7%, https://aimewebapp.blob.core.w 7%, https://aimewebapp.blob.core.w 7%, https://aimewebapp.blob.core.w 7%, https://aimewebapp.blob.core.w 7%, https://aimewebapp.blob.core.w 7%, https://aimewebapp.blob.core.w 7%

GLOBALID: 66e77a83-5fa5-4f23-8834-1d0147 8%, a6d02140-de43-446e-8b1a-9e854a 8%, 388fad74-911b-4f34-b954-f3c16f 8%, 60d15f72-9833-442d-9aba-392d58 8%, f66badb1-fcc0-4438-b6ac-b835fd 8%, c8b126ee-4c88-4a25-845b-22ea2e 8%, 588cb8c8-c6fa-4965-a107-40f9bb 8%, d1890cf3-5266-48e4-9cd4-889174 8%, b14c802d-6ccc-4e31-bb2e-b8e291 8%, aeaf8a3e-c8ae-44a7-85b2-e45191 8%, 1454a9c0-d88b-453e-92b6-0b0344 8%, 75c3db84-9922-4fda-971d-5d60f3 8%

STATUSTYPE: Complete 73%, Filed 27%

GEOMETRY: {"type": "MultiPolygon", "coor 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%, {"type": "Polygon", "coordinat 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | category | 15 | 0 | 15 1; 14 1; 13 1; 12 1 |
| FROM_ZONE | category | 6 | 0 | I2 8; I-2 3; I1, I2 1; VARIOUS 1 |
| TO_ZONE | category | 10 | 0 | MR-4A 3; MR-4A-C 3; PD-MU 2; MRC-3 1 |
| DOCKET_NO | category | 15 | 0 | Z-06-135 1; Z-12-002 1; Z-06-139 1; Z-07-102 1 |
| STATUS | category | 4 | 0 | COMPLETE 7; nan 5; FILED 2; APPROVED 1 |
| FINAL_UPDA | date | 8 | 0 | nan 8; 1402272000000.0 1; 1199318400000.0 1; 1600992000000.0 1 |
| STATUS_SUBTYPE | category | 2 | 0 | 2 11; 4 4 |
| ORDINANCE | category | 10 | 0 | nan 6; 12-O-0157 1; 07-O-0149 1; 08-O-0524 1 |
| ORDHYPERLINK | category | 10 | 0 | nan 6; https://aimewebapp.blob.c 1; https://aimewebapp.blob.c 1; https://aimewebapp.blob.c 1 |
| CREATED_USER | other | 1 | 0 | GIS 15 |
| CREATED_DATE | date | 2 | 0 | 1524574527000 14; 1584629821000 1 |
| LAST_EDITED_USER | other | 1 | 0 | GIS 15 |
| LAST_EDITED_DATE | date | 5 | 0 | 1610562389000 5; 1610562390000 5; 1610562394000 2; 1610562388000 2 |
| GLOBALID | category | 15 | 0 | 66e77a83-5fa5-4f23-8834-1 1; a6d02140-de43-446e-8b1a-9 1; 388fad74-911b-4f34-b954-f 1; 60d15f72-9833-442d-9aba-3 1 |
| STATUSTYPE | category | 2 | 0 | Complete 11; Filed 4 |
| ACRES | amount | 15 | 0 | 50.20185946 1; 5.60793911 1; 8.33958115 1; 5.27638552 1 |
| SHAPE__AREA | amount | 15 | 0 | 2186784.2521972656 1; 244280.85009765625 1; 363270.7019042969 1; 229838.4345703125 1 |
| SHAPE__LENGTH | amount | 15 | 0 | 12400.897595578484 1; 2713.011351296809 1; 2348.2836201343257 1; 2115.801673510814 1 |
| GEOMETRY | category | 15 | 0 | {"type": "MultiPolygon",  1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1; {"type": "Polygon", "coor 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:46:49.85401 15 |
| SOURCE_RUN_ID | audit | 1 | 0 | c710f37f-07a2-40b7-9b98-6 15 |
| SRC_SHA256 | who | 1 | 0 | c4ef245dcafc3df064ff4bc51 15 |
