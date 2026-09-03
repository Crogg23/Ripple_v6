# PORTAL_CKA_WESTERN_PENNSYLV_8863985427

rows 277  columns 25  scan 3.3s

roles: amount 2, audit 2, category 7, date 1, empty 1, other 11, who 2

## when

INGESTED_AT
  2026       277  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 277 | 39.86 | 40.43 | 41.37 | 41.63 | 11.2K |
| LONGITUDE | 277 | -80.75 | -79.93 | -78.21 | -77.23 | -22.1K |

## who

VENUE_NAME by rows
         2  Pizzaiolo Primo
         2  Jackson's Restaurant and Bar
         1  St. Michael, Greenville - at Knights of Columbus
         1  Our Lady of Lourdes Altoona
         1  St. Vincent de Paul and St. Vitus (Holy Spirit Parish) Fish Fry, New C
         1  Fire Department of North Versailles at the South Wilmerding Social Clu
         1  Saint Joseph School, Holy Family Parish
         1  Mahoning Township VFD
         1  Skyview VFC
         1  Trough Creek Valley VFD
         1  St. Mary of the Assumption Marian Hall, Our Lady of Perpetual Help Par
         1  St. Therese of the Child Jesus Parish
         1  A.W. Beattie Career Center Restaurant
         1  North Irwin Volunteer Fire Department
         1  St. Catherine of Siena Social Hall, St. Teresa of Kolkata Parish
         1  Coleman's Fish Market
         1  Pittsburgh Sandwich Society
         1  Immaculate Heart of Mary
         1  Walnut Grill - Wexford
         1  Mary, Queen of Peace Parish

VENUE_NAME by dollars
       80.97        2 rows  Jackson's Restaurant and Bar
       80.80        2 rows  Pizzaiolo Primo
       41.63        1 rows  The Epiphany of the Lord Parish
       41.43        1 rows  Utica Volunteer Fire Department
       41.39        1 rows  St. Michael, Greenville - at Knights of Columbus
       41.36        1 rows  St. Boniface
       41.31        1 rows  St. Joseph Parish
       41.22        1 rows  St. Anthony Parish
       41.15        1 rows  Church of the Beloved Disciple/Grove City Knights of Columbu
       41.06        1 rows  St. Peter Church, St. Faustina Parish
       41.06        1 rows  Slippery Rock Fire Rescue
       41.01        1 rows  St. Louis Church, St. Faustina Parish 
       41.01        1 rows  Mahoning Township VFD
          41        1 rows  American Legion Post 343
       40.99        1 rows  St. Vincent de Paul and St. Vitus (Holy Spirit Parish) Fish 
       40.86        1 rows  Holy Redeemer, Ellwood City
       40.85        1 rows  All Saints Parish at St. Conrad Church
       40.83        1 rows  St. Mary (Herman) - St. Francis of Assisi Parish
       40.82        1 rows  First United Methodist Church Covenant Center
       40.82        1 rows  St. Mary Our Lady of Guadalupe Parish

SRC_SHA256 by rows
       277  9e207448fa0e2b0e1ca3336848061549f5832745e29e2953b7adcb45563b2e8a

SRC_SHA256 by dollars
       11.2K      277 rows  9e207448fa0e2b0e1ca3336848061549f5832745e29e2953b7adcb45563b

## who x when

