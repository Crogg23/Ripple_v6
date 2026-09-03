# FED_NTSB_AVIATION_AIRCRAFT

rows 31.5K  columns 96  scan 4.8s

roles: amount 9, audit 2, category 34, date 2, id 2, other 32, who 15

## when

DATE_LAST_INSP
  1980         1  
  1983         1  
  1989         1  
  1991         1  
  1994         2  
  1995         1  
  1997         1  
  1998         1  
  1999         2  
  2000         4  
  2001         7  
  2002         4  
  2003         5  
  2004         3  
  2005        12  
  2006        27  #
  2007       376  ########
  2008      1.3K  #############################
  2009      1.3K  ############################
  2010      1.3K  #############################
  2011      1.3K  ##############################
  2012      1.2K  ############################
  2013      1.1K  #########################
  2014      1.1K  ########################
  2015      1.2K  ##########################
  2016      1.1K  #########################
  2017      1.1K  #########################
  2018      1.1K  ########################
  2019      1.1K  ########################
  2020       965  #####################
  2021      1.0K  #######################
  2022      1.1K  #######################
  2023      1.0K  #######################
  2024       943  #####################
  2025       745  #################
  2026       175  ####

LCHG_DATE
  2020     19.2K  ##############################
  2021      1.8K  ###
  2022      2.3K  ####
  2023      1.9K  ###
  2024      1.9K  ###
  2025      2.6K  ####
  2026      1.8K  ###

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| CERT_MAX_GR_WT | 21.5K | 0 | 2.5K | 240.0K | 990.0K | 253.86M |
| FC_SEATS | 12.6K | 0 | 2 | 4 | 10 | 20.9K |
| CC_SEATS | 1.7K | 0 | 1 | 13 | 108 | 3.4K |
| PAX_SEATS | 11.5K | 0 | 2 | 239.00 | 660 | 138.0K |
| TOTAL_SEATS | 24.7K | 0 | 4 | 184.89 | 8.3K | 227.3K |
| AFM_HRS_LAST_INSP | 8.6K | -33 | 26 | 3.2K | 12.14M | 13.42M |

## who

OPER_NAME by rows
     15.6K  None
       255  Pilot
        77  SOUTHWEST AIRLINES CO
        72  DELTA AIR LINES INC
        54  American Airlines
        50  Delta Air Lines
        45  UNITED AIRLINES INC
        45  AMERICAN AIRLINES INC
        41  Ryanair
        41  United Airlines
        27  ON FILE
        26  Southwest Airlines
        22  Unknown
        22  UNITED AIR LINES INC
        22  SKYWEST AIRLINES INC
        21  CIVIL AIR PATROL INC
        18  Private Individual
        17  AIR METHODS CORP
        17  British Airways
        16  Private

OPER_NAME by dollars
       44.6K    15.6K rows  None
       14.3K       72 rows  DELTA AIR LINES INC
       10.4K       45 rows  UNITED AIRLINES INC
       10.1K       77 rows  SOUTHWEST AIRLINES CO
        8.9K      255 rows  Pilot
        8.3K       45 rows  AMERICAN AIRLINES INC
        6.3K       50 rows  Delta Air Lines
        4.5K       41 rows  United Airlines
        3.3K       54 rows  American Airlines
        3.3K        1 rows  Robert C. Davis
        3.0K       22 rows  UNITED AIR LINES INC
        2.9K       26 rows  Southwest Airlines
        2.8K       15 rows  JETBLUE AIRWAYS CORP
        2.5K        1 rows  John Geyman
        2.2K       14 rows  US AIRWAYS INC
        2.0K        1 rows  Swifton Aviation
        1.3K        5 rows  ATLAS AIR INC
        1.3K        7 rows  IndiGo Air
        1.3K        6 rows  United Airlines 
        1.2K        8 rows  Delta Air Lines, Inc.

