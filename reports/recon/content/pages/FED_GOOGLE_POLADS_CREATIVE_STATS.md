# FED_GOOGLE_POLADS_CREATIVE_STATS

rows 1.56M  columns 63  scan 9.3s

roles: amount 24, audit 2, category 4, date 4, empty 3, id 2, other 19, who 5

## when

DATE_RANGE_START
  2018       652  
  2019     89.6K  ######
  2020    335.6K  #####################
  2021     77.0K  #####
  2022    203.4K  #############
  2023    144.9K  #########
  2024    480.9K  ##############################
  2025    133.0K  ########
  2026     97.7K  ######

DATE_RANGE_END
  2019     59.9K  ####
  2020    361.9K  #######################
  2021     61.9K  ####
  2022    216.1K  #############
  2023    141.2K  #########
  2024    482.4K  ##############################
  2025    134.8K  ########
  2026    104.7K  #######

FIRST_SERVED_TIMESTAMP
  2018       652  
  2019     89.6K  ######
  2020    335.6K  #####################
  2021     77.0K  #####
  2022    203.4K  #############
  2023    144.9K  #########
  2024    480.9K  ##############################
  2025    133.0K  ########
  2026     97.7K  ######

LAST_SERVED_TIMESTAMP
  2019     59.9K  ####
  2020    361.9K  #######################
  2021     61.9K  ####
  2022    216.1K  #############
  2023    141.2K  #########
  2024    482.4K  ##############################
  2025    134.8K  ########
  2026    104.7K  #######

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SPEND_RANGE_MIN_USD | 1.56M | 0 | 0 | 25.0K | 3.00M | 2.25B |
| SPEND_RANGE_MAX_USD | 1.56M | 0 | 100 | 30.0K | 3.00M | 2.84B |
| SPEND_RANGE_MIN_INR | 1.56M | 0 | 0 | 89.6K | 3.00M | 7.56B |
| SPEND_RANGE_MAX_INR | 1.56M | 0 | 250 | 98.7K | 3.00M | 8.62B |
| SPEND_RANGE_MIN_GBP | 1.56M | 0 | 0 | 0 | 500.0K | 10.76M |
| SPEND_RANGE_MAX_GBP | 1.56M | 0 | 50 | 50.00 | 600.0K | 90.88M |

## who

ADVERTISER_NAME by rows
    274.6K  Bharatiya Janata Party
     64.1K  MIKE BLOOMBERG 2020 INC
     62.8K  BIDEN FOR PRESIDENT
     38.1K  KEVIN COMBS
     34.2K  Money Metals Exchange LLC
     27.0K  TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE
     23.0K  DONALD J. TRUMP FOR PRESIDENT, INC.
     17.5K  The Labour Party
     17.4K  Sprizzy Media LLC
     14.0K  HARRIS FOR PRESIDENT
     12.2K  TILAK SHARMA
     12.2K  JEXAN LLC
     10.0K  Populus Empowerment Network Private Limited
      9.1K  NRSC
      9.1K  FF PAC
      8.7K  MARKETFUEL SUBSCRIPTION SERVICES
      8.7K  INDIAN PAC CONSULTING PRIVATE LIMITED
      8.2K  PROGRESSNOW
      7.5K  Juntos por el Cambio
      7.3K  Indian National Congress

