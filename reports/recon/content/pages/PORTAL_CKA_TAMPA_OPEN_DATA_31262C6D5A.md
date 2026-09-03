# PORTAL_CKA_TAMPA_OPEN_DATA_31262C6D5A

rows 348  columns 13  scan 4.3s

roles: amount 1, audit 2, category 3, date 2, other 2, who 4

## when

DATE
  2022        20  #####
  2023        71  ################
  2024       130  ##############################
  2025        86  ####################
  2026        41  #########

INGESTED_AT
  2026       348  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 348 | 0 | 601.2K | 321.69M | 332.61M | 9.01B |

## who

C_ORGANIZATION by rows
       348  Revenue & Finance (Revenue and Finance)

C_ORGANIZATION by dollars
       9.01B      348 rows  Revenue & Finance (Revenue and Finance)

TYPEDATA by rows
       348  Period

TYPEDATA by dollars
       9.01B      348 rows  Period

DESCRIPTION by rows
       348  Accounting Office OpenGov story

DESCRIPTION by dollars
       9.01B      348 rows  Accounting Office OpenGov story

SRC_SHA256 by rows
       348  87e0a6451b6c5c5c46a192f266889f74e0b62104a4870da4d93de752d5e456be

SRC_SHA256 by dollars
       9.01B      348 rows  87e0a6451b6c5c5c46a192f266889f74e0b62104a4870da4d93de752d5e4

## who x when

C_ORGANIZATION by DATE, dollars = VALUE
  Revenue & Finance (Revenue and Finance)   2022:477.01M 2023:1.03B 2024:5.13B 2025:1.78B 2026:583.35M

TYPEDATA by DATE, dollars = VALUE
  Period                                    2022:477.01M 2023:1.03B 2024:5.13B 2025:1.78B 2026:583.35M

## what

CHARTNAME: R&F - Accounts Receivable 23%, R&F - Property Control 14%, R&F - Accounts Payable 12%, R&F - Capital Projects - Invoi 9%, R&F - Capital Projects - Avg N 9%, R&F - Grants - Awards & Match 6%, R&F - Grants - Expenditures &  5%, R&F - Capital Projects - Total 5%, R&F - Billing - Invoices ($) 5%, R&F - Billing - Invoices (#) 5%, R&F - Capital Projects - Total 4%, R&F - Capital Projects - Requi 4%

CATEGORY: Design 14%, Construction 13%, Match 8%, Total Projects 8%, Assets Inventoried 8%, Total Invoiced Amount 7%, Total Number of Invoices 7%, (5) Outstanding (180+ Days) 7%, (4) Outstanding (91-180 Days) 7%, (3) Outstanding (61-90 Days) 7%, (2) Outstanding (31-60 Days) 7%, (1) Outstanding (Current) 7%

PERIOD: FY24-Q3 10%, FY24-Q4 10%, FY24-Q2 9%, FY24-Q1 9%, FY23-Q3 9%, FY23-Q2 9%, FY23-Q1 9%, FY23-Q4 9%, FY25-Q2 7%, FY26-Q1 7%, FY25-Q4 6%, FY25-Q3 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 343 | 0 | 20581 2; 20580 2; 20579 2; 20578 2 |
| C_ORGANIZATION | who | 1 | 0 | Revenue & Finance (Revenu 348 |
| CHARTNAME | category | 14 | 0 | R&F - Accounts Receivable 75; R&F - Property Control 46; R&F - Accounts Payable 38; R&F - Capital Projects -  30 |
| DESCRIPTION | who | 1 | 0 | Accounting Office OpenGov 348 |
| CATEGORY | category | 25 | 0 | Design 30; Construction 28; Match 17; Total Projects 16 |
| SUMMARY | other | 1 | 0 | Total 348 |
| TYPEDATA | who | 1 | 0 | Period 348 |
| DATE | date | 278 | 0 | 2024-09-06T00:00:00 9; 2022-12-27T00:00:00 9; 2023-01-17T00:00:00 8; 2024-06-03T09:13:00 5 |
| PERIOD | category | 18 | 0 | FY24-Q3 28; FY24-Q4 28; FY24-Q2 27; FY24-Q1 27 |
| VALUE | amount | 319 | 0 | 501.0 6; 446.0 4; 0.0 4; 523.0 4 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:19:22.98786 348 |
| SOURCE_RUN_ID | audit | 1 | 0 | 2d47d8dd-9f6e-4a36-b71a-5 348 |
| SRC_SHA256 | who | 1 | 0 | 87e0a6451b6c5c5c46a192f26 348 |
