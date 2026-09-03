# FED_NASA_OPEN_DATA

rows 54  columns 11  scan 3.6s

roles: audit 2, category 4, date 1, other 3, who 1

## when

RESPONSE_DATE
  1998         1  #
  2004         2  ##
  2009         1  #
  2010         1  #
  2012         1  #
  2014         1  #
  2016         1  #
  2020         2  ##
  2022         4  ####
  2023         1  #
  2024         3  ###
  2025         2  ##
  2026        34  ##############################

## who

_SRC_SHA256 by rows
        54  bf0f37ba62f00baed9e1370be15cfe3ca0cbe0816fc618d0655ce7d0dc9a088d

## who x when

_SRC_SHA256 by RESPONSE_DATE
  bf0f37ba62f00baed9e1370be15cfe3ca0cbe081  1998:1 2004:2 2009:1 2010:1 2012:1 2014:1 2016:1 2020:2 2022:4 2023:1 2024:3 2025:2 2026:34

## what

API_NAME: NeoWs Near Earth Objects 63%, NASA Image and Video Library 37%

REQUEST_URL: https://api.nasa.gov/neo/rest/ 63%, https://images-api.nasa.gov/se 37%

TITLE: Axiom Space’s AxEMU Spacesuit 35%, (2018 NV) 6%, (2018 LW5) 6%, (2016 TA57) 6%, (2016 JH17) 6%, (2014 NV63) 6%, (2014 MR67) 6%, (2002 EM7) 6%, 499998 (2011 PT) 6%, (2019 NG) 6%, (2018 VP5) 6%, (2016 XR23) 6%

MEDIA_TYPE: data 63%, image 37%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| API_NAME | category | 2 | 0 | NeoWs Near Earth Objects 34; NASA Image and Video Libr 20 |
| REQUEST_URL | category | 2 | 0 | https://api.nasa.gov/neo/ 34; https://images-api.nasa.g 20 |
| RESPONSE_DATE | date | 22 | 0 | 2026-06-26 8; 2026-07-02 7; 2026-06-27 6; 2026-07-01 5 |
| TITLE | category | 49 | 0 | Axiom Space’s AxEMU Space 6; (2018 NV) 1; (2018 LW5) 1; (2016 TA57) 1 |
| DESCRIPTION | other | 53 | 0 | An up close image of a gl 2; Hazardous: False / Miss d 1; Hazardous: False / Miss d 1; Hazardous: True / Miss di 1 |
| URL | other | 54 | 0 | https://ssd.jpl.nasa.gov/ 1; https://ssd.jpl.nasa.gov/ 1; https://ssd.jpl.nasa.gov/ 1; https://ssd.jpl.nasa.gov/ 1 |
| MEDIA_TYPE | category | 2 | 0 | data 34; image 20 |
| RAW_JSON | other | 54 | 0 | {"links": {"self": "http: 1; {"links": {"self": "http: 1; {"links": {"self": "http: 1; {"links": {"self": "http: 1 |
| _INGESTED_AT | audit | 1 | 0 | 1783011108768880 54 |
| _SOURCE_RUN_ID | audit | 1 | 0 | 865acf0c-d2b2-41de-88a2-c 54 |
| _SRC_SHA256 | who | 1 | 0 | bf0f37ba62f00baed9e1370be 54 |
