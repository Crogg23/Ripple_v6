# PORTAL_CKA_TAMPA_OPEN_DATA_E290DD0B04

rows 44  columns 13  scan 3.5s

roles: amount 1, audit 2, category 4, date 2, empty 1, other 1, who 3

## when

DATE
  2021        23  ##############################
  2022         5  #######
  2023         4  #####
  2024         4  #####
  2025         4  #####
  2026         4  #####

INGESTED_AT
  2026        44  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 44 | 17 | 107.0K | 290.38M | 293.93M | 1.78B |

## who

C_ORGANIZATION by rows
        44  Contract Administration (Contract Administration)

C_ORGANIZATION by dollars
       1.78B       44 rows  Contract Administration (Contract Administration)

TYPEDATA by rows
        44  Period

TYPEDATA by dollars
       1.78B       44 rows  Period

SRC_SHA256 by rows
        44  6891416b923082bb3e7ab6991163ce4ad394b3fc79659f33d184d25b4571a2f0

SRC_SHA256 by dollars
       1.78B       44 rows  6891416b923082bb3e7ab6991163ce4ad394b3fc79659f33d184d25b4571

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Contract Administration (Contract Admini  2021:528.14M 2022:234.35M 2023:294.54M 2024:286.14M 2025:284.08M 2026:153.69M

TYPEDATA by DATE, dollars = VALUE
  Period                                    2021:528.14M 2022:234.35M 2023:294.54M 2024:286.14M 2025:284.08M 2026:153.69M

## what

ID: 18949 8%, 18948 8%, 18947 8%, 18946 8%, 15724 8%, 15723 8%, 15722 8%, 15721 8%, 12205 8%, 12204 8%, 12203 8%, 12201 8%

CHARTNAME: CIP Throughput: RQSs 25%, CIP Throughput: Contracts by F 25%, CIP Throughput: Average RQS Am 25%, CIP Throughput: Amount Certifi 25%

CATEGORY: Number of RQSs 25%, Contracts 25%, RQS Amounts 25%, Amount Certified 25%

PERIOD: 2026 9%, 2025 9%, 2024 9%, 2023 9%, 2022 9%, 2021 9%, 2020 9%, 2019 9%, 2018 9%, 2017 9%, 2016 9%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | category | 44 | 0 | 18949 1; 18948 1; 18947 1; 18946 1 |
| C_ORGANIZATION | who | 1 | 0 | Contract Administration ( 44 |
| CHARTNAME | category | 4 | 0 | CIP Throughput: RQSs 11; CIP Throughput: Contracts 11; CIP Throughput: Average R 11; CIP Throughput: Amount Ce 11 |
| DESCRIPTION | empty | 1 | 44 |  |
| CATEGORY | category | 4 | 0 | Number of RQSs 11; Contracts 11; RQS Amounts 11; Amount Certified 11 |
| SUMMARY | other | 1 | 0 | Total 44 |
| TYPEDATA | who | 1 | 0 | Period 44 |
| DATE | date | 15 | 0 | 05/12/2021 00:00:00 11; 02/05/2026 00:00:00 4; 02/06/2025 00:00:00 4; 02/26/2024 00:00:00 4 |
| PERIOD | category | 11 | 0 | 2026 4; 2025 4; 2024 4; 2023 4 |
| VALUE | amount | 44 | 0 | 589.000 1; 111.000 1; 260495.580 1; 153431896.670 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:12:15.46174 44 |
| SOURCE_RUN_ID | audit | 1 | 0 | 55c4bc04-89cf-4c5c-84ea-a 44 |
| SRC_SHA256 | who | 1 | 0 | 6891416b923082bb3e7ab6991 44 |
