# PORTAL_ARC_TUCSON_OPEN_DATA_55D5164315

rows 60  columns 36  scan 3.5s

roles: amount 1, audit 2, category 11, date 1, other 17, who 5

## when

INGESTED_AT
  2026        60  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| SCHOOLS_DISTANCE | 60 | 0.93 | 9.61 | 17.90 | 18.64 | 580.20 |

## who

SCHOOLS_NAME by rows
         1  Cottonwood Elementary School
         1  Borman Elementary School
         1  Dunham Elementary School
         1  Sunrise Drive Elementary School
         1  Copper View Elementary School
         1  Math and Science Success Academy
         1  Mesquite Elementary School
         1  Painted Sky Elementary School
         1  Ironwood Elementary School
         1  Centennial Elementary School
         1  Winifred Harelson Elementary School
         1  Academy Of Tucson Middle School
         1  BASIS Oro Valley Primary
         1  Desert Willow Elementary School
         1  BASIS Tucson North
         1  BASIS Tucson Primary
         1  Fruchthendler Elementary School
         1  Ida Flood Dodge Traditional Middle Magnet School
         1  BASIS Oro Valley
         1  Emily Gray Junior High School

SCHOOLS_NAME by dollars
       18.64        1 rows  Copper View Elementary School
       17.39        1 rows  Acacia Elementary School
       17.23        1 rows  Old Vail Middle School
       16.83        1 rows  Ocotillo Ridge Elementary School
       16.50        1 rows  Cienega High School
       16.02        1 rows  Twin Peaks Elementary School
       15.68        1 rows  The Innovation Academy
       14.97        1 rows  Painted Sky Elementary School
       14.68        1 rows  Leman Academy Of Excellence-Oro Valley Arizona
       14.61        1 rows  Richard B Wilson Jr School
       13.96        1 rows  Esmond Station School
       13.25        1 rows  Empire High School
       13.19        1 rows  Leman Academy of Excellence
       13.01        1 rows  BASIS Oro Valley
       13.01        1 rows  BASIS Oro Valley Primary
       12.63        1 rows  Ironwood Elementary School
       12.25        1 rows  Cottonwood Elementary School
       11.87        1 rows  Tanque Verde Elementary School
       11.71        1 rows  Legacy Traditional School - Northwest Tucson
       11.65        1 rows  Hermosa Montessori Charter School

SCHOOLS_COUNTY by rows
        60  Pima County

SCHOOLS_COUNTY by dollars
      580.20       60 rows  Pima County

SCHOOLS_RATING_DESCRIPTION by rows
        60  The GreatSchools Rating helps parents compare schools within a state b

SCHOOLS_RATING_DESCRIPTION by dollars
      580.20       60 rows  The GreatSchools Rating helps parents compare schools within

SCHOOL_RATING_TEXT by rows
        60  Above Average

SCHOOL_RATING_TEXT by dollars
      580.20       60 rows  Above Average

## who x when

SCHOOLS_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCHOOLS_DISTANCE
  Acacia Elementary School                  2026:17.39
  Academy Of Tucson Middle School           2026:5.39
  BASIS Oro Valley                          2026:13.01
  BASIS Oro Valley Primary                  2026:13.01
  BASIS Tucson North                        2026:4.79
  BASIS Tucson Primary                      2026:1.28
  Borman Elementary School                  2026:4.34
  Centennial Elementary School              2026:6.87
  Cienega High School                       2026:16.50
  Copper View Elementary School             2026:18.64
  Cottonwood Elementary School              2026:12.25
  Desert Willow Elementary School           2026:11.32
  Dunham Elementary School                  2026:8.57
  Emily Gray Junior High School             2026:10.25
  Empire High School                        2026:13.25
  Esmond Station School                     2026:13.96
  Fruchthendler Elementary School           2026:6.34
  Ida Flood Dodge Traditional Middle Magne  2026:3.77
  Ironwood Elementary School                2026:12.63
  Leman Academy Of Excellence-Oro Valley A  2026:14.68
  Math and Science Success Academy          2026:6.81
  Mesquite Elementary School                2026:10.79
  Ocotillo Ridge Elementary School          2026:16.83
  Old Vail Middle School                    2026:17.23
  Painted Sky Elementary School             2026:14.97
  Richard B Wilson Jr School                2026:14.61
  Sunrise Drive Elementary School           2026:6.74
  The Innovation Academy                    2026:15.68
  Twin Peaks Elementary School              2026:16.02
  Winifred Harelson Elementary School       2026:9.17

