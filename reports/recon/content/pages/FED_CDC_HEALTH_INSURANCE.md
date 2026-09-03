# FED_CDC_HEALTH_INSURANCE

rows 16.1K  columns 19  scan 4.9s

roles: amount 4, audit 2, category 4, date 2, other 2, who 5

## when

TIME_PERIOD_START_DATE
  2020      4.3K  #############################
  2021      4.4K  ##############################
  2022      2.8K  ###################
  2023      2.5K  #################
  2024      2.0K  ##############

TIME_PERIOD_END_DATE
  2020      4.3K  ##############################
  2021      4.2K  ##############################
  2022      3.0K  #####################
  2023      2.5K  #################
  2024      2.1K  ###############

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PHASE | 14.0K | -1 | 3.20 | 4.20 | 4.20 | 39.4K |
| VALUE | 15.1K | 0.90 | 24 | 86.47 | 93 | 567.1K |
| LOWCI | 15.1K | 0.10 | 20.10 | 82.84 | 92.50 | 510.2K |
| HIGHCI | 15.1K | 2.80 | 28.30 | 90.23 | 95.50 | 627.4K |

## who

QUARTILE_RANGE by rows
       277  Estimate not reliable
        39  6.7-8.9
        37  6.8-8.4
        28  6.5-8.4
        27  9.6-13.8
        27  72.3-77.1
        26  11.7-21.0
        26  5.9-8.5
        26  78.3-81.3
        26  23.5-26.7
        26  10.7-14.8
        26  8.5-10.6
        26  78.3-81.4
        26  78.1-81.4
        26  13.6-21.4
        26  78.2-81.8
        25  11.9-19.9
        24  6.2-7.8
        24  80.4-86.2
        23  82.2-87.0

QUARTILE_RANGE by dollars
        2.1K       26 rows  78.2-81.8
        2.1K       26 rows  78.3-81.4
        2.1K       26 rows  78.1-81.4
        2.1K       26 rows  78.3-81.3
        2.0K       27 rows  72.3-77.1
        2.0K       24 rows  80.4-86.2
        1.9K       23 rows  82.2-87.0
        1.2K       15 rows  77.4-80.2
        1.2K       15 rows  75.2-78.8
        1.2K       15 rows  73.5-78.1
        1.1K       14 rows  80.0-82.1
        1.1K       14 rows  77.7-81.4
        1.1K       14 rows  77.7-80.3
        1.1K       14 rows  76.4-80.9
        1.1K       14 rows  77.1-80.5
        1.1K       14 rows  76.9-80.1
        1.1K       14 rows  75.7-81.1
        1.1K       15 rows  62.4-76.1
        1.1K       14 rows  76.4-79.7
        1.1K       14 rows  75.0-78.5

TIME_PERIOD_LABEL by rows
       225  Apr 26 - May 8, 2023
       225  Apr 2 - Apr 29, 2024
       225  Jul 26 - Aug 7, 2023
       225  Dec 29, 2021 - Jan 10, 2022
       225  Jun 7 - Jun 19, 2023
       225  Mar 5 - Apr 1, 2024
       225  Aug 20 - Sep 16, 2024
       225  Aug 18 - Aug 30, 2021
       225  Sep 1 - Sep 13, 2021
       225  Mar 30 - Apr 11, 2022
       225  Mar 1 - Mar 13, 2023
       225  Jun 1 - Jun 13, 2022
       225  Sep 14 - Sep 26, 2022
       225  Nov 2 - Nov 14, 2022
       225  Sep 15 - Sep 27, 2021
       225  Jun 29 - Jul 11, 2022
       225  Feb 6 - Mar 4, 2024
       225  Aug 23 - Sep 4, 2023
       225  Aug 4 - Aug 16, 2021
       225  Jan 9 - Feb 5, 2024

