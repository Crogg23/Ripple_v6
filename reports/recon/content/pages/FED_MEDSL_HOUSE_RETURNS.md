# FED_MEDSL_HOUSE_RETURNS

rows 29.6K  columns 22  scan 5.3s

roles: amount 1, audit 2, category 10, date 1, other 2, state 1, who 5

## when

VERSION
  2017     28.3K  ##############################
  2019      1.4K  #

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTALVOTES | 29.6K | 0 | 201.2K | 387.0K | 762.5K | 6.15B |

## who

PARTY by rows
      9.1K  democrat
      8.8K  republican
      2.6K  libertarian
      2.1K  NA
      1.1K  independent
       621  conservative
       491  green
       371  natural law
       266  liberal
       245  working families
       229  independence
       225  right to life
       173  reform
       165  peace and freedom
       140  constitution
       132  socialist workers
       104  american independent
       101  democratic-farmer-labor
        72  american
        67  none

PARTY by dollars
       1.84B     9.1K rows  democrat
       1.83B     8.8K rows  republican
     539.70M     2.6K rows  libertarian
     448.48M     2.1K rows  NA
     232.22M     1.1K rows  independent
     117.29M      491 rows  green
     112.22M      621 rows  conservative
      77.88M      371 rows  natural law
      55.66M      245 rows  working families
      54.03M      229 rows  independence
      40.23M      225 rows  right to life
      40.02M      173 rows  reform
      39.55M      266 rows  liberal
      35.88M      140 rows  constitution
      31.45M      165 rows  peace and freedom
      28.77M      101 rows  democratic-farmer-labor
      22.01M      132 rows  socialist workers
      18.03M       67 rows  none
      17.76M      104 rows  american independent
      17.49M       63 rows  no party affiliation

OFFICE by rows
     29.6K  US House

OFFICE by dollars
       6.15B    29.6K rows  US House

CANDIDATEVOTES by rows
       306  1
       101  2
        96  3
        72  5
        68  4
        54  9
        54  8
        54  7
        53  6
        45  10
        38  11
        38  13
        36  20
        36  12
        33  17
        32  18
        28  16
        26  23
        22  15
        21  14

CANDIDATEVOTES by dollars
      22.22M      306 rows  1
      18.83M      101 rows  2
      17.92M       96 rows  3
      14.58M       72 rows  5
      12.21M       68 rows  4
      10.93M       54 rows  9
      10.51M       54 rows  7
      10.33M       53 rows  6
       9.88M       54 rows  8
       9.42M       45 rows  10
       7.99M       36 rows  20
       7.86M       38 rows  13
       7.73M       38 rows  11
       7.06M       36 rows  12
       6.58M       32 rows  18
       6.14M       28 rows  16
       5.96M       33 rows  17
       4.99M       26 rows  23
       4.36M       20 rows  19
       4.13M       22 rows  15

CANDIDATE by rows
      2.1K  NA
       415  Other
       373  Blank Vote/Scattering
       319  scatter
        65  Blank Vote
        54  Blank Vote/Void Vote/Scattering
        47  Charles B. Rangel
        42  Peter T. King
        35  Eliot L. Engel
        35  Gary L. Ackerman
        33  Carolyn B. Maloney
        28  John J. LaFalce
        28  Michael R. McNulty
        27  Maurice D. Hinchey
        27  Nita M. Lowey
        26  Edolphus Towns
        26  James T. Walsh
        25  Jerrold Nadler
        24  Carolyn McCarthy
        24  Major R. Owens

CANDIDATE by dollars
     447.21M     2.1K rows  NA
      96.17M      415 rows  Other
      82.81M      373 rows  Blank Vote/Scattering
      66.23M      319 rows  scatter
      18.55M       65 rows  Blank Vote
      11.05M       54 rows  Blank Vote/Void Vote/Scattering
      10.37M       42 rows  Peter T. King
       7.09M       28 rows  Michael R. McNulty
       6.96M       33 rows  Carolyn B. Maloney
       6.34M       27 rows  Nita M. Lowey
       6.26M       27 rows  Maurice D. Hinchey
       6.19M       35 rows  Eliot L. Engel
       6.10M       26 rows  James T. Walsh
       6.03M       35 rows  Gary L. Ackerman
       5.78M       47 rows  Charles B. Rangel
       5.77M       24 rows  Louise McIntosh Slaughter
       5.66M       24 rows  Carolyn McCarthy
       5.19M       28 rows  John J. LaFalce
       5.11M       16 rows  Void Vote
       5.11M       25 rows  Jerrold Nadler

## who x when

