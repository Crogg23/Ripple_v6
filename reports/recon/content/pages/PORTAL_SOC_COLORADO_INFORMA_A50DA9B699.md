# PORTAL_SOC_COLORADO_INFORMA_A50DA9B699

rows 2.0K  columns 20  scan 4.1s

roles: amount 2, audit 2, category 7, date 1, id 1, other 5, who 3

## when

INGESTED_AT
  2026      2.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTALEMPLOYEECNT | 2.0K | 0 | 4 | 822 | 38.0K | 165.5K |
| TOTALVOLUNTEERSCNT | 1.7K | 0 | 22 | 1.9K | 30.0K | 243.7K |

## who

BUSINESSNAME1 by rows
         5  REAL LIFE MINISTRIES
         4  ASPEN COMMUNITY FOUNDATION
         4  Rocky Mountain Health Care Services
         4  Thornton Junior Football League
         4  ROCKY MOUNTAIN MULTIPLE SCLEROSIS CENTER
         4  RONALD MCDONALD HOUSE CHARITIES OF
         4  ARAPAHOE COUNTY BAR ASSOCIATION
         4  SHINING STARS BASKETBALL INC
         4  BANDIMERE FAMILY FOUNDATION
         4  BAL SWAN CHILDREN'S CENTER
         4  Winter Park Horseman's Association
         4  CREDIT UNIONS CHARTERED IN THE STATE OF COLORADO
         4  BRIDGES CHILD PLACEMENT AGENCY
         4  COMMUNITY UPLIFT MINISTRIES
         4  SUMMER SCHOLARS
         4  COLORADO ALLIANCE OF RESEARCH LIBRARIES
         4  ALMOST HOME INC
         4  HABITAT FOR HUMANITY INTERNATIONAL INC
         4  THE DENVER STREET SCHOOL
         4  BethHaven Incorporated

BUSINESSNAME1 by dollars
       38.0K        1 rows  BANNER HEALTH
       23.5K        3 rows  COLORADO SEMINARY
       13.7K        2 rows  KAISER FOUNDATION HEALTH PLAN OF COLORADO
        7.0K        3 rows  PARKVIEW HEALTH SYSTEM INC
        3.8K        1 rows  Community Development Institute
        3.5K        1 rows  PARKVIEW MEDICAL CENTER INC
        2.4K        3 rows  SIMPSON UNIVERSITY
        2.1K        1 rows  Centura Health Corporation
        2.0K        1 rows  GOODWILL INDUSTRIES OF DENVER
        1.9K        3 rows  WIND CREST INC
        1.9K        3 rows  PLAN DE SALUD DEL VALLE INC
        1.8K        3 rows  CROWN COLLEGE
        1.8K        3 rows  MESA DEVELOPMENTAL SERVICES
        1.6K        2 rows  DEVELOPMENTAL DISABILITIES CENTER
        1.6K        2 rows  HILLTOP HEALTH SERVICES CORPORATION
        1.6K        2 rows  NORTH METRO COMMUNITY SERVICES
        1.5K        4 rows  SUMMER SCHOLARS
        1.3K        2 rows  CLASSICAL ACADEMY
        1.2K        1 rows  Doane College
        1.2K        2 rows  Fellowship of Catholic University Students

BUSINESSNAME2 by rows
      1.8K  nan
        12  INC
         4  FOUNDATION INC
         4  DBA ALMOST HOME SHELTER COALITION
         4  HABITAT FOR HUMANITY OF GUNNISON VALLEY
         4  CENTER
         4  RESEARCH
         4  DEVELOPMENT CORPORATION
         3  BARRISTERS INC
         3  Education in Colorado Springs
         3  FOUNDATION
         3  STUDY OF LUNG CANCER
         3  UNITED STATES
         3  PEDIATRICS INC
         3  C/O TOBIN RUPAREL KONCZAK & MUNDELL PC
         3  Community Council Inc
         3  SOCIETY OF CPAS
         3  C/O ALPHA CHI OMEGA NATL HOUSING CORP
         3  Colorado Springs/Pikes Peak Region
         3  EDUCATION

