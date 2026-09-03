# FED_SEC_MONEY_MARKET_FUND_INFORMATION

rows 1.2K  columns 14  scan 2.8s

roles: audit 2, category 2, date 1, other 4, who 5

## when

REPORTMONTH
  2026      1.2K  ##############################

## who

CLASS_NAME by rows
        56  Institutional Class
        32  Class A
        31  Institutional Shares
        26  Class I
        25  Service Shares
        23  Select Class
        22  Investor Shares
        21  Premium Class
        18  Investor Class
        16  Class II
        16  Class III
        14  Capital Shares
        14  Class C
        12  Class A Shares
        12  Class Y
        12  Premier
        11  Cash Management Class
        11  Agency
        11  Service Class
        10  Morgan

SERIES_NAME by rows
        33  GOVERNMENT PORTFOLIO
        32  TREASURY PORTFOLIO
        27  MONEY MARKET PORTFOLIO
        23  AMERICAN FUNDS U.S. GOVERNMENT MONEY MARKET FUND
        21  FIDELITY GOVERNMENT MONEY MARKET FUND
        21  TAX-EXEMPT PORTFOLIO
        18  TREASURY ONLY PORTFOLIO
        16  GOLDMAN SACHS FINANCIAL SQUARE GOVERNMENT FUND
        15  FEDFUND
        14  GOVERNMENT MONEY MARKET PORTFOLIO
        13  TREASURY SECURITIES PORTFOLIO
        13  STATE STREET INSTITUTIONAL U.S. GOVERNMENT MONEY MARKET FUND
        12  PUTNAM GOVERNMENT MONEY MARKET FUND
        12  GOLDMAN SACHS FINANCIAL SQUARE TREASURY INSTRUMENTS FUND
        12  INVESCO GOVERNMENT MONEY MARKET FUND
        12  FIDELITY TAX-EXEMPT MONEY MARKET FUND
        12  JPMORGAN U.S. GOVERNMENT MONEY MARKET FUND
        12  FIDELITY TREASURY MONEY MARKET FUND
        11  FEDERATED HERMES GOVERNMENT OBLIGATIONS FUND
        10  STATE STREET INSTITUTIONAL TREASURY PLUS MONEY MARKET FUND

REGISTRANT by rows
        77  GOLDMAN SACHS TRUST
        73  MORGAN STANLEY INSTITUTIONAL LIQUIDITY FUNDS
        72  FEDERATED HERMES MONEY MARKET OBLIGATIONS TRUST
        44  BLACKROCK LIQUIDITY FUNDS
        42  STATE STREET INSTITUTIONAL INVESTMENT TRUST
        39  FIRST AMERICAN FUNDS TRUST
        38  JPMORGAN TRUST I
        34  JPMORGAN TRUST II
        25  ALLSPRING FUNDS TRUST
        24  SHORT TERM INVESTMENTS TRUST
        23  AMERICAN FUNDS U.S. GOVERNMENT MONEY MARKET FUND
        21  FIDELITY GOVERNMENT MONEY MARKET FUND
        18  FIDELITY INVESTMENTS MONEY MARKET TREASURY PORTFOLIO
        18  LEGG MASON PARTNERS INSTITUTIONAL TRUST
        18  CHARLES SCHWAB FAMILY OF FUNDS
        18  FIDELITY INVESTMENTS MONEY MARKET TREASURY ONLY PORTFOLIO
        17  INVESCO INVESTMENT SECURITIES FUNDS
        17  NORTHERN INSTITUTIONAL FUNDS
        15  FIDELITY INVESTMENTS MONEY MARKET MONEY MARKET PORTFOLIO
        15  FIDELITY INVESTMENTS MONEY MARKET GOVERNMENT PORTFOLIO

INVESTMENT_ADVISOR by rows
       219  Fidelity Management &amp; Research Company LLC
        79  Goldman Sachs Asset Management, L.P.
        78  J.P. Morgan Investment Management Inc.
        75  Morgan Stanley Investment Management, Inc.
        73  Federated Investment Management Company
        59  BlackRock Advisors, LLC
        53  Invesco Advisers, Inc.
        47  SSGA Funds Management, Inc.
        39  BNY Mellon Investment Adviser, Inc.
        39  U.S. Bancorp Asset Management, Inc.
        25  Allspring Funds Management, LLC
        24  Capital Research and Management Company
        23  Franklin Templeton Fund Adviser LLC
        22  Franklin Advisors, Inc.
        20  Northern Trust Investments, Inc.
        20  DWS Investment Management Americas, Inc.
        20  UBS ASSET MANAGEMENT (AMERICAS) LLC
        20  Charles Schwab Investment Management, Inc.
        12  HSBC Global Asset Management (USA) Inc.
        12  T. Rowe Price Associates, Inc.

## who x when