OWNER_ACFT by rows
     14.7K  None
       177  Pilot
        98  DELTA AIR LINES INC
        95  WELLS FARGO BANK NORTHWEST NA TRUSTEE
        85  SOUTHWEST AIRLINES CO
        56  UNITED AIRLINES INC
        52  AMERICAN AIRLINES INC
        39  BANK OF UTAH TRUSTEE
        29  Individual
        26  WILMINGTON TRUST CO TRUSTEE
        25  Unknown
        24  ON FILE
        22  CIVIL AIR PATROL INC
        21  CHRISTIANSEN AVIATION INC
        21  Ryanair
        20  Wells Fargo Trust Co Na Trustee
        19  Private
        19  American Airlines Inc
        19  JETBLUE AIRWAYS CORP
        17  Delta Air Lines Inc

OWNER_ACFT by dollars
       42.7K    14.7K rows  None
       16.6K       98 rows  DELTA AIR LINES INC
       11.5K       85 rows  SOUTHWEST AIRLINES CO
       11.0K       56 rows  UNITED AIRLINES INC
        8.7K      177 rows  Pilot
        8.2K       52 rows  AMERICAN AIRLINES INC
        7.0K       95 rows  WELLS FARGO BANK NORTHWEST NA TRUSTEE
        3.3K        1 rows  Robert C. Davis
        3.1K       10 rows  UNITED AIR LINES INC
        3.1K       19 rows  JETBLUE AIRWAYS CORP
        2.5K        1 rows  John Geyman
        2.5K       26 rows  WILMINGTON TRUST CO TRUSTEE
        2.4K       39 rows  BANK OF UTAH TRUSTEE
        2.0K        1 rows  Winemiller Steve
        1.7K       10 rows  WELLS FARGO TRUST CO NA TRUSTEE
        1.6K        8 rows  United Airlines
        1.4K       11 rows  UMB BANK NA TRUSTEE
        1.3K        9 rows  WILMINGTON TRUST COMPANY TRUSTEE
        1.3K       16 rows  American Airlines
        1.2K        7 rows  US AIRWAYS INC

ELT_MANUFACTURER by rows
     23.5K  None
      1.4K  Artex
       784  ACK
       490  Ameri-King
       413  Narco
       385  ACK Technologies
       310  Pointer
       303  Kannad
       290  Unknown
       253  ARTEX
       167  EBC
        99  Dorne & Margolin
        97  Ameri-King Corp
        93  Ameriking
        82  Emergency Beacon Corp
        71  Airtex
        70  AmeriKing
        58  NARCO
        56  Narco Avionics
        52  Emergency Beacon Corp.

ELT_MANUFACTURER by dollars
      167.4K    23.5K rows  None
        7.9K     1.4K rows  Artex
        6.6K       36 rows  Honeywell
        5.7K       35 rows  ELTA
        4.5K      303 rows  Kannad
        2.5K      784 rows  ACK
        2.3K      253 rows  ARTEX
        2.0K       12 rows  Thales
        1.6K      413 rows  Narco
        1.4K      490 rows  Ameri-King
        1.2K      385 rows  ACK Technologies
        1.2K      310 rows  Pointer
        1.1K      290 rows  Unknown
         547        3 rows  Techtest LTD
         476      167 rows  EBC
         459        3 rows  Exail Aerospace
         440        2 rows  Delta
         440        1 rows  Safran
         440        1 rows  Astronics/DME Corp
         400        1 rows  TechTest LTD

ACFT_MAKE by rows
      6.4K  CESSNA
      3.7K  PIPER
      1.7K  BOEING
      1.4K  BEECH
      1.0K  Cessna
       716  BELL
       606  Piper
       411  AIRBUS
       383  ROBINSON
       329  CIRRUS DESIGN CORP
       305  MOONEY
       282  AIR TRACTOR INC
       274  ROBINSON HELICOPTER
       227  ROBINSON HELICOPTER COMPANY
       226  Beech
       205  BELLANCA
       187  EMBRAER
       181  MAULE
       175  AERONCA
       168  SCHWEIZER

