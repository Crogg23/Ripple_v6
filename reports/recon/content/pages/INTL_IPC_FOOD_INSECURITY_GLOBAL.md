# INTL_IPC_FOOD_INSECURITY_GLOBAL

rows 735  columns 12  scan 2.8s

roles: amount 2, audit 2, category 4, date 2, other 1, who 1

## when

C_FROM
  2021        42  ####
  2022         7  #
  2023         7  #
  2024        28  ###
  2025       329  ##############################
  2026       322  #############################

C_TO
  2021        28  ##
  2022        21  ##
  2024        28  ##
  2025       252  ####################
  2026       385  ##############################
  2027        21  ##

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_COUNTRY_POPULATION | 735 | 0 | 18.08M | 256.77M | 256.77M | 24.13B |
| PERCENTAGE | 735 | 0 | 0.18 | 1 | 1 | 229.47 |

## who

SRC_SHA256 by rows
       735  c07a949bab8f676af92012bb4dff7d2085c69f39b64328d5904f00db98725030

SRC_SHA256 by dollars
      24.13B      735 rows  c07a949bab8f676af92012bb4dff7d2085c69f39b64328d5904f00db9872

## who x when

SRC_SHA256 by C_FROM, dollars = TOTAL_COUNTRY_POPULATION
  c07a949bab8f676af92012bb4dff7d2085c69f39  2021:2.15B 2022:44.28M 2023:9.38M 2024:406.52M 2025:7.93B 2026:13.59B

## what

DATE_OF_ANALYSIS: Nov 2025 30%, Mar 2026 13%, Oct 2025 10%, Apr 2026 8%, Mar 2025 7%, Aug 2025 6%, Feb 2026 6%, May 2025 6%, Jun 2025 5%, Aug 2021 3%, Jan 2026 3%, Jul 2025 3%

COUNTRY: YEM 9%, SLV 9%, SDN 9%, NAM 9%, HND 9%, GTM 9%, ECU 9%, DOM 9%, BDI 9%, AFG 9%, ZMB 6%, UGA 6%

VALIDITY_PERIOD: first projection 47%, current 43%, second projection 10%

PHASE: 5 14%, 4 14%, 3 14%, 2 14%, 1 14%, 3+ 14%, all 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DATE_OF_ANALYSIS | category | 21 | 0 | Nov 2025 182; Mar 2026 77; Oct 2025 63; Apr 2026 49 |
| COUNTRY | category | 50 | 0 | YEM 21; SLV 21; SDN 21; NAM 21 |
| TOTAL_COUNTRY_POPULATION | amount | 49 | 0 | 0 28; 35312824 21; 6325827 21; 47535794 21 |
| VALIDITY_PERIOD | category | 3 | 0 | first projection 343; current 315; second projection 77 |
| C_FROM | date | 29 | 0 | 2025-10-01 161; 2026-06-01 126; 2026-04-01 84; 2025-05-01 35 |
| C_TO | date | 30 | 0 | 2026-08-31 126; 2025-12-31 126; 2026-03-31 77; 2025-09-30 49 |
| PHASE | category | 7 | 0 | 5 105; 4 105; 3 105; 2 105 |
| NUMBER | other | 513 | 0 | 0 127; 10479422 5; 6325827 5; 10073915 4 |
| PERCENTAGE | amount | 79 | 0 | 0 154; 1.0 105; 0.01 28; 0.16 20 |
| INGESTED_AT | audit | 1 | 0 | 1782620032052404 735 |
| SOURCE_RUN_ID | audit | 1 | 0 | 4f50951f-b7e7-44fa-a397-9 735 |
| SRC_SHA256 | who | 1 | 0 | c07a949bab8f676af92012bb4 735 |
