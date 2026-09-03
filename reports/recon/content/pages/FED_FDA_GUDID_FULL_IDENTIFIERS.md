# FED_FDA_GUDID_FULL_IDENTIFIERS

rows 6.77M  columns 12  scan 2.7s

roles: audit 2, category 3, date 2, id 2, other 4

## errors
  _INGESTED_AT: 100039 (22003): Numeric value '56656541' is out of range

## when

PKGDISCONTINUEDATE
  1969         3  
  1970         1  
  1994         1  
  1998         2  
  1999       247  #
  2000         3  
  2002         2  
  2004         1  
  2005         1  
  2006         1  
  2007         1  
  2008         2  
  2009         5  
  2013         2  
  2014        16  
  2015       372  #
  2016      1.4K  ####
  2017      2.8K  #######
  2018      5.3K  ##############
  2019      8.7K  ######################
  2020      6.9K  ##################
  2021     11.6K  ##############################
  2022      6.9K  ##################
  2023     10.9K  ############################
  2024     11.5K  ##############################
  2025     10.9K  ############################
  2026      4.6K  ############
  2027       319  #
  2028       161  
  2029       107  
  2030       140  
  2031        57  
  2032         6  
  2033        19  
  2034        18  
  2035        12  

## what

DEVICEIDTYPE: Primary 77%, Package 16%, Unit of Use 5%, Secondary 1%, Previous 1%, Direct Marking 1%

DEVICEIDISSUINGAGENCY: GS1 88%, HIBCC 12%, NDC/NHRIC 0%, ICCBBA 0%

PKGSTATUS: In Commercial Distribution 93%, Not in Commercial Distribution 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PRIMARYDI | other | 5.26M | 0 | 10197106234617 5.0K; 10197106234624 5.0K; 10197106234631 5.0K; 10197106234655 5.0K |
| DEVICEID | id | 6.71M | 0 | 00000008857972 5.5K; M6334949850 5.0K; M6334949870 5.0K; M6334949880 5.0K |
| DEVICEIDTYPE | category | 6 | 0 | Primary 5.18M; Package 1.11M; Unit of Use 307.9K; Secondary 86.5K |
| DEVICEIDISSUINGAGENCY | category | 4 | 0 | GS1 5.93M; HIBCC 836.5K; NDC/NHRIC 219; ICCBBA 87 |
| CONTAINSDINUMBER | id | 1.09M | 5.66M | 10190886015612 1.1K; 10190886015629 1.1K; 10190886015636 1.1K; 10190886015643 1.1K |
| PKGQUANTITY | other | 414 | 5.66M | 2 185.4K; 10 143.1K; 1 123.7K; 3 95.2K |
| PKGDISCONTINUEDATE | date | 3.3K | 6.68M | 2025-12-31 2.1K; 2021-06-14 1.6K; 2021-06-15 1.4K; 2040-12-31 893 |
| PKGSTATUS | category | 2 | 5.66M | In Commercial Distributio 1.03M; Not in Commercial Distrib 82.1K |
| PKGTYPE | other | 3.4K | 5.87M | CASE 557.7K; Case 75.4K; Box 52.7K; BOX 39.8K |
| _INGESTED_AT | audit date | 1 | 0 | 56656541-01-26 18:47:58.0 6.77M |
| _SOURCE_RUN_ID | audit | 1 | 0 | 69a3809b-96b8-42d1-aebf-0 6.77M |
| _SRC_SHA256 | other | 1 | 0 | b069d3950b2c75da08b2adbf4 6.77M |
