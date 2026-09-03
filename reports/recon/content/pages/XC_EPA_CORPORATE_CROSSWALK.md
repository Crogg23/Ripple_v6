# XC_EPA_CORPORATE_CROSSWALK

rows 5.30M  columns 13  scan 6.5s

roles: amount 1, audit 2, category 1, date 1, id 1, other 3, who 5

## when

_INGESTED_AT
  2026     5.30M  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| MATCH_CONFIDENCE | 279.6K | 0.80 | 0.85 | 1 | 1 | 246.0K |

## who

FACILITY_NAME by rows
     33.3K  RESIDENCE
     14.3K  CON EDISON
     10.3K  UNKNOWN
      2.1K  SUNOCO SERVICE STATION
      1.6K  PACIFIC BELL
      1.4K  MI DEPT/TRANSPORTATION
      1.3K  VACANT RESIDENCE
      1.1K  SHELL SERVICE STATION
      1.0K  NEW CINGULAR WIRELESS PCS LLC
       844  MI DEPT/STATE POLICE
       825  PENSKE TRUCK LEASING CO LP
       821  DOLLAR GENERAL
       777  VERIZON WIRELESS
       736  SHELL OIL CO
       717  IDOT
       710  VACANT HOUSE
       665  SHELL
       640  LA DOTD
       624  MI DEPT/NATURAL RESOURCES AND ENVIRONMENT
       623  AMOCO OIL CO

FACILITY_NAME by dollars
       12.2K    14.3K rows  CON EDISON
        1.8K     2.1K rows  SUNOCO SERVICE STATION
        1.4K     1.6K rows  PACIFIC BELL
      966.45     1.1K rows  SHELL SERVICE STATION
      855.10     1.0K rows  NEW CINGULAR WIRELESS PCS LLC
      693.80      821 rows  DOLLAR GENERAL
      660.45      777 rows  VERIZON WIRELESS
      625.60      736 rows  SHELL OIL CO
      504.90      594 rows  AT&T MOBILITY
      481.60      602 rows  ATLANTIC CITY ELECTRIC CO
         442      520 rows  CHEVRON USA INC
      419.05      493 rows  CSX TRANSPORTATION INC
      419.05      493 rows  UNION PACIFIC RAILROAD
      411.40      484 rows  EXXON MOBIL CORPORATION
      379.95      447 rows  SHERWIN WILLIAMS CO
      348.50      410 rows  MOBIL OIL CORP
         348      348 rows  TEXAS DEPARTMENT OF TRANSPORTATION
      334.05      393 rows  FAMILY DOLLAR STORES
      317.05      373 rows  SUNOCO INC
      279.65      329 rows  CHEVRON

MATCHED_LEGAL_NAME by rows
     50.9K  CONSOLIDATED EDISON, INC.
     13.3K  CVS HEALTH CORPORATION
     12.9K  AT&T INC.
     12.6K  VERIZON COMMUNICATIONS INC.
      9.8K  EXXONMOBIL OIL CORPORATION
      8.2K  WALMART INC.
      7.7K  WALGREEN CO.
      7.5K  DOLLAR GENERAL CORPORATION
      7.4K  DOLLAR TREE, INC.
      7.3K  Chevron U.S.A. Inc.
      6.6K  7-Eleven, Inc.
      5.6K  CIRCLE K STORES INC.
      5.4K  SUNOCO LP
      4.1K  Rite Aid Corporation
      3.8K  SHELL USA, INC.
      3.6K  PACIFIC GAS AND ELECTRIC COMPANY
      3.3K  THE SHERWIN-WILLIAMS COMPANY
      3.2K  NOBLE ENERGY, INC.
      3.1K  AutoZone, Inc.
      2.9K  HOME DEPOT U.S.A., INC.

