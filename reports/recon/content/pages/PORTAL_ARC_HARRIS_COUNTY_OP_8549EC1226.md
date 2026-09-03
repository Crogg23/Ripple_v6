# PORTAL_ARC_HARRIS_COUNTY_OP_8549EC1226

rows 1.5K  columns 31  scan 3.7s

roles: amount 2, audit 2, category 8, date 3, id 4, other 8, who 5

## when

SOURCEDATE
  2021      1.5K  ##############################
  2022         1  

VAL_DATE
  2016       146  #####
  2018         2  
  2019        45  ##
  2020       798  ##############################
  2022       473  ##################

INGESTED_AT
  2026      1.5K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 1.5K | 29.52 | 29.80 | 30.12 | 30.15 | 43.7K |
| LONGITUDE | 1.5K | -95.95 | -95.46 | -94.96 | -94.93 | -139.7K |

## who

NAME by rows
         8  The Goddard School
         5  Alianza Eco International School
         5  Childtime Learning Centers
         5  La Petite Academy
         5  The Learning Experience
         3  Life Time Kids Camp
         3  Kidz Rocket
         3  Life Time Fitness Camps
         3  Montessori Country Day School
         2  Creative Corner
         2  Growing Scholars Montessori School
         2  Childrens Lighthouse Learning Center
         2  Land Of The Little People
         2  Attitude Respect N Manners Learning Center
         2  Kids In Kare
         2  Kiddies Excel Academy
         2  Montessori Learning Institute
         2  Americas Choice Children Center
         2  Precious Moments Learning Center
         2  Texas Kids Learning Center

NAME by dollars
      239.39        8 rows  The Goddard School
      149.73        5 rows  La Petite Academy
      149.61        5 rows  Childtime Learning Centers
      149.51        5 rows  The Learning Experience
      149.13        5 rows  Alianza Eco International School
       89.73        3 rows  Life Time Fitness Camps
       89.21        3 rows  Life Time Kids Camp
       89.19        3 rows  Montessori Country Day School
       89.14        3 rows  Kidz Rocket
       60.22        2 rows  Spanish Schoolhouse
       60.07        2 rows  Kids R Kids
          60        2 rows  True Love Childcare
       59.93        2 rows  Childrens Lighthouse Learning Center
       59.89        2 rows  Little Laughter's Childcare Center
       59.87        2 rows  Growing Scholars Montessori School
       59.80        2 rows  Whiz Children's Academy
       59.75        2 rows  School For Little Children
       59.74        2 rows  Precious Moments Learning Center
       59.73        2 rows  Texas Kids Learning Center
       59.70        2 rows  Creative Corner

WEBSITE by rows
      1.5K  Not Available

WEBSITE by dollars
       43.7K     1.5K rows  Not Available

ZIP4 by rows
      1.5K  Not Available

ZIP4 by dollars
       43.7K     1.5K rows  Not Available

COUNTY by rows
      1.5K  Harris

COUNTY by dollars
       43.7K     1.5K rows  Harris

## who x when

NAME by VAL_DATE, dollars = LATITUDE
  Alianza Eco International School          2020:89.58 2022:59.55
  Americas Choice Children Center           2020:59.40
  Attitude Respect N Manners Learning Cent  2016:59.40
  Childrens Lighthouse Learning Center      2020:59.93
  Childtime Learning Centers                2016:30.06 2020:119.55
  Creative Corner                           2016:59.70
  Growing Scholars Montessori School        2020:59.87
  Kiddies Excel Academy                     2016:29.67 2020:29.73
  Kids In Kare                              2020:59.51
  Kids R Kids                               2016:30.01 2020:30.06
  Kidz Rocket                               2016:29.73 2020:59.41
  La Petite Academy                         2016:29.95 2020:119.78
  Land Of The Little People                 2020:29.65 2022:29.66
  Life Time Fitness Camps                   2020:89.73
  Life Time Kids Camp                       2019:29.55 2020:29.93 2022:29.73
  Little Laughter's Childcare Center        2020:59.89
  Montessori Country Day School             2020:89.19
  Montessori Learning Institute             2016:29.69 2020:29.69
  Precious Moments Learning Center          2020:59.74
  School For Little Children                2022:59.75
  Spanish Schoolhouse                       2020:60.22
  Texas Kids Learning Center                2020:59.73
  The Goddard School                        2016:30.07 2020:209.32
  The Learning Experience                   2020:119.63 2022:29.88
  True Love Childcare                       2020:60
  Whiz Children's Academy                   2020:59.80

WEBSITE by VAL_DATE, dollars = LATITUDE
  Not Available                             2016:4.4K 2018:59.37 2019:1.3K 2020:23.8K 2022:14.1K

