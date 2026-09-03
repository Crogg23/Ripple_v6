# FED_COURTLISTENER_SCHOOLS

rows 6.0K  columns 9  scan 2.9s

roles: audit 2, date 3, id 1, other 2, who 2

## when

DATE_CREATED
  2010      5.8K  ##############################
  2019        93  
  2020         1  
  2022        97  

DATE_MODIFIED
  2010      5.8K  ##############################
  2019        93  
  2020         1  
  2022        97  #
  2025         1  

_INGESTED_AT
  2026      6.0K  ##############################

## who

NAME by rows
         2  Carleton College
         2  Cuesta College
         1  ECU
         1  Hardin-Simmons University
         1  Penn State
         1  Concordia University-Ann Arbor
         1  Chamberlain College of NursingAddison
         1  ITT Technical Institute-Akron
         1  CNM
         1  Northwestern Oklahoma State
         1  Bryant & Stratton College-Albany
         1  Trinity School for Ministry
         1  Southwest Acupuncture College-Albuquerque
         1  Ohio University-Main Campus
         1  SUNY College of Technology at Alfred
         1  Sul Ross State University
         1  Bethesda University of California
         1  Bard College
         1  Trinity Episcopal School for Ministry
         1  Pennsylvania State University-Penn State Abington

_SRC_SHA256 by rows
      6.0K  c9f95708b1fcbc98c47b1d293ee21a1f5d3df55820de6992a3f698615d5dbffd

## who x when

NAME by DATE_CREATED
  Bard College                              2010:1
  Bethesda University of California         2010:1
  Bryant & Stratton College-Albany          2010:1
  CNM                                       2010:1
  Carleton College                          2010:1 2022:1
  Chamberlain College of NursingAddison    2010:1
  Concordia University-Ann Arbor            2010:1
  Cuesta College                            2010:1 2022:1
  ECU                                       2010:1
  Hardin-Simmons University                 2010:1
  ITT Technical Institute-Akron             2010:1
  Northwestern Oklahoma State               2010:1
  Ohio University-Main Campus               2010:1
  Penn State                                2010:1
  Pennsylvania State University-Penn State  2010:1
  SUNY College of Technology at Alfred      2010:1
  Southwest Acupuncture College-Albuquerqu  2010:1
  Sul Ross State University                 2010:1
  Trinity Episcopal School for Ministry     2010:1
  Trinity School for Ministry               2010:1

_SRC_SHA256 by DATE_CREATED
  c9f95708b1fcbc98c47b1d293ee21a1f5d3df558  2010:5.8K 2019:93 2020:1 2022:97

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 5.9K | 0 | 5210 31; 6539 31; 6538 31; 6536 31 |
| DATE_CREATED | date | 192 | 0 | 2010-06-08 00:00:00+00 5.8K; 2022-08-09 21:34:17.20303 1; 2022-08-05 16:58:31.11207 1; 2022-08-02 16:59:11.91654 1 |
| DATE_MODIFIED | date | 191 | 0 | 2010-06-08 00:00:00+00 5.8K; 2025-06-16 05:32:10.95750 1; 2022-08-09 21:34:17.20305 1; 2022-08-05 16:58:31.11209 1 |
| NAME | who | 5.9K | 0 | UC Law San Francisco 31; University College of Lon 31; Texas Arts & Industries U 31; Tyler Junior College 31 |
| EIN | other | 2.5K | 2.5K | 362061311 127; 860344364 78; 362781982 53; 460276203 31 |
| IS_ALIAS_OF_ID | other | 1.2K | 3.6K | 5721 30; 5867 28; 3330 24; 3244 24 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-12 00:04:02.059 6.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 4b58cf9c-40a9-4607-b705-a 6.0K |
| _SRC_SHA256 | who | 1 | 0 | c9f95708b1fcbc98c47b1d293 6.0K |
