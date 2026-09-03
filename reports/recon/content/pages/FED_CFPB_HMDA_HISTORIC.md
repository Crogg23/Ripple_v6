# FED_CFPB_HMDA_HISTORIC

rows 19.14M  columns 81  scan 26.6s

roles: amount 4, audit 2, category 44, date 1, empty 6, id 1, other 19, state 1, who 5

## when

_INGESTED_AT
  2026    19.14M  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LOAN_AMOUNT_000S | 19.13M | 1 | 205 | 1.0K | 320.0K | 4.86B |
| RATE_SPREAD | 1.04M | 1.50 | 1.80 | 5.26 | 99.99 | 2.11M |
| MINORITY_POPULATION | 19.10M | 0 | 21.98 | 97.21 | 100 | 568.21M |
| TRACT_TO_MSAMD_INCOME | 19.10M | 0 | 112.57 | 251.02 | 507.47 | 2.26B |

## who

MSAMD_NAME by rows
    509.1K  Los Angeles, Long Beach, Glendale - CA
    453.7K  Chicago, Naperville, Arlington Heights - IL
    428.2K  Atlanta, Sandy Springs, Roswell - GA
    416.2K  Phoenix, Mesa, Scottsdale - AZ
    410.4K  New York, Jersey City, White Plains - NY, NJ
    390.5K  Washington, Arlington, Alexandria - DC, VA, MD, WV
    353.4K  Denver, Aurora, Lakewood - CO
    352.9K  Houston, The Woodlands, Sugar Land - TX
    335.4K  Riverside, San Bernardino, Ontario - CA
    312.3K  Dallas, Plano, Irving - TX
    305.5K  Minneapolis, St. Paul, Bloomington - MN, WI
    267.0K  Seattle, Bellevue, Everett - WA
    246.6K  San Diego, Carlsbad - CA
    235.1K  Oakland, Hayward, Berkeley - CA
    220.2K  Portland, Vancouver, Hillsboro - OR, WA
    219.3K  Warren, Troy, Farmington Hills - MI
    215.3K  Anaheim, Santa Ana, Irvine - CA
    208.8K  St. Louis - MO, IL
    207.9K  Sacramento, Roseville, Arden-Arcade - CA
    196.9K  Charlotte, Concord, Gastonia - NC, SC

MSAMD_NAME by dollars
     241.68M   509.1K rows  Los Angeles, Long Beach, Glendale - CA
     167.20M   410.4K rows  New York, Jersey City, White Plains - NY, NJ
     150.43M   390.5K rows  Washington, Arlington, Alexandria - DC, VA, MD, WV
     121.52M   453.7K rows  Chicago, Naperville, Arlington Heights - IL
     114.59M   235.1K rows  Oakland, Hayward, Berkeley - CA
     108.66M   215.3K rows  Anaheim, Santa Ana, Irvine - CA
     107.30M   246.6K rows  San Diego, Carlsbad - CA
     104.52M   353.4K rows  Denver, Aurora, Lakewood - CO
     103.70M   267.0K rows  Seattle, Bellevue, Everett - WA
      99.61M   428.2K rows  Atlanta, Sandy Springs, Roswell - GA
      98.96M   416.2K rows  Phoenix, Mesa, Scottsdale - AZ
      93.83M   335.4K rows  Riverside, San Bernardino, Ontario - CA
      88.29M   142.5K rows  San Jose, Sunnyvale, Santa Clara - CA
      83.98M   352.9K rows  Houston, The Woodlands, Sugar Land - TX
      80.85M   312.3K rows  Dallas, Plano, Irving - TX
      71.23M   305.5K rows  Minneapolis, St. Paul, Bloomington - MN, WI
      67.01M    90.9K rows  San Francisco, Redwood City, South San Francisco - CA
      63.35M   220.2K rows  Portland, Vancouver, Hillsboro - OR, WA
      62.82M   207.9K rows  Sacramento, Roseville, Arden-Arcade - CA
      61.58M   166.2K rows  Cambridge, Newton, Framingham - MA

