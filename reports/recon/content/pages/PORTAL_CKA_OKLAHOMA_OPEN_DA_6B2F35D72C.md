# PORTAL_CKA_OKLAHOMA_OPEN_DA_6B2F35D72C

rows 4.2K  columns 9  scan 3.3s

roles: amount 1, audit 2, category 2, date 1, other 2, who 2

## when

INGESTED_AT
  2026      4.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TAX_CREDIT_AMOUNT | 4.2K | 1 | 400 | 61.8K | 586.0K | 13.62M |

## who

NAME by rows
         3  JURGENSMEYER, CURTIS & ELLEN
         3  DUNLAP, DANIELLE
         3  FERGESON, CLINT & MARY
         3  BROWNE, MATTHEW
         3  WEST, KENDALL & CRISTINA
         2  CLARK, ROBERT & BONNEY
         2  SUMUAN, DJEFRIE & PANDA, SISKA
         2  WESTBROOK, JOHN & SHARON
         2  MORDY, MICHAEL & CHRISTY
         2  ECKLUND, SCOTT & ROBYN
         2  JONES, BARBARA
         2  LIVERMORE JR, EDWARD & LIVERMORE, MARCIA
         2  LEGATE, RICHARD & JAROL
         2  WILLIS, BUCKY & A L
         2  KALKA, LEE & LINDA
         2  BOOKS, RICHARD & REBECCA
         2  MCKINNEY JR, M ROBERT  & A MARGUER
         2  STEWART-DOYLE  , ANN GODFR
         2  REISER, RONALD & LYNDA
         2  OGDEN, JAMES & DOROTHY

NAME by dollars
      586.0K        1 rows  BENNETT, ROBERT & GINA
      494.1K        2 rows  GIBBS, EDWARD
      280.0K        1 rows  HAYWOOD, KENNETH & CYNTHIA
      203.9K        2 rows  GHAZANFARI, AHMAD & FERESHTEH
      203.9K        1 rows  ROBERTSON, CARL & DEBORAH
      152.9K        2 rows  DAKIL, SAMUEL & JENNY
      142.1K        1 rows  SWITZER, LARUE
      132.2K        1 rows  HARPER, JAY & DEBORAH
      126.7K        1 rows  FROELICH, CRAIG & BARBARA
      123.6K        1 rows  MEINDERS, HERMAN & LADONNA
      119.7K        1 rows  PAYNE, STEVEN & SILVIA
      118.5K        3 rows  FERGESON, CLINT & MARY
      117.7K        1 rows  LAGERE, WILLIAM & MARILYN
      110.0K        1 rows  LYBARGER, STANLEY & MARCIA
      110.0K        1 rows  MAYES EST, HOYT & MAYES, MAVA
      101.9K        2 rows  DILLON, BRADY & GINA
      100.0K        1 rows  HATFIELD, STEVEN & SUZETTE
      100.0K        1 rows  BLEVINS, PAT & JANICE
       92.1K        1 rows  BERRYHILL, ROBERT & JANE
       90.1K        1 rows  HUCKABAY, WADE & SHERRY

SRC_SHA256 by rows
      4.2K  219c06fbfff907bc34cf13694e0a0c6ea54a2581073a31f9d8597fbc84ef2bad

SRC_SHA256 by dollars
      13.62M     4.2K rows  219c06fbfff907bc34cf13694e0a0c6ea54a2581073a31f9d8597fbc84ef

## who x when

NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = TAX_CREDIT_AMOUNT
  BENNETT, ROBERT & GINA                    2026:586.0K
  BOOKS, RICHARD & REBECCA                  2026:20.4K
  BROWNE, MATTHEW                           2026:40.2K
  CLARK, ROBERT & BONNEY                    2026:1.8K
  DAKIL, SAMUEL & JENNY                     2026:152.9K
  DUNLAP, DANIELLE                          2026:350
  ECKLUND, SCOTT & ROBYN                    2026:2.3K
  FERGESON, CLINT & MARY                    2026:118.5K
  FROELICH, CRAIG & BARBARA                 2026:126.7K
  GHAZANFARI, AHMAD & FERESHTEH             2026:203.9K
  GIBBS, EDWARD                             2026:494.1K
  HARPER, JAY & DEBORAH                     2026:132.2K
  HAYWOOD, KENNETH & CYNTHIA                2026:280.0K
  JONES, BARBARA                            2026:1.9K
  JURGENSMEYER, CURTIS & ELLEN              2026:28.5K
  KALKA, LEE & LINDA                        2026:1.3K
  LEGATE, RICHARD & JAROL                   2026:424
  LIVERMORE JR, EDWARD & LIVERMORE, MARCIA  2026:10.1K
  MCKINNEY JR, M ROBERT  & A MARGUER        2026:57
  MEINDERS, HERMAN & LADONNA                2026:123.6K
  MORDY, MICHAEL & CHRISTY                  2026:20.4K
  OGDEN, JAMES & DOROTHY                    2026:128
  REISER, RONALD & LYNDA                    2026:256
  ROBERTSON, CARL & DEBORAH                 2026:203.9K
  STEWART-DOYLE  , ANN GODFR                2026:1.0K
  SUMUAN, DJEFRIE & PANDA, SISKA            2026:250
  SWITZER, LARUE                            2026:142.1K
  WEST, KENDALL & CRISTINA                  2026:1.1K
  WESTBROOK, JOHN & SHARON                  2026:1.7K
  WILLIS, BUCKY & A L                       2026:128

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TAX_CREDIT_AMOUNT
  219c06fbfff907bc34cf13694e0a0c6ea54a2581  2026:13.62M

## what

TAX_CREDIT_TYPE: VOLUNTEER FIREFIGHTER CREDIT 38%, CREDIT FOR BIOMEDICAL RESEARCH 27%, OKLAHOMA INVESTMENT/NEW JOBS C 9%, CREDIT FOR CONVERSION OF MOTOR 8%, RURAL SMALL BUSINESS CAPITAL C 4%, CREDIT FOR ENERGY ASSISTANCE F 3%, SMALL BUSINESS CAPITAL CREDIT 2%, SMALL BUSINESS GUARANTY FEE CR 2%, POULTRY LITTER CREDIT 2%, CREDIT FOR THE CONSTRUCTION OF 2%, OTHER OKLAHOMA CREDITS 2%, CREDIT FOR VENTURE CAPITAL INV 2%

TAX_CREDIT_DESCRIPTION: An income tax credit of Two Hu 39%, An income tax credit for donat 27%, Income tax credit (nonrefundab 9%, A one-time income tax credit f 8%, An income tax credit for inves 4%, Individuals or corporations ar 3%, An income tax credit for inves 2%, Credit of any amount paid by a 2%, An income tax credit of Five D 2%, A nonrefundable income tax cre 2%, Individuals or corporations ar 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FISCAL_YEAR | other | 1 | 0 | FYE08 4.2K |
| YEAR | other | 1 | 0 | 2007 4.2K |
| NAME | who | 4.0K | 0 | STAYER, RALPH & CAROL 21; HENRY, CHRISTOPH & CATHER 21; HAYES, KENNETH 21; WILLIAMS, GORDON 21 |
| TAX_CREDIT_TYPE | category | 33 | 0 | VOLUNTEER FIREFIGHTER CRE 1.5K; CREDIT FOR BIOMEDICAL RES 1.1K; OKLAHOMA INVESTMENT/NEW J 347; CREDIT FOR CONVERSION OF  301 |
| TAX_CREDIT_AMOUNT | amount | 972 | 0 | 400 781; 200 765; 1500 187; 25 148 |
| TAX_CREDIT_DESCRIPTION | category | 33 | 73 | An income tax credit of T 1.5K; An income tax credit for  1.1K; Income tax credit (nonref 347; A one-time income tax cre 301 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:32:25.83724 4.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | d1fd84e3-ae36-40bd-a2ae-d 4.2K |
| SRC_SHA256 | who | 1 | 0 | 219c06fbfff907bc34cf13694 4.2K |
