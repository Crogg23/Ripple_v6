# PORTAL_CKA_ANALYZE_BOSTON_DB1AEFD5B6

rows 2.6K  columns 31  scan 6.3s

roles: amount 2, audit 2, category 21, date 2, id 1, other 1, who 3

## when

CREATION_DATE
  2025      2.6K  ##############################

INGESTED_AT
  2026      2.6K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| X_COORD | 2.6K | -71.14 | -71.06 | -70.92 | -70.92 | -186.8K |
| Y_COORD | 2.6K | 42.27 | 42.35 | 42.37 | 42.38 | 111.3K |

## who

BUSINESS_NAME by rows
       307  NA
        14  Bank of America
        13  Starbucks
         8  Citizens
         8  Dunkin'
         7  7-Eleven
         6  Dunkin
         5  Dunkin’
         5  CVS
         5  CVS Pharmacy
         5  Santander
         5  Bank of America ATM
         5  Tatte
         5  Chase
         4  Starbucks Coffee
         4  Chipotle
         3  Burger King
         3  Mobil
         3  Stanhope Garage
         3  bb.q chicken

BUSINESS_NAME by dollars
      -70.92        1 rows  Exhale yoga
      -70.92        1 rows  Sandy’s cleaners
      -70.92        1 rows  Elliot Powers Attorney at Law
      -70.92        1 rows  Regal
      -70.92        1 rows  Chez vous
      -70.92        1 rows  Regan communications
      -70.92        1 rows  Fiya hen
      -70.92        1 rows  Comm ave canna
      -70.92        1 rows  Boston light source
      -70.92        1 rows  Rent wise Boston
      -70.92        1 rows  Good faith tattoo
      -70.92        1 rows  Kayuga
      -70.92        1 rows  sasa skin care & spa
      -70.92        1 rows  Carbon salon
      -70.92        1 rows  Atlantic
      -70.92        1 rows  Polkadogbakery
      -70.92        1 rows  O’brien and Levine court reporting
      -70.92        1 rows  Lattti associates llc
      -70.92        1 rows  Ari Boston
      -70.92        1 rows  Trillium brewery

BUSINESS_SUBTYPE by rows
       306  Sit_down_restaurant
       144  Cafe/Smoothie/beverage_shop
       126  Takeout_with_seating
       108  other
       101  Hair_Salon
        77  Bank
        57  Convenience_Store
        55  Real_Estate_Broker
        53  Clothing_Store
        46  Barber_Shop
        43  Takeout_with_no_seating
        42  Alcohol_Store
        37  Dentist's_or_Orthodontist's_Off
        37  Grocery_Store_(Fresh_Produce)
        37  Fitness_Studio
        36  Auto_Repair_or_Service_Shop
        32  Laundry_Service/Dry_cleaner
        32  Nail_Salon
        29  Parking_Garage
        28  Sit_down_restaurant,Takeout_with_seating

BUSINESS_SUBTYPE by dollars
      -70.92        1 rows  Takeout_with_no_seating,Takeout_with_seating
      -70.92        1 rows  Night_Club, Bar,Sit_down_restaurant
      -70.92        1 rows  Advertising agency, other
      -70.92        1 rows  Parking_Lot,Parking_Garage
      -70.92        1 rows  Massage,Doctor's_Office_-_Specialist
      -70.92        1 rows  Spa,Massage
      -70.92        1 rows  Web designer, other
      -70.92        1 rows  Brow_and_Lash_Services,Waxing/Hair_Removal,Nail_Salon
      -70.92        1 rows  Interior designer, other
      -71.05        1 rows  Fitness_Studio,Gym
      -71.05        1 rows  Massage,Spa,Chiropractor's_Office
      -71.05        1 rows  Cafe/Smoothie/beverage_shop,Sit_down_restaurant,Takeout_with
      -71.05        1 rows  Spa,Optometrist_or_Other_Eye_Care
      -71.05        1 rows  Fitness_Studio,Spa,other
      -71.05        1 rows  Waxing/Hair_Removal,Nail_Salon,Brow_and_Lash_Services
      -71.05        1 rows  Community_Center, Doctor's_Office_-_Specialist,Dentist's_or_
      -71.05        1 rows  Insurance_Broker,Real_Estate_Broker
      -71.05        1 rows  Skateshop, other
      -71.05        1 rows  Bank,Real_Estate_Broker
      -71.05        1 rows  Commercial Printing, other

SRC_SHA256 by rows
      2.6K  782edd91101796721c25a8df83979152dc74f9533ff53d62f19ee8e344fd3014

SRC_SHA256 by dollars
     -186.8K     2.6K rows  782edd91101796721c25a8df83979152dc74f9533ff53d62f19ee8e344fd

## who x when

