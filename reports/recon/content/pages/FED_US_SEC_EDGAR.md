# FED_US_SEC_EDGAR

rows 49.0K  columns 17  scan 2.5s

roles: audit 3, category 6, date 2, empty 1, id 3, other 1, state 1, who 1

## when

FILED_AT
  1995         4  
  1999         1  
  2000         1  
  2001         1  
  2002        25  
  2003        38  
  2004        26  
  2005        24  
  2006        28  
  2007        38  
  2008        32  
  2009        33  
  2010        29  
  2011        29  
  2012        42  
  2013       123  
  2014       137  
  2015       336  #
  2016       380  #
  2017       699  #
  2018       899  ##
  2019      1.4K  ###
  2020      2.1K  ####
  2021      2.4K  #####
  2022      2.2K  ####
  2023      3.0K  ######
  2024      3.8K  #######
  2025     15.5K  ##############################
  2026     15.6K  ##############################

PERIOD_OF_REPORT
  2001         1  
  2002        17  
  2003        20  
  2004        20  
  2005        16  
  2006        18  
  2007        22  
  2008        24  
  2009        24  
  2010        21  
  2011        21  
  2012        33  
  2013        83  #
  2014       120  #
  2015       252  ###
  2016       324  ####
  2017       583  #######
  2018       780  #########
  2019      1.2K  #############
  2020      1.8K  ####################
  2021      1.8K  ####################
  2022      1.8K  ####################
  2023      2.1K  ########################
  2024      2.6K  ##############################
  2025      2.6K  #############################
  2026      1.4K  ################

## who

_SRC_SHA256 by rows
     49.0K  d70ee4b6aa808882e62d207648e850ca87754a7813107add76a78024bfe7b695

## who x when

_SRC_SHA256 by PERIOD_OF_REPORT
  d70ee4b6aa808882e62d207648e850ca87754a78  2001:1 2002:17 2003:20 2004:20 2005:16 2006:18 2007:22 2008:24 2009:24 2010:21 2011:21 2012:33 2013:83 2014:120 2015:252 2016:324 2017:583 2018:780 2019:1.2K 2020:1.8K 2021:1.8K 2022:1.8K 2023:2.1K 2024:2.6K 2025:2.6K 2026:1.4K

## where

STATE_OF_INCORPORATION: DE 40.4K, NJ 2.0K, WA 1.0K, IN 1.0K, TX 1.0K, DC 1.0K, CA 1.0K

## what

CIK: 0000019617 70%, 0001403161 3%, 0000104169 3%, 0000034088 3%, 0000858877 3%, 0001141391 3%, 0001018724 3%, 0000002488 3%, 0001652044 3%, 0000018230 3%, 0001326801 3%, 0000789019 3%

ENTITY_NAME: JPMORGAN CHASE & CO 70%, VISA INC. 3%, Walmart Inc. 3%, EXXON MOBIL CORP 3%, CISCO SYSTEMS, INC. 3%, Mastercard Inc 3%, AMAZON COM INC 3%, ADVANCED MICRO DEVICES INC 3%, Alphabet Inc. 3%, CATERPILLAR INC 3%, Meta Platforms, Inc. 3%, MICROSOFT CORP 3%

TICKER: JPM 70%, V 3%, WMT 3%, XOM 3%, CSCO 3%, MA 3%, AMZN 3%, AMD 3%, GOOGL 3%, CAT 3%, META 3%, MSFT 3%

SIC_CODE: 6021 55%, 3674 13%, 2834 7%, 7389 4%, 7370 4%, 3559 3%, 5331 2%, 2911 2%, 3576 2%, 5961 2%, 3531 2%, 7372 2%

BUSINESS_ADDRESS: 270 PARK AVENUE, NEW YORK, NY, 70%, P.O. BOX 8999, SAN FRANCISCO,  3%, 1 CUSTOMER DRIVE, BENTONVILLE, 3%, 22777 SPRINGWOODS VILLAGE PARK 3%, 170 WEST TASMAN DR, SAN JOSE,  3%, 2000 PURCHASE STREET, PURCHASE 3%, 410 TERRY AVENUE NORTH, SEATTL 3%, 2485 AUGUSTINE DRIVE, SANTA CL 3%, 1600 AMPHITHEATRE PARKWAY, MOU 3%, 5205 N. O'CONNOR BOULEVARD, SU 3%, 1 META WAY, MENLO PARK, CA, 94 3%, ONE MICROSOFT WAY, REDMOND, WA 3%

EIN: 132624428 70%, 260267673 3%, 710415188 3%, 135409005 3%, 770059951 3%, 134172551 3%, 911646860 3%, 941692300 3%, 611767919 3%, 370602744 3%, 201665019 3%, 911144442 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACCESSION_NUMBER | id | 48.9K | 0 | 0001141391-18-000078 245; 0001141391-18-000092 245; 0001141391-18-000093 245; 0001141391-18-000094 245 |
| CIK | category | 25 | 0 | 0000019617 25.4K; 0001403161 1.0K; 0000104169 1.0K; 0000034088 1.0K |
| ENTITY_NAME | category | 25 | 0 | JPMORGAN CHASE & CO 25.4K; VISA INC. 1.0K; Walmart Inc. 1.0K; EXXON MOBIL CORP 1.0K |
| TICKER | category | 25 | 0 | JPM 25.4K; V 1.0K; WMT 1.0K; XOM 1.0K |
| FORM_TYPE | other | 95 | 0 | 424B2 22.2K; 4 12.9K; 144 2.4K; 8-K 2.2K |
| FILED_AT | audit date | 3.0K | 0 | 2026-03-03 379; 2025-11-04 371; 2026-06-02 352; 2026-02-03 334 |
| PERIOD_OF_REPORT | date | 3.2K | 31.4K | 2021-02-28 106; 2020-02-28 105; 2019-06-25 103; 2020-05-08 103 |
| FILING_URL | id | 48.4K | 0 | https://www.sec.gov/Archi 245; https://www.sec.gov/Archi 245; https://www.sec.gov/Archi 245; https://www.sec.gov/Archi 245 |
| DOCUMENT_URL | id | 48.7K | 6 | https://www.sec.gov/Archi 245; https://www.sec.gov/Archi 245; https://www.sec.gov/Archi 245; https://www.sec.gov/Archi 245 |
| SIC_CODE | category | 15 | 0 | 6021 25.4K; 3674 6.0K; 2834 3.0K; 7389 2.0K |
| STATE_OF_INCORPORATION | state | 8 | 1.6K | DE 40.4K; NJ 2.0K; WA 1.0K; IN 1.0K |
| BUSINESS_ADDRESS | category | 25 | 0 | 270 PARK AVENUE, NEW YORK 25.4K; P.O. BOX 8999, SAN FRANCI 1.0K; 1 CUSTOMER DRIVE, BENTONV 1.0K; 22777 SPRINGWOODS VILLAGE 1.0K |
| ISIN | empty | 1 | 49.0K |  |
| EIN | category | 25 | 0 | 132624428 25.4K; 260267673 1.0K; 710415188 1.0K; 135409005 1.0K |
| _INGESTED_AT | audit | 1 | 0 | 1782938391987908 49.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | d124f698-ff64-462e-803c-9 49.0K |
| _SRC_SHA256 | who | 1 | 0 | d70ee4b6aa808882e62d20764 49.0K |
