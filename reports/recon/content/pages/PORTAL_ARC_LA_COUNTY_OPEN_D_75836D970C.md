# PORTAL_ARC_LA_COUNTY_OPEN_D_75836D970C

rows 2.0K  columns 16  scan 4.3s

roles: amount 2, audit 2, category 1, date 1, id 3, other 4, who 4

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 2.0K | 33.33 | 34 | 34.51 | 34.80 | 68.0K |
| Y | 2.0K | -118.85 | -118.21 | -117.75 | -117.66 | -236.4K |

## who

FAC_NAME by rows
         7  NEW CINGULAR WIRELESS PCS, AT&T MOBILITY
         6  VERIZON WIRELESS
         6  SAN GABRIEL VALLEY WATER COMPANY
         3  LAS VIRGENES MUNICIPAL WATER DISTRICT
         3  KINNELOA IRRIGATION DISTRICT
         3  SO CAL EDISON CO
         3  EXXONMOBIL OIL CORPORATION
         3  FREY ENVIRONMENTAL INC
         3  WABA GRILL
         3  LA CITY DWP
         2  FAZIO CLEANERS, INC
         2  CALIFORNIA WATER SERVICE CO
         2  UNOCAL CORP
         2  FATBURGER
         2  PROPEL FUELS, INC
         2  CAL ST, WATER RESOURCES DEPT
         2  ROBERTSON'S READY MIX
         2  METROPOLITAN WATER DISTRICT OF SO CAL
         2  FLIGHT LINE PRODUCTS
         2  EL POLLO LOCO

FAC_NAME by dollars
      238.27        7 rows  NEW CINGULAR WIRELESS PCS, AT&T MOBILITY
      205.18        6 rows  VERIZON WIRELESS
      204.11        6 rows  SAN GABRIEL VALLEY WATER COMPANY
      102.56        3 rows  LA CITY DWP
      102.53        3 rows  KINNELOA IRRIGATION DISTRICT
      102.45        3 rows  EXXONMOBIL OIL CORPORATION
      102.41        3 rows  LAS VIRGENES MUNICIPAL WATER DISTRICT
      101.89        3 rows  WABA GRILL
      101.76        3 rows  FREY ENVIRONMENTAL INC
      101.75        3 rows  SO CAL EDISON CO
       69.57        2 rows  CAL ST, WATER RESOURCES DEPT
       68.91        2 rows  FLIGHT LINE PRODUCTS
       68.67        2 rows  SIEMENS HEALTHCARE DIAGNOSTICS
       68.27        2 rows  UNIVISION RADIO LOS ANGELES, INC.
       68.21        2 rows  WHOLE FOODS MARKET
       68.20        2 rows  FAZIO CLEANERS, INC
       68.17        2 rows  CHEVRON USA INC
       68.12        2 rows  FATBURGER
       68.12        2 rows  LA CITY, DEPT OF GEN SERVICES
       68.03        2 rows  THE FLAME BROILER

STREET by rows
       195  VARIOUS LO
        29  IMPERIAL
        26  VALLEY
        26  ALAMEDA
        25  FOOTHILL
        18  WASHINGTON
        18  SLAUSON
        17  FIGUEROA
        17  ROSECRANS
        17  WHITTIER
        16  ROSEMEAD
        16  BROADWAY
        16  CRENSHAW
        16  EL SEGUNDO
        15  MAIN
        15  WILSHIRE
        14  SANTA MONI
        14  NORMANDIE
        13  ATLANTIC
        13  OLYMPIC

STREET by dollars
        6.6K      195 rows  VARIOUS LO
      983.83       29 rows  IMPERIAL
      884.89       26 rows  VALLEY
      882.17       26 rows  ALAMEDA
      854.47       25 rows  FOOTHILL
      612.28       18 rows  WASHINGTON
      611.80       18 rows  SLAUSON
      577.96       17 rows  WHITTIER
      576.30       17 rows  ROSECRANS
      576.13       17 rows  FIGUEROA
      545.53       16 rows  ROSEMEAD
      542.72       16 rows  EL SEGUNDO
      542.65       16 rows  BROADWAY
      542.48       16 rows  CRENSHAW
      510.85       15 rows  WILSHIRE
      508.56       15 rows  MAIN
      476.68       14 rows  SANTA MONI
      473.88       14 rows  NORMANDIE
      442.26       13 rows  OLYMPIC
      442.16       13 rows  ATLANTIC

CITY by rows
       428  LOS ANGELES
       119  GARDENA
       117  CITY OF INDUSTRY
        76  SANTA FE SPRINGS
        75  WHITTIER
        66  COMPTON
        47  COVINA
        44  HAWTHORNE
        43  TORRANCE
        40  MARINA DEL REY
        39  LA PUENTE
        38  PASADENA
        37  SOUTH EL MONTE
        31  CALABASAS
        29  VALENCIA
        27  LYNWOOD
        26  AZUSA
        26  WALNUT
        24  SOUTH GATE
        23  RANCHO DOMINGUEZ

