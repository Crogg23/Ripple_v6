# PORTAL_CKA_SAN_JOSE_OPEN_DA_5C575BFEB9

rows 94  columns 15  scan 5.8s

roles: amount 2, audit 2, category 4, date 1, other 2, who 5

## when

INGESTED_AT
  2026        94  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 94 | 6.11M | 6.15M | 6.22M | 6.22M | 578.17M |
| Y | 94 | 1.88M | 1.94M | 1.98M | 1.99M | 182.73M |

## who

INTNAME by rows
         2  E Gish Rd
         2  Oakland Rd
         2  Winchester Blvd
         2  E Brokaw Rd
         2  N 10th St
         2  Auzerais Ave
         2  Old Bayshore Hwy
         1  Stevens Creek Blvd
         1  N 7th St
         1  Tilton Ave
         1  N 1st St
         1  Fruitdale Ave
         1  E Hamilton Ave
         1  Bubb Rd
         1  Kennedy Ave
         1  Queens Ln
         1  Horning St
         1  Santa Teresa LRT Station
         1  Civic Center Dr
         1  Catherine St

INTNAME by dollars
      12.31M        2 rows  Oakland Rd
      12.31M        2 rows  N 10th St
      12.31M        2 rows  E Gish Rd
      12.31M        2 rows  Old Bayshore Hwy
      12.31M        2 rows  E Brokaw Rd
      12.31M        2 rows  Auzerais Ave
      12.27M        2 rows  Winchester Blvd
       6.22M        1 rows  Tilton Ave
       6.22M        1 rows  Live Oak Ave
       6.21M        1 rows  Palm Ave
       6.20M        1 rows  Blanchard Rd
       6.19M        1 rows  Santa Teresa LRT Station
       6.18M        1 rows  Chynoweth Ave
       6.18M        1 rows  Branham Ln
       6.17M        1 rows  Skyway Dr
       6.16M        1 rows  Monterey Rd
       6.16M        1 rows  Winfield Blvd
       6.16M        1 rows  Phelan Ave
       6.16M        1 rows  Blossom River Way
       6.16M        1 rows  Blossom Hill Rd

STATUS by rows
        94  Active

STATUS by dollars
     578.17M       94 rows  Active

FACILITYID by rows
         1  260
         1  139
         1  179
         1  289
         1  261
         1  279
         1  287
         1  151
         1  145
         1  157
         1  168
         1  167
         1  148
         1  180
         1  149
         1  138
         1  227
         1  263
         1  177
         1  189

FACILITYID by dollars
       6.22M        1 rows  300
       6.22M        1 rows  299
       6.21M        1 rows  298
       6.20M        1 rows  297
       6.19M        1 rows  293
       6.18M        1 rows  296
       6.18M        1 rows  295
       6.17M        1 rows  294
       6.16M        1 rows  189
       6.16M        1 rows  290
       6.16M        1 rows  192
       6.16M        1 rows  291
       6.16M        1 rows  292
       6.16M        1 rows  190
       6.16M        1 rows  247
       6.16M        1 rows  191
       6.16M        1 rows  302
       6.16M        1 rows  301
       6.16M        1 rows  159
       6.16M        1 rows  158

CREATIONDATE by rows
        94  1900/01/01 00:00:00+00

CREATIONDATE by dollars
     578.17M       94 rows  1900/01/01 00:00:00+00

## who x when

INTNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  Auzerais Ave                              2026:12.31M
  Blanchard Rd                              2026:6.20M
  Blossom River Way                         2026:6.16M
  Branham Ln                                2026:6.18M
  Bubb Rd                                   2026:6.11M
  Catherine St                              2026:6.13M
  Chynoweth Ave                             2026:6.18M
  Civic Center Dr                           2026:6.14M
  E Brokaw Rd                               2026:12.31M
  E Gish Rd                                 2026:12.31M
  E Hamilton Ave                            2026:6.14M
  Fruitdale Ave                             2026:6.15M
  Horning St                                2026:6.16M
  Kennedy Ave                               2026:6.14M
  Live Oak Ave                              2026:6.22M
  Monterey Rd                               2026:6.16M
  N 10th St                                 2026:12.31M
  N 1st St                                  2026:6.16M
  N 7th St                                  2026:6.16M
  Oakland Rd                                2026:12.31M
  Old Bayshore Hwy                          2026:12.31M
  Palm Ave                                  2026:6.21M
  Phelan Ave                                2026:6.16M
  Queens Ln                                 2026:6.15M
  Santa Teresa LRT Station                  2026:6.19M
  Skyway Dr                                 2026:6.17M
  Stevens Creek Blvd                        2026:6.11M
  Tilton Ave                                2026:6.22M
  Winchester Blvd                           2026:12.27M
  Winfield Blvd                             2026:6.16M

STATUS by INGESTED_AT  LOAD STAMP, not an event date, dollars = X
  Active                                    2026:578.17M

## what

PUCID: Unk 81%, E 50.80-C 2%, E 49.60-C C 2%, E 49.90-C C 2%, E 50.40-C C 2%, L 49.71 2%, L 49.70 2%, L 49.40 2%, L 48.90 2%, L 48.60 2%, L 48.00 2%, L 47.90 2%

LASTUPDATE: 2019/11/16 00:21:26+00 85%, 2019/11/16 00:21:27+00 14%, 2019/11/16 00:22:21+00 1%

NAME: Union Pacific 93%, Light Rail 7%

RAILTYPE: Rail 93%, Lightrail 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 94 | 0 | 6150670.44219425 1; 6158823.19327717 1; 6157403.06324342 1; 6218802.63729441 1 |
| Y | amount | 93 | 0 | 1991600.88653798 1; 1976043.84612982 1; 1975628.32202648 1; 1881053.97967948 1 |
| OBJECTID | other | 95 | 0 | 175 1; 174 1; 173 1; 172 1 |
| FACILITYID | who | 94 | 0 | 303 1; 302 1; 301 1; 300 1 |
| INTID | other | 94 | 0 | 303 1; 302 1; 301 1; 300 1 |
| PUCID | category | 47 | 0 | Unk 47; E 50.80-C 1; E 49.60-C C 1; E 49.90-C C 1 |
| LASTUPDATE | category | 3 | 0 | 2019/11/16 00:21:26+00 80; 2019/11/16 00:21:27+00 13; 2019/11/16 00:22:21+00 1 |
| INTNAME | who | 87 | 0 | Winchester Blvd 2; E Brokaw Rd 2; Auzerais Ave 2; N 10th St 2 |
| NAME | category | 2 | 0 | Union Pacific 87; Light Rail 7 |
| RAILTYPE | category | 2 | 0 | Rail 87; Lightrail 7 |
| STATUS | who | 1 | 0 | Active 94 |
| CREATIONDATE | who | 1 | 0 | 1900/01/01 00:00:00+00 94 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:14:56.33168 94 |
| SOURCE_RUN_ID | audit | 1 | 0 | 72850d1b-3d44-40c1-8d4a-d 94 |
| SRC_SHA256 | who | 1 | 0 | b10938041e5100baaf6c0b94a 94 |