BUSINESSNAME2 by dollars
      154.3K     1.8K rows  nan
        3.8K        1 rows  Head Start
        1.9K       12 rows  INC
         457        2 rows  SERVICES
         415        1 rows  COLORADO INC
         362        3 rows  PEDIATRICS INC
         334        3 rows  Education in Colorado Springs
         277        2 rows  D/B/A OPPORTUNITY INTERNATIONAL-US
         276        2 rows  VALLEY INC
         252        1 rows  C/O PURCHASE COLLEGE SUNY
         220        1 rows  HUMANITIES
         216        1 rows  PALLIATIVE CARE
         209        4 rows  CENTER
         205        1 rows  at Colorado Christian Home
         191        1 rows  D/B/A COLORADO HEIGHTS UNIVERSITY
         145        2 rows  INTERCULTURAL LEARNING
         119        4 rows  DEVELOPMENT CORPORATION
          85        2 rows  CHILDREN
          74        1 rows  Care
          72        1 rows  STANDARDS INC

SRC_SHA256 by rows
      2.0K  47e296c52e7aeed63624ed529cee756e3940a28d2d83d897a0e8f124ab0a86fe

SRC_SHA256 by dollars
      165.5K     2.0K rows  47e296c52e7aeed63624ed529cee756e3940a28d2d83d897a0e8f124ab0a

## who x when

BUSINESSNAME1 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTALEMPLOYEECNT
  ALMOST HOME INC                           2026:29
  ARAPAHOE COUNTY BAR ASSOCIATION           2026:4
  ASPEN COMMUNITY FOUNDATION                2026:45
  BAL SWAN CHILDREN'S CENTER                2026:325
  BANDIMERE FAMILY FOUNDATION               2026:0
  BANNER HEALTH                             2026:38.0K
  BRIDGES CHILD PLACEMENT AGENCY            2026:26
  BethHaven Incorporated                    2026:102
  COLORADO ALLIANCE OF RESEARCH LIBRARIES   2026:38
  COLORADO SEMINARY                         2026:23.5K
  COMMUNITY UPLIFT MINISTRIES               2026:7
  CREDIT UNIONS CHARTERED IN THE STATE OF   2026:44
  Centura Health Corporation                2026:2.1K
  Community Development Institute           2026:3.8K
  GOODWILL INDUSTRIES OF DENVER             2026:2.0K
  HABITAT FOR HUMANITY INTERNATIONAL INC    2026:4
  KAISER FOUNDATION HEALTH PLAN OF COLORAD  2026:13.7K
  PARKVIEW HEALTH SYSTEM INC                2026:7.0K
  PARKVIEW MEDICAL CENTER INC               2026:3.5K
  REAL LIFE MINISTRIES                      2026:10
  ROCKY MOUNTAIN MULTIPLE SCLEROSIS CENTER  2026:132
  RONALD MCDONALD HOUSE CHARITIES OF        2026:60
  Rocky Mountain Health Care Services       2026:1.0K
  SHINING STARS BASKETBALL INC              2026:0
  SIMPSON UNIVERSITY                        2026:2.4K
  SUMMER SCHOLARS                           2026:1.5K
  THE DENVER STREET SCHOOL                  2026:112
  Thornton Junior Football League           2026:0
  WIND CREST INC                            2026:1.9K
  Winter Park Horseman's Association        2026:0

BUSINESSNAME2 by INGESTED_AT  LOAD STAMP, not an event date, dollars = TOTALEMPLOYEECNT
  BARRISTERS INC                            2026:8
  C/O ALPHA CHI OMEGA NATL HOUSING CORP     2026:0
  C/O PURCHASE COLLEGE SUNY                 2026:252
  C/O TOBIN RUPAREL KONCZAK & MUNDELL PC    2026:0
  CENTER                                    2026:209
  COLORADO INC                              2026:415
  Colorado Springs/Pikes Peak Region        2026:47
  Community Council Inc                     2026:0
  D/B/A COLORADO HEIGHTS UNIVERSITY         2026:191
  D/B/A OPPORTUNITY INTERNATIONAL-US        2026:277
  DBA ALMOST HOME SHELTER COALITION         2026:29
  DEVELOPMENT CORPORATION                   2026:119
  EDUCATION                                 2026:30
  Education in Colorado Springs             2026:334
  FOUNDATION                                2026:59
  FOUNDATION INC                            2026:7
  HABITAT FOR HUMANITY OF GUNNISON VALLEY   2026:4
  HUMANITIES                                2026:220
  Head Start                                2026:3.8K
  INC                                       2026:1.9K
  PALLIATIVE CARE                           2026:216
  PEDIATRICS INC                            2026:362
  RESEARCH                                  2026:29
  SERVICES                                  2026:457
  SOCIETY OF CPAS                           2026:0
  STUDY OF LUNG CANCER                      2026:38
  UNITED STATES                             2026:45
  VALLEY INC                                2026:276
  at Colorado Christian Home                2026:205
  nan                                       2026:154.3K

