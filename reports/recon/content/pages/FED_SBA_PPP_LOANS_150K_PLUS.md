# FED_SBA_PPP_LOANS_150K_PLUS

rows 968.5K  columns 56  scan 8.0s

roles: amount 6, audit 2, category 11, date 3, id 1, other 15, state 4, who 14

## when

DATEAPPROVED
  2020    659.4K  ##############################
  2021    309.1K  ##############

LOANSTATUSDATE
  2020     60.2K  ###
  2021    689.2K  ##############################
  2022    195.5K  #########
  2023     10.2K  
  2024      2.1K  

FORGIVENESSDATE
  2020    118.2K  #####
  2021    683.4K  ##############################
  2022    136.8K  ######
  2023      4.1K  
  2024       594  

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| INITIALAPPROVALAMOUNT | 968.5K | 0 | 295.2K | 3.78M | 10.00M | 515.52B |
| CURRENTAPPROVALAMOUNT | 968.5K | 150.0K | 295.0K | 3.75M | 10.00M | 513.92B |
| UNDISBURSEDAMOUNT | 968.5K | 0 | 0 | 0 | 491.1K | 491.1K |
| PAYROLL_PROCEED | 966.7K | 0 | 287.1K | 3.60M | 10.00M | 497.73B |
| REFINANCE_EIDL_PROCEED | 22.8K | 0 | 0 | 199.9K | 2.95M | 157.65M |
| FORGIVENESSAMOUNT | 943.1K | 0.01 | 295.6K | 3.71M | 10.36M | 499.25B |

## who

BORROWERNAME by rows
        40  FIRST UNITED METHODIST CHURCH
        37  NEW APPLICATION
        28  THE CATHOLIC BISHOP OF CHICAGO
        26  FIRST BAPTIST CHURCH
        25  THE ROMAN CATHOLIC WELFARE CORPORATION OF OAKLAND
        24  TRINITY LUTHERAN CHURCH
        16  CHRIST UNITED METHODIST CHURCH
        15  YOUNG MEN'S CHRISTIAN ASSOCIATION
        14  SACRED HEART SCHOOL
        14  IMMACULATE CONCEPTION CHURCH
        13  CALVARY BAPTIST CHURCH
        13  FIRST PRESBYTERIAN CHURCH
        12  CENTRAL CATHOLIC HIGH SCHOOL
        12  TRINITY EVANGELICAL LUTHERAN CHURCH
        11  IMMANUEL LUTHERAN CHURCH
        11  TEMPLE SINAI
        11  FIRST CHRISTIAN CHURCH
        11  ST JOSEPH CHURCH
        10  OUR SAVIOR LUTHERAN CHURCH
        10  CHRIST EPISCOPAL CHURCH

BORROWERNAME by dollars
      24.27M       37 rows  NEW APPLICATION
      18.14M       15 rows  YOUNG MEN'S CHRISTIAN ASSOCIATION
      13.48M        2 rows  COMMUNITY BRIDGES INC
      13.35M       28 rows  THE CATHOLIC BISHOP OF CHICAGO
      12.34M        7 rows  NAVAJO NATION GAMING ENTERPRISE
      12.00M        2 rows  FRIES RESTAURANT MANAGEMENT LLC
      12.00M        2 rows  LAZY DOG RESTAURANTS LLC
      12.00M        2 rows  CARIBBEAN RESTAURANTS LLC
      12.00M        2 rows  ACTION ENTERPRISE HOLDINGS LLC
      12.00M        2 rows  SOUTH AMERICAN RESTAURANTS CORP.
      12.00M        2 rows  SHARI'S MANAGEMENT CORPORATION
      12.00M        2 rows  O'CHARLEY'S HOLDINGS LLC
      12.00M        2 rows  BERTUCCIS RESTAURANTS LLC
      12.00M        2 rows  MAD ANTHONY'S INCORPORATED
      12.00M        2 rows  OCEAN PARK MECHANICAL INC
      12.00M        2 rows  ROSE CASUAL DINING LP
      12.00M        2 rows  BRAVO BRIO RESTAURANTS LLC
      12.00M        2 rows  RMH FRANCHISE CORPORATION
      12.00M        2 rows  TSFR APPLE VENTURE LLC
      12.00M        2 rows  GRILL CONCEPTS INC

