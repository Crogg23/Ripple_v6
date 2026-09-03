# PORTAL_CKA_OPEN_DATA_SA_6D1B83AC0A

rows 115  columns 28  scan 4.2s

roles: amount 2, audit 2, category 6, date 3, other 14, who 2

## when

LAST_UPDATED
  2023         4  #
  2024        10  ####
  2025        16  ######
  2026        85  ##############################

DATE_FOUNDED
  1968         1  ########
  1979         1  ########
  1984         1  ########
  1990         1  ########
  1999         1  ########
  2004         1  ########
  2006         2  ###############
  2017         1  ########
  2018         3  ######################
  2019         1  ########
  2020         1  ########
  2021         1  ########
  2022         1  ########
  2023         4  ##############################
  2025         3  ######################

INGESTED_AT
  2026       115  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SHAPE__AREA | 115 | 1.5K | 95.7K | 14.29B | 14.29B | 102.31B |
| SHAPE__LENGTH | 115 | 185.85 | 1.3K | 2.31M | 2.31M | 17.11M |

## who

COMMUNITY_ORGANIZATION by rows
         1  Prospect Hill Neighborhood Association
         1  Poseidon Disaster Response
         1  Girl Scout Troop 05078
         1  Girl Scout Troop 05060
         1  Gardening Volunteers of South Texas
         1  Alpha Kappa Alpha Sorority Alpha Alpha Xi Omega Chapter
         1  The Curiosity Club
         1  Glenoaks Neighbors Together
         1  Friends of Lorence Creek Park
         1  YES 2 YOU
         1  The Rock SCT
         1  Empower House
         1  Youth For Liberation SATX 
         1  Friendship Is The New Pretty 2, INC
         1  Filipino American National Historical Society San Antonio 
         1  PrepperNet San Antonio
         1  HUG ME Ink
         1  Friends of McAllister Park
         1  Parent Child Incorporated
         1  T.H.U.G.G.I.N. for Christ

COMMUNITY_ORGANIZATION by dollars
      14.29B        1 rows  Women in Film & Television Texas
      14.29B        1 rows  AMPED Inc.
      14.29B        1 rows  Liberation Library
      14.29B        1 rows  NextGen Education and Success Foundation (NES Foundation)
      14.29B        1 rows  San Antonio African American Community Archive Museum
      14.29B        1 rows  Lifeline Overeaters Anonymous
      14.29B        1 rows  Kool Kids Friendship Homeschool Co-Op
       1.28B        1 rows  irSol
     816.75M        1 rows  San Antonio Texas District One Resident Association
      80.43M        1 rows  Prospect Hill Neighborhood Association
      60.05M        1 rows  Brady Gardens Neighborhood Association 
      16.35M        1 rows  Government Hill Tomorrow
       8.08M        1 rows  Randolph Hills Civic Club
       6.83M        1 rows  Glenoaks Neighbors Together
       3.86M        1 rows  Friends of Lorence Creek Park
       2.22M        1 rows  Woodglen Neighborhood Group
       1.69M        1 rows  Gardening Volunteers of South Texas
      814.3K        1 rows  Alpha Kappa Alpha Sorority Alpha Alpha Xi Omega Chapter
      639.4K        1 rows  The Curiosity Club
      436.5K        1 rows  Jeevan Pehar

SRC_SHA256 by rows
       115  d31b2ae0c1400072baeadc90a25bc941ac617133096c9e1b80fd3997d42fcb5e

SRC_SHA256 by dollars
     102.31B      115 rows  d31b2ae0c1400072baeadc90a25bc941ac617133096c9e1b80fd3997d42f

## who x when

COMMUNITY_ORGANIZATION by DATE_FOUNDED, dollars = SHAPE__AREA
  Brady Gardens Neighborhood Association    2023:60.05M
  Friends of Lorence Creek Park             2020:3.86M
  Glenoaks Neighbors Together               2025:6.83M
  Lifeline Overeaters Anonymous             2006:14.29B
  Parent Child Incorporated                 1979:102.5K
  Prospect Hill Neighborhood Association    2006:80.43M
  San Antonio African American Community A  2017:14.29B
  San Antonio Texas District One Resident   2021:816.75M
  Women in Film & Television Texas          2023:14.29B
  irSol                                     2025:1.28B

SRC_SHA256 by DATE_FOUNDED, dollars = SHAPE__AREA
  d31b2ae0c1400072baeadc90a25bc941ac617133  1968:170.8K 1979:102.5K 1984:8.08M 1990:44.9K 1999:14.4K 2004:2.22M 2006:14.37B 2017:14.29B 2018:82.8K 2019:6.8K 2020:3.86M 2021:816.75M 2022:355.8K 2023:14.37B 2025:1.29B

## what

DISTRICT: 2 23%, 10 17%, Other 12%, 5 11%, 1 8%, 9 7%, 8 6%, 7 6%, 3 3%, 4 3%, Other  1%, 6 1%

