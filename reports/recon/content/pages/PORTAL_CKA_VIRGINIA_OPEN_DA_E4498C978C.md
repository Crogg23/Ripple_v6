# PORTAL_CKA_VIRGINIA_OPEN_DA_E4498C978C

rows 1.5K  columns 21  scan 4.4s

roles: amount 2, audit 2, category 4, date 4, empty 1, id 2, other 4, who 3

## when

PRP_REPORT_RECEIVED_DATE_TIME
  2020         1  
  2021       122  ########
  2022       208  #############
  2023       294  ###################
  2024       241  ###############
  2025       473  ##############################
  2026       161  ##########

PRP_INCIDENT_DATE_TIME
  2021       115  ########
  2022       193  ##############
  2023       266  ###################
  2024       222  ################
  2025       420  ##############################
  2026       139  ##########

PRP_INCIDENT_CLOSURE_DATE
  2021        80  ######
  2022       238  #################
  2023       288  ####################
  2024       242  #################
  2025       426  ##############################
  2026       184  #############

INGESTED_AT
  2026      1.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 1.5K | -9.27M | -8.66M | -8.46M | -8.39M | -13.09B |
| Y | 1.5K | 4.38M | 4.48M | 4.75M | 4.77M | 6.77B |

## who

PRP_SITE_NAME by rows
        41  Bristol landfill - Bristol - odor
        16  SSO - WVWA
        13  SSO - HCPSA
        10  SSO - Alleghany County
         9  SSO - City of Salem
         8  SSO - City of Lynchburg
         7  SSO - Town of Christiansburg
         5  SSO - City of Danville
         5  TTA Diesel - Unknown RP
         4  Uncovered Poultry Litter
         4  SSO - City of Covington
         3  Bristol landfill - Bristol-Odor
         3  SSO - Town of Pulaski
         3  SSO - PCPSA
         3  Bristol landfill-Bristol-odor
         3  Bristol Landfill - Bristol-Odor
         3  Dominion Lakes Odor Concerns
         3  PDV - 4000 Coast Guard Blvd - Portsmouth
         3  MVP -
         3  Chemical Odor Concern - Boxley Materials

PRP_SITE_NAME by dollars
      -8.39M        1 rows  Chincoteague Marina - Unknown Sheen
      -8.40M        1 rows  Vessel Releasing Unknown Fluids - 3415 Bayside Drive - Accom
      -8.40M        1 rows  3324 Starboard St. Greenbackville
      -8.40M        1 rows  Land disturbance and runnoff - 6029 Willow Dr. Horntown
      -8.40M        1 rows  PDV - Atlantic Ocean - Virginia Beach
      -8.40M        1 rows  3 Gallons of Motor Oil to Tidal Marsh - 2502 Fleming Road - 
      -8.41M        1 rows  Ish Farm LLC - VPG250125
      -8.43M        1 rows  30442 Madison Ave - Keller
      -8.43M        1 rows  Diesel Release - 31390 Lankford Hwy - Accomack Co
      -8.44M        1 rows  12210 Houston St. Exmore - SSO
      -8.44M        1 rows  Poultry Waste Managment and Antibiotics - Harborton
      -8.45M        1 rows  David's Nursery - Exmore - Hydraulic oil
      -8.45M        1 rows  TTA - US-13 NB @ Bell Ln
      -8.45M        1 rows  Wilsonia Neck Rd. Machipango - Open Burning
      -8.46M        1 rows  Home Heating Oil - 4184 Sunnyside Rd. Cheriton
      -8.46M        1 rows  Sunken Vessel - 524 Fishermans Bend Pacific Ave - Virginia B
      -8.46M        1 rows  HRSD Atlantic STP - Contact Tank Water Release
      -8.46M        1 rows  Private SSO - 333 Lake Dr - Virginia Beach
      -8.46M        1 rows  19th St and Atlantic Ave
      -8.46M        1 rows  Unknown Fuel Release - 1501 Mediterranean Ave - Virginia Bea