SERVICINGLENDERNAME by rows
     57.2K  JPMorgan Chase Bank, National Association
     40.3K  Bank of America, National Association
     25.5K  PNC Bank, National Association
     21.0K  Truist Bank
     17.1K  Manufacturers and Traders Trust Company
     16.5K  U.S. Bank, National Association
     15.9K  Loan Source Incorporated
     15.5K  Wells Fargo Bank, National Association
     15.4K  TD Bank, National Association
     14.2K  The Huntington National Bank
     13.4K  KeyBank National Association
     12.7K  Zions Bank, A Division of
     12.1K  BMO Bank National Association
     10.7K  First-Citizens Bank & Trust Company
      9.9K  Cross River Bank
      9.3K  Customers Bank
      8.5K  Fifth Third Bank
      7.9K  Citizens Bank, National Association
      7.6K  First Horizon Bank
      7.5K  Regions Bank

SERVICINGLENDERNAME by dollars
      29.89B    57.2K rows  JPMorgan Chase Bank, National Association
      20.30B    40.3K rows  Bank of America, National Association
      16.50B    25.5K rows  PNC Bank, National Association
      12.70B    21.0K rows  Truist Bank
      10.55B    17.1K rows  Manufacturers and Traders Trust Company
       8.83B    13.4K rows  KeyBank National Association
       8.57B    14.2K rows  The Huntington National Bank
       8.35B    16.5K rows  U.S. Bank, National Association
       8.34B    12.1K rows  BMO Bank National Association
       8.25B    15.4K rows  TD Bank, National Association
       7.83B    15.9K rows  Loan Source Incorporated
       7.57B    12.7K rows  Zions Bank, A Division of
       6.59B    15.5K rows  Wells Fargo Bank, National Association
       6.06B    10.7K rows  First-Citizens Bank & Trust Company
       5.63B     8.5K rows  Fifth Third Bank
       5.07B     7.4K rows  City National Bank
       4.59B     7.9K rows  Citizens Bank, National Association
       4.34B     7.6K rows  First Horizon Bank
       4.30B     5.2K rows  Comerica Bank
       4.28B     7.5K rows  Regions Bank

FRANCHISENAME by rows
      1.8K  McDonalds
      1.7K  General Motors, LLC (Chevrolet, Buick, GM, Cadillac) Dealer Sales and 
      1.3K  Ford Motor Company Dealer Sales and Service Agreement
      1.1K  IHOP
       882  Subway
       720  Chrysler - Sales and Service Agreement
       577  Denny's
       571  Holiday Inn Express (License Agreement)
       560  Hampton Inn
       502  Nissan North America, Inc. - Dealer Sales and Service Agreement
       485  Toyota Motors Sales, U.S.A., Inc. - Dealer Agreement
       464  Great Clips
       462  Hilton Garden Inn
       462  Honda Automobile Division - Dealer Sales and Service Agreement
       455  Holiday Inn
       442  Massage Envy
       423  Dunkin' Donuts
       419  Best Western - Membership Agreement
       362  Primrose Schools
       345  Courtyard by Marriott

FRANCHISENAME by dollars
       1.38B     1.7K rows  General Motors, LLC (Chevrolet, Buick, GM, Cadillac) Dealer 
       1.23B     1.8K rows  McDonalds
     948.86M     1.3K rows  Ford Motor Company Dealer Sales and Service Agreement
     570.36M      485 rows  Toyota Motors Sales, U.S.A., Inc. - Dealer Agreement
     522.63M      720 rows  Chrysler - Sales and Service Agreement
     449.73M      462 rows  Honda Automobile Division - Dealer Sales and Service Agreeme
     395.80M      502 rows  Nissan North America, Inc. - Dealer Sales and Service Agreem
     328.78M      882 rows  Subway
     318.42M     1.1K rows  IHOP
     310.34M      209 rows  Wendy's
     306.21M      272 rows  Burger King
     294.65M      577 rows  Denny's
     272.93M      268 rows  Marriott/JW Marriott
     270.41M      155 rows  Taco Bell
     262.13M      168 rows  Applebee's Neighborhood Grill & Bar
     229.29M      464 rows  Great Clips
     199.00M      110 rows  Pizza Hut
     192.53M       70 rows  Panera Bread
     190.22M      423 rows  Dunkin' Donuts
     171.95M      455 rows  Holiday Inn