ACFT_MAKE by dollars
       73.9K     1.7K rows  BOEING
       25.2K     6.4K rows  CESSNA
       23.3K      411 rows  AIRBUS
       14.3K     1.4K rows  BEECH
       12.3K     3.7K rows  PIPER
        4.1K       28 rows  AIRBUS INDUSTRIE
        3.9K      187 rows  EMBRAER
        3.9K       89 rows  BOMBARDIER INC
        3.8K      110 rows  Boeing
        3.2K     1.0K rows  Cessna
        3.2K       90 rows  MCDONNELL DOUGLAS
        2.8K       46 rows  DE HAVILLAND
        2.2K      716 rows  BELL
        2.0K       31 rows  Grumman
        1.9K      606 rows  Piper
        1.5K       25 rows  Airbus
        1.3K      329 rows  CIRRUS DESIGN CORP
        1.2K       21 rows  EMBRAER S A
        1.2K       10 rows  MCDONNELL DOUGLAS AIRCRAFT CO
        1.1K      305 rows  MOONEY

## who x when

OPER_NAME by DATE_LAST_INSP, dollars = TOTAL_SEATS
  AIR METHODS CORP                          2010:5 2011:7 2013:5 2015:5 2016:1 2017:15 2018:1 2022:20 2023:8
  AMERICAN AIRLINES INC                     2011:220 2012:44 2015:136 2018:590 2021:191 2023:536 2024:1.7K 2025:199 2026:175
  ATLAS AIR INC                             2010:8 2024:10
  American Airlines                         2012:225 2016:1 2017:186 2018:554 2019:2 2020:187 2023:621
  CIVIL AIR PATROL INC                      2001:4 2010:14 2012:8 2013:2 2014:8 2015:8 2017:4 2021:12 2022:6 2023:8 2025:4
  DELTA AIR LINES INC                       2008:507 2009:710 2011:487 2012:189 2013:191 2014:348 2015:168 2021:530 2022:695 2024:1.4K 2025:1.3K 2026:199
  Delta Air Lines                           2008:284 2011:674 2013:159 2014:498 2015:403 2016:285 2017:673 2018:309 2019:570 2023:355
  Delta Air Lines, Inc.                     2009:418 2010:152 2015:159 2016:157 2017:201 2024:117
  JETBLUE AIRWAYS CORP                      2009:160 2010:160 2011:160 2022:200 2025:172 2026:171
  John Geyman                               2010:2.5K
  None                                      1980:3 1989:4 1994:2 1995:2 1997:1 1998:4 1999:4 2000:4 2001:6 2002:8 2003:6 2004:8 2005:15 2006:38 2007:946 2008:1.8K 2009:1.2K 2010:1.2K 2011:1.3K 2012:1.1K 2013:964 2014:1.1K 2015:1.9K 2016:2.3K 2017:2.4K 2018:2.1K 2019:1.9K 2020:1.9K 2021:1.9K 2022:2.1K 2023:2.3K 2024:2.0K 2025:1.5K 2026:305
  ON FILE                                   2010:6 2011:33 2012:11 2013:4 2015:4 2016:4
  Pilot                                     2006:2 2007:6 2008:27 2009:8.3K 2010:41 2011:41 2012:60 2013:61 2014:32 2015:46 2016:13 2017:39 2018:22 2019:40 2020:20 2021:23 2022:26 2023:1 2025:1
  Private Individual                        2010:1 2012:7 2014:4 2020:14
  Robert C. Davis                           2007:3.3K
  SKYWEST AIRLINES INC                      2009:30 2010:154 2011:55 2016:80 2017:80 2022:55 2025:74
  SOUTHWEST AIRLINES CO                     2008:427 2009:145 2010:578 2011:430 2012:285 2013:151 2014:151 2015:302 2017:151 2018:521 2020:151 2021:370 2022:771 2023:648 2024:1.1K 2025:1.1K
  Southwest Airlines                        2011:145 2012:149 2014:486 2015:143 2016:302 2017:336 2018:151 2019:302 2022:148
  Swifton Aviation                          2020:2.0K
  UNITED AIR LINES INC                      2010:128 2011:178 2012:124 2015:259 2019:188
  UNITED AIRLINES INC                       2014:228 2021:1.2K 2022:840 2023:1.6K 2024:1.4K 2025:453 2026:175
  US AIRWAYS INC                            2008:130 2010:379 2014:159 2015:105
  United Airlines                           2007:162 2011:368 2013:1 2014:190 2017:187 2019:179 2020:158 2021:400 2022:158
  United Airlines                           2024:188
  Unknown                                   2008:4