COUNTY_NAME by rows
    509.3K  Los Angeles County
    380.9K  Maricopa County
    320.1K  Orange County
    283.1K  Cook County
    246.7K  San Diego County
    236.0K  Clark County
    234.0K  Montgomery County
    222.7K  Jefferson County
    205.1K  Harris County
    191.4K  Riverside County
    187.3K  King County
    180.2K  Washington County
    161.8K  Middlesex County
    144.1K  San Bernardino County
    137.0K  Santa Clara County
    130.4K  Douglas County
    128.9K  Franklin County
    127.2K  Sacramento County
    125.3K  Lake County
    123.8K  Alameda County

COUNTY_NAME by dollars
     241.80M   509.3K rows  Los Angeles County
     133.57M   320.1K rows  Orange County
     107.34M   246.7K rows  San Diego County
      92.80M   380.9K rows  Maricopa County
      86.12M   137.0K rows  Santa Clara County
      80.54M   283.1K rows  Cook County
      78.18M   187.3K rows  King County
      65.13M   234.0K rows  Montgomery County
      62.47M   123.8K rows  Alameda County
      57.49M   161.8K rows  Middlesex County
      55.33M   191.4K rows  Riverside County
      55.04M   236.0K rows  Clark County
      52.16M   111.3K rows  Contra Costa County
      48.71M   205.1K rows  Harris County
      48.03M   222.7K rows  Jefferson County
      41.36M   180.2K rows  Washington County
      39.00M    89.0K rows  Fairfax County
      38.53M   144.1K rows  San Bernardino County
      38.28M    52.9K rows  San Mateo County
      35.10M   127.2K rows  Sacramento County

STATE_NAME by rows
     2.57M  California
     1.43M  Texas
     1.16M  Florida
    748.6K  Illinois
    645.3K  Ohio
    633.4K  Pennsylvania
    624.5K  Michigan
    622.5K  Georgia
    607.9K  North Carolina
    605.6K  Colorado
    600.1K  Washington
    582.9K  Virginia
    569.2K  New York
    545.8K  Arizona
    457.3K  New Jersey
    442.6K  Massachusetts
    419.7K  Indiana
    413.2K  Minnesota
    407.3K  Maryland
    404.7K  Tennessee

STATE_NAME by dollars
       1.07B    2.57M rows  California
     320.24M    1.43M rows  Texas
     262.37M    1.16M rows  Florida
     184.80M   600.1K rows  Washington
     179.39M   569.2K rows  New York
     174.56M   582.9K rows  Virginia
     171.60M   748.6K rows  Illinois
     171.35M   605.6K rows  Colorado
     145.55M   442.6K rows  Massachusetts
     139.13M   457.3K rows  New Jersey
     133.54M   622.5K rows  Georgia
     127.61M   607.9K rows  North Carolina
     126.21M   407.3K rows  Maryland
     124.30M   545.8K rows  Arizona
     121.87M   633.4K rows  Pennsylvania
     106.94M   624.5K rows  Michigan
     105.19M   645.3K rows  Ohio
      88.41M   413.2K rows  Minnesota
      80.81M   306.3K rows  Oregon
      80.03M   404.7K rows  Tennessee

APPLICANT_INCOME_000S by rows
    221.5K  60
    202.5K  50
    191.7K  52
    187.3K  55
    187.1K  48
    187.0K  65
    184.2K  70
    179.7K  62
    179.0K  75
    175.8K  42
    173.4K  54
    172.4K  80
    171.9K  58
    169.5K  53
    169.1K  56
    168.4K  45
    167.4K  57
    166.6K  72
    166.1K  40
    163.7K  46

APPLICANT_INCOME_000S by dollars
      39.33M   221.5K rows  60
      37.76M   172.4K rows  80
      37.42M   179.0K rows  75
      37.24M   156.0K rows  90
      36.57M   142.8K rows  100
      36.56M   184.2K rows  70
      35.54M   155.7K rows  85
      35.25M   187.0K rows  65
      33.73M   166.6K rows  72
      33.48M   114.6K rows  120
      32.64M   132.1K rows  95
      32.62M   179.7K rows  62
      31.83M   148.1K rows  78
      31.80M   116.4K rows  110
      31.45M   202.5K rows  50
      31.20M   187.3K rows  55
      31.19M   152.4K rows  73
      30.92M   136.8K rows  84
      30.76M   144.8K rows  77
      30.74M   158.1K rows  68

## who x when