PROJECTCOUNTYNAME by rows
     36.2K  LOS ANGELES
     21.2K  ORANGE
     21.2K  NEW YORK
     19.1K  COOK
     15.9K  HARRIS
     12.6K  MONTGOMERY
     11.9K  MARICOPA
     11.3K  MIDDLESEX
     11.3K  SAN DIEGO
     11.1K  DALLAS
     11.0K  SUFFOLK
     11.0K  JEFFERSON
     10.5K  MIAMI-DADE
      9.9K  KING
      8.2K  CLARK
      7.6K  WASHINGTON
      7.3K  SANTA CLARA
      7.1K  BROWARD
      6.9K  ALAMEDA
      6.9K  HENNEPIN

PROJECTCOUNTYNAME by dollars
      19.22B    36.2K rows  LOS ANGELES
      13.16B    21.2K rows  NEW YORK
      11.51B    19.1K rows  COOK
      11.48B    21.2K rows  ORANGE
       9.10B    15.9K rows  HARRIS
       6.94B    12.6K rows  MONTGOMERY
       6.49B    11.1K rows  DALLAS
       6.44B    11.3K rows  MIDDLESEX
       6.30B    11.9K rows  MARICOPA
       6.24B    11.0K rows  SUFFOLK
       6.08B    11.3K rows  SAN DIEGO
       6.03B    11.0K rows  JEFFERSON
       5.80B     9.9K rows  KING
       5.04B    10.5K rows  MIAMI-DADE
       4.30B     6.9K rows  HENNEPIN
       4.21B     8.2K rows  CLARK
       4.08B     6.9K rows  ALAMEDA
       4.03B     7.3K rows  SANTA CLARA
       3.89B     7.6K rows  WASHINGTON
       3.79B     6.7K rows  KINGS

## who x when

BORROWERNAME by DATEAPPROVED, dollars = INITIALAPPROVALAMOUNT
  ACTION ENTERPRISE HOLDINGS LLC            2020:10.00M 2021:2.00M
  BERTUCCIS RESTAURANTS LLC                 2020:10.00M 2021:2.00M
  CALVARY BAPTIST CHURCH                    2020:3.36M 2021:509.5K
  CARIBBEAN RESTAURANTS LLC                 2020:10.00M 2021:2.00M
  CENTRAL CATHOLIC HIGH SCHOOL              2020:4.32M 2021:2.16M
  CHRIST EPISCOPAL CHURCH                   2020:1.95M 2021:320.4K
  CHRIST UNITED METHODIST CHURCH            2020:4.03M 2021:1.48M
  COMMUNITY BRIDGES INC                     2020:3.48M 2021:10.00M
  FIRST BAPTIST CHURCH                      2020:6.15M 2021:369.8K
  FIRST CHRISTIAN CHURCH                    2020:1.96M 2021:580.9K
  FIRST PRESBYTERIAN CHURCH                 2020:3.20M 2021:934.8K
  FIRST UNITED METHODIST CHURCH             2020:8.05M 2021:1.37M
  FRIES RESTAURANT MANAGEMENT LLC           2020:10.00M 2021:2.00M
  IMMACULATE CONCEPTION CHURCH              2020:3.78M 2021:189.8K
  IMMANUEL LUTHERAN CHURCH                  2020:2.21M 2021:536.8K
  LAZY DOG RESTAURANTS LLC                  2020:10.00M 2021:2.00M
  NAVAJO NATION GAMING ENTERPRISE           2020:11.15M 2021:1.19M
  NEW APPLICATION                           2020:24.27M
  O'CHARLEY'S HOLDINGS LLC                  2020:10.00M 2021:2.00M
  OUR SAVIOR LUTHERAN CHURCH                2020:1.64M 2021:742.0K
  SACRED HEART SCHOOL                       2020:3.11M 2021:841.4K
  SHARI'S MANAGEMENT CORPORATION            2020:10.00M 2021:2.00M
  SOUTH AMERICAN RESTAURANTS CORP.          2020:10.00M 2021:2.00M
  ST JOSEPH CHURCH                          2020:2.60M 2021:802.5K
  TEMPLE SINAI                              2020:1.78M 2021:1.83M
  THE CATHOLIC BISHOP OF CHICAGO            2020:8.96M 2021:4.39M
  THE ROMAN CATHOLIC WELFARE CORPORATION O  2020:10.01M 2021:346.8K
  TRINITY EVANGELICAL LUTHERAN CHURCH       2020:3.48M 2021:514.8K
  TRINITY LUTHERAN CHURCH                   2020:4.76M 2021:1.22M
  YOUNG MEN'S CHRISTIAN ASSOCIATION         2020:3.69M 2021:14.45M

