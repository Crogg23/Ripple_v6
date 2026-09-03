# PORTAL_CKA_CALIFORNIA_OPEN_09F2ECF408

rows 380  columns 24  scan 4.5s

roles: amount 3, audit 2, category 8, date 1, other 7, who 4

## when

INGESTED_AT
  2026       380  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X | 380 | -13.84M | -13.57M | -12.96M | -12.85M | -5.14B |
| Y | 380 | 3.83M | 4.65M | 5.14M | 5.16M | 1.77B |
| AWARD | 380 | 30.0K | 758.4K | 8.03M | 13.43M | 459.49M |

## who

GRANTEE by rows
        25  Regents of the University of California, Davis
        21  California Trout, Inc.
        14  Trout Unlimited, Inc.
        12  River Partners
         9  American Rivers
         8  Truckee River Watershed Council
         7  Scott River Watershed Council
         5  Smith River Alliance
         5  Regents of the University of California, Santa Cruz
         5  Yurok Tribe
         4  Trout Unlimited
         4  Family Water Alliance, Inc.
         4  Humboldt County Resource Conservation District
         4  California State Coastal Conservancy
         4  Sierra Foothill Conservancy
         4  San Francisco State University
         4  South Yuba River Citizens League
         4  The Nature Conservancy
         3  Sutter Butte Flood Control Agency
         3  Yurok Tribe 

GRANTEE by dollars
      23.59M       21 rows  California Trout, Inc.
      21.79M       25 rows  Regents of the University of California, Davis
      21.74M        3 rows  Ventura County Watershed Protection District
      15.54M       14 rows  Trout Unlimited, Inc.
      14.75M       12 rows  River Partners
      12.25M        5 rows  Yurok Tribe
      10.39M        1 rows  Reclamation District 341
       9.92M        3 rows  Yurok Tribe 
       9.60M        8 rows  Truckee River Watershed Council
       9.34M        2 rows  The Trust for Public Land
       8.28M        9 rows  American Rivers
       8.13M        1 rows  Reclamation District 2035
       8.00M        2 rows  State Coastal Conservancy
       7.75M        5 rows  Regents of the University of California, Santa Cruz
       7.33M        4 rows  South Yuba River Citizens League
       7.16M        2 rows  Tolowa Dee-ni Nation
       6.40M        2 rows  Northcoast Regional Land Trust
       6.35M        3 rows  Sutter Butte Flood Control Agency
       6.16M        4 rows  California State Coastal Conservancy
       5.97M        2 rows  Ducks Unlimited, Inc.

PT_EXTENT by rows
       132  Discrete Site
        19  Discrete site
         9  Region - Delta
         7  Lab Site - UC Davis
         6  Delta
         3  Range of longfin smelt
         2  Delta and SF Bay (Range of Delta Smelt)
         2  4  Lahontan Basin Meadows - Lassen/Alpine Counties
         2  Big Springs Ranch Wildlife Area
         2  Lab Site - SF State University
         1  Robles Diversion and Fish Passage Facility, Meiner Oaks
         1  Lower Putah Creek
         1  Range of Longfin Smelt
         1  Small area of Russian River floodplain
         1  waters near Evans spring
         1  9 sites within .25 mi of each other
         1  select land in Scott River watershed
         1  1 mile of East Fork Scott River and 1.6 miles of Grouse Creek
         1  4240' reach of Lakeville Creek
         1  Large fire region

PT_EXTENT by dollars
     177.91M      132 rows  Discrete Site
      24.93M       19 rows  Discrete site
      10.39M        1 rows  Discrete Site - Sherman Island
       9.00M        1 rows  range of 2022 McKinney fire
       8.13M        1 rows  Discrete Site - intake facility on Sac Rive
       6.89M        1 rows  9 sites within .25 mi of each other
       6.75M        1 rows  Robles diversion facility and Meiners Oaks
       5.58M        1 rows  Discrete Site - Hill Slough
       5.46M        1 rows  Tuolumne R mainsten upstream of Old La Grange Bridge
       5.39M        7 rows  Lab Site - UC Davis
       5.37M        9 rows  Region - Delta
       5.05M        6 rows  Delta
       5.00M        1 rows  Two salt ponds - Ravenswood and Mountain View
       4.97M        1 rows  3 fish passage barriers
       4.66M        1 rows  Lagunitas Cr. within Samuel P. Taylor State Park
       3.99M        1 rows  Oregon Gulch
       3.64M        1 rows  Region - Watershed
       3.47M        3 rows  Range of longfin smelt
       3.38M        1 rows  55,000 acres of Inyo National Forest lands
       3.30M        1 rows  Matilija Creek - Los Padres National Forest

COUNTY by rows
        31  Siskiyou
        24  Humboldt
        18  Mendocino
        17  Sonoma
        13  Marin
        13  Yolo
        12  Shasta
        10  Ventura
        10  Multiple Delta
         8  Butte
         8  Stanislaus
         8  Santa Barbara
         8  Solano
         7  San Diego
         7  Monterey
         7  Tehama
         6  Placer
         6  Plumas
         6  Del Norte
         5  Tuolumne