PRP_SITE_CITY by rows
        74  Norfolk
        73  Bristol
        60  Virginia Beach
        41  Chesapeake
        34  Roanoke
        32  Portsmouth
        30  Richmond
        25  Newport News
        25  Suffolk
        23  Covington
        19  Hampton
        18  Lynchburg
        17  Alexandria
        16  Abingdon
        16  Manassas
        16  Staunton
        14  Williamsburg
        14  Charlottesville
        14  Front Royal
        13  Salem

PRP_SITE_CITY by dollars
      -8.39M        1 rows  Chincoteague Island
      -8.40M        1 rows  Horntown
      -8.40M        1 rows  New Church
      -8.41M        1 rows  Oak Hall
      -8.43M        1 rows  Keller
      -8.43M        1 rows  Painter
      -8.44M        1 rows  Harborton
      -8.45M        1 rows  Machipongo
      -8.46M        1 rows  Cheriton
      -8.46M        1 rows  Tangier
      -8.49M        1 rows  Moon
      -8.49M        1 rows  Chespeake
      -8.49M        1 rows  Fort Monroe
      -8.50M        1 rows  Kilmarnock
      -8.50M        1 rows  Poquoson
      -8.51M        1 rows  Weems
      -8.51M        1 rows  James Store
      -8.52M        1 rows  Gloucester Point
      -8.52M        1 rows  CALLAO
      -8.52M        1 rows  Kinsale

SRC_SHA256 by rows
      1.5K  28e0c366edb26808c635bc9824e674197a8e29260bdf4e1e04ba233f8022378f

SRC_SHA256 by dollars
     -13.09B     1.5K rows  28e0c366edb26808c635bc9824e674197a8e29260bdf4e1e04ba233f8022

## who x when

PRP_SITE_NAME by PRP_REPORT_RECEIVED_DATE_TIME, dollars = X
  12210 Houston St. Exmore - SSO            2025:-8.44M
  3 Gallons of Motor Oil to Tidal Marsh -   2024:-8.40M
  30442 Madison Ave - Keller                2022:-8.43M
  3324 Starboard St. Greenbackville         2022:-8.40M
  Bristol Landfill - Bristol-Odor           2021:-27.44M
  Bristol landfill - Bristol - odor         2021:-128.03M 2022:-246.92M
  Bristol landfill - Bristol-Odor           2021:-27.44M
  Bristol landfill-Bristol-odor             2021:-27.44M
  Chemical Odor Concern - Boxley Materials  2023:-26.11M
  Chincoteague Marina - Unknown Sheen       2022:-8.39M
  Diesel Release - 31390 Lankford Hwy - Ac  2024:-8.43M
  Dominion Lakes Odor Concerns              2023:-25.48M
  Ish Farm LLC - VPG250125                  2022:-8.41M
  Land disturbance and runnoff - 6029 Will  2026:-8.40M
  MVP -                                     2024:-17.89M 2025:-8.92M
  PDV - 4000 Coast Guard Blvd - Portsmouth  2025:-17.00M 2026:-8.50M
  PDV - Atlantic Ocean - Virginia Beach     2025:-8.40M
  SSO - Alleghany County                    2023:-44.50M 2024:-26.67M 2025:-17.81M
  SSO - City of Covington                   2022:-8.90M 2024:-8.90M 2025:-8.90M 2026:-8.90M
  SSO - City of Danville                    2023:-17.67M 2024:-8.84M 2025:-8.84M 2026:-8.83M
  SSO - City of Lynchburg                   2021:-8.81M 2022:-8.81M 2024:-17.63M 2025:-35.25M
  SSO - City of Salem                       2022:-8.92M 2024:-35.65M 2025:-35.65M
  SSO - HCPSA                               2021:-26.69M 2022:-35.56M 2023:-35.59M 2025:-17.81M
  SSO - PCPSA                               2021:-8.96M 2022:-8.96M 2025:-8.96M
  SSO - Town of Christiansburg              2021:-8.94M 2023:-17.90M 2024:-26.84M 2025:-8.95M
  SSO - Town of Pulaski                     2023:-8.99M 2025:-17.98M
  SSO - WVWA                                2021:-8.90M 2022:-26.70M 2023:-35.60M 2024:-35.60M 2025:-35.60M
  TTA Diesel - Unknown RP                   2022:-8.62M 2023:-17.18M 2025:-17.20M
  Uncovered Poultry Litter                  2021:-8.79M 2022:-17.53M 2023:-8.78M
  Vessel Releasing Unknown Fluids - 3415 B  2023:-8.40M

