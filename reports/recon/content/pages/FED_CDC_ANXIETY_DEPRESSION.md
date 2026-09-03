# FED_CDC_ANXIETY_DEPRESSION

rows 16.8K  columns 17  scan 4.9s

roles: amount 4, audit 2, category 2, date 2, other 2, who 5

## when

TIME_PERIOD_START_DATE
  2020      4.5K  #############################
  2021      4.6K  ##############################
  2022      2.9K  ###################
  2023      2.7K  #################
  2024      2.1K  ##############

TIME_PERIOD_END_DATE
  2020      4.5K  ##############################
  2021      4.4K  ##############################
  2022      3.1K  #####################
  2023      2.6K  #################
  2024      2.2K  ###############

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PHASE | 14.7K | -1 | 3.20 | 4.20 | 4.20 | 40.9K |
| VALUE | 16.1K | 4.60 | 27.70 | 56.54 | 85.20 | 452.7K |
| LOWCI | 16.1K | 3.30 | 24.10 | 51.97 | 79.90 | 396.4K |
| HIGHCI | 16.1K | 6 | 31.60 | 61.89 | 89.50 | 513.1K |

## who

QUARTILE_RANGE by rows
        37  23.2-27.3
        27  12.1-13.8
        27  14.9-19.5
        27  28.8-31.4
        27  23.4-25.7
        26  23.9-29.4
        26  29.5-32.0
        26  28.6-31.7
        26  19.6-21.2
        26  21.6-26.2
        25  21.3-22.7
        25  27.4-29.8
        25  33.4-36.0
        25  19.4-21.5
        25  19.2-20.8
        25  23.6-29.7
        25  33.2-35.5
        25  22.4-24.6
        25  19.6-21.3
        25  23.9-26.0

QUARTILE_RANGE by dollars
      927.10       37 rows  23.2-27.3
      891.50       24 rows  35.2-39.4
      872.20       25 rows  33.4-36.0
      859.60       25 rows  33.2-35.5
      820.90       27 rows  28.8-31.4
      803.90       26 rows  29.5-32.0
      795.90       23 rows  31.8-37.1
      787.60       26 rows  28.6-31.7
         716       25 rows  27.4-29.8
      715.20       26 rows  23.9-29.4
      691.20       24 rows  26.9-31.8
      671.70       27 rows  23.4-25.7
      667.60       25 rows  23.6-29.7
      641.70       26 rows  21.6-26.2
         622       25 rows  23.9-26.0
      597.40       14 rows  41.7-43.6
      592.30       25 rows  22.4-24.6
         582       14 rows  40.5-42.8
      559.50       13 rows  41.6-44.3
      559.10       12 rows  44.2-50.0

TIME_PERIOD_LABEL by rows
       234  Sep 29 - Oct 11, 2021
       234  Jun 7 - Jun 19, 2023
       234  Jul 23 - Aug 19, 2024
       234  Jun 29 - Jul 11, 2022
       234  Apr 27 - May 9, 2022
       234  Aug 23 - Sep 4, 2023
       234  Jul 21 - Aug 2, 2021
       234  Jan 4 - Jan 16, 2023
       234  Apr 30 - May 27, 2024
       234  Mar 1 - Mar 13, 2023
       234  Jun 28 - Jul 10, 2023
       234  Sep 14 - Sep 26, 2022
       234  Feb 1 - Feb 13, 2023
       234  May 28 - Jun 24, 2024
       234  Aug 20 - Sep 16, 2024
       234  Apr 26 - May 8, 2023
       234  Mar 30 - Apr 11, 2022
       234  Jan 26 - Feb 7, 2022
       234  Sep 20 - Oct 2, 2023
       234  Mar 29 - Apr 10, 2023

TIME_PERIOD_LABEL by dollars
        7.5K      210 rows  Dec 9 - Dec 21, 2020
        7.5K      210 rows  Nov 11 - Nov 23, 2020
        7.4K      234 rows  Oct 5 - Oct 17, 2022
        7.4K      210 rows  Nov 25 - Dec 7, 2020
        7.4K      234 rows  Sep 14 - Sep 26, 2022
        7.3K      210 rows  July 16 - July 21, 2020
        7.3K      210 rows  Oct 28 - Nov 9, 2020
        7.3K      210 rows  Jan 6 - Jan 18, 2021
        7.2K      234 rows  Nov 2 - Nov 14, 2022
        7.2K      210 rows  Jan 20 - Feb 1, 2021
        7.0K      210 rows  July 9 - July 14, 2020
        7.0K      234 rows  Oct 18 - Oct 30, 2023
        6.9K      210 rows  Feb 3 - Feb 15, 2021
        6.9K      234 rows  Jun 29 - Jul 11, 2022
        6.9K      234 rows  Dec 9 - Dec 19, 2022
        6.9K      210 rows  July 2 - July 7, 2020
        6.9K      234 rows  Sep 20 - Oct 2, 2023
        6.8K      210 rows  Feb 17 - Mar 1, 2021
        6.8K      234 rows  Jun 1 - Jun 13, 2022
        6.7K      234 rows  Dec 29, 2021 - Jan 10, 2022