VENUE_NAME by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  A.W. Beattie Career Center Restaurant     2026:40.58
  American Legion Post 343                  2026:41
  Church of the Beloved Disciple/Grove Cit  2026:41.15
  Coleman's Fish Market                     2026:40.06
  Fire Department of North Versailles at t  2026:40.39
  Immaculate Heart of Mary                  2026:40.46
  Jackson's Restaurant and Bar              2026:80.97
  Mahoning Township VFD                     2026:41.01
  Mary, Queen of Peace Parish               2026:40.43
  North Irwin Volunteer Fire Department     2026:40.34
  Our Lady of Lourdes Altoona               2026:40.50
  Pittsburgh Sandwich Society               2026:40.48
  Pizzaiolo Primo                           2026:80.80
  Saint Joseph School, Holy Family Parish   2026:40.51
  Skyview VFC                               2026:40.36
  Slippery Rock Fire Rescue                 2026:41.06
  St. Anthony Parish                        2026:41.22
  St. Boniface                              2026:41.36
  St. Catherine of Siena Social Hall, St.   2026:40.41
  St. Joseph Parish                         2026:41.31
  St. Louis Church, St. Faustina Parish     2026:41.01
  St. Mary of the Assumption Marian Hall,   2026:40.56
  St. Michael, Greenville - at Knights of   2026:41.39
  St. Peter Church, St. Faustina Parish     2026:41.06
  St. Therese of the Child Jesus Parish     2026:40.53
  St. Vincent de Paul and St. Vitus (Holy   2026:40.99
  The Epiphany of the Lord Parish           2026:41.63
  Trough Creek Valley VFD                   2026:40.29
  Utica Volunteer Fire Department           2026:41.43
  Walnut Grill - Wexford                    2026:40.64

SRC_SHA256 by INGESTED_AT  LOAD STAMP, not an event date, dollars = LATITUDE
  9e207448fa0e2b0e1ca3336848061549f5832745  2026:11.2K

## what

VENUE_TYPE: Church 43%, Fire Department 22%, Restaurant 18%, Community Organization 6%, Unsure / N/A 6%, Veteran's Organization 2%, Other 2%, VFW 1%, Food Truck 0%, Market 0%

EMAIL: office@2ndavechurch.org 9%, lloydsvillevfd114@comcast.net 9%, bworls@wactc.net 9%, eweaa1963@gmail.com 9%, admin@saintaugustineparish.com 9%,  turkeytownvfd107@gmail.com 9%, info@ckpgh.org 9%, hoffstotscafemonaco@gmail.com 9%, Office@stnicholasmonroeville.o 9%, unionvilleumccalendar@gmail.co 9%, thepubchipshop@gmail.com 9%

HOMEMADE_PIEROGIES: False 64%, True 36%

TAKE_OUT: True 100%

ALCOHOL: False 52%, True 48%

LUNCH: True 52%, False 48%

HANDICAP: True 93%, False 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| VALIDATED | other | 1 | 0 | True 277 |
| VENUE_NAME | who | 272 | 0 | Jackson's Restaurant and  3; Smock Volunteer Fire Depa 2; American Legion Post 343 2; Avonmore Polish Club 2 |
| VENUE_TYPE | category | 10 | 0 | Church 118; Fire Department 62; Restaurant 49; Community Organization 16 |
| VENUE_ADDRESS | other | 269 | 0 | 125 Shaffer Avenue, Smock 2; 134 North Jefferson Stree 2; 501 Indiana Avenue, Avonm 2; 758 Brookline Boulevard,  2 |
| WEBSITE | other | 246 | 19 | https://catholicpartnerpa 3; https://eatwalnut.com/ 3; https://www.facebook.com/ 2; https://www.facebook.com/ 2 |
| EVENTS | other | 175 | 5 | Friday Feb 20 from 4:00 P 42; Friday Feb 20 from 4:00 P 12; Wednesday Feb 18 from 11: 12; Friday Feb 20 from 11:00  11 |
| ETC | other | 51 | 227 | 412-321-1834 phone orders 1; https://www.wkbn.com/comm 1; Drive thru is 4:30-6:30 1; last pick up at 6:15 1 |
| MENU_URL | other | 188 | 78 | https://saintluke.net/fis 3; https://files.ecatholic.c 2; https://files.ecatholic.c 2; https://files.ecatholic.c 2 |
| MENU_TEXT | other | 143 | 129 | Lenten Menu
Appetizer
Sho 3; APPETIZERS
HUSH PUPPIES S 2; Potato, sauerkraut, cotta 1; Buffet pricing: Adults $1 1 |
| VENUE_NOTES | other | 119 | 155 | eat in or take out 4; dine in or take out 2; Dine in or take out 1; Dine in or take out; call 1 |
| PHONE | other | 207 | 61 | 412-828-9846 3; 724-677-2400  2; 724-658-3990 2; 724-697-4921 2 |
| EMAIL | category | 23 | 255 | office@2ndavechurch.org 1; lloydsvillevfd114@comcast 1; bworls@wactc.net 1; eweaa1963@gmail.com 1 |
| HOMEMADE_PIEROGIES | category | 3 | 182 | False 61; True 34 |
| TAKE_OUT | category | 2 | 33 | True 244 |
| ALCOHOL | category | 3 | 161 | False 60; True 56 |
| LUNCH | category | 3 | 34 | True 126; False 117 |
| HANDICAP | category | 3 | 220 | True 53; False 4 |
| PUBLISH | other | 1 | 0 | True 277 |
| ID | empty | 1 | 277 |  |
| LATITUDE | amount | 278 | 0 | 40.000808 2; 41.002206 2; 40.529724 2; 40.393608 2 |
| LONGITUDE | amount | 275 | 0 | -79.786315 2; -80.346786 2; -79.464513 2; -80.020161 2 |
| EVENTS_JSON | other | 178 | 0 | [{"dt_start": "2026-02-20 45; [{"dt_start": "2026-02-20 13; [{"dt_start": "2026-02-20 13; [{"dt_start": "2026-02-18 13 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:38:24.03832 277 |
| SOURCE_RUN_ID | audit | 1 | 0 | e0a8a66b-8095-4aff-89c5-7 277 |
| SRC_SHA256 | who | 1 | 0 | 9e207448fa0e2b0e1ca333684 277 |
