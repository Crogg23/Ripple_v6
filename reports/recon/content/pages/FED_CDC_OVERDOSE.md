# FED_CDC_OVERDOSE

rows 83.8K  columns 15  scan 4.1s

roles: amount 4, audit 2, category 5, other 1, who 3

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| DATA_VALUE | 69.1K | 0 | 306 | 132.1K | 3.54M | 886.67M |
| PERCENT_COMPLETE | 83.8K | 99.50 | 100 | 100 | 100 | 8.38M |
| PERCENT_PENDING_INVESTIGATION | 83.8K | 0 | 0.06 | 1.61 | 2.78 | 11.4K |
| PREDICTED_VALUE | 54.8K | 0 | 307 | 27.9K | 112.4K | 78.46M |

## who

STATE_NAME by rows
      1.6K  Montana
      1.6K  Iowa
      1.6K  Wisconsin
      1.6K  Texas
      1.6K  Oregon
      1.6K  Utah
      1.6K  Vermont
      1.6K  Hawaii
      1.6K  Washington
      1.6K  Indiana
      1.6K  Nevada
      1.6K  Kentucky
      1.6K  Mississippi
      1.6K  Wyoming
      1.6K  Illinois
      1.6K  Florida
      1.6K  Minnesota
      1.6K  South Dakota
      1.6K  New York
      1.6K  Nebraska

STATE_NAME by dollars
     443.56M     1.6K rows  United States
      41.53M     1.6K rows  California
      31.67M     1.6K rows  Florida
      31.11M     1.6K rows  Texas
      19.50M     1.6K rows  Ohio
      19.32M      399 rows  Pennsylvania
      16.40M     1.6K rows  Illinois
      15.42M     1.6K rows  New York
      15.00M     1.6K rows  North Carolina
      14.57M     1.6K rows  Michigan
      13.27M     1.6K rows  Georgia
      12.05M     1.6K rows  Tennessee
      11.44M     1.6K rows  New Jersey
      10.79M     1.6K rows  Virginia
      10.10M     1.6K rows  Indiana
       9.84M     1.6K rows  Arizona
       9.75M     1.6K rows  Missouri
       9.35M     1.6K rows  Massachusetts
       9.20M     1.6K rows  Washington
       9.01M     1.6K rows  New York City

PERIOD by rows
     83.8K  12 month-ending

PERIOD by dollars
     886.67M    83.8K rows  12 month-ending

SRC_SHA256 by rows
     83.8K  2b99be1038f4e5de25704d223e42a0862b2a2d446d9d2e1fa507a0351ae095cb

SRC_SHA256 by dollars
     886.67M    83.8K rows  2b99be1038f4e5de25704d223e42a0862b2a2d446d9d2e1fa507a0351ae0

## what

YEAR: 2025 9%, 2024 9%, 2023 9%, 2022 9%, 2021 9%, 2020 9%, 2019 9%, 2018 9%, 2017 9%, 2016 9%, 2015 9%, 2026 1%

MONTH: January 9%, December 8%, November 8%, October 8%, September 8%, August 8%, July 8%, June 8%, May 8%, April 8%, March 8%, February 8%

INDICATOR: Percent with drugs specified 9%, Number of Drug Overdose Deaths 9%, Number of Deaths 9%, Synthetic opioids, excl. metha 8%, Psychostimulants with abuse po 8%, Opioids (T40.0-T40.4,T40.6) 8%, Natural, semi-synthetic, & syn 8%, Natural & semi-synthetic opioi 8%, Natural & semi-synthetic opioi 8%, Methadone (T40.3) 8%, Heroin (T40.1) 8%, Cocaine (T40.5) 8%

FOOTNOTE: Numbers may differ from publis 73%, Numbers may differ from publis 15%, Underreported due to incomplet 9%, Numbers may differ from publis 2%, Underreported due to incomplet 0%, Underreported due to incomplet 0%

FOOTNOTE_SYMBOL: ** 90%, * 10%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATE | other | 54 | 0 | YC 1.6K; WY 1.6K; WV 1.6K; WI 1.6K |
| YEAR | category | 12 | 0 | 2025 7.6K; 2024 7.6K; 2023 7.6K; 2022 7.6K |
| MONTH | category | 12 | 0 | January 7.6K; December 6.9K; November 6.9K; October 6.9K |
| PERIOD | who | 1 | 0 | 12 month-ending 83.8K |
| INDICATOR | category | 12 | 0 | Percent with drugs specif 7.2K; Number of Drug Overdose D 7.2K; Number of Deaths 7.2K; Synthetic opioids, excl.  6.9K |
| DATA_VALUE | amount | 18.2K | 14.7K | 100 431; 0 392; 28 374; 27 369 |
| PERCENT_COMPLETE | amount | 2 | 0 | 100 83.8K; 99.5 24 |
| PERCENT_PENDING_INVESTIGATION | amount | 6.2K | 0 | 0 10.7K; 0.04497414 374; 0.431370417 370; 0.272755189 370 |
| STATE_NAME | who | 53 | 0 | New York City 1.6K; Wyoming 1.6K; West Virginia 1.6K; Wisconsin 1.6K |
| FOOTNOTE | category | 6 | 0 | Numbers may differ from p 61.5K; Numbers may differ from p 12.4K; Underreported due to inco 7.6K; Numbers may differ from p 1.7K |
| FOOTNOTE_SYMBOL | category | 2 | 0 | ** 75.6K; * 8.2K |
| PREDICTED_VALUE | amount | 5.6K | 29.0K | 0 339; 28 307; 27 297; 29 295 |
| INGESTED_AT | audit | 1 | 0 | 1782620211141584 83.8K |
| SOURCE_RUN_ID | audit | 1 | 0 | 1f0db505-53a9-412a-8fce-2 83.8K |
| SRC_SHA256 | who | 1 | 0 | 2b99be1038f4e5de25704d223 83.8K |