PRP_SITE_CITY by PRP_REPORT_RECEIVED_DATE_TIME, dollars = X
  Abingdon                                  2021:-27.37M 2022:-9.13M 2023:-18.26M 2024:-9.13M 2025:-73.01M 2026:-9.14M
  Alexandria                                2021:-17.16M 2022:-34.32M 2023:-25.74M 2024:-34.34M 2025:-34.31M
  Bristol                                   2021:-310.93M 2022:-274.36M 2023:-18.29M 2024:-9.15M 2025:-54.89M
  Charlottesville                           2022:-17.46M 2023:-17.47M 2024:-8.75M 2025:-52.43M 2026:-26.23M
  Cheriton                                  2025:-8.46M
  Chesapeake                                2021:-25.46M 2022:-16.99M 2023:-76.47M 2024:-25.47M 2025:-152.89M 2026:-50.97M
  Chincoteague Island                       2022:-8.39M
  Covington                                 2021:-17.81M 2022:-17.81M 2023:-44.52M 2024:-53.43M 2025:-62.31M 2026:-8.90M
  Front Royal                               2021:-8.71M 2022:-8.71M 2023:-26.11M 2025:-69.54M 2026:-8.70M
  Hampton                                   2022:-33.99M 2023:-42.50M 2024:-17.00M 2025:-59.50M 2026:-8.49M
  Harborton                                 2026:-8.44M
  Horntown                                  2026:-8.40M
  Keller                                    2022:-8.43M
  Lynchburg                                 2021:-17.63M 2022:-8.81M 2023:-26.44M 2024:-35.26M 2025:-52.88M 2026:-17.63M
  Machipongo                                2025:-8.45M
  Manassas                                  2021:-17.25M 2022:-25.89M 2023:-25.89M 2025:-51.75M 2026:-17.25M
  New Church                                2024:-8.40M
  Newport News                              2021:-25.53M 2023:-34.04M 2024:-42.57M 2025:-85.16M 2026:-25.53M
  Norfolk                                   2021:-42.44M 2022:-59.45M 2023:-169.83M 2024:-110.42M 2025:-178.33M 2026:-67.93M
  Oak Hall                                  2022:-8.41M
  Painter                                   2024:-8.43M
  Portsmouth                                2021:-17.00M 2022:-33.99M 2023:-42.49M 2024:-67.98M 2025:-59.48M 2026:-50.98M
  Richmond                                  2022:-8.62M 2023:-60.41M 2024:-60.38M 2025:-86.20M 2026:-43.09M
  Roanoke                                   2021:-17.80M 2022:-80.10M 2023:-71.19M 2024:-26.71M 2025:-80.09M 2026:-26.70M
  Salem                                     2022:-8.92M 2023:-8.91M 2024:-35.65M 2025:-44.56M 2026:-17.83M
  Staunton                                  2022:-44.01M 2023:-35.21M 2025:-61.62M
  Suffolk                                   2021:-42.62M 2023:-42.59M 2024:-25.56M 2025:-76.74M 2026:-25.60M
  Tangier                                   2023:-8.46M
  Virginia Beach                            2021:-33.90M 2022:-59.30M 2023:-127.05M 2024:-59.25M 2025:-143.94M 2026:-84.69M
  Williamsburg                              2021:-8.54M 2022:-17.08M 2023:-8.54M 2025:-51.23M 2026:-34.16M

