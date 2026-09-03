# PORTAL_CKA_WPRDC_ALLEGHENY_B62C61BBEB

rows 47  columns 16  scan 3.9s

roles: amount 5, audit 2, category 5, date 1, empty 2, other 1, who 1

## when

INGESTED_AT
  2026        47  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| BL_SYEARTO | 6 | 2.34 | 4.19 | 12.04 | 12.26 | 34.24 |
| YEARTOT | 6 | 3.25 | 6.08 | 7.40 | 7.42 | 35.45 |
| BIKEINFDIS | 47 | 0 | 0.30 | 5.66 | 7.42 | 37.86 |
| SLMDIST | 47 | 0 | 0 | 0.40 | 0.75 | 0.75 |
| BLDIST | 47 | 0 | 0.44 | 3.03 | 3.79 | 28.62 |

## who

SRC_SHA256 by rows
        47  16fc449f0af2c8b66ee24d7cb76a339bc9243df59af328bc461ff579c686ece6

SRC_SHA256 by dollars
       37.86       47 rows  16fc449f0af2c8b66ee24d7cb76a339bc9243df59af328bc461ff579c686

## who x when

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = BIKEINFDIS
  16fc449f0af2c8b66ee24d7cb76a339bc9243df5  2026:37.86

## what

BLNAME: Forbes Avenue (Craig to Margar 8%, S. 10th St. 8%, Hazelwood Avenue 8%, 3rd St. 8%, Phineas 8%, Negley 8%, Greenfield Bridge 8%, Federal Street 8%, Federal St 8%, Cedar 8%, Bigelow 8%, One wild Pl 8%

NOTE: Bike Lane 100%

CROSSST: Loop 17%, Craig to Margaret Morrison 8%, E. Carson to Bingham 8%, Blair to Irvine 8%, Stanwix to Smithfield 8%, Chestnut to Vinial 8%, Ellsworth to Stanton 8%, Alger to Greenfield Rd 8%, Lacock to Commons 8%, Commons to Hemlock 8%, E Ohio to North 8%

YEAR_ADDED: 2012 21%, 2015 10%, 2009 10%, 2013 10%, 2019 7%, 2017 7%, 2016 7%, 1980 7%, 2007 7%, 2008 7%, 2010 7%

DATASPATIAL_WKB: \x0000000005000000010000000002 8%, \x0000000005000000010000000002 8%, \x0000000005000000010000000002 8%, \x0000000005000000010000000002 8%, \x0000000005000000010000000002 8%, \x0000000005000000010000000002 8%, \x0000000005000000010000000002 8%, \x0000000005000000010000000002 8%, \x0000000005000000010000000002 8%, \x0000000005000000010000000002 8%, \x0000000005000000020000000002 8%, \x0000000005000000010000000002 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| BL_SYEARTO | amount | 7 | 41 | 3.49 1; 12.26 1; 7.77 1; 4 1 |
| RS | empty | 1 | 47 |  |
| BLNAME | category | 47 | 0 | Forbes Avenue (Craig to M 1; S. 10th St. 1; Hazelwood Avenue 1; 3rd St. 1 |
| YEARTOT | amount | 7 | 41 | 7.09 1; 7.42 1; 5.54 1; 3.25 1 |
| NOTE | category | 2 | 2 | Bike Lane 45 |
| BIKEINFDIS | amount | 27 | 0 | 0.0 16; 0.5 2; 0.1 2; 0.4 2 |
| CROSSST | category | 36 | 11 | Loop 2; Craig to Margaret Morriso 1; E. Carson to Bingham 1; Blair to Irvine 1 |
| SLMDIST | amount | 2 | 0 | 0.0 46; 0.75 1 |
| YEAR_ADDED | category | 17 | 12 | 2012 6; 2015 3; 2009 3; 2013 3 |
| ID | other | 1 | 0 | 0 47 |
| BLDIST | amount | 46 | 0 | 0.62862 1; 0.049326 1; 0.0 1; 0.285317 1 |
| RBL | empty | 1 | 47 |  |
| DATASPATIAL_WKB | category | 47 | 0 | \x00000000050000000100000 1; \x00000000050000000100000 1; \x00000000050000000100000 1; \x00000000050000000100000 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:23:24.68201 47 |
| SOURCE_RUN_ID | audit | 1 | 0 | 89e46a89-dd2a-4387-9cf9-b 47 |
| SRC_SHA256 | who | 1 | 0 | 16fc449f0af2c8b66ee24d7cb 47 |