ADVERTISER_NAME by dollars
      88.61M    62.8K rows  BIDEN FOR PRESIDENT
      74.65M    23.0K rows  DONALD J. TRUMP FOR PRESIDENT, INC.
      59.30M     2.2K rows  HARRIS VICTORY FUND
      56.69M     9.1K rows  FF PAC
      54.53M    64.1K rows  MIKE BLOOMBERG 2020 INC
      48.48M    14.0K rows  HARRIS FOR PRESIDENT
      38.74M    27.0K rows  TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE
      38.35M     3.5K rows  SENATE LEADERSHIP FUND
      29.72M     1.9K rows  DSCC
      29.29M     5.5K rows  DONALD J. TRUMP FOR PRESIDENT 2024, INC.
      27.85M     3.5K rows  BIDEN VICTORY FUND
      26.41M     1.3K rows  WinSenate
      24.37M      366 rows  TRUMP NATIONAL COMMITTEE JFC
      23.77M     6.7K rows  DNC SERVICES CORP / DEMOCRATIC NATIONAL COMMITTEE
      21.94M     5.2K rows  CONGRESSIONAL LEADERSHIP FUND
      20.06M     2.1K rows  AMERICANS FOR PROSPERITY ACTION INC
      18.95M     9.1K rows  NRSC
      18.38M     6.5K rows  DCCC
      17.98M      520 rows  PRESERVE AMERICA PAC
      16.80M    34.2K rows  Money Metals Exchange LLC

GEO_TARGETING_INCLUDED by rows
    238.0K  United States
     31.7K  India
     15.9K  Pennsylvania,United States
     15.5K  Arizona,United States
     13.3K  Wisconsin,United States
     13.2K  Maharashtra,India
     13.2K  Georgia,United States
     13.1K  Michigan,United States
     12.2K  North Carolina,United States
     11.2K  Argentina
     10.6K  Nevada,United States
      9.9K  Tamil Nadu,India
      9.9K  Florida,United States
      9.0K  Iowa,United States
      8.6K  West Bengal,India
      7.2K  Colorado,United States
      6.7K  New Hampshire,United States
      6.6K  Minnesota,United States
      6.1K  Ohio,United States
      6.0K  Rajasthan,India

GEO_TARGETING_INCLUDED by dollars
     429.61M   238.0K rows  United States
      79.02M    13.2K rows  Georgia,United States
      70.70M    15.9K rows  Pennsylvania,United States
      59.66M     5.4K rows  California,United States
      57.74M    13.1K rows  Michigan,United States
      56.02M    13.3K rows  Wisconsin,United States
      42.45M     6.1K rows  Ohio,United States
      41.74M    12.2K rows  North Carolina,United States
      37.70M    15.5K rows  Arizona,United States
      29.87M      779 rows  Alabama,United States, Alaska,United States, Arizona,United 
      28.51M     9.9K rows  Florida,United States
      27.87M    10.6K rows  Nevada,United States
      23.13M     3.8K rows  Texas,United States
      20.13M     5.5K rows  Montana,United States
      17.81M     9.0K rows  Iowa,United States
      13.48M     2.0K rows  New Jersey,United States
      13.10M     3.9K rows  Virginia,United States
      12.43M     3.2K rows  Maine,United States
      11.40M     6.7K rows  New Hampshire,United States
      10.64M     1.4K rows  Kentucky,United States

GEO_TARGETING_EXCLUDED by rows
     33.4K  Brazil, Canada, India, Japan, Mexico, Nigeria, Puerto Rico, Russia, Tu
     12.1K  Afghanistan, Alaska,United States, Albania, Algeria, Andorra, Angola, 
      9.5K  Afghanistan, Albania, Algeria, Andorra, Angola, Anguilla, Antigua and 
      5.1K  Bangladesh, India, Indonesia, Pakistan, Thailand
      5.0K  Bangladesh, India, Indonesia, Malaysia, Pakistan, Philippines, Thailan
      4.7K  Arizona,United States, California,United States, Florida,United States
      4.7K  Bulgaria, China, El Salvador, India, Romania, Russia, South Africa, Uk
      4.4K  Mumbai,Maharashtra,India, Navi Mumbai,Maharashtra,India, Pimpri-Chinch
      3.3K  Jaipur,Rajasthan,India
      3.0K  Alabama,United States, Florida,United States, North Carolina,United St
      2.6K  Illinois,United States, Indiana,United States, Iowa,United States, Ken
      2.5K  Montana,United States, New York,United States, Vermont,United States, 
      2.5K  Afghanistan, Albania, Algeria, Andorra, Angola, Antigua and Barbuda, A
      2.4K  Chennai,Chennai,Tamil Nadu,India
      2.4K  Delaware,United States, Maryland,United States, New Jersey,United Stat
      2.2K  Islampur,Malda Division,West Bengal,India
      2.2K  Afghanistan, Albania, Algeria, American Samoa, Andorra, Angola, Anguil
      2.2K  Afghanistan, Albania, Algeria, American Samoa, Andorra, Angola, Anguil
      2.0K  32011,Florida,United States, 32043,Florida,United States, 32131,Florid
      2.0K  Alabama,United States, Arkansas,United States, California,United State