TIME_PERIOD_LABEL by dollars
        8.4K      225 rows  Jun 28 - Jul 10, 2023
        8.4K      225 rows  Mar 29 - Apr 10, 2023
        8.4K      225 rows  Jul 26 - Aug 7, 2023
        8.4K      225 rows  Jun 7 - Jun 19, 2023
        8.4K      225 rows  Aug 23 - Sep 4, 2023
        8.3K      225 rows  Sep 14 - Sep 26, 2022
        8.3K      225 rows  Feb 1 - Feb 13, 2023
        8.3K      225 rows  Dec 9 - Dec 19, 2022
        8.3K      225 rows  Jul 27 - Aug 8, 2022
        8.3K      225 rows  Apr 26 - May 8, 2023
        8.3K      225 rows  Jun 29 - Jul 11, 2022
        8.3K      225 rows  Mar 1 - Mar 13, 2023
        8.3K      225 rows  Jun 25 - Jul 22, 2024
        8.3K      225 rows  Oct 18 - Oct 30, 2023
        8.3K      225 rows  Oct 5 - Oct 17, 2022
        8.3K      225 rows  Sep 20 - Oct 2, 2023
        8.3K      225 rows  Jan 4 - Jan 16, 2023
        8.3K      225 rows  May 28 - Jun 24, 2024
        8.3K      225 rows  Apr 30 - May 27, 2024
        8.3K      225 rows  Jun 1 - Jun 13, 2022

SUBGROUP by rows
       246  Non-Hispanic White, single race
       246  Non-Hispanic Black, single race
       246  Less than a high school diploma
       246  Female
       246  Non-Hispanic, other races and multiple races
       246  25 - 34 years
       246  18 - 24 years
       246  Male
       246  High school diploma or GED
       246  Non-Hispanic Asian, single race
       246  Some college/Associate's degree
       246  45 - 64 years
       246  Bachelor's degree or higher
       246  United States
       246  Hispanic or Latino
       246  35 - 44 years
       216  Nebraska
       216  North Carolina
       216  Indiana
       216  Montana

SUBGROUP by dollars
        8.4K      246 rows  Non-Hispanic Black, single race
        8.2K      216 rows  New Mexico
        8.2K      216 rows  Arkansas
        8.2K      246 rows  Less than a high school diploma
        8.1K      216 rows  Alabama
        8.1K      216 rows  South Carolina
        8.1K      216 rows  Mississippi
        8.1K      246 rows  Non-Hispanic, other races and multiple races
        8.1K      216 rows  Louisiana
        8.1K      246 rows  High school diploma or GED
        8.1K      216 rows  Virginia
        8.1K      246 rows  45 - 64 years
        8.1K      246 rows  Some college/Associate's degree
        8.1K      216 rows  Alaska
        8.1K      216 rows  New York
        8.1K      216 rows  Hawaii
        8.0K      216 rows  Georgia
        8.0K      216 rows  Florida
        8.0K      216 rows  North Carolina
        8.0K      246 rows  Hispanic or Latino

STATE by rows
      5.0K  United States
       216  Idaho
       216  Washington
       216  Maine
       216  Florida
       216  Alabama
       216  Arizona
       216  South Dakota
       216  New York
       216  Connecticut
       216  Nevada
       216  Virginia
       216  Delaware
       216  Arkansas
       216  Vermont
       216  Alaska
       216  Wyoming
       216  Wisconsin
       216  West Virginia
       216  New Jersey

STATE by dollars
      163.2K     5.0K rows  United States
        8.2K      216 rows  New Mexico
        8.2K      216 rows  Arkansas
        8.1K      216 rows  Alabama
        8.1K      216 rows  South Carolina
        8.1K      216 rows  Mississippi
        8.1K      216 rows  Louisiana
        8.1K      216 rows  Virginia
        8.1K      216 rows  Alaska
        8.1K      216 rows  New York
        8.1K      216 rows  Hawaii
        8.0K      216 rows  Georgia
        8.0K      216 rows  Florida
        8.0K      216 rows  North Carolina
        8.0K      216 rows  Nevada
        8.0K      216 rows  Kentucky
        8.0K      216 rows  Oklahoma
        8.0K      216 rows  California
        8.0K      216 rows  Maryland
        8.0K      216 rows  Idaho

