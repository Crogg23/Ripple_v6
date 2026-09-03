# XC_VERA_INCARCERATION_TRENDS

rows 128.5K  columns 167  scan 7.9s

roles: amount 81, audit 2, category 6, other 76, state 1, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LAND_AREA | 128.5K | 2.05 | 598.15 | 6.5K | 20.1K | 118.96M |
| TOTAL_JAIL_POP | 97.9K | 0 | 66 | 3.1K | 23.5K | 23.99M |
| NATIVE_JAIL_POP | 88.4K | 0 | 0 | 50.40 | 966.13 | 260.5K |
| AAPI_JAIL_POP | 88.4K | 0 | 0 | 43.85 | 862.36 | 207.6K |
| OTHER_RACE_JAIL_POP | 73.5K | 0 | 0 | 83.13 | 1.6K | 278.5K |
| TOTAL_PRETRIAL_CUSTODY | 93.6K | 0 | 32.61 | 2.0K | 13.5K | 13.92M |

## who

COUNTY_NAME by rows
      1.2K  Washington County
      1.0K  Jefferson County
       957  Jackson County
       914  Franklin County
       911  Lincoln County
       795  Madison County
       740  Clay County
       739  Montgomery County
       713  Marion County
       710  Monroe County
       683  Union County
       669  Wayne County
       594  Warren County
       577  Greene County
       559  Grant County
       540  Douglas County
       530  Carroll County
       525  Johnson County
       524  Polk County
       512  Lee County

COUNTY_NAME by dollars
      772.8K       45 rows  Los Angeles County
      388.8K      312 rows  Orange County
      359.0K      103 rows  Harris County
      345.8K      138 rows  Cook County
      270.9K      187 rows  Dallas County
      268.2K       43 rows  Maricopa County
      268.0K     1.0K rows  Jefferson County
      242.8K       44 rows  Philadelphia County
      228.2K       45 rows  Miami-Dade County
      220.9K      739 rows  Montgomery County
      218.8K       45 rows  San Diego County
      218.0K      375 rows  Shelby County
      203.5K      479 rows  Clark County
      187.9K       45 rows  San Bernardino County
      183.8K      713 rows  Marion County
      183.1K       90 rows  Kings County
      178.0K       45 rows  Broward County
      170.9K      335 rows  Fulton County
      161.5K       45 rows  Santa Clara County
      150.4K       45 rows  Queens County

## where

STATE_ABBR: TX 11.8K, GA 9.0K, KY 5.4K, VA 5.4K, MO 4.6K, NC 4.4K, TN 4.3K, IL 4.2K, NE 3.9K, OH 3.8K, MN 3.6K, IA 3.6K

## what

STATE_FIPS: 48 18%, 13 14%, 21 8%, 51 8%, 29 7%, 37 7%, 47 7%, 17 7%, 31 6%, 39 6%, 27 6%, 19 6%

STATE_CODE: US_TX 18%, US_GA 14%, US_KY 8%, US_VA 8%, US_MO 7%, US_NC 7%, US_TN 7%, US_IL 7%, US_NE 6%, US_OH 6%, US_MN 6%, US_IA 6%

URBANICITY: rural 62%, small/mid 24%, suburban 12%, urban 2%

REGION: South 49%, Midwest 32%, West 12%, Northeast 7%

DIVISION: South Atlantic 21%, West North Central 21%, West South Central 15%, East South Central 12%, East North Central 11%, Mountain 7%, Middle Atlantic 6%, Pacific 5%, New England 1%

