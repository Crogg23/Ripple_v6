# PORTAL_ARC_FORT_WORTH_OPEN_2259070522

rows 19  columns 20  scan 2.6s

roles: audit 2, category 12, date 4, other 1, who 2

## when

STARTDATE
  2004         1  ###############
  2007         2  ##############################
  2008         2  ##############################
  2009         2  ##############################
  2013         1  ###############

LASTEDITED
  2018        12  ##############################
  2021         2  #####
  2023         5  ############

SOURCEDATE
  2018        12  ##############################
  2021         2  #####
  2023         5  ############

INGESTED_AT
  2026        19  ##############################

## who

CITY by rows
        19  Fort Worth

SRC_SHA256 by rows
        19  206663cc10118ce5259d07d76239a39f08beab37e6c1f8151ce48d6a9428f626

## who x when

CITY by STARTDATE
  Fort Worth                                2004:1 2007:2 2008:2 2009:2 2013:1

SRC_SHA256 by STARTDATE
  206663cc10118ce5259d07d76239a39f08beab37  2004:1 2007:2 2008:2 2009:2 2013:1

## what

FID: 6612 8%, 6588 8%, 6069 8%, 3629 8%, 3593 8%, 3312 8%, 2762 8%, 2058 8%, 2001 8%, 1733 8%, 1013 8%, 986 8%

EMPNAME: Amazon Fullfillment Center 14%, Ben E Keith Beverages 14%, Amazon Air 7%, American Airlines Group 7%, Home Goods Distribution Center 7%, Amazon Fulfillment Center 7%, Alcon Laboratories 7%, Union Pacific Railroad 7%, Dyncorp International 7%, AT&T Wireless Distribution 7%, Burlington Northern Santa Fe R 7%, Lockheed Martin Corp 7%

EMPADDR: 301 Intermodal Pkwy 8%, 1 Skyview Dr 8%, 7601 Oak Grove Rd 8%, 4601 Gold Spike Dr 8%, 15201 Heritage Pkwy 8%, 700 Westport Pkwy 8%, 6201 S Fwy 8%, 5701 W Vickery Blvd 8%, 13500 Heritage Pkwy 8%, 13500 Independence Pkwy 8%, 2650 Lou Menk Dr 8%, 1 Lockheed Blvd 8%

EMPLOYEES: 1000 24%, 4000 12%, 1200 12%, 2000 6%, 3000 6%, 4500 6%, 900 6%, 4900 6%, 18700 6%, 1404 6%, 2500 6%, 2366 6%

NAICS: Retail Trade 47%, Wholesale Trade 21%, Transportation, Warehousing, P 16%, Manufacturing 16%

EMPID: 40867 8%, 39252 8%, 29825 8%, 8032 8%, 7987 8%, 7638 8%, 6706 8%, 5005 8%, 4856 8%, 4189 8%, 2421 8%, 2353 8%

MAILADDR: 301 Intermodal Pkwy, Haslet, T 8%, PO Box 619616, Dallas, TX 7526 8%, 770 Cochituate Rd, Framingham, 8%, 4601 Gold Spike Dr, Fort Worth 8%, 15201 Heritage Pkwy, Fort Wort 8%, 700 Westport Pkwy, Fort Worth, 8%, 6201 S Fwy, Fort Worth, TX 761 8%, 5701 W Vickery Blvd, Fort Wort 8%, 13500 Heritage Pkwy, Fort Wort 8%, 13500 Independence Pkwy, Fort  8%, 2650 Lou Menk Dr, Fort Worth,  8%, 1 Lockheed Blvd, Fort Worth, T 8%

MAILCITY: Fort Worth 84%, Haslet 5%, Dallas 5%, Framingham 5%

MAILZIP: 76177 29%, 76106 12%, 76155 6%, 01701 6%, 76134 6%, 76107 6%, 76131 6%, 76108 6%, 76102 6%, 76161 6%, 76140 6%, 76101 6%

FEATURENAM: Amazon Fulfillment Center 15%, Amazon Air 8%, American Airlines - Skyview 8 8%, Carter Park East Ph 3 8%, Amazon Fulfillment Center (Rai 8%, Alcon Laboratories Inc 8%, Union Pacific Railroad Davidso 8%, Dyncorp 8%, Alliance Gateway South 8%, Burlington Northern Santa Fe R 8%, Lockheed Martin Corp 8%, Ben E Keith 8%

TOP20RF: 0 63%, 1 37%

GEOMETRY: {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%, {"type": "Point", "coordinates 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FID | category | 19 | 0 | 6612 1; 6588 1; 6069 1; 3629 1 |
| EMPNAME | category | 17 | 0 | Amazon Fullfillment Cente 2; Ben E Keith Beverages 2; Amazon Air 1; American Airlines Group 1 |
| EMPADDR | category | 19 | 0 | 301 Intermodal Pkwy 1; 1 Skyview Dr 1; 7601 Oak Grove Rd 1; 4601 Gold Spike Dr 1 |
| EMPLOYEES | category | 14 | 0 | 1000 4; 4000 2; 1200 2; 2000 1 |
| NAICS | category | 4 | 0 | Retail Trade 9; Wholesale Trade 4; Transportation, Warehousi 3; Manufacturing 3 |
| STARTDATE | date | 9 | 0 | nan 11; 1370044800000.0 1; 1176768000000.0 1; 1101859200000.0 1 |
| LASTEDITED | date | 17 | 0 | 2/26/2018 2; 1/6/2023 2; 5/3/2023 1; 3/29/2023 1 |
| CITY | who | 1 | 0 | Fort Worth 19 |
| EMPID | category | 19 | 0 | 40867 1; 39252 1; 29825 1; 8032 1 |
| MAILADDR | category | 19 | 0 | 301 Intermodal Pkwy, Hasl 1; PO Box 619616, Dallas, TX 1; 770 Cochituate Rd, Framin 1; 4601 Gold Spike Dr, Fort  1 |
| MAILCITY | category | 4 | 0 | Fort Worth 16; Haslet 1; Dallas 1; Framingham 1 |
| MAILZIP | category | 14 | 0 | 76177 5; 76106 2; 76155 1; 01701 1 |
| SOURCEDATE | date | 17 | 0 | 1519603200000 2; 1672963200000 2; 1683072000000 1; 1680048000000 1 |
| FEATURENAM | category | 18 | 0 | Amazon Fulfillment Center 2; Amazon Air 1; American Airlines - Skyvi 1; Carter Park East Ph 3 1 |
| ACTIVITYSE | other | 1 | 0 | Basic 19 |
| TOP20RF | category | 2 | 0 | 0 12; 1 7 |
| GEOMETRY | category | 19 | 0 | {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:14:41.14120 19 |
| SOURCE_RUN_ID | audit | 1 | 0 | d1cce32a-ca90-4490-8e75-e 19 |
| SRC_SHA256 | who | 1 | 0 | 206663cc10118ce5259d07d76 19 |