BUSINESS_NAME by CREATION_DATE, dollars = X_COORD
  7-Eleven                                  2025:-497.53
  Bank of America                           2025:-994.89
  Bank of America ATM                       2025:-355.40
  Boston light source                       2025:-70.92
  Burger King                               2025:-213.29
  CVS                                       2025:-355.44
  CVS Pharmacy                              2025:-355.45
  Chase                                     2025:-355.39
  Chez vous                                 2025:-70.92
  Chipotle                                  2025:-284.27
  Citizens                                  2025:-568.58
  Comm ave canna                            2025:-70.92
  Dunkin                                    2025:-426.42
  Dunkin'                                   2025:-568.55
  Dunkin’                                   2025:-355.36
  Elliot Powers Attorney at Law             2025:-70.92
  Exhale yoga                               2025:-70.92
  Fiya hen                                  2025:-70.92
  Mobil                                     2025:-213.27
  NA                                        2025:-21.6K
  Regal                                     2025:-70.92
  Regan communications                      2025:-70.92
  Rent wise Boston                          2025:-70.92
  Sandy’s cleaners                          2025:-70.92
  Santander                                 2025:-355.33
  Stanhope Garage                           2025:-213.18
  Starbucks                                 2025:-923.86
  Starbucks Coffee                          2025:-284.24
  Tatte                                     2025:-355.30
  bb.q chicken                              2025:-213.30

BUSINESS_SUBTYPE by CREATION_DATE, dollars = X_COORD
  Advertising agency, other                 2025:-70.92
  Alcohol_Store                             2025:-3.0K
  Auto_Repair_or_Service_Shop               2025:-2.6K
  Bank                                      2025:-5.5K
  Barber_Shop                               2025:-3.3K
  Brow_and_Lash_Services,Waxing/Hair_Remov  2025:-70.92
  Cafe/Smoothie/beverage_shop               2025:-10.2K
  Clothing_Store                            2025:-3.8K
  Convenience_Store                         2025:-4.1K
  Dentist's_or_Orthodontist's_Off           2025:-2.6K
  Fitness_Studio                            2025:-2.6K
  Fitness_Studio,Gym                        2025:-71.05
  Grocery_Store_(Fresh_Produce)             2025:-2.6K
  Hair_Salon                                2025:-7.2K
  Interior designer, other                  2025:-70.92
  Laundry_Service/Dry_cleaner               2025:-2.3K
  Massage,Doctor's_Office_-_Specialist      2025:-70.92
  Nail_Salon                                2025:-2.3K
  Night_Club, Bar,Sit_down_restaurant       2025:-70.92
  Parking_Garage                            2025:-2.1K
  Parking_Lot,Parking_Garage                2025:-70.92
  Real_Estate_Broker                        2025:-3.8K
  Sit_down_restaurant                       2025:-21.7K
  Sit_down_restaurant,Takeout_with_seating  2025:-2.0K
  Spa,Massage                               2025:-70.92
  Takeout_with_no_seating                   2025:-3.1K
  Takeout_with_no_seating,Takeout_with_sea  2025:-70.92
  Takeout_with_seating                      2025:-9.0K
  Web designer, other                       2025:-70.92
  other                                     2025:-7.7K

## what

ADDRESS_ENTERED_MANUALLY: 0 96%, 1 4%

BUSINESS_TYPE: Food_and_Beverage_Service 33%, Beauty_Services 10%, Financial_and_Legal_Services 9%, Consumables_Retail 9%, Health_Services 8%, Specialized_Services 6%, NA 6%, Specialized_Retail 6%, Apparel_and_Wearables_Retail 4%, Automotive 2%, Entertainment_and_Cultural_Ser 2%, Parking 2%

VACANT: occupied active 89%, vacant 8%, occupied inactive 3%, NA 0%

WINDOW_SIZE: Large windows, or full glass s 57%, Medium sized windows 26%, No windows, or small windows 13%, NA 4%

BUSINESS_SIZE: Small - like a corner store 65%, Medium - like a chain pharmacy 25%, Large - like a supermarket 8%, NA 2%, Extra Large - like a big box s 1%

FLOOR_NUMBER: 1st Floor 93%, Basement 4%, 2nd Floor or Higher 2%, NA 2%

MULTIPLE_FLOORS: NA 95%, Yes 5%

BUILDING_TYPE: Multi-story building 66%, One story building, not detach 24%, Detached building 7%, NA 2%, Big box or warehouse 1%, other 0%

FACING_DIRECTION: Faces sidewalk or pedestrian a 94%, Business faces a parking lot 3%, NA 1%, Business is inside a building 1%, Business faces an alleyway 0%, other 0%

OWN_PARKING_LOT: No 86%, Yes 10%, Not sure 2%, NA 2%

LOADING_DOCK: No 91%, Not sure 3%, Yes 3%, NA 2%

ART: No 97%, Yes 2%, NA 1%

ART_STATE: NA 98%, Mural is in great shape 1%, Mural is showing signs of wear 1%, Mural is badly damaged or cove 0%

ACCESS_INFO: No 89%, Yes 6%, NA 3%, Not sure 2%