GEO_TARGETING_EXCLUDED by dollars
      26.16M     9.5K rows  Afghanistan, Albania, Algeria, Andorra, Angola, Anguilla, An
      20.14M     3.0K rows  Alabama,United States, Florida,United States, North Carolina
      19.97M     2.4K rows  Delaware,United States, Maryland,United States, New Jersey,U
      14.30M      787 rows  Georgia,United States
      12.32M     1.1K rows  Illinois,United States, Indiana,United States, Ohio,United S
      10.60M     1.3K rows  Illinois,United States, Indiana,United States, Iowa,United S
       9.52M      114 rows  Indiana,United States, Kentucky,United States, Maryland,Unit
       9.45M       18 rows  Afghanistan, Albania, Algeria, Andorra, Angola, Antigua and 
       7.88M      208 rows  Kentucky,United States, Maryland,United States, North Caroli
       7.09M     1.7K rows  Georgia,United States, South Carolina,United States, Tenness
       6.81M      160 rows  Alabama,United States, Alaska,United States, Arizona,United 
       6.55M       37 rows  Arizona,United States, Georgia,United States, Michigan,Unite
       6.38M      344 rows  Alabama,United States, Alaska,United States, Arizona,United 
       5.82M      219 rows  Alabama,United States, Arkansas,United States, Colorado,Unit
       5.74M      958 rows  California,United States, Colorado,United States, Nevada,Uni
       5.58M      209 rows  93224,California,United States, 93226,California,United Stat
       5.54M      111 rows  Nevada,United States
       5.51M      314 rows  Arkansas,United States, Louisiana,United States, New Mexico,
       5.35M      229 rows  Indiana,United States, Iowa,United States, Kentucky,United S
       5.35M     2.5K rows  Afghanistan, Albania, Algeria, Andorra, Angola, Antigua and 

AGE_TARGETING by rows
    241.3K  18-24, 25-34, 35-44, 45-54, 55-64, ≥65, Unknown age
     94.5K  18-24, 25-34, 35-44, 45-54, 55-64, ≥65
     67.9K  35-44, 45-54, 55-64, ≥65
     39.6K  35-44, 45-54, 55-64, ≥65, Unknown age
     29.1K  25-34, 35-44, 45-54, 55-64, ≥65, Unknown age
     28.6K  18-24, 25-34
     19.5K  25-34, 35-44, 45-54, 55-64, ≥65
     12.6K  35-44, 45-54
     11.8K  18-24, 25-34, 35-44, 45-54
     10.2K  55-64, ≥65
      8.4K  18-24, 25-34, 35-44
      8.2K  45-54, 55-64, ≥65, Unknown age
      7.9K  ≥65
      7.6K  18-24, 25-34, 35-44, 45-54, Unknown age
      6.2K  18-24
      6.0K  18-24, 25-34, Unknown age
      5.4K  18-24, 25-34, 35-44, 45-54, 55-64
      5.3K  45-54, 55-64, ≥65
      4.9K  25-34, 35-44, 45-54
      4.6K  25-34

