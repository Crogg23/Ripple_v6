# FED_SEC_EDGAR_INSIDERS

rows 69.3K  columns 17  scan 4.2s

roles: audit 2, category 6, date 3, id 1, other 2, who 3

## when

FILING_DATE
  2026     69.3K  ##############################

PERIOD_OF_REPORT
  2002         1  
  2006         1  
  2008         1  
  2013         2  
  2014         2  
  2015         1  
  2016         5  
  2017         2  
  2018         2  
  2019         3  
  2020        11  
  2021        20  
  2022        29  
  2023        49  
  2024       134  
  2025      4.3K  ##
  2026     64.7K  ##############################

DATE_OF_ORIG_SUB
  2020         1  
  2022         4  
  2023         5  
  2024        21  #
  2025       255  #########
  2026       876  ##############################

## who

ISSUERNAME by rows
       104  LEGGETT & PLATT INC
       104  CHURCH & DWIGHT CO INC /DE/
        99  PPG INDUSTRIES INC
        96  ENTERGY CORP /DE/
        95  Accenture plc
        92  REPUBLIC SERVICES, INC.
        92  ASSOCIATED BANC-CORP
        92  HUNTINGTON BANCSHARES INC /MD/
        87  PACCAR INC
        85  VERIZON COMMUNICATIONS INC
        79  Texas Pacific Land Corp
        78  JPMORGAN CHASE & CO
        77  UMB FINANCIAL CORP
        76  Walmart Inc.
        75  LABCORP HOLDINGS INC.
        72  AT&T INC.
        72  CoreWeave, Inc.
        71  ALEXANDRIA REAL ESTATE EQUITIES, INC.
        71  MCCORMICK & CO INC
        71  UNITED BANKSHARES INC/WV

REMARKS by rows
      1.4K  Exhibit 24 - Power of Attorney
       365  Exhibit List: Exhibit 24 - Power of Attorney
       230  Exhibit 24.1 - Power of Attorney
       190  Exhibit 24 - Power of Attorney.
       153  Exhibit List - Exhibit 24 - Power of Attorney
       139  Exhibit List - Exhibit 24.1 - Power of Attorney
        91  See Exhibit 24.1 - Power of Attorney
        64  Exhibit 24 Power of Attorney
        61  [Exhibit 24 - Power of Attorney.]
        61  No securities are beneficially owned.
        59  This Form 3 is being filed to report the Reporting Persons beneficial 
        54  Power of Attorney on file
        50  Exhibit 24: Power of Attorney
        47  Ex. 24 - Power of Attorney
        47  castropoa.txt
        45  Exhibit List: Exhibit 24 - Power of Attorney.
        42  Power of Attorney on file.
        42  Exhibit 24
        37  Due to the issuer's status as a foreign private issuer pursuant to Rul
        35  Exhibit List: Exhibit 24 - Power of Attorney. Pacific Investment Manag

_SRC_SHA256 by rows
     69.3K  5585f53093397a5baa6c662e66b7c39f9761a0261a40d238b323119ce62a19e4

## who x when

ISSUERNAME by PERIOD_OF_REPORT
  ALEXANDRIA REAL ESTATE EQUITIES, INC.     2025:7 2026:64
  ASSOCIATED BANC-CORP                      2026:92
  AT&T INC.                                 2025:5 2026:67
  Accenture plc                             2026:95
  CHURCH & DWIGHT CO INC /DE/               2025:20 2026:84
  CoreWeave, Inc.                           2025:3 2026:69
  ENTERGY CORP /DE/                         2026:96
  HUNTINGTON BANCSHARES INC /MD/            2025:1 2026:91
  JPMORGAN CHASE & CO                       2025:4 2026:74
  LABCORP HOLDINGS INC.                     2026:75
  LEGGETT & PLATT INC                       2026:104
  MCCORMICK & CO INC                        2025:2 2026:69
  PACCAR INC                                2026:87
  PPG INDUSTRIES INC                        2025:9 2026:90
  REPUBLIC SERVICES, INC.                   2024:1 2025:1 2026:90
  Texas Pacific Land Corp                   2025:1 2026:78
  UMB FINANCIAL CORP                        2025:12 2026:65
  UNITED BANKSHARES INC/WV                  2025:13 2026:58
  VERIZON COMMUNICATIONS INC                2025:9 2026:76
  Walmart Inc.                              2025:10 2026:66

