# PORTAL_ARC_OPEN_DATA_DC_E28C8C471A

rows 83  columns 50  scan 4.1s

roles: amount 3, audit 2, category 28, date 4, empty 5, other 6, who 3

## when

EFFECTIVE_DATE
  2018         4  ##
  2019         1  #
  2020         1  #
  2021        53  ##############################
  2022        17  ##########

ORIGINAL_ISSUE_DATE
  1974         1  ##
  1976        15  ##############################
  1995         1  ##
  1996         1  ##
  2000         1  ##
  2004         1  ##
  2015        10  ####################
  2016         9  ##################
  2017         2  ####
  2018         8  ################
  2019         1  ##
  2020        11  ######################
  2021        12  ########################
  2022         3  ######

COVERAGE_EXPIRATION
  2023         5  ###
  2025         1  #
  2026        57  ##############################
  2027        13  #######

INGESTED_AT
  2026        83  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 83 | 38.81 | 38.87 | 38.96 | 38.96 | 3.2K |
| LONGITUDE | 83 | -77.11 | -77.01 | -76.96 | -76.94 | -6.4K |
| PRIMARY_SIC | 73 | 3.0K | 4.5K | 8.7K | 8.7K | 374.8K |

## who

FACILITY_NAME by rows
        12  Washington Navy Yard
         7  nan
         4  RONALD REAGAN WASHINGTON NATIONAL AIRPORT
         4  Joint Base Anacostia-Bolling
         1  Ft Totten Fuel Site
         1  Former General Services Administration West Heating Plant
         1  Southwest Bus Terminal
         1  VIRGINIA CONCRETE - Vulcan SWDC Plant
         1  Blue Plains Impound Lot
         1  Washington Aqueduct
         1  2000 Adams Place NE
         1  SUPERIOR CONCRETE MATERIALS INC.
         1  DDOT Streetcar Car Barn Site
         1  AMERICAN AIRLINES
         1  EAST POTOMAC MAINTENANCE FACILITY
         1  SHEPHERD PARKWAY BUS DIVISION
         1  Delta Air Lines Inc.
         1  SOUTHWEST AIRLINES CO.
         1  BLADENSBURG BUS FACILITY
         1  Capital Asphalt

FACILITY_NAME by dollars
      466.44       12 rows  Washington Navy Yard
      271.74        7 rows  nan
      155.42        4 rows  RONALD REAGAN WASHINGTON NATIONAL AIRPORT
      155.40        4 rows  Joint Base Anacostia-Bolling
       38.96        1 rows  ROCK CREEK PARK - MAINTENANCE YARD
       38.96        1 rows  WESTERN BUS DIVISION
       38.95        1 rows  Aggregate Industries
       38.95        1 rows  Fort Reno Salt Storage Facility
       38.95        1 rows  SWMA Waste/Recycling Transfer Facility
       38.95        1 rows  SWMA, SACD Leaf Transfer Station
       38.95        1 rows  Ft Totten Fuel Site
       38.95        1 rows  DDOT Farragut Street and Bridge Maintenance Facility
       38.94        1 rows  2nd District Fuel Site
       38.94        1 rows  Washington Aqueduct
       38.92        1 rows  FIRST VEHICLE SERVICES
       38.92        1 rows  2000 Adams Place NE
       38.92        1 rows  Rodgers Brothers Custodial Services, Inc.
       38.92        1 rows  DDOT W Street and Bridge Maintenance Facility
       38.92        1 rows  Adams Pl Fuel Site
       38.92        1 rows  AMTRAK IVY CITY YARD

FACILITY_ADDRESS_1 by rows
        12  1411 Parsons Ave SE
         7  nan
         4  20 MacDill Blvd SW
         2  1 AVIATION CIRCLE
         1  4902 Bates Rd NE
         1  5001 Fort Totten Drive NE
         1  2860 South Capitol Street SE
         1  2400 East Capitol St NE
         1  3 DC VILLAGE LANE SW
         1  1 AVIATION CIRCLE, TERMINAL A
         1  1735 15th Street N.E.
         1  100 42nd St NE
         1  4901 Shepherd Parkway SW
         1  RONALD REAGAN WASHINGTON NATIONAL AIRPORT
         1  Base 537
         1  2200 Adams Pl NE
         1  1400 Mississippi Ave SE
         1  550 Water St SW
         1  3400 Benning Road 
         1  5000 Shepherd Pkwy SW