AGE_TARGETING by dollars
     295.23M    94.5K rows  18-24, 25-34, 35-44, 45-54, 55-64, ≥65
     285.46M   241.3K rows  18-24, 25-34, 35-44, 45-54, 55-64, ≥65, Unknown age
     269.69M    67.9K rows  35-44, 45-54, 55-64, ≥65
     131.32M    39.6K rows  35-44, 45-54, 55-64, ≥65, Unknown age
      86.37M    19.5K rows  25-34, 35-44, 45-54, 55-64, ≥65
      45.32M    28.6K rows  18-24, 25-34
      40.59M    10.2K rows  55-64, ≥65
      40.34M    29.1K rows  25-34, 35-44, 45-54, 55-64, ≥65, Unknown age
      34.28M     8.2K rows  45-54, 55-64, ≥65, Unknown age
      28.63M     8.4K rows  18-24, 25-34, 35-44
      26.43M     5.3K rows  45-54, 55-64, ≥65
      23.91M    11.8K rows  18-24, 25-34, 35-44, 45-54
      17.21M     7.6K rows  18-24, 25-34, 35-44, 45-54, Unknown age
      15.62M    12.6K rows  35-44, 45-54
      14.16M     6.0K rows  18-24, 25-34, Unknown age
      13.99M     4.1K rows  55-64, ≥65, Unknown age
      12.69M     4.9K rows  25-34, 35-44, 45-54
      11.76M     7.9K rows  ≥65
      10.08M     3.3K rows  18-24, 25-34, 35-44, Unknown age
       6.78M     3.4K rows  35-44, 45-54, 55-64

## who x when

ADVERTISER_NAME by DATE_RANGE_START, dollars = SPEND_RANGE_MIN_USD
  AMERICANS FOR PROSPERITY ACTION INC       2019:360.3K 2020:3.39M 2022:3.17M 2023:1.92M 2024:8.54M 2025:88.0K 2026:2.59M
  BIDEN FOR PRESIDENT                       2019:6.98M 2020:65.67M 2023:2.16M 2024:13.80M
  BIDEN VICTORY FUND                        2020:14.28M 2023:5.76M 2024:7.82M
  Bharatiya Janata Party                    2020:0 2021:0 2022:0 2023:0 2024:0 2025:0 2026:0
  CONGRESSIONAL LEADERSHIP FUND             2019:179.1K 2020:3.00M 2021:10.9K 2022:6.82M 2023:60.0K 2024:11.87M
  DNC SERVICES CORP / DEMOCRATIC NATIONAL   2019:2.01M 2020:11.62M 2021:3.64M 2022:1.64M 2023:102.8K 2024:298.6K 2025:3.52M 2026:931.0K
  DONALD J. TRUMP FOR PRESIDENT 2024, INC.  2023:100 2024:29.29M
  DONALD J. TRUMP FOR PRESIDENT, INC.       2019:3.56M 2020:71.09M
  DSCC                                      2019:740.6K 2020:11.12M 2021:3.55M 2022:5.17M 2023:1.65M 2024:6.20M 2025:1.25M 2026:43.0K
  FF PAC                                    2020:345.0K 2024:56.34M
  HARRIS FOR PRESIDENT                      2024:48.48M
  HARRIS VICTORY FUND                       2023:500.0K 2024:58.80M
  INDIAN PAC CONSULTING PRIVATE LIMITED     2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0 2026:0
  Indian National Congress                  2022:0 2023:0 2024:0 2025:0 2026:0
  JEXAN LLC                                 2019:1.2K 2020:4.7K
  Juntos por el Cambio                      2023:0
  KEVIN COMBS                               2019:0 2020:5.9K 2021:834.8K 2022:28.5K 2023:100
  MARKETFUEL SUBSCRIPTION SERVICES          2019:298.9K 2020:699.9K 2021:2.2K 2022:911.3K 2023:787.0K 2024:168.6K 2025:286.1K 2026:90.7K
  MIKE BLOOMBERG 2020 INC                   2019:16.80M 2020:37.74M
  Money Metals Exchange LLC                 2019:251.8K 2020:3.10M 2021:3.93M 2022:2.68M 2023:6.08M 2024:616.8K 2025:125.0K 2026:5.0K
  NRSC                                      2019:21.9K 2020:8.16M 2021:5.37M 2022:2.96M 2023:187.8K 2024:1.91M 2025:67.7K 2026:280.4K
  PROGRESSNOW                               2019:54.7K 2020:326.0K 2021:2.7K 2022:254.7K 2023:45.5K 2024:89.6K 2025:219.1K 2026:222.0K
  Populus Empowerment Network Private Limi  2024:0 2025:0 2026:0
  SENATE LEADERSHIP FUND                    2020:8.94M 2022:8.66M 2024:20.73M 2025:25.0K
  Sprizzy Media LLC                         2019:0 2020:0 2021:0 2022:0 2023:0 2024:6.5K 2025:7.9K 2026:1.6K
  TILAK SHARMA                              2024:0
  TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE  2018:225.0K 2019:11.40M 2020:27.11M
  TRUMP NATIONAL COMMITTEE JFC              2024:24.12M 2026:250.0K
  The Labour Party                          2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0 2026:0
  WinSenate                                 2024:26.19M 2026:219.2K

