# PORTAL_CKA_SAN_JOSE_OPEN_DA_D8576CBEB1

rows 786  columns 21  scan 4.7s

roles: amount 1, audit 2, category 8, date 1, empty 2, other 3, who 5

## when

INGESTED_AT
  2026       786  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE_LENGTH | 786 | 34.97 | 307.59 | 1.3K | 1.9K | 325.9K |

## who

STREETNAME by rows
        42  E William St
        37  E Reed St
        30  Margaret St
        27  Eden Ave
        26  E San Fernando St
        25  W San Fernando St
        23  E St John St
        22  E San Carlos St
        20  S 12th St
        18  E Santa Clara St
        18  E St James St
        17  Lexington Dr
        14  Laurel Grove Ln
        14  Auzerais Ave
        11  S 17th St
        11  Park Ave
        11  Valley Forge Way
        11  Payne Ave
        11  Cape Buffalo Dr
        10  S 14th St

STREETNAME by dollars
       18.0K       42 rows  E William St
       14.7K       37 rows  E Reed St
       13.1K       30 rows  Margaret St
       11.3K       27 rows  Eden Ave
       10.5K       26 rows  E San Fernando St
       10.1K       17 rows  Lexington Dr
        9.1K       20 rows  S 12th St
        9.0K       23 rows  E St John St
        8.7K       22 rows  E San Carlos St
        7.3K       18 rows  E Santa Clara St
        7.0K       18 rows  E St James St
        5.5K       25 rows  W San Fernando St
        5.0K       10 rows  S 13th St
        4.9K       11 rows  S 17th St
        4.5K        7 rows  Cadillac Dr
        4.4K       10 rows  S 14th St
        4.0K        7 rows  S 15th St
        3.9K        6 rows  Opal Dr
        3.9K       14 rows  Auzerais Ave
        3.9K        9 rows  Mesa Dr

STATUS by rows
       786  ACTIVE

STATUS by dollars
      325.9K      786 rows  ACTIVE

FACILITYID by rows
         1  5244
         1  5204
         1  5217
         1  5337
         1  5277
         1  5338
         1  5343
         1  5379
         1  5345
         1  5383
         1  5302
         1  5384
         1  5355
         1  5234
         1  5230
         1  5182
         1  5421
         1  5330
         1  5257
         1  5232

FACILITYID by dollars
        1.9K        1 rows  5179
        1.9K        1 rows  5180
        1.5K        1 rows  5648
        1.5K        1 rows  5641
        1.4K        1 rows  5220
        1.3K        1 rows  5227
        1.3K        1 rows  5639
        1.3K        1 rows  5640
        1.3K        1 rows  5642
        1.3K        1 rows  5643
        1.2K        1 rows  5293
        1.2K        1 rows  5291
        1.2K        1 rows  5417
        1.2K        1 rows  5644
        1.2K        1 rows  5645
        1.2K        1 rows  5694
        1.2K        1 rows  5655
        1.1K        1 rows  5692
        1.1K        1 rows  5661
        1.1K        1 rows  5611

LASTUPDATE by rows
        13  2023/02/23 23:18:59+00
        12  2023/02/23 23:18:57+00
        12  2023/02/23 23:19:02+00
        12  2023/02/23 23:21:21+00
        12  2023/02/23 23:18:58+00
        12  2023/02/23 23:19:05+00
        12  2023/02/23 23:19:00+00
        12  2023/02/23 23:19:03+00
        12  2023/02/23 23:21:22+00
        12  2023/02/23 23:18:56+00
        11  2023/02/23 23:20:40+00
        11  2023/02/23 23:20:44+00
        11  2023/02/23 23:19:04+00
        11  2023/02/23 23:21:23+00
        11  2023/02/23 23:20:49+00
        11  2023/02/23 23:21:24+00
        11  2023/02/23 23:22:27+00
        11  2023/02/23 23:20:39+00
        11  2023/02/23 23:21:29+00
        11  2023/02/23 23:20:45+00

LASTUPDATE by dollars
        8.3K        9 rows  2023/02/23 23:21:14+00
        8.1K       12 rows  2023/02/23 23:18:56+00
        8.0K       13 rows  2023/02/23 23:18:59+00
        6.6K       12 rows  2023/02/23 23:21:21+00
        6.5K        9 rows  2023/02/23 23:21:15+00
        6.3K       12 rows  2023/02/23 23:19:05+00
        6.1K       12 rows  2023/02/23 23:21:22+00
        6.0K        8 rows  2023/02/23 23:21:35+00
        5.7K       12 rows  2023/02/23 23:19:03+00
        5.2K       10 rows  2023/02/23 23:20:41+00
        5.1K       12 rows  2023/02/23 23:19:02+00
        5.1K        9 rows  2023/02/23 23:21:11+00
        5.0K        9 rows  2023/02/23 23:21:20+00
        4.9K       11 rows  2023/02/23 23:20:44+00
        4.9K       11 rows  2023/02/23 23:20:40+00
        4.8K       10 rows  2023/02/23 23:20:37+00
        4.7K       10 rows  2023/02/23 23:21:10+00
        4.7K       10 rows  2023/02/23 23:20:38+00
        4.6K       11 rows  2023/02/23 23:20:49+00
        4.5K       11 rows  2023/02/23 23:21:23+00

