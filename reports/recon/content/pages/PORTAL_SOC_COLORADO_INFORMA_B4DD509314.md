# PORTAL_SOC_COLORADO_INFORMA_B4DD509314

rows 2.0K  columns 47  scan 5.6s

roles: amount 33, audit 2, category 7, date 1, id 1, other 1, who 3

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PYGRANTSANDSIMILARPAIDAMT | 1.3K | 0 | 280 | 8.42M | 109.12M | 578.36M |
| CYGRANTSANDSIMILARPAIDAMT | 2.0K | 0 | 0 | 6.24M | 121.25M | 638.49M |
| PYBENEFITSPAIDTOMEMBERSAMT | 1.1K | 0 | 0 | 73.3K | 456.6K | 3.78M |
| CYBENEFITSPAIDTOMEMBERSAMT | 2.0K | 0 | 0 | 37.4K | 487.8K | 3.23M |
| PYSALARIESCOMPEMPBNFTPAIDAMT | 1.7K | -28 | 197.6K | 26.07M | 2.13B | 5.80B |
| CYSALARIESCOMPEMPBNFTPAIDAMT | 2.0K | 0 | 152.0K | 25.36M | 2.22B | 6.06B |

## who

BUSINESSNAME1 by rows
        10  COLORADO ROCKY MOUNTAIN SCHOOL
         7  Pikes Peak United Way
         7  Colorado Juniors Volleyball Inc
         6  ROCKY MOUNTAIN MULTIPLE SCLEROSIS CENTER
         6  THE WILDERNESS LAND TRUST
         6  The Word for the World USA
         5  COLORADO NURSERY & GREENHOUSE
         5  Committee For Catholic Secondary
         5  Humane Society of the Pikes Peak Region
         5  ASPEN COMMUNITY FOUNDATION
         4  BRIDGES CHILD PLACEMENT AGENCY
         4  Kids on Bikes Inc
         4  Silver Key Senior Services Inc
         4  TRI-COUNTY HEALTH NETWORK
         4  Centennial Mental Health Center
         4  Cherry Creek School District Parent Teacher
         4  DENVER BAR ASSOCIATION
         4  CLEAN ENERGY ECONOMY FOR THE REGION
         4  Global Mapping Project Inc
         4  RONALD MCDONALD HOUSE CHARITIES OF

BUSINESSNAME1 by dollars
     121.25M        1 rows  COLORADO SEMINARY
      56.23M        5 rows  ASPEN COMMUNITY FOUNDATION
      38.06M        4 rows  EDUCAUSE
      35.27M        3 rows  OPPORTUNITY INTERNATIONAL INC
      32.46M        1 rows  ENTERTAINMENT INDUSTRY FOUNDATION
      24.67M        7 rows  Pikes Peak United Way
      17.24M        2 rows  WESTERN KENTUCKY UNIVERSITY FOUNDATION
      13.64M        1 rows  new schools fund dba newschools venture fund
      12.35M        2 rows  SIMPSON UNIVERSITY
      11.92M        2 rows  CROWN COLLEGE
      11.45M        1 rows  Doane College
      11.14M        1 rows  THE SALVATION ARMY WORLD SERVICE OFFICE
       9.63M       10 rows  COLORADO ROCKY MOUNTAIN SCHOOL
       8.16M        2 rows  Neighborhood Development Collaborative Inc
       7.40M        1 rows  HELP INTERNATIONAL
       7.31M        1 rows  ASPEN VALLEY HOSPITAL FOUNDATION
       6.92M        3 rows  COLORADO ACADEMY
       6.75M        2 rows  DENVER SCHOOL OF SCIENCE AND TECHNOLOGY
       6.24M        1 rows  Mercy Ships
       6.21M        1 rows  SAINT JOSEPH HOSPITAL FOUNDATION

BUSINESSNAME2 by rows
      1.8K  nan
        17  INC
         8  FOUNDATION INC
         6  ASSOCIATION
         5  Education in Colorado Springs
         4  FOUNDATION
         4  CENTER
         4  Community Council Inc
         3  RESEARCH
         3  DBA HEART AND HAND CENTER
         3  VALLEY INC
         3  SENIOR COMMUNITIES
         3  C/O ALPHA CHI OMEGA NATL HOUSING CORP
         3  HABITAT FOR HUMANITY OF GUNNISON VALLEY
         3  SOUTHERN COLORADO
         3  UNITED STATES
         3  SWEET ADELINES INTERNATIONAL
         3  DEVELOPMENT CORPORATION
         3  SERVICES
         3  Association (CSAHA)

