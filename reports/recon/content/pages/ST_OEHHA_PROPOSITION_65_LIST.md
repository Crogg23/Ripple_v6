# ST_OEHHA_PROPOSITION_65_LIST

rows 1.0K  columns 12  scan 2.8s

roles: amount 1, audit 2, category 2, date 1, empty 3, other 2, who 1

## when

DATE_LISTED
  1987        85  ###############
  1988       166  ##############################
  1989        77  ##############
  1990       147  ###########################
  1991        23  ####
  1992        44  ########
  1993         6  #
  1994        13  ##
  1995         2  
  1996        23  ####
  1997        32  ######
  1998        35  ######
  1999        66  ############
  2000        11  ##
  2001        16  ###
  2002         6  #
  2003         6  #
  2004        11  ##
  2005        11  ##
  2006         4  #
  2007         3  #
  2008        12  ##
  2009        25  #####
  2010        13  ##
  2011        25  #####
  2012        11  ##
  2013        11  ##
  2014        23  ####
  2015        11  ##
  2016        16  ###
  2017        12  ##
  2018         4  #
  2019         8  #
  2020         3  #
  2021         8  #
  2022         1  
  2023        12  ##
  2025         4  #
  2026         4  #

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| NSRL_OR_MADL_G_DAY_A | 269 | 0 | 1 | 1.5K | 10.0K | 26.4K |

## who

_SRC_SHA256 by rows
      1.0K  d084c22cda0d1add009a1ab5405007d48468dbf8f4c1f22f7490a524ff3e624a

_SRC_SHA256 by dollars
       26.4K     1.0K rows  d084c22cda0d1add009a1ab5405007d48468dbf8f4c1f22f7490a524ff3e

## who x when

_SRC_SHA256 by DATE_LISTED, dollars = NSRL_OR_MADL_G_DAY_A
  d084c22cda0d1add009a1ab5405007d48468dbf8  1987:124.88 1988:2.3K 1989:973.59 1990:5.4K 1991:174 1992:9.06 1993:6 1994:2.37 1995:2 1996:52.50 1997:89 1998:479.90 1999:2.7K 2000:96.11 2001:16 2002:6.50 2003:6 2004:11 2005:8.70 2006:4 2007:2.2K 2008:11 2009:20 2010:5.10 2011:10.2K 2012:11 2013:155.90 2014:23 2015:11 2016:207.95 2017:1.1K 2018:4 2019:23 2020:3 2021:8 2022:1 2023:12 2025:4 2026:4

## what

TYPE_OF_TOXICITY: cancer 59%, developmental 16%, cancer  8%, developmental  7%, male  2%, developmental, female, male  2%, developmental, male  2%, developmental, female 1%, male 1%, developmental, male 1%, developmental, female  1%

LISTING_MECHANISM: SQE 33%, AB 31%, FR 20%, LC 15%, LC SQE 0%, LC     0%, AB                         0%, SQE - developmental     FR - f 0%, SQE - developmental    FR - fe 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CHEMICAL | other | 955 | 0 | f Hydrogen cyanide and cy 6; e Sulfur dioxide MADL was 6; d Butyl benzyl phthalate  6; c Level represents absorb 6 |
| TYPE_OF_TOXICITY | category | 26 | 31 | cancer 564; developmental 153; cancer  81; developmental  70 |
| LISTING_MECHANISM | category | 11 | 32 | SQE 328; AB 310; FR 199; LC 146 |
| CAS_NO | other | 799 | 32 | --- 83;  --- 19;   --- 8; 106-87-6 6 |
| DATE_LISTED | date | 187 | 31 | 1988-01-01 100; 1990-07-01 49; 1988-04-01 48; 1990-01-01 46 |
| NSRL_OR_MADL_G_DAY_A | amount | 163 | 684 | 0.2 12; 20 12; 5 11; 0.3 10 |
| COL_6 | empty | 1 | 1.0K |  |
| COL_7 | empty | 1 | 1.0K |  |
| COL_8 | empty | 1 | 1.0K |  |
| _INGESTED_AT | audit | 1 | 0 | 1785965286666319 1.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 74b460f0-6897-40f8-ab47-1 1.0K |
| _SRC_SHA256 | who | 1 | 0 | d084c22cda0d1add009a1ab54 1.0K |
