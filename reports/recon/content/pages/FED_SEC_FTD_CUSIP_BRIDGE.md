# FED_SEC_FTD_CUSIP_BRIDGE

rows 128.3K  columns 10  scan 3.9s

roles: amount 1, audit 2, category 1, date 1, other 3, who 2

## when

SETTLEMENT_DATE
  2026    128.3K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PRICE | 128.3K | 0 | 24.79 | 338.06 | 12.6K | 5.32M |

## who

CUSIP by rows
        22  022865869
        22  097751861
        22  21874J586
        22  48132A107
        22  55286W504
        22  33738D770
        22  38747T518
        22  063679559
        22  00972D105
        22  09661T784
        22  74350U740
        22  30243C107
        22  71989C208
        22  45782C284
        22  136945102
        22  G9503X103
        22  45782C730
        22  518416870
        22  52110K608
        22  02072L185

CUSIP by dollars
       87.3K        7 rows  842243107
       23.6K       12 rows  21037X100
       23.4K        2 rows  50187G104
       22.0K       11 rows  08986R408
       21.8K       13 rows  80004C200
       19.9K       11 rows  58733R102
       18.9K        2 rows  308243104
       14.8K       16 rows  595112103
       14.2K       19 rows  78462F103
       14.1K        8 rows  N07059210
       12.8K        2 rows  62944T105
       12.7K       18 rows  46090E103
       11.1K       15 rows  55024U109
       10.6K        9 rows  384637104
       10.6K       10 rows  38141G104
       10.5K       18 rows  92189F676
       10.4K       10 rows  N07045102
       10.3K       11 rows  22160K105
       10.2K        8 rows  893641100
       10.0K        6 rows  303901102

DESCRIPTION by rows
      1.3K  THEMES ETF TR LEVERAGE SHS 2X 
      1.1K  TIDAL TR II DEFIANCE DAILY TAR
       850  INVESTMENT MANAGERS SER TR II 
       518  INVESCO EXCHANGE-TRADED FD TR 
       480  DIREXION SHS ETF TR DIREXION D
       468  ETF OPPORTUNITIES TR T-REX 2X 
       427  ISHARES TR
       419  PGIM ROCK ETF TR PGIM S&P 500 
       345  AMERICAN CENTY ETF TR AVANTIS 
       338  J P MORGAN EXCHANGE-TRADED FD 
       314  GRANITESHARES ETF TR GRANITESH
       285  FIRST TR EXCHANGE-TRADED FD VI
       268  T ROWE PRICE EXCHANGE-TRADED F
       267  BANK MONTREAL QUE MICROSECTORS
       234  THEMES ETF TR LEVERAGE SHARES 
       231  AIM ETF PRODS TR ALLIANZIM U.S
       220  FRANKLIN TEMPLETON ETF TR
       216  SPDR SER TR STATE STREET SPDR 
       211  SELECT SECTOR SPDR TR STATE ST
       202  SSGA ACTIVE TRUST STATE STREET

DESCRIPTION by dollars
       87.3K        7 rows  SOUTHERN BANCSHARES N C INC CO
       43.5K      518 rows  INVESCO EXCHANGE-TRADED FD TR 
       40.8K      427 rows  ISHARES TR
       32.1K      480 rows  DIREXION SHS ETF TR DIREXION D
       31.6K      216 rows  SPDR SER TR STATE STREET SPDR 
       27.1K      345 rows  AMERICAN CENTY ETF TR AVANTIS 
       24.9K      850 rows  INVESTMENT MANAGERS SER TR II 
       23.6K       12 rows  CONSTELLATION SOFTWARE INC COM
       23.4K        2 rows  LICT Corporation Common Stock 
       22.0K       11 rows  BIGLARI HLDGS INC CL A
       21.8K       13 rows  SANDISK CORP COM
       21.3K      338 rows  J P MORGAN EXCHANGE-TRADED FD 
       19.9K       11 rows  MERCADOLIBRE INC COM STK (DE) 
       19.2K     1.1K rows  TIDAL TR II DEFIANCE DAILY TAR
       18.9K        2 rows  FARMERS & MERCH BK LONG/BCH CA
       17.0K     1.3K rows  THEMES ETF TR LEVERAGE SHS 2X 
       14.8K       16 rows  MICRON TECHNOLOGY INC
       14.6K      194 rows  VANGUARD WELLESLEY INCOME FD T
       14.2K       19 rows  STATE STREET SPDR S&P 500 ETF 
       14.1K        8 rows  ASML HOLDING NV NY REG SHS NEW

## who x when