## what

CITY: Houston 66%, Spring 6%, Katy 6%, Humble 5%, Cypress 4%, Pasadena 3%, Tomball 3%, Baytown 2%, Kingwood 2%, Deer Park 1%, La Porte 1%, Webster 1%

TYPE: Center Based 63%, School Based 27%, Religious Facility 5%, Head Start 4%

NAICS_DESC: Child Day Care Centers 87%, Child Day Care, Before Or Afte 9%, Head Start Programs, Separate  4%

SOURCE: http://www.dfps.state.tx.us/ch 100%, https://dhs.arkansas.gov/dccec 0%

VAL_METHOD: Imagery/other 79%, Imagery 12%, Geocode 8%, Unverified 1%

ST_SUBTYPE: Licensed Center - Child Care P 85%, Licensed Center - School Age P 9%, Licensed Center - Before/after 6%, Small Employer Based Child Car 0%, Child Care Center 0%

PCT: 3 30%, 4 26%, 1 25%, 2 19%

UNINCORP: No 57%, Yes 43%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 1.5K | 0 | 119838 8; 119837 8; 119831 8; 119826 8 |
| ID | id | 1.5K | 0 | 0266177375 8; 1222358461 8; 1222358459 8; 1222281676 8 |
| NAME | who | 1.4K | 0 | The Goddard School 14; The Learning Experience 11; Zion Lutheran School And  8; Zion Lutheran Early Child 8 |
| ADDRESS | id | 1.5K | 0 | 907 Hicks St 8; 5050 E Sam Houston Pkwy S 8; 12750 Kimberley Ln 8; 23221 Aldine Westfield Rd 8 |
| CITY | category | 29 | 0 | Houston 931; Spring 87; Katy 83; Humble 74 |
| STATE | other | 1 | 0 | TX 1.5K |
| ZIP | other | 134 | 0 | 77084 37; 77449 35; 77346 33; 77429 32 |
| ZIP4 | who | 1 | 0 | Not Available 1.5K |
| TELEPHONE | other | 1.3K | 0 | (281) 360-2500 30; (281) 468-8013 18; (281) 392-5055 15; (281) 495-9100 10 |
| TYPE | category | 4 | 0 | Center Based 926; School Based 396; Religious Facility 80; Head Start 62 |
| STATUS | other | 1 | 0 | Open 1.5K |
| POPULATION | other | 291 | 0 | 60 67; 100 48; 102 40; 85 40 |
| COUNTY | who | 1 | 0 | Harris 1.5K |
| COUNTYFIPS | other | 1 | 0 | 48201 1.5K |
| COUNTRY | other | 1 | 0 | USA 1.5K |
| LATITUDE | amount | 1.4K | 0 | 30.09736 8; 29.635408 8; 29.7757 8; 30.04925 8 |
| LONGITUDE | amount | 1.4K | 0 | -95.62532 8; -95.165992 8; -95.559791 8; -95.38864 8 |
| NAICS_CODE | other | 1 | 0 | 624410 1.5K |
| NAICS_DESC | category | 3 | 0 | Child Day Care Centers 1.3K; Child Day Care, Before Or 129; Head Start Programs, Sepa 63 |
| SOURCE | category | 2 | 0 | http://www.dfps.state.tx. 1.5K; https://dhs.arkansas.gov/ 1 |
| SOURCEDATE | date | 2 | 0 | 1633582800000 1.5K; 1650258000000 1 |
| VAL_METHOD | category | 4 | 0 | Imagery/other 1.2K; Imagery 175; Geocode 122; Unverified 8 |
| VAL_DATE | date | 60 | 0 | 1654146000000 473; 1585717200000 75; 1589259600000 73; 1586840400000 54 |
| WEBSITE | who | 1 | 0 | Not Available 1.5K |
| ST_SUBTYPE | category | 5 | 0 | Licensed Center - Child C 1.2K; Licensed Center - School  129; Licensed Center - Before/ 90; Small Employer Based Chil 2 |
| PCT | category | 4 | 0 | 3 433; 4 386; 1 365; 2 280 |
| UNINCORP | category | 2 | 0 | No 830; Yes 634 |
| GEOMETRY | id | 1.4K | 0 | {"type": "Point", "coordi 8; {"type": "Point", "coordi 8; {"type": "Point", "coordi 8; {"type": "Point", "coordi 8 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:31:02.37905 1.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 1c828d68-645e-41be-99de-7 1.5K |
| SRC_SHA256 | who | 1 | 0 | a3bf829672143caf64b1ffc66 1.5K |
