# XC_WIKIPEDIA_LARGEST_US_COMPANIES

rows 100  columns 10  scan 2.7s

roles: amount 1, audit 2, category 1, other 4, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| REVENUE_USD_MILLIONS | 100 | 45.0K | 84.8K | 638.4K | 681.0K | 13.05M |

## who

NAME by rows
         1  TIAA
         1  Kroger
         1  HP
         1  Cigna
         1  Coca-Cola
         1  Microsoft
         1  The Home Depot
         1  United Parcel Service
         1  Goldman Sachs Group
         1  IBM
         1  Humana
         1  Plains GP Holdings
         1  Morgan Stanley
         1  Oracle
         1  Valero Energy
         1  Apple
         1  General Dynamics
         1  Exxon Mobil
         1  United Airlines Holdings
         1  Comcast

NAME by dollars
      681.0K        1 rows  Walmart
      638.0K        1 rows  Amazon
      400.3K        1 rows  UnitedHealth Group
      391.0K        1 rows  Apple
      372.8K        1 rows  CVS Health
      371.4K        1 rows  Berkshire Hathaway
      350.0K        1 rows  Alphabet
      349.6K        1 rows  Exxon Mobil
      309.0K        1 rows  McKesson Corporation
      294.0K        1 rows  Cencora
      278.9K        1 rows  JPMorgan Chase
      254.5K        1 rows  Costco Wholesale
      247.1K        1 rows  Cigna
      245.1K        1 rows  Microsoft
      226.8K        1 rows  Cardinal Health
      202.8K        1 rows  Chevron
      192.4K        1 rows  Bank of America
      187.4K        1 rows  General Motors
      185.0K        1 rows  Ford Motor
      177.0K        1 rows  Elevance Health

_SRC_SHA256 by rows
       100  19a5d25c4242a457fcf0462f9211b7e12aa230ed93e392b2e8dd18da7c7b4648

_SRC_SHA256 by dollars
      13.05M      100 rows  19a5d25c4242a457fcf0462f9211b7e12aa230ed93e392b2e8dd18da7c7b

## what

INDUSTRY: Financials 21%, Technology 12%, Petroleum 12%, Retail 12%, Healthcare 9%, Insurance 8%, Pharmaceutical 6%, Aerospace and defense 5%, Food processing 4%, Airline 4%, Telecommunications 4%, Technology and cloud computing 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| RANK | other | 99 | 0 | 100 1; 99 1; 98 1; 97 1 |
| NAME | who | 100 | 0 | Eli Lilly 1; Travelers 1; TIAA 1; Coca-Cola 1 |
| INDUSTRY | category | 30 | 0 | Financials 16; Technology 9; Petroleum 9; Retail 9 |
| REVENUE_USD_MILLIONS | amount | 100 | 0 | 45043 1; 46423 1; 46946 1; 47061 1 |
| REVENUE_GROWTH | other | 88 | 0 | 0.9% 3; 6.2% 3; -0.1% 2; 2.8% 2 |
| EMPLOYEES | other | 98 | 0 | 108000 2; 47000 1; 34000 1; 15623 1 |
| HEADQUARTERS | other | 71 | 0 | New York City, New York 13; Houston, Texas 6; Atlanta, Georgia 4; Indianapolis, Indiana 2 |
| _INGESTED_AT | audit | 1 | 0 | 1781708911467445 100 |
| _SOURCE_RUN_ID | audit | 1 | 0 | f07296d8-6128-423d-a537-b 100 |
| _SRC_SHA256 | who | 1 | 0 | 19a5d25c4242a457fcf0462f9 100 |
