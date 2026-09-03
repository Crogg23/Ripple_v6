# PORTAL_CKA_SAN_JOSE_OPEN_DA_FAAD5A2133

rows 3.2K  columns 28  scan 4.5s

roles: amount 2, audit 2, category 15, date 1, empty 1, id 2, who 6

## when

INGESTED_AT
  2026      3.2K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SEGMENTMILES | 3.2K | 0 | 0.07 | 1.49 | 8.02 | 562.40 |
| SHAPE_LENGTH | 3.2K | 0 | 377.55 | 7.6K | 42.4K | 2.87M |

## who

FULLSTREETNAME by rows
        85  Santa Teresa Bl
        71  Capitol Av
        61  Monterey Rd
        56  Curtner Av
        54  White Rd
        49  Willow St
        48  Senter Rd
        47  Piedmont Rd
        46  Los Gatos-Almaden Rd
        44  Williams Rd
        41  Snell Av
        40  Story Rd
        39  Union Av
        39  Blossom Hill Rd
        39  Bird Av
        37  Nieman Bl
        37  Leigh Av
        36  Hillsdale Av
        36  Mclaughlin Av
        36  Campbell Av

FULLSTREETNAME by dollars
       50.2K       85 rows  Santa Teresa Bl
       49.8K       61 rows  Monterey Rd
       34.1K       39 rows  Blossom Hill Rd
       32.3K       54 rows  White Rd
       31.8K       27 rows  Camden Av
       31.3K       15 rows  1St St
       28.4K       71 rows  Capitol Av
       28.2K        9 rows  King Rd
       27.2K       12 rows  Branham Ln
       26.6K        9 rows  10Th St
       26.5K       32 rows  Tully Rd
       26.4K       35 rows  Yerba Buena Rd
       25.0K       56 rows  Curtner Av
       24.9K       48 rows  Senter Rd
       23.5K        8 rows  Hedding St
       22.6K       18 rows  Bernal Rd
       21.4K       37 rows  Leigh Av
       21.4K       20 rows  Zanker Rd
       21.1K        6 rows  7Th St
       21.1K       14 rows  Tasman Dr

STREETNAME by rows
        86  Santa Teresa
        71  Capitol
        61  Monterey
        56  Curtner
        54  White
        49  Meridian
        49  Willow
        48  Senter
        47  Yerba Buena
        47  Piedmont
        46  Los Gatos-Almaden
        44  Williams
        42  Snell
        42  Coleman
        40  Story
        39  Bird
        39  Union
        38  Blossom Hill
        37  Leigh
        37  Nieman

STREETNAME by dollars
       50.5K       86 rows  Santa Teresa
       49.8K       61 rows  Monterey
       34.7K       38 rows  Blossom Hill
       34.4K       35 rows  Stevens Creek
       32.3K       54 rows  White
       31.8K       27 rows  Camden
       31.3K       15 rows  1St
       31.3K       47 rows  Yerba Buena
       28.4K       71 rows  Capitol
       28.2K        9 rows  King
       27.2K       12 rows  Branham
       26.6K        9 rows  10Th
       26.5K       32 rows  Tully
       25.5K       49 rows  Meridian
       25.0K       56 rows  Curtner
       24.9K       48 rows  Senter
       23.5K        8 rows  Hedding
       22.6K       18 rows  Bernal
       22.0K       30 rows  Almaden
       21.6K       42 rows  Coleman

STATUS by rows
      3.2K  Existing

STATUS by dollars
       2.87M     3.2K rows  Existing

FACILITYID by rows
         1  60
         1  45
         1  35
         1  89
         1  69
         1  90
         1  96
         1  129
         1  108
         1  163
         1  212
         1  169
         1  120
         1  47
         1  48
         1  15
         1  186
         1  82
         1  114
         1  64

FACILITYID by dollars
       42.4K        1 rows  4
       41.9K        1 rows  55
       32.7K        1 rows  15
       27.9K        1 rows  29
       21.7K        1 rows  6
       17.7K        1 rows  28
       16.3K        1 rows  1291
       15.4K        1 rows  1399
       15.2K        1 rows  235
       14.3K        1 rows  5
       13.6K        1 rows  3638
       12.3K        1 rows  54
       12.2K        1 rows  4728
       11.8K        1 rows  2508
       11.6K        1 rows  1
       11.6K        1 rows  68
       11.3K        1 rows  27
       10.3K        1 rows  48
       10.1K        1 rows  56
        9.0K        1 rows  4011

## who x when

FULLSTREETNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  10Th St                                   2026:26.6K
  1St St                                    2026:31.3K
  Bernal Rd                                 2026:22.6K
  Bird Av                                   2026:16.7K
  Blossom Hill Rd                           2026:34.1K
  Branham Ln                                2026:27.2K
  Camden Av                                 2026:31.8K
  Campbell Av                               2026:14.2K
  Capitol Av                                2026:28.4K
  Curtner Av                                2026:25.0K
  Hedding St                                2026:23.5K
  Hillsdale Av                              2026:19.0K
  King Rd                                   2026:28.2K
  Leigh Av                                  2026:21.4K
  Los Gatos-Almaden Rd                      2026:13.3K
  Mclaughlin Av                             2026:11.8K
  Monterey Rd                               2026:49.8K
  Nieman Bl                                 2026:10.2K
  Piedmont Rd                               2026:13.6K
  Santa Teresa Bl                           2026:50.2K
  Senter Rd                                 2026:24.9K
  Snell Av                                  2026:17.7K
  Story Rd                                  2026:17.8K
  Tully Rd                                  2026:26.5K
  Union Av                                  2026:17.0K
  White Rd                                  2026:32.3K
  Williams Rd                               2026:15.4K
  Willow St                                 2026:14.0K
  Yerba Buena Rd                            2026:26.4K
  Zanker Rd                                 2026:21.4K

STREETNAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SHAPE_LENGTH
  10Th                                      2026:26.6K
  1St                                       2026:31.3K
  Almaden                                   2026:22.0K
  Bernal                                    2026:22.6K
  Bird                                      2026:16.7K
  Blossom Hill                              2026:34.7K
  Branham                                   2026:27.2K
  Camden                                    2026:31.8K
  Capitol                                   2026:28.4K
  Coleman                                   2026:21.6K
  Curtner                                   2026:25.0K
  Hedding                                   2026:23.5K
  King                                      2026:28.2K
  Leigh                                     2026:21.4K
  Los Gatos-Almaden                         2026:13.3K
  Meridian                                  2026:25.5K
  Monterey                                  2026:49.8K
  Nieman                                    2026:10.2K
  Piedmont                                  2026:13.6K
  Santa Teresa                              2026:50.5K
  Senter                                    2026:24.9K
  Snell                                     2026:19.2K
  Stevens Creek                             2026:34.4K
  Story                                     2026:17.8K
  Tully                                     2026:26.5K
  Union                                     2026:17.0K
  White                                     2026:32.3K
  Williams                                  2026:15.4K
  Willow                                    2026:14.0K
  Yerba Buena                               2026:31.3K

## what

YEARINSTALLED: 2000 12%, 2018 12%, 2019 10%, 2017 10%, 1999 10%, 2020 10%, 2014 9%, 1974 8%, 2016 7%, 1995 7%, 2009 6%

YEARENHANCED: 2018 18%, 2021 18%, 2019 17%, 2017 13%, 2020 11%, 2015 6%, 2014 5%, 2022 4%, 2016 4%, 2013 3%, 2012 1%

COUNCILDISTRICT: 6 14%, 3 12%, 10 12%, 4 11%, 8 11%, 1 10%, 5 8%, 9 7%, 2 7%, 7 6%, 2;7 1%

SUBTYPEID: 2 40%, 3 34%, 4 14%, 6 8%, 1 2%, 5 2%

EXISTINGBIKEWAYCLASS: Class 2 (Basic) 40%, Class 2 (Buffered) 34%, Class 3 (Sharrow) 14%, Class 4 8%, Class 1 2%, Class 3 (Bike Blvd) 2%, Class 3 (Sharrows) 0%, Class 2 (BUFFERED) 0%

PROGRAMMEDBIKEWAYCLASS: Class 4 46%, Class 3 (Sharrow) 42%, Class 2 (Buffered) 6%, Class 3 (Bike Blvd) 4%, Class 2 (Basic) 2%

BIKEPLAN2020: Basic Bikeway 58%, Primary Bikeway 23%, Not included in Bike Plan 2020 19%

STREETCLASS: Av 38%, Rd 30%, St 14%, Bl 6%, Dr 5%, Ave 1%, CO 1%, Wy 1%, RE 1%, Ln 1%, MA 1%

FHWACLASS: Minor Arterial 36%, Major Arterial 25%, Residential 20%, Collector 19%, RE 0%, Freeway 0%, Expressway 0%, Ramp 0%, Path 0%

FUND: 2019 Pavement Maintenance 26%, 2018 Pavement Maintenance 16%, ESJ OBAG 16%, 2017 Pavement Maintenance 9%, 2020 Pavement Maintenance 7%, 2018 Pavement Maintenance Prog 7%, 2017 Pavement Maintenance Prog 4%, 2019 Pavement Maintenance Prog 4%, 2020 Pavement Maintenance Prog 4%, Local Projects 3%, 2021 Pavement Maintenance 3%

SECONDYEARENHANCED: 2018 73%, 2021 21%, 2020 6%

INCORPORATED: Yes 95%, No 5%

