# FED_FBI_CDE

rows 477.4K  columns 9  scan 3.2s

roles: amount 1, audit 2, category 2, other 2, state 1, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RATE_PER_100K | 476.7K | -81.24 | 8.40 | 406.71 | 7.8K | 19.15M |

## who

MONTH by rows
      1.0K  03-2014
      1.0K  01-2013
      1.0K  02-1985
      1.0K  02-2013
      1.0K  01-2010
      1.0K  03-1991
      1.0K  03-2000
      1.0K  03-2010
      1.0K  03-2007
      1.0K  04-2000
      1.0K  04-2017
      1.0K  04-2001
      1.0K  03-2015
      1.0K  03-1998
      1.0K  01-2016
      1.0K  01-2003
      1.0K  04-2011
      1.0K  03-2022
      1.0K  01-2019
      1.0K  01-2017

MONTH by dollars
      102.8K     1.0K rows  12-1997
       90.0K     1.0K rows  12-1996
       87.7K     1.0K rows  12-1991
       82.9K     1.0K rows  12-1998
       76.1K     1.0K rows  12-1993
       74.7K     1.0K rows  12-1992
       72.6K     1.0K rows  12-1999
       68.2K     1.0K rows  12-1995
       66.3K     1.0K rows  12-1990
       65.4K     1.0K rows  12-2001
       64.6K     1.0K rows  12-2002
       64.1K     1.0K rows  12-1994
       63.9K     1.0K rows  12-2000
       63.6K     1.0K rows  06-1996
       63.2K     1.0K rows  12-1989
       62.5K     1.0K rows  12-2003
       62.1K     1.0K rows  08-1995
       62.0K     1.0K rows  12-2004
       61.4K     1.0K rows  08-1990
       60.4K     1.0K rows  07-1990

## where

STATE: WY 9.4K, WI 9.4K, WV 9.4K, WA 9.4K, VA 9.4K, VT 9.4K, UT 9.4K, TX 9.4K, TN 9.4K, SD 9.4K, SC 9.4K, RI 9.4K

## what

OFFENSE: arson 10%, motor-vehicle-theft 10%, larceny 10%, burglary 10%, property-crime 10%, aggravated-assault 10%, robbery 10%, rape 10%, homicide 10%, violent-crime 10%

SERIES: OFFENSES 50%, CLEARANCES 50%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATE | state | 51 | 0 | WY 9.4K; WI 9.4K; WV 9.4K; WA 9.4K |
| OFFENSE | category | 10 | 0 | arson 47.7K; motor-vehicle-theft 47.7K; larceny 47.7K; burglary 47.7K |
| MONTH | who | 461 | 0 | 12-2023 2.4K; 12-2022 2.4K; 12-2021 2.4K; 12-2020 2.4K |
| SERIES | category | 2 | 0 | OFFENSES 238.7K; CLEARANCES 238.7K |
| COUNT | other | 24.9K | 640 | 0 16.3K; 1 6.0K; 2 5.6K; 3 5.3K |
| RATE_PER_100K | amount | 36.6K | 640 | 0.0 16.5K; 0.18 2.5K; 0.21 2.4K; 0.2 2.4K |
| _INGESTED_AT | audit | 1 | 0 | 1786302277430423 477.4K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 92cd2f6a-00a5-4f47-b2ea-0 477.4K |
| _SRC_SHA256 | other | 1 | 0 | f6962d1f64688dc28c6716398 477.4K |
