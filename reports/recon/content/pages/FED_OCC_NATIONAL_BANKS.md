# FED_OCC_NATIONAL_BANKS

rows 724  columns 10  scan 3.1s

roles: amount 2, audit 2, other 3, state 1, who 2

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CERT | 723 | 0 | 12.5K | 59.3K | 91.3K | 13.57M |
| RSSD | 721 | 505 | 659.3K | 5.81M | 6.06M | 795.87M |

## who

NAME by rows
        11  First National Bank
         3  American Bank, National Association
         3  Citizens National Bank
         3  Western National Bank
         3  Community National Bank
         2  First National Community Bank
         2  Central National Bank
         2  First Farmers & Merchants National Bank
         2  First National Bank & Trust
         2  First National Bank and Trust
         2  City National Bank
         2  Texas National Bank
         2  Farmers National Bank
         2  Liberty National Bank
         2  Neighborhood National Bank
         1  Bessemer Trust Company, National Association
         1  Edison National Bank
         1  Canandaigua National Trust Company of Florida
         1  First National Bank of McGregor
         1  First National Bank of Commerce

NAME by dollars
      143.5K       11 rows  First National Bank
       91.3K        1 rows  CIBC National Trust Company
       69.0K        2 rows  Liberty National Bank
       59.4K        1 rows  Alvarez & Marsal Trust Company, National Association
       59.4K        1 rows  Erebor Bank, National Association
       59.4K        1 rows  IRACE Digital Bank, National Association
       59.4K        1 rows  Paycom National Trust Bank
       59.4K        1 rows  The Preferred Legacy National Trust Bank
       59.3K        1 rows  Inspire Trust Company, National Association
       59.3K        1 rows  Bessemer Trust Company of Nevada, NA
       59.3K        1 rows  TIAA Trust, National Association
       59.3K        1 rows  Dayforce National Trust Bank
       59.3K        1 rows  Hightower Trust Company, National Association
       59.3K        1 rows  Anchorage Digital Bank National Association
       59.3K        1 rows  Chilton Trust Company, National Association
       59.2K        1 rows  Agility Bank, National Association
       59.2K        1 rows  RockPointBank, National Association
       59.2K        1 rows  ADP Trust Company, National Association
       59.2K        1 rows  Varo Bank, National Association
       59.1K        1 rows  Grasshopper Bank, National Association

_SRC_SHA256 by rows
       724  dd6d1f169193ccae4c7d2ba0bb7c29b432cb697103f3e83833f390d3f039f719

_SRC_SHA256 by dollars
      13.57M      724 rows  dd6d1f169193ccae4c7d2ba0bb7c29b432cb697103f3e83833f390d3f039

## where

STATE: TX 133, IL 83, MN 44, OH 42, NY 37, OK 33, KS 28, FL 24, GA 19, WI 19, CA 19, DE 18

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CHARTER_NO | other | 715 | 0 | =COUNT(A5:A727) 4; 4341 4; 14955 4; 23926 4 |
| NAME | who | 713 | 0 | First National Bank 11; Western National Bank 6; None 4; Zions Bancorporation, Nat 4 |
| ADDRESS_LOC | other | 703 | 0 | Main Street 8; None 4; One South Main Street 4; 703 Hidalgo Blvd 4 |
| CITY | other | 557 | 0 | Wilmington 16; New York 13; Sioux Falls 9; Houston 9 |
| STATE | state | 50 | 0 | TX 133; IL 83; MN 44; OH 42 |
| CERT | amount | 716 | 0 | nan 4; 2270.0 4; 18454.0 4; 1417.0 4 |
| RSSD | amount | 734 | 0 | nan 4; 276579.0 4; 218261.0 4; 980951.0 4 |
| _INGESTED_AT | audit | 1 | 0 | 1785965657612245 724 |
| _SOURCE_RUN_ID | audit | 1 | 0 | manual-1785965656 724 |
| _SRC_SHA256 | who | 1 | 0 | dd6d1f169193ccae4c7d2ba0b 724 |
