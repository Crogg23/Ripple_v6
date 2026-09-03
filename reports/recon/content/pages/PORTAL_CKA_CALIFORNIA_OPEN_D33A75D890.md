# PORTAL_CKA_CALIFORNIA_OPEN_D33A75D890

rows 10.0K  columns 7  scan 3.0s

roles: audit 2, date 2, id 1, other 1, who 2

## when

EXPIRATION_DATE
  2026      1.1K  ########
  2027      4.2K  ##############################
  2028      2.9K  #####################
  2029      1.7K  ############
  2030        51  

INGESTED_AT
  2026     10.0K  ##############################

## who

ELECTRICIAN_NAME by rows
         6  CORTEZ  AQUINO, MIGUEL A
         5  CARRILLO, DANIEL
         4  CASTREJON, FRANCISCO A
         4  CASTELLANOS, DANIEL
         4  DURAN, CHRISTIAN
         4  BYRD, LESTER P
         3  ESPARZA, JOSE
         3  CHANN, VISALL
         3  CARRILLO, JUAN C
         3  BARRIENTOS GARCIA, KENERT B
         3  BUCKALEW, CHARLES E
         3  BRIGGS, JASON D
         3  CORTEZ, ERNESTO
         3  CHAVEZ, MIGUEL A
         3  CANSECO, EDMUNDO
         3  AVELAR, FERNANDO
         3  CORTEZ, JOSE M
         3  CHAMPLIN, KENNETH R
         3  BABSON, FREDERICK A
         3  ANDRADE, ALBERTO

SRC_SHA256 by rows
     10.0K  ebc91823d2a9682c493ee9986cabebbe6e4a5a3355df0cf8bb15770f7e05f53c

## who x when

ELECTRICIAN_NAME by EXPIRATION_DATE
  ANDRADE, ALBERTO                          2028:3
  AVELAR, FERNANDO                          2026:1 2027:1 2029:1
  BABSON, FREDERICK A                       2026:1 2029:2
  BARRIENTOS GARCIA, KENERT B               2026:2 2028:1
  BRIGGS, JASON D                           2028:2 2029:1
  BUCKALEW, CHARLES E                       2027:3
  BYRD, LESTER P                            2026:2 2029:2
  CANSECO, EDMUNDO                          2026:1 2027:1 2029:1
  CARRILLO, DANIEL                          2026:2 2028:1 2029:2
  CARRILLO, JUAN C                          2026:1 2028:1 2029:1
  CASTELLANOS, DANIEL                       2026:2 2029:2
  CASTREJON, FRANCISCO A                    2026:2 2029:2
  CHAMPLIN, KENNETH R                       2026:1 2027:1 2029:1
  CHANN, VISALL                             2027:2 2028:1
  CHAVEZ, MIGUEL A                          2027:2 2029:1
  CORTEZ  AQUINO, MIGUEL A                  2027:3 2030:3
  CORTEZ, ERNESTO                           2026:1 2027:1 2029:1
  CORTEZ, JOSE M                            2026:2 2029:1
  DURAN, CHRISTIAN                          2026:2 2029:2
  ESPARZA, JOSE                             2026:1 2027:2

SRC_SHA256 by EXPIRATION_DATE
  ebc91823d2a9682c493ee9986cabebbe6e4a5a33  2026:1.1K 2027:4.2K 2028:2.9K 2029:1.7K 2030:51

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ELECTRICIAN_NAME | who | 9.3K | 0 | FELLER, SETH W 51; FELIX JUAREZ, ROBIN A 51; FEENEY, ROBERT 51; FAWCETT, JOSEPH M 51 |
| ZIP_CODE | other | 1.7K | 0 | 95023 71; 95020 62; 94561 61; 93312 58 |
| CERTIFICATE_NUMBER | id | 9.7K | 0 | E-125328-G 51; E-152821-G 51; E-176060-G 51; E-138639-F 51 |
| EXPIRATION_DATE | date | 1.3K | 0 | 06/01/2029 88; 06/01/2027 72; 06/05/2029 54; 05/22/2029 52 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:52:08.38747 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 258bc52d-eb2c-43bb-994c-1 10.0K |
| SRC_SHA256 | who | 1 | 0 | ebc91823d2a9682c493ee9986 10.0K |