MATCHED_LEGAL_NAME by dollars
       43.3K    50.9K rows  CONSOLIDATED EDISON, INC.
       11.3K    13.3K rows  CVS HEALTH CORPORATION
       10.9K    12.9K rows  AT&T INC.
       10.7K    12.6K rows  VERIZON COMMUNICATIONS INC.
        8.3K     9.8K rows  EXXONMOBIL OIL CORPORATION
        7.0K     8.2K rows  WALMART INC.
        6.5K     7.7K rows  WALGREEN CO.
        6.4K     7.5K rows  DOLLAR GENERAL CORPORATION
        6.3K     7.4K rows  DOLLAR TREE, INC.
        6.2K     7.3K rows  Chevron U.S.A. Inc.
        5.7K     6.6K rows  7-Eleven, Inc.
        4.8K     5.6K rows  CIRCLE K STORES INC.
        4.6K     5.4K rows  SUNOCO LP
        3.5K     4.1K rows  Rite Aid Corporation
        3.2K     3.8K rows  SHELL USA, INC.
        3.1K     3.6K rows  PACIFIC GAS AND ELECTRIC COMPANY
        2.8K     3.3K rows  THE SHERWIN-WILLIAMS COMPANY
        2.7K     3.2K rows  NOBLE ENERGY, INC.
        2.7K     3.1K rows  AutoZone, Inc.
        2.5K     2.9K rows  HOME DEPOT U.S.A., INC.

PARENT_LEGAL_NAME by rows
     50.9K  CONSOLIDATED EDISON, INC.
     13.3K  CVS HEALTH CORPORATION
     12.9K  AT&T INC.
     12.6K  VERIZON COMMUNICATIONS INC.
      9.8K  EXXONMOBIL HOLDINGS CORPORATION
      8.2K  WALMART INC.
      7.7K  WALGREEN CO.
      7.5K  DOLLAR GENERAL CORPORATION
      7.4K  DOLLAR TREE, INC.
      7.3K  Chevron U.S.A. Inc.
      6.6K  7-Eleven, Inc.
      5.6K  CIRCLE K STORES INC.
      5.4K  ENERGY TRANSFER LP
      4.1K  Rite Aid Corporation
      4.0K  SHELL PLC
      3.6K  PG&E CORPORATION
      3.3K  THE SHERWIN-WILLIAMS COMPANY
      3.2K  NOBLE ENERGY, INC.
      3.1K  AutoZone, Inc.
      2.9K  HOME DEPOT U.S.A., INC.

PARENT_LEGAL_NAME by dollars
       43.3K    50.9K rows  CONSOLIDATED EDISON, INC.
       11.3K    13.3K rows  CVS HEALTH CORPORATION
       10.9K    12.9K rows  AT&T INC.
       10.7K    12.6K rows  VERIZON COMMUNICATIONS INC.
        8.4K     9.8K rows  EXXONMOBIL HOLDINGS CORPORATION
        7.0K     8.2K rows  WALMART INC.
        6.5K     7.7K rows  WALGREEN CO.
        6.4K     7.5K rows  DOLLAR GENERAL CORPORATION
        6.3K     7.4K rows  DOLLAR TREE, INC.
        6.2K     7.3K rows  Chevron U.S.A. Inc.
        5.7K     6.6K rows  7-Eleven, Inc.
        4.8K     5.6K rows  CIRCLE K STORES INC.
        4.6K     5.4K rows  ENERGY TRANSFER LP
        3.5K     4.1K rows  Rite Aid Corporation
        3.5K     4.0K rows  SHELL PLC
        3.1K     3.6K rows  PG&E CORPORATION
        2.8K     3.3K rows  THE SHERWIN-WILLIAMS COMPANY
        2.7K     3.2K rows  NOBLE ENERGY, INC.
        2.7K     3.1K rows  AutoZone, Inc.
        2.5K     2.9K rows  HOME DEPOT U.S.A., INC.

