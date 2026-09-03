# PORTAL_CKA_WPRDC_ALLEGHENY_31D26600C9

rows 10.0K  columns 13  scan 4.7s

roles: amount 1, audit 2, category 1, date 2, empty 1, id 1, other 2, who 4

## when

FILING_DATE
  2009      4.7K  ##############################
  2010      4.1K  ##########################
  2011      1.1K  #######

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | 0 | 74.0K | 1.04M | 54.81M | 2.20B |

## who

PLAINTIFF by rows
       819  Wells Fargo Bank N.A.
       667  Deutsche Bank National Trust Company
       645  Citimortgage Inc.
       633  BAC Home Loans Servicing L.P.
       499  U.S. Bank National Association
       293  Bank of America N.A.
       283  Bank of New York Mellon
       264  Chase Home Finance LLC
       191  PHH Mortgage Corporation
       173  JPMorgan Chase Bank N.A.
       160  First Commonwealth Bank
       155  Nationstar Mortgage LLC
       145  PNC Bank National Association
       141  U.S. Bank N.A.
       119  PNC Mortgage
       118  PNC Bank N.A.
       116  Midfirst Bank
       114  Beneficial Consumer Discount Company
       114  Household Finance Consumer Discount Company
       113  HSBC Bank USA N.A.

PLAINTIFF by dollars
     469.69M       15 rows  PMCF Holdings LLC
     137.05M      819 rows  Wells Fargo Bank N.A.
     109.63M        2 rows  Anglo Irish Bank Corporation Limited
     105.24M      499 rows  U.S. Bank National Association
      67.19M      667 rows  Deutsche Bank National Trust Company
      62.06M        4 rows  SL Investment US-RE Holdings 2009-1 Inc.
      60.66M      160 rows  First Commonwealth Bank
      59.92M      633 rows  BAC Home Loans Servicing L.P.
      58.82M      645 rows  Citimortgage Inc.
      53.74M       23 rows  Plaintiffs All
      51.63M        2 rows  California National Bank
      50.84M        2 rows  German American Capital Corporation
      44.08M      293 rows  Bank of America N.A.
      28.77M      283 rows  Bank of New York Mellon
      28.39M       27 rows  Washington Financial Bank
      25.11M        2 rows  Regions Bank
      24.59M      264 rows  Chase Home Finance LLC
      23.87M        1 rows  RRE VIP Borrower LLC
      23.37M        1 rows  Jefferson-Pilot Investments Inc.
      22.68M       81 rows  S & T Bank

MUNICIPALITY by rows
      2.6K  Pittsburgh
       738  Penn Hills Township
       227  Wilkinsburg Boro
       215  Monroeville Boro
       209  City of McKeesport
       200  Plum Boro
       200  Shaler Township
       186  West Mifflin Boro
       158  Bethel Park Boro
       152  Ross Township
       142  Moon Township
       133  Mt. Lebanon Township
       128  Baldwin Boro
       118  Elizabeth Township
       116  Munhall Boro
       114  Swissvale Boro
       111  N. Versailles Twp.
       110  N. Fayette Township
       103  South Park Township
       103  Brentwood Boro

MUNICIPALITY by dollars
     479.74M      128 rows  Baldwin Boro
     405.41M     2.6K rows  Pittsburgh
     180.74M      110 rows  N. Fayette Township
     128.68M       74 rows  Robinson Township
      71.44M       92 rows  Scott Township
      62.36M      738 rows  Penn Hills Township
      50.79M       56 rows  O'Hara Township
      41.49M      142 rows  Moon Township
      41.04M      152 rows  Ross Township
      37.64M       82 rows  Whitehall Boro
      36.51M      118 rows  Elizabeth Township
      29.59M       38 rows  Collier Township
      26.90M      215 rows  Monroeville Boro
      24.68M      200 rows  Plum Boro
      23.72M      133 rows  Mt. Lebanon Township
      22.82M      200 rows  Shaler Township
      20.45M       99 rows  McCandless Township
      20.13M      158 rows  Bethel Park Boro
      19.21M       98 rows  Upper St. Clair Twp.
      16.36M       75 rows  Hampton Township