## who x when

QUARTILE_RANGE by TIME_PERIOD_START_DATE, dollars = VALUE
  10.7-14.8                                 2020:327.90
  11.7-21.0                                 2022:236.60 2024:231.40
  11.9-19.9                                 2020:216 2021:187.20
  13.6-21.4                                 2023:482.40
  23.5-26.7                                 2021:648.20
  5.9-8.5                                   2024:194.10
  6.2-7.8                                   2021:77.20 2024:94.80
  6.5-8.4                                   2022:207.40
  6.7-8.9                                   2021:102.30 2024:210.40
  6.8-8.4                                   2021:92.90 2023:105.10 2024:84.30
  72.3-77.1                                 2020:2.0K
  73.5-78.1                                 2021:1.2K
  75.2-78.8                                 2024:1.2K
  75.7-81.1                                 2020:1.1K
  76.4-80.9                                 2020:1.1K
  76.9-80.1                                 2021:1.1K
  77.1-80.5                                 2022:1.1K
  77.4-80.2                                 2022:1.2K
  77.7-80.3                                 2020:1.1K
  77.7-81.4                                 2022:1.1K
  78.1-81.4                                 2020:1.0K 2024:1.0K
  78.2-81.8                                 2021:1.0K 2023:1.0K
  78.3-81.3                                 2020:1.0K 2023:1.0K
  78.3-81.4                                 2021:1.0K 2023:1.0K
  8.5-10.6                                  2020:250.60
  80.0-82.1                                 2023:1.1K
  80.4-86.2                                 2020:993.60 2022:990.20
  82.2-87.0                                 2022:1.0K 2023:927
  9.6-13.8                                  2020:155 2021:169.80
  Estimate not reliable                     2020:35 2021:111 2022:50 2023:43 2024:38

TIME_PERIOD_LABEL by TIME_PERIOD_START_DATE, dollars = VALUE
  Apr 2 - Apr 29, 2024                      2024:8.2K
  Apr 26 - May 8, 2023                      2023:8.3K
  Aug 18 - Aug 30, 2021                     2021:8.2K
  Aug 20 - Sep 16, 2024                     2024:8.2K
  Aug 23 - Sep 4, 2023                      2023:8.4K
  Aug 4 - Aug 16, 2021                      2021:8.2K
  Dec 29, 2021 - Jan 10, 2022               2021:8.2K
  Dec 9 - Dec 19, 2022                      2022:8.3K
  Feb 1 - Feb 13, 2023                      2023:8.3K
  Feb 6 - Mar 4, 2024                       2024:8.2K
  Jan 4 - Jan 16, 2023                      2023:8.3K
  Jan 9 - Feb 5, 2024                       2024:8.2K
  Jul 26 - Aug 7, 2023                      2023:8.4K
  Jul 27 - Aug 8, 2022                      2022:8.3K
  Jun 1 - Jun 13, 2022                      2022:8.3K
  Jun 25 - Jul 22, 2024                     2024:8.3K
  Jun 28 - Jul 10, 2023                     2023:8.4K
  Jun 29 - Jul 11, 2022                     2022:8.3K
  Jun 7 - Jun 19, 2023                      2023:8.4K
  Mar 1 - Mar 13, 2023                      2023:8.3K
  Mar 29 - Apr 10, 2023                     2023:8.4K
  Mar 30 - Apr 11, 2022                     2022:8.2K
  Mar 5 - Apr 1, 2024                       2024:8.2K
  Nov 2 - Nov 14, 2022                      2022:8.2K
  Oct 18 - Oct 30, 2023                     2023:8.3K
  Oct 5 - Oct 17, 2022                      2022:8.3K
  Sep 1 - Sep 13, 2021                      2021:8.2K
  Sep 14 - Sep 26, 2022                     2022:8.3K
  Sep 15 - Sep 27, 2021                     2021:8.2K
  Sep 20 - Oct 2, 2023                      2023:8.3K