SERVICINGLENDERNAME by DATEAPPROVED, dollars = INITIALAPPROVALAMOUNT
  BMO Bank National Association             2020:6.57B 2021:1.77B
  Bank of America, National Association     2020:15.89B 2021:4.42B
  Citizens Bank, National Association       2020:3.44B 2021:1.15B
  City National Bank                        2020:3.83B 2021:1.23B
  Comerica Bank                             2020:3.46B 2021:839.61M
  Cross River Bank                          2020:2.53B 2021:848.90M
  Customers Bank                            2020:2.72B 2021:976.37M
  Fifth Third Bank                          2020:4.35B 2021:1.28B
  First Horizon Bank                        2020:3.26B 2021:1.07B
  First-Citizens Bank & Trust Company       2020:4.71B 2021:1.35B
  JPMorgan Chase Bank, National Associatio  2020:22.20B 2021:7.69B
  KeyBank National Association              2020:6.75B 2021:2.08B
  Loan Source Incorporated                  2020:3.86B 2021:3.97B
  Manufacturers and Traders Trust Company   2020:7.68B 2021:2.87B
  PNC Bank, National Association            2020:13.02B 2021:3.48B
  Regions Bank                              2020:3.41B 2021:870.28M
  TD Bank, National Association             2020:5.99B 2021:2.27B
  The Huntington National Bank              2020:6.72B 2021:1.85B
  Truist Bank                               2020:10.22B 2021:2.47B
  U.S. Bank, National Association           2020:6.34B 2021:2.01B
  Wells Fargo Bank, National Association    2020:5.37B 2021:1.22B
  Zions Bank, A Division of                 2020:5.54B 2021:2.04B

## where

BORROWERSTATE: CA 130.6K, TX 76.2K, NY 74.1K, FL 60.0K, IL 40.8K, PA 38.5K, OH 32.6K, NJ 32.5K, MI 29.8K, MA 27.5K, GA 25.8K, WA 23.8K

SERVICINGLENDERSTATE: OH 124.1K, NC 80.3K, NY 61.3K, CA 58.1K, TX 54.8K, DE 44.6K, IL 40.0K, PA 39.3K, UT 29.2K, FL 26.2K, NJ 25.6K, SD 25.0K

PROJECTSTATE: CA 130.6K, TX 76.2K, NY 74.1K, FL 60.0K, IL 40.8K, PA 38.5K, OH 32.6K, NJ 32.5K, MI 29.8K, MA 27.5K, GA 25.8K, WA 23.8K

ORIGINATINGLENDERSTATE: CA 78.0K, NC 76.6K, OH 76.3K, IL 72.9K, TX 57.0K, NY 47.1K, DE 39.7K, PA 35.3K, UT 30.2K, NJ 29.7K, SD 29.7K, FL 25.3K

## what

PROCESSINGMETHOD: PPP 70%, PPS 30%

LOANSTATUS: Paid in Full 97%, Charged Off 2%, Exemption 4 1%

RURALURBANINDICATOR: U 85%, R 15%

HUBZONEINDICATOR: N 73%, Y 27%

LMIINDICATOR: N 74%, Y 26%

BUSINESSAGEDESCRIPTION: Existing or more than 2 years  89%, New Business or 2 years or les 6%, Unanswered 5%, Change of Ownership 0%, Startup, Loan Funds will Open  0%

RACE: Unanswered 79%, White 17%, Asian 2%, Black or African American 1%, American Indian or Alaska Nati 1%, Native Hawaiian or Other Pacif 0%, Puerto Rican 0%, Multi Group 0%, Eskimo & Aleut 0%

ETHNICITY: Unknown/NotStated 71%, Not Hispanic or Latino 26%, Hispanic or Latino 2%