CLASS_NAME by REPORTMONTH
  Agency                                    2026:11
  Capital Shares                            2026:14
  Cash Management Class                     2026:11
  Class A                                   2026:32
  Class A Shares                            2026:12
  Class C                                   2026:14
  Class I                                   2026:26
  Class II                                  2026:16
  Class III                                 2026:16
  Class Y                                   2026:12
  Institutional Class                       2026:56
  Institutional Shares                      2026:31
  Investor Class                            2026:18
  Investor Shares                           2026:22
  Morgan                                    2026:10
  Premier                                   2026:12
  Premium Class                             2026:21
  Select Class                              2026:23
  Service Class                             2026:11
  Service Shares                            2026:25

SERIES_NAME by REPORTMONTH
  AMERICAN FUNDS U.S. GOVERNMENT MONEY MAR  2026:23
  FEDERATED HERMES GOVERNMENT OBLIGATIONS   2026:11
  FEDFUND                                   2026:15
  FIDELITY GOVERNMENT MONEY MARKET FUND     2026:21
  FIDELITY TAX-EXEMPT MONEY MARKET FUND     2026:12
  FIDELITY TREASURY MONEY MARKET FUND       2026:12
  GOLDMAN SACHS FINANCIAL SQUARE GOVERNMEN  2026:16
  GOLDMAN SACHS FINANCIAL SQUARE TREASURY   2026:12
  GOVERNMENT MONEY MARKET PORTFOLIO         2026:14
  GOVERNMENT PORTFOLIO                      2026:33
  INVESCO GOVERNMENT MONEY MARKET FUND      2026:12
  JPMORGAN U.S. GOVERNMENT MONEY MARKET FU  2026:12
  MONEY MARKET PORTFOLIO                    2026:27
  PUTNAM GOVERNMENT MONEY MARKET FUND       2026:12
  STATE STREET INSTITUTIONAL TREASURY PLUS  2026:10
  STATE STREET INSTITUTIONAL U.S. GOVERNME  2026:13
  TAX-EXEMPT PORTFOLIO                      2026:21
  TREASURY ONLY PORTFOLIO                   2026:18
  TREASURY PORTFOLIO                        2026:32
  TREASURY SECURITIES PORTFOLIO             2026:13

## what

SERIES_CATEGORY: Government 72%, Prime 13%, Other Tax Exempt 8%, Single State 6%

SUB_ADVISOR: FMR Investment Management (UK) 21%, Fidelity Management &amp; Rese 21%, Fidelity Management &amp; Rese 21%, Allspring Global Investments,  7%, Western Asset Management Compa 7%, Voya Investment Management Co. 4%, BlackRock International Limite 4%, Putnam Investment Management,  3%, Franklin Templeton Investment  3%, Wilmington Trust Investment Ad 3%, PGIM, Inc. 3%, BlackRock Investment Managemen 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REPORTMONTH | date | 1 | 0 | 2026-04-30 1.2K |
| REGISTRANT_CIK | other | 175 | 0 | 0000356173 78; 0000822977 77; 0001227155 73; 0000856517 72 |
| REGISTRANT | who | 187 | 0 | GOLDMAN SACHS TRUST 77; MORGAN STANLEY INSTITUTIO 73; FEDERATED HERMES MONEY MA 72; BLACKROCK LIQUIDITY FUNDS 44 |
| SERIES_NAME | who | 303 | 0 | GOVERNMENT PORTFOLIO 33; TREASURY PORTFOLIO 32; MONEY MARKET PORTFOLIO 27; AMERICAN FUNDS U.S. GOVER 24 |
| SERIES_ID | other | 322 | 0 | S000025394 24; S000007051 21; S000004819 18; S000004818 18 |
| SERIES_CATEGORY | category | 4 | 0 | Government 869; Prime 160; Other Tax Exempt 102; Single State 75 |
| CLASS_NAME | who | 415 | 0 | Institutional Class 56; Class A 32; Institutional Shares 31; Class I 26 |
| CLASS_ID | other | 1.0K | 0 | C000261149 8; C000255665 8; C000195869 8; C000177594 8 |
| INVESTMENT_ADVISOR | who | 88 | 0 | Fidelity Management &amp; 219; Goldman Sachs Asset Manag 79; J.P. Morgan Investment Ma 78; Morgan Stanley Investment 75 |
| CLASS_TICKER_SYMBOL | other | 846 | 210 | FYOXX 7; FYHXX 7; FMQXX 7; FLGXX 7 |
| SUB_ADVISOR | category | 25 | 812 | FMR Investment Management 73; Fidelity Management &amp; 73; Fidelity Management &amp; 73; Allspring Global Investme 25 |
| _INGESTED_AT | audit | 1 | 0 | 1785096119721890 1.2K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 598adf30-9e90-4709-8134-3 1.2K |
| _SRC_SHA256 | who | 1 | 0 | cd9dbe7bfe19f246cbe6b0d68 1.2K |