## what

INDICATOR: Private Health Insurance Cover 33%, Public Health Insurance Covera 33%, Uninsured at the Time of Inter 33%

C_GROUP: By State 69%, By Race/Hispanic ethnicity 8%, By Education 6%, By Age 6%, By Sex 3%, By Sexual orientation 2%, By Gender identity 2%, By Disability status 2%, National Estimate 2%

QUARTILE_NUMBER: 2 25%, 3 25%, 1 24%, 4 23%, -1 3%

SUPPRESSION_FLAG: 1 100%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDICATOR | category | 3 | 0 | Private Health Insurance  5.4K; Public Health Insurance C 5.4K; Uninsured at the Time of  5.4K |
| C_GROUP | category | 9 | 0 | By State 11.0K; By Race/Hispanic ethnicit 1.2K; By Education 984; By Age 984 |
| STATE | who | 51 | 0 | United States 5.0K; Wyoming 216; Wisconsin 216; West Virginia 216 |
| SUBGROUP | who | 75 | 0 | Bachelor's degree or high 246; Some college/Associate's  246; High school diploma or GE 246; Less than a high school d 246 |
| PHASE | amount | 17 | 0 | 1 2.4K; 3.1 1.9K; 3.2 1.4K; 3 (Jan 6 - Mar 29) 1.2K |
| TIME_PERIOD | other | 72 | 0 | 1 813; 72 225; 71 225; 70 225 |
| TIME_PERIOD_LABEL | who | 81 | 0 | Aug 20 - Sep 16, 2024 225; Jul 23 - Aug 19, 2024 225; Jun 25 - Jul 22, 2024 225; May 28 - Jun 24, 2024 225 |
| TIME_PERIOD_START_DATE | date | 83 | 0 | 2024-08-20T00:00:00.000 225; 2024-07-23T00:00:00.000 225; 2024-06-25T00:00:00.000 225; 2024-05-28T00:00:00.000 225 |
| TIME_PERIOD_END_DATE | date | 83 | 0 | 2024-09-16T00:00:00.000 225; 2024-08-19T00:00:00.000 225; 2024-07-22T00:00:00.000 225; 2024-06-24T00:00:00.000 225 |
| VALUE | amount | 798 | 911 | 9.1 89; 78 82; 8.9 80; 6.9 80 |
| LOWCI | amount | 798 | 911 | 6.4 85; 8 83; 8.2 83; 6.8 81 |
| HIGHCI | amount | 828 | 911 | 12.1 81; 10.2 81; 83.7 79; 29.7 79 |
| CONFIDENCE_INTERVAL | other | 12.9K | 911 | 73.3 - 87.8 77; 80.5 - 89.5 77; 56.7 - 70.6 77; 80.0 - 86.3 77 |
| QUARTILE_RANGE | who | 837 | 5.0K | Estimate not reliable 277; 6.7-8.9 65; 5.9-8.5 65; 74.9-77.4 63 |
| QUARTILE_NUMBER | category | 6 | 5.0K | 2 2.8K; 3 2.8K; 1 2.7K; 4 2.6K |
| SUPPRESSION_FLAG | category | 2 | 15.8K | 1 299 |
| INGESTED_AT | audit | 1 | 0 | 1782620754288220 16.1K |
| SOURCE_RUN_ID | audit | 1 | 0 | 11a3daf2-42bb-462a-84ef-6 16.1K |
| SRC_SHA256 | who | 1 | 0 | aba65d394dc7d6f871216ad12 16.1K |