DOCKET_TYPE by rows
      4.2K  Sheriff Return
      1.3K  Discontinued without Prejudice
      1.1K  Certificate-Recorder of Deeds
       660  Settled and Discontinued
       632  Order of Court
       344  Correction to Judgment Index
       223  Complaint
       211  Case Terminated
       148  Satisfaction
       116  Default Judgment
       114  Praecipe to Withdraw
       105  Mail Returned
       105  Discontinued
        93  Praecipe to Substitute
        62  Motion & Order
        40  Praecipe to Vacate Judgment
        39  Affidavit
        38  Certificate of Service
        33  Suggestion of Bankruptcy
        33  Release of Judgment Lien

DOCKET_TYPE by dollars
     522.75M     4.2K rows  Sheriff Return
     469.69M       15 rows  Report
     227.78M      211 rows  Case Terminated
     169.40M      660 rows  Settled and Discontinued
     152.97M       12 rows  Discontinued with Prejudice
     131.75M     1.3K rows  Discontinued without Prejudice
     115.17M     1.1K rows  Certificate-Recorder of Deeds
      87.76M      148 rows  Satisfaction
      85.54M      632 rows  Order of Court
      34.89M      344 rows  Correction to Judgment Index
      25.11M        2 rows  Answer to Complaint
      20.90M      223 rows  Complaint
      17.08M       33 rows  Suggestion of Bankruptcy
      11.98M      114 rows  Praecipe to Withdraw
      11.62M      105 rows  Mail Returned
      11.42M        9 rows  Order of Court FMV/Judgment
      10.17M      105 rows  Discontinued
       8.44M       93 rows  Praecipe to Substitute
       8.43M      116 rows  Default Judgment
       6.56M       16 rows  Judgment by Court Order

SRC_SHA256 by rows
     10.0K  fdcfd7066c2d17029dc45650f75e947bc1576f2260b456f01ecb00c4eecf41ff

SRC_SHA256 by dollars
       2.20B    10.0K rows  fdcfd7066c2d17029dc45650f75e947bc1576f2260b456f01ecb00c4eecf

## who x when

PLAINTIFF by FILING_DATE, dollars = AMOUNT
  Anglo Irish Bank Corporation Limited      2009:109.63M
  BAC Home Loans Servicing L.P.             2009:29.45M 2010:27.85M 2011:2.62M
  Bank of America N.A.                      2009:11.26M 2010:23.22M 2011:9.60M
  Bank of New York Mellon                   2009:11.48M 2010:12.85M 2011:4.43M
  Beneficial Consumer Discount Company      2009:4.50M 2010:6.18M 2011:310.1K
  California National Bank                  2009:51.63M
  Chase Home Finance LLC                    2009:11.93M 2010:12.52M 2011:130.0K
  Citimortgage Inc.                         2009:27.92M 2010:23.07M 2011:7.83M
  Deutsche Bank National Trust Company      2009:33.38M 2010:27.61M 2011:6.20M
  First Commonwealth Bank                   2009:5.80M 2010:9.15M 2011:45.72M
  German American Capital Corporation       2010:50.84M
  HSBC Bank USA N.A.                        2009:4.25M 2010:5.45M 2011:1.10M
  Household Finance Consumer Discount Comp  2009:4.44M 2010:6.43M 2011:252.3K
  JPMorgan Chase Bank N.A.                  2009:8.39M 2010:7.91M 2011:64.0K
  Jefferson-Pilot Investments Inc.          2011:23.37M
  Midfirst Bank                             2009:2.86M 2010:2.02M 2011:460.1K
  Nationstar Mortgage LLC                   2009:5.97M 2010:5.83M 2011:825.7K
  PHH Mortgage Corporation                  2009:6.81M 2010:7.25M 2011:3.06M
  PMCF Holdings LLC                         2010:469.69M
  PNC Bank N.A.                             2009:1.18M 2010:3.18M 2011:1.73M
  PNC Bank National Association             2009:1.89M 2010:3.95M 2011:3.22M
  PNC Mortgage                              2009:678.9K 2010:7.85M 2011:849.3K
  Plaintiffs All                            2009:1.14M 2010:52.22M 2011:382.5K
  RRE VIP Borrower LLC                      2009:23.87M
  Regions Bank                              2009:25.11M
  SL Investment US-RE Holdings 2009-1 Inc.  2011:62.06M
  U.S. Bank N.A.                            2009:5.11M 2010:4.05M 2011:281.6K
  U.S. Bank National Association            2009:26.31M 2010:38.74M 2011:40.19M
  Washington Financial Bank                 2009:27.07M 2011:1.31M
  Wells Fargo Bank N.A.                     2009:44.29M 2010:85.99M 2011:6.77M

