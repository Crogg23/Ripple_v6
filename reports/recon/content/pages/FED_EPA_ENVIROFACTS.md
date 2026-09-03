# FED_EPA_ENVIROFACTS

rows 5.0K  columns 17  scan 2.5s

roles: audit 2, empty 8, other 2, who 5

## who

FACILITY_NAME by rows
        17  TILCON CONNECTICUT INC
         9  AGGREGATE INDUSTRIES NORTHEAST REGION INC
         7  PRATT & WHITNEY
         7  HOLCIM - NER INC.
         6  DAUPHINAIS CONCRETE INC.
         6  GE CO
         5  SAFETY-KLEEN SYSTEMS INC
         5  POLAROID CORP
         5  DIGITAL EQUIPMENT CORP
         5  PARADIGM MANCHESTER INC
         5  AGGREGATE INDUSTRIES NORTHEAST REGION INC.
         5  OSRAM SYLVANIA INC
         5  TILCON CONNECTICUT INC.
         5  DELUXE CHECK PRINTERS INC
         4  BROX INDUSTRIES INC
         4  NEW BALANCE ATHLETIC SHOE INC
         4  ANTAYA TECHNOLOGIES CORP
         4  HP HOOD LLC
         4  BODYCOTE THERMAL PROCESSING
         4  O&G INDUSTRIES INC.

TABLE_NAME by rows
      5.0K  tri.tri_facility

CITY_NAME by rows
       110  NEWARK
        86  PROVIDENCE
        67  WATERBURY
        59  WORCESTER
        47  MANCHESTER
        47  BRIDGEPORT
        44  CLIFTON
        42  PAWTUCKET
        40  MILFORD
        40  SOUTH PLAINFIELD
        39  NASHUA
        38  FALL RIVER
        37  SPRINGFIELD
        37  LINDEN
        36  WATERTOWN
        36  NEW BEDFORD
        35  CRANSTON
        35  HUDSON
        35  ATTLEBORO
        34  DANBURY

COUNTY_NAME by rows
       507  MIDDLESEX
       384  ESSEX
       294  PROVIDENCE
       288  WORCESTER
       275  NEW HAVEN
       264  HARTFORD
       225  BRISTOL
       195  FAIRFIELD
       154  HAMPDEN
       147  NORFOLK
       138  UNION
       125  HILLSBOROUGH
       121  BERGEN
       100  HUDSON
        85  PASSAIC
        84  ROCKINGHAM
        84  LITCHFIELD
        68  SUFFOLK
        64  WINDHAM
        63  FRANKLIN

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| TABLE_NAME | who | 1 | 0 | tri.tri_facility 5.0K |
| PROGRAM_SCHEMA | other | 1 | 0 | TRI 5.0K |
| STATE_CODE | empty | 1 | 5.0K |  |
| CITY_NAME | who | 826 | 0 | NEWARK 125; PROVIDENCE 91; WATERBURY 79; BRIDGEPORT 59 |
| POSTAL_CODE | other | 1.5K | 0 | 07105 82; 07080 54; 07036 54; 06810 47 |
| COUNTY_NAME | who | 138 | 0 | MIDDLESEX 507; ESSEX 384; PROVIDENCE 294; WORCESTER 288 |
| FRS_ID | empty | 1 | 5.0K |  |
| HANDLER_ID | empty | 1 | 5.0K |  |
| SITE_ID | empty | 1 | 5.0K |  |
| FACILITY_NAME | who | 4.7K | 0 | TILCON CONNECTICUT INC 33; NEW YORK TWIST DRILL INC 26; KEARFOTT GUIDANCE & NAVIG 26; REPEAT-O-TYPE MANUFACTURI 25 |
| LATITUDE | empty | 1 | 5.0K |  |
| LONGITUDE | empty | 1 | 5.0K |  |
| CREATED_DATE | empty | 1 | 5.0K |  |
| MEDIA_NAME | empty | 1 | 5.0K |  |
| _INGESTED_AT | audit | 1 | 0 | 1782950869008704 5.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | 60bff868-e540-4580-8cef-e 5.0K |
| _SRC_SHA256 | who | 1 | 0 | ed7ab5828ac50c3b7bfc681be 5.0K |