CUSIP by SETTLEMENT_DATE, dollars = PRICE
  00972D105                                 2026:28.84
  02072L185                                 2026:771.14
  022865869                                 2026:570.78
  063679559                                 2026:754.04
  08986R408                                 2026:22.0K
  09661T784                                 2026:547.10
  097751861                                 2026:5.3K
  136945102                                 2026:208.13
  21037X100                                 2026:23.6K
  21874J586                                 2026:572.18
  30243C107                                 2026:1.0K
  308243104                                 2026:18.9K
  33738D770                                 2026:452.81
  38747T518                                 2026:533.18
  45782C284                                 2026:741.56
  45782C730                                 2026:847.60
  48132A107                                 2026:87.78
  50187G104                                 2026:23.4K
  518416870                                 2026:1.6K
  52110K608                                 2026:611.76
  55286W504                                 2026:640.82
  58733R102                                 2026:19.9K
  595112103                                 2026:14.8K
  71989C208                                 2026:109.69
  74350U740                                 2026:346.86
  78462F103                                 2026:14.2K
  80004C200                                 2026:21.8K
  842243107                                 2026:87.3K
  G9503X103                                 2026:37.71
  N07059210                                 2026:14.1K

DESCRIPTION by SETTLEMENT_DATE, dollars = PRICE
  AIM ETF PRODS TR ALLIANZIM U.S            2026:8.9K
  AMERICAN CENTY ETF TR AVANTIS             2026:27.1K
  BANK MONTREAL QUE MICROSECTORS            2026:10.3K
  BIGLARI HLDGS INC CL A                    2026:22.0K
  CONSTELLATION SOFTWARE INC COM            2026:23.6K
  DIREXION SHS ETF TR DIREXION D            2026:32.1K
  ETF OPPORTUNITIES TR T-REX 2X             2026:5.4K
  FARMERS & MERCH BK LONG/BCH CA            2026:18.9K
  FIRST TR EXCHANGE-TRADED FD VI            2026:8.3K
  FRANKLIN TEMPLETON ETF TR                 2026:8.7K
  GRANITESHARES ETF TR GRANITESH            2026:6.1K
  INVESCO EXCHANGE-TRADED FD TR             2026:43.5K
  INVESTMENT MANAGERS SER TR II             2026:24.9K
  ISHARES TR                                2026:40.8K
  J P MORGAN EXCHANGE-TRADED FD             2026:21.3K
  LICT Corporation Common Stock             2026:23.4K
  MERCADOLIBRE INC COM STK (DE)             2026:19.9K
  MICRON TECHNOLOGY INC                     2026:14.8K
  PGIM ROCK ETF TR PGIM S&P 500             2026:12.7K
  SANDISK CORP COM                          2026:21.8K
  SELECT SECTOR SPDR TR STATE ST            2026:11.9K
  SOUTHERN BANCSHARES N C INC CO            2026:87.3K
  SPDR SER TR STATE STREET SPDR             2026:31.6K
  SSGA ACTIVE TRUST STATE STREET            2026:5.0K
  STATE STREET SPDR S&P 500 ETF             2026:14.2K
  T ROWE PRICE EXCHANGE-TRADED F            2026:11.5K
  THEMES ETF TR LEVERAGE SHARES             2026:3.6K
  THEMES ETF TR LEVERAGE SHS 2X             2026:17.0K
  TIDAL TR II DEFIANCE DAILY TAR            2026:19.2K
  VANGUARD WELLESLEY INCOME FD T            2026:14.6K

## what

SRC_FILE: cnsfails202607b.zip 57%, cnsfails202607a.zip 43%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| SETTLEMENT_DATE | date | 22 | 0 | 20260701 7.1K; 20260702 6.5K; 20260717 6.4K; 20260707 6.3K |
| CUSIP | who | 14.8K | 0 | 989817101 642; 98980W206 642; 98980F104 642; 98980A105 642 |
| SYMBOL | other | 14.7K | 36 | ZUMZ 642; ZSPC 642; GTM 642; ZTO 642 |
| QUANTITY_FAILS | other | 29.8K | 0 | 1 3.7K; 2 1.8K; 3 1.2K; 4 901 |
| DESCRIPTION | who | 12.8K | 0 | THEMES ETF TR LEVERAGE SH 1.3K; TIDAL TR II DEFIANCE DAIL 1.1K; INVESTMENT MANAGERS SER T 862; T ROWE PRICE EXCHANGE-TRA 646 |
| PRICE | amount | 16.8K | 0 | . 737; 0.16 642; 37.77 642; 0.48 642 |
| SRC_FILE | category | 2 | 0 | cnsfails202607b.zip 73.3K; cnsfails202607a.zip 55.0K |
| INGESTED_AT | audit | 1 | 0 | 1787843067815237 128.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 97c4f3b2-9b00-434b-b262-7 128.3K |
| SRC_SHA256 | other | 1 | 0 | 1c0f6231355756aca254813f7 128.3K |
