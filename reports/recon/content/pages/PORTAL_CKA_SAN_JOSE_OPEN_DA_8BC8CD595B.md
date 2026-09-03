# PORTAL_CKA_SAN_JOSE_OPEN_DA_8BC8CD595B

rows 569  columns 28  scan 4.3s

roles: amount 3, audit 2, category 11, date 1, other 5, who 7

## when

INGESTED_AT
  2026       569  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AREASQFT | 569 | 71.94 | 5.1K | 181.4K | 1.15M | 10.32M |
| SHAPE_LENGTH | 569 | 52.65 | 1.0K | 9.3K | 18.6K | 911.5K |
| SHAPE_AREA | 569 | 71.94 | 5.1K | 181.4K | 1.15M | 10.32M |

## who

SUBCORRIDORGROUP by rows
         8  Monterey Rd 4
         8  S 2nd St Alleys
         8  Vine St Alleys 2
         7  Old Piedmont Rd 4
         7  Bailey Ave 1
         7  McLaughlin Ave
         6  Vine St Alleys 1
         6  San Felipe Rd 3
         6  Hostetter Rd 2
         6  San Felipe Rd 8
         5  Coyote Creek Fields at Hwy 280
         5  Alviso 1
         5  Yerba Buena Rd
         5  Coleman Ave
         5  Taylor St 1
         5  Zanker Rd 2
         5  Fowler Rd
         5  Almaden Expwy
         5  Sierra Rd 3
         5  Hedding St 2

SUBCORRIDORGROUP by dollars
       1.57M        5 rows  Coyote Creek Fields at Hwy 280
       1.15M        1 rows  Basking Ridge Ave
      384.9K        8 rows  Monterey Rd 4
      265.7K        1 rows  Branham Ln 3
      223.4K        2 rows  Monterey Rd 2
      203.6K        2 rows  Camden Ave 5
      192.5K        1 rows  Camden Ave 4
      174.6K        1 rows  Monterey Rd 11
      162.2K        4 rows  Mabury Rd
      149.6K        3 rows  Curtner Ave
      145.5K        1 rows  Monterey Rd 10
      143.1K        1 rows  McKean Rd Fire Station
      133.3K        4 rows  Cropley Ave
      132.0K        1 rows  Monterey Rd 9
      130.2K        5 rows  Almaden Expwy
      129.3K        7 rows  Bailey Ave 1
      101.7K        3 rows  Old Piedmont Rd 3
       99.5K        2 rows  Bailey Ave 4
       94.1K        3 rows  Coleman Rd 3
       93.9K        2 rows  Santa Teresa Blvd 4

CORRIDORGROUP by rows
        21  San Felipe Rd
        20  Monterey Rd
        14  Bailey Ave
        14  Vine St Alleys
        13  Almaden Rd
        13  Sierra Rd
        13  Old Piedmont Rd
        11  Zanker Rd
        10  Bascom Ave
         9  Camden Ave
         9  Santa Teresa Blvd
         9  Taylor St
         9  Branham Ln
         9  Chynoweth Ave
         9  Bernal Rd
         8  S 2nd St Alleys
         8  Coyote Rd
         8  Fuller Ave
         7  McLaughlin Ave
         7  Aborn Rd

CORRIDORGROUP by dollars
       1.57M        5 rows  Coyote Creek Fields at Hwy 280
       1.36M       20 rows  Monterey Rd
       1.15M        1 rows  Basking Ridge Ave
      475.2K        9 rows  Camden Ave
      365.7K       14 rows  Bailey Ave
      325.8K        9 rows  Branham Ln
      274.5K        9 rows  Santa Teresa Blvd
      193.9K       11 rows  Zanker Rd
      183.4K        5 rows  Coleman Rd
      183.4K       21 rows  San Felipe Rd
      163.6K        7 rows  McKean Rd
      162.9K       13 rows  Old Piedmont Rd
      162.2K        4 rows  Mabury Rd
      149.6K        3 rows  Curtner Ave
      143.1K        1 rows  McKean Rd Fire Station
      133.3K        4 rows  Cropley Ave
      130.2K        5 rows  Almaden Expwy
      129.5K        8 rows  Coyote Rd
      114.2K       13 rows  Almaden Rd
      113.7K        3 rows  Los Esteros Rd

FACILITYID by rows
         1  1620
         1  1488
         1  1545
         1  1556
         1  1518
         1  1565
         1  1569
         1  1493
         1  1641
         1  1535
         1  1621
         1  1579
         1  1687
         1  1602
         1  1500
         1  1478
         1  1619
         1  1525
         1  1539
         1  1519