FACILITY_ADDRESS_1 by dollars
      466.44       12 rows  1411 Parsons Ave SE
      271.74        7 rows  nan
      155.40        4 rows  20 MacDill Blvd SW
       77.72        2 rows  1 AVIATION CIRCLE
       38.96        1 rows  5000 GLOVER ROAD NW
       38.96        1 rows  5230 WISCONSIN AVENUE NW
       38.95        1 rows  3865 Fort Reno Drive, NW
       38.95        1 rows  414 Farragut Street NE
       38.95        1 rows  3865 Fort Drive, NW
       38.95        1 rows  4900 John McCormack Dr, NE
       38.95        1 rows  4902 Bates Rd NE
       38.95        1 rows  5001 Fort Totten Drive NE
       38.94        1 rows  2900 MacArthur Boulevard NW
       38.94        1 rows  3320 Idaho Ave NW
       38.92        1 rows  1403 W street NE
       38.92        1 rows  1401 W STREET, N. E.
       38.92        1 rows  2200 Adams Pl NE
       38.92        1 rows  2175 WEST VIRGINIA AVENUE N.E.
       38.92        1 rows  2000 Adams Place NE
       38.92        1 rows  2225 Lawrence Ave NE

SRC_SHA256 by rows
        83  150bdf0fbe312be39f0dee82607d09b9a6c92ba4b088f82511674d12bd6cddba

SRC_SHA256 by dollars
        3.2K       83 rows  150bdf0fbe312be39f0dee82607d09b9a6c92ba4b088f82511674d12bd6c

## who x when

FACILITY_NAME by ORIGINAL_ISSUE_DATE, dollars = LATITUDE
  2000 Adams Place NE                       2020:38.92
  2nd District Fuel Site                    2018:38.94
  AMERICAN AIRLINES                         2015:38.86
  Aggregate Industries                      1996:38.95
  BLADENSBURG BUS FACILITY                  2015:38.92
  Blue Plains Impound Lot                   2020:38.81
  Capital Asphalt                           2021:38.81
  DDOT Farragut Street and Bridge Maintena  2021:38.95
  DDOT Streetcar Car Barn Site              2021:38.90
  Delta Air Lines Inc.                      2016:38.86
  EAST POTOMAC MAINTENANCE FACILITY         2021:38.88
  FIRST VEHICLE SERVICES                    2016:38.92
  Former General Services Administration W  1976:38.90
  Fort Reno Salt Storage Facility           2020:38.95
  Ft Totten Fuel Site                       2018:38.95
  Joint Base Anacostia-Bolling              2016:38.85 2021:116.55
  ROCK CREEK PARK - MAINTENANCE YARD        2016:38.96
  RONALD REAGAN WASHINGTON NATIONAL AIRPOR  2015:77.70 2016:77.72
  Rodgers Brothers Custodial Services, Inc  2022:38.92
  SHEPHERD PARKWAY BUS DIVISION             2018:38.82
  SOUTHWEST AIRLINES CO.                    2015:38.85
  SUPERIOR CONCRETE MATERIALS INC.          2017:38.87
  SWMA Waste/Recycling Transfer Facility    2020:38.95
  SWMA, SACD Leaf Transfer Station          2020:38.95
  Southwest Bus Terminal                    2019:38.81
  VIRGINIA CONCRETE - Vulcan SWDC Plant     2015:38.87
  WESTERN BUS DIVISION                      2015:38.96
  Washington Aqueduct                       1976:38.94
  Washington Navy Yard                      1976:466.44

FACILITY_ADDRESS_1 by ORIGINAL_ISSUE_DATE, dollars = LATITUDE
  1 AVIATION CIRCLE                         2016:77.72
  1 AVIATION CIRCLE, TERMINAL A             2015:38.85
  100 42nd St NE                            2018:38.89
  1400 Mississippi Ave SE                   2000:38.84
  1401 W STREET, N. E.                      2016:38.92
  1403 W street NE                          2021:38.92
  1411 Parsons Ave SE                       1976:466.44
  1735 15th Street N.E.                     2020:38.91
  20 MacDill Blvd SW                        2016:38.85 2021:116.55
  2200 Adams Pl NE                          2018:38.92
  2400 East Capitol St NE                   2020:38.89
  2860 South Capitol Street SE              2021:38.86
  2900 MacArthur Boulevard NW               1976:38.94
  3 DC VILLAGE LANE SW                      2018:38.81
  3320 Idaho Ave NW                         2018:38.94
  3400 Benning Road                         1976:38.90
  3865 Fort Drive, NW                       2020:38.95
  3865 Fort Reno Drive, NW                  2020:38.95
  414 Farragut Street NE                    2021:38.95
  4900 John McCormack Dr, NE                2020:38.95
  4901 Shepherd Parkway SW                  2021:38.81
  4902 Bates Rd NE                          2018:38.95
  5000 GLOVER ROAD NW                       2016:38.96
  5000 Shepherd Pkwy SW                     2022:38.81
  5001 Fort Totten Drive NE                 1996:38.95
  5230 WISCONSIN AVENUE NW                  2015:38.96
  550 Water St SW                           2020:38.87
  Base 537                                  2021:38.84
  RONALD REAGAN WASHINGTON NATIONAL AIRPOR  2015:38.86