NUMBER_OF_MEMBERS: 4 21%, 100 14%, 31 7%, 20 7%, 30 7%, 1 7%, 90 7%, 225 7%, 1200 7%, 240 7%, 35 7%

HOUSING_UNITS_IN_AREA: 400 23%, 206 8%, 20000 8%, 1000 8%, 1500 8%, 6114 8%, 0 8%, 500 8%, 90 8%, 1 8%, 3100 8%

DSD_NOTICES: No 80%, Yes 20%

STATUS: Registered 77%, Not Registered 23%

ALLCOSA: No 97%, Yes 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| COMMUNITY_ORGANIZATION | who | 116 | 0 | San Antonio City Wide NSB 1; H. E. Butt Foundation 1; Gen Alpha STEM Lab 1; San Antonio Persian Cultu 1 |
| PRIMARY_CONTACT | other | 110 | 0 | Seyit Ozturk 3; Michael Martinez 3; Nastassia Thomas 2; Rachel Cywinski 2 |
| PRIMARY_PHONE_NUMBER | other | 108 | 0 | 832-215-4799 3; 210-317-9487 3; 915-792-1109 2; N/A 2 |
| PRIMARY_EMAIL_ADDRESS | other | 110 | 0 | seyitozturk@gmail.com 3; mike@itisour.biz 2; sanantonionsbejr@gmail.co 1; egonzales@hebfdn.org 1 |
| PRIMARY_ADDRESS | other | 117 | 0 | 2503 Verona Park 1; 140 W Sunset Rd., San Ant 1; 5900 Balcones Drive Suite 1; PO BOX 780573, SA, TX 782 1 |
| ALTERNATE_CONTACT | other | 110 | 0 | Ferda Akgul 3; Nastassia Thomas 2; N/A 2; Veronica Shepherd 2 |
| ALTERNATE_PHONE_NUMBER | other | 108 | 0 | N/A 3; 281-965-7436 3; 830-542-9438 3; 915-792-1109 2 |
| ALTERNATE_EMAIL_ADDRESS | other | 108 | 0 | N/A 3; ferdaakgul@gmail.com 3; nastassiat20@gmail.com 2; pastoramaribelpr@gmail.co 2 |
| ALTERNATE_ADDRESS | other | 110 | 1 | N/A 4; 2503 Verona Park 1; 140 W Sunset Rd., San Ant 1; 5900 Balcones Drive Suite 1 |
| DISTRICT | category | 12 | 0 | 2 27; 10 20; Other 14; 5 13 |
| MEETING_DAY_AND_TIME | other | 99 | 0 | N/A 6; Third Saturdays at 10 a.m 3; First Saturdays at 1 p.m. 2; Mondays 2 |
| MEETING_LOCATION | other | 86 | 0 | N/A 8; Julia Yates Semmes Librar 7; Molly Pruitt Library - 51 4; Zoom 3 |
| WEBSITE | other | 76 | 8 | N/A 33; https://www.sanantonionsb 1; https://hebfdn.org/ 1; www.mehrfoundationsa.org 1 |
| LAST_UPDATED | date | 94 | 0 | 3/26/2026 12:00:00 AM 8; 3/25/2026 12:00:00 AM 8; 4/13/2026 12:00:00 AM 4; 5/13/2026 12:00:00 AM 2 |
| DATE_FOUNDED | date | 24 | 92 | 12/1/2018 3:18:19 PM 1; 10/22/2004 1:34:01 PM 1; 1/1/2006 3:49:30 PM 1; 8/20/2025 4:50:45 PM 1 |
| NUMBER_OF_MEMBERS | category | 19 | 94 | 4 3; 100 2; 31 1; 20 1 |
| HOUSING_UNITS_IN_AREA | category | 14 | 100 | 400 3; 206 1; 20000 1; 1000 1 |
| DSD_NOTICES | category | 3 | 1 | No 91; Yes 23 |
| OBJECTID | other | 114 | 0 | 115 1; 114 1; 113 1; 112 1 |
| COMMUNITYID | other | 114 | 0 | 19 1; 14 1; 98 1; 4 1 |
| GLOBALID | other | 116 | 0 | f5a58b74-598c-4fc9-a2ae-e 1; d2ece49c-f95f-4ccb-931c-5 1; 0320e886-b4b8-4037-aed9-5 1; 349d219d-00c8-4fc7-8e9c-c 1 |
| STATUS | category | 2 | 0 | Registered 89; Not Registered 26 |
| ALLCOSA | category | 2 | 0 | No 111; Yes 4 |
| SHAPE__AREA | amount | 72 | 0 | 50943.662109375 14; 209954.06640625 7; 14288951446.4492 7; 22818.658203125 6 |
| SHAPE__LENGTH | amount | 72 | 0 | 863.475249111798 14; 1965.27006734538 7; 2314124.96766306 7; 592.511143881846 6 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:33:03.28604 115 |
| SOURCE_RUN_ID | audit | 1 | 0 | 512944b2-fe9c-462f-8e91-e 115 |
| SRC_SHA256 | who | 1 | 0 | d31b2ae0c1400072baeadc90a 115 |
