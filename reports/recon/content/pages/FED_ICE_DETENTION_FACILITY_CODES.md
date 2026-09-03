# FED_ICE_DETENTION_FACILITY_CODES

rows 1.5K  columns 15  scan 5.1s

roles: amount 2, audit 2, category 3, other 3, state 1, who 4

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 1.5K | 13.45 | 37.13 | 56.51 | 64.83 | 54.4K |
| LONGITUDE | 1.5K | -166.54 | -95.36 | -66.13 | 145.75 | -139.3K |

## who

DETENTION_FACILITY_NAME by rows
         7  Jefferson County Jail
         6  Washington County Jail
         3  Montgomery County Jail
         3  Columbia County Jail
         2  Platte County Jail
         2  Polk County Jail
         2  Phelps County Jail
         2  Clark County Jail
         2  University Hospital
         2  Butler County Jail
         2  Alexandria City Jail
         2  Mercy Hospital
         2  Monroe County Jail
         2  Brown County Jail
         2  Martin County Jail
         2  Montgomery City Jail
         2  Orange County Jail
         2  Madison County Jail
         2  US Marshals  SDTX
         2  Marion County Jail

DETENTION_FACILITY_NAME by dollars
      281.22        7 rows  Jefferson County Jail
      246.42        6 rows  Washington County Jail
      117.07        3 rows  Columbia County Jail
      112.27        3 rows  Montgomery County Jail
       93.60        2 rows  Sheridan County Jail
       89.98        2 rows  Brown County Jail
       87.88        2 rows  Cass County Jail
       86.90        2 rows  Madison County Jail
          85        2 rows  Clinton County Jail
          85        2 rows  Essex County Jail
       83.91        2 rows  Clark County Jail
       83.75        2 rows  Park County Jail
       83.23        2 rows  Seneca County Jail
       82.78        2 rows  Pike County Jail
       81.43        2 rows  Platte County Jail
       80.16        2 rows  Frederick Holdroom
       78.39        2 rows  Phelps County Jail
       77.60        2 rows  Alexandria City Jail
       77.21        2 rows  Butler County Jail
       76.49        2 rows  Lake County Jail

DETENTION_FACILITY_CODE by rows
         1  ALBHOLD
         1  ADAMSWA
         1  AKANVIL
         1  ARRMCCA
         1  AMTHOLD
         1  BAYAMPR
         1  BSQUETX
         1  BEDFOOH
         1  ALLEGVA
         1  BELCOTX
         1  BLKREOK
         1  BERGENJ
         1  AMHERVA
         1  AKFAIRB
         1  ADVHBCA
         1  ABRXSPA
         1  BHCALCA
         1  ARAPACO
         1  AFRC
         1  ADVHCHI

DETENTION_FACILITY_CODE by dollars
       64.83        1 rows  AKFAIRB
       64.54        1 rows  AKANVIL
       61.69        1 rows  AKPALMC
       61.60        1 rows  AKMATSU
       61.36        1 rows  AKGSCCC
       61.30        1 rows  AKHIGHL
       61.22        1 rows  ANCHOLD
       61.22        1 rows  ANCHOAK
       61.22        1 rows  AKCOOKI
       61.19        1 rows  AKMCYOU
       60.58        1 rows  AKWILCC
       60.58        1 rows  AKWILPT
       58.36        1 rows  AKLEMON
       57.80        1 rows  KODIAAK
       57.05        1 rows  SITKAAK
       55.35        1 rows  AKKETCH
       53.87        1 rows  DUTCHAK
       48.85        1 rows  FDLHOLD
       48.84        1 rows  ROSEAMN
       48.83        1 rows  BOTTIND

COUNTY by rows
        29  El Paso
        26  Maricopa
        25  Bexar
        24  San Diego
        22  Miami-Dade
        18  Orange
        18  Los Angeles
        18  Cameron
        18  Hidalgo
        15  Washington
        13  Montgomery
        13  Pinal
        12  Cook
        12  San Bernardino
        12  Kern
        12  Harris
        11  Broward
        10  Erie
        10  Suffolk
        10  Essex