MUNICIPALITY by FILING_DATE, dollars = AMOUNT
  Baldwin Boro                              2009:4.03M 2010:474.78M 2011:932.0K
  Bethel Park Boro                          2009:7.45M 2010:10.80M 2011:1.89M
  Brentwood Boro                            2009:4.20M 2010:6.77M 2011:331.7K
  City of McKeesport                        2009:5.75M 2010:4.33M 2011:1.93M
  Collier Township                          2009:26.41M 2010:2.49M 2011:679.3K
  Elizabeth Township                        2009:32.64M 2010:2.91M 2011:958.8K
  Hampton Township                          2009:8.94M 2010:5.88M 2011:1.53M
  McCandless Township                       2009:11.71M 2010:7.32M 2011:1.42M
  Monroeville Boro                          2009:10.39M 2010:14.06M 2011:2.45M
  Moon Township                             2009:12.10M 2010:27.33M 2011:2.06M
  Mt. Lebanon Township                      2009:14.14M 2010:6.56M 2011:3.02M
  Munhall Boro                              2009:3.81M 2010:3.49M 2011:408.0K
  N. Fayette Township                       2009:9.81M 2010:169.26M 2011:1.66M
  N. Versailles Twp.                        2009:3.29M 2010:4.34M 2011:934.3K
  O'Hara Township                           2009:42.78M 2010:7.64M 2011:368.9K
  Penn Hills Township                       2009:27.57M 2010:23.57M 2011:11.22M
  Pittsburgh                                2009:190.64M 2010:119.78M 2011:95.00M
  Plum Boro                                 2009:12.06M 2010:10.34M 2011:2.28M
  Robinson Township                         2009:113.80M 2010:6.06M 2011:8.82M
  Ross Township                             2009:8.89M 2010:8.01M 2011:24.14M
  Scott Township                            2009:4.16M 2010:4.50M 2011:62.78M
  Shaler Township                           2009:10.63M 2010:10.29M 2011:1.90M
  South Park Township                       2009:4.53M 2010:5.16M 2011:1.48M
  Swissvale Boro                            2009:4.62M 2010:2.23M 2011:710.1K
  Upper St. Clair Twp.                      2009:9.18M 2010:7.87M 2011:2.16M
  West Mifflin Boro                         2009:7.38M 2010:4.47M 2011:3.36M
  Whitehall Boro                            2009:34.17M 2010:3.02M 2011:441.8K
  Wilkinsburg Boro                          2009:7.99M 2010:4.38M 2011:3.30M

## what

WARD: 19 18%, 20 13%, 27 11%, 10 9%, 26 8%, 11 8%, 29 8%, 2 7%, 15 6%, 18 6%, 28 6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PIN | other | 9.2K | 61 | 0319C00202000000 52; 0222K00334000000 50; 0222K00332000000 50; 0222K00330000000 50 |
| BLOCK_LOT | other | 9.0K | 51 | 319C202 52; 222K334 50; 222K332 50; 222K330 50 |
| FILING_DATE | date | 763 | 0 | 2011-10-28 71; 2011-01-19 65; 2010-08-16 64; 2010-09-14 62 |
| CASE_ID | id | 9.5K | 0 | GD-11-022232 71; MG-11-000487 52; MG-11-000467 52; MG-11-000458 51 |
| MUNICIPALITY | who | 129 | 0 | Pittsburgh 2.6K; Penn Hills Township 738; Wilkinsburg Boro 227; Monroeville Boro 215 |
| WARD | category | 33 | 7.1K | 19 307; 20 232; 27 187; 10 164 |
| DOCKET_TYPE | who | 115 | 0 | Sheriff Return 4.2K; Discontinued without Prej 1.3K; Certificate-Recorder of D 1.1K; Settled and Discontinued 660 |
| AMOUNT | amount | 8.7K | 2 | 0.0 689; 132096.68 49; 125201.18 49; 62457.51 48 |
| PLAINTIFF | who | 788 | 0 | Wells Fargo Bank N.A. 819; Deutsche Bank National Tr 667; Citimortgage Inc. 645; BAC Home Loans Servicing  633 |
| LAST_ACTIVITY | empty | 1 | 10.0K |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:04:37.04413 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | e1c6e056-b96c-48c5-847f-5 10.0K |
| SRC_SHA256 | who | 1 | 0 | fdcfd7066c2d17029dc45650f 10.0K |
