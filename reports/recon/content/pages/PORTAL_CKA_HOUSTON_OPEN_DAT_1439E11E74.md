# PORTAL_CKA_HOUSTON_OPEN_DAT_1439E11E74

rows 135  columns 7  scan 2.9s

roles: audit 2, date 2, other 1, who 3

## when

EXPIRES
  2015       120  ##############################
  2016        13  ###

INGESTED_AT
  2026       135  ##############################

## who

EMPLOYER_BEHALF_OF by rows
         6  CenterPoint Energey
         4  Walmart
         4  Delaware North Companies, Inc
         3  Westfield Concession Management, LLC
         3  4 Families of Houston LLC
         3  AECOM
         3  Houston Super Bowl Bidding Committee
         3  AT&T
         3  Center Point Energy
         2  Taser International, Inc.
         2  Greater Houston Partnership
         2  Black Forest Ventures
         2  the Joint Venture for the Advertising Concession at Houston Airports, 
         2  Houston Police Officers' Pension System
         2  Blue Cross Blue Shield of Texas
         2  Human Rights Campaign
         2  Hudson Group
         2  Verizon Wireless
         2  American Express
         2  Landry's Restaurants, Inc.

REGISTRANT by rows
        21  Jones, Dallas S.
        11  Partida, Neftali
         9  Miller, Robert D.
         8  Sanders, Joshua
         7  Staas, David
         7  Carter, Darryl B.
         6  Huey, Helen
         6  Chevalier, Felix
         5  Margraves, Ross D.
         5  Joiner, Patricia Knudson
         3  McCulley, Hugh L. 
         2  Perkins, Arthur Val
         1  Clutterbuck, Anne
         1  Teas, Andrew
         1  Harder, Charles J.
         1  Bering, Adam
         1  Prado, Nina
         1  Warbelow, Sarah
         1  Hall, Darrin M.
         1  Brown, Kenneth W.

SRC_SHA256 by rows
       135  c3d338ea42908415bf003be2e44621ac623c22a3f3cdc7f28c20f97b26198d3d

## who x when

EMPLOYER_BEHALF_OF by EXPIRES
  4 Families of Houston LLC                 2015:2 2016:1
  AECOM                                     2015:3
  AT&T                                      2015:1 2016:2
  American Express                          2015:2
  Black Forest Ventures                     2015:2
  Blue Cross Blue Shield of Texas           2015:2
  Center Point Energy                       2015:3
  CenterPoint Energey                       2015:5 2016:1
  Delaware North Companies, Inc             2015:3 2016:1
  Greater Houston Partnership               2015:2
  Houston Police Officers' Pension System   2015:2
  Houston Super Bowl Bidding Committee      2015:1 2016:1
  Hudson Group                              2015:2
  Human Rights Campaign                     2015:2
  Landry's Restaurants, Inc.                2015:2
  Taser International, Inc.                 2015:2
  Verizon Wireless                          2015:2
  Walmart                                   2015:4
  Westfield Concession Management, LLC      2015:3
  the Joint Venture for the Advertising Co  2015:2

REGISTRANT by EXPIRES
  Bering, Adam                              2015:1
  Brown, Kenneth W.                         2015:1
  Carter, Darryl B.                         2015:7
  Chevalier, Felix                          2015:6
  Clutterbuck, Anne                         2015:1
  Hall, Darrin M.                           2015:1
  Harder, Charles J.                        2015:1
  Huey, Helen                               2015:6
  Joiner, Patricia Knudson                  2015:5
  Jones, Dallas S.                          2015:21
  Margraves, Ross D.                        2015:5
  McCulley, Hugh L.                         2016:3
  Miller, Robert D.                         2015:9
  Partida, Neftali                          2015:11
  Perkins, Arthur Val                       2015:2
  Prado, Nina                               2015:1
  Sanders, Joshua                           2015:8
  Staas, David                              2015:7
  Teas, Andrew                              2016:1
  Warbelow, Sarah                           2015:1

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REGISTRANT | who | 57 | 0 | Jones, Dallas S. 21; Partida, Neftali 11; Miller, Robert D. 9; Sanders, Joshua 8 |
| ACCOUNT_NO | other | 56 | 0 | 359 21; 381 11; 6 9; 374 8 |
| EMPLOYER_BEHALF_OF | who | 92 | 0 | CenterPoint Energey 6; Delaware North Companies, 4; Walmart 4; 4 Families of Houston LLC 3 |
| EXPIRES | date | 40 | 0 | 2015-12-18 00:00:00 22; 2015-12-26 00:00:00 20; 2015-05-12 00:00:00 12; 2015-06-27 00:00:00 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:16:17.33561 135 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0f95b48e-c1a2-4906-b2a0-4 135 |
| SRC_SHA256 | who | 1 | 0 | c3d338ea42908415bf003be2e 135 |