PROGRAMMEDFORENHANCEMENTFLAG: No 99%, Yes 1%

CREATIONDATE: 2024/01/26 00:36:12+00 13%, 2024/01/26 00:33:41+00 13%, 2023/08/01 16:52:57+00 13%, 2023/07/31 22:21:49+00 13%, 2024/09/11 17:22:12+00 7%, 2024/09/11 17:10:55+00 7%, 2024/09/11 17:06:12+00 7%, 2024/04/02 17:29:21+00 7%, 2024/01/26 00:51:02+00 7%, 2024/01/25 21:15:29+00 7%, 2024/01/25 21:14:35+00 7%

NOTES: Speed limit (HD 63339) 36%, BM HD 90821 31%, SW HD 44092 & 45792 10%, Directions: Address Gap Ignore 8%, DS: ZipUpdate 3%, DX Tool Validated 3%, BM HD 87480 3%, BM HD 77218 3%, Muni int fixed 3%, T_Shape: Address Gap Ignored 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 3.2K | 0 | 10053 16; 10052 16; 10051 16; 10050 16 |
| STATUS | who | 1 | 0 | Existing 3.2K |
| YEARINSTALLED | category | 45 | 181 | 2000 208; 2018 205; 2019 182; 2017 182 |
| YEARENHANCED | category | 14 | 2.4K | 2018 149; 2021 142; 2019 137; 2017 104 |
| FACILITYID | who | 3.2K | 0 | 9656 16; 9655 16; 9654 16; 9653 16 |
| INTID | id | 3.2K | 0 | 9656 16; 9655 16; 9654 16; 9653 16 |
| COUNCILDISTRICT | category | 23 | 151 | 6 406; 3 350; 10 345; 4 331 |
| SALESFORCEID | empty | 1 | 3.2K |  |
| SUBTYPEID | category | 6 | 0 | 2 1.3K; 3 1.1K; 4 460; 6 258 |
| EXISTINGBIKEWAYCLASS | category | 9 | 5 | Class 2 (Basic) 1.3K; Class 2 (Buffered) 1.1K; Class 3 (Sharrow) 460; Class 4 252 |
| PROGRAMMEDBIKEWAYCLASS | category | 6 | 3.0K | Class 4 78; Class 3 (Sharrow) 70; Class 2 (Buffered) 10; Class 3 (Bike Blvd) 6 |
| BIKEPLAN2020 | category | 4 | 1.6K | Basic Bikeway 927; Primary Bikeway 368; Not included in Bike Plan 295 |
| STREETNAME | who | 359 | 75 | Santa Teresa 86; Capitol 71; Monterey 61; Curtner 56 |
| STREETCLASS | category | 19 | 105 | Av 1.1K; Rd 905; St 427; Bl 193 |
| FULLSTREETNAME | who | 381 | 76 | Santa Teresa Bl 85; Capitol Av 71; Monterey Rd 61; Curtner Av 56 |
| FHWACLASS | category | 10 | 254 | Minor Arterial 1.1K; Major Arterial 730; Residential 576; Collector 559 |
| SEGMENTMILES | amount | 3.1K | 31 | 2.36981938 19; 1.15385368 18; 0.42096503 18; 0.97554501 18 |
| FUND | category | 14 | 2.3K | 2019 Pavement Maintenance 228; 2018 Pavement Maintenance 140; ESJ OBAG 137; 2017 Pavement Maintenance 78 |
| SECONDYEARENHANCED | category | 4 | 3.2K | 2018 24; 2021 7; 2020 2 |
| INCORPORATED | category | 3 | 32 | Yes 3.0K; No 147 |
| PROGRAMMEDFORENHANCEMENTFLAG | category | 3 | 41 | No 3.1K; Yes 27 |
| CREATIONDATE | category | 31 | 3.2K | 2024/01/26 00:36:12+00 2; 2024/01/26 00:33:41+00 2; 2023/08/01 16:52:57+00 2; 2023/07/31 22:21:49+00 2 |
| LASTUPDATE | who | 90 | 0 | 2023/02/23 20:22:50+00 2.0K; 2023/02/23 20:16:49+00 924; 2024/01/10 00:00:37+00 19; 2024/04/02 17:10:21+00 15 |
| NOTES | category | 11 | 3.2K | Speed limit (HD 63339) 14; BM HD 90821 12; SW HD 44092 & 45792 4; Directions: Address Gap I 3 |
| SHAPE_LENGTH | amount | 3.1K | 0 | 499.182155194378 17; 275.911296979961 17; 262.14102497141 17; 619.823569637873 16 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:05:39.46488 3.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 2f83ef58-2b97-4b87-ac91-7 3.2K |
| SRC_SHA256 | who | 1 | 0 | 9cd581e33e9f93d1040ed4499 3.2K |