MATCHED_LEI by rows
     50.9K  54930033SBW53OO8T749
     13.3K  549300EJG376EN5NQE29
     12.9K  549300Z40J86GGSTL398
     12.6K  2S72QS2UO2OESLG6Y829
      9.8K  549300NCY2P2FLJT9D42
      8.2K  Y87794H0US1R65VBXU25
      7.7K  E1OI0SEUGJMPPTKRDD35
      7.5K  OPX52SQVOZI8IVSWYU66
      7.4K  549300PMSTQITB1WHR43
      7.3K  VA8TZDWPEZYU430RZ444
      6.6K  549300K23JPL0SS3LB18
      5.6K  549300TM4PEF0BWPGP66
      5.4K  54930001NJU8E40NQ561
      4.1K  529900W353T1JY1DKT44
      3.8K  549300UYFI41EIQ10304
      3.6K  1HNPXZSMMB7HMBMVBS46
      3.3K  Z15BMIOX8DDH0X2OBP21
      3.2K  02VFQXG2D1LR5ZH3K186
      3.1K  GA3JGKJ41LJKXDN23E90
      2.9K  549300FEMQDH6Q0NT330

MATCHED_LEI by dollars
       43.3K    50.9K rows  54930033SBW53OO8T749
       11.3K    13.3K rows  549300EJG376EN5NQE29
       10.9K    12.9K rows  549300Z40J86GGSTL398
       10.7K    12.6K rows  2S72QS2UO2OESLG6Y829
        8.3K     9.8K rows  549300NCY2P2FLJT9D42
        7.0K     8.2K rows  Y87794H0US1R65VBXU25
        6.5K     7.7K rows  E1OI0SEUGJMPPTKRDD35
        6.4K     7.5K rows  OPX52SQVOZI8IVSWYU66
        6.3K     7.4K rows  549300PMSTQITB1WHR43
        6.2K     7.3K rows  VA8TZDWPEZYU430RZ444
        5.7K     6.6K rows  549300K23JPL0SS3LB18
        4.8K     5.6K rows  549300TM4PEF0BWPGP66
        4.6K     5.4K rows  54930001NJU8E40NQ561
        3.5K     4.1K rows  529900W353T1JY1DKT44
        3.2K     3.8K rows  549300UYFI41EIQ10304
        3.1K     3.6K rows  1HNPXZSMMB7HMBMVBS46
        2.8K     3.3K rows  Z15BMIOX8DDH0X2OBP21
        2.7K     3.2K rows  02VFQXG2D1LR5ZH3K186
        2.7K     3.1K rows  GA3JGKJ41LJKXDN23E90
        2.5K     2.9K rows  549300FEMQDH6Q0NT330

## who x when

FACILITY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = MATCH_CONFIDENCE
  AMOCO OIL CO                              2026:623
  AT&T MOBILITY                             2026:504.90
  ATLANTIC CITY ELECTRIC CO                 2026:481.60
  CHEVRON USA INC                           2026:442
  CON EDISON                                2026:12.2K
  CSX TRANSPORTATION INC                    2026:419.05
  DOLLAR GENERAL                            2026:693.80
  EXXON MOBIL CORPORATION                   2026:411.40
  FAMILY DOLLAR STORES                      2026:334.05
  IDOT                                      2026:717
  LA DOTD                                   2026:640
  MI DEPT/NATURAL RESOURCES AND ENVIRONMEN  2026:624
  MI DEPT/STATE POLICE                      2026:844
  MI DEPT/TRANSPORTATION                    2026:1.4K
  MOBIL OIL CORP                            2026:348.50
  NEW CINGULAR WIRELESS PCS LLC             2026:855.10
  PACIFIC BELL                              2026:1.4K
  PENSKE TRUCK LEASING CO LP                2026:825
  RESIDENCE                                 2026:33.3K
  SHELL                                     2026:665
  SHELL OIL CO                              2026:625.60
  SHELL SERVICE STATION                     2026:966.45
  SHERWIN WILLIAMS CO                       2026:379.95
  SUNOCO SERVICE STATION                    2026:1.8K
  TEXAS DEPARTMENT OF TRANSPORTATION        2026:348
  UNION PACIFIC RAILROAD                    2026:419.05
  UNKNOWN                                   2026:10.3K
  VACANT HOUSE                              2026:710
  VACANT RESIDENCE                          2026:1.3K
  VERIZON WIRELESS                          2026:660.45