BUSINESSNAME2 by dollars
     566.83M     1.8K rows  nan
      35.27M        3 rows  D/B/A OPPORTUNITY INTERNATIONAL-US
      11.25M       17 rows  INC
       6.19M        8 rows  FOUNDATION INC
       3.26M        2 rows  Western Colorado
       2.39M        2 rows  PROMOTION & EDUCATION
       1.73M        1 rows  C/O PURCHASE SUNY
       1.29M        4 rows  Community Council Inc
       1.21M        1 rows  C/O PURCHASE COLLEGE SUNY
       1.12M        1 rows  TASK FORCE
      678.1K        4 rows  FOUNDATION
      673.3K        2 rows  PEDIATRICS INC
      596.2K        1 rows  INTERNATIONAL FRIENDS TSOKNYI NEPAL NUNS
      491.2K        3 rows  DEVELOPMENT CORPORATION
      450.0K        1 rows  STUDY OF LUNG CANCER
      435.5K        1 rows  C/O REESE HENRY & COMPANY
      404.5K        1 rows  OF LUNG CANCER
      394.9K        2 rows  C/O TOBIN RUPAREL KONCZAK & MUNDELL PC
      327.1K        2 rows  ASSOCIATION FOUNDATION
      284.6K        1 rows  CHILDREN'S FOUNDATION

SRC_SHA256 by rows
      2.0K  fd33df8b55dd605fe7cfe369b4b05fd2337074dbeac5282177506089bdcf592f

SRC_SHA256 by dollars
     638.49M     2.0K rows  fd33df8b55dd605fe7cfe369b4b05fd2337074dbeac5282177506089bdcf

## who x when

BUSINESSNAME1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CYGRANTSANDSIMILARPAIDAMT
  ASPEN COMMUNITY FOUNDATION                2026:56.23M
  BRIDGES CHILD PLACEMENT AGENCY            2026:0
  CLEAN ENERGY ECONOMY FOR THE REGION       2026:527.4K
  COLORADO NURSERY & GREENHOUSE             2026:0
  COLORADO ROCKY MOUNTAIN SCHOOL            2026:9.63M
  COLORADO SEMINARY                         2026:121.25M
  CROWN COLLEGE                             2026:11.92M
  Centennial Mental Health Center           2026:0
  Cherry Creek School District Parent Teac  2026:1.29M
  Colorado Juniors Volleyball Inc           2026:0
  Committee For Catholic Secondary          2026:0
  DENVER BAR ASSOCIATION                    2026:0
  Doane College                             2026:11.45M
  EDUCAUSE                                  2026:38.06M
  ENTERTAINMENT INDUSTRY FOUNDATION         2026:32.46M
  Global Mapping Project Inc                2026:0
  Humane Society of the Pikes Peak Region   2026:0
  Kids on Bikes Inc                         2026:0
  OPPORTUNITY INTERNATIONAL INC             2026:35.27M
  Pikes Peak United Way                     2026:24.67M
  ROCKY MOUNTAIN MULTIPLE SCLEROSIS CENTER  2026:750.5K
  RONALD MCDONALD HOUSE CHARITIES OF        2026:27.9K
  SIMPSON UNIVERSITY                        2026:12.35M
  Silver Key Senior Services Inc            2026:2.28M
  THE SALVATION ARMY WORLD SERVICE OFFICE   2026:11.14M
  THE WILDERNESS LAND TRUST                 2026:0
  TRI-COUNTY HEALTH NETWORK                 2026:0
  The Word for the World USA                2026:0
  WESTERN KENTUCKY UNIVERSITY FOUNDATION    2026:17.24M
  new schools fund dba newschools venture   2026:13.64M

