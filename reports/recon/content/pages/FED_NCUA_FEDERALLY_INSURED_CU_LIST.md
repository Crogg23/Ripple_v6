# FED_NCUA_FEDERALLY_INSURED_CU_LIST

rows 4.2K  columns 26  scan 4.8s

roles: amount 11, audit 2, category 3, id 3, other 2, state 1, who 4

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_ASSETS | 4.2K | 1 | 66.14M | 8.61B | 203.56B | 2483.96B |
| TOTAL_LOANS | 4.2K | 0 | 32.59M | 5.73B | 143.35B | 1729.49B |
| TOTAL_DEPOSITS | 4.2K | 0 | 57.05M | 7.33B | 173.18B | 2122.79B |
| RETURN_ON_AVERAGE_ASSETS | 4.2K | -314.01 | 0.66 | 3.53 | 400 | 2.0K |
| NET_WORTH_RATIO_EXCLUDES_CECL_TRANSITION_PROVISION | 4.2K | -107.94 | 12.44 | 42.15 | 100 | 60.8K |
| LOAN_TO_SHARE_RATIO | 4.2K | 0 | 67.85 | 111.13 | 144.29 | 278.5K |

## who

CREDIT_UNION_NAME by rows
         5  UNIVERSITY
         5  COMMUNITY FIRST
         4  HEARTLAND
         4  FIRST COMMUNITY
         4  CITY
         4  HORIZON
         3  CONSUMERS
         3  FIRST CHOICE
         3  MEMBERS FIRST
         3  COMMUNITY
         3  ADVANTAGE
         3  MEMBERS
         3  UNITED
         3  FEDERAL EMPLOYEES
         3  FINANCIAL PLUS
         3  PUBLIC SERVICE
         3  PEOPLES
         3  MEMBERS 1ST
         3  VALLEY
         3  FINANCIAL PARTNERS

CREDIT_UNION_NAME by dollars
     203.56B        1 rows  NAVY FEDERAL CREDIT UNION
      59.76B        1 rows  STATE EMPLOYEES'
      36.74B        1 rows  SCHOOLSFIRST
      30.01B        1 rows  BOEING EMPLOYEES
      29.40B        1 rows  PENTAGON
      28.58B        1 rows  FIRST TECHNOLOGY
      24.73B        1 rows  AMERICA FIRST
      22.66B        1 rows  MOUNTAIN AMERICA
      21.74B        1 rows  THE GOLDEN 1
      20.54B        1 rows  SUNCOAST
      19.66B        1 rows  ALLIANT
      19.48B        1 rows  ENT
      19.19B        1 rows  RANDOLPH-BROOKS
      16.86B        1 rows  LAKE MICHIGAN
      14.95B        1 rows  IDAHO CENTRAL
      14.37B        1 rows  FOURLEAF
      14.21B        1 rows  SECURITY SERVICE
      13.80B        1 rows  VYSTAR
      12.86B        1 rows  GLOBAL
      11.29B        4 rows  FIRST COMMUNITY

YEAR_AND_QUARTER by rows
      4.2K  2026.1

YEAR_AND_QUARTER by dollars
    2483.96B     4.2K rows  2026.1

CITY_MAILING_ADDRESS by rows
        39  Houston
        26  Chicago
        20  Washington
        19  Springfield
        16  Honolulu
        15  Dallas
        15  Pittsburgh
        15  Austin
        13  New York
        13  San Antonio
        13  Philadelphia
        12  New Orleans
        12  Baton Rouge
        12  WASHINGTON
        12  Portland
        12  Birmingham
        11  JACKSON
        11  Richmond
        11  Fort Worth
        11  Nashville

CITY_MAILING_ADDRESS by dollars
     203.56B        2 rows  VIENNA
      62.96B        3 rows  RALEIGH
      36.75B        2 rows  SANTA ANA
      35.64B        4 rows  SAN JOSE
      30.01B        1 rows  TUKWILA
      29.40B        1 rows  MCLEAN
      24.73B        1 rows  RIVERDALE
      23.77B        3 rows  TAMPA
      22.66B        1 rows  SANDY
      22.64B        7 rows  San Diego
      21.97B       13 rows  San Antonio
      21.74B        1 rows  SACRAMENTO
      20.48B        5 rows  Colorado Spring
      20.33B        9 rows  CHICAGO
      19.73B        9 rows  Phoenix
      19.19B        1 rows  UNIVERSAL CITY
      18.91B       39 rows  Houston
      18.56B        6 rows  Grand Rapids
      17.67B        8 rows  Jacksonville
      17.58B       13 rows  Philadelphia

SRC_SHA256 by rows
      4.2K  41f7d9655ef7d1d105c9718c2f307f30b8a94a37b2e11f953600ca09ab31a050

