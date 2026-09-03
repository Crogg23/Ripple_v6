# PORTAL_CKA_HOUSTON_OPEN_DAT_0AA7C87F45

rows 10.0K  columns 23  scan 3.5s

roles: amount 5, audit 2, category 8, date 3, id 1, other 3, who 2

## when

DATE_POSITION_BEGAN
  2023       845  ####
  2024       532  ###
  2025      2.5K  ############
  2026      6.1K  ##############################

DATE_POSITION_ENDED
  2024        25  
  2025       231  ###
  2026      2.1K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PAY_GRADE | 6.1K | 3 | 16 | 34 | 38 | 105.4K |
| ANNUAL_BASE_SALARY | 10.0K | 502 | 73.4K | 161.2K | 289.8K | 755.32M |
| GROSS_PAY | 10.0K | -6.2K | 35.1K | 93.7K | 236.6K | 374.18M |
| BASE_PAY | 10.0K | -32.9K | 29.8K | 76.8K | 144.9K | 309.52M |
| OTHER_PAY | 10.0K | -2.0K | 1.2K | 18.3K | 208.0K | 33.73M |

## who

OVERTIME_PAY by rows
      4.4K  0.0
        40  337.5
        16  356.25
        14  328.13
         6  2265.48
         4  7.93
         4  137.96
         4  282.8
         3  8.59
         3  85.47
         3  7.61
         3  332.9
         2  23.67
         2  735.5
         2  169.04
         2  858.52
         2  57.16
         2  276.95
         2  11043.2
         2  86.67

OVERTIME_PAY by dollars
     351.62M     4.4K rows  0.0
       2.08M       40 rows  337.5
      832.0K       16 rows  356.25
      728.0K       14 rows  328.13
      224.3K        6 rows  2265.48
      223.3K        4 rows  137.96
      202.4K        2 rows  2556.48
      202.4K        2 rows  3834.7200000000003
      202.4K        2 rows  11043.2
      202.4K        2 rows  2685.76
      189.5K        2 rows  96.24
      179.0K        2 rows  4396.7
      177.1K        1 rows  773.44
      175.9K        2 rows  2125.2
      175.8K        4 rows  7.93
      174.8K        3 rows  85.47
      174.8K        2 rows  403.74
      169.1K        1 rows  731.84
      168.1K        2 rows  1948.26
      165.0K        1 rows  686.32

SRC_SHA256 by rows
     10.0K  f65e28e26c1fe7c94a46bdd11d7d7d585157b50d0248899b44f643ebcbbc794c

SRC_SHA256 by dollars
     755.32M    10.0K rows  f65e28e26c1fe7c94a46bdd11d7d7d585157b50d0248899b44f643ebcbbc

## who x when

OVERTIME_PAY by DATE_POSITION_BEGAN, dollars = ANNUAL_BASE_SALARY
  0.0                                       2023:38.64M 2024:30.86M 2025:96.98M 2026:185.15M
  11043.2                                   2026:202.4K
  137.96                                    2026:223.3K
  169.04                                    2026:114.4K
  1948.26                                   2026:168.1K
  2125.2                                    2025:85.1K 2026:90.8K
  2265.48                                   2026:224.3K
  23.67                                     2026:86.9K
  2556.48                                   2025:202.4K
  2685.76                                   2025:202.4K
  276.95                                    2026:87.7K
  282.8                                     2026:156.5K
  328.13                                    2025:676.0K 2026:52.0K
  332.9                                     2026:138.5K
  337.5                                     2025:1.82M 2026:260.0K
  356.25                                    2025:780.0K 2026:52.0K
  3834.7200000000003                        2023:101.2K 2025:101.2K
  403.74                                    2025:84.0K 2026:90.8K
  4396.7                                    2026:179.0K
  57.16                                     2025:44.8K 2026:39.4K
  7.61                                      2023:40.8K 2025:42.2K 2026:40.5K
  7.93                                      2025:44.0K 2026:131.8K
  731.84                                    2023:169.1K
  735.5                                     2026:127.3K
  773.44                                    2026:177.1K
  8.59                                      2026:142.5K
  85.47                                     2026:174.8K
  858.52                                    2025:62.3K 2026:43.7K
  86.67                                     2026:141.1K
  96.24                                     2025:74.9K 2026:114.5K

SRC_SHA256 by DATE_POSITION_BEGAN, dollars = ANNUAL_BASE_SALARY
  f65e28e26c1fe7c94a46bdd11d7d7d585157b50d  2023:68.28M 2024:42.16M 2025:192.07M 2026:452.81M

## what

GENDER: Male 69%, Female 31%