SUBGROUP by rows
       246  50 - 59 years
       246  70 - 79 years
       246  Non-Hispanic Asian, single race
       246  Bachelor's degree or higher
       246  30 - 39 years
       246  40 - 49 years
       246  18 - 29 years
       246  60 - 69 years
       246  Non-Hispanic, other races and multiple races
       246  Hispanic or Latino
       246  Female
       246  80 years and above
       246  Male
       246  High school diploma or GED
       246  Less than a high school diploma
       246  Some college/Associate's degree
       246  Non-Hispanic Black, single race
       246  Non-Hispanic White, single race
       246  United States
       216  New Mexico

SUBGROUP by dollars
        8.9K      246 rows  18 - 29 years
        7.9K      246 rows  Non-Hispanic, other races and multiple races
        7.5K      246 rows  Less than a high school diploma
        7.2K      246 rows  30 - 39 years
        7.2K      156 rows  With disability
        7.0K      216 rows  Louisiana
        7.0K      132 rows  Transgender
        6.9K      216 rows  Mississippi
        6.8K      246 rows  Hispanic or Latino
        6.8K      246 rows  Some college/Associate's degree
        6.7K      216 rows  Oklahoma
        6.7K      216 rows  West Virginia
        6.7K      216 rows  Nevada
        6.6K      246 rows  Female
        6.6K      216 rows  Arkansas
        6.6K      216 rows  Kentucky
        6.6K      216 rows  New Mexico
        6.5K      216 rows  Oregon
        6.5K      216 rows  Texas
        6.4K      246 rows  40 - 49 years

STATE by rows
      5.8K  United States
       216  Vermont
       216  Utah
       216  Arkansas
       216  Alaska
       216  New Hampshire
       216  Massachusetts
       216  Washington
       216  Florida
       216  Connecticut
       216  Alabama
       216  Maine
       216  Missouri
       216  Arizona
       216  Wyoming
       216  Idaho
       216  Mississippi
       216  Kansas
       216  Illinois
       216  Indiana

STATE by dollars
      149.6K     5.8K rows  United States
        7.0K      216 rows  Louisiana
        6.9K      216 rows  Mississippi
        6.7K      216 rows  Oklahoma
        6.7K      216 rows  West Virginia
        6.7K      216 rows  Nevada
        6.6K      216 rows  Arkansas
        6.6K      216 rows  Kentucky
        6.6K      216 rows  New Mexico
        6.5K      216 rows  Oregon
        6.5K      216 rows  Texas
        6.4K      216 rows  Alabama
        6.3K      216 rows  California
        6.3K      216 rows  Tennessee
        6.2K      216 rows  Georgia
        6.2K      216 rows  Arizona
        6.2K      216 rows  Florida
        6.1K      216 rows  Alaska
        6.1K      216 rows  Washington
        6.1K      216 rows  Missouri

## who x when

QUARTILE_RANGE by TIME_PERIOD_START_DATE, dollars = VALUE
  12.1-13.8                                 2024:349.60
  14.9-19.5                                 2023:249.50 2024:237.60
  19.2-20.8                                 2024:502.30
  19.4-21.5                                 2021:269.10 2024:243.60
  19.6-21.2                                 2021:265.50 2024:263.80
  19.6-21.3                                 2023:515.40
  21.3-22.7                                 2023:265 2024:286.70
  21.6-26.2                                 2020:320.50 2021:321.20
  22.4-24.6                                 2021:308.90 2024:283.40
  23.2-27.3                                 2021:657.50 2024:269.60
  23.4-25.7                                 2021:348.20 2022:323.50
  23.6-29.7                                 2023:667.60
  23.9-26.0                                 2020:295.90 2021:326.10
  23.9-29.4                                 2021:360.70 2023:354.50
  26.9-31.8                                 2020:691.20
  27.4-29.8                                 2021:716
  28.6-31.7                                 2022:787.60
  28.8-31.4                                 2021:426.80 2022:394.10
  29.5-32.0                                 2023:803.90
  31.8-37.1                                 2020:795.90
  33.2-35.5                                 2020:412.10 2021:447.50
  33.4-36.0                                 2021:421.30 2022:450.90
  35.2-39.4                                 2023:891.50
  40.5-42.8                                 2021:582
  41.6-44.3                                 2020:559.50
  41.7-43.6                                 2020:597.40
  44.2-50.0                                 2020:559.10