SCHOOLS_COUNTY by INGESTED_AT  LOAD STAMP, not an event date, dollars = SCHOOLS_DISTANCE
  Pima County                               2026:580.20

## what

SCHOOLS_TYPE: public 70%, charter 30%

SCHOOLS_LEVEL_CODES: e 25%, p,e 18%, m 12%, e,m 12%, e,m,h 12%, h 10%, p,e,m 8%, m,h 3%

SCHOOLS_LEVEL: 9,10,11,12 12%, KG,1,2,3,4,5 12%, 6,7,8 10%, PK,KG,1,2,3,4,5,UG 10%, KG,1,2,3,4,5,6,7,8 10%, PK,KG,1,2,3,4,5 8%, KG,1,2,3,4,5,6,UG 8%, PK,KG,1,2,3,4,5,6,7,8,UG 6%, KG,1,2,3,4,5,6 6%, KG,1,2,3,4,5,6,7,8,9,10,11,12 6%, KG,1,2,3,4,5,UG 4%, PK,KG,1,2,3,4,5,6,7,8 4%

SCHOOLS_CITY: Tucson 82%, Oro Valley 10%, Vail 7%, Sahuarita 2%

SCHOOLS_ZIP: 85747 20%, 85749 11%, 85750 11%, 85641 9%, 85718 9%, 85755 7%, 85742 7%, 85741 7%, 85748 7%, 85719 7%, 85743 4%, 85737 4%

SCHOOLS_PHONE: (520) 879-2000 25%, (520) 225-6060 16%, (520) 209-7500 14%, (520) 696-5000 10%, (520) 749-5751 6%, (520) 696-8801 6%, (520) 733-0096 6%, (520) 682-4749 4%, (520) 222-8253 4%, (520) 293-2676 4%, (520) 326-3444 4%, (520) 625-3502 2%

SCHOOLS_FAX: (520) 625-4609 9%, (520) 762-9849 9%, (520) 879-2401 9%, (520) 879-3601 9%, (520) 762-2801 9%, (520) 579-4785 9%, (520) 696-3888 9%, (520) 696-5900 9%, (520) 308-5078 9%, (520) 579-5164 9%, (520) 762-2601 9%

