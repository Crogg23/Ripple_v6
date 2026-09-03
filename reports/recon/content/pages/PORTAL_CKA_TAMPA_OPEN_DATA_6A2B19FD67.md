# PORTAL_CKA_TAMPA_OPEN_DATA_6A2B19FD67

rows 477  columns 13  scan 3.7s

roles: amount 1, audit 2, category 5, date 2, other 1, who 3

## when

DATE
  2021        32  ####
  2022        52  #######
  2023        45  ######
  2024        53  #######
  2025        78  ###########
  2026       217  ##############################

INGESTED_AT
  2026       477  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 477 | 0 | 83.90 | 655.5K | 689.3K | 37.42M |

## who

C_ORGANIZATION by rows
       477  Wastewater Department

C_ORGANIZATION by dollars
      37.42M      477 rows  Wastewater Department

PERIOD by rows
        10  10/2025
        10  9/2026
        10  8/2026
        10  11/2025
        10  12/2025
        10  3/2026
        10  2/2026
        10  6/2026
        10  1/2026
        10  7/2026
        10  4/2026
        10  5/2026
         6  FY 2017
         6  FY 2025
         6  FY 2016
         6  FY 2023
         6  FY 2018
         6  FY 2022
         6  FY 2026
         6  FY 2024

PERIOD by dollars
      616.2K        4 rows  FY-2023
      603.7K        4 rows  FY-2025
      592.9K        4 rows  FY-2026
      590.3K        4 rows  FY-2024
      587.8K        4 rows  FY-2022
      579.6K        4 rows  FY-2018
      578.3K        4 rows  FY-2021
      569.3K        4 rows  FY-2019
      547.3K        4 rows  FY-2020
       14.8K        6 rows  FY 2019
       14.7K        6 rows  FY 2023
       14.6K        6 rows  FY 2018
       14.6K        6 rows  FY 2020
       14.5K        6 rows  FY 2022
       13.7K        6 rows  FY 2021
       12.3K        4 rows  FY 2014
       12.3K        6 rows  FY 2025
       12.1K        6 rows  FY 2017
       11.9K        4 rows  FY 2013
       11.7K        6 rows  FY 2024

SRC_SHA256 by rows
       477  92644be2ee1521597c77c1134f823508d156ee1ea78cf8731ad34c71411a30c0

SRC_SHA256 by dollars
      37.42M      477 rows  92644be2ee1521597c77c1134f823508d156ee1ea78cf8731ad34c71411a

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Wastewater Department                     2021:4.65M 2022:7.76M 2023:6.06M 2024:7.74M 2025:7.47M 2026:3.72M

PERIOD by DATE, dollars = VALUE
  1/2026                                    2026:534.41
  10/2025                                   2025:179.50
  11/2025                                   2025:297.17
  12/2025                                   2025:420.84
  2/2026                                    2026:650.86
  3/2026                                    2026:755.91
  4/2026                                    2026:837.52
  5/2026                                    2026:920.13
  6/2026                                    2026:995.18
  7/2026                                    2026:1.0K
  8/2026                                    2026:422.34
  9/2026                                    2026:460
  FY 2016                                   2026:11.5K
  FY 2017                                   2026:12.1K
  FY 2018                                   2026:14.6K
  FY 2019                                   2026:14.8K
  FY 2022                                   2026:14.5K
  FY 2023                                   2026:14.7K
  FY 2024                                   2026:11.7K
  FY 2025                                   2026:12.3K
  FY 2026                                   2026:7.2K
  FY-2018                                   2021:579.6K
  FY-2019                                   2021:569.3K
  FY-2020                                   2021:547.3K
  FY-2021                                   2021:578.3K
  FY-2022                                   2021:587.8K
  FY-2023                                   2022:616.2K
  FY-2024                                   2023:75.90 2024:590.2K
  FY-2025                                   2024:603.7K
  FY-2026                                   2026:592.9K

## what

CHARTNAME: Wastewater AWTP Average Wastew 14%, Wastewater AWTP Average Wastew 14%, Wastewater AWTP Laboratory Ana 14%, Wastewater AWTP Nitrogen Remov 13%, Wastewater Cave In Repairs by  6%, Wastewater Grease Traps Inspec 6%, Wastewater Inspect Manholes by 6%, Wastewater Inspect Gravity Sew 6%, Wastewater Howard F. Curren AW 6%, Wastewater Clean Gravity Sewer 6%, Wastewater Cave In Repairs by  6%, Wastewater Inspect Manholes by 4%

DESCRIPTION: Wastewater Cave In Repairs by  11%, Wastewater Grease Traps Inspec 11%, Wastewater Inspect Manholes by 11%, Wastewater Inspect Gravity Sew 11%, Wastewater Howard F. Curren AW 11%, Wastewater Clean Gravity Sewer 11%, Wastewater Cave In Repairs by  10%, Wastewater Inspect Manholes by 7%, Wastewater Grease Traps Inspec 6%, Wastewater Inspect Gravity Sew 6%, Wastewater Clean Gravity Sewer 6%

CATEGORY: Million Gallons 27%, Analyses 13%, Pounds 13%, Annual Goal 10%, % of Annual Goal 10%, Flow (MGD) 5%, DEPRESSIONS 5%, CAVE INS 5%, Sewer Manholes Inspected 3%, # of Inspections 3%, Miles Inspected 3%, Miles Cleaned 3%

SUMMARY: Total 80%, Percent 20%

TYPEDATA: Date 51%, Period 49%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 474 | 0 | 722702 3; 722701 3; 722700 3; 722699 3 |
| C_ORGANIZATION | who | 1 | 0 | Wastewater Department 477 |
| CHARTNAME | category | 19 | 0 | Wastewater AWTP Average W 56; Wastewater AWTP Average W 55; Wastewater AWTP Laborator 54; Wastewater AWTP Nitrogen  53 |
| DESCRIPTION | category | 12 | 254 | Wastewater Cave In Repair 24; Wastewater Grease Traps I 24; Wastewater Inspect Manhol 24; Wastewater Inspect Gravit 24 |
| CATEGORY | category | 12 | 0 | Million Gallons 129; Analyses 63; Pounds 62; Annual Goal 48 |
| SUMMARY | category | 2 | 0 | Total 381; Percent 96 |
| TYPEDATA | category | 2 | 0 | Date 242; Period 235 |
| DATE | date | 97 | 0 | 07/02/2026 12:12:00 79; 05/01/2026 00:00:00 14; 04/01/2026 00:00:00 14; 03/01/2026 00:00:00 14 |
| PERIOD | who | 59 | 218 | 9/2026 10; 8/2026 10; 7/2026 10; 6/2026 10 |
| VALUE | amount | 386 | 0 | 0.000 13; 90.000 8; 13.100 6; 224.000 5 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:20:59.31421 477 |
| SOURCE_RUN_ID | audit | 1 | 0 | acf6797f-9ac2-4493-84c2-b 477 |
| SRC_SHA256 | who | 1 | 0 | 92644be2ee1521597c77c1134 477 |
