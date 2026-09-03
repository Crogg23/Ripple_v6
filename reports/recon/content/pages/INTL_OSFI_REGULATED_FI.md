# INTL_OSFI_REGULATED_FI

rows 343  columns 16  scan 2.4s

roles: audit 2, category 5, other 3, who 6

## who

COMPANY_NAME by rows
         2  Natixis
         2  Swiss Reinsurance Company Ltd
         1  Agricultural Bank of China Limited
         1  Bank of Communications Co., Ltd.
         1  Central 1 Trust Company
         1  Green Shield Canada
         1  American Agricultural Insurance Company
         1  BMO Mortgage Corp.
         1  Bridgewater Bank
         1  Canadian Imperial Bank of Commerce
         1  Chicago Title Insurance Company
         1  Equitable Bank
         1  Canada Guaranty Mortgage Insurance Company
         1  Investors Group Trust Co. Ltd.
         1  Canada Trust Company (The)
         1  Chubb Life Insurance Company of Canada
         1  FCT Insurance Company Ltd.
         1  AWP Health & Life SA
         1  Hannover Re (Ireland) Designated Activity Company
         1  Canadian Tire Bank

REPRESENTATIVE_NAME by rows
        10  Laurie  LaPalme
         7  Colleen Anne Sexsmith
         6  James V.  Russell
         5  Louis  Gagnon
         5  London  Bradley
         4  Stuart  McAlister
         4  NAVINDER  DHILLON
         4  Gordon P. Goodman
         4  Thierry  Langevin
         4  Silvy  Wright
         3  Gordon  Goodman
         3  Marie-Soleil  Lemieux
         3  Colleen  Sexsmith
         3  Rowan B. Saunders
         3  Valérie  Lavoie
         3  Scott  Wood
         3  Rob  Wesseling
         2  Matthew  Cox
         2  David  Rawlings
         2  Philip James Witherington

CANADIAN_TRADE_COMPANY_NAME by rows
         1  SCOR Insurance – Canadian Branch
         1  Continental Casualty Company
         1  Protective Insurance Company
         1  XL Specialty Insurance Company
         1  Swiss Reinsurance Company Ltd (Life Branch)
         1  Combined Insurance Company of America
         1  Crédit Agricole Corporate and Investment Bank (Canada Branch)
         1  Lloyd's Underwriters
         1  Factory Mutual Insurance Company
         1  N.V. Hagelunie
         1  Europ Assistance S.A.
         1  China Construction Bank Toronto Branch
         1  Fifth Third Bank,  National Association
         1  Hannover Rück SE
         1  Ecclesiastical Insurance Office Public Limited Company
         1  Atradius Crédito y Caución S.A. de Seguros y Reaseguros
         1  Connecticut General Life Insurance Company
         1  Toa Reinsurance Company of America (The)
         1  HDI Global SE Canada Branch
         1  Life Insurance Company of North America

ADDRESS_LINE_2 by rows
         8  SUITE 400
         7  SUITE 600
         6  SUITE 2200
         6  SUITE 500
         6  ROYAL BANK PLAZA, SOUTH TOWER
         6  SUITE 100
         5  SUITE 1400
         5  SUITE 200
         4  40 TEMPERANCE ST
         4  CIBC SQUARE
         4  SUITE 2500
         3  P.O. BOX 2000
         3  390 BAY ST
         3  SUITE 300
         3  SUITE 1100
         3  5TH FLOOR WEST
         3  50 CRÉMAZIE PL
         3  Suite 1500-A
         3  12th Floor
         3  9TH FLOOR

## what

FI_TYPE_NAME: Federally Regulated Financial  96%, Foreign Bank Representative Of 4%

FI_GROUP_NAME: Property & Casualty Insurance  39%, Banks 22%, Life Insurance Companies 16%, Trust Companies 12%, Foreign Bank Representative Of 4%, Loan Companies 3%, Fraternal Benefit Societies 2%

FI_INDUSTRY_NAME: Foreign Property & Casualty In 21%, Canadian Property & Casualty I 18%, Trust Companies 12%, Domestic Banks 10%, Canadian Life Insurance Compan 10%, Foreign Bank Branches - Full S 8%, Foreign Life Insurance Compani 6%, Foreign Banks 4%, Foreign Bank Representative Of 4%, Loan Companies 4%, Canadian Fraternal Benefit Soc 2%, Canadian Mortgage Insurers 1%

TITLE: Chief Executive Officer 41%, Chief Agent 26%, President and Chief Executive  10%, President & Chief Executive Of 6%, Principal Officer 5%, Chief Representative 4%, President & CEO 3%, President and CEO 2%, CEO, Canada 1%, Chief Agent for Canada 1%, Branch Management - CEO & Chie 1%, General Manager 1%

PROVINCE_STATE: Ontario 78%, Quebec 9%, British Columbia 4%, Alberta 3%, Manitoba 2%, Saskatchewan 2%, Nova Scotia 1%, New Brunswick 1%, Newfoundland and Labrador 0%, Kansas 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COMPANY_NAME | who | 340 | 0 | Swiss Reinsurance Company 3; Natixis 3; ivari 2; Zurich Insurance Company  2 |
| FI_TYPE_NAME | category | 2 | 0 | Federally Regulated Finan 328; Foreign Bank Representati 15 |
| FI_GROUP_NAME | category | 7 | 0 | Property & Casualty Insur 135; Banks 77; Life Insurance Companies 55; Trust Companies 41 |
| FI_INDUSTRY_NAME | category | 14 | 0 | Foreign Property & Casual 70; Canadian Property & Casua 62; Trust Companies 41; Domestic Banks 34 |
| CANADIAN_TRADE_COMPANY_NAME | who | 124 | 221 | Zurich Insurance Company  1; XL Specialty Insurance Co 1; XL Reinsurance America In 1; Wells Fargo Bank, Nationa 1 |
| REPRESENTATIVE_NAME | who | 249 | 3 | Laurie  LaPalme 10; Colleen Anne Sexsmith 7; James V.  Russell 6; Louis  Gagnon 5 |
| TITLE | category | 40 | 3 | Chief Executive Officer 127; Chief Agent 82; President and Chief Execu 30; President & Chief Executi 19 |
| ADDRESS_LINE_1 | other | 241 | 0 | 330 EAGLE STREET 9; 1 YORK STREET 6; 77 KING STREET WEST 6; 145 KING STREET WEST 6 |
| ADDRESS_LINE_2 | who | 124 | 129 | SUITE 400 8; SUITE 600 7; SUITE 2200 6; SUITE 100 6 |
| CITY | who | 53 | 0 | TORONTO 156; Toronto 44; MONTREAL 18; VANCOUVER 9 |
| PROVINCE_STATE | category | 10 | 0 | Ontario 267; Quebec 31; British Columbia 14; Alberta 11 |
| POSTAL_ZIP_CODE | other | 189 | 0 | M5H 1J8 10; L3Y 1K1 9; M5K 0A1 9; M5J 2J5 7 |
| AUTHORIZED_INSURANCE_CLASSES | other | 158 | 146 | Life; Accident and sickne 22; Life. 6; Credit protection; Life;  5; Liability; Automobile; Pr 4 |
| INGESTED_AT | audit | 1 | 0 | 1786134159064193 343 |
| SOURCE_RUN_ID | audit | 1 | 0 | c77db8be-8f67-4ca6-ba57-8 343 |
| SRC_SHA256 | who | 1 | 0 | a4c0645f6620e4f0b74ae65ad 343 |