MSAMD_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = LOAN_AMOUNT_000S
  Anaheim, Santa Ana, Irvine - CA           2026:108.66M
  Atlanta, Sandy Springs, Roswell - GA      2026:99.61M
  Cambridge, Newton, Framingham - MA        2026:61.58M
  Charlotte, Concord, Gastonia - NC, SC     2026:45.71M
  Chicago, Naperville, Arlington Heights -  2026:121.52M
  Dallas, Plano, Irving - TX                2026:80.85M
  Denver, Aurora, Lakewood - CO             2026:104.52M
  Houston, The Woodlands, Sugar Land - TX   2026:83.98M
  Los Angeles, Long Beach, Glendale - CA    2026:241.68M
  Minneapolis, St. Paul, Bloomington - MN,  2026:71.23M
  New York, Jersey City, White Plains - NY  2026:167.20M
  Oakland, Hayward, Berkeley - CA           2026:114.59M
  Phoenix, Mesa, Scottsdale - AZ            2026:98.96M
  Portland, Vancouver, Hillsboro - OR, WA   2026:63.35M
  Riverside, San Bernardino, Ontario - CA   2026:93.83M
  Sacramento, Roseville, Arden-Arcade - CA  2026:62.82M
  San Diego, Carlsbad - CA                  2026:107.30M
  San Francisco, Redwood City, South San F  2026:67.01M
  San Jose, Sunnyvale, Santa Clara - CA     2026:88.29M
  Seattle, Bellevue, Everett - WA           2026:103.70M
  St. Louis - MO, IL                        2026:40.26M
  Warren, Troy, Farmington Hills - MI       2026:43.88M
  Washington, Arlington, Alexandria - DC,   2026:150.43M

COUNTY_NAME by _INGESTED_AT  LOAD STAMP, not an event date, dollars = LOAN_AMOUNT_000S
  Alameda County                            2026:62.47M
  Clark County                              2026:55.04M
  Contra Costa County                       2026:52.16M
  Cook County                               2026:80.54M
  Douglas County                            2026:33.25M
  Fairfax County                            2026:39.00M
  Franklin County                           2026:22.92M
  Harris County                             2026:48.71M
  Jefferson County                          2026:48.03M
  King County                               2026:78.18M
  Lake County                               2026:27.27M
  Los Angeles County                        2026:241.80M
  Maricopa County                           2026:92.80M
  Middlesex County                          2026:57.49M
  Montgomery County                         2026:65.13M
  Orange County                             2026:133.57M
  Riverside County                          2026:55.33M
  Sacramento County                         2026:35.10M
  San Bernardino County                     2026:38.53M
  San Diego County                          2026:107.34M
  San Mateo County                          2026:38.28M
  Santa Clara County                        2026:86.12M
  Washington County                         2026:41.36M

## where

STATE_ABBR: CA 2.57M, TX 1.43M, FL 1.16M, IL 748.6K, OH 645.3K, PA 633.4K, MI 624.5K, GA 622.5K, NC 607.9K, CO 605.6K, WA 600.1K, VA 582.9K

## what

AS_OF_YEAR: 2016 37%, 2015 32%, 2017 31%

SOURCE_YEAR: 2016 37%, 2015 32%, 2017 31%

AGENCY_NAME: Department of Housing and Urba 51%, Consumer Financial Protection  24%, Federal Deposit Insurance Corp 9%, National Credit Union Administ 7%, Office of the Comptroller of t 5%, Federal Reserve System 3%

AGENCY_ABBR: HUD 51%, CFPB 24%, FDIC 9%, NCUA 7%, OCC 5%, FRS 3%

AGENCY_CODE: 7 51%, 9 24%, 3 9%, 5 7%, 1 5%, 2 3%

LOAN_TYPE_NAME: Conventional 69%, FHA-insured 19%, VA-guaranteed 11%, FSA/RHS-guaranteed 2%

LOAN_TYPE: 1 69%, 2 19%, 3 11%, 4 2%

LOAN_PURPOSE_NAME: Home purchase 53%, Refinancing 43%, Home improvement 3%

LOAN_PURPOSE: 1 53%, 3 43%, 2 3%

PREAPPROVAL_NAME: Not applicable 79%, Preapproval was not requested 18%, Preapproval was requested 4%

PREAPPROVAL: 3 79%, 2 18%, 1 4%