MATCHED_LEGAL_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = MATCH_CONFIDENCE
  7-Eleven, Inc.                            2026:5.7K
  AT&T INC.                                 2026:10.9K
  AutoZone, Inc.                            2026:2.7K
  CIRCLE K STORES INC.                      2026:4.8K
  CONSOLIDATED EDISON, INC.                 2026:43.3K
  CVS HEALTH CORPORATION                    2026:11.3K
  Chevron U.S.A. Inc.                       2026:6.2K
  DOLLAR GENERAL CORPORATION                2026:6.4K
  DOLLAR TREE, INC.                         2026:6.3K
  EXXONMOBIL OIL CORPORATION                2026:8.3K
  HOME DEPOT U.S.A., INC.                   2026:2.5K
  NOBLE ENERGY, INC.                        2026:2.7K
  PACIFIC GAS AND ELECTRIC COMPANY          2026:3.1K
  Rite Aid Corporation                      2026:3.5K
  SHELL USA, INC.                           2026:3.2K
  SUNOCO LP                                 2026:4.6K
  THE SHERWIN-WILLIAMS COMPANY              2026:2.8K
  VERIZON COMMUNICATIONS INC.               2026:10.7K
  WALGREEN CO.                              2026:6.5K
  WALMART INC.                              2026:7.0K

## what

MATCH_METHOD: brand 74%, exact 21%, fuzzy 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| EPA_REGISTRY_ID | id | 5.35M | 0 | 110038808010 5.1K; 110038807949 5.1K; 110038807226 5.1K; 110038785829 5.1K |
| FACILITY_NAME | who | 4.42M | 7.2K | RESIDENCE 45.9K; CON EDISON 15.5K; HELENA CHEMICAL CO 9.2K; PIONEER CONCRETE OF TEXAS 5.1K |
| MATCHED_LEI | who | 22.8K | 5.02M | 54930033SBW53OO8T749 50.9K; 549300EJG376EN5NQE29 13.3K; 549300Z40J86GGSTL398 12.9K; 2S72QS2UO2OESLG6Y829 12.5K |
| MATCHED_LEGAL_NAME | who | 22.7K | 5.02M | CONSOLIDATED EDISON, INC. 50.9K; CVS HEALTH CORPORATION 13.3K; AT&T INC. 12.9K; VERIZON COMMUNICATIONS IN 12.5K |
| MATCH_METHOD | category | 3 | 5.02M | brand 205.7K; exact 59.1K; fuzzy 14.8K |
| MATCH_CONFIDENCE | amount | 3 | 5.02M | 0.85 209.7K; 1.00 59.1K; 0.80 10.8K |
| ULTIMATE_PARENT_LEI | who | 1.2K | 5.26M | J3WHBG0MTS7O8ZVMDC91 9.8K; MTLVN9N7JE8MIBIJ1H73 5.4K; 21380068P1DRHMJ8KU70 4.0K; 8YQ2GSDWYZXO2EDN3511 3.6K |
| PARENT_LEGAL_NAME | who | 22.0K | 5.02M | CONSOLIDATED EDISON, INC. 50.9K; CVS HEALTH CORPORATION 13.3K; AT&T INC. 12.9K; VERIZON COMMUNICATIONS IN 12.5K |
| PARENT_CIK | other | 705 | 5.18M | 1047862 50.9K; 732717 12.9K; 732712 12.6K; 104169 8.2K |
| PARENT_UEI | other | 31.0K | 5.26M | C1VZZJXDJQS6 116; C653LL6T6267 112; C795SEMN4AF4 98; C6APNVPPJPL9 76 |
| REVIEW_FLAG | other | 1 | 3.82M | false 1.48M |
| _INGESTED_AT | audit date | 1 | 0 | 2026-07-28 18:42:38.554 5.30M |
| _SOURCE_RUN_ID | audit | 3 | 0 | xc-build-v1 3.90M; xc-v2-rb 1.20M; xc-v2-cur 205.7K |
