# PORTAL_SOC_MARYLAND_OPEN_DA_BAA13FC4EC

rows 2.0K  columns 24  scan 5.3s

roles: amount 4, audit 2, category 10, date 1, other 4, who 4

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| APPROVED_AMOUNT | 2.0K | 1 | 29.0K | 5.00M | 23.00M | 563.55M |
| TOTAL_PROJECT_COSTS | 703 | 0 | 106.0K | 109.80M | 500.00M | 3.67B |
| AVERAGE_WAGE | 65 | 30.4K | 68.8K | 148.4K | 156.0K | 4.74M |
| LOAN_GUARANTEE_AMOUNT | 75 | 0 | 0 | 23.28M | 32.61M | 64.69M |

## who

RECIPIENT by rows
        18  Northrop Grumman Systems Corp
        14  Root3 Labs Inc
        12  Johns Hopkins University, The
        11  University Of Maryland Baltimore
        10  Tactical Network Solutions LLC
        10  Zenimax Media Inc
         9  CK Signals Inc
         9  VariQ Corp
         9  Tensley Consulting Inc
         9  Booz Allen Hamilton Inc
         9  ATI Inc
         9  Clear Ridge Defense LLC
         9  Univ of MD College Park Foundation
         9  Project Enhancement Corp
         9  Anthem Engineering LLC
         9  Tiber Technologies Inc
         9  Lingual Information System Technologies Inc
         9  Vision Technologies Inc
         9  Oakleaf Technology Group Inc
         8  Washington College

