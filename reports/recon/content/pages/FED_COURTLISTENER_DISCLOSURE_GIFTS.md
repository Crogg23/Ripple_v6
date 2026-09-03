# FED_COURTLISTENER_DISCLOSURE_GIFTS

rows 2.0K  columns 11  scan 4.6s

roles: amount 1, audit 2, category 1, date 3, id 1, other 2, who 2

## when

DATE_CREATED
  2021      1.9K  ##############################
  2022       156  ###
  2023         9  

DATE_MODIFIED
  2021      1.9K  ##############################
  2022       156  ###
  2023         9  

_INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 1.5K | 0 | 900 | 71.1K | 2.51M | 10.69M |

## who

SOURCE by rows
        41  Federal Bar Council
        37  Union League Club of Chicago
        28  David A. Blanton
        26  Exempt
        22  Membership Dues
        21  American College of Trial Lawyers
        20  Umion League Chub of Chicago
        15  Southeastern Bankruptcy Law Institute
        15  Minneapolis Club
        14  Herzog Contracting Corp.
        13  Federal Judicial Guest Privileges
        12  David C. Pratt
        12  Northampton County Bar Association
        12  Duke University
        11  James Nobile
        11  Umon League Club of Chicago
        11  Federal Bar Association
        10  West Publishing Co.
         9  Reduced Membership
         9  Jose R. Rivas

SOURCE by dollars
       3.25M        5 rows  Latham & Watkins, LLP
       1.00M        1 rows  The Berggruen Institute
      491.7K        1 rows  Ashington Golf and Country Club
      200.0K        2 rows  Morgan Stanley Smith Bamey
      199.0K        2 rows  Duke Law School
      194.4K       12 rows  Duke University
      168.2K        2 rows  Covington & Burling, Washington, DC
      163.2K        3 rows  Kukland & Ellis LLP, Wash., DX
      163.2K        3 rows  Kirkland & Ellis, LLP, Washington, DC
      125.9K        3 rows  Kirkland & Ellis, LLP, Washington, DC.
      119.6K        6 rows  Susman Godfrey, LLP
      112.1K        2 rows  David and Dem Kiersznowsk
      100.0K        1 rows  National Constitution Center
      100.0K        1 rows  Morgan Stanley Smith Barney
       80.0K        1 rows  Jamey McMahon
       73.8K       12 rows  David C. Pratt
       72.3K        1 rows  Dallas Asian Amencan Bar Association
       71.8K        1 rows  Nexsen Proer PLLC
       71.1K        1 rows  Davis Polk & Wardwell
       71.1K        1 rows  Winograd, Shine Land & Finkle, P.C

_SRC_SHA256 by rows
      2.0K  81738829cff941b710e2dc8523e595d7092459c16858a30b5fbb9230147fec6b

_SRC_SHA256 by dollars
      10.69M     2.0K rows  81738829cff941b710e2dc8523e595d7092459c16858a30b5fbb9230147f

## who x when

SOURCE by DATE_CREATED, dollars = VALUE
  American College of Trial Lawyers         2021:17.7K
  Ashington Golf and Country Club           2021:491.7K
  Covington & Burling, Washington, DC       2022:168.2K
  David A. Blanton                          2021:26.9K 2022:987.56
  David C. Pratt                            2021:73.8K
  Duke Law School                           2021:199.0K
  Duke University                           2021:194.4K
  Exempt                                    2021:8 2022:18
  Federal Bar Association                   2021:19.7K
  Federal Bar Council                       2021:30.8K 2022:3.5K
  Federal Judicial Guest Privileges         2021:11 2022:2
  Herzog Contracting Corp.                  2021:21.3K 2022:3.0K
  James Nobile                              2021:23.2K 2022:4.2K
  Jose R. Rivas                             2021:10.9K 2022:3.1K
  Kirkland & Ellis, LLP, Washington, DC     2021:163.2K
  Kirkland & Ellis, LLP, Washington, DC.    2021:125.9K
  Kukland & Ellis LLP, Wash., DX            2021:163.2K
  Latham & Watkins, LLP                     2021:3.25M
  Membership Dues                           2021:10.5K
  Minneapolis Club                          2021:175
  Morgan Stanley Smith Bamey                2021:200.0K
  Northampton County Bar Association        2021:22.3K 2022:470
  Reduced Membership                        2021:2.7K
  Southeastern Bankruptcy Law Institute     2021:17.0K
  Susman Godfrey, LLP                       2021:119.6K
  The Berggruen Institute                   2021:1.00M
  Umion League Chub of Chicago              2021:29.2K
  Umon League Club of Chicago               2021:7.7K
  Union League Club of Chicago              2021:14.9K 2022:6.2K
  West Publishing Co.                       2021:22.5K

_SRC_SHA256 by DATE_CREATED, dollars = VALUE
  81738829cff941b710e2dc8523e595d7092459c1  2021:10.23M 2022:439.6K 2023:23.4K

## what

REDACTED: f 96%, t 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 2.0K | 0 | 5540 11; 5539 11; 5538 11; 5537 11 |
| DATE_CREATED | date | 2.0K | 0 | 2023-08-31 15:48:38.09952 11; 2023-08-31 15:48:38.09951 11; 2023-08-31 15:48:38.09949 11; 2023-08-31 15:47:57.11495 11 |
| DATE_MODIFIED | date | 2.0K | 0 | 2023-08-31 15:48:38.09952 11; 2023-08-31 15:48:38.09951 11; 2023-08-31 15:48:38.09949 11; 2023-08-31 15:47:57.11495 11 |
| SOURCE | who | 1.1K | 58 | Federal Bar Council 41; Union League Club of Chic 37; David A. Blanton 28; Exempt 27 |
| DESCRIPTION | other | 1.3K | 101 | Honorary Membership 52; Honorary Membership (dues 19; Cash gift 18; Judicial Robe 16 |
| VALUE | amount | 529 | 441 | $500.00 92; $600.00 65; $1,000.00 61; $400.00 59 |
| REDACTED | category | 2 | 0 | f 1.9K; t 91 |
| FINANCIAL_DISCLOSURE_ID | other | 1.5K | 0 | 25631 18; 34210 15; 19015 15; 17430 15 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:05:04.147 2.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 5ea73c7b-7a25-48fc-801c-2 2.0K |
| _SRC_SHA256 | who | 1 | 0 | 81738829cff941b710e2dc852 2.0K |
