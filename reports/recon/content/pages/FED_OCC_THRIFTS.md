# FED_OCC_THRIFTS

rows 218  columns 13  scan 3.2s

roles: amount 2, audit 2, other 6, state 1, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CERT | 217 | 1.4K | 29.6K | 58.2K | 90.3K | 6.63M |
| RSSD | 217 | 4.0K | 606.2K | 3.32M | 3.53M | 167.44M |

## who

NAME by rows
         4  First FS & LA
         2  First Federal Bank
         2  First Federal Savings Bank
         1  First Seacoast Bank
         1  Home Savings Bank, FSB
         1  El Dorado Savings Bank, F.S.B.
         1  Home Federal Bank
         1  Kentland FS & LA
         1  Auburn Savings Bank, FSB
         1  First Federal SB of Twin Falls
         1  Windsor Federal Bank
         1  Pickens Savings and Loan Association, F.A.
         1  Midwest Heritage Bank, F.S.B.
         1  Massena Savings and Loan
         1  Lyons Federal Bank
         1  Woodruff FS & LA
         1  Martinsville First Savings Bank
         1  First Shore FS & LA
         1  First Piedmont FS & LA of Gaffney
         1  Cumberland Federal Bank, FSB

NAME by dollars
      120.6K        4 rows  First FS & LA
       90.3K        1 rows  Westfield Bank
       62.4K        2 rows  First Federal Bank
       60.4K        2 rows  First Federal Savings Bank
       58.5K        1 rows  Think Mutual Bank
       58.3K        1 rows  Ameriprise Bank, FSB
       57.8K        1 rows  Quontic Bank
       57.5K        1 rows  Members Trust Company
       57.1K        1 rows  Community Federal Savings Bank
       57.1K        1 rows  Everence Trust Company
       57.1K        1 rows  Northwestern Mutual Wealth Management
       35.6K        1 rows  Country Trust Bank
       35.5K        1 rows  Axos Bank
       35.5K        1 rows  The Federal Savings Bank
       35.5K        1 rows  D.A. Davidson Trust Company
       35.4K        1 rows  MassMutual Private Wealth & Trust, FSB
       35.4K        1 rows  United Trust Bank
       35.4K        1 rows  SEI Private Trust Company
       35.2K        1 rows  John Deere Financial, f.s.b.
       35.2K        1 rows  Fidelity Personal Trust Company, FSB

_SRC_SHA256 by rows
       218  fdaa13543e7aa95b07a5d28b3295ca89f05e1da0cce9d647187eb75da0d071ba

_SRC_SHA256 by dollars
       6.63M      218 rows  fdaa13543e7aa95b07a5d28b3295ca89f05e1da0cce9d647187eb75da0d0

## where

STATE: OH 24, IL 16, NY 15, LA 11, PA 10, CA 9, IN 9, WI 8, KY 8, MA 7, KS 7, MD 7

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CHARTER_NO | other | 222 | 0 | =COUNT(A5:A222) 2; 703435 2; 703150 2; 701149 2 |
| NAME | who | 216 | 0 | First FS & LA 4; None 2; Worthington Federal Savin 2; Woodruff FS & LA 2 |
| ADDRESS_LOC | other | 220 | 0 | None 2; 418 11th St 2; 247 N Main St 2; 342 Broadway 2 |
| CITY | other | 200 | 0 | Chicago 5; Covington 3; Somerville 2; Wilmington 2 |
| STATE | state | 48 | 0 | OH 24; IL 16; NY 15; LA 11 |
| CERT | amount | 217 | 0 | nan 2; 29426.0 2; 29238.0 2; 28213.0 2 |
| RSSD | amount | 215 | 0 | nan 2; 258874.0 2; 661474.0 2; 822275.0 2 |
| COL7 | other | 1 | 0 | None 218 |
| COL8 | other | 1 | 0 | None 218 |
| COL9 | other | 1 | 0 | None 218 |
| _INGESTED_AT | audit | 1 | 0 | 1785965666725918 218 |
| _SOURCE_RUN_ID | audit | 1 | 0 | manual-1785965656 218 |
| _SRC_SHA256 | who | 1 | 0 | fdaa13543e7aa95b07a5d28b3 218 |