CITY by dollars
       14.6K      428 rows  LOS ANGELES
        4.0K      119 rows  GARDENA
        4.0K      117 rows  CITY OF INDUSTRY
        2.6K       76 rows  SANTA FE SPRINGS
        2.5K       75 rows  WHITTIER
        2.2K       66 rows  COMPTON
        1.6K       47 rows  COVINA
        1.5K       44 rows  HAWTHORNE
        1.5K       43 rows  TORRANCE
        1.4K       40 rows  MARINA DEL REY
        1.3K       39 rows  LA PUENTE
        1.3K       38 rows  PASADENA
        1.3K       37 rows  SOUTH EL MONTE
        1.1K       31 rows  CALABASAS
      998.58       29 rows  VALENCIA
      916.09       27 rows  LYNWOOD
      887.20       26 rows  AZUSA
      884.22       26 rows  WALNUT
      814.61       24 rows  SOUTH GATE
      784.43       23 rows  IRWINDALE

SRC_SHA256 by rows
      2.0K  d92aff3c8868a4f964442cbb87d69f66093b7d73972cde4aff1d2894710afa6b

SRC_SHA256 by dollars
       68.0K     2.0K rows  d92aff3c8868a4f964442cbb87d69f66093b7d73972cde4aff1d2894710a

## who x when

FAC_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  CAL ST, WATER RESOURCES DEPT              2026:69.57
  CALIFORNIA WATER SERVICE CO               2026:67.88
  CHEVRON USA INC                           2026:68.17
  EL POLLO LOCO                             2026:67.87
  EXXONMOBIL OIL CORPORATION                2026:102.45
  FATBURGER                                 2026:68.12
  FAZIO CLEANERS, INC                       2026:68.20
  FLIGHT LINE PRODUCTS                      2026:68.91
  FREY ENVIRONMENTAL INC                    2026:101.76
  KINNELOA IRRIGATION DISTRICT              2026:102.53
  LA CITY DWP                               2026:102.56
  LA CITY, DEPT OF GEN SERVICES             2026:68.12
  LAS VIRGENES MUNICIPAL WATER DISTRICT     2026:102.41
  METROPOLITAN WATER DISTRICT OF SO CAL     2026:67.96
  NEW CINGULAR WIRELESS PCS, AT&T MOBILITY  2026:238.27
  PROPEL FUELS, INC                         2026:67.65
  ROBERTSON'S READY MIX                     2026:67.91
  SAN GABRIEL VALLEY WATER COMPANY          2026:204.11
  SIEMENS HEALTHCARE DIAGNOSTICS            2026:68.67
  SO CAL EDISON CO                          2026:101.75
  THE FLAME BROILER                         2026:68.03
  UNIVISION RADIO LOS ANGELES, INC.         2026:68.27
  UNOCAL CORP                               2026:67.81
  VERIZON WIRELESS                          2026:205.18
  WABA GRILL                                2026:101.89
  WHOLE FOODS MARKET                        2026:68.21

STREET by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  ALAMEDA                                   2026:882.17
  ATLANTIC                                  2026:442.16
  BROADWAY                                  2026:542.65
  CRENSHAW                                  2026:542.48
  EL SEGUNDO                                2026:542.72
  FIGUEROA                                  2026:576.13
  FOOTHILL                                  2026:854.47
  IMPERIAL                                  2026:983.83
  MAIN                                      2026:508.56
  NORMANDIE                                 2026:473.88
  OLYMPIC                                   2026:442.26
  ROSECRANS                                 2026:576.30
  ROSEMEAD                                  2026:545.53
  SANTA MONI                                2026:476.68
  SLAUSON                                   2026:611.80
  VALLEY                                    2026:884.89
  VARIOUS LO                                2026:6.6K
  WASHINGTON                                2026:612.28
  WHITTIER                                  2026:577.96
  WILSHIRE                                  2026:510.85

## what

TITLEV: nan 100%, YES 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| X | amount | 1.8K | 0 | 33.889088600000036 16; 33.990815000000055 14; 34.09683920000003 12; 33.975585000000024 12 |
| Y | amount | 1.7K | 0 | -118.27131369999995 16; -118.33612499999998 14; -118.09395409999996 12; -118.25645999999995 12 |
| MATCH_ADDR | other | 1.8K | 0 |    VARIOUS LO  190; 42230  N LAKE HUGHE RD 10; 1601   CORPORATE  DR 10; 535  W ALLEN AVE 10 |
| STREET | who | 716 | 0 | VARIOUS LO 195; IMPERIAL 29; ALAMEDA 26; VALLEY 26 |
| CITY | who | 132 | 0 | LOS ANGELES 428; GARDENA 119; CITY OF INDUSTRY 117; SANTA FE SPRINGS 76 |
| ZIPCODE | other | 183 | 0 | 90248 79; 90670 73; 91748 55; 90022 51 |
| FAC_ID | id | 2.0K | 0 | 195909 10; 91134 10; 74227 10; 119778 10 |
| FAC_NAME | who | 1.9K | 0 | EXXONMOBIL OIL CORPORATIO 11; VERIZON WIRELESS 11; CAL ST, WATER RESOURCES D 11; NEW CINGULAR WIRELESS PCS 11 |
| NAICS_CODE | other | 472 | 0 | 722511 100; 811121 81; 722513 63; 811111 61 |
| FAC_ID_INTEGER | id | 2.0K | 0 | 195909 10; 91134 10; 74227 10; 119778 10 |
| TITLEV | category | 2 | 0 | nan 2.0K; YES 7 |
| GEOMETRY | other | 1.7K | 0 | {"type": "Point", "coordi 16; {"type": "Point", "coordi 14; {"type": "Point", "coordi 12; {"type": "Point", "coordi 12 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:35:30.31498 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | d4dcde47-00bb-4575-be32-6 2.0K |
| SRC_SHA256 | who | 1 | 0 | d92aff3c8868a4f964442cbb8 2.0K |