PARTY by VERSION, dollars = TOTALVOTES
  NA                                        2017:405.53M 2019:42.95M
  american                                  2017:13.05M 2019:727.3K
  american independent                      2017:17.76M
  conservative                              2017:107.87M 2019:4.35M
  constitution                              2017:33.86M 2019:2.02M
  democrat                                  2017:1.71B 2019:130.75M
  democratic-farmer-labor                   2017:26.19M 2019:2.58M
  green                                     2017:109.57M 2019:7.71M
  independence                              2017:50.67M 2019:3.37M
  independent                               2017:216.48M 2019:15.74M
  liberal                                   2017:39.55M
  libertarian                               2017:509.61M 2019:30.09M
  natural law                               2017:77.88M
  no party affiliation                      2017:13.69M 2019:3.81M
  none                                      2017:18.03M
  peace and freedom                         2017:31.45M
  reform                                    2017:34.22M 2019:5.80M
  republican                                2017:1.71B 2019:123.01M
  right to life                             2017:40.23M
  socialist workers                         2017:22.01M
  working families                          2017:49.03M 2019:6.63M

OFFICE by VERSION, dollars = TOTALVOTES
  US House                                  2017:5.75B 2019:397.83M

## where

STATE_PO: NY 3.6K, CA 3.1K, TX 1.8K, MI 1.5K, NJ 1.2K, PA 1.1K, IL 1.1K, FL 1.1K, OH 1.1K, VA 773, MA 761, TN 734

## what

YEAR: 1996 10%, 2000 9%, 1992 9%, 2010 9%, 2016 8%, 2002 8%, 2012 8%, 2008 8%, 2006 8%, 1998 8%, 2018 8%, 2014 8%

STATE: New York 20%, California 18%, Texas 10%, Michigan 8%, New Jersey 7%, Pennsylvania 6%, Illinois 6%, Florida 6%, Ohio 6%, Virginia 4%, Massachusetts 4%, Tennessee 4%

STATE_FIPS: 36 20%, 6 18%, 48 10%, 26 8%, 34 7%, 42 6%, 17 6%, 12 6%, 39 6%, 51 4%, 25 4%, 47 4%

STATE_CEN: 21 20%, 93 18%, 74 10%, 34 8%, 22 7%, 23 6%, 33 6%, 59 6%, 31 6%, 54 4%, 14 4%, 62 4%

STATE_IC: 13 20%, 71 18%, 49 10%, 23 8%, 12 7%, 14 6%, 21 6%, 43 6%, 24 6%, 40 4%, 3 4%, 54 4%

STAGE: gen 100%, pri 0%

RUNOFF: FALSE 71%, NA 29%, TRUE 0%

SPECIAL: FALSE 100%, TRUE 0%

WRITEIN: FALSE 93%, TRUE 7%

UNOFFICIAL: FALSE 100%, TRUE 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | category | 22 | 0 | 1996 1.7K; 2000 1.6K; 1992 1.5K; 2010 1.5K |
| STATE | category | 49 | 0 | New York 3.6K; California 3.1K; Texas 1.8K; Michigan 1.5K |
| STATE_PO | state | 50 | 0 | NY 3.6K; CA 3.1K; TX 1.8K; MI 1.5K |
| STATE_FIPS | category | 50 | 0 | 36 3.6K; 6 3.1K; 48 1.8K; 26 1.5K |
| STATE_CEN | category | 50 | 0 | 21 3.6K; 93 3.1K; 74 1.8K; 34 1.5K |
| STATE_IC | category | 49 | 0 | 13 3.6K; 71 3.1K; 49 1.8K; 23 1.5K |
| OFFICE | who | 1 | 0 | US House 29.6K |
| DISTRICT | other | 54 | 0 | 2 3.0K; 1 2.9K; 3 2.5K; 4 2.3K |
| STAGE | category | 3 | 30 | gen 29.5K; pri 60 |
| RUNOFF | category | 3 | 0 | FALSE 21.0K; NA 8.7K; TRUE 8 |
| SPECIAL | category | 2 | 0 | FALSE 29.5K; TRUE 90 |
| CANDIDATE | who | 15.0K | 6 | NA 2.1K; Other 425; Blank Vote/Scattering 418; scatter 319 |
| PARTY | who | 423 | 1.3K | democrat 9.1K; republican 8.8K; libertarian 2.6K; NA 2.1K |
| WRITEIN | category | 2 | 0 | FALSE 27.5K; TRUE 2.2K |
| MODE | other | 1 | 0 | total 29.6K |
| CANDIDATEVOTES | who | 24.2K | 0 | 1 306; 391 148; 6070 148; 6918 148 |
| TOTALVOTES | amount | 9.3K | 0 | 1 181; 287986 153; 235267 152; 192173 152 |
| UNOFFICIAL | category | 2 | 0 | FALSE 29.6K; TRUE 39 |
| VERSION | date | 4 | 0 | 20171005 28.3K; 20190110 1.4K; 20190222 5; 20190307 4 |
| _INGESTED_AT | audit | 1 | 0 | 1782860772170916 29.6K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 741a02e3-9803-4bca-b22d-1 29.6K |
| _SRC_SHA256 | who | 1 | 0 | 0b8db55210fdc7998d14fe767 29.6K |