## what

TAXYR: 2013 30%, 2011 24%, 2016 12%, 2012 11%, 2015 8%, 2014 8%, 2010 6%, 2017 1%, 2009 1%

TYPEOFORGANIZATIONCORPIND: t 94%, f 6%

TYPEOFORGANIZATIONTRUSTIND: f 99%, t 1%

TYPEOFORGANIZATIONASSOCIND: f 98%, t 2%

TYPEOFORGANIZATIONOTHERIND: f 99%, t 1%

LEGALDOMICILESTATECD: CO 94%, nan 2%, DC 1%, TX 1%, CA 1%, MA 0%, VA 0%, NE 0%, PA 0%, MD 0%, WA 0%, NY 0%

OTHERORGANIZATIONDSC: nan 99%, FOUNDATION 0%, ENDOWMENT 0%, PUBLIC FOUNDATION 0%, Foundation 0%, Non-Profit 0%, PERSONAL SER 0%, Non-P 0%, Non-Profit Labor Union 0%, 501C 0%, 501(3)(c) 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 2.0K | 0 | 201340579349300009 10; 201332919349301113 10; 201320299349300022 10; 201612679349300221 10 |
| TAXYR | category | 9 | 0 | 2013 597; 2011 476; 2016 230; 2012 229 |
| BUSINESSNAME1 | who | 1.3K | 0 | BELLA NATURAL WOMEN'S CAR 11; IMAGINE HOUSING CORP II 11; MUSIC IN THE MOUNTAINS IN 11; POUDRE SCHOOL DISTRICT FO 11 |
| EIN | other | 1.2K | 0 | 462578248 11; 263619775 11; 742550850 11; 841555092 11 |
| VOTINGMEMBERSGOVERNINGBODYCNT | other | 76 | 0 | 5 177; 10 175; 9 171; 7 161 |
| VOTINGMEMBERSINDEPENDENTCNT | other | 77 | 0 | 0 182; 5 154; 7 146; 10 146 |
| TOTALEMPLOYEECNT | amount | 232 | 0 | 0 640; 1 107; 2 107; 3 96 |
| TOTALVOLUNTEERSCNT | amount | 274 | 0 | 0 371; nan 320; 100 66; 20 66 |
| ACTIVITYORMISSIONDESC | other | 1.4K | 0 | STATE CHARTERED CREDIT UN 13; SEE SCHEDULE O 11; LOW INCOME HOUSING FOR PE 11; UNITE COMMUNITY RESOURCES 11 |
| TYPEOFORGANIZATIONCORPIND | category | 2 | 0 | t 1.9K; f 127 |
| TYPEOFORGANIZATIONTRUSTIND | category | 2 | 0 | f 2.0K; t 18 |
| TYPEOFORGANIZATIONASSOCIND | category | 2 | 0 | f 2.0K; t 48 |
| TYPEOFORGANIZATIONOTHERIND | category | 2 | 0 | f 2.0K; t 22 |
| FORMATIONYR | other | 113 | 0 | 2004 78; 2005 62; 2002 60; nan 60 |
| LEGALDOMICILESTATECD | category | 29 | 0 | CO 1.8K; nan 47; DC 13; TX 10 |
| BUSINESSNAME2 | who | 147 | 0 | nan 1.8K; INC 12; DEVELOPMENT CORPORATION 4; RESEARCH 4 |
| OTHERORGANIZATIONDSC | category | 11 | 0 | nan 2.0K; FOUNDATION 2; ENDOWMENT 2; PUBLIC FOUNDATION 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 04:43:18.44787 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 4a985968-7b5e-4689-a2cc-8 2.0K |
| SRC_SHA256 | who | 1 | 0 | 47e296c52e7aeed63624ed529 2.0K |
