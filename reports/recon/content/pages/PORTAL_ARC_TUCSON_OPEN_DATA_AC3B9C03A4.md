# PORTAL_ARC_TUCSON_OPEN_DATA_AC3B9C03A4

rows 2.0K  columns 29  scan 5.1s

roles: audit 2, category 10, date 1, id 3, other 6, who 8

## when

INGESTED_AT
  2026      2.0K  ##############################

## who

CONAME by rows
        65  ATM
        18  AmeriGas Propane Exchange
        17  Redbox
        13  Circle K
        10  Blue Rhino
         9  Western Union Agent Location
         6  Cricket Wireless Authorized Retailer
         6  Starbucks
         5  Dollar General
         5  Coinstar
         5  Family Dollar
         4  Walgreens
         4  Taco Bell
         4  Minute Key
         4  U-Haul Neighborhood Dealer
         4  Subway
         4  Raytheon Co
         3  AutoZone
         3  Dollar Tree
         3  Edward Jones

HQNAME by rows
        21  Walmart U.S. Division
        18  AmeriGas Propane, Inc
        17  Redbox Automated Retail LLC
        14  Circle K Stores Inc
        10  Blue Rhino Global Sourcing, Inc
         9  The Western Union Company
         6  Starbucks Corporation
         6  Cricket Wireless LLC
         5  Dollar General Corporation
         5  Farmers Group, Inc
         5  Family Dollar Stores, Inc
         5  Coinstar, LLC
         4  U-Haul International, Inc
         4  Franchise World Headquarters, LLC
         4  US Indian Affairs Bureau
         4  Food City
         4  Safeway Inc
         4  Raytheon Company
         4  Walgreens Boots Alliance, Inc
         4  Taco Bell Corp

STATE_NAME by rows
      2.0K  Arizona

NAICS by rows
       123  72251117
        73  99999004
        65  52211001
        62  81311008
        40  81211202
        36  81111104
        31  52421001
        28  61111007
        28  45721017
        24  62111107
        23  44513101
        21  62149301
        20  53121003
        19  51711214
        17  53228207
        17  53111002
        16  53113001
        16  62121003
        15  45521903
        14  44134001

## who x when

CONAME by INGESTED_AT  LOAD STAMP, not an event date
  ATM                                       2026:65
  AmeriGas Propane Exchange                 2026:18
  AutoZone                                  2026:3
  Blue Rhino                                2026:10
  Circle K                                  2026:13
  Coinstar                                  2026:5
  Cricket Wireless Authorized Retailer      2026:6
  Dollar General                            2026:5
  Dollar Tree                               2026:3
  Edward Jones                              2026:3
  Family Dollar                             2026:5
  Minute Key                                2026:4
  Raytheon Co                               2026:4
  Redbox                                    2026:17
  Starbucks                                 2026:6
  Subway                                    2026:4
  Taco Bell                                 2026:4
  U-Haul Neighborhood Dealer                2026:4
  Walgreens                                 2026:4
  Western Union Agent Location              2026:9

HQNAME by INGESTED_AT  LOAD STAMP, not an event date
  AmeriGas Propane, Inc                     2026:18
  Blue Rhino Global Sourcing, Inc           2026:10
  Circle K Stores Inc                       2026:14
  Coinstar, LLC                             2026:5
  Cricket Wireless LLC                      2026:6
  Dollar General Corporation                2026:5
  Family Dollar Stores, Inc                 2026:5
  Farmers Group, Inc                        2026:5
  Food City                                 2026:4
  Franchise World Headquarters, LLC         2026:4
  Raytheon Company                          2026:4
  Redbox Automated Retail LLC               2026:17
  Safeway Inc                               2026:4
  Starbucks Corporation                     2026:6
  Taco Bell Corp                            2026:4
  The Western Union Company                 2026:9
  U-Haul International, Inc                 2026:4
  US Indian Affairs Bureau                  2026:4
  Walgreens Boots Alliance, Inc             2026:4
  Walmart U.S. Division                     2026:21

## what

CITY: Tucson 60%, Green Valley 33%, Sahuarita 4%, South Tucson 3%, Amado 0%

ZIP: 85706 31%, 85614 26%, 85713 12%, 85714 9%, 85622 8%, 85629 4%, 85756 4%, 85746 3%, 85757 2%, 85735 2%, 85736 1%, 85723 1%

AFFILIATE: Cricket Wireless Authorized Re 20%, Ace 13%, Freeway 10%, Boys & Girls Club 10%, Parts Plus Car Care Center 10%, UPS Access Point Location 7%, CrossFit 7%, Verizon Authorized Retailer,Vi 7%, American Legion 7%, AutoService Experts 7%, Metro by T-Mobile Authorized R 3%

BRAND: AMEX ATM 46%, STAR,AMEX ATM 19%, Farmers Insurance 7%, Citibank ATM,AMEX ATM 6%, American Family 4%, Valero 3%, Progressive Insurance 3%, STAR 3%, Shell 3%, Firestone 3%, Chevron 3%