COUNTY by dollars
      39.74M       31 rows  Siskiyou
      33.28M       10 rows  Ventura
      30.02M       24 rows  Humboldt
      17.62M       13 rows  Yolo
      15.02M       13 rows  Marin
      13.90M        8 rows  Stanislaus
      13.84M       18 rows  Mendocino
      12.71M       12 rows  Shasta
      12.40M        2 rows  Sacramento
      12.32M        7 rows  San Diego
      11.92M       17 rows  Sonoma
      11.16M        8 rows  Butte
      10.30M        7 rows  Monterey
      10.15M        8 rows  Solano
       9.91M       10 rows  Multiple Delta
       9.73M        6 rows  Del Norte
       9.16M        5 rows  El Dorado
       8.82M        8 rows  Santa Barbara
       8.69M        7 rows  Tehama
       8.41M        2 rows  Orange 

SRC_SHA256 by rows
       380  191425b6cf970c5ed02dc5addeb4bf17a663b24d4759444105830c51b4a82aa1

SRC_SHA256 by dollars
     459.49M      380 rows  191425b6cf970c5ed02dc5addeb4bf17a663b24d4759444105830c51b4a8

## who x when

GRANTEE by INGESTED_AT  LOAD STAMP, not an event date, dollars = AWARD
  American Rivers                           2026:8.28M
  California State Coastal Conservancy      2026:6.16M
  California Trout, Inc.                    2026:23.59M
  Ducks Unlimited, Inc.                     2026:5.97M
  Family Water Alliance, Inc.               2026:1.99M
  Humboldt County Resource Conservation Di  2026:3.69M
  Northcoast Regional Land Trust            2026:6.40M
  Reclamation District 2035                 2026:8.13M
  Reclamation District 341                  2026:10.39M
  Regents of the University of California,  2026:21.79M
  Regents of the University of California,  2026:7.75M
  River Partners                            2026:14.75M
  San Francisco State University            2026:2.70M
  Scott River Watershed Council             2026:5.43M
  Sierra Foothill Conservancy               2026:4.68M
  Smith River Alliance                      2026:3.51M
  South Yuba River Citizens League          2026:7.33M
  State Coastal Conservancy                 2026:8.00M
  Sutter Butte Flood Control Agency         2026:6.35M
  The Nature Conservancy                    2026:2.59M
  The Trust for Public Land                 2026:9.34M
  Tolowa Dee-ni Nation                      2026:7.16M
  Trout Unlimited                           2026:3.45M
  Trout Unlimited, Inc.                     2026:15.54M
  Truckee River Watershed Council           2026:9.60M
  Ventura County Watershed Protection Dist  2026:21.74M
  Yurok Tribe                               2026:12.25M
  Yurok Tribe                               2026:9.92M

PT_EXTENT by INGESTED_AT  LOAD STAMP, not an event date, dollars = AWARD
  1 mile of East Fork Scott River and 1.6   2026:970.7K
  3 fish passage barriers                   2026:4.97M
  4  Lahontan Basin Meadows - Lassen/Alpin  2026:692.7K
  4240' reach of Lakeville Creek            2026:2.20M
  9 sites within .25 mi of each other       2026:6.89M
  Big Springs Ranch Wildlife Area           2026:2.77M
  Delta                                     2026:5.05M
  Delta and SF Bay (Range of Delta Smelt)   2026:2.38M
  Discrete Site                             2026:177.91M
  Discrete Site - Hill Slough               2026:5.58M
  Discrete Site - Sherman Island            2026:10.39M
  Discrete Site - intake facility on Sac R  2026:8.13M
  Discrete site                             2026:24.93M
  Lab Site - SF State University            2026:733.5K
  Lab Site - UC Davis                       2026:5.39M
  Lagunitas Cr. within Samuel P. Taylor St  2026:4.66M
  Large fire region                         2026:382.2K
  Lower Putah Creek                         2026:990.3K
  Oregon Gulch                              2026:3.99M
  Range of Longfin Smelt                    2026:330.8K
  Range of longfin smelt                    2026:3.47M
  Region - Delta                            2026:5.37M
  Robles Diversion and Fish Passage Facili  2026:1.56M
  Robles diversion facility and Meiners Oa  2026:6.75M
  Small area of Russian River floodplain    2026:717.9K
  Tuolumne R mainsten upstream of Old La G  2026:5.46M
  Two salt ponds - Ravenswood and Mountain  2026:5.00M
  range of 2022 McKinney fire               2026:9.00M
  select land in Scott River watershed      2026:512.9K
  waters near Evans spring                  2026:500.9K

## what

PROGRAM: Prop 1 Watershed 46%, Watershed Grants 22%, Prop 1 Delta 16%, Greenhouse Gas Reduction Fund 6%, Prop 68 Rivers 4%, Fisheries Restoration Grants 2%, Prop 68 1%, Prop 68 Habitats 1%, Prop 68 Southern Steelhead 1%, Prop 1 0%, Unk 0%