BUSINESSNAME2 by INGESTED_AT  LOAD STAMP, not an event date, dollars = CYGRANTSANDSIMILARPAIDAMT
  ASSOCIATION                               2026:0
  Association (CSAHA)                       2026:27.0K
  C/O ALPHA CHI OMEGA NATL HOUSING CORP     2026:0
  C/O PURCHASE COLLEGE SUNY                 2026:1.21M
  C/O PURCHASE SUNY                         2026:1.73M
  C/O REESE HENRY & COMPANY                 2026:435.5K
  CENTER                                    2026:0
  Community Council Inc                     2026:1.29M
  D/B/A OPPORTUNITY INTERNATIONAL-US        2026:35.27M
  DBA HEART AND HAND CENTER                 2026:0
  DEVELOPMENT CORPORATION                   2026:491.2K
  Education in Colorado Springs             2026:0
  FOUNDATION                                2026:678.1K
  FOUNDATION INC                            2026:6.19M
  HABITAT FOR HUMANITY OF GUNNISON VALLEY   2026:0
  INC                                       2026:11.25M
  INTERNATIONAL FRIENDS TSOKNYI NEPAL NUNS  2026:596.2K
  PEDIATRICS INC                            2026:673.3K
  PROMOTION & EDUCATION                     2026:2.39M
  RESEARCH                                  2026:37.6K
  SENIOR COMMUNITIES                        2026:0
  SERVICES                                  2026:0
  SOUTHERN COLORADO                         2026:27.9K
  STUDY OF LUNG CANCER                      2026:450.0K
  SWEET ADELINES INTERNATIONAL              2026:1.0K
  TASK FORCE                                2026:1.12M
  UNITED STATES                             2026:265.2K
  VALLEY INC                                2026:0
  Western Colorado                          2026:3.26M
  nan                                       2026:566.83M

## what

TAXYR: 2013 30%, 2011 23%, 2016 12%, 2012 11%, 2015 8%, 2014 7%, 2010 6%, 2009 1%, 2017 1%

PROFESSIONALFUNDRAISINGIND: f 95%, t 5%

COMPENSATIONPROCESSCEOIND: t 52%, f 48%

COMPENSATIONPROCESSOTHERIND: f 63%, t 37%

INDIVRCVDGREATERTHAN100KCNT: 0 52%, nan 29%, 1 12%, 2 4%, 3 1%, 4 1%, 7 1%, 6 1%, 5 1%, 9 0%, 10 0%, 23 0%

CNTRCTRCVDGREATERTHAN100KCNT: 0 50%, nan 41%, 1 4%, 2 1%, 5 1%, 3 1%, 4 0%, 7 0%, 13 0%, 19 0%, 9 0%, 8 0%