FACILITYID by dollars
       1.15M        1 rows  1624
      980.2K        1 rows  1496
      280.4K        1 rows  1495
      265.7K        1 rows  1763
      226.9K        1 rows  1498
      192.5K        1 rows  1740
      176.2K        1 rows  1839
      174.6K        1 rows  1835
      145.5K        1 rows  1834
      143.1K        1 rows  1598
      135.4K        1 rows  1741
      132.0K        1 rows  2016
       98.6K        1 rows  1840
       86.8K        1 rows  1633
       79.4K        1 rows  1497
       76.5K        1 rows  1778
       74.2K        1 rows  1493
       71.5K        1 rows  1841
       70.5K        1 rows  1836
       70.1K        1 rows  1842

CREATIONDATE by rows
       569  2025/04/08 19:46:58+00

CREATIONDATE by dollars
      10.32M      569 rows  2025/04/08 19:46:58+00

## who x when

SUBCORRIDORGROUP by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREASQFT
  Almaden Expwy                             2026:130.2K
  Alviso 1                                  2026:46.5K
  Bailey Ave 1                              2026:129.3K
  Basking Ridge Ave                         2026:1.15M
  Branham Ln 3                              2026:265.7K
  Camden Ave 4                              2026:192.5K
  Camden Ave 5                              2026:203.6K
  Coleman Ave                               2026:71.1K
  Coyote Creek Fields at Hwy 280            2026:1.57M
  Curtner Ave                               2026:149.6K
  Fowler Rd                                 2026:76.0K
  Hedding St 2                              2026:10.4K
  Hostetter Rd 2                            2026:6.1K
  Mabury Rd                                 2026:162.2K
  McKean Rd Fire Station                    2026:143.1K
  McLaughlin Ave                            2026:5.8K
  Monterey Rd 10                            2026:145.5K
  Monterey Rd 11                            2026:174.6K
  Monterey Rd 2                             2026:223.4K
  Monterey Rd 4                             2026:384.9K
  Old Piedmont Rd 4                         2026:25.6K
  S 2nd St Alleys                           2026:22.2K
  San Felipe Rd 3                           2026:22.0K
  San Felipe Rd 8                           2026:42.5K
  Sierra Rd 3                               2026:14.1K
  Taylor St 1                               2026:26.0K
  Vine St Alleys 1                          2026:13.7K
  Vine St Alleys 2                          2026:10.2K
  Yerba Buena Rd                            2026:23.6K
  Zanker Rd 2                               2026:82.4K

CORRIDORGROUP by INGESTED_AT  LOAD STAMP, not an event date, dollars = AREASQFT
  Aborn Rd                                  2026:62.7K
  Almaden Expwy                             2026:130.2K
  Almaden Rd                                2026:114.2K
  Bailey Ave                                2026:365.7K
  Bascom Ave                                2026:9.6K
  Basking Ridge Ave                         2026:1.15M
  Bernal Rd                                 2026:74.1K
  Branham Ln                                2026:325.8K
  Camden Ave                                2026:475.2K
  Chynoweth Ave                             2026:79.5K
  Coleman Rd                                2026:183.4K
  Coyote Creek Fields at Hwy 280            2026:1.57M
  Coyote Rd                                 2026:129.5K
  Cropley Ave                               2026:133.3K
  Curtner Ave                               2026:149.6K
  Fuller Ave                                2026:64.2K
  Los Esteros Rd                            2026:113.7K
  Mabury Rd                                 2026:162.2K
  McKean Rd                                 2026:163.6K
  McKean Rd Fire Station                    2026:143.1K
  McLaughlin Ave                            2026:5.8K
  Monterey Rd                               2026:1.36M
  Old Piedmont Rd                           2026:162.9K
  S 2nd St Alleys                           2026:22.2K
  San Felipe Rd                             2026:183.4K
  Santa Teresa Blvd                         2026:274.5K
  Sierra Rd                                 2026:101.3K
  Taylor St                                 2026:60.2K
  Vine St Alleys                            2026:23.9K
  Zanker Rd                                 2026:193.9K

## what

TYPEOFWORK: Spray 95%, Mow 5%, Handwork 1%

PARCELTYPE: Roadside 65%, Lot 13%, Alley 9%, Dirt Island 8%, Backup 4%, Median 1%, Bike Path 0%

CURRENTDATE: 2026/01/16 06:02:15+00 76%, 2026/01/16 06:02:16+00 24%

LASTWORKDATE: 2024/12/30 00:00:00+00 24%, 2025/09/25 00:00:00+00 22%, 2023/02/01 00:00:00+00 19%, 2024/06/30 00:00:00+00 14%, 2025/06/30 00:00:00+00 10%, 2024/02/25 00:00:00+00 6%, 2024/08/30 00:00:00+00 1%, 2024/07/26 00:00:00+00 1%, 2024/08/02 00:00:00+00 1%, 2024/08/23 00:00:00+00 0%, 2021/06/04 00:00:00+00 0%

