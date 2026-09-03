# PORTAL_CKA_ISRAEL_NATIONAL_CB289C316E

rows 10.0K  columns 11  scan 3.5s

roles: audit 2, date 1, other 4, who 5

## when

INGESTED_AT
  2026     10.0K  ##############################

## who

REGION_NAME by rows
     10.0K  ירושלים 

STREET_NAME by rows
        15  השקד 
        14  הזית 
        14  האלה 
        13  הרימון 
        13  הגפן 
        12  התאנה 
        11  הערבה 
        10  האלון 
         9  החרוב 
         9  הברוש 
         9  האגוז 
         9  הדקל 
         9  האורן 
         9  רימון 
         8  התמר 
         7  הארז 
         7  אלון 
         7  גפן 
         7  ערבה 
         7  תאנה 

STREET_NAME_STATUS by rows
      3.9K  official 
        96  synonym of 9000 
        33  synonym of 4085 
        28  synonym of 101 
        28  synonym of 4066 
        26  synonym of 103 
        26  synonym of 102 
        24  synonym of 4159 
        24  synonym of 4034 
        24  synonym of 4002 
        24  synonym of 104 
        24  synonym of 4022 
        22  synonym of 116 
        22  synonym of 106 
        22  synonym of 4143 
        22  synonym of 108 
        22  synonym of 107 
        22  synonym of 110 
        20  synonym of 4129 
        19  synonym of 109 

CITY_NAME by rows
      7.4K  ירושלים 
       962  בית שמש 
       343  מבשרת ציון 
       138  צור הדסה 
       119  עין ראפה 
       118  אבו גוש 
       117  עין נקובא 
        88  נתיב הלה 
        73  קרית יערים 
        37  מבוא ביתר 
        36  נס הרים 
        36  אורה 
        34  מוצא עילית 
        31  שריגים )לי-און( 
        30  נווה אילן 
        29  לוזית 
        29  עמינדב 
        28  גבעות עדן 
        28  בית זית 
        24  כפר אוריה 

## who x when

REGION_NAME by INGESTED_AT  LOAD STAMP, not an event date
  ירושלים                                   2026:10.0K

STREET_NAME by INGESTED_AT  LOAD STAMP, not an event date
  אלון                                      2026:7
  גפן                                       2026:7
  האגוז                                     2026:9
  האורן                                     2026:9
  האלה                                      2026:14
  האלון                                     2026:10
  הארז                                      2026:7
  הברוש                                     2026:9
  הגפן                                      2026:13
  הדקל                                      2026:9
  הזית                                      2026:14
  החרוב                                     2026:9
  הערבה                                     2026:11
  הרימון                                    2026:13
  השקד                                      2026:15
  התאנה                                     2026:12
  התמר                                      2026:8
  ערבה                                      2026:7
  רימון                                     2026:9
  תאנה                                      2026:7

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| REGION_CODE | other | 1 | 0 | 11 10.0K |
| REGION_NAME | who | 1 | 0 | ירושלים  10.0K |
| CITY_CODE | other | 70 | 0 | 3000 7.4K; 2610 962; 1015 343; 1113 138 |
| CITY_NAME | who | 71 | 0 | ירושלים  7.4K; בית שמש  962; מבשרת ציון  343; צור הדסה  138 |
| STREET_CODE | other | 7.4K | 0 | 9000  69; 14403 50; 14402 50; 4494  50 |
| STREET_NAME | who | 8.9K | 0 | קהילת שומ  51; קהילת שום  51; קהילות שום  51; המשורר אצג  51 |
| STREET_NAME_STATUS | who | 1.8K | 0 | official  3.9K; synonym of 9000  96; synonym of 4085  54; synonym of 4066  49 |
| OFFICIAL_CODE | other | 2.5K | 0 | 9000 165; 4085 71; 4066 66; 4159 64 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:58:32.95647 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 2fae2b7c-df49-4733-a1d5-b 10.0K |
| SRC_SHA256 | who | 1 | 0 | 9f4a2adaf26cb55bb9208fb55 10.0K |