GEO_TARGETING_INCLUDED by DATE_RANGE_START, dollars = SPEND_RANGE_MIN_USD
  Alabama,United States, Alaska,United Sta  2018:0 2019:1.22M 2020:823.9K 2021:23.6K 2022:3.6K 2023:8.4K 2024:27.79M
  Argentina                                 2022:0 2023:0 2024:0 2025:0 2026:0
  Arizona,United States                     2018:15.5K 2019:276.3K 2020:11.24M 2021:1.58M 2022:10.23M 2023:396.4K 2024:12.35M 2025:220.9K 2026:1.39M
  California,United States                  2018:63.9K 2019:1.67M 2020:12.51M 2021:1.00M 2022:20.16M 2023:1.19M 2024:9.58M 2025:3.91M 2026:9.58M
  Colorado,United States                    2019:603.3K 2020:3.72M 2021:259.5K 2022:2.91M 2023:341.0K 2024:1.07M 2025:91.8K 2026:897.6K
  Florida,United States                     2019:167.1K 2020:15.70M 2021:287.4K 2022:5.81M 2023:284.9K 2024:4.66M 2025:186.1K 2026:1.42M
  Georgia,United States                     2019:147.7K 2020:26.70M 2021:2.14M 2022:18.47M 2023:58.8K 2024:21.49M 2025:1.35M 2026:8.65M
  India                                     2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0 2026:100
  Iowa,United States                        2019:2.68M 2020:8.41M 2021:24.9K 2022:369.5K 2023:2.27M 2024:602.6K 2025:393.4K 2026:3.05M
  Kentucky,United States                    2019:553.4K 2020:4.69M 2021:42.3K 2022:276.1K 2023:1.24M 2024:519.1K 2025:404.5K 2026:2.92M
  Maharashtra,India                         2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0 2026:0
  Maine,United States                       2019:558.5K 2020:3.04M 2021:14.0K 2022:689.7K 2023:137.1K 2024:274.5K 2025:1.55M 2026:6.17M
  Michigan,United States                    2019:357.9K 2020:10.05M 2021:173.5K 2022:4.48M 2023:77.9K 2024:37.54M 2025:452.0K 2026:4.62M
  Minnesota,United States                   2019:128.5K 2020:2.41M 2021:44.9K 2022:2.24M 2023:20.6K 2024:641.2K 2025:50.9K 2026:993.1K
  Montana,United States                     2018:10.6K 2019:23.0K 2020:4.78M 2021:91.1K 2022:79.6K 2023:390.6K 2024:13.98M 2025:1.0K 2026:764.5K
  Nevada,United States                      2019:254.9K 2020:2.46M 2021:671.0K 2022:7.41M 2023:178.0K 2024:15.19M 2025:32.5K 2026:1.68M
  New Hampshire,United States               2019:818.1K 2020:1.72M 2021:1.08M 2022:2.75M 2023:1.57M 2024:2.96M 2025:12.1K 2026:495.9K
  New Jersey,United States                  2018:30.0K 2019:92.7K 2020:11.6K 2021:1.38M 2022:69.1K 2023:70.9K 2024:370.9K 2025:11.43M 2026:27.8K
  North Carolina,United States              2019:2.57M 2020:14.40M 2021:244.3K 2022:4.82M 2023:597.7K 2024:14.59M 2025:2.47M 2026:2.05M
  Ohio,United States                        2019:78.3K 2020:1.53M 2021:364.7K 2022:3.47M 2023:2.10M 2024:29.78M 2025:1.06M 2026:4.06M
  Pennsylvania,United States                2019:131.8K 2020:12.01M 2021:587.1K 2022:9.13M 2023:487.8K 2024:47.16M 2025:506.9K 2026:688.2K
  Rajasthan,India                           2020:0 2021:0 2022:0 2023:0 2024:0 2025:0 2026:0
  Tamil Nadu,India                          2020:0 2021:0 2022:0 2023:0 2024:0 2025:0 2026:0
  Texas,United States                       2019:624.6K 2020:2.47M 2021:561.1K 2022:2.50M 2023:716.1K 2024:10.37M 2025:2.11M 2026:3.76M
  United States                             2018:1.79M 2019:55.15M 2020:102.51M 2021:39.88M 2022:45.43M 2023:43.90M 2024:82.26M 2025:36.96M 2026:21.74M
  Virginia,United States                    2018:1.5K 2019:230.5K 2020:1.11M 2021:3.09M 2022:38.3K 2023:229.1K 2024:653.7K 2025:3.86M 2026:3.89M
  West Bengal,India                         2019:0 2020:0 2021:0 2022:0 2023:0 2024:0 2025:0 2026:0
  Wisconsin,United States                   2019:32.7K 2020:7.17M 2021:775.2K 2022:13.72M 2023:1.37M 2024:28.41M 2025:4.10M 2026:434.6K