BUSINESSTYPE: Corporation 43%, Limited  Liability Company(LLC 27%, Subchapter S Corporation 18%, Non-Profit Organization 6%, Partnership 2%, Limited Liability Partnership 1%, Sole Proprietorship 1%, Professional Association 1%, Cooperative 0%, 501(c)3 � Non Profit 0%, Non-Profit Childcare Center 0%, 501(c)6 � Non Profit Membershi 0%

GENDER: Unanswered 59%, Male Owned 34%, Female Owned 7%

VETERAN: Unanswered 67%, Non-Veteran 31%, Veteran 2%, Active Duty Military eligible  0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| LOANNUMBER | id | 964.3K | 0 | 9152437103 770; 3609278506 770; 5099057207 770; 1005377701 770 |
| DATEAPPROVED | date | 241 | 0 | 05/01/2020 70.6K; 04/15/2020 58.7K; 04/28/2020 47.7K; 04/14/2020 47.6K |
| SBAOFFICECODE | other | 76 | 0 | 0202 43.7K; 0455 42.9K; 0914 40.9K; 0507 40.8K |
| PROCESSINGMETHOD | category | 2 | 0 | PPP 676.9K; PPS 291.7K |
| BORROWERNAME | who | 849.0K | 4 | SCG-B INC 770; THE ARC OF SAN ANTONIO IN 770; SKYLINE COUNTRY CLUB MANA 770; BALDWIN METALS CO INC 770 |
| BORROWERADDRESS | other | 865.8K | 14 | 1650 HIGHWAY 6 Suite 170 770; 13430 West Ave 770; 5430 LBJ Freeway Ste 1400 770; 1901 W COMMERCE 770 |
| BORROWERCITY | who | 27.8K | 12 | New York 13.2K; NEW YORK 9.8K; HOUSTON 7.7K; Houston 7.3K |
| BORROWERSTATE | state | 56 | 13 | CA 130.6K; TX 76.2K; NY 74.1K; FL 60.0K |
| BORROWERZIP | who | 508.0K | 13 | 78045 771; 77478-4957 770; 78216-2005 770; 75240 770 |
| LOANSTATUSDATE | date | 1.3K | 11.3K | 01/21/2021 13.8K; 02/18/2022 11.8K; 07/22/2021 11.2K; 09/29/2021 8.7K |
| LOANSTATUS | category | 3 | 0 | Paid in Full 940.1K; Charged Off 17.1K; Exemption 4 11.3K |
| TERM | other | 145 | 0 | 24 619.8K; 60 322.6K; 59 4.7K; 41 1.5K |
| SBAGUARANTYPERCENTAGE | other | 1 | 0 | 100 968.5K |
| INITIALAPPROVALAMOUNT | amount | 386.0K | 0 | 150000 7.1K; 2000000 6.0K; 600000 3.4K; 625000 2.2K |
| CURRENTAPPROVALAMOUNT | amount | 390.9K | 0 | 150000 7.2K; 2000000 6.0K; 600000 3.4K; 625000 1.5K |
| UNDISBURSEDAMOUNT | amount | 2 | 43 | 0 968.5K; 491066.85 1 |
| FRANCHISENAME | who | 1.5K | 933.1K | McDonalds 1.8K; General Motors, LLC (Chev 1.7K; Ford Motor Company Dealer 1.3K; IHOP 1.1K |
| SERVICINGLENDERLOCATIONID | other | 4.5K | 0 | 48270 57.2K; 9551 40.3K; 44449 25.5K; 225134 21.0K |
| SERVICINGLENDERNAME | who | 4.1K | 0 | JPMorgan Chase Bank, Nati 57.2K; Bank of America, National 40.3K; PNC Bank, National Associ 25.5K; Truist Bank 21.0K |
| SERVICINGLENDERADDRESS | who | 4.4K | 0 | 1111 Polaris Pkwy 57.2K; 100 N Tryon St, Ste 170 40.3K; 222 Delaware Ave 25.5K; 214 N Tryon St 21.0K |
| SERVICINGLENDERCITY | who | 2.9K | 0 | COLUMBUS 77.5K; CHARLOTTE 61.2K; WILMINGTON 47.8K; CINCINNATI 27.0K |
| SERVICINGLENDERSTATE | state | 55 | 0 | OH 124.1K; NC 80.3K; NY 61.3K; CA 58.1K |
| SERVICINGLENDERZIP | who | 4.5K | 0 | 43240-2031 57.2K; 28202-4024 40.3K; 19801-1621 25.5K; 28202-1078 21.0K |
| RURALURBANINDICATOR | category | 2 | 0 | U 823.9K; R 144.6K |
| HUBZONEINDICATOR | category | 2 | 0 | N 708.7K; Y 259.8K |
| LMIINDICATOR | category | 2 | 0 | N 713.9K; Y 254.6K |
| BUSINESSAGEDESCRIPTION | category | 5 | 1 | Existing or more than 2 y 861.9K; New Business or 2 years o 54.9K; Unanswered 51.1K; Change of Ownership 422 |
| PROJECTCITY | who | 27.8K | 13 | New York 13.3K; NEW YORK 9.8K; HOUSTON 7.7K; Houston 7.3K |
| PROJECTCOUNTYNAME | who | 1.9K | 57 | LOS ANGELES 36.4K; NEW YORK 21.6K; ORANGE 21.3K; COOK 19.5K |
| PROJECTSTATE | state | 56 | 9 | CA 130.6K; TX 76.2K; NY 74.1K; FL 60.0K |
| PROJECTZIP | who | 514.2K | 14 | 78045-0001 771; 77478-4957 770; 78216-2005 770; 75240-1000 770 |
| CD | other | 461 | 46 | NY-12 14.9K; NY-10 8.2K; IL-07 6.3K; CA-11 6.2K |
| JOBSREPORTED | other | 495 | 1 | 15 29.5K; 20 28.6K; 18 26.3K; 14 25.6K |
| NAICSCODE | who | 1.2K | 6.6K | 722511 76.6K; 621111 28.3K; 541110 20.0K; 721110 19.2K |
| RACE | category | 9 | 0 | Unanswered 768.6K; White 163.2K; Asian 22.2K; Black or African American 7.7K |
| ETHNICITY | category | 3 | 0 | Unknown/NotStated 690.9K; Not Hispanic or Latino 254.1K; Hispanic or Latino 23.6K |
| UTILITIES_PROCEED | other | 48.2K | 629.2K | 1 224.2K; 0 6.6K; 10000 2.5K; 5000 2.3K |
| PAYROLL_PROCEED | amount | 445.6K | 1.8K | 2000000 2.2K; 550000 2.2K; 1999998 1.5K; 510000 1.4K |
| MORTGAGE_INTEREST_PROCEED | other | 18.9K | 922.4K | 0 17.5K; 10000 449; 5000 404; 20000 391 |
| RENT_PROCEED | other | 42.7K | 869.0K | 0 6.0K; 20000 1.9K; 10000 1.6K; 30000 1.6K |
| REFINANCE_EIDL_PROCEED | amount | 732 | 945.7K | 0 21.1K; 10000 763; 150000 41; 1 24 |
| HEALTH_CARE_PROCEED | other | 27.0K | 911.1K | 0 5.7K; 20000 849; 10000 837; 15000 666 |
| DEBT_INTEREST_PROCEED | other | 8.0K | 936.8K | 0 15.3K; 10000 445; 5000 424; 2000 363 |
| BUSINESSTYPE | category | 25 | 713 | Corporation 418.2K; Limited  Liability Compan 261.5K; Subchapter S Corporation 174.8K; Non-Profit Organization 56.0K |
| ORIGINATINGLENDERLOCATIONID | other | 5.0K | 0 | 9551 40.3K; 194093 36.4K; 225134 21.0K; 44449 20.6K |
| ORIGINATINGLENDER | who | 4.2K | 0 | JPMorgan Chase Bank, Nati 57.2K; Bank of America, National 40.3K; Truist Bank 21.0K; PNC Bank, National Associ 20.6K |
| ORIGINATINGLENDERCITY | who | 3.1K | 0 | CHARLOTTE 61.2K; CHICAGO 43.2K; WILMINGTON 42.9K; COLUMBUS 34.0K |
| ORIGINATINGLENDERSTATE | state | 55 | 0 | CA 78.0K; NC 76.6K; OH 76.3K; IL 72.9K |
| GENDER | category | 3 | 0 | Unanswered 567.9K; Male Owned 328.7K; Female Owned 71.8K |
| VETERAN | category | 4 | 0 | Unanswered 647.4K; Non-Veteran 300.9K; Veteran 20.1K; Active Duty Military elig 31 |
| NONPROFIT | other | 1 | 911.7K | Y 56.9K |
| FORGIVENESSAMOUNT | amount | 898.1K | 25.5K | 508959.97 753; 501766.21 753; 502547.82 753; 504887.08 753 |
| FORGIVENESSDATE | date | 920 | 25.5K | 11/03/2020 22.1K; 03/31/2021 22.0K; 06/11/2021 17.8K; 02/16/2021 16.9K |
| INGESTED_AT | audit | 1 | 0 | 1786164855345512 968.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | e356dcf5-3f03-496f-b466-b 968.5K |
| SRC_SHA256 | other | 1 | 0 | 3760a581dc3fd7ca12d09996a 968.5K |