REMARKS by PERIOD_OF_REPORT
  Due to the issuer's status as a foreign   2026:37
  Ex. 24 - Power of Attorney                2026:47
  Exhibit 24                                2026:42
  Exhibit 24 - Power of Attorney            2021:3 2022:1 2023:1 2024:2 2025:35 2026:1.4K
  Exhibit 24 - Power of Attorney.           2024:1 2025:1 2026:188
  Exhibit 24 Power of Attorney              2026:64
  Exhibit 24.1 - Power of Attorney          2025:1 2026:229
  Exhibit 24: Power of Attorney             2025:1 2026:49
  Exhibit List - Exhibit 24 - Power of Att  2026:153
  Exhibit List - Exhibit 24.1 - Power of A  2026:139
  Exhibit List: Exhibit 24 - Power of Atto  2022:1 2025:10 2026:354
  Exhibit List: Exhibit 24 - Power of Atto  2026:45
  Exhibit List: Exhibit 24 - Power of Atto  2026:35
  No securities are beneficially owned.     2014:2 2017:1 2020:1 2021:1 2023:1 2024:1 2025:4 2026:50
  Power of Attorney on file                 2026:54
  Power of Attorney on file.                2026:42
  See Exhibit 24.1 - Power of Attorney      2025:5 2026:86
  This Form 3 is being filed to report the  2026:59
  [Exhibit 24 - Power of Attorney.]         2026:61
  castropoa.txt                             2025:47

## what

NO_SECURITIES_OWNED: 0 67%, 1 33%

NOT_SUBJECT_SEC16: 0 90%, false 7%, 1 2%, true 1%

FORM3_HOLDINGS_REPORTED: 0 99%, 1 1%

FORM4_TRANS_REPORTED: 0 86%, 1 14%

DOCUMENT_TYPE: 4 82%, 3 15%, 5 1%, 4/A 1%, 3/A 0%, 5/A 0%

AFF10B5ONE: 0 72%, false 20%, 1 6%, true 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ACCESSION_NUMBER | id | 70.7K | 0 | 0001598318-26-000001 347; 0000897069-26-000200 347; 0000874015-26-000096 347; 0000912282-26-000228 347 |
| FILING_DATE | date | 61 | 0 | 18-MAR-2026 5.0K; 03-MAR-2026 3.4K; 05-JAN-2026 3.0K; 17-MAR-2026 2.3K |
| PERIOD_OF_REPORT | date | 487 | 0 | 18-MAR-2026 5.7K; 31-DEC-2025 2.8K; 02-JAN-2026 2.3K; 02-MAR-2026 2.1K |
| DATE_OF_ORIG_SUB | date | 205 | 68.1K | 18-MAR-2026 54; 03-MAR-2026 52; 05-FEB-2026 43; 05-JAN-2026 41 |
| NO_SECURITIES_OWNED | category | 3 | 58.7K | 0 7.0K; 1 3.5K |
| NOT_SUBJECT_SEC16 | category | 5 | 35.9K | 0 29.9K; false 2.5K; 1 691; true 274 |
| FORM3_HOLDINGS_REPORTED | category | 3 | 68.3K | 0 976; 1 9 |
| FORM4_TRANS_REPORTED | category | 3 | 68.3K | 0 845; 1 140 |
| DOCUMENT_TYPE | category | 6 | 0 | 4 56.9K; 3 10.3K; 5 972; 4/A 904 |
| CIK | other | 5.3K | 0 | 0000101382 362; 0000097476 362; 0001563411 360; 0000800457 360 |
| ISSUERNAME | who | 5.4K | 0 | UMB FINANCIAL CORP 362; TEXAS INSTRUMENTS INC 362; CONSTELLIUM SE 360; DONEGAL GROUP INC 360 |
| ISSUERTRADINGSYMBOL | other | 5.2K | 604 | UMBF 361; TXN 361; N/A 361; CSTM 359 |
| REMARKS | who | 2.7K | 60.3K | Exhibit 24 - Power of Att 1.4K; Exhibit List: Exhibit 24  365; Exhibit 24.1 - Power of A 230; Exhibit 24 - Power of Att 190 |
| AFF10B5ONE | category | 5 | 10.5K | 0 42.4K; false 11.5K; 1 3.6K; true 1.2K |
| _INGESTED_AT | audit | 1 | 0 | 1784823224267987 69.3K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 28056e24-35e1-4fe3-94e8-d 69.3K |
| _SRC_SHA256 | who | 1 | 0 | 5585f53093397a5baa6c662e6 69.3K |