SRC_SHA256 by dollars
    2483.96B     4.2K rows  41f7d9655ef7d1d105c9718c2f307f30b8a94a37b2e11f953600ca09ab31

## where

STATE_MAILING_ADDRESS: TX 376, PA 272, NY 269, CA 232, IL 175, MI 170, OH 159, LA 136, NJ 127, TN 126, MA 122, IN 116

## what

CREDIT_UNION_TYPE: FCU 63%, FISCU 37%

NCUA_REGION: 2 35%, 1 33%, 3 32%, 8 0%

LOW_INCOME_DESIGNATION: Yes 56%, No 44%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| CHARTER_NUMBER | id | 4.2K | 0 | 68748 22; 68747 22; 68746 22; 68745 22 |
| YEAR_AND_QUARTER | who | 1 | 0 | 2026.1 4.2K |
| CREDIT_UNION_NAME | who | 4.0K | 0 | MID OREGON 22; MT. RAINIER 22; CHRISTIAN FAMILY 22; UNITY FINANCIAL 22 |
| STREET_MAILING_ADDRESS | id | 4.1K | 0 | 63088 18th St 22; 303 W Meeker 22; PO BOX 2800 22; 20 York St, Rm 80CB 22 |
| CITY_MAILING_ADDRESS | who | 2.3K | 0 | Houston 39; Springfield 29; Nashville 28; Chicago 28 |
| STATE_MAILING_ADDRESS | state | 54 | 0 | TX 376; PA 272; NY 269; CA 232 |
| ZIP_CODE_MAILING_ADDRESS | other | 3.3K | 0 | 37214 24; 97701 22; 98371 22; 44720 22 |
| CREDIT_UNION_TYPE | category | 2 | 0 | FCU 2.7K; FISCU 1.6K |
| NCUA_REGION | category | 4 | 0 | 2 1.5K; 1 1.4K; 3 1.4K; 8 12 |
| LOW_INCOME_DESIGNATION | category | 2 | 0 | Yes 2.4K; No 1.9K |
| MEMBERS | other | 3.7K | 0 | 52362 22; 1146 22; 5069 22; 8186 22 |
| TOTAL_ASSETS | amount | 4.3K | 0 | 877737189 22; 26870942 22; 95827445 22; 65388728 22 |
| TOTAL_LOANS | amount | 4.3K | 0 | 748608800 22; 6728323 22; 37452058 22; 44093004 22 |
| TOTAL_DEPOSITS | amount | 4.2K | 0 | 775270477 22; 23327153 22; 84829406 22; 56960397 22 |
| RETURN_ON_AVERAGE_ASSETS | amount | 4.2K | 0 | 1.8353035454931979 22; 0.033927231287175105 22; 0.7298705252602838 22; 0.3034424254518163 22 |
| NET_WORTH_RATIO_EXCLUDES_CECL_TRANSITION_PROVISION | amount | 4.3K | 0 | 11.40265847844804 22; 13.050435671365745 22; 13.107212657083783 22; 12.839087495324883 22 |
| LOAN_TO_SHARE_RATIO | amount | 4.2K | 0 | 96.56098383841851 22; 28.843309768663154 22; 44.149852941325555 22; 77.40993097362015 22 |
| TOTAL_DEPOSITS_4_QUARTER_GROWTH | amount | 4.3K | 0 | 12.500231959846442 22; 1.348899956514149 22; 20.063656404537223 22; -0.7184943423182988 22 |
| TOTAL_LOANS_4_QUARTER_GROWTH | amount | 4.3K | 0 | 0 23; 10.834140222347965 22; 8.867079483067997 22; 11.267091706377963 22 |
| TOTAL_ASSETS_4_QUARTER_GROWTH | amount | 4.3K | 0 | 12.792184322402878 22; 2.0956069994172655 22; 20.429504308595693 22; -0.3386053748089646 22 |
| MEMBERS_4_QUARTER_GROWTH | amount | 4.2K | 0 | 0 48; 5.472857286735833 22; -2.9635901778154117 22; 43.43520090548954 22 |
| NET_WORTH_4_QUARTER_GROWTH_EXCLUDES_CECL_TRANSITION_PROVISION | amount | 4.2K | 0 | 17.325586352897272 22; 7.17101704394385 22; 11.852972860910938 22; -1.0785158400386075 22 |
| NCUA_INTERNAL_ID_JOIN_NUMBER | id | 4.2K | 0 | 6007 22; 9522 22; 25253 22; 2973 22 |
| INGESTED_AT | audit | 1 | 0 | 1786129683120485 4.2K |
| SOURCE_RUN_ID | audit | 1 | 0 | 7818e4e3-3281-4b5f-b70e-b 4.2K |
| SRC_SHA256 | who | 1 | 0 | 41f7d9655ef7d1d105c9718c2 4.2K |