RECIPIENT by dollars
      36.79M       18 rows  Northrop Grumman Systems Corp
      23.00M        1 rows  Associated Catholic Charities
      20.00M        1 rows  Northrop Grumman Corp
      18.08M       12 rows  Johns Hopkins University, The
      16.00M        1 rows  It's My Ampitheater Inc
      14.10M       11 rows  University Of Maryland Baltimore
      13.50M        1 rows  Knight Takes King Productions LLC / House of Cards (Season 4
      12.00M        3 rows  Marriott International Inc
      10.00M        1 rows  Random Productions LLC / HBO (We Own the City) (6 episodes)
      10.00M        1 rows  King Street Productions Inc (Special Ops: Lioness)
       9.94M        9 rows  Univ of MD College Park Foundation
       7.73M        8 rows  Washington College
       7.59M        5 rows  American Gene Technologies International Inc
       7.20M        1 rows  Knight Takes King Productions LLC / House of Cards (Season 6
       7.05M        1 rows  Knight Takes King Productions LLC / House of Cards (Season 5
       6.57M        1 rows  Garrison Forest School
       6.46M        5 rows  Amazoncomdedc LLC
       5.52M        8 rows  CoolTech LLC
       5.10M        1 rows  Murphy's Crusting and Uniloader Services Inc
       5.05M        2 rows  Standard Wellness Maryland LLC

ADDRESS by rows
       760  nan
         7  7467 Ridge Road, Suite 330
         7  1781 Forest Dr #343
         6  6990 Columbia Gateway Drive
         6  7030 Dorsey Road, Suite 102
         6  6100 Seaforth Street
         6  8357 Main Street
         6  11408 Cronridge Dr Ste C
         6  5520 Research Park Drive, Suite 100
         6  6722 Senecca Lane
         6  2910 Francis Scott Key Highway
         5  55 Thiokol Road
         5  9220 Rumsey Road, Suite 100
         5  3460 Ellicott Center Drive, Suite 105A
         5  11900 Parklawn Drive, Suite 420
         5  6700 Alexander Bell Drive, Suite 115
         5  2600 Longstone Lane, Suite 201
         5  1201 Clopper Road
         5  Various
         5  4824 Tilly Drive

ADDRESS by dollars
     308.84M      760 rows  nan
      23.00M        1 rows  1966 Greenspring Drive
       8.93M        4 rows  Linthicum Campus
       8.01M        5 rows  Various
       7.00M        2 rows  7750 Wisconsin Ave
       6.57M        1 rows  300 Garrison Forest Road
       5.05M        2 rows  12108 Early Lilacs Path
       5.05M        2 rows  221 Oakengate Turn
       5.00M        1 rows  11140 Rockville Pike
       5.00M        1 rows  420 W. Huron
       5.00M        1 rows  4119 Century Towne Road
       5.00M        1 rows  10515 Theodore Green Blvd
       5.00M        1 rows  4119 Centruy Towne Road
       4.98M        2 rows  1312 Harbor Road
       4.55M        1 rows  1 South Street
       4.20M        1 rows  2717 Wilcarco Avenue
       4.00M        1 rows  4991 New Design Road
       3.00M        1 rows  401 Rosemont Avenue
       2.99M        2 rows  9640 Medical Center Drive
       2.80M        3 rows  8 Market Place, Suite 804

CITY by rows
       694  nan
       189  Baltimore
       154  Columbia
        60  Rockville
        46  Annapolis
        44  Ellicott City
        37  Frederick
        33  Gaithersburg
        33  Annapolis Junction
        25  Hanover
        25  Bethesda
        22  Owings Mills
        17  Germantown
        17  Odenton
        17  Laurel
        16  Sykesville
        15  Gambrills
        15  Linthicum
        15  Aberdeen
        14  Beltsville

CITY by dollars
     230.08M      694 rows  nan
      59.37M      189 rows  Baltimore
      51.51M       15 rows  Linthicum
      23.27M        5 rows  Timonium
      22.61M       60 rows  Rockville
      22.17M      154 rows  Columbia
      13.94M       25 rows  Bethesda
      12.00M       37 rows  Frederick
      10.04M        7 rows  Randallstown
       9.24M       46 rows  Annapolis
       8.81M       33 rows  Gaithersburg
       7.24M       22 rows  Owings Mills
       5.30M        3 rows  White Plains
       5.09M       10 rows  Clarksville
       5.05M        2 rows  Virginia Beach
       5.00M        1 rows  Chicago
       4.92M        5 rows  Riverdale
       4.09M        8 rows  College Park
       3.70M        9 rows  Hunt Valley
       3.21M        7 rows  Cumberland

SRC_SHA256 by rows
      2.0K  ec1ce63cfebefdfadd7090868e000baa5316d4bef0cf0a681de87696da1dea5e

SRC_SHA256 by dollars
     563.55M     2.0K rows  ec1ce63cfebefdfadd7090868e000baa5316d4bef0cf0a681de87696da1d

## who x when

RECIPIENT by INGESTED_AT  LOAD STAMP, not an event date, dollars = APPROVED_AMOUNT
  ATI Inc                                   2026:229.7K
  American Gene Technologies International  2026:7.59M
  Anthem Engineering LLC                    2026:45.8K
  Associated Catholic Charities             2026:23.00M
  Booz Allen Hamilton Inc                   2026:1.69M
  CK Signals Inc                            2026:63.6K
  Clear Ridge Defense LLC                   2026:98.9K
  It's My Ampitheater Inc                   2026:16.00M
  Johns Hopkins University, The             2026:18.08M
  King Street Productions Inc (Special Ops  2026:10.00M
  Knight Takes King Productions LLC / Hous  2026:13.50M
  Knight Takes King Productions LLC / Hous  2026:7.05M
  Knight Takes King Productions LLC / Hous  2026:7.20M
  Lingual Information System Technologies   2026:651.8K
  Marriott International Inc                2026:12.00M
  Northrop Grumman Corp                     2026:20.00M
  Northrop Grumman Systems Corp             2026:36.79M
  Oakleaf Technology Group Inc              2026:58.1K
  Project Enhancement Corp                  2026:53.6K
  Random Productions LLC / HBO (We Own the  2026:10.00M
  Root3 Labs Inc                            2026:132.6K
  Tactical Network Solutions LLC            2026:108.5K
  Tensley Consulting Inc                    2026:233.7K
  Tiber Technologies Inc                    2026:127.7K
  Univ of MD College Park Foundation        2026:9.94M
  University Of Maryland Baltimore          2026:14.10M
  VariQ Corp                                2026:612.8K
  Vision Technologies Inc                   2026:842.2K
  Washington College                        2026:7.73M
  Zenimax Media Inc                         2026:2.70M

ADDRESS by INGESTED_AT  LOAD STAMP, not an event date, dollars = APPROVED_AMOUNT
  10515 Theodore Green Blvd                 2026:5.00M
  11140 Rockville Pike                      2026:5.00M
  11408 Cronridge Dr Ste C                  2026:87.2K
  11900 Parklawn Drive, Suite 420           2026:11.1K
  1201 Clopper Road                         2026:732.0K
  12108 Early Lilacs Path                   2026:5.05M
  1781 Forest Dr #343                       2026:844.5K
  1966 Greenspring Drive                    2026:23.00M
  221 Oakengate Turn                        2026:5.05M
  2600 Longstone Lane, Suite 201            2026:72.8K
  2910 Francis Scott Key Highway            2026:828.0K
  300 Garrison Forest Road                  2026:6.57M
  3460 Ellicott Center Drive, Suite 105A    2026:47.8K
  4119 Century Towne Road                   2026:5.00M
  420 W. Huron                              2026:5.00M
  4824 Tilly Drive                          2026:10.9K
  55 Thiokol Road                           2026:1.74M
  5520 Research Park Drive, Suite 100       2026:119.5K
  6100 Seaforth Street                      2026:43.8K
  6700 Alexander Bell Drive, Suite 115      2026:62.5K
  6722 Senecca Lane                         2026:44.3K
  6990 Columbia Gateway Drive               2026:14.7K
  7030 Dorsey Road, Suite 102               2026:95.3K
  7467 Ridge Road, Suite 330                2026:320.0K
  7750 Wisconsin Ave                        2026:7.00M
  8357 Main Street                          2026:35.3K
  9220 Rumsey Road, Suite 100               2026:167.0K
  Linthicum Campus                          2026:8.93M
  Various                                   2026:8.01M
  nan                                       2026:308.84M

## what

FISCAL_YEAR: 2025 14%, 2023 13%, 2018 12%, 2022 10%, 2016 9%, 2024 9%, 2021 9%, 2019 8%, 2017 8%, 2020 8%

PROGRAM_NAME_LEVEL_ONE: Employer Security Clearances C 33%, Buy Maryland Cybersecurity Tax 13%, Export Maryland Grant 10%, Biotechnology Investment Incen 10%, Job Creation Tax Credit (JCTC) 7%, Child Care Captial Support Rev 6%, Maryland Economic Development  6%, Maryland Manufacturing 4.0 Gra 5%, Maryland E-Nnovation Initiativ 4%, Cannabis Business Assistance F 3%, Maryland Alcohol Manufacturing 2%, Film Production Tax Credit 1%

PROGRAM_NAME_LEVEL_TWO: ESCC Tax Credit 33%, Buy Maryland Cyber tax credit 13%, Export Maryland 10%, Biotech Tax Credit 10%, Job Creation Tax Credit 7%, CCCRLF 6%, Advantage Maryland (MEDAAF) -  5%, M4 Grant Program 5%, E-Nnovation 4%, Cannabis Business Assistance F 3%, MD AMP Fund 2%, Film Tax Credit 1%

PROGRAM_NAME_LEVEL_THREE: ESCC 33%, BMC 13%, Export Maryland 11%, BIITC 10%, JCTC 7%, Child Care 7%, M4 Grant Program 5%, MEDAAF-2 Cond. Loan 4%, MEIF 4%, CBAF 3%, MD AMP Fund 2%, Film Tax Credit 1%

COUNTY: Howard 20%, Montgomery 16%, Baltimore City 15%, Anne Arundel 13%, Baltimore 11%, Prince George's 8%, Frederick 4%, Carroll 4%, Harford 4%, Multiple 3%, Charles 2%, Cecil 1%

STATE: MD 64%, nan 35%, VA 1%, PA 0%, MD
MD 0%, MA 0%, NY 0%, IL 0%

INCENTIVE_TYPE: Tax Credit 63%, Loan/Grant 37%

EMPLOYMENT_REPORTING_REQUIRED: nan 96%, No 2%, N 1%, Y 1%, Yes 1%

MARYLAND_LOCAL_HIRES_FILM: nan 99%, 30 0%, 10 0%, 24 0%, 9 0%, 39 0%, 2 0%, 57 0%, 45 0%, 15 0%, 46 0%, 55 0%

NUMBER_OF_MARYLAND_BUSINESSES: nan 99%, 17 0%, 67 0%, 251 0%, 3 0%, 69 0%, 145 0%, 44 0%, 83 0%, 128 0%, 53 0%, 284 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FISCAL_YEAR | category | 10 | 0 | 2025 287; 2023 255; 2018 235; 2022 197 |
| RECIPIENT | who | 1.1K | 0 | Johns Hopkins University, 20; University Of Maryland Ba 19; Northrop Grumman Systems  18; Univ of MD College Park F 17 |
| PROGRAM_NAME_LEVEL_ONE | category | 22 | 0 | Employer Security Clearan 629; Buy Maryland Cybersecurit 244; Export Maryland Grant 199; Biotechnology Investment  193 |
| PROGRAM_NAME_LEVEL_TWO | category | 28 | 0 | ESCC Tax Credit 629; Buy Maryland Cyber tax cr 244; Export Maryland 199; Biotech Tax Credit 193 |
| PROGRAM_NAME_LEVEL_THREE | category | 42 | 0 | ESCC 629; BMC 244; Export Maryland 199; BIITC 193 |
| APPROVED_AMOUNT | amount | 1.3K | 0 | 5000 146; 50000 56; 10000 44; 500000 41 |
| TOTAL_PROJECT_COSTS | amount | 536 | 0 | nan 1.3K; 500000 23; 200000 15; 1000000 13 |
| RETAINED_JOBS | other | 155 | 0 | nan 1.6K; 0 36; 1 17; 3 10 |
| NAICS_CODE | other | 341 | 0 | 541330 161; 541511 159; 624410 124; 541519 116 |
| COUNTY | category | 33 | 0 | Howard 368; Montgomery 283; Baltimore City 273; Anne Arundel 232 |
| CITY | who | 193 | 0 | nan 694; Baltimore 189; Columbia 154; Rockville 60 |
| STATE | category | 8 | 0 | MD 1.3K; nan 694; VA 11; PA 1 |
| INCENTIVE_TYPE | category | 2 | 0 | Tax Credit 1.3K; Loan/Grant 729 |
| ADDRESS | who | 880 | 0 | nan 760; 1781 Forest Dr #343 12; 1201 Clopper Road 10; 2910 Francis Scott Key Hi 10 |
| ZIP | other | 221 | 0 | nan 750; 21046 91; 21043 40; 21045 37 |
| AVERAGE_WAGE | amount | 65 | 0 | nan 1.9K; 68811.98876404495 2; 48582.3698630137 1; 100107.40243902439 1 |
| NEW_JOBS | other | 120 | 0 | nan 1.5K; 0 94; 2 44; 1 35 |
| EMPLOYMENT_REPORTING_REQUIRED | category | 5 | 0 | nan 1.9K; No 48; N 18; Y 11 |
| LOAN_GUARANTEE_AMOUNT | amount | 11 | 0 | nan 1.9K; 0 66; 1500000 1; 1000000 1 |
| MARYLAND_LOCAL_HIRES_FILM | category | 28 | 0 | nan 2.0K; 30 3; 10 2; 24 2 |
| NUMBER_OF_MARYLAND_BUSINESSES | category | 30 | 0 | nan 2.0K; 17 3; 67 1; 251 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:38:31.34480 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 651ddbc8-b5b9-4854-985c-0 2.0K |
| SRC_SHA256 | who | 1 | 0 | ec1ce63cfebefdfadd7090868 2.0K |