APPLICANT_ETHNICITY_NAME: Not Hispanic or Latino 81%, Information not provided by ap 10%, Hispanic or Latino 9%, Not applicable 0%

APPLICANT_ETHNICITY: 2 81%, 3 10%, 1 9%, 4 0%

CO_APPLICANT_ETHNICITY_NAME: No co-applicant 52%, Not Hispanic or Latino 38%, Information not provided by ap 5%, Hispanic or Latino 4%, Not applicable 0%

CO_APPLICANT_ETHNICITY: 5 52%, 2 38%, 3 5%, 1 4%, 4 0%

APPLICANT_RACE_NAME_1: White 77%, Information not provided by ap 10%, Black or African American 6%, Asian 6%, American Indian or Alaska Nati 1%, Native Hawaiian or Other Pacif 0%, Not applicable 0%

APPLICANT_RACE_1: 5 77%, 6 10%, 3 6%, 2 6%, 1 1%, 4 0%, 7 0%

APPLICANT_RACE_NAME_2: White 75%, Black or African American 9%, Native Hawaiian or Other Pacif 8%, Asian 5%, American Indian or Alaska Nati 3%

APPLICANT_RACE_2: 5 75%, 3 9%, 4 8%, 2 5%, 1 3%

APPLICANT_RACE_NAME_3: White 71%, Black or African American 17%, Native Hawaiian or Other Pacif 7%, American Indian or Alaska Nati 3%, Asian 2%

APPLICANT_RACE_3: 5 71%, 3 17%, 4 7%, 1 3%, 2 2%

APPLICANT_RACE_NAME_4: Native Hawaiian or Other Pacif 59%, White 34%, Asian 4%, Black or African American 2%, American Indian or Alaska Nati 2%

APPLICANT_RACE_4: 4 59%, 5 34%, 2 4%, 3 2%, 1 2%

APPLICANT_RACE_NAME_5: White 91%, American Indian or Alaska Nati 4%, Black or African American 2%, Asian 2%, Native Hawaiian or Other Pacif 2%

APPLICANT_RACE_5: 5 91%, 1 4%, 3 2%, 2 2%, 4 2%

CO_APPLICANT_RACE_NAME_1: No co-applicant 52%, White 37%, Information not provided by ap 6%, Asian 3%, Black or African American 2%, Native Hawaiian or Other Pacif 0%, American Indian or Alaska Nati 0%, Not applicable 0%

CO_APPLICANT_RACE_1: 8 52%, 5 37%, 6 6%, 2 3%, 3 2%, 4 0%, 1 0%, 7 0%

CO_APPLICANT_RACE_NAME_2: White 74%, Native Hawaiian or Other Pacif 10%, Black or African American 7%, Asian 6%, American Indian or Alaska Nati 3%

CO_APPLICANT_RACE_2: 5 74%, 4 10%, 3 7%, 2 6%, 1 3%

CO_APPLICANT_RACE_NAME_3: White 68%, Black or African American 16%, Native Hawaiian or Other Pacif 11%, American Indian or Alaska Nati 3%, Asian 2%

CO_APPLICANT_RACE_3: 5 68%, 3 16%, 4 11%, 1 3%, 2 2%

CO_APPLICANT_RACE_NAME_4: Native Hawaiian or Other Pacif 52%, White 42%, Asian 3%, Black or African American 2%, American Indian or Alaska Nati 1%

CO_APPLICANT_RACE_4: 4 52%, 5 42%, 2 3%, 3 2%, 1 1%

CO_APPLICANT_RACE_NAME_5: White 87%, American Indian or Alaska Nati 7%, Asian 3%, Black or African American 2%, Native Hawaiian or Other Pacif 1%

CO_APPLICANT_RACE_5: 5 87%, 1 7%, 2 3%, 3 2%, 4 1%

APPLICANT_SEX_NAME: Male 66%, Female 28%, Information not provided by ap 6%, Not applicable 0%

APPLICANT_SEX: 1 66%, 2 28%, 3 6%, 4 0%

CO_APPLICANT_SEX_NAME: No co-applicant 52%, Female 36%, Male 9%, Information not provided by ap 3%, Not applicable 0%

CO_APPLICANT_SEX: 5 52%, 2 36%, 1 9%, 3 3%, 4 0%