## what

DOEE_REVIEW_NOTES: MS4 52%, Should be in Virginia 17%, Should be MS4 9%, Federal Faciility; EPA to Veri 6%, not MS4 3%, Should not be MS4 3%, Site in CSS.  Discharge (Outfa 2%, MS4 (Outfall MS4-01E) 2%, MS4 (Outfall CSO-15H) 2%, MS4 (Outfall CSO-15G) 2%, MS4 (Outfall CSO-14F) 2%, MS4 (Outfall 014) 2%

EPA_STATED_DISCHARGE_TO_MS4: Yes 40%, nan 34%, No 27%

PERMIT_NAME: nan 66%, Washington Navy Yard 14%, Mirant Potomac River L.L.C. (P 8%, World War II Memorial 1%, JFK Center for Performing Arts 1%, WMATA Minnesota Avenue Pumping 1%, Bardon Inc (Formerly Super Con 1%, Lincoln Memorial Reflecting Po 1%, Georgetown 29K Acquisition (Fo 1%, D.C. WASA (Blue Plains) 1%, PEPCO Environment Management S 1%, Washington Aqueduct 1%

TYPE_OF_FACILITY: MSGP 66%, NPDES Core 34%

SUBTYPE: nan 66%, Minor 23%, Major 11%

OPERATOR_NAME: Washington Navy Yard Naval Sup 24%, PERMIT TERMINATED 14%, District Department of Public  14%, District of Columbia Departmen 10%, Government of the District of  10%, United States Air Force 8%, WMATA 6%, National Park Service, Nationa 4%, District of Columbia Departmen 4%, Smithsonian  2%, Washington Metropolitan Area T 2%, Aggregate Industries 2%

OPERATOR_POC: Jasmine Tyson/Molly Bergren/Ju 26%, nan 15%, Marlon Wright 13%, Jason Nordt 13%, Ryan LeBlanc 9%, Claire Fox 7%, Brittany Grouge/Catherine Dewe 4%, John P Thomas 4%, Carissa Faroughi / Udit H. Pat 2%, Basil Borisov / Claire Fox 2%, James Carroll 2%, Christina Lewis 2%

OPERATOR_EMAIL: jasmin.n.dunhamtyson.civ@us.na 24%, nan 14%, marlon.wright@dc.gov 14%, jason.nordt@dc.gov 12%, ryan.leblanc@us.af.mil 8%, cfox@wmata.com 6%, john.pthomas@dc.gov 6%, brittany_grouge@nps.gov / cath 4%, kristen.audette@dc.gov 4%, CIFaroughi@kennedy-center.org  2%, bborisov@wmata.com / cfox@wmat 2%, james.carroll@lafargeholcim.co 2%

OPERATOR_ADDRESS_1: 1411 Parsons Ave SE Suite 200 24%, nan 16%, 2000 14th St NW 12%, 2000 14TH STREET, NW 6TH FLR 10%, 370 Brookley Ave SW 8%, 900 Ohio Drive SW 6%, 3500 Pennsy Drive 6%, 2000 14th Street NW 6th Floor 6%, 2000 14th St 4%, 250 M Street SE 4%, 2700 F Street NW 2%, 1400 Mississippi Ave SE 2%

OPERATOR_ADDRESS_2: nan 92%, C-172 4%, Suite 450 1%, Floor 2 1%, Suite E 1%, 8th Floor 1%

OPERATOR_CITY: Washington 56%, WASHINGTON 12%, nan 10%, Washington  6%, Washington DC 5%, Landover 4%, Malvern 1%, Memphis 1%, Herndon 1%, Jacksonville 1%, Washington` 1%, Knoxville 1%

OPERATOR_STATE: DC 55%, D.C. 24%, nan 10%, MD 4%, TN 2%, PA 1%, VA 1%, FL 1%, IL 1%

OPERATOR_ZIPCODE: 20009 23%, 20374 17%, 20032 11%, nan 11%, 20001 8%, 20003 7%, 20024 6%, 20785 4%, 20018 4%, 20011 3%, 20001-4901 3%, 20002 3%

OWNER_NAME: nan 82%, NAVFAC 14%, Bardon, Inc 1%, Georgetown 29K Acquisition, LL 1%, Pepco Electric Power Company 1%

OWNER_ADDRESS_1: nan 83%, 9500 MacArthur Blvd. 14%, 3500 Pennsy Dr Building C 1%, 500 Park Avenue, 10th Floor 1%

OWNER_CITY: nan 83%, West Bethesda 14%, Hyattsville 1%, New York 1%

OWNER_STATE: nan 83%, MD 16%, NY 1%

OWNER_ZIPCODE: nan 83%, 20718.0 14%, 22078.0 1%, 100652.0 1%

FACILITY_ADDRESS_2: nan 89%, RONALD REAGAN WASHINGTON NATIO 5%, BLDG B, 2ND FLOOR 1%, SOUTHWEST AIRLINES @ REAGAN NA 1%, RONALD REAGAN NATIONAL AIRPORT 1%, 901 Air Cargo Rd, Bay 102, Rm  1%, RONALD REAGAN WASHINGTON NATIO 1%

FACILITY_CITY: Washington 59%, WASHINGTON 33%, Washington DC 5%, Washington  2%, Washington D.C. 1%

FACILITY_ZIPCODE: 20032 20%, 20374 16%, 20001 11%, nan 9%, 20018 8%, 20024 7%, 20016 7%, 20002 7%, 20019 5%, 20003 5%, 20011 4%, 20020 3%

INACTIVE_UNSTAFFED: No 65%, nan 34%, Yes 1%

EXPOSED_TO_STORMWATER: nan 99%, No 1%

PRIMARY_SECTOR: P 40%, Minor 23%, S 14%, nan 8%, E 4%, Q 2%, N 2%, Major  1%, Major 1%, D 1%, M 1%, R 1%

SUBMISSION_STATUS: Approved 66%, nan 34%

SUBMISSION_TYPE: nan 34%, Renewal 33%, Change 20%, New 8%, Reapplication 5%

COVERAGE_TYPE: General Permit 66%, nan 34%

COVERAGE_STATUS: Active 66%, Current 25%, nan 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 83 | 0 | 83 1; 82 1; 81 1; 80 1 |
| OBJ_ID | other | 67 | 0 | 64 12; 59 7; 66 1; 65 1 |
| DOEE_REVIEW_NOTES | category | 30 | 0 | MS4 34; Should be in Virginia 11; Should be MS4 6; Federal Faciility; EPA to 4 |
| EPA_STATED_DISCHARGE_TO_MS4 | category | 3 | 0 | Yes 33; nan 28; No 22 |
| NPDES_ID | other | 67 | 0 | DC0000141 12; DC0022004 7; DC0000345 1; DC0000248 1 |
| PERMIT_NAME | category | 12 | 0 | nan 55; Washington Navy Yard 12; Mirant Potomac River L.L. 7; World War II Memorial 1 |
| TYPE_OF_FACILITY | category | 2 | 0 | MSGP 55; NPDES Core 28 |
| SUBTYPE | category | 3 | 0 | nan 55; Minor 19; Major 9 |
| OPERATOR_NAME | category | 45 | 0 | Washington Navy Yard Nava 12; PERMIT TERMINATED 7; District Department of Pu 7; District of Columbia Depa 5 |
| OPERATOR_POC | category | 49 | 0 | Jasmine Tyson/Molly Bergr 12; nan 7; Marlon Wright 6; Jason Nordt 6 |
| OPERATOR_EMAIL | category | 46 | 0 | jasmin.n.dunhamtyson.civ@ 12; nan 7; marlon.wright@dc.gov 7; jason.nordt@dc.gov 6 |
| OPERATOR_ADDRESS_1 | category | 45 | 0 | 1411 Parsons Ave SE Suite 12; nan 8; 2000 14th St NW 6; 2000 14TH STREET, NW 6TH  5 |
| OPERATOR_ADDRESS_2 | category | 5 | 0 | nan 76; C-172 3; Suite 450 1; Floor 2 1 |
| OPERATOR_CITY | category | 13 | 0 | Washington 46; WASHINGTON 10; nan 8; Washington  5 |
| OPERATOR_STATE | category | 9 | 0 | DC 46; D.C. 20; nan 8; MD 3 |
| OPERATOR_ZIPCODE | category | 24 | 0 | 20009 16; 20374 12; 20032 8; nan 8 |
| OWNER_NAME | category | 5 | 0 | nan 68; NAVFAC 12; Bardon, Inc 1; Georgetown 29K Acquisitio 1 |
| OWNER_POC | empty | 1 | 83 |  |
| OWNER_EMAIL | empty | 1 | 83 |  |
| OWNER_ADDRESS_1 | category | 4 | 0 | nan 69; 9500 MacArthur Blvd. 12; 3500 Pennsy Dr Building C 1; 500 Park Avenue, 10th Flo 1 |
| OWNER_ADDRESS_2 | empty | 1 | 83 |  |
| OWNER_CITY | category | 4 | 0 | nan 69; West Bethesda 12; Hyattsville 1; New York 1 |
| OWNER_STATE | category | 3 | 0 | nan 69; MD 13; NY 1 |
| OWNER_ZIPCODE | category | 4 | 0 | nan 69; 20718.0 12; 22078.0 1; 100652.0 1 |
| FACILITY_NAME | who | 58 | 0 | Washington Navy Yard 12; nan 7; Joint Base Anacostia-Boll 4; RONALD REAGAN WASHINGTON  4 |
| FACILITY_POC | empty | 1 | 83 |  |
| FACILITY_POC_EMAIL | empty | 1 | 83 |  |
| FACILITY_ADDRESS_1 | who | 62 | 0 | 1411 Parsons Ave SE 12; nan 7; 20 MacDill Blvd SW 4; 1 AVIATION CIRCLE 2 |
| FACILITY_ADDRESS_2 | category | 7 | 0 | nan 74; RONALD REAGAN WASHINGTON  4; BLDG B, 2ND FLOOR 1; SOUTHWEST AIRLINES @ REAG 1 |
| FACILITY_CITY | category | 5 | 0 | Washington 49; WASHINGTON 27; Washington DC 4; Washington  2 |
| FACILITY_STATE | other | 1 | 0 | DC 83 |
| FACILITY_ZIPCODE | category | 18 | 0 | 20032 15; 20374 12; 20001 8; nan 7 |
| LATITUDE | amount | 72 | 0 | 38.8635 5; 38.8459 4; 38.87167 3; 38.82056 3 |
| LONGITUDE | amount | 70 | 0 | -77.0425 5; -77.04028 4; -77.015 4; -76.99806 2 |
| INACTIVE_UNSTAFFED | category | 3 | 0 | No 54; nan 28; Yes 1 |
| EXPOSED_TO_STORMWATER | category | 2 | 0 | nan 82; No 1 |
| PRIMARY_SECTOR | category | 12 | 0 | P 33; Minor 19; S 12; nan 7 |
| PRIMARY_SIC | amount | 25 | 0 | 8744.0 12; nan 10; 5171.0 7; 4225.0 6 |
| REGION | other | 1 | 0 | 3 83 |
| SUBMISSION_STATUS | category | 2 | 0 | Approved 55; nan 28 |
| SUBMISSION_TYPE | category | 5 | 0 | nan 28; Renewal 27; Change 17; New 7 |
| COVERAGE_TYPE | category | 2 | 0 | General Permit 55; nan 28 |
| COVERAGE_STATUS | category | 3 | 0 | Active 55; Current 21; nan 7 |
| EFFECTIVE_DATE | date | 44 | 0 | 1643673600000.0 12; 1627171200000.0 9; nan 7; 1625788800000.0 4 |
| ORIGINAL_ISSUE_DATE | date | 51 | 0 | 209952000000.0 12; nan 7; 1536105600000.0 5; 1443657600000.0 3 |
| COVERAGE_EXPIRATION | date | 10 | 0 | 1772236800000.0 55; 1801353600000.0 12; nan 7; 1688256000000.0 2 |
| GEOMETRY | other | 75 | 0 | {"type": "Point", "coordi 5; {"type": "Point", "coordi 4; {"type": "Point", "coordi 3; {"type": "Point", "coordi 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:19:00.11262 83 |
| SOURCE_RUN_ID | audit | 1 | 0 | 860a76df-36d5-4fd9-bad9-9 83 |
| SRC_SHA256 | who | 1 | 0 | 150bdf0fbe312be39f0dee826 83 |