OWNER_ACFT by DATE_LAST_INSP, dollars = TOTAL_SEATS
  AMERICAN AIRLINES INC                     2003:70 2012:44 2015:136 2018:590 2021:191 2023:536 2024:1.7K 2025:280 2026:175
  American Airlines                         2012:225 2023:621
  American Airlines Inc                     2017:186 2018:187 2019:159 2020:81
  BANK OF UTAH TRUSTEE                      2009:4 2013:20 2014:1 2020:11 2021:4 2022:194 2023:221 2024:90 2025:255
  CHRISTIANSEN AVIATION INC                 2009:4 2010:2 2011:8 2012:24 2014:4 2015:2 2016:1 2017:4 2018:4 2021:10 2022:4
  CIVIL AIR PATROL INC                      2001:4 2008:4 2010:14 2012:8 2013:2 2014:8 2015:8 2017:4 2021:12 2022:6 2023:8 2025:4
  DELTA AIR LINES INC                       2008:168 2009:710 2011:567 2012:189 2013:191 2014:657 2015:168 2016:168 2017:565 2018:309 2021:530 2022:695 2023:95 2024:1.4K 2025:1.4K 2026:199
  Delta Air Lines Inc                       2009:149 2010:141 2018:1 2019:738
  Individual                                2010:1 2011:6 2012:9 2013:1 2015:6 2016:5 2017:8 2018:3 2019:1 2020:1
  JETBLUE AIRWAYS CORP                      2009:160 2010:160 2011:160 2022:200 2025:172 2026:171
  John Geyman                               2010:2.5K
  None                                      1980:3 1989:4 1994:2 1995:2 1997:1 1998:4 1999:4 2000:4 2001:6 2002:8 2003:6 2004:8 2005:15 2006:26 2007:529 2008:1.1K 2009:1.4K 2010:1.2K 2011:1.3K 2012:1.1K 2013:964 2014:1.1K 2015:1.9K 2016:2.3K 2017:2.4K 2018:2.1K 2019:1.8K 2020:1.7K 2021:1.5K 2022:1.7K 2023:1.8K 2024:1.6K 2025:1.1K 2026:215
  ON FILE                                   2010:6 2011:27 2012:11 2013:4 2015:4 2016:4
  Pilot                                     2006:2 2007:14 2008:30 2009:8.3K 2010:27 2011:20 2012:42 2013:31 2014:30 2015:22 2016:11 2017:30 2018:8 2019:9 2020:20 2021:17 2022:4 2023:1 2024:2
  Private                                   2018:4
  Robert C. Davis                           2007:3.3K
  SOUTHWEST AIRLINES CO                     2008:427 2009:145 2010:578 2011:575 2012:285 2013:151 2014:637 2015:151 2016:151 2017:336 2018:370 2020:151 2021:370 2022:771 2023:648 2024:1.1K 2025:1.1K
  UMB BANK NA TRUSTEE                       2025:188
  UNITED AIR LINES INC                      2010:128 2011:178
  UNITED AIRLINES INC                       2014:228 2015:259 2021:1.2K 2022:1.0K 2023:1.6K 2024:1.4K 2025:508 2026:175
  US AIRWAYS INC                            2010:379 2011:36 2014:159 2015:105
  United Airlines                           2017:187 2020:158 2021:400
  WELLS FARGO BANK NORTHWEST NA TRUSTEE     2008:204 2009:286 2010:700 2011:896 2012:292 2013:1 2014:160 2015:446 2016:158 2017:624
  WELLS FARGO TRUST CO NA TRUSTEE           2021:181 2022:306 2023:100 2024:117
  WILMINGTON TRUST CO TRUSTEE               2009:4 2011:142 2016:1 2021:5 2022:180 2024:188 2025:186
  WILMINGTON TRUST COMPANY TRUSTEE          2011:192 2014:190 2015:1 2023:68
  Wells Fargo Trust Co Na Trustee           2018:349 2019:680
  Winemiller Steve                          2020:2.0K