PURCHASER_TYPE_NAME: Fannie Mae (FNMA) 21%, Loan was not originated or was 20%, Ginnie Mae (GNMA) 16%, Freddie Mac (FHLMC) 14%, Life insurance company, credit 11%, Commercial bank, savings bank  11%, Other type of purchaser 6%, Affiliate institution 1%, Private securitization 1%, Farmer Mac (FAMC) 0%

PURCHASER_TYPE: 1 21%, 0 20%, 2 16%, 3 14%, 7 11%, 6 11%, 9 6%, 8 1%, 5 1%, 4 0%

HOEPA_STATUS_NAME: Not a HOEPA loan 100%, HOEPA loan 0%

HOEPA_STATUS: 2 100%, 1 0%

APPLICATION_DATE_INDICATOR: 0 100%, 1 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AS_OF_YEAR | category | 3 | 0 | 2016 7.04M; 2015 6.11M; 2017 5.99M |
| SOURCE_YEAR | category | 3 | 0 | 2016 7.04M; 2015 6.11M; 2017 5.99M |
| RESPONDENT_ID | other | 7.0K | 0 | 7197000003 1.13M; 0000451965 980.4K; 0000852218 440.0K; 0000480228 383.4K |
| AGENCY_NAME | category | 6 | 0 | Department of Housing and 9.77M; Consumer Financial Protec 4.68M; Federal Deposit Insurance 1.81M; National Credit Union Adm 1.31M |
| AGENCY_ABBR | category | 6 | 0 | HUD 9.77M; CFPB 4.68M; FDIC 1.81M; NCUA 1.31M |
| AGENCY_CODE | category | 6 | 0 | 7 9.77M; 9 4.68M; 3 1.81M; 5 1.31M |
| LOAN_TYPE_NAME | category | 4 | 0 | Conventional 13.18M; FHA-insured 3.59M; VA-guaranteed 2.01M; FSA/RHS-guaranteed 356.5K |
| LOAN_TYPE | category | 4 | 0 | 1 13.18M; 2 3.59M; 3 2.01M; 4 356.5K |
| PROPERTY_TYPE_NAME | other | 1 | 0 | One-to-four family dwelli 19.14M |
| PROPERTY_TYPE | other | 1 | 0 | 1 19.14M |
| LOAN_PURPOSE_NAME | category | 3 | 0 | Home purchase 10.18M; Refinancing 8.32M; Home improvement 637.9K |
| LOAN_PURPOSE | category | 3 | 0 | 1 10.18M; 3 8.32M; 2 637.9K |
| OWNER_OCCUPANCY_NAME | other | 1 | 0 | Owner-occupied as a princ 19.14M |
| OWNER_OCCUPANCY | other | 1 | 0 | 1 19.14M |
| LOAN_AMOUNT_000S | amount | 4.8K | 1.5K | 417 226.0K; 200 160.5K; 100 139.8K; 150 137.3K |
| PREAPPROVAL_NAME | category | 3 | 0 | Not applicable 15.03M; Preapproval was not reque 3.42M; Preapproval was requested 691.4K |
| PREAPPROVAL | category | 3 | 0 | 3 15.03M; 2 3.42M; 1 691.4K |
| ACTION_TAKEN_NAME | other | 1 | 0 | Loan originated 19.14M |
| ACTION_TAKEN | other | 1 | 0 | 1 19.14M |
| MSAMD_NAME | who | 412 | 1.74M | Los Angeles, Long Beach,  509.1K; Chicago, Naperville, Arli 453.7K; Atlanta, Sandy Springs, R 428.2K; Phoenix, Mesa, Scottsdale 416.2K |
| MSAMD | other | 584 | 1.74M | 31084 509.1K; 16974 453.7K; 12060 428.2K; 38060 416.2K |
| STATE_NAME | who | 52 | 23.1K | California 2.57M; Texas 1.43M; Florida 1.16M; Illinois 748.6K |
| STATE_ABBR | state | 53 | 23.1K | CA 2.57M; TX 1.43M; FL 1.16M; IL 748.6K |
| STATE_CODE | other | 53 | 23.1K | 6 2.57M; 48 1.43M; 12 1.16M; 17 748.6K |
| COUNTY_NAME | who | 2.0K | 30.9K | Los Angeles County 509.4K; Maricopa County 381.6K; Orange County 320.4K; Cook County 283.6K |
| COUNTY_CODE | other | 326 | 30.9K | 13 703.7K; 37 688.6K; 3 622.1K; 31 622.1K |
| CENSUS_TRACT_NUMBER | other | 24.1K | 38.6K | 0002.00 60.0K; 0006.00 59.2K; 0105.00 59.1K; 0028.00 48.5K |
| APPLICANT_ETHNICITY_NAME | category | 4 | 0 | Not Hispanic or Latino 15.46M; Information not provided  1.86M; Hispanic or Latino 1.80M; Not applicable 17.4K |
| APPLICANT_ETHNICITY | category | 4 | 0 | 2 15.46M; 3 1.86M; 1 1.80M; 4 17.4K |
| CO_APPLICANT_ETHNICITY_NAME | category | 5 | 0 | No co-applicant 9.99M; Not Hispanic or Latino 7.34M; Information not provided  1.02M; Hispanic or Latino 780.0K |
| CO_APPLICANT_ETHNICITY | category | 5 | 0 | 5 9.99M; 2 7.34M; 3 1.02M; 1 780.0K |
| APPLICANT_RACE_NAME_1 | category | 7 | 0 | White 14.75M; Information not provided  1.99M; Black or African American 1.13M; Asian 1.06M |
| APPLICANT_RACE_1 | category | 7 | 0 | 5 14.75M; 6 1.99M; 3 1.13M; 2 1.06M |
| APPLICANT_RACE_NAME_2 | category | 5 | 19.03M | White 78.2K; Black or African American 9.6K; Native Hawaiian or Other  8.5K; Asian 5.4K |
| APPLICANT_RACE_2 | category | 5 | 19.03M | 5 78.2K; 3 9.6K; 4 8.5K; 2 5.4K |
| APPLICANT_RACE_NAME_3 | category | 5 | 19.13M | White 4.6K; Black or African American 1.1K; Native Hawaiian or Other  466; American Indian or Alaska 199 |
| APPLICANT_RACE_3 | category | 5 | 19.13M | 5 4.6K; 3 1.1K; 4 466; 1 199 |
| APPLICANT_RACE_NAME_4 | category | 5 | 19.14M | Native Hawaiian or Other  688; White 391; Asian 46; Black or African American 22 |
| APPLICANT_RACE_4 | category | 5 | 19.14M | 4 688; 5 391; 2 46; 3 22 |
| APPLICANT_RACE_NAME_5 | category | 5 | 19.14M | White 687; American Indian or Alaska 27; Black or African American 15; Asian 14 |
| APPLICANT_RACE_5 | category | 5 | 19.14M | 5 687; 1 27; 3 15; 2 14 |
| CO_APPLICANT_RACE_NAME_1 | category | 8 | 0 | No co-applicant 9.99M; White 7.16M; Information not provided  1.07M; Asian 511.3K |
| CO_APPLICANT_RACE_1 | category | 8 | 0 | 8 9.99M; 5 7.16M; 6 1.07M; 2 511.3K |
| CO_APPLICANT_RACE_NAME_2 | category | 5 | 19.10M | White 30.2K; Native Hawaiian or Other  4.1K; Black or African American 2.8K; Asian 2.5K |
| CO_APPLICANT_RACE_2 | category | 5 | 19.10M | 5 30.2K; 4 4.1K; 3 2.8K; 2 2.5K |
| CO_APPLICANT_RACE_NAME_3 | category | 5 | 19.13M | White 1.5K; Black or African American 358; Native Hawaiian or Other  235; American Indian or Alaska 59 |
| CO_APPLICANT_RACE_3 | category | 5 | 19.13M | 5 1.5K; 3 358; 4 235; 1 59 |
| CO_APPLICANT_RACE_NAME_4 | category | 5 | 19.14M | Native Hawaiian or Other  241; White 195; Asian 15; Black or African American 8 |
| CO_APPLICANT_RACE_4 | category | 5 | 19.14M | 4 241; 5 195; 2 15; 3 8 |
| CO_APPLICANT_RACE_NAME_5 | category | 5 | 19.14M | White 239; American Indian or Alaska 20; Asian 8; Black or African American 5 |
| CO_APPLICANT_RACE_5 | category | 5 | 19.14M | 5 239; 1 20; 2 8; 3 5 |
| APPLICANT_SEX_NAME | category | 4 | 0 | Male 12.58M; Female 5.36M; Information not provided  1.19M; Not applicable 12.5K |
| APPLICANT_SEX | category | 4 | 0 | 1 12.58M; 2 5.36M; 3 1.19M; 4 12.5K |
| CO_APPLICANT_SEX_NAME | category | 5 | 0 | No co-applicant 9.99M; Female 6.81M; Male 1.67M; Information not provided  655.6K |
| CO_APPLICANT_SEX | category | 5 | 0 | 5 9.99M; 2 6.81M; 1 1.67M; 3 655.6K |
| APPLICANT_INCOME_000S | who | 6.1K | 1.23M | 60 221.5K; 50 202.5K; 52 191.7K; 55 187.3K |
| PURCHASER_TYPE_NAME | category | 10 | 0 | Fannie Mae (FNMA) 3.94M; Loan was not originated o 3.89M; Ginnie Mae (GNMA) 3.08M; Freddie Mac (FHLMC) 2.62M |
| PURCHASER_TYPE | category | 10 | 0 | 1 3.94M; 0 3.89M; 2 3.08M; 3 2.62M |
| DENIAL_REASON_NAME_1 | empty | 0 | 19.14M |  |
| DENIAL_REASON_1 | empty | 0 | 19.14M |  |
| DENIAL_REASON_NAME_2 | empty | 0 | 19.14M |  |
| DENIAL_REASON_2 | empty | 0 | 19.14M |  |
| DENIAL_REASON_NAME_3 | empty | 0 | 19.14M |  |
| DENIAL_REASON_3 | empty | 0 | 19.14M |  |
| RATE_SPREAD | amount | 967 | 18.10M | 01.50 25.7K; 01.51 22.7K; 01.53 21.5K; 01.52 21.3K |
| HOEPA_STATUS_NAME | category | 2 | 0 | Not a HOEPA loan 19.13M; HOEPA loan 4.4K |
| HOEPA_STATUS | category | 2 | 0 | 2 19.13M; 1 4.4K |
| LIEN_STATUS_NAME | other | 1 | 0 | Secured by a first lien 19.14M |
| LIEN_STATUS | other | 1 | 0 | 1 19.14M |
| EDIT_STATUS_NAME | other | 1 | 17.02M | Quality edit failure only 2.11M |
| EDIT_STATUS | other | 1 | 17.02M | 6 2.11M |
| SEQUENCE_NUMBER | other | 809.7K | 5.99M | 0000108 33.1K; 0002809 22.0K; 0000345 20.1K; 0000042 20.1K |
| POPULATION | other | 10.6K | 39.6K | 4346 36.8K; 5717 36.7K; 4888 36.1K; 4811 36.1K |
| MINORITY_POPULATION | amount | 10.1K | 39.7K | 9.9399995803833 36.5K; 25.329999923706055 36.5K; 5.5 36.4K; 10.470000267028809 36.1K |
| HUD_MEDIAN_FAMILY_INCOME | other | 497 | 38.6K | 74700 311.6K; 72500 251.1K; 62400 248.8K; 64300 229.5K |
| TRACT_TO_MSAMD_INCOME | amount | 20.5K | 40.7K | 94.91000366210938 24.9K; 93.81999969482422 24.9K; 138.6199951171875 24.8K; 95.16999816894531 24.8K |
| NUMBER_OF_OWNER_OCCUPIED_UNITS | who | 3.6K | 41.0K | 1543 48.5K; 1025 48.4K; 1209 48.3K; 1644 48.3K |
| NUMBER_OF_1_TO_4_FAMILY_UNITS | other | 4.7K | 40.8K | 1470 49.2K; 1556 48.5K; 1450 48.4K; 1357 47.2K |
| APPLICATION_DATE_INDICATOR | category | 2 | 5.99M | 0 13.15M; 1 14 |
| _INGESTED_AT | audit date | 1 | 0 | 2026-08-05 17:27:42.452 19.14M |
| _SOURCE_RUN_ID | audit id | 18.87M | 0 | 49cd34a0-82b5-47fd-9688-2 12.5K; f8e0d96d-7b90-4abc-a8ab-9 12.5K; ff7b6206-ee80-4ee1-a4f1-9 12.5K; d361e92b-0b6b-41ca-8e74-a 12.5K |