SCHOOLS_DISTRICT_NAME: Vail Unified District 27%, Tucson Unified District 16%, Catalina Foothills Unified Dis 14%, Amphitheater Unified District 10%, Tanque Verde Unified District 6%, Flowing Wells Unified District 6%, Academy Of Tucson  Inc. 6%, Marana Unified District 4%, Leman Academy of Excellence IN 4%, Sahuarita Unified District 2%, Basis Charter Schools INC. (92 2%, Basis Charter Schools INC. (90 2%

SCHOOLS_DISTRICT_ID: 1847 27%, 1834 16%, 1582 14%, 1548 10%, 1823 6%, 1643 6%, 1524 6%, 1709 4%, 2804 4%, 1798 2%, 2767 2%, 2579 2%

SCHOOLS_RATING: 7 43%, 8 27%, 9 22%, 10 8%

SCHOOLS_RATING_NUM: 7 43%, 8 27%, 9 22%, 10 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OID | other | 60 | 0 | 458 1; 445 1; 444 1; 442 1 |
| SCHOOLS_UNIVERSAL_ID | other | 59 | 0 | 0405775 1; 0401520 1; 0401739 1; 0403647 1 |
| SCHOOLS_NCES_ID | other | 59 | 0 | 040730003339 1; 040885001510 1; 040885000909 1; 040885002765 1 |
| SCHOOLS_STATE_ID | other | 60 | 0 | 91338 1; 91168 1; 05850 1; 89575 1 |
| SCHOOLS_NAME | who | 59 | 0 | Copper View Elementary Sc 1; Acacia Elementary School 1; Old Vail Middle School 1; Ocotillo Ridge Elementary 1 |
| SCHOOLS_SCHOOL_SUMMARY | other | 60 | 0 | Copper View Elementary Sc 1; Acacia Elementary School, 1; Old Vail Middle School, a 1; Ocotillo Ridge Elementary 1 |
| SCHOOLS_TYPE | category | 2 | 0 | public 42; charter 18 |
| SCHOOLS_LEVEL_CODES | category | 8 | 0 | e 15; p,e 11; m 7; e,m 7 |
| SCHOOLS_LEVEL | category | 21 | 0 | 9,10,11,12 6; KG,1,2,3,4,5 6; 6,7,8 5; PK,KG,1,2,3,4,5,UG 5 |
| SCHOOLS_STREET | other | 58 | 0 | 11155 North Oracle Road 2; 16200 South Starlight Vie 1; 12955 East Colossal Cave  1; 13299 East Colossal Cave  1 |
| SCHOOLS_CITY | category | 4 | 0 | Tucson 49; Oro Valley 6; Vail 4; Sahuarita 1 |
| SCHOOLS_STATE | other | 1 | 0 | AZ 60 |
| SCHOOLS_FIPSCOUNTY | other | 1 | 0 | 4019 60 |
| SCHOOLS_ZIP | category | 22 | 0 | 85747 9; 85749 5; 85750 5; 85641 4 |
| SCHOOLS_PHONE | category | 21 | 0 | (520) 879-2000 13; (520) 225-6060 8; (520) 209-7500 7; (520) 696-5000 5 |
| SCHOOLS_FAX | category | 50 | 9 | (520) 625-4609 1; (520) 762-9849 1; (520) 879-2401 1; (520) 879-3601 1 |
| SCHOOLS_COUNTY | who | 1 | 0 | Pima County 60 |
| SCHOOLS_LAT | other | 58 | 0 | 32.409412 2; 31.955441 1; 32.042191 1; 32.050533 1 |
| SCHOOLS_LON | other | 58 | 0 | -110.944611 2; -110.976936 1; -110.718185 1; -110.712334 1 |
| SCHOOLS_DISTRICT_NAME | category | 23 | 0 | Vail Unified District 13; Tucson Unified District 8; Catalina Foothills Unifie 7; Amphitheater Unified Dist 5 |
| SCHOOLS_DISTRICT_ID | category | 23 | 0 | 1847 13; 1834 8; 1582 7; 1548 5 |
| SCHOOLS_WEB_SITE | other | 53 | 5 | http://www.vail.k12.az.us 3; http://www.amphi.com 2; http://www.susd30.us/ 1; http://aca.vail.k12.az.us 1 |
| SCHOOLS_OVERVIEW_URL | other | 60 | 0 | https://www.greatschools. 1; https://www.greatschools. 1; https://www.greatschools. 1; https://www.greatschools. 1 |
| SCHOOLS_RATING | category | 4 | 0 | 7 26; 8 16; 9 13; 10 5 |
| SCHOOLS_YEAR | other | 1 | 0 | 2020 60 |
| SCHOOLS_RATING_DESCRIPTION | who | 1 | 0 | The GreatSchools Rating h 60 |
| SCHOOLS_DISTANCE | amount | 59 | 0 | 13.007677060161308 2; 18.63734947245455 1; 17.392697006226154 1; 17.233180682764363 1 |
| DDLAT | other | 58 | 0 | 32.409412 2; 31.955441 1; 32.042191 1; 32.050533 1 |
| DDLON | other | 58 | 0 | -110.944611 2; -110.976936 1; -110.718185 1; -110.712334 1 |
| ORIG_OID | other | 60 | 0 | 458 1; 445 1; 444 1; 442 1 |
| SCHOOLS_RATING_NUM | category | 4 | 0 | 7 26; 8 16; 9 13; 10 5 |
| SCHOOL_RATING_TEXT | who | 1 | 0 | Above Average 60 |
| GEOMETRY | other | 59 | 0 | {"type": "Point", "coordi 2; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:17:55.89252 60 |
| SOURCE_RUN_ID | audit | 1 | 0 | 0ad34535-9bff-4258-adab-a 60 |
| SRC_SHA256 | who | 1 | 0 | e1af64077ca5f4b2f35bed051 60 |