## what

AIRCRAFT_KEY: 1 98%, 2 2%, 3 0%, 5 0%

ACFT_MISSING: N 100%, Y 0%

FAR_PART: 091 71%, NUSN 8%, NUSC 5%, 137 4%, 121 3%, 135 3%, None 2%, UNK 2%, 129 1%, PUBU 1%, 133 0%, ARMF 0%

FLT_PLAN_FILED: NONE 59%, None 17%, IFR 10%, UNK 6%, VFR 4%, CVFR 3%, VFIF 0%, MVFR 0%

FLIGHT_PLAN_ACTIVATED: N 42%, None 40%, Y 14%, U 4%

DAMAGE: SUBS 77%, DEST 11%, None 7%, MINR 4%, UNK 1%

ACFT_FIRE: NONE 85%, GRD 9%, UNK 4%, None 1%, IFLT 1%, BOTH 0%, UNKT 0%

ACFT_EXPL: NONE 90%, UNK 5%, None 3%, GRD 1%, IFLT 0%, BOTH 0%, UNKT 0%

ACFT_CATEGORY: AIR 84%, HELI 11%, GLI 1%, None 1%, BALL 1%, WSFT 1%, GYRO 1%, PPAR 0%, ULTR 0%, UNK 0%, PLFT 0%, BLIM 0%

HOMEBUILT: N 89%, Y 11%

NUM_ENG: 1.0 71%, nan 15%, 2.0 12%, 0.0 1%, 4.0 0%, 3.0 0%, 6.0 0%, 8.0 0%

FIXED_RETRACTABLE: FIXD 76%, RETR 24%

TYPE_LAST_INSP: ANNL 42%, None 26%, 100H 11%, COND 9%, UNK 6%, COAW 4%, AAIP 2%

ELT_INSTALL: Y 60%, None 29%, N 11%

ELT_OPER: None 45%, N 39%, Y 16%

ELT_AIDED_LOC_EV: None 69%, N 28%, Y 2%

ELT_TYPE: None 55%, UNK 18%, C126 11%, C91 8%, C91A 7%, C91a 0%

OPER_INDIVIDUAL_NAME: N 62%, Y 38%

CERTS_HELD: Y 88%, None 12%

OPER_SCHED: None 88%, NSCH 6%, SCHD 6%

OPER_DOM_INT: None 89%, DOM 8%, INT 3%

OPER_PAX_CARGO: None 90%, PAX 9%, CARG 1%, MAIL 0%

TYPE_FLY: PERS 54%, None 21%, INST 12%, AAPL 4%, POSI 2%, BUS  1%, OWRK 1%, AOBV 1%, FLTS 1%, UNK  1%, BUS 1%, FERY 0%

SECOND_PILOT: N 62%, None 20%, Y 18%

DPRT_PT_SAME_EV: None 82%, S 9%, L 6%, Y 2%, U 1%

AFM_HRS_SINCE: N 69%, Y 31%

SITE_SEEING: N 87%, None 12%, Y 1%

AIR_MEDICAL: N 87%, None 12%, Y 1%

MED_TYPE_FLIGHT: None 100%, MEDE 0%, DISC 0%, ORGT 0%

COMMERCIAL_SPACE_FLIGHT: False 100%, True 0%

UNMANNED: False 100%, True 0%

IFR_EQUIPPED_CERT: False 83%, True 17%

ELT_MOUNTED_AIRCRAFT: False 70%, True 30%

