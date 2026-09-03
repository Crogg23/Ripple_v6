# FED_FATCA_FFI

rows 516.3K  columns 6  scan 2.6s

roles: audit 2, id 1, other 1, who 2

## who

FI_NAME by rows
        43  BNP PARIBAS - Branch
        35  Deutsche Bank Aktiengesellschaft - Branch
        34  Citibank NA - Branch
        32  Officine Maccaferri Spa - Branch
        30  Bank of China Limited - Branch
        24  Industrial and Commercial Bank of China Limited - Branch
        24  ING Bank N.V. - Branch
        23  Standard Chartered Bank - Branch
        22  Societe Generale - Branch
        22  STATE BANK OF INDIA - Branch
        22  Barclays Bank plc - Branch
        21  Citibank Europe plc - Branch
        18  CREDIT AGRICOLE CORPORATE AND INVESTMENT BANK - Branch
        18  China Construction Bank Corporation - Branch
        17  Sumitomo Mitsui Banking Corporation - Branch
        17  MUFG Bank, Ltd. - Branch
        17  UBS AG - Branch
        17  Australia and New Zealand Banking Group Limited - Branch
        17  Mizuho Bank, Ltd. - Branch
        16  Finance in Motion GmbH - Branch

COUNTRY_NAME by rows
    103.0K  CAYMAN ISLANDS
     52.4K  BRAZIL
     41.0K  UNITED KINGDOM
     29.0K  LUXEMBOURG
     28.0K  JAPAN
     19.7K  CANADA
     18.3K  VIRGIN ISLANDS (BRITISH)
     12.5K  GUERNSEY
     11.2K  AUSTRALIA
     11.2K  IRELAND
     10.9K  SINGAPORE
     10.9K  JERSEY
      9.9K  HONG KONG
      9.2K  FRANCE
      9.0K  NETHERLANDS
      8.6K  NEW ZEALAND
      7.5K  THAILAND
      7.2K  MAURITIUS
      7.1K  SWITZERLAND
      6.2K  INDIA

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GIIN | id | 512.7K | 0 | CAVRDW.00016.ME.702 1.6K; 5XQ6X0.00000.SP.044 1.6K; E64C5U.00001.ME.044 1.6K; M5HYPT.99999.SL.044 1.6K |
| FI_NAME | who | 499.8K | 0 | M2 GLOBAL WEALTH LIMITED 1.6K; ILP II VENTURES XIV PTE.  1.6K; Baraterre Limited 1.6K; Burhou Limited 1.6K |
| COUNTRY_NAME | who | 244 | 0 | CAYMAN ISLANDS 103.0K; BRAZIL 52.4K; UNITED KINGDOM 41.0K; LUXEMBOURG 29.0K |
| INGESTED_AT | audit | 1 | 0 | 1785965090345862 516.3K |
| SOURCE_RUN_ID | audit | 1 | 0 | 2b11fe9d-b185-43c1-a7f0-f 516.3K |
| SRC_SHA256 | other | 1 | 0 | 3ea9619aa91c331d6463a2084 516.3K |
