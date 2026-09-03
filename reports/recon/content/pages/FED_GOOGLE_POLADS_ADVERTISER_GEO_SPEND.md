# FED_GOOGLE_POLADS_ADVERTISER_GEO_SPEND

rows 614.1K  columns 27  scan 4.5s

roles: amount 2, audit 2, category 1, other 20, state 1, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SPEND_USD | 614.1K | 0 | 100 | 44.4K | 15.60M | 2.53B |
| SPEND_GBP | 614.1K | 0 | 0 | 0 | 50 | 50 |

## who

ADVERTISER_NAME by rows
       625  Inmo Khang
       311  MAXWELL RYMER
       208  Nicholas Perhai
       177  Lovead Limited
       164  NANCY MACE FOR CONGRESS
       162  New Yorkers for Lower Costs
       157  Republican Party of Iowa
       157  MONICA TRANEL FOR MONTANA
       156  COLLINS FOR CONGRESS
       156  Thomas Massie for Congress
       156  Ryan O'Daniel
       148  MAGGIE FOR NH
       146  US House of Representatives
       137  LALOTA FOR CONGRESS
       136  One Person One Vote
       134  Defend and Protect Idaho
       128  Friends for Kathy Hochul
       121  FRIENDS OF JEVIN D. HODGE
       119  CIATTARELLI FOR GOVERNOR
       115  SAM BROWN FOR NEVADA

ADVERTISER_NAME by dollars
     100.72M       57 rows  BIDEN FOR PRESIDENT
      81.81M       57 rows  DONALD J. TRUMP FOR PRESIDENT, INC.
      67.18M       57 rows  HARRIS VICTORY FUND
      62.14M       57 rows  FF PAC
      61.89M       56 rows  MIKE BLOOMBERG 2020 INC
      53.65M       57 rows  HARRIS FOR PRESIDENT
      43.21M       57 rows  TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE
      42.22M      109 rows  SENATE LEADERSHIP FUND
      32.71M       57 rows  DSCC
      32.28M       57 rows  DONALD J. TRUMP FOR PRESIDENT 2024, INC.
      30.87M       57 rows  BIDEN VICTORY FUND
      28.99M       56 rows  WinSenate
      28.48M       57 rows  TRUMP NATIONAL COMMITTEE JFC
      26.25M       57 rows  DNC SERVICES CORP / DEMOCRATIC NATIONAL COMMITTEE
      24.34M      110 rows  CONGRESSIONAL LEADERSHIP FUND
      21.89M       54 rows  AMERICANS FOR PROSPERITY ACTION INC
      20.95M       57 rows  NRSC
      20.39M       57 rows  DCCC
      19.59M      106 rows  PRESERVE AMERICA PAC
      18.50M       57 rows  Money Metals Exchange LLC

## where

COUNTRY_SUBDIVISION_PRIMARY: CA 13.1K, FL 13.0K, TX 12.9K, PA 12.7K, IL 12.7K, VA 12.6K, NC 12.6K, GA 12.5K, OH 12.5K, NY 12.4K, IN 12.4K, MI 12.4K

## what

COUNTRY: US 100%, GB 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ADVERTISER_ID | other | 16.0K | 0 | AR11496704995496034305 2.1K; AR05130965087980355585 2.1K; AR14923847657980952577 2.0K; AR11600903616516325377 2.0K |
| ADVERTISER_NAME | who | 15.6K | 0 | BIRD FOR GOVERNOR 2.1K; Friends of Sara Knizhnik 2.1K; Sparacino for Oregon 2.0K; Jim Jordan for Congress 2.0K |
| COUNTRY | category | 2 | 0 | US 614.1K; GB 1 |
| COUNTRY_SUBDIVISION_PRIMARY | state | 56 | 11.3K | CA 13.1K; FL 13.0K; TX 12.9K; PA 12.7K |
| SPEND_USD | amount | 3.4K | 0 | 100 432.6K; 0 104.8K; 200 12.4K; 300 7.0K |
| SPEND_EUR | other | 1 | 0 | 0 614.1K |
| SPEND_INR | other | 1 | 0 | 0 614.1K |
| SPEND_BGN | other | 1 | 0 | 0 614.1K |
| SPEND_CZK | other | 1 | 0 | 0 614.1K |
| SPEND_DKK | other | 1 | 0 | 0 614.1K |
| SPEND_HUF | other | 1 | 0 | 0 614.1K |
| SPEND_PLN | other | 1 | 0 | 0 614.1K |
| SPEND_RON | other | 1 | 0 | 0 614.1K |
| SPEND_SEK | other | 1 | 0 | 0 614.1K |
| SPEND_GBP | amount | 2 | 0 | 0 614.1K; 50 1 |
| SPEND_NZD | other | 1 | 0 | 0 614.1K |
| SPEND_ILS | other | 1 | 0 | 0 614.1K |
| SPEND_AUD | other | 1 | 0 | 0 614.1K |
| SPEND_TWD | other | 1 | 0 | 0 614.1K |
| SPEND_BRL | other | 1 | 0 | 0 614.1K |
| SPEND_ARS | other | 1 | 0 | 0 614.1K |
| SPEND_ZAR | other | 1 | 0 | 0 614.1K |
| SPEND_CLP | other | 1 | 0 | 0 614.1K |
| SPEND_MXN | other | 1 | 0 | 0 614.1K |
| INGESTED_AT | audit | 1 | 0 | 1785965602280091 614.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4141cf7d-a262-4c65-b58b-3 614.1K |
| SRC_SHA256 | other | 1 | 0 | b4de0c2647cdab05b29b428eb 614.1K |
