# FED_USGS_TOPOVIEW

rows 250  columns 21  scan 3.0s

roles: audit 2, date 3, empty 8, other 6, who 2

## when

DATECREATED
  2018       108  ##############################
  2019         1  
  2023        77  #####################
  2024        62  #################
  2025         2  #

LASTUPDATED
  2025       250  ##############################

PUBLICATIONDATE
  1943         1  
  1947       143  ##############################
  1949        18  ####
  1950        55  ############
  1972         1  
  1978         2  
  1979         5  #
  1980         1  
  1981         1  
  1982         1  
  1983         4  #
  1984         2  
  1985         9  ##
  1986         1  
  1989         2  
  1990         2  
  1994         2  

## who

SOURCENAME by rows
       250  ScienceBase

_SRC_SHA256 by rows
       250  b7f26d3fac33d384da64a7c234c0a8d2fc2c9ad0bc585a0f279bc51f56c66c78

## who x when

SOURCENAME by DATECREATED
  ScienceBase                               2018:108 2019:1 2023:77 2024:62 2025:2

_SRC_SHA256 by DATECREATED
  b7f26d3fac33d384da64a7c234c0a8d2fc2c9ad0  2018:108 2019:1 2023:77 2024:62 2025:2

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TITLE | other | 239 | 0 | USGS 1:100000-scale Quadr 3; USGS 1:100000-scale Quadr 3; USGS 1:100000-scale Quadr 3; USGS 1:100000-scale Quadr 3 |
| MPDESC | empty | 1 | 250 |  |
| SOURCEID | other | 248 | 0 | 5a8a5018e4b00f54eb4090e5 2; 5a8a3ecee4b00f54eb3eaaeb 2; 5a8a3ecde4b00f54eb3eaae9 2; 5a8a3ef5e4b00f54eb3eae13 2 |
| SOURCENAME | who | 1 | 0 | ScienceBase 250 |
| DATECREATED | date | 255 | 0 | 2018-02-18T21:18:32.704-0 2; 2018-02-18T20:04:46.097-0 2; 2018-02-18T20:04:45.879-0 2; 2018-02-18T20:05:25.535-0 2 |
| LASTUPDATED | date | 205 | 0 | 2025-09-17T18:23:54.013-0 3; 2025-09-17T18:25:06.157-0 3; 2025-09-17T18:25:42.230-0 3; 2025-09-17T18:27:42.469-0 3 |
| PUBLICATIONDATE | date | 17 | 0 | 1947-01-01 143; 1950-01-01 55; 1949-01-01 18; 1985-01-01 9 |
| DOWNLOADURL | other | 252 | 0 | https://prd-tnm.s3.amazon 2; https://prd-tnm.s3.amazon 2; https://prd-tnm.s3.amazon 2; https://prd-tnm.s3.amazon 2 |
| FILESIZE | empty | 1 | 250 |  |
| FILEFORMAT | empty | 1 | 250 |  |
| DATASETS | empty | 1 | 250 |  |
| BOUNDINGBOX | other | 226 | 0 | {"minX": -74.0, "maxX": - 4; {"minX": -94.0, "maxX": - 3; {"minX": -106.0, "maxX":  3; {"minX": -114.0, "maxX":  3 |
| FIPS | empty | 1 | 250 |  |
| STATE | empty | 1 | 250 |  |
| COUNTIES | empty | 1 | 250 |  |
| MAPSCALE | empty | 1 | 250 |  |
| PREVIEWGRAPHICURL | other | 251 | 0 | https://prd-tnm.s3.amazon 2; https://prd-tnm.s3.amazon 2; https://prd-tnm.s3.amazon 2; https://prd-tnm.s3.amazon 2 |
| METAURL | other | 253 | 0 | https://www.sciencebase.g 2; https://www.sciencebase.g 2; https://www.sciencebase.g 2; https://www.sciencebase.g 2 |
| _INGESTED_AT | audit | 1 | 0 | 1783016317772389 250 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 52a94513-0f62-430b-bdbb-f 250 |
| _SRC_SHA256 | who | 1 | 0 | b7f26d3fac33d384da64a7c23 250 |