IS_REGIONAL_JAIL: false 85%, true 15%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| YEAR | other | 57 | 0 | 2014 3.1K; 2011 3.0K; 2012 3.0K; 2004 3.0K |
| COUNTY_FIPS | other | 3.1K | 0 | 27125 439; 27149 439; 27041 439; 27101 439 |
| COUNTY_NAME | who | 1.9K | 0 | Washington County 1.2K; Jefferson County 1.0K; Jackson County 974; Lincoln County 915 |
| STATE_ABBR | state | 45 | 0 | TX 11.8K; GA 9.0K; KY 5.4K; VA 5.4K |
| STATE_FIPS | category | 45 | 0 | 48 11.8K; 13 9.0K; 21 5.4K; 51 5.4K |
| STATE_CODE | category | 45 | 0 | US_TX 11.8K; US_GA 9.0K; US_KY 5.4K; US_VA 5.4K |
| COUNTY_CODE | other | 3.1K | 0 | US_MD_BALTIMORE 456; US_MO_ST._LOUIS 455; US_MN_RED_LAKE 439; US_MN_POPE 439 |
| URBANICITY | category | 4 | 0 | rural 79.4K; small/mid 30.5K; suburban 15.6K; urban 2.9K |
| REGION | category | 4 | 0 | South 62.5K; Midwest 41.7K; West 16.0K; Northeast 8.4K |
| DIVISION | category | 9 | 0 | South Atlantic 27.2K; West North Central 27.1K; West South Central 19.5K; East South Central 15.8K |
| METRO_AREA | other | 900 | 53.2K | 12060 1.7K; 35620 1.1K; 47900 1.1K; 33460 820 |
| COMMUTING_ZONE | other | 677 | 43 | 141 1.1K; 89 887; 74 873; 39 870 |
| LAND_AREA | amount | 3.0K | 0 | 432.407 439; 563.612 439; 636.76 439; 704.7 439 |
| TOTAL_JAIL_POP | amount | 16.5K | 30.6K | 1 1.2K; 4 1.2K; 5 1.1K; 2 1.1K |
| MALE_JAIL_POP | other | 23.8K | 34.9K | 0 1.5K; 5 1.1K; 1 1.1K; 4 1.1K |
| FEMALE_JAIL_POP | other | 13.3K | 34.9K | 0 13.3K; 1 4.8K; 2 3.7K; 3 2.8K |
| BLACK_JAIL_POP | other | 20.8K | 39.3K | 0 13.5K; 1 1.9K; 2 1.4K; 3 960 |
| BLACK_MALE_JAIL_POP | other | 291 | 127.9K | 2 24; 1 22; 4 20; 5 19 |
| BLACK_FEMALE_JAIL_POP | other | 110 | 127.9K | 0 181; 1 65; 2 45; 3 35 |
| LATINX_JAIL_POP | other | 13.3K | 39.5K | 0 22.9K; 1 2.7K; 2 1.9K; 3 1.3K |
| LATINX_MALE_JAIL_POP | other | 186 | 127.9K | 0 122; 1 78; 2 50; 3 25 |
| LATINX_FEMALE_JAIL_POP | other | 58 | 127.9K | 0 351; 1 65; 2 37; 3 21 |
| WHITE_JAIL_POP | other | 24.7K | 39.1K | 0 1.1K; 2 917; 4 902; 3 875 |
| WHITE_MALE_JAIL_POP | other | 360 | 127.9K | 48 7; 98 7; 93 6; 52 6 |
| WHITE_FEMALE_JAIL_POP | other | 182 | 127.9K | 0 47; 11 14; 18 14; 35 13 |
| NATIVE_JAIL_POP | amount | 5.4K | 40.1K | 0 55.4K; 1 2.5K; 2 1.1K; 3 622 |
| AAPI_JAIL_POP | amount | 5.3K | 40.1K | 0 60.3K; 1 2.1K; 2 1.0K; 3 573 |
| OTHER_RACE_JAIL_POP | amount | 4.1K | 55.0K | 0 63.2K; 1 384; 2 267; 3 160 |
| TOTAL_PRETRIAL_CUSTODY | amount | 20.7K | 34.9K | 0 3.9K; 1 1.7K; 2 1.6K; 3 1.4K |
| TOTAL_PRETRIAL_JURIS | amount | 208 | 127.2K | 0 670; 1 43; 0.5 37; 0.25 35 |
| TOTAL_JAIL_FROM_FED | amount | 6.0K | 38.6K | 0 50.9K; 1 2.3K; 2 1.3K; 3 864 |
| TOTAL_JAIL_FROM_PRISON | amount | 8.9K | 39.4K | 0 34.2K; 1 2.5K; 2 1.8K; 3 1.4K |
| TOTAL_JAIL_FROM_OTHER_JAIL | amount | 5.0K | 42.0K | 0 43.5K; 1 2.9K; 2 2.0K; 3 1.4K |
| TOTAL_JAIL_FROM_BIA | amount | 483 | 50.5K | 0 76.3K; 1 119; 2 75; 3 50 |
| TOTAL_JAIL_FROM_BOP | amount | 1.3K | 57.6K | 0 63.8K; 1 605; 2 359; 3 231 |
| TOTAL_JAIL_FROM_ICE | amount | 3.0K | 47.7K | 0 61.0K; 1 1.7K; 2 991; 3 603 |
| TOTAL_JAIL_FROM_MARSHALS | amount | 4.9K | 50.5K | 0 52.3K; 1 1.2K; 2 667; 3 420 |
| TOTAL_JAIL_FROM_OTHER_FED | amount | 1.1K | 47.5K | 0 76.5K; 1 403; 2 232; 3 144 |
| TOTAL_CONTRACTED_OUT | amount | 291 | 126.4K | 0 1.3K; 1 39; 2 33; 0.25 27 |
| TOTAL_CONTRACTED_IN | amount | 938 | 122.9K | 0 3.0K; 1 116; 2 63; 0.25 63 |
| TOTAL_JAIL_ADMITS | amount | 34.3K | 40.4K | 0 526; 65 525; 130 482; 13 470 |
| MALE_JAIL_ADMITS | amount | 29.1K | 69.1K | 0 1.6K; 250 305; 75 295; 150 294 |
| FEMALE_JAIL_ADMITS | amount | 19.8K | 69.1K | 0 2.1K; 75 312; 50 310; 10 298 |
| TOTAL_JAIL_DISCHARGES | amount | 44.9K | 43.6K | 65 557; 26 514; 39 509; 130 484 |
| MALE_JAIL_DISCHARGES | amount | 41.9K | 75.8K | 87.23 265; 27.53 180; 22.43 180; 21.08 179 |
| FEMALE_JAIL_DISCHARGES | amount | 30.3K | 75.8K | 0 1.1K; 59.91 261; 11.47 178; 3.57 178 |
| JAIL_RATED_CAPACITY | other | 17.2K | 34.4K | 12 1.0K; 8 923; 10 899; 16 862 |
| TOTAL_SENTENCED_CUSTODY | amount | 22.3K | 40.3K | 1 1.7K; 2 1.6K; 3 1.5K; 4 1.3K |
| IS_REGIONAL_JAIL | category | 2 | 0 | false 109.4K; true 19.1K |
| IS_UNIFIED_STATE | other | 1 | 0 | false 128.5K |
| TOTAL_PRISON_POP | amount | 4.2K | 37.9K | 0 1.8K; 4 1.4K; 6 1.2K; 5 1.2K |
| FEMALE_PRISON_POP | other | 871 | 70.0K | 0 12.3K; 4 3.9K; 5 3.4K; 6 2.9K |
| MALE_PRISON_POP | other | 4.0K | 69.0K | 0 1.3K; 4 833; 5 733; 6 710 |
| BLACK_PRISON_POP | other | 2.8K | 81.9K | 0 7.0K; 4 1.1K; 5 978; 6 882 |
| BLACK_MALE_PRISON_POP | other | 2.5K | 98.1K | 0 2.1K; 4 681; 5 618; 6 582 |
| BLACK_FEMALE_PRISON_POP | other | 556 | 99.5K | 0 6.0K; 1 3.5K; 2 2.7K; 3 2.1K |
| LATINX_PRISON_POP | other | 1.6K | 91.6K | 0 15.0K; 4 1.4K; 5 1.1K; 6 936 |
| LATINX_MALE_PRISON_POP | other | 1.4K | 105.5K | 0 5.7K; 4 981; 5 857; 6 709 |
| LATINX_FEMALE_PRISON_POP | other | 413 | 107.0K | 0 10.1K; 1 3.3K; 2 1.7K; 3 1.1K |
| WHITE_PRISON_POP | other | 2.1K | 69.0K | 0 1.4K; 4 1.1K; 5 987; 6 919 |
| WHITE_MALE_PRISON_POP | other | 2.0K | 89.8K | 4 458; 0 440; 5 382; 6 357 |
| WHITE_FEMALE_PRISON_POP | other | 534 | 90.7K | 0 3.6K; 4 2.6K; 5 2.2K; 6 1.9K |
| NATIVE_PRISON_POP | other | 426 | 100.8K | 0 18.8K; 4 898; 5 729; 6 580 |
| NATIVE_MALE_PRISON_POP | other | 384 | 113.6K | 0 7.8K; 4 626; 5 518; 6 466 |
| NATIVE_FEMALE_PRISON_POP | other | 122 | 114.0K | 0 9.4K; 1 1.5K; 2 941; 3 609 |
| AAPI_PRISON_POP | other | 338 | 115.0K | 0 10.1K; 4 403; 5 282; 6 242 |
| AAPI_MALE_PRISON_POP | other | 322 | 116.3K | 0 8.7K; 4 357; 5 293; 6 245 |
| AAPI_FEMALE_PRISON_POP | other | 123 | 116.7K | 0 9.8K; 1 859; 2 354; 3 190 |
| OTHER_RACE_PRISON_POP | other | 566 | 101.7K | 0 19.1K; 4 1.8K; 5 1.1K; 6 675 |
| OTHER_RACE_MALE_PRISON_POP | other | 512 | 115.5K | 0 8.5K; 4 509; 5 360; 6 280 |
| OTHER_RACE_FEMALE_PRISON_POP | other | 189 | 115.8K | 0 9.7K; 1 1.1K; 2 540; 3 301 |
| TOTAL_PRISON_ADMITS | amount | 2.9K | 39.2K | 0 3.1K; 4 2.3K; 6 2.2K; 5 2.2K |
| MALE_PRISON_ADMITS | other | 2.6K | 72.7K | 0 2.2K; 4 1.3K; 5 1.2K; 6 1.1K |
| FEMALE_PRISON_ADMITS | other | 819 | 73.6K | 0 13.8K; 4 3.9K; 5 3.2K; 6 2.6K |
| BLACK_PRISON_ADMITS | other | 1.9K | 85.4K | 0 9.3K; 4 1.4K; 5 1.1K; 6 955 |
| BLACK_MALE_PRISON_ADMITS | other | 1.6K | 102.7K | 0 3.2K; 4 820; 5 679; 6 636 |
| BLACK_FEMALE_PRISON_ADMITS | other | 471 | 103.7K | 0 6.4K; 1 2.9K; 2 2.3K; 3 1.9K |
| LATINX_PRISON_ADMITS | other | 1.2K | 94.3K | 0 18.8K; 4 1.2K; 5 984; 6 743 |
| LATINX_MALE_PRISON_ADMITS | other | 1.1K | 109.2K | 0 7.3K; 4 812; 5 684; 6 546 |
| LATINX_FEMALE_PRISON_ADMITS | other | 408 | 109.9K | 0 10.1K; 1 2.3K; 2 1.4K; 3 819 |
| WHITE_PRISON_ADMITS | other | 1.4K | 72.8K | 0 2.6K; 4 1.6K; 5 1.4K; 6 1.3K |
| WHITE_MALE_PRISON_ADMITS | other | 1.2K | 94.3K | 0 934; 4 583; 5 542; 6 526 |
| WHITE_FEMALE_PRISON_ADMITS | other | 507 | 95.1K | 0 4.2K; 4 2.3K; 5 2.1K; 6 1.7K |
| NATIVE_PRISON_ADMITS | other | 316 | 100.3K | 0 22.4K; 4 666; 5 488; 6 405 |
| NATIVE_MALE_PRISON_ADMITS | other | 276 | 114.5K | 0 9.5K; 4 411; 5 331; 6 266 |
| NATIVE_FEMALE_PRISON_ADMITS | other | 97 | 114.7K | 0 10.3K; 1 887; 2 613; 3 421 |
| AAPI_PRISON_ADMITS | other | 247 | 114.1K | 0 12.5K; 4 252; 5 201; 6 159 |
| AAPI_MALE_PRISON_ADMITS | other | 244 | 116.4K | 0 10.3K; 4 240; 5 191; 6 145 |
| AAPI_FEMALE_PRISON_ADMITS | other | 88 | 116.5K | 0 10.9K; 1 432; 2 234; 3 106 |
| OTHER_RACE_PRISON_ADMITS | other | 463 | 100.7K | 0 22.0K; 4 1.6K; 5 909; 6 563 |
| OTHER_RACE_MALE_PRISON_ADMITS | other | 413 | 115.7K | 0 9.9K; 4 364; 5 276; 6 221 |
| OTHER_RACE_FEMALE_PRISON_ADMITS | other | 185 | 115.9K | 0 10.7K; 1 635; 2 344; 3 176 |
| TOTAL_POP_15TO64 | amount | 61.3K | 1.7K | 9191 636; 6503 636; 3108 425; 20403 425 |
| MALE_POP_15TO64 | other | 45.2K | 1.7K | 4822 638; 3251 637; 1426 637; 1566 425 |
| FEMALE_POP_15TO64 | other | 46.0K | 1.7K | 3253 637; 1297 637; 4164 637; 5125 636 |
| BLACK_POP_15TO64 | other | 19.7K | 32.2K | 1 1.3K; 2 1.1K; 3 875; 0 872 |
| BLACK_MALE_POP_15TO64 | other | 14.7K | 33.7K | 1 1.7K; 2 1.3K; 4 1.2K; 3 1.1K |
| BLACK_FEMALE_POP_15TO64 | other | 14.6K | 35.6K | 1 2.3K; 2 2.0K; 3 1.7K; 4 1.3K |
| LATINX_POP_15TO64 | other | 17.4K | 30.0K | 2 547; 4 535; 8 516; 5 502 |
| LATINX_MALE_POP_15TO64 | other | 13.3K | 30.6K | 1 725; 2 648; 9 625; 8 617 |
| LATINX_FEMALE_POP_15TO64 | other | 12.6K | 30.5K | 17 671; 12 659; 10 654; 15 650 |
| WHITE_POP_15TO64 | other | 49.3K | 29.7K | 4777 497; 2524 497; 4563 497; 3044 496 |
| WHITE_MALE_POP_15TO64 | other | 37.3K | 29.7K | 2423 497; 1859 497; 6204 497; 1550 334 |
| WHITE_FEMALE_POP_15TO64 | other | 37.2K | 29.7K | 3006 496; 1525 334; 9215 334; 5389 334 |
| NATIVE_POP_15TO64 | other | 5.3K | 30.8K | 7 1.3K; 1 1.2K; 2 1.2K; 8 1.2K |
| NATIVE_MALE_POP_15TO64 | other | 3.5K | 32.5K | 1 2.3K; 2 2.2K; 3 2.2K; 4 2.1K |
| NATIVE_FEMALE_POP_15TO64 | other | 3.6K | 32.5K | 4 2.3K; 3 2.2K; 1 2.2K; 5 2.2K |
| AAPI_POP_15TO64 | other | 10.7K | 32.1K | 1 1.7K; 2 1.7K; 3 1.6K; 6 1.3K |
| AAPI_MALE_POP_15TO64 | other | 8.2K | 36.2K | 1 3.6K; 2 2.9K; 3 2.7K; 4 2.4K |
| AAPI_FEMALE_POP_15TO64 | other | 8.5K | 33.4K | 1 2.4K; 2 2.3K; 3 2.1K; 4 1.9K |
| TOTAL_INCARCERATION | amount | 21.2K | 63.0K | 29 344; 24 339; 17 335; 38 334 |
| TOTAL_INCARCERATION_RATE | amount | 53.7K | 63.1K | 707.85 232; 1970.3 232; 710.38 232; 556.37 232 |
| TOTAL_JAIL_POP_RATE | amount | 54.2K | 32.2K | 0 902; 128.7 326; 357.79 326; 100.18 326 |
| MALE_JAIL_POP_RATE | amount | 63.7K | 35.9K | 0 1.5K; 191.57 313; 568.87 313; 182.45 313 |
| FEMALE_JAIL_POP_RATE | amount | 28.4K | 35.9K | 0 13.3K; 30.64 274; 64.85 273; 75.76 273 |
| BLACK_JAIL_POP_RATE | amount | 51.5K | 55.2K | 0 8.0K; 1376 331; 800 330; 1000 226 |
| LATINX_JAIL_POP_RATE | amount | 42.9K | 54.3K | 0 14.2K; 650.41 207; 354.72 207; 21875 207 |
| WHITE_JAIL_POP_RATE | amount | 43.6K | 53.8K | 0 678; 130.08 254; 235.35 254; 82.7 254 |
| NATIVE_JAIL_POP_RATE | amount | 22.1K | 55.3K | 0 43.0K; 4166.67 92; 129.25 91; 8.09 91 |
| AAPI_JAIL_POP_RATE | amount | 19.0K | 55.9K | 0 45.9K; 1069.77 135; 355.87 135; 913.24 135 |
| TOTAL_PRETRIAL_CUSTODY_RATE | amount | 54.1K | 52.2K | 0 2.5K; 100000 392; 33333.33 376; 200000 374 |
| TOTAL_SENTENCED_CUSTODY_RATE | amount | 53.7K | 55.8K | 200000 368; 75000 367; 24705.88 367; 300000 367 |
| TOTAL_JAIL_ADMITS_RATE | amount | 79.3K | 40.6K | 0 471; 1473.37 442; 710.72 442; 1457.52 442 |
| MALE_JAIL_ADMITS_RATE | amount | 55.6K | 69.1K | 0 1.6K; 2855.19 293; 3482.8 293; 3622.11 293 |
| FEMALE_JAIL_ADMITS_RATE | amount | 50.2K | 69.1K | 0 2.1K; 443.65 290; 312.35 290; 698.95 290 |
| TOTAL_JAIL_DISCHARGES_RATE | amount | 75.8K | 43.8K | 1473.37 426; 710.72 426; 1353.41 426; 1147.4 426 |
| MALE_JAIL_DISCHARGES_RATE | amount | 50.8K | 75.8K | 1434.92 265; 2505.6 265; 1193.27 265; 5261.52 265 |
| FEMALE_JAIL_DISCHARGES_RATE | amount | 45.5K | 75.8K | 0 1.1K; 810.67 261; 732.65 261; 315.27 261 |
| TOTAL_PRISON_POP_RATE | amount | 60.4K | 38.0K | 0 1.8K; 538.42 448; 765.97 448; 380.89 448 |
| MALE_PRISON_POP_RATE | amount | 50.3K | 69.1K | 0 1.3K; 1313.19 294; 761.25 294; 1403.14 294 |
| FEMALE_PRISON_POP_RATE | amount | 22.2K | 70.1K | 0 12.3K; 157.11 234; 142.84 234; 193.54 234 |
| BLACK_PRISON_POP_RATE | amount | 28.3K | 92.1K | 0 3.4K; 4566.21 167; 4365.08 167; 2006.69 167 |
| BLACK_MALE_PRISON_POP_RATE | amount | 22.2K | 100.2K | 0 1.6K; 7692.31 136; 7246.38 136; 3076.92 136 |
| BLACK_FEMALE_PRISON_POP_RATE | amount | 13.7K | 101.6K | 0 4.7K; 359.71 114; 492.61 113; 961.54 113 |
| LATINX_PRISON_POP_RATE | amount | 16.6K | 99.6K | 0 9.2K; 866.34 101; 1023.62 100; 1338.58 100 |
| LATINX_MALE_PRISON_POP_RATE | amount | 14.5K | 107.0K | 0 4.2K; 1634.88 88; 2350.27 88; 2287.58 88 |
| LATINX_FEMALE_PRISON_POP_RATE | amount | 7.6K | 108.5K | 0 8.6K; 146.84 59; 145.99 59; 263.85 59 |
| WHITE_PRISON_POP_RATE | amount | 36.1K | 80.2K | 0 889; 725.5 240; 398.98 240; 688.28 240 |
| WHITE_MALE_PRISON_POP_RATE | amount | 31.9K | 91.6K | 0 406; 1239.54 185; 802.33 185; 1229.32 185 |
| WHITE_FEMALE_PRISON_POP_RATE | amount | 18.6K | 92.4K | 0 2.7K; 159.18 169; 131.65 169; 196.76 169 |
| NATIVE_PRISON_POP_RATE | amount | 6.6K | 108.5K | 0 11.8K; 30769.23 44; 2083.33 43; 1574.8 43 |
| NATIVE_MALE_PRISON_POP_RATE | amount | 5.2K | 115.3K | 0 6.1K; 4166.67 39; 5555.56 39; 66666.67 39 |
| NATIVE_FEMALE_PRISON_POP_RATE | amount | 3.5K | 115.7K | 0 7.7K; 1123.6 29; 1190.48 29; 1388.89 28 |
| AAPI_PRISON_POP_RATE | amount | 3.2K | 116.7K | 0 8.3K; 588.24 18; 1285.35 18; 884.96 18 |
| AAPI_MALE_PRISON_POP_RATE | amount | 3.2K | 118.3K | 0 6.8K; 1078.17 18; 2500 18; 1442.31 18 |
| AAPI_FEMALE_PRISON_POP_RATE | amount | 1.6K | 118.5K | 0 8.1K; 8.94 11; 7.37 11; 14.23 11 |
| TOTAL_PRISON_ADMITS_RATE | amount | 45.7K | 39.3K | 0 3.1K; 200.33 436; 109.45 435; 35.17 435 |
| MALE_PRISON_ADMITS_RATE | amount | 41.0K | 72.8K | 0 2.2K; 214.75 271; 163.5 271; 406.87 271 |
| FEMALE_PRISON_ADMITS_RATE | amount | 19.5K | 73.7K | 0 13.7K; 15.97 208; 17 208; 68.66 208 |
| BLACK_PRISON_ADMITS_RATE | amount | 23.4K | 95.0K | 0 5.1K; 2380.95 145; 1598.17 144; 643.92 144 |
| BLACK_MALE_PRISON_ADMITS_RATE | amount | 17.7K | 104.6K | 0 2.6K; 1882.85 109; 2429.15 108; 3623.19 108 |
| BLACK_FEMALE_PRISON_ADMITS_RATE | amount | 11.7K | 105.8K | 0 5.1K; 523.56 90; 877.19 90; 492.61 90 |
| LATINX_PRISON_ADMITS_RATE | amount | 12.2K | 101.9K | 0 12.7K; 472.44 71; 551.18 71; 553.25 71 |
| LATINX_MALE_PRISON_ADMITS_RATE | amount | 10.5K | 110.6K | 0 6.0K; 759.01 62; 817.44 61; 833.97 61 |
| LATINX_FEMALE_PRISON_ADMITS_RATE | amount | 6.4K | 111.3K | 0 8.7K; 245.7 43; 146.84 43; 63.43 43 |
| WHITE_PRISON_ADMITS_RATE | amount | 28.9K | 83.4K | 0 1.7K; 223.23 220; 271.14 220; 74.31 220 |
| WHITE_MALE_PRISON_ADMITS_RATE | amount | 26.4K | 95.9K | 0 834; 357.41 161; 452.43 161; 147.25 161 |
| WHITE_FEMALE_PRISON_ADMITS_RATE | amount | 16.7K | 96.7K | 0 3.4K; 123.95 145; 75.4 144; 84.63 144 |
| NATIVE_PRISON_ADMITS_RATE | amount | 4.8K | 107.8K | 0 15.4K; 941.62 28; 816.33 27; 354.14 27 |
| NATIVE_MALE_PRISON_ADMITS_RATE | amount | 3.7K | 116.1K | 0 8.0K; 1119.4 23; 584.27 23; 1250 23 |
| NATIVE_FEMALE_PRISON_ADMITS_RATE | amount | 2.8K | 116.3K | 0 8.8K; 1190.48 20; 316.46 20; 507.61 20 |
| AAPI_PRISON_ADMITS_RATE | amount | 1.7K | 115.7K | 0 10.9K; 21.2 11; 372.44 10; 728.6 10 |
| AAPI_MALE_PRISON_ADMITS_RATE | amount | 1.7K | 118.3K | 0 8.4K; 600 10; 816.33 10; 514.58 10 |
| AAPI_FEMALE_PRISON_ADMITS_RATE | amount | 941 | 118.2K | 0 9.2K; 9.58 7; 11.31 7; 2.4 7 |
| INGESTED_AT | audit | 1 | 0 | 1782616883476104 128.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | dc9c30cc-01e4-4049-bed4-5 128.5K |
| SRC_SHA256 | other | 1 | 0 | 3aa4b13de3adb9963e1850f0d 128.5K |