ELT_CONNECTED_ANTENNA: False 72%, True 28%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| EV_ID | id | 31.4K | 0 | 20260731203497 159; 20260709203356 159; 20260731203496 158; 20260730203490 158 |
| AIRCRAFT_KEY | category | 4 | 0 | 1 31.0K; 2 538; 3 9; 5 1 |
| REGIS_NO | other | 29.6K | 0 | UNREG 163; EC-MYC 158; SP-RNT 158; LV-KGR 158 |
| NTSB_NO | id | 30.7K | 0 | DCA26WA297B 158; DCA26WA297A 158; GAA26WA267 158; CEN26LA274 158 |
| ACFT_MISSING | category | 2 | 0 | N 31.5K; Y 35 |
| FAR_PART | category | 17 | 0 | 091 22.2K; NUSN 2.4K; NUSC 1.6K; 137 1.2K |
| FLT_PLAN_FILED | category | 8 | 0 | NONE 18.6K; None 5.4K; IFR 3.1K; UNK 1.9K |
| FLIGHT_PLAN_ACTIVATED | category | 4 | 0 | N 13.2K; None 12.6K; Y 4.3K; U 1.4K |
| DAMAGE | category | 5 | 0 | SUBS 24.3K; DEST 3.5K; None 2.2K; MINR 1.3K |
| ACFT_FIRE | category | 7 | 0 | NONE 26.9K; GRD 2.7K; UNK 1.3K; None 270 |
| ACFT_EXPL | category | 7 | 0 | NONE 28.4K; UNK 1.5K; None 1.1K; GRD 399 |
| ACFT_MAKE | who | 4.6K | 0 | CESSNA 6.4K; PIPER 3.7K; BOEING 1.7K; BEECH 1.4K |
| ACFT_MODEL | other | 6.1K | 0 | 172 934; 737 719; R44 393; PA28 380 |
| ACFT_SERIES | other | 1.0K | 0 | None 19.9K; NO SERIES 1.6K; B 649; A 586 |
| ACFT_SERIAL_NO | other | 24.5K | 0 | None 3.1K; 001 177; 5724 143; 3506 143 |
| CERT_MAX_GR_WT | amount | 2.0K | 0 | nan 10.0K; 2300.0 724; 1320.0 701; 2550.0 665 |
| ACFT_CATEGORY | category | 13 | 0 | AIR 26.6K; HELI 3.3K; GLI 444; None 414 |
| ACFT_REG_CLS | other | 1 | 0 | None 31.5K |
| HOMEBUILT | category | 2 | 0 | N 28.0K; Y 3.5K |
| FC_SEATS | amount | 11 | 0 | nan 18.9K; 2.0 7.4K; 1.0 4.8K; 3.0 165 |
| CC_SEATS | amount | 21 | 0 | nan 29.8K; 0.0 825; 2.0 281; 1.0 200 |
| PAX_SEATS | amount | 178 | 0 | nan 20.0K; 2.0 3.7K; 1.0 2.5K; 4.0 1.7K |
| TOTAL_SEATS | amount | 232 | 0 | 4.0 8.4K; 2.0 8.4K; nan 6.8K; 6.0 2.2K |
| NUM_ENG | category | 8 | 0 | 1.0 22.4K; nan 4.6K; 2.0 3.9K; 0.0 390 |
| FIXED_RETRACTABLE | category | 2 | 0 | FIXD 24.0K; RETR 7.5K |
| TYPE_LAST_INSP | category | 7 | 0 | ANNL 13.4K; None 8.2K; 100H 3.4K; COND 2.7K |
| DATE_LAST_INSP | date | 6.3K | 0 | NaT 10.8K; 2025-05-01 00:00:00 115; 2025-03-01 00:00:00 111; 2025-07-01 00:00:00 110 |
| AFM_HRS_LAST_INSP | amount | 1.2K | 0 | nan 22.9K; 1.0 305; 10.0 248; 2.0 227 |
| AFM_HRS | amount | 13.6K | 0 | nan 11.2K; 4292.7001953125 102; 748.0 102; 2632.0 102 |
| ELT_INSTALL | category | 3 | 0 | Y 18.8K; None 9.2K; N 3.6K |
| ELT_OPER | category | 3 | 0 | None 14.1K; N 12.2K; Y 5.2K |
| ELT_AIDED_LOC_EV | category | 3 | 0 | None 21.9K; N 8.9K; Y 781 |
| ELT_TYPE | category | 6 | 0 | None 17.4K; UNK 5.7K; C126 3.5K; C91 2.6K |
| OWNER_ACFT | who | 14.2K | 0 | None 14.7K; Pilot 177; DELTA AIR LINES INC 114; UNITED AIRLINES INC 112 |
| OWNER_STREET | who | 8.7K | 65 | None 21.0K; 3511 SILVERSIDE RD STE 10 114; On File 100; 2702 LOVE FIELD DR # HDQ- 63 |
| OWNER_CITY | who | 8.7K | 0 | None 5.2K; WILMINGTON 511; ANCHORAGE 326; Wilmington 240 |
| OWNER_STATE | who | 57 | 0 | None 5.7K; TX 2.4K; CA 2.2K; FL 1.8K |
| OWNER_COUNTRY | who | 191 | 0 | USA 26.9K; None 2.0K; BR  216; CA  168 |
| OWNER_ZIP | who | 18.5K | 0 | None 6.5K; 198104902 167; 30354 133; 59901 129 |
| OPER_INDIVIDUAL_NAME | category | 2 | 0 | N 19.4K; Y 12.1K |
| OPER_NAME | who | 13.1K | 0 | None 15.6K; Pilot 255; UNITED AIRLINES INC 105; DELTA AIR LINES INC 104 |
| OPER_SAME | other | 1 | 0 | None 31.5K |
| OPER_DBA | who | 1.2K | 0 | None 29.9K; N/A 108; American Eagle 16; United Express 15 |
| OPER_ADDR_SAME | other | 1 | 0 | None 31.5K |
| OPER_STREET | who | 7.2K | 63 | None 23.1K; On File 144; 2702 LOVE FIELD DR # HDQ- 52; 1775 M H JACKSON SERVICE  48 |
| OPER_CITY | who | 8.9K | 0 | None 5.8K; ANCHORAGE 248; Anchorage 223; WILMINGTON 184 |
| OPER_STATE | other | 57 | 0 | None 6.4K; TX 2.4K; CA 2.3K; FL 1.9K |
| OPER_COUNTRY | other | 193 | 0 | USA 26.6K; None 2.1K; BR  220; CA  149 |
| OPER_ZIP | other | 17.0K | 0 | None 8.0K; 30354 123; 60606 123; 59901 121 |
| OPER_CODE | other | 1.1K | 0 | None 29.4K; N/A 132; DALA 59; AALA 51 |
| CERTS_HELD | category | 2 | 0 | Y 27.6K; None 3.9K |
| OPRTNG_CERT | other | 1 | 0 | None 31.5K |
| OPER_CERT | other | 1 | 0 | None 31.5K |
| OPER_CERT_NUM | other | 751 | 0 | None 30.2K; N/A 110; SWAA304A 34; UALA011A 27 |
| OPER_SCHED | category | 3 | 0 | None 27.7K; NSCH 1.9K; SCHD 1.9K |
| OPER_DOM_INT | category | 3 | 0 | None 28.1K; DOM 2.4K; INT 1.0K |
| OPER_PAX_CARGO | category | 4 | 0 | None 28.3K; PAX 2.7K; CARG 450; MAIL 8 |
| TYPE_FLY | category | 25 | 0 | PERS 16.4K; None 6.3K; INST 3.6K; AAPL 1.3K |
| SECOND_PILOT | category | 3 | 0 | N 19.6K; None 6.2K; Y 5.7K |
| DPRT_PT_SAME_EV | category | 5 | 0 | None 25.8K; S 2.8K; L 1.8K; Y 684 |
| DPRT_APT_ID | other | 8.2K | 0 | None 9.4K; PVT  218; NONE 195; PVT 149 |
| DPRT_CITY | who | 7.5K | 0 | None 6.8K; Anchorage 181; Houston 137; Fort Lauderdale 129 |
| DPRT_STATE | other | 58 | 0 | None 8.7K; CA 2.1K; TX 1.9K; FL 1.8K |
| DPRT_COUNTRY | other | 184 | 0 | USA 23.2K; None 6.2K; BR  232; GB 103 |
| DPRT_TIME | other | 1.2K | 0 | nan 11.9K; 1700.0 417; 1600.0 414; 1800.0 409 |
| DPRT_TIMEZN | other | 1 | 0 | None 31.5K |
| DEST_SAME_LOCAL | other | 1 | 0 | None 31.5K |
| DEST_APT_ID | other | 7.4K | 0 | None 12.1K; PVT  238; NONE 190; PVT 123 |
| DEST_CITY | who | 7.0K | 0 | None 9.4K; Anchorage 145; Houston 122; Fairbanks 114 |
| DEST_STATE | other | 58 | 0 | None 11.1K; CA 1.9K; TX 1.7K; FL 1.6K |
| DEST_COUNTRY | other | 190 | 0 | USA 21.0K; None 8.5K; BR  226; CA  104 |
| PHASE_FLT_SPEC | other | 1 | 0 | None 31.5K |
| REPORT_TO_ICAO | other | 1 | 0 | None 31.5K |
| EVACUATION | other | 1 | 0 | None 31.5K |
| LCHG_DATE | date | 10.0K | 0 | 2020-09-25 18:00:53 374; 2020-09-25 18:01:38 373; 2020-09-25 18:06:16 356; 2020-09-25 17:59:24 345 |
| LCHG_USERID | other | 191 | 0 | None 19.0K; coln 5.1K; broda 961; dobn 695 |
| AFM_HRS_SINCE | category | 2 | 0 | N 21.6K; Y 9.9K |
| RWY_NUM | other | 341 | 0 | None 17.2K; 18 709; 36 587; 27 550 |
| RWY_LEN | amount | 2.3K | 0 | nan 17.6K; 5000.0 439; 3000.0 311; 4000.0 273 |
| RWY_WIDTH | amount | 165 | 0 | nan 17.7K; 100.0 3.4K; 75.0 3.3K; 150.0 2.7K |
| SITE_SEEING | category | 3 | 0 | N 27.3K; None 3.9K; Y 305 |
| AIR_MEDICAL | category | 3 | 0 | N 27.4K; None 3.9K; Y 235 |
| MED_TYPE_FLIGHT | category | 4 | 0 | None 31.4K; MEDE 88; DISC 54; ORGT 5 |
| ACFT_YEAR | other | 106 | 0 | nan 14.7K; 1979.0 537; 1978.0 490; 1977.0 476 |
| FUEL_ON_BOARD | other | 711 | 0 | None 21.6K; 20 481; 40 475; 30 473 |
| COMMERCIAL_SPACE_FLIGHT | category | 2 | 0 | False 31.5K; True 1 |
| UNMANNED | category | 2 | 0 | False 31.4K; True 62 |
| IFR_EQUIPPED_CERT | category | 2 | 0 | False 26.2K; True 5.3K |
| ELT_MOUNTED_AIRCRAFT | category | 2 | 0 | False 22.1K; True 9.4K |
| ELT_CONNECTED_ANTENNA | category | 2 | 0 | False 22.6K; True 8.9K |
| ELT_MANUFACTURER | who | 958 | 0 | None 23.5K; Artex 1.4K; ACK 784; Ameri-King 490 |
| ELT_MODEL | other | 1.6K | 0 | None 24.4K; AK-450 555; E-04 527; E-01 419 |
| ELT_REASON_OTHER | other | 1 | 0 | None 31.5K |
| INGESTED_AT | audit | 1 | 0 | 1786154107240125 31.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 767e3583-447f-4101-bd46-a 31.5K |
| SRC_SHA256 | who | 1 | 0 | 0cf30a610d18eb109035b8310 31.5K |
