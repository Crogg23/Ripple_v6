# PORTAL_ARC_LA_COUNTY_OPEN_D_73B029DCD6

rows 1.8K  columns 27  scan 3.3s

roles: amount 4, audit 2, category 7, date 1, empty 1, id 2, other 4, who 7

## when

INGESTED_AT
  2026      1.8K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SALESVOL | 1.6K | 109.0K | 326.0K | 43.47M | 217.33M | 4.80B |
| EMPNUM | 1.8K | 1 | 4 | 350 | 2.0K | 46.9K |
| MIN_SQFT | 1.7K | 1 | 2.5K | 100.0K | 100.0K | 27.73M |
| MAX_SQFT | 1.6K | 1.5K | 5.0K | 100.0K | 100.0K | 27.33M |

## who

CONAME by rows
        15  Motel 6
        10  Extended Stay America
         5  Budget Inn
         4  Travel King Motel
         4  Apple Nine Hospitality Management, Inc
         3  Holiday Motel
         3  Colonial Motel
         3  Economy Inn
         3  Value Inn
         3  Travel Inn
         2  Broadway Inn
         2  Parq Hospitality LLC
         2  Royal Inn Motel
         2  Mitchell Hospitality Investments LLC
         2  Cni THL Ops, LLC
         2  La Mirage Inn
         2  Monterey Motel
         2  Islander Motel
         2  Fiesta Inn
         2  HPT TRS Ihg-2, Inc

CONAME by dollars
        2.0K        1 rows  The Ritz-Carlton Los Angeles
        1.2K        1 rows  Terranea California
        1.0K        1 rows  JW Marriott Los Angeles LA Live
         799        1 rows  The Beverly Hilton
         770        1 rows  Beverly Wilshire, A Four Seasons Hotel
         750        1 rows  The Westin Bonaventure Hotel & Suites, Los Angeles
         600        1 rows  Four Seasons Hotel Los Angeles at Beverly Hills
         600        1 rows  Los Angeles Airport Marriott
         600        1 rows  The Spa at Four Seasons Hotel Westlake Village
         550        1 rows  Queen Mary
         450        1 rows  Pacific Palms Resort
         450        1 rows  Hyatt Regency Long Beach
         440        1 rows  The Peninsula Beverly Hills
         420        1 rows  Sheraton Gateway Los Angeles Hotel
         400        1 rows  Hilton Los Angeles/Universal City
         400        1 rows  Loews Hollywood
         400        1 rows  SLS Hotel, Luxury Collection Hotel, Beverly Hills
         350        1 rows  Sheraton Universal Hotel
         350        1 rows  Intercontinental Los Angeles Downtown, An IHG Hotel
         340        1 rows  The Ritz-Carlton, Marina Del Rey

HQNAME by rows
        83  Marriott International, Inc
        78  Hilton Worldwide Inc
        39  Choice Hotels International, Inc
        37  Best Western International Inc
        34  G6 Hospitality LLC
        24  Holiday Hospitality Franchising, LLC
        15  Hyatt Hotels Corporation
        13  Extended Stay America, Inc
        13  Travelodge Hotels, Inc
        10  Days Inns Worldwide, Inc
        10  Ramada International Inc
         9  Super 8 Motels Inc
         9  Sheraton Hotels & Resorts
         7  Red Lion Hotels Corporation
         7  Vagabond Inn Hotels
         6  Proper Hospitality, LLC
         6  Sonesta International Hotels Corporation
         5  Westin Hotels & Resorts
         5  La Quinta Holdings Inc
         4  Kimpton Hotel & Restaurant Group LLC