LASTINSPECTIONDATE: 2025/11/17 20:00:00+00 26%, 2025/11/18 20:00:00+00 20%, 2025/03/12 19:00:00+00 8%, 2025/03/07 20:00:00+00 8%, 2025/03/13 19:00:00+00 7%, 2025/03/10 19:00:00+00 7%, 2025/03/04 20:00:00+00 6%, 2025/03/14 19:00:00+00 5%, 2025/03/05 20:00:00+00 5%, 2025/03/03 20:00:00+00 4%, 2025/03/06 20:00:00+00 4%

NOTES: Salesforce ID is duplicate 100%

DATETHREEMO: 2025/10/16 06:02:15+00 76%, 2025/10/16 06:02:16+00 24%

DATEONEYR: 2025/01/16 06:02:15+00 76%, 2025/01/16 06:02:16+00 24%

DATETWOMONTHS: 2025/11/16 06:02:15+00 76%, 2025/11/16 06:02:16+00 24%

WILDFIRERISK: No 75%, Yes 25%

COUNCILDISTRICT: 3 17%, 2 16%, 6 15%, 4 14%, 7 8%, 8 8%, 10 6%, 5 6%, 1 5%, 9 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 569 | 0 | 2040 3; 2039 3; 2038 3; 2037 3 |
| FACILITYID | who | 569 | 0 | 2040 3; 2039 3; 2038 3; 2037 3 |
| INTID | other | 569 | 0 | 2040 3; 2039 3; 2038 3; 2037 3 |
| SALESFORCEID | other | 572 | 0 | a0qPl000007ZyJyIAK 3; a0qPl000007ZyJxIAK 3; a0qPl000007ZysuIAC 3; a0qj0000003aGOUAA2 3 |
| PARCELID | other | 579 | 0 | 2040 3; 2039 3; 2038 3; B57515013 3 |
| TYPEOFWORK | category | 3 | 0 | Spray 538; Mow 28; Handwork 3 |
| LOCATION | other | 345 | 0 | San Felipe RD & Park Esta 20; Monterey Hw. W/side bet.  14; Bet. Almaden & Vine - Wil 13; Bailey Rd. B/sides bet. S 12 |
| PARCELTYPE | category | 7 | 0 | Roadside 371; Lot 76; Alley 49; Dirt Island 45 |
| AREASQFT | amount | 574 | 0 | 2471.11878401 3; 4774.417135 3; 552.04439477 3; 1892.64551866 3 |
| CURRENTDATE | category | 2 | 0 | 2026/01/16 06:02:15+00 431; 2026/01/16 06:02:16+00 138 |
| LASTWORKDATE | category | 26 | 5 | 2024/12/30 00:00:00+00 132; 2025/09/25 00:00:00+00 123; 2023/02/01 00:00:00+00 103; 2024/06/30 00:00:00+00 78 |
| LASTINSPECTIONDATE | category | 19 | 18 | 2025/11/17 20:00:00+00 131; 2025/11/18 20:00:00+00 102; 2025/03/12 19:00:00+00 43; 2025/03/07 20:00:00+00 39 |
| CREATIONDATE | who | 1 | 0 | 2025/04/08 19:46:58+00 569 |
| LASTUPDATE | who | 1 | 0 | 2026/01/16 14:02:22+00 569 |
| NOTES | category | 2 | 383 | Salesforce ID is duplicat 186 |
| DATETHREEMO | category | 2 | 0 | 2025/10/16 06:02:15+00 431; 2025/10/16 06:02:16+00 138 |
| DATEONEYR | category | 2 | 0 | 2025/01/16 06:02:15+00 431; 2025/01/16 06:02:16+00 138 |
| SHAPE_LENGTH | amount | 570 | 0 | 385.130757605861 3; 787.049855411362 3; 559.810356849365 3; 473.193277761959 3 |
| SHAPE_AREA | amount | 574 | 0 | 2471.11878400826 3; 4774.417134996 3; 552.04439477423 3; 1892.64551866405 3 |
| DATETWOMONTHS | category | 2 | 0 | 2025/11/16 06:02:15+00 431; 2025/11/16 06:02:16+00 138 |
| WILDFIRERISK | category | 2 | 0 | No 424; Yes 145 |
| GEOMETRYNOTES | who | 1 | 0 | Updated with 2024 satelli 569 |
| CORRIDORGROUP | who | 184 | 0 | San Felipe Rd 21; Monterey Rd 20; Bailey Ave 14; Vine St Alleys 14 |
| SUBCORRIDORGROUP | who | 274 | 0 | Vine St Alleys 2 9; S 2nd St Alleys 9; Bailey Ave 1 8; Monterey Rd 4 8 |
| COUNCILDISTRICT | category | 10 | 0 | 3 98; 2 92; 6 83; 4 79 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:42:57.63167 569 |
| SOURCE_RUN_ID | audit | 1 | 0 | 8e1350ee-cf1e-4b99-8005-a 569 |
| SRC_SHA256 | who | 1 | 0 | 1d3871e94817d2cfc4251f557 569 |
