# PORTAL_CKA_TAMPA_OPEN_DATA_18B980D54D

rows 952  columns 13  scan 3.4s

roles: amount 1, audit 2, category 7, date 2, other 1, who 1

## when

DATE
  2022       129  #####################
  2023       130  ######################
  2024       133  ######################
  2025       165  ###########################
  2026       181  ##############################
  2027       130  ######################
  2028        71  ############
  2029        13  ##

INGESTED_AT
  2026       952  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| VALUE | 952 | 0 | 53.50 | 754.49 | 877 | 113.9K |

## who

SRC_SHA256 by rows
       952  8254652d07e183574e5fa3e038d1300bb158eb9d8cfb5ff0066545ac88d4cb0e

SRC_SHA256 by dollars
      113.9K      952 rows  8254652d07e183574e5fa3e038d1300bb158eb9d8cfb5ff0066545ac88d4

## who x when

SRC_SHA256 by DATE, dollars = VALUE
  8254652d07e183574e5fa3e038d1300bb158eb9d  2022:18.8K 2023:18.7K 2024:20.2K 2025:21.4K 2026:20.7K 2027:10.0K 2028:3.4K 2029:627

## what

C_ORGANIZATION: Equal Business Opportunity 91%, Neighborhood & Comm Affairs (N 9%

CHARTNAME: Certifications by Month 84%, Certifications by Year 8%, EBO - Total Certifications Pro 2%, EBO - Annual Subcontractor Goa 1%, EBO - Annual Prime Goals 1%, EBO - Certifications by Ethnic 1%, EBO - Certifications by Ethnic 1%, EBO - Certifications by Ethnic 1%, EBO - Certifications by Ethnic 1%, EBO - Certifications by Ethnic 1%, EBO - Reciprocal  Certificatio 0%, EBO - Recertification Certific 0%

DESCRIPTION: Certifications by Month 83%, Certifications by Year 7%, Total Certifications Processed 2%, Annual Subcontractor Goals 1%, Annual Prime Goals 1%, Professional Services 1%, Non-Professional Services 1%, Goods 1%, Construction-Related 1%, Construction 1%, Reciprocal  Certification Proc 0%, Recertification Certification  0%

CATEGORY: S 11%, HM 9%, HF 9%, CF 9%, BM 9%, AM 9%, BF 9%, AF 9%, NM 9%, NF 9%, SLBE 2%, WMBE 2%

SUMMARY: Total 97%, Percent 3%

TYPEDATA: Date 97%, Period 3%

PERIOD: FY25 14%, FY24 14%, FY23 14%, FY22 14%, FY21 14%, FY20 14%, FY19 14%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | other | 865 | 0 | 21285 5; 21284 5; 21283 5; 21282 5 |
| C_ORGANIZATION | category | 2 | 0 | Equal Business Opportunit 863; Neighborhood & Comm Affai 89 |
| CHARTNAME | category | 18 | 0 | Certifications by Month 792; Certifications by Year 71; EBO - Total Certification 20; EBO - Annual Subcontracto 14 |
| DESCRIPTION | category | 13 | 0 | Certifications by Month 792; Certifications by Year 71; Total Certifications Proc 20; Annual Subcontractor Goal 14 |
| CATEGORY | category | 18 | 0 | S 104; HM 86; HF 86; CF 86 |
| SUMMARY | category | 2 | 0 | Total 924; Percent 28 |
| TYPEDATA | category | 2 | 0 | Date 924; Period 28 |
| DATE | date | 129 | 0 | 06/30/2026 00:00:00 32; 07/01/2027 00:00:00 20; 07/01/2026 00:00:00 20; 07/01/2025 00:00:00 20 |
| PERIOD | category | 8 | 924 | FY25 4; FY24 4; FY23 4; FY22 4 |
| VALUE | amount | 304 | 0 | 1.000 108; 4.000 34; 16.000 27; 15.000 21 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:23:44.40793 952 |
| SOURCE_RUN_ID | audit | 1 | 0 | 03b6ebb5-1a29-4012-a1f7-1 952 |
| SRC_SHA256 | who | 1 | 0 | 8254652d07e183574e5fa3e03 952 |