TIME_PERIOD_LABEL by TIME_PERIOD_START_DATE, dollars = VALUE
  Apr 26 - May 8, 2023                      2023:6.6K
  Apr 27 - May 9, 2022                      2022:6.4K
  Apr 30 - May 27, 2024                     2024:4.4K
  Aug 20 - Sep 16, 2024                     2024:4.3K
  Aug 23 - Sep 4, 2023                      2023:5.9K
  Dec 9 - Dec 21, 2020                      2020:7.5K
  Feb 1 - Feb 13, 2023                      2023:6.6K
  Jan 20 - Feb 1, 2021                      2021:7.2K
  Jan 26 - Feb 7, 2022                      2022:6.6K
  Jan 4 - Jan 16, 2023                      2023:6.5K
  Jan 6 - Jan 18, 2021                      2021:7.3K
  Jul 21 - Aug 2, 2021                      2021:6.5K
  Jul 23 - Aug 19, 2024                     2024:4.3K
  July 16 - July 21, 2020                   2020:7.3K
  July 9 - July 14, 2020                    2020:7.0K
  Jun 28 - Jul 10, 2023                     2023:6.6K
  Jun 29 - Jul 11, 2022                     2022:6.9K
  Jun 7 - Jun 19, 2023                      2023:6.6K
  Mar 1 - Mar 13, 2023                      2023:6.7K
  Mar 29 - Apr 10, 2023                     2023:6.6K
  Mar 30 - Apr 11, 2022                     2022:6.5K
  May 28 - Jun 24, 2024                     2024:4.2K
  Nov 11 - Nov 23, 2020                     2020:7.5K
  Nov 2 - Nov 14, 2022                      2022:7.2K
  Nov 25 - Dec 7, 2020                      2020:7.4K
  Oct 28 - Nov 9, 2020                      2020:7.3K
  Oct 5 - Oct 17, 2022                      2022:7.4K
  Sep 14 - Sep 26, 2022                     2022:7.4K
  Sep 20 - Oct 2, 2023                      2023:6.9K
  Sep 29 - Oct 11, 2021                     2021:6.5K

## what

INDICATOR: Symptoms of Anxiety Disorder o 33%, Symptoms of Anxiety Disorder 33%, Symptoms of Depressive Disorde 33%

C_GROUP: By State 66%, By Age 10%, By Race/Hispanic ethnicity 7%, By Education 6%, By Sex 3%, By Sexual orientation 2%, By Gender identity 2%, By Disability status 2%, National Estimate 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| INDICATOR | category | 3 | 0 | Symptoms of Anxiety Disor 5.6K; Symptoms of Anxiety Disor 5.6K; Symptoms of Depressive Di 5.6K |
| C_GROUP | category | 9 | 0 | By State 11.0K; By Age 1.7K; By Race/Hispanic ethnicit 1.2K; By Education 984 |
| STATE | who | 51 | 0 | United States 5.8K; Wyoming 216; Wisconsin 216; West Virginia 216 |
| SUBGROUP | who | 78 | 0 | Bachelor's degree or high 246; Some college/Associate's  246; High school diploma or GE 246; Less than a high school d 246 |
| PHASE | amount | 17 | 0 | 1 2.5K; 3.1 2.0K; 3.2 1.4K; 3.0 (Jan 6 - Mar 29) 1.3K |
| TIME_PERIOD | other | 72 | 0 | 1 912; 72 234; 71 234; 70 234 |
| TIME_PERIOD_LABEL | who | 81 | 0 | Aug 20 - Sep 16, 2024 234; Jul 23 - Aug 19, 2024 234; Jun 25 - Jul 22, 2024 234; May 28 - Jun 24, 2024 234 |
| TIME_PERIOD_START_DATE | date | 83 | 0 | 2024-08-20T00:00:00.000 234; 2024-07-23T00:00:00.000 234; 2024-06-25T00:00:00.000 234; 2024-05-28T00:00:00.000 234 |
| TIME_PERIOD_END_DATE | date | 83 | 0 | 2024-09-16T00:00:00.000 234; 2024-08-19T00:00:00.000 234; 2024-07-22T00:00:00.000 234; 2024-06-24T00:00:00.000 234 |
| VALUE | amount | 600 | 707 | 26.5 94; 31.4 94; 19 91; 14.7 90 |
| LOWCI | amount | 562 | 707 | 21.4 107; 25.1 99; 21.7 96; 23.4 93 |
| HIGHCI | amount | 637 | 707 | 31.4 92; 25.4 91; 21.5 90; 36.8 90 |
| CONFIDENCE_INTERVAL | other | 12.6K | 707 | 17.0 - 19.3 82; 19.3 - 32.8 81; 13.4 - 21.2 81; 21.5 - 31.4 81 |
| QUARTILE_RANGE | who | 842 | 5.8K | 12.1-13.8 66; 19.2-20.8 65; 14.9-19.5 65; 13.0-16.3 64 |
| INGESTED_AT | audit | 1 | 0 | 1782620738476426 16.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | 8f7d3388-980c-4b61-806e-f 16.8K |
| SRC_SHA256 | who | 1 | 0 | da30d844692414767ebfb19f9 16.8K |