## what

REFERENCE_POINT: PG 86%, FC 14%

RSC_STATUS_DESCRIPTION: Closed 97%, Under Investigation 3%

SRC_STATUS_REASON_DESC: Appropriate compliance actions 32%, Pollution report being managed 16%, SSO/CSO/Bypass being tracked u 11%, Joint jurisdiction. Notified a 11%, No release observed. 9%, Not within DEQ jurisdiction. R 7%, No compliance issue observed. 5%, Corrective actions taken by Re 3%, No additional action required  3%, Duplicate pollution report. 2%, Insufficient info provided in  1%

PRP_SITE_STATE: VA 100%, TN 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 1.4K | 0 | -9145177.1391 65; -8837434.0098 8; -8785079.8317 8; -8976592.676 8 |
| Y | amount | 1.4K | 0 | 4383659.1823 65; 4387486.179 8; 4591659.4703 8; 4379917.4173 8 |
| OBJECTID | id | 1.5K | 0 | 1500 8; 1499 8; 1498 8; 1497 8 |
| REFERENCE_POINT | category | 2 | 0 | PG 1.3K; FC 217 |
| PRP_REPORT_ID | id | 1.5K | 0 | 320743 8; 320740 8; 320732 8; 320675 8 |
| PRP_REPORT_RECEIVED_DATE_TIME | date | 1.5K | 0 | 2025-05-15T00:00:00 11; 2025-02-18T12:26:00 9; 2025-09-25T11:45:00 8; 2025-09-25T12:40:00 8 |
| PRP_INCIDENT_DATE_TIME | date | 1.3K | 145 | 2025-09-23T14:55:00 7; 2025-09-25T10:00:00 7; 2025-09-24T14:55:00 7; 2025-09-19T14:05:00 7 |
| PRP_INCIDENT_CLOSURE_DATE | date | 1.4K | 42 | 2025-09-26T08:45:37 8; 2025-10-06T10:30:40 8; 2025-10-17T10:42:39 8; 2025-09-25T15:08:53 8 |
| RSC_STATUS_DESCRIPTION | category | 2 | 0 | Closed 1.5K; Under Investigation 44 |
| SRC_STATUS_REASON_DESC | category | 16 | 44 | Appropriate compliance ac 468; Pollution report being ma 232; SSO/CSO/Bypass being trac 155; Joint jurisdiction. Notif 152 |
| PRP_SITE_NAME | who | 1.3K | 0 | Bristol landfill - Bristo 41; SSO - WVWA 16; SSO - HCPSA 13; SSO - Alleghany County 11 |
| PRP_SITE_ADDRESS1 | other | 1.3K | 45 | 2655 Valley Dr 32; 2655 Valley Drive 28; 4000 Coast Guard Boulevar 9; 148 Andes Dr 8 |
| PRP_SITE_ADDRESS2 | other | 96 | 1.4K | Willis Rd 2; Bldg 3165 Suite 100 2; Lilleigh Court 1; Also reported as 5100 Woo 1 |
| PRP_SITE_CITY | who | 370 | 33 | Norfolk 74; Bristol 73; Virginia Beach 60; Chesapeake 41 |
| PRP_SITE_STATE | category | 2 | 0 | VA 1.5K; TN 1 |
| PRP_SITE_ZIP_CODE | other | 415 | 435 | 24426 23; 23511 18; 23434 16; 23451 13 |
| PRP_ASSIGNED_STAFF_PROGRAM_ID | other | 143 | 6 | 627 134; 235 103; 548 94; 540 73 |
| DATA_DISCLAIMER | empty | 1 | 1.5K |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:55:12.26863 1.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 3f274f37-203d-4d2b-ac2f-d 1.5K |
| SRC_SHA256 | who | 1 | 0 | 28e0c366edb26808c635bc982 1.5K |