## who x when

STREETNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  Auzerais Ave                              2026:3.9K
  Cadillac Dr                               2026:4.5K
  Cape Buffalo Dr                           2026:3.0K
  E Reed St                                 2026:14.7K
  E San Carlos St                           2026:8.7K
  E San Fernando St                         2026:10.5K
  E Santa Clara St                          2026:7.3K
  E St James St                             2026:7.0K
  E St John St                              2026:9.0K
  E William St                              2026:18.0K
  Eden Ave                                  2026:11.3K
  Laurel Grove Ln                           2026:2.2K
  Lexington Dr                              2026:10.1K
  Margaret St                               2026:13.1K
  Mesa Dr                                   2026:3.9K
  Opal Dr                                   2026:3.9K
  Park Ave                                  2026:2.6K
  Payne Ave                                 2026:3.4K
  S 12th St                                 2026:9.1K
  S 13th St                                 2026:5.0K
  S 14th St                                 2026:4.4K
  S 15th St                                 2026:4.0K
  S 17th St                                 2026:4.9K
  Valley Forge Way                          2026:2.2K
  W San Fernando St                         2026:5.5K

STATUS by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  ACTIVE                                    2026:325.9K

## what

ZONEID: 14 22%, 13 14%, 8 14%, 17 9%, 12 7%, 18 6%, 2 6%, 22 5%, 5 5%, 6 4%, 10 4%, 20 3%

ZONENAME: University 22%, SUN 14%, Horace Mann 14%, Cadillac 9%, St. Leo's 7%, Lynhaven 6%, Berryessa 6%, Eden 5%, College Park 5%, Delmas Park 4%, Parkside 4%, Via Monte 3%

STICKERLIMIT: Unlimited 49%, 3 24%, 0 15%, 1 10%, 4 2%

HANGERLIMIT: 2 88%, 1 12%

EXPIRATIONDATE: August 31st of every ODD year 21%, July 31st of EVERY year 14%, September 30th of EVERY year 13%, February 28th/29th of every EV 11%, December 31st of every ODD yea 10%, January 31st of every ODD year 7%, March 31st of every EVEN year 7%, February 28th of every ODD yea 7%, August 31st of every EVEN year 5%, March 31st of every ODD year 4%, October 31st of every EVEN yea 2%

RESIDENTIALID: 537 26%, 942 17%, 0 17%, 573 8%, 600 7%, 771 6%, 857 5%, 598 4%, 854 4%, 570 3%, 532 2%

ZONEAPPLICATION: https://www.sanjoseca.gov/home 89%, https://www.sanjoseca.gov/home 11%

ALTERNATEZONEID: 20 23%, 19 15%, 12 15%, 4 10%, 18 7%, 13 6%, 3 6%, 8 6%, 9 4%, 15 4%, 21 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ZONEID | category | 22 | 0 | 14 148; 13 97; 8 95; 17 62 |
| ZONENAME | category | 21 | 0 | University 148; SUN 97; Horace Mann 95; Cadillac 62 |
| ZONETYPE | other | 1 | 0 | RPP 786 |
| STATUS | who | 1 | 0 | ACTIVE 786 |
| STICKERLIMIT | category | 5 | 0 | Unlimited 387; 3 192; 0 118; 1 76 |
| HANGERLIMIT | category | 2 | 0 | 2 695; 1 91 |
| EXPIRATIONDATE | category | 17 | 36 | August 31st of every ODD  148; July 31st of EVERY year 97; September 30th of EVERY y 95; February 28th/29th of eve 78 |
| STREETNAME | who | 134 | 0 | E William St 42; E Reed St 37; Margaret St 30; Eden Ave 27 |
| SHAPE_LENGTH | amount | 785 | 0 | 254.118490880664 5; 301.31167502146 4; 889.332744039963 4; 222.373299408511 4 |
| OBJECTID | other | 782 | 0 | 3951 4; 3950 4; 3949 4; 3948 4 |
| FACILITYID | who | 780 | 0 | 5964 4; 5963 4; 5962 4; 5961 4 |
| INTID | other | 780 | 0 | 5964 4; 5963 4; 5962 4; 5961 4 |
| RESIDENTIALID | category | 17 | 171 | 537 148; 942 97; 0 95; 573 46 |
| ZONEAPPLICATION | category | 2 | 0 | https://www.sanjoseca.gov 703; https://www.sanjoseca.gov 83 |
| ALTERNATEZONEID | category | 22 | 36 | 20 148; 19 97; 12 95; 4 62 |
| CREATIONDATE | empty | 1 | 786 |  |
| LASTUPDATE | who | 147 | 0 | 2023/02/23 23:18:59+00 13; 2023/02/23 23:21:22+00 12; 2023/02/23 23:21:21+00 12; 2023/02/23 23:19:05+00 12 |
| NOTES | empty | 1 | 786 |  |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:47:04.59156 786 |
| SOURCE_RUN_ID | audit | 1 | 0 | 21654d79-fee2-4c83-8a83-6 786 |
| SRC_SHA256 | who | 1 | 0 | 91c0fcf7d703cd63046fc4f5c 786 |