LOC_CONF: Very High 96%, High 3%, Medium 1%, Low 1%

PLACETYPE: Independent 68%, Branch 25%, Kiosk 6%, Headquarters 1%

PROFSPEC: General Dentistry 30%, Internal Medicine 15%, Gastroenterology 11%, Certified Public Accounting 11%, Internal Medicine,Osteopathy ( 7%, Small Animals 7%, Family Practice 4%, Radiology 4%, Dental Periodontics 4%, Orthopedic Surgery,Pediatrics, 4%, Internal Medicine,Anesthesiolo 4%

SQFOOTAGE: 1 - 1,499 30%, 1,500 - 2,499 20%, 2,500 - 4,999 20%, 5,000 - 9,999 11%, 10,000 - 19,999 6%, 20,000 - 39,999 5%, 40,000 - 99,999 4%, 100,000+ 3%

LOC_NAME: PointAddress 96%, StreetAddress 2%, POI 1%, StreetName 1%, Postal 1%, StreetAddressExt 0%, StreetInt 0%

JURISDICTION: TUCSON 49%, UNINCORPORATED PIMA COUNTY 39%, SAHUARITA 12%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| JOIN_COUNT | other | 1 | 0 | 1 2.0K |
| TARGET_FID | id | 2.0K | 0 | 2000 10; 1999 10; 1998 10; 1997 10 |
| CONAME | who | 1.7K | 0 | ATM 65; AmeriGas Propane Exchange 27; Redbox 19; Western Union Agent Locat 16 |
| STREET | who | 386 | 29 | South Nogales Highway 111; South 12Th Avenue 106; West Continental Road 105; South 6Th Avenue 100 |
| CITY | category | 5 | 0 | Tucson 1.2K; Green Valley 659; Sahuarita 88; South Tucson 53 |
| STATE_NAME | who | 1 | 0 | Arizona 2.0K |
| STATE | other | 1 | 0 | AZ 2.0K |
| ZIP | category | 20 | 3 | 85706 611; 85614 506; 85713 233; 85714 171 |
| ZIP4 | other | 983 | 104 | 6508 20; 5284 18; 3555 18; 1165 17 |
| NAICS | who | 587 | 0 | 72251117 123; 99999004 73; 52211001 65; 81311008 62 |
| SIC | who | 579 | 0 | 581208 123; 999977 73; 602103 65; 866107 62 |
| AFFILIATE | category | 26 | 2.0K | Cricket Wireless Authoriz 6; Ace 4; Freeway 3; Boys & Girls Club 3 |
| BRAND | category | 35 | 1.9K | AMEX ATM 32; STAR,AMEX ATM 13; Farmers Insurance 5; Citibank ATM,AMEX ATM 4 |
| HQNAME | who | 322 | 1.4K | Walmart U.S. Division 21; AmeriGas Propane, Inc 19; Redbox Automated Retail L 17; Circle K Stores Inc 14 |
| LOC_CONF | category | 4 | 0 | Very High 1.9K; High 61; Medium 17; Low 11 |
| PLACETYPE | category | 4 | 0 | Independent 1.4K; Branch 496; Kiosk 127; Headquarters 13 |
| PROFSPEC | category | 36 | 1.9K | General Dentistry 8; Internal Medicine 4; Gastroenterology 3; Certified Public Accounti 3 |
| SQFOOTAGE | category | 9 | 168 | 1 - 1,499 547; 1,500 - 2,499 374; 2,500 - 4,999 369; 5,000 - 9,999 196 |
| EMPNUM | other | 83 | 0 | 3 277; 2 251; 0 216; 4 171 |
| SALESVOL | other | 688 | 0 | 0 522; 422000 39; 268000 20; 340000 18 |
| SOURCE | who | 1 | 0 | Data Axle 2.0K |
| ESRI_PID | id | 2.0K | 0 | 027ebf701144823ffe9607bd0 10; 39e366401c0a8b7a91f97092a 10; db335b3ee16f6989331af1a91 10; 77d0013df23da35618a7b9f1c 10 |
| LOC_NAME | category | 7 | 0 | PointAddress 1.9K; StreetAddress 43; POI 18; StreetName 15 |
| JURISDICTION | category | 3 | 0 | TUCSON 974; UNINCORPORATED PIMA COUNT 785; SAHUARITA 241 |
| GEOMETRY | other | 1.2K | 0 | {"type": "Point", "coordi 34; {"type": "Point", "coordi 20; {"type": "Point", "coordi 20; {"type": "Point", "coordi 18 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:32:50.16419 2.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 6ffdc348-67be-48f3-bf86-1 2.0K |
| SRC_SHA256 | who | 1 | 0 | 51a7568ec4f3f08aaed925467 2.0K |