HQNAME by dollars
        6.8K       78 rows  Hilton Worldwide Inc
        6.5K       83 rows  Marriott International, Inc
        2.7K        3 rows  The Ritz-Carlton Hotel Co LLC
        1.7K        9 rows  Sheraton Hotels & Resorts
        1.6K       15 rows  Hyatt Hotels Corporation
        1.6K        5 rows  Westin Hotels & Resorts
        1.0K       24 rows  Holiday Hospitality Franchising, LLC
         741       37 rows  Best Western International Inc
         646        6 rows  Sonesta International Hotels Corporation
         549        4 rows  AccorHotels North America
         529       39 rows  Choice Hotels International, Inc
         510       34 rows  G6 Hospitality LLC
         400        1 rows  Dakota Development
         400        2 rows  Intercontinental Hotels Group
         400        1 rows  Loews Hotels
         263        5 rows  La Quinta Holdings Inc
         237       10 rows  Ramada International Inc
         235        2 rows  W Hotels Worldwide
         219        1 rows  Omni Hotels & Resorts
         218        4 rows  Kimpton Hotel & Restaurant Group LLC

STATE_NAME by rows
      1.8K  California

STATE_NAME by dollars
       46.9K     1.8K rows  California

SOURCE by rows
      1.8K  Data Axle

SOURCE by dollars
       46.9K     1.8K rows  Data Axle

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = EMPNUM
  Apple Nine Hospitality Management, Inc    2026:26
  Beverly Wilshire, A Four Seasons Hotel    2026:770
  Broadway Inn                              2026:16
  Budget Inn                                2026:24
  Cni THL Ops, LLC                          2026:12
  Colonial Motel                            2026:7
  Economy Inn                               2026:7
  Extended Stay America                     2026:120
  Fiesta Inn                                2026:9
  Four Seasons Hotel Los Angeles at Beverl  2026:600
  HPT TRS Ihg-2, Inc                        2026:16
  Holiday Motel                             2026:4
  Islander Motel                            2026:8
  JW Marriott Los Angeles LA Live           2026:1.0K
  La Mirage Inn                             2026:7
  Los Angeles Airport Marriott              2026:600
  Mitchell Hospitality Investments LLC      2026:9
  Monterey Motel                            2026:7
  Motel 6                                   2026:266
  Parq Hospitality LLC                      2026:6
  Queen Mary                                2026:550
  Royal Inn Motel                           2026:3
  Terranea California                       2026:1.2K
  The Beverly Hilton                        2026:799
  The Ritz-Carlton Los Angeles              2026:2.0K
  The Spa at Four Seasons Hotel Westlake V  2026:600
  The Westin Bonaventure Hotel & Suites, L  2026:750
  Travel Inn                                2026:9
  Travel King Motel                         2026:5
  Value Inn                                 2026:10

HQNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = EMPNUM
  AccorHotels North America                 2026:549
  Best Western International Inc            2026:741
  Choice Hotels International, Inc          2026:529
  Dakota Development                        2026:400
  Days Inns Worldwide, Inc                  2026:74
  Extended Stay America, Inc                2026:159
  G6 Hospitality LLC                        2026:510
  Hilton Worldwide Inc                      2026:6.8K
  Holiday Hospitality Franchising, LLC      2026:1.0K
  Hyatt Hotels Corporation                  2026:1.6K
  Intercontinental Hotels Group             2026:400
  Kimpton Hotel & Restaurant Group LLC      2026:218
  La Quinta Holdings Inc                    2026:263
  Loews Hotels                              2026:400
  Marriott International, Inc               2026:6.5K
  Omni Hotels & Resorts                     2026:219
  Proper Hospitality, LLC                   2026:151
  Ramada International Inc                  2026:237
  Red Lion Hotels Corporation               2026:53
  Sheraton Hotels & Resorts                 2026:1.7K
  Sonesta International Hotels Corporation  2026:646
  Super 8 Motels Inc                        2026:62
  The Ritz-Carlton Hotel Co LLC             2026:2.7K
  Travelodge Hotels, Inc                    2026:137
  Vagabond Inn Hotels                       2026:87
  W Hotels Worldwide                        2026:235
  Westin Hotels & Resorts                   2026:1.6K

## what

SIC: 701101 82%, 701103 17%, 701112 0%

NAICS: 72111002 82%, 72111001 17%, 72111003 0%

PLACETYPE: Independent 72%, Branch 27%, Headquarters 1%

SQFTCODE: 2.0 34%, 3.0 17%, 7.0 9%, 8.0 9%, 4.0 8%, 5.0 6%, 1.0 6%, nan 5%, 6.0 4%

