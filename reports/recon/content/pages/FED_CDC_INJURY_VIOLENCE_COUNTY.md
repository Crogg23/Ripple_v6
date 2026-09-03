# FED_CDC_INJURY_VIOLENCE_COUNTY

rows 132.0K  columns 15  scan 5.1s

roles: amount 2, audit 2, category 4, date 1, other 4, who 2

## when

DATA_AS_OF
  2026    132.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| RATE | 132.0K | -999 | 9.60 | 52.46 | 284 | -5.09M |
| RATE_M | 132.0K | 0 | 1 | 1 | 1 | 70.6K |

## who

NAME by rows
      1.3K  Washington County
      1.1K  Jefferson County
      1.0K  Franklin County
       966  Jackson County
       966  Lincoln County
       798  Madison County
       756  Clay County
       756  Montgomery County
       714  Marion County
       714  Monroe County
       714  Union County
       672  Wayne County
       588  Greene County
       588  Grant County
       588  Warren County
       546  Carroll County
       504  Lee County
       504  Johnson County
       504  Adams County
       504  Marshall County

NAME by dollars
        2.6K      210 rows  Carter County
        2.4K      168 rows  Sumter County
        1.9K      168 rows  Lancaster County
        1.8K       42 rows  Baltimore city
        1.8K       42 rows  St. Louis city
        1.8K      126 rows  Bedford County
        1.6K       84 rows  Davidson County
        1.5K       84 rows  Rowan County
        1.5K       84 rows  Halifax County
        1.5K       42 rows  Orleans Parish
        1.5K       84 rows  Laurens County
        1.5K      126 rows  Erie County
        1.3K       84 rows  Blount County
        1.3K       84 rows  Berkeley County
        1.3K       42 rows  Hinds County
        1.3K       84 rows  St. Louis County
        1.3K       42 rows  Coahoma County
        1.3K       42 rows  Robeson County
        1.3K       84 rows  Winston County
        1.3K      126 rows  Oneida County

RATE_M_CI by rows
      6.5K  -999
        23  0.8-5.2
        23  0.7-4.5
        21  0.8-6.6
        20  0.9-6.0
        20  1.2-7.0
        19  1.0-8.0
        19  1.2-9.4
        19  0.8-6.7
        18  0.7-5.8
        18  0.7-3.9
        18  0.7-3.7
        18  1.2-7.7
        18  1.1-8.6
        18  1.1-7.9
        18  0.8-6.0
        17  0.6-4.5
        17  1.2-9.2
        17  0.5-3.4
        17  1.3-8.7

RATE_M_CI by dollars
      186.80       13 rows  8.6-24.0
         181       10 rows  12.0-27.3
         175       14 rows  7.0-22.3
      168.10       12 rows  8.4-23.4
      162.10       10 rows  11.0-23.9
      159.90       13 rows  7.2-21.0
         157        9 rows  11.9-25.6
      156.80       11 rows  8.3-24.5
      156.30       15 rows  6.4-17.0
      154.80       12 rows  7.7-21.6
      152.20        9 rows  9.7-29.5
         152        8 rows  13.0-27.8
      151.30       13 rows  7.0-19.4
      151.20        9 rows  11.6-24.3
      148.70       12 rows  7.7-19.9
      147.30       11 rows  7.9-22.7
      147.10       13 rows  6.6-19.4
      146.80       14 rows  6.2-17.7
      146.50        9 rows  10.8-24.5
      146.20       12 rows  7.0-21.2

## who x when

NAME by DATA_AS_OF, dollars = RATE
  Adams County                              2026:-15.0K
  Baltimore city                            2026:1.8K
  Bedford County                            2026:1.8K
  Carroll County                            2026:-20.0K
  Carter County                             2026:2.6K
  Clay County                               2026:-53.4K
  Davidson County                           2026:1.6K
  Franklin County                           2026:-35.3K
  Grant County                              2026:-54.5K
  Greene County                             2026:-19.5K
  Halifax County                            2026:1.5K
  Jackson County                            2026:-48.1K
  Jefferson County                          2026:-25.9K
  Johnson County                            2026:-10.6K
  Lancaster County                          2026:1.9K
  Lee County                                2026:-10.9K
  Lincoln County                            2026:-27.2K
  Madison County                            2026:-25.7K
  Marion County                             2026:-9.8K
  Marshall County                           2026:-33.7K
  Monroe County                             2026:-23.2K
  Montgomery County                         2026:-15.0K
  Orleans Parish                            2026:1.5K
  Rowan County                              2026:1.5K
  St. Louis city                            2026:1.8K
  Sumter County                             2026:2.4K
  Union County                              2026:-33.1K
  Warren County                             2026:-11.5K
  Washington County                         2026:-30.9K
  Wayne County                              2026:-23.7K

