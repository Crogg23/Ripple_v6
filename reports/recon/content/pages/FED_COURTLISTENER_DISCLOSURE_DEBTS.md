# FED_COURTLISTENER_DISCLOSURE_DEBTS

rows 18.8K  columns 11  scan 4.1s

roles: audit 2, category 2, date 3, id 1, other 1, who 3

## when

DATE_CREATED
  2021     16.2K  ##############################
  2022      2.5K  #####
  2023        11  

DATE_MODIFIED
  2021     16.2K  ##############################
  2022      2.5K  #####
  2023        11  
  2025        27  

_INGESTED_AT
  2026     18.8K  ##############################

## who

CREDITOR_NAME by rows
      1.2K  Bank of America
       760  American Express
       472  Chase Bank
       459  Chase
       343  Citibank
       258  Wells Fargo
       239  Discover
       197  Capital One
       168  Wells Fargo Bank
       167  Amcrican Express
       156  U.S. Department of Education
       125  Visa
       111  Sallie Mae
       109  Bank Of America
       103  Amencan Express
        97  Navient
        90  Discover Card
        80  PNC Bank
        75  Chase Visa
        66  Mastercard

DESCRIPTION by rows
      4.6K  Credit Card
       536  Student Loan
       497  credit card
       383  Line of Credit
       293  Student Loans
       273  Loan
       232  Credit card
       229  CREDIT CARD
       186  Tuition
       159  Personal Loan
       118  Credit Cards
        99  Tuition Agreement
        93  Credit Line
        89  Mortgage on Rental Property
        63  Revolving Credit
        63  Promissory Note
        62  student loan
        57  Educational Loans
        57  Mortgage on rental property
        57  Mortgage

_SRC_SHA256 by rows
     18.8K  4af99e6bdf975261bef97f2794f1d6470531ad6e6bf0abf307e8b56a8e9f0783

## who x when

CREDITOR_NAME by DATE_MODIFIED
  Amcrican Express                          2021:167
  Amencan Express                           2021:103
  American Express                          2021:642 2022:118
  Bank Of America                           2021:109
  Bank of America                           2021:1.1K 2022:133
  Capital One                               2021:167 2022:30
  Chase                                     2021:406 2022:53
  Chase Bank                                2021:425 2022:47
  Chase Visa                                2021:58 2022:17
  Citibank                                  2021:280 2022:63
  Discover                                  2021:194 2022:44 2025:1
  Discover Card                             2021:75 2022:15
  Mastercard                                2021:56 2022:10
  Navient                                   2021:39 2022:57 2025:1
  PNC Bank                                  2021:70 2022:10
  Sallie Mae                                2021:83 2022:26 2025:2
  U.S. Department of Education              2021:133 2022:23
  Visa                                      2021:112 2022:13
  Wells Fargo                               2021:203 2022:53 2025:2
  Wells Fargo Bank                          2021:130 2022:38

DESCRIPTION by DATE_MODIFIED
  CREDIT CARD                               2021:224 2022:5
  Credit Card                               2021:4.1K 2022:548
  Credit Cards                              2021:114 2022:4
  Credit Line                               2021:89 2022:4
  Credit card                               2021:194 2022:38
  Educational Loans                         2021:51 2022:6
  Line of Credit                            2021:340 2022:43
  Loan                                      2021:216 2022:57
  Mortgage                                  2021:52 2022:5
  Mortgage on Rental Property               2021:74 2022:15
  Mortgage on rental property               2021:44 2022:13
  Personal Loan                             2021:112 2022:47
  Promissory Note                           2021:62 2022:1
  Revolving Credit                          2021:56 2022:7
  Student Loan                              2021:398 2022:134 2025:4
  Student Loans                             2021:228 2022:64 2023:1
  Tuition                                   2021:160 2022:26
  Tuition Agreement                         2021:57 2022:42
  credit card                               2021:399 2022:98
  student loan                              2021:53 2022:9

## what

VALUE_CODE: J 29%, K 29%, -1 16%, M 10%, L 8%, N 5%, P1 1%, O 1%, P2 0%, P4 0%, P3 0%

REDACTED: f 97%, t 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 18.9K | 0 | 53640 94; 53657 94; 53670 94; 53669 94 |
| DATE_CREATED | date | 19.0K | 0 | 2022-05-19 15:57:08.47642 94; 2022-05-19 15:59:00.45989 94; 2022-05-19 19:02:30.30986 94; 2022-05-19 19:02:22.10320 94 |
| DATE_MODIFIED | date | 18.7K | 0 | 2025-02-05 14:22:46.15704 94; 2025-02-05 14:21:53.80743 94; 2022-05-19 19:02:30.30987 94; 2022-05-19 19:02:22.10322 94 |
| CREDITOR_NAME | who | 3.9K | 36 | Bank of America 1.2K; American Express 760; Chase Bank 472; Chase 459 |
| DESCRIPTION | who | 4.0K | 92 | Credit Card 4.6K; Student Loan 536; credit card 497; Line of Credit 383 |
| VALUE_CODE | category | 11 | 1.7K | J 5.0K; K 5.0K; -1 2.7K; M 1.7K |
| REDACTED | category | 2 | 0 | f 18.2K; t 584 |
| FINANCIAL_DISCLOSURE_ID | other | 8.8K | 0 | 33655 123; 33949 113; 33554 111; 33461 107 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:05:10.740 18.8K |
| _SOURCE_RUN_ID | audit | 1 | 0 | dc6f35d2-8561-4d7c-ae79-2 18.8K |
| _SRC_SHA256 | who | 1 | 0 | 4af99e6bdf975261bef97f279 18.8K |