SQFOOTAGE: 1500 - 2499 35%, 2500 - 4999 18%, 40000 - 99999 10%, 100000+ 9%, 5000 - 9999 9%, 10000 - 19999 7%, 1 - 1499 7%, 20000 - 39999 5%

AFFILIATE: Five Star Alliance 56%, Mr & Mrs Smith 12%, Preferred Hotels & Resorts,Fiv 6%, Mr & Mrs Smith,Design Hotels 6%, Magnuson Independents 5%, Mr & Mrs Smith,Five Star Allia 5%, SureStay Collection by Best We 3%, Historic Hotels of America,Fiv 3%, BW Signature Collection by Bes 2%, Preferred Hotels & Resorts,His 2%, Preferred Hotels & Resorts 2%

LOC_CONF: Very High 96%, High 4%, Low 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.8K | 0 | 502859 10; 502379 9; 502005 9; 502004 9 |
| CONAME | who | 1.7K | 0 | Motel 6 17; Extended Stay America 12; Cni THL Ops, LLC 10; PCG Hospitality Group 10 |
| STREET | who | 675 | 0 | W Sunset Blvd 44; W Century Blvd 36; S Western Ave 35; Wilshire Blvd 33 |
| CITY | who | 123 | 0 | Los Angeles 477; Long Beach 115; Santa Monica 62; Inglewood 48 |
| STATE | other | 1 | 0 | CA 1.8K |
| STATE_NAME | who | 1 | 0 | California 1.8K |
| ZIP | other | 255 | 0 | 90028 50; 90069 34; 90045 27; 90304 26 |
| ZIP4 | other | 1.2K | 10 | 4414 12; 3737 12; 7404 12; 3409 12 |
| SIC | category | 3 | 0 | 701101 1.5K; 701103 312; 701112 8 |
| NAICS | category | 3 | 0 | 72111002 1.5K; 72111001 312; 72111003 8 |
| SALESVOL | amount | 132 | 0 | 218000.0 425; 326000.0 307; 109000.0 162; nan 158 |
| EMPNUM | amount | 128 | 0 | 2.0 377; 3.0 309; 1.0 165; 4.0 96 |
| PLACETYPE | category | 3 | 0 | Independent 1.3K; Branch 489; Headquarters 10 |
| HQNAME | who | 70 | 1.3K | Marriott International, I 83; Hilton Worldwide Inc 78; Choice Hotels Internation 39; Best Western Internationa 37 |
| SQFTCODE | category | 9 | 0 | 2.0 604; 3.0 315; 7.0 170; 8.0 157 |
| SQFOOTAGE | category | 9 | 92 | 1500 - 2499 604; 2500 - 4999 315; 40000 - 99999 170; 100000+ 157 |
| MIN_SQFT | amount | 9 | 0 | 1500.0 604; 2500.0 315; 40000.0 170; 100000.0 157 |
| MAX_SQFT | amount | 8 | 0 | 2499.0 604; 4999.0 315; nan 249; 99999.0 170 |
| AFFILIATE | category | 13 | 1.7K | Five Star Alliance 37; Mr & Mrs Smith 8; Preferred Hotels & Resort 4; Mr & Mrs Smith,Design Hot 4 |
| BRAND | empty | 1 | 1.8K |  |
| LOC_CONF | category | 3 | 0 | Very High 1.7K; High 77; Low 4 |
| SOURCE | who | 1 | 0 | Data Axle 1.8K |
| ESRI_PID | id | 1.8K | 0 | 4418bb31b441698ce31c1c951 10; 2d4343b748b389701c5992f87 9; f6013bd39cfff07257490e8dc 9; fcab461ce284244746da39668 9 |
| GEOMETRY | other | 1.6K | 0 | {"type": "Point", "coordi 11; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10; {"type": "Point", "coordi 10 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:31:15.34703 1.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | a4a26dcf-0dae-4c39-8e02-9 1.8K |
| SRC_SHA256 | who | 1 | 0 | 0d03df608a7fc407a5ab4ff25 1.8K |