CATEGORY: Implementation 40%, Planning 33%, Scientific Studies 16%, Acquisition 8%, Monitoring 2%, na 1%, Planning  0%, Implementation  0%

FISCAL_YR: 2022-2023 26%, 2020-2021 11%, 2023-2024 11%, 2019-2020 10%, 2016-2017 10%, 2017-2018 9%, 2015-2016 7%, 2021-2022 7%, 2018-2019 6%, 2014-2015 3%, 2016-2017, 2019-2020 0%, 2016-2017, 2021-2022 0%

REGION: 3 30%, 1 30%, 2 15%, 5 11%, 4 10%, 6 3%, 2, 3 1%, 1, 2 1%, 4, 6 0%, 1, 2, 3 0%, 1, 3 0%

PRIORITY: Protect and Restore Anadromous 31%, Scientific Studies 17%, Protect and Restore Coastal We 7%, Drought 7%, Climate 7%, Protect and Restore Mountain M 7%, Rivers and streams 5%, NBS-Wetlands/Meadows 5%, Manage Headwaters for Multiple 5%, NBS-Wildlife Corridors 3%, Mountain Meadow 3%, Drought - Protecting Salmon 3%

STATUS: Ongoing 52%, Closed 30%, Awarded 18%

RELATED: Tied to Master Agreement Q2296 21%, Tied to Master Agreement Q2296 14%, P1496007 7%, Q1996027 7%, P1796010, P1696019 7%, P1896043 7%, P1896045 7%, merged three apps 7%, P1596013 7%, P1696011 7%, P1596017 7%

COMMENT: March 2023 17%, April 2023 15%, May 2023 14%, November 2023 10%, September 2023 10%, Cutting the Green Tape Project 10%, August 2023 9%, July 2023 7%, June 2023 5%, October 2023 2%, April 2023; Tied to Master Agr 2%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| X | amount | 374 | 0 | -13675762.527 3; -13748446.9188 3; -13820102.2731 3; -13279327.2039 3 |
| Y | amount | 374 | 0 | 4953557.7063 3; 4823294.6102 3; 5144453.0886 3; 4091420.4676 3 |
| OBJECTID | other | 379 | 0 | 380 2; 379 2; 378 2; 377 2 |
| PROGRAM | category | 12 | 1 | Prop 1 Watershed 176; Watershed Grants 82; Prop 1 Delta 62; Greenhouse Gas Reduction  21 |
| GRANTEE | who | 196 | 0 | Regents of the University 25; California Trout, Inc. 21; Trout Unlimited, Inc. 14; River Partners 12 |
| CATEGORY | category | 8 | 0 | Implementation 153; Planning 126; Scientific Studies 60; Acquisition 31 |
| KEY | other | 379 | 0 | 2023_1729752 3; 2023_1730552 3; 2023_1730617 2; 2023_1730452 2 |
| FISCAL_YR | category | 12 | 0 | 2022-2023 98; 2020-2021 43; 2023-2024 40; 2019-2020 39 |
| TITLE | other | 376 | 0 | Indian Creek Fish Passage 3; Tenmile Creek Sediment Re 3; Dillon Beach Ranch 2; Tuolumne River Mainstem C 2 |
| REGION | category | 11 | 0 | 3 113; 1 113; 2 56; 5 41 |
| COUNTY | who | 103 | 0 | Siskiyou 31; Humboldt 24; Mendocino 18; Sonoma 17 |
| PRIORITY | category | 34 | 0 | Protect and Restore Anadr 100; Scientific Studies 54; Protect and Restore Coast 23; Drought 22 |
| DESCRIPTION | other | 376 | 0 | The project is on Indian  3; The Eel River Watershed I 3; Western Rivers seeks to a 2; The implementation of the 2 |
| DESC_SHORT | other | 253 | 130 | This project seeks to pro 2; This project will identif 2; The purpose of this proje 2; Specific objectives of th 2 |
| NUMBER | other | 376 | 0 | 1729752 3; 1730552 3; Q2196507 3; 1730617 2 |
| AWARD | amount | 366 | 0 | $1,000,000 5; $1,500,000 4; $500,000 4; $787,250 3 |
| STATUS | category | 3 | 0 | Ongoing 196; Closed 115; Awarded 69 |
| RELATED | category | 24 | 354 | Tied to Master Agreement  3; Tied to Master Agreement  2; P1496007 1; Q1996027 1 |
| COMMENT | category | 34 | 252 | March 2023 18; April 2023 16; May 2023 15; November 2023 11 |
| PT_EXTENT | who | 205 | 1 | Discrete Site 132; Discrete site 19; Region - Delta 9; Lab Site - UC Davis 7 |
| WRGB_PIN | other | 359 | 13 | 1729085 3; 1730887 2; 1729869 2; 1730569 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:19:57.83597 380 |
| SOURCE_RUN_ID | audit | 1 | 0 | 513949d4-f1ae-4f63-98a0-b 380 |
| SRC_SHA256 | who | 1 | 0 | 191425b6cf970c5ed02dc5add 380 |