JOINTCOSTSIND: f 95%, t 5%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 2.0K | 0 | 201312789349300001 10; 201721209349300302 10; 201741229349300624 10; 201111329349302986 10 |
| TAXYR | category | 9 | 0 | 2013 590; 2011 467; 2016 235; 2012 219 |
| BUSINESSNAME1 | who | 1.3K | 0 | ASPEN COMMUNITY FOUNDATIO 11; EAGLE COUNTY JUNIOR LIVES 11; COLORADO NURSERY & GREENH 11; ARVADA COMMUNITY FOOD BAN 11 |
| EIN | other | 1.2K | 0 | 840829226 11; 260320552 11; 841316133 11; 510166842 11 |
| PYGRANTSANDSIMILARPAIDAMT | amount | 625 | 0 | nan 701; 0 639; 5000 6; 99211 4 |
| CYGRANTSANDSIMILARPAIDAMT | amount | 661 | 0 | 0 1.3K; 5000 8; 500 5; 64633 4 |
| PYBENEFITSPAIDTOMEMBERSAMT | amount | 57 | 0 | 0 1.0K; nan 936; 168119 1; 2862 1 |
| CYBENEFITSPAIDTOMEMBERSAMT | amount | 52 | 0 | 0 1.9K; 107249 1; 2145 1; 3798 1 |
| PYSALARIESCOMPEMPBNFTPAIDAMT | amount | 1.5K | 0 | nan 275; 0 260; 109671 8; 298580 8 |
| CYSALARIESCOMPEMPBNFTPAIDAMT | amount | 1.5K | 0 | 0 477; 98582 8; 318951 8; 1149000 8 |
| PYTOTALPROFFNDRSNGEXPNSAMT | amount | 125 | 0 | 0 965; nan 909; 13500 2; 40681 2 |
| CYTOTALPROFFNDRSNGEXPNSAMT | amount | 113 | 0 | 0 1.9K; 5000 3; 75000 2; 55345 2 |
| CYTOTALFUNDRAISINGEXPENSEAMT | amount | 1.0K | 0 | 0 989; 6550 6; 80361 6; 335978 6 |
| PYOTHEREXPENSESAMT | amount | 1.1K | 0 | nan 873; 0 17; 134824 6; 176459 6 |
| CYOTHEREXPENSESAMT | amount | 2.0K | 0 | 0 14; 117492 10; 163925 10; 88887 10 |
| PYTOTALEXPENSESAMT | amount | 1.9K | 0 | nan 58; 0 22; 223708 10; 433404 10 |
| CYTOTALEXPENSESAMT | amount | 2.0K | 0 | 216074 10; 482876 10; 153520 10; 1701147 10 |
| PYREVENUESLESSEXPENSESAMT | amount | 1.9K | 0 | nan 54; 0 24; -33256 10; 6841 10 |
| CYREVENUESLESSEXPENSESAMT | amount | 1.9K | 0 | 0 12; 9812 10; 33976 10; 74788 10 |
| PROFESSIONALFUNDRAISINGIND | category | 2 | 0 | f 1.9K; t 92 |
| COMPENSATIONPROCESSCEOIND | category | 2 | 0 | t 1.0K; f 957 |
| COMPENSATIONPROCESSOTHERIND | category | 2 | 0 | f 1.3K; t 748 |
| INDIVRCVDGREATERTHAN100KCNT | category | 42 | 0 | 0 1.0K; nan 560; 1 226; 2 69 |
| CNTRCTRCVDGREATERTHAN100KCNT | category | 30 | 0 | 0 985; nan 818; 1 85; 2 28 |
| COMPCURRENTOFCRDIRECTORSGRP_TOTALAMT | amount | 1.1K | 0 | nan 695; 0 163; 30000 9; 75000 8 |
| COMPCURRENTOFCRDIRECTORSGRP_MANAGEMENTANDGENERALAMT | amount | 905 | 0 | nan 1.0K; 0 60; 4000 7; 75000 6 |
| TOTALFUNCTIONALEXPENSESGRP_TOTALAMT | amount | 2.0K | 0 | 216074 10; 482876 10; 153520 10; 1701147 10 |
| TOTALFUNCTIONALEXPENSESGRP_PROGRAMSERVICESAMT | amount | 1.9K | 0 | 0 68; nan 63; 185856 10; 439584 10 |
| TOTALFUNCTIONALEXPENSESGRP_MANAGEMENTANDGENERALAMT | amount | 1.7K | 0 | 0 219; nan 77; 23668 9; 43292 9 |
| TOTALFUNCTIONALEXPENSESGRP_FUNDRAISINGAMT | amount | 1.0K | 0 | 0 892; nan 97; 6550 6; 80361 6 |
| JOINTCOSTSIND | category | 2 | 0 | f 1.9K; t 96 |
| GRANTSTODOMESTICORGSGRP_TOTALAMT | amount | 394 | 0 | nan 1.3K; 0 265; 5000 5; 64633 3 |
| GRANTSTODOMESTICORGSGRP_PROGRAMSERVICESAMT | amount | 381 | 0 | nan 1.5K; 0 58; 5000 5; 500 3 |
| GRANTSTODOMESTICINDIVIDUALSGRP_TOTALAMT | amount | 317 | 0 | nan 1.4K; 0 290; 1000 5; 5000 4 |
| GRANTSTODOMESTICINDIVIDUALSGRP_PROGRAMSERVICESAMT | amount | 314 | 0 | nan 1.6K; 0 57; 1000 5; 5000 4 |
| FOREIGNGRANTSGRP_TOTALAMT | amount | 116 | 0 | nan 1.6K; 0 311; 1439383 1; 28698 1 |
| FOREIGNGRANTSGRP_PROGRAMSERVICESAMT | amount | 116 | 0 | nan 1.8K; 0 55; 1439383 1; 28698 1 |
| COMPCURRENTOFCRDIRECTORSGRP_PROGRAMSERVICESAMT | amount | 886 | 0 | nan 1.0K; 0 62; 40000 6; 30000 6 |
| COMPCURRENTOFCRDIRECTORSGRP_FUNDRAISINGAMT | amount | 581 | 0 | nan 1.3K; 0 132; 12000 5; 4000 4 |
| BUSINESSNAME2 | who | 149 | 0 | nan 1.8K; INC 17; FOUNDATION INC 8; ASSOCIATION 6 |
| TOTALJOINTCOSTSGRP_FUNDRAISINGAMT | amount | 12 | 0 | nan 2.0K; 922259 1; 5141 1; 271144 1 |
| TOTALJOINTCOSTSGRP_MANAGEMENTANDGENERALAMT | amount | 8 | 0 | nan 2.0K; 0 4; 11809 1; 44483 1 |
| TOTALJOINTCOSTSGRP_PROGRAMSERVICESAMT | amount | 12 | 0 | nan 2.0K; 2245721 1; 31955 1; 454182 1 |
| TOTALJOINTCOSTSGRP_TOTALAMT | amount | 13 | 0 | nan 2.0K; 0 8; 3167980 1; 48905 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:41:45.41524 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 38910d45-c6ee-492e-bc35-8 2.0K |
| SRC_SHA256 | who | 1 | 0 | fd33df8b55dd605fe7cfe369b 2.0K |