RACE: Black or African American 37%, Hispanic/Latino 30%, White 25%, Asian 7%, American Indian or Alaskan Nat 0%, Two or More Races 0%, Others 0%, Native Hawaiian or Other Pacif 0%, Asian/Pacific Islander 0%

FLSA_STATUS: Non-Exempt 81%, Exempt 19%

EEOJ_CODE: D: Protective Service Workers 35%, B: Professionals 26%, C: Technicians 14%, G: Skilled Craft Workers 8%, A: Officials & Administrators 6%, H: Service/Maintenance 4%, E: Para-Professionals 4%, F: Administrative Support 3%

EMPLOYMENT_TYPE: Full Time 96%, Part time 3%, Temporary 1%, Part Time 30 0%

DEPARTMENT_ID: 1000 36%, 2000 19%, 1200 15%, 2800 7%, 3800 4%, 3600 4%, 2100 3%, 3400 3%, 8000 3%, 6500 2%, 6700 2%, 1500 2%

DEPARTMENT_NAME: Police 36%, Houston Public Works 19%, Fire 15%, Houston Airport System 7%, Health & Human Services 4%, Parks & Recreation 4%, Solid Waste Management 3%, Library 3%, Human Resources 3%, Admin. & Regulatory Affairs 2%, Fleet Management 2%, Houston Emergency Center 2%

STATUS: Active 94%, Withdrawn 6%, Inactive 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| HASH1 | other | 9.3K | 0 | AF2723B23F5C3FE6A0A02F977 50; EFA3CD03DDD02D222A28F7909 50; A4109E86C79C29E7ADB1D0848 50; EA4CF32BC8EF37BC1411E7972 50 |
| HASH2 | id | 10.1K | 0 | D3A1A0B7F18D9F4A08527D2A0 50; 9B21D738533F10E8CB07A7D74 50; 352C5EB083592E8007C7CDD47 50; 2B44B287375A56AA873BC174B 50 |
| BIRTH_YEAR | other | 65 | 0 | 1970 281; 1993 279; 1984 272; 1985 260 |
| GENDER | category | 2 | 0 | Male 6.9K; Female 3.1K |
| RACE | category | 9 | 0 | Black or African American 3.7K; Hispanic/Latino 3.0K; White 2.5K; Asian 744 |
| PAY_GRADE | amount | 189 | 0 | 13 653; 10 624; PA04 - 17 554; 17 376 |
| FLSA_STATUS | category | 2 | 0 | Non-Exempt 8.1K; Exempt 1.9K |
| EEOJ_CODE | category | 8 | 0 | D: Protective Service Wor 3.5K; B: Professionals 2.6K; C: Technicians 1.4K; G: Skilled Craft Workers 832 |
| EMPLOYMENT_TYPE | category | 4 | 0 | Full Time 9.6K; Part time 285; Temporary 84; Part Time 30 22 |
| DEPARTMENT_ID | category | 24 | 0 | 1000 3.3K; 2000 1.8K; 1200 1.4K; 2800 680 |
| DEPARTMENT_NAME | category | 24 | 0 | Police 3.3K; Houston Public Works 1.8K; Fire 1.4K; Houston Airport System 680 |
| STATUS | category | 3 | 0 | Active 9.4K; Withdrawn 589; Inactive 50 |
| YEAR | other | 1 | 0 | 2026 10.0K |
| DATE_POSITION_BEGAN | date | 491 | 0 | 01/21/2023 564; 02/14/2026 489; 02/28/2026 486; 03/14/2026 373 |
| DATE_POSITION_ENDED | date | 229 | 7.6K | 06/30/2026 493; 02/18/2026 94; 03/13/2026 90; 01/30/2026 89 |
| ANNUAL_BASE_SALARY | amount | 2.0K | 0 | 101195.0 592; 116656.0 306; 84030.0 279; 52000.0 251 |
| GROSS_PAY | amount | 9.6K | 0 | 15000.0 108; 7190.0 83; 25000.0 79; 21067.800000000003 70 |
| BASE_PAY | amount | 5.7K | 0 | 50597.3 428; 0.0 283; 58328.14 234; 42015.09 140 |
| OVERTIME_PAY | who | 5.5K | 0 | 0.0 4.4K; 337.5 40; 2265.48 31; 8.59 29 |
| OTHER_PAY | amount | 6.9K | 0 | 0.0 653; 325.0 170; 1000.0 161; 39.0 71 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:43:51.06854 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 0396a138-c275-4e8e-9774-5 10.0K |
| SRC_SHA256 | who | 1 | 0 | f65e28e26c1fe7c94a46bdd11 10.0K |