DOOR_OPEN_BUTTON: No 89%, Yes 6%, NA 3%, Not sure 2%

ADA_RAMP: No 84%, Yes 12%, NA 2%, Not sure 2%

FLAT_ENTRANCE: Yes 55%, No 41%, NA 2%, Not sure 1%

CURRENT_STATE: NA 93%, About move in ready 5%, Visible Disrepair 1%, Looks particularly new or read 1%

BOARDED_UP: NA 89%, No 9%, Yes 2%

UNDER_CONSTRUCTION: NA 89%, No 9%, Yes 2%

ACTIVE_LEASE: NA 92%, Yes 4%, No 4%, Not sure 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| ID | id | 2.6K | 0 | 2634 14; 2633 14; 2632 14; 2631 14 |
| BUSINESS_NAME | who | 2.2K | 0 | NA 307; Bank of America 16; Stanhope Garage 14; Citizens 13 |
| ADDRESS | other | 2.1K | 0 | NA 75; 200 Faneuil Hall Marketpl 35; 100 Hanover St, BOSTON, M 26; 315 Centre St, BOSTON, MA 18 |
| ADDRESS_ENTERED_MANUALLY | category | 2 | 0 | 0 2.5K; 1 103 |
| X_COORD | amount | 1.6K | 5 | -70.92373016 48; -71.0547975 35; -71.057538 29; -71.0564805 18 |
| Y_COORD | amount | 1.5K | 5 | 42.35245853 48; 42.36021 35; 42.362235 29; 42.353154 17 |
| BUSINESS_TYPE | category | 47 | 0 | Food_and_Beverage_Service 819; Beauty_Services 243; Financial_and_Legal_Servi 231; Consumables_Retail 218 |
| BUSINESS_SUBTYPE | who | 319 | 241 | Sit_down_restaurant 306; Cafe/Smoothie/beverage_sh 144; Takeout_with_seating 126; other 108 |
| VACANT | category | 4 | 0 | occupied active 2.3K; vacant 219; occupied inactive 72; NA 2 |
| WINDOW_SIZE | category | 4 | 0 | Large windows, or full gl 1.5K; Medium sized windows 685; No windows, or small wind 342; NA 104 |
| BUSINESS_SIZE | category | 5 | 0 | Small - like a corner sto 1.7K; Medium - like a chain pha 661; Large - like a supermarke 201; NA 42 |
| FLOOR_NUMBER | category | 4 | 0 | 1st Floor 2.5K; Basement 94; 2nd Floor or Higher 46; NA 40 |
| MULTIPLE_FLOORS | category | 2 | 0 | NA 2.5K; Yes 121 |
| BUILDING_TYPE | category | 6 | 0 | Multi-story building 1.7K; One story building, not d 628; Detached building 174; NA 56 |
| FACING_DIRECTION | category | 6 | 0 | Faces sidewalk or pedestr 2.5K; Business faces a parking  83; NA 35; Business is inside a buil 22 |
| OWN_PARKING_LOT | category | 4 | 0 | No 2.3K; Yes 262; Not sure 52; NA 50 |
| LOADING_DOCK | category | 4 | 0 | No 2.4K; Not sure 90; Yes 85; NA 58 |
| ART | category | 3 | 0 | No 2.5K; Yes 58; NA 33 |
| ART_STATE | category | 4 | 0 | NA 2.6K; Mural is in great shape 37; Mural is showing signs of 20; Mural is badly damaged or 1 |
| ACCESS_INFO | category | 4 | 0 | No 2.3K; Yes 167; NA 77; Not sure 44 |
| DOOR_OPEN_BUTTON | category | 4 | 0 | No 2.4K; Yes 160; NA 66; Not sure 56 |
| ADA_RAMP | category | 4 | 0 | No 2.2K; Yes 315; NA 59; Not sure 47 |
| FLAT_ENTRANCE | category | 4 | 0 | Yes 1.5K; No 1.1K; NA 56; Not sure 35 |
| CURRENT_STATE | category | 4 | 0 | NA 2.4K; About move in ready 141; Visible Disrepair 31; Looks particularly new or 25 |
| BOARDED_UP | category | 3 | 0 | NA 2.3K; No 232; Yes 54 |
| UNDER_CONSTRUCTION | category | 3 | 0 | NA 2.3K; No 237; Yes 54 |
| ACTIVE_LEASE | category | 4 | 0 | NA 2.4K; Yes 106; No 106; Not sure 6 |
| CREATION_DATE | date | 2.1K | 0 | 2025-08-11T12:57:00 15; 2025-08-06T13:24:00 15; 2025-08-21T15:01:00 14; 2025-08-21T13:24:00 14 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:28:36.89013 2.6K |
| SOURCE_RUN_ID | audit | 1 | 0 | f54de39d-3d6e-472a-8e6d-c 2.6K |
| SRC_SHA256 | who | 1 | 0 | 782edd91101796721c25a8df8 2.6K |