COUNTY by dollars
      935.87       29 rows  El Paso
      870.14       26 rows  Maricopa
      784.97       24 rows  San Diego
      736.51       25 rows  Bexar
      619.98       18 rows  Orange
      613.59       18 rows  Los Angeles
      608.91       15 rows  Washington
      566.60       22 rows  Miami-Dade
      502.26       12 rows  Cook
      477.88       18 rows  Hidalgo
      470.09       18 rows  Cameron
      433.41       13 rows  Montgomery
      428.89       13 rows  Pinal
      428.29       10 rows  Erie
      425.70       12 rows  Kern
      418.81       10 rows  Essex
      417.26       10 rows  Suffolk
      412.91       12 rows  San Bernardino
      392.51       10 rows  Jefferson
      388.53       10 rows  Monroe

SRC_SHA256 by rows
      1.5K  c0fa39d2a30f306e40c86ccab2840e28e36aa83c9691f15cb3fd5ce83c02afdd

SRC_SHA256 by dollars
       54.4K     1.5K rows  c0fa39d2a30f306e40c86ccab2840e28e36aa83c9691f15cb3fd5ce83c02

## where

STATE: TX 250, CA 124, FL 92, NY 91, AZ 63, VA 59, CO 52, PA 46, LA 34, GA 32, IL 31, WA 30

## what

AOR: Chicago 12%, Miami 12%, St. Paul 9%, El Paso 9%, New Orleans 8%, Denver 8%, Seattle 7%, Salt Lake City 7%, Buffalo 7%, San Antonio 7%, Phoenix 7%, Philadelphia 7%

TYPE_DETAILED: IGSA 29%, Hospital 16%, USMS IGA 16%, Hold 14%, Unknown 7%, Medical 4%, Hotel 4%, BOP 3%, Other 3%, DIGSA 2%, Juvenile 2%

TYPE_GROUPED: Non-Dedicated 29%, Federal 19%, Medical 19%, Hold/Staging 13%, Other/Unknown 10%, Dedicated 4%, Hotel 4%, Family/Youth 3%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| DETENTION_FACILITY_CODE | who | 1.5K | 0 | ZAVCOTX 8; YUMHOLD 8; YUBAJCA 8; YRMDCAZ 8 |
| DETENTION_FACILITY_NAME | who | 1.5K | 0 | Washington County Jail 13; Jefferson County Jail 10; Williamson County Jail 9; Zavala County Jail 8 |
| ADDRESS | other | 1.4K | 66 | 200 E Uvalde Street #5 8; 3911 S. Pico Ave. 8; 215 5th Street 8; 2400 S Avenue A 8 |
| CITY | other | 890 | 8 | San Antonio 24; El Paso 24; Miami 19; Phoenix 19 |
| COUNTY | who | 609 | 8 | El Paso 29; Maricopa 26; Bexar 25; San Diego 24 |
| STATE | state | 57 | 1 | TX 250; CA 124; FL 92; NY 91 |
| ZIP | other | 1.1K | 70 | 78550 9; 79772 9; 78839 8; 85365 8 |
| AOR | category | 26 | 0 | Chicago 109; Miami 108; St. Paul 84; El Paso 81 |
| LATITUDE | amount | 1.4K | 8 | 33.4482948 10; 31.7618778 10; 27.3698188 9; 28.6794662 8 |
| LONGITUDE | amount | 1.5K | 8 | -112.0725488 10; -106.4850217 10; -99.4902136 9; -99.8269368 8 |
| TYPE_DETAILED | category | 25 | 32 | IGSA 408; Hospital 223; USMS IGA 222; Hold 189 |
| TYPE_GROUPED | category | 8 | 0 | Non-Dedicated 438; Federal 279; Medical 277; Hold/Staging 200 |
| INGESTED_AT | audit | 1 | 0 | 1785965529980834 1.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | 2e9397be-fb77-4be7-9bfc-a 1.5K |
| SRC_SHA256 | who | 1 | 0 | c0fa39d2a30f306e40c86ccab 1.5K |