RATE_M_CI by DATA_AS_OF, dollars = RATE
  -999                                      2026:-6.54M
  0.5-3.4                                   2026:22
  0.6-4.5                                   2026:28.20
  0.7-3.7                                   2026:29.10
  0.7-3.9                                   2026:29.30
  0.7-4.5                                   2026:40.60
  0.7-5.8                                   2026:36.50
  0.8-5.2                                   2026:46.70
  0.8-6.0                                   2026:39.20
  0.8-6.6                                   2026:48.20
  0.8-6.7                                   2026:44.30
  0.9-6.0                                   2026:46.70
  1.0-8.0                                   2026:53.80
  1.1-7.9                                   2026:52.90
  1.1-8.6                                   2026:55.10
  1.2-7.0                                   2026:57.50
  1.2-7.7                                   2026:54.70
  1.2-9.2                                   2026:56.80
  1.2-9.4                                   2026:63.80
  1.3-8.7                                   2026:57.30
  11.0-23.9                                 2026:162.10
  11.9-25.6                                 2026:157
  12.0-27.3                                 2026:181
  6.4-17.0                                  2026:156.30
  7.0-22.3                                  2026:175
  7.2-21.0                                  2026:159.90
  7.7-21.6                                  2026:154.80
  8.3-24.5                                  2026:156.80
  8.4-23.4                                  2026:168.10
  8.6-24.0                                  2026:186.80

## what

ST_NAME: Texas 17%, Georgia 11%, Virginia 9%, Kentucky 8%, Missouri 8%, Kansas 7%, Illinois 7%, North Carolina 7%, Iowa 7%, Tennessee 6%, Nebraska 6%, Indiana 6%

INTENT: FA_Suicide 17%, FA_Deaths 17%, Drug_OD 17%, All_Homicide 17%, All_Suicide 17%, FA_Homicide 17%

PERIOD: TTM 14%, 2023 14%, 2020 14%, 2021 14%, 2024 14%, 2022 14%, 2019 14%

TTM_DATE_RANGE: February, 2025 to January, 202 83%, December, 2024 to November, 20 17%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| GEOID | other | 3.2K | 0 | 08053 666; 09001 664; 08077 664; 08071 664 |
| NAME | who | 1.9K | 0 | Washington County 1.3K; Jefferson County 1.1K; Franklin County 1.0K; Lincoln County 968 |
| ST_GEOID | other | 51 | 0 | 48 10.7K; 13 6.7K; 51 5.6K; 21 5.0K |
| ST_NAME | category | 50 | 0 | Texas 10.7K; Georgia 6.7K; Virginia 5.6K; Kentucky 5.0K |
| INTENT | category | 6 | 0 | FA_Suicide 22.0K; FA_Deaths 22.0K; Drug_OD 22.0K; All_Homicide 22.0K |
| PERIOD | category | 7 | 0 | TTM 18.9K; 2023 18.9K; 2020 18.9K; 2021 18.9K |
| COUNT_SUP | other | 635 | 0 | 1-9 70.5K; 0 30.8K; 10 2.3K; 11 1.9K |
| RATE | amount | 1.0K | 0 | 0.000000000000000 30.8K; -999.0000000000000 6.5K; 14.10000000000000 515; 11.80000000000000 505 |
| RATE_M | amount | 2 | 0 | 1.000000000000000 70.6K; 0.000000000000000 61.4K |
| RATE_M_CI | who | 27.2K | 61.4K | -999 6.5K; 3.0-8.2 324; 1.2-6.5 324; 1.9-5.1 324 |
| DATA_AS_OF | date | 2 | 0 | 2026-05-14T00:00:00.000 113.1K; 2026-06-22T00:00:00.000 18.9K |
| TTM_DATE_RANGE | category | 3 | 113.1K | February, 2025 to January 15.7K; December, 2024 to Novembe 3.1K |
| INGESTED_AT | audit | 1 | 0 | 1782620745491012 132.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | d1307177-68cb-45a7-aa32-8 132.0K |
| SRC_SHA256 | other | 1 | 0 | 4070c54c7aa5b6b3f49f25fa5 132.0K |