## what

AD_TYPE: VIDEO 48%, IMAGE 39%, TEXT 13%

REGIONS: US 59%, IN 26%, AR 4%, BR 4%, AU 3%, GB 2%, MX 1%, IL 0%, CL 0%, TW 0%, NZ 0%, ZA 0%

GENDER_TARGETING: Male, Female, Unknown gender 80%, Female 9%, Male 6%, Male, Female 3%, Female, Unknown gender 1%, Male, Unknown gender 1%, Unknown gender 0%

IS_FUNDED_BY_GOOGLE_AD_GRANTS: No 100%, Yes 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AD_ID | id | 1.55M | 0 | CR02519036664572018689 1.2K; CR15312103046452871169 1.2K; CR12492039786325868545 1.2K; CR16498326318723629057 1.2K |
| AD_URL | id | 1.58M | 0 | https://adstransparency.g 1.2K; https://adstransparency.g 1.2K; https://adstransparency.g 1.2K; https://adstransparency.g 1.2K |
| AD_TYPE | category | 3 | 0 | VIDEO 747.6K; IMAGE 606.7K; TEXT 208.6K |
| REGIONS | category | 13 | 0 | US 923.3K; IN 398.7K; AR 63.7K; BR 58.1K |
| ADVERTISER_ID | other | 20.8K | 0 | AR02607373078014984193 275.1K; AR09516581413973917697 64.8K; AR12365610929977556993 64.2K; AR01324533691786985473 40.1K |
| ADVERTISER_NAME | who | 20.6K | 0 | Bharatiya Janata Party 275.1K; MIKE BLOOMBERG 2020 INC 64.8K; BIDEN FOR PRESIDENT 64.2K; KEVIN COMBS 40.1K |
| AD_CAMPAIGNS_LIST | empty | 0 | 1.56M |  |
| DATE_RANGE_START | date | 2.9K | 0 | 2024-05-10 19.1K; 2024-04-01 15.1K; 2024-04-06 14.6K; 2020-07-07 12.2K |
| DATE_RANGE_END | date | 2.5K | 0 | 2024-04-17 36.0K; 2020-11-03 26.1K; 2024-04-19 23.4K; 2024-11-05 21.8K |
| NUM_OF_DAYS | other | 1.2K | 0 | 1 150.3K; 2 144.1K; 3 115.6K; 4 108.2K |
| IMPRESSIONS | who | 56 | 0 | 0-1000 539.9K; 1000-2000 91.6K; 10000-15000 68.2K; 2000-3000 59.3K |
| SPEND_USD | empty | 0 | 1.56M |  |
| FIRST_SERVED_TIMESTAMP | date | 664.6K | 0 | 2024-05-10T18:30 13.4K; 2019-08-31T07:00 5.3K; 2019-09-01T07:00 4.9K; 2019-08-22T07:00 3.2K |
| LAST_SERVED_TIMESTAMP | date | 581.0K | 0 | 2024-05-10T18:31 6.4K; 2020-03-03T22:00 3.9K; 2020-03-03T22:01 3.5K; 2024-11-18T11:28 3.3K |
| AGE_TARGETING | who | 101 | 897.6K | 18-24, 25-34, 35-44, 45-5 241.3K; 18-24, 25-34, 35-44, 45-5 94.5K; 35-44, 45-54, 55-64, ≥65 67.9K; 35-44, 45-54, 55-64, ≥65, 39.6K |
| GENDER_TARGETING | category | 7 | 1.02M | Male, Female, Unknown gen 434.6K; Female 47.7K; Male 31.0K; Male, Female 16.1K |
| GEO_TARGETING_INCLUDED | who | 46.3K | 40.8K | United States 238.1K; India 32.2K; Pennsylvania,United State 16.0K; Arizona,United States 15.6K |
| GEO_TARGETING_EXCLUDED | who | 5.8K | 1.24M | Brazil, Canada, India, Ja 33.7K; Afghanistan, Alaska,Unite 12.3K; Afghanistan, Albania, Alg 9.7K; Bangladesh, India, Indone 5.5K |
| IS_FUNDED_BY_GOOGLE_AD_GRANTS | category | 2 | 0 | No 1.56M; Yes 375 |
| SPEND_RANGE_MIN_USD | amount | 57 | 0 | 0 1.15M; 100 65.2K; 200 39.0K; 1000 34.0K |
| SPEND_RANGE_MAX_USD | amount | 57 | 5 | 100 1.15M; 200 65.2K; 300 39.0K; 1500 34.0K |
| SPEND_RANGE_MIN_EUR | other | 1 | 0 | 0 1.56M |
| SPEND_RANGE_MAX_EUR | other | 1 | 0 | 50 1.56M |
| SPEND_RANGE_MIN_INR | amount | 51 | 0 | 0 1.40M; 250 24.1K; 500 13.6K; 1000 12.8K |
| SPEND_RANGE_MAX_INR | amount | 51 | 258 | 250 1.40M; 500 24.1K; 750 13.6K; 1500 12.8K |
| SPEND_RANGE_MIN_BGN | other | 1 | 0 | 0 1.56M |
| SPEND_RANGE_MAX_BGN | other | 1 | 0 | 100 1.56M |
| SPEND_RANGE_MIN_CZK | other | 1 | 0 | 0 1.56M |
| SPEND_RANGE_MAX_CZK | other | 1 | 0 | 1500 1.56M |
| SPEND_RANGE_MIN_DKK | other | 1 | 0 | 0 1.56M |
| SPEND_RANGE_MAX_DKK | other | 1 | 0 | 500 1.56M |
| SPEND_RANGE_MIN_HUF | other | 1 | 0 | 0 1.56M |
| SPEND_RANGE_MAX_HUF | other | 1 | 0 | 20000 1.56M |
| SPEND_RANGE_MIN_PLN | other | 1 | 0 | 0 1.56M |
| SPEND_RANGE_MAX_PLN | other | 1 | 0 | 250 1.56M |
| SPEND_RANGE_MIN_RON | other | 1 | 0 | 0 1.56M |
| SPEND_RANGE_MAX_RON | other | 1 | 0 | 250 1.56M |
| SPEND_RANGE_MIN_SEK | other | 1 | 0 | 0 1.56M |
| SPEND_RANGE_MAX_SEK | other | 1 | 0 | 1000 1.56M |
| SPEND_RANGE_MIN_GBP | amount | 47 | 0 | 0 1.55M; 50 2.7K; 100 1.3K; 150 770 |
| SPEND_RANGE_MAX_GBP | amount | 48 | 0 | 50 1.55M; 100 2.7K; 150 1.3K; 200 770 |
| SPEND_RANGE_MIN_NZD | amount | 31 | 0 | 0 1.56M; 200 470; 400 216; 600 157 |
| SPEND_RANGE_MAX_NZD | amount | 32 | 0 | 200 1.56M; 400 470; 600 216; 800 157 |
| SPEND_RANGE_MIN_ILS | amount | 32 | 0 | 0 1.56M; 250 776; 500 359; 1000 253 |
| SPEND_RANGE_MAX_ILS | amount | 33 | 0 | 250 1.56M; 500 776; 750 359; 1500 253 |
| SPEND_RANGE_MIN_AUD | amount | 48 | 0 | 0 1.54M; 150 4.7K; 300 2.7K; 1000 2.6K |
| SPEND_RANGE_MAX_AUD | amount | 49 | 0 | 150 1.54M; 300 4.7K; 450 2.7K; 1500 2.6K |
| SPEND_RANGE_MIN_TWD | amount | 27 | 0 | 0 1.56M; 3000 500; 6000 201; 9000 164 |
| SPEND_RANGE_MAX_TWD | amount | 27 | 0 | 3000 1.56M; 6000 500; 9000 201; 12000 164 |
| SPEND_RANGE_MIN_BRL | amount | 28 | 0 | 0 1.54M; 500 5.8K; 1000 2.9K; 1500 2.0K |
| SPEND_RANGE_MAX_BRL | amount | 27 | 148 | 500 1.54M; 1000 5.8K; 1500 2.9K; 2000 2.0K |
| SPEND_RANGE_MIN_ARS | amount | 35 | 0 | 0 1.54M; 15000 4.5K; 30000 2.5K; 45000 1.7K |
| SPEND_RANGE_MAX_ARS | amount | 34 | 52 | 15000 1.54M; 30000 4.5K; 45000 2.5K; 60000 1.7K |
| SPEND_RANGE_MIN_ZAR | amount | 11 | 0 | 0 1.56M; 15000 40; 30000 29; 45000 12 |
| SPEND_RANGE_MAX_ZAR | amount | 11 | 0 | 15000 1.56M; 30000 40; 45000 29; 60000 12 |
| SPEND_RANGE_MIN_CLP | amount | 28 | 0 | 0 1.56M; 50000 818; 100000 455; 150000 294 |
| SPEND_RANGE_MAX_CLP | amount | 27 | 11 | 50000 1.56M; 100000 818; 150000 455; 200000 294 |
| SPEND_RANGE_MIN_MXN | amount | 39 | 0 | 0 1.55M; 1000 2.0K; 2000 1.1K; 10000 659 |
| SPEND_RANGE_MAX_MXN | amount | 39 | 0 | 1000 1.55M; 2000 2.0K; 3000 1.1K; 15000 659 |
| UNNAMED_59 | empty | 0 | 1.56M |  |
| INGESTED_AT | audit | 1 | 0 | 1785965602280091 1.56M |
| SOURCE_RUN_ID | audit | 1 | 0 | 4141cf7d-a262-4c65-b58b-3 1.56M |
| SRC_SHA256 | other | 1 | 0 | b4de0c2647cdab05b29b428eb 1.56M |
