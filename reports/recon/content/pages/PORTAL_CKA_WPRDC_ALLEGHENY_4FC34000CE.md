# PORTAL_CKA_WPRDC_ALLEGHENY_4FC34000CE

rows 1.0K  columns 15  scan 3.8s

roles: amount 1, audit 2, category 3, date 2, id 1, other 3, who 4

## when

ISSUED_DATE
  2023      1.0K  ##############################

INGESTED_AT
  2026      1.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_PROJECT_VALUE | 1.0K | 0 | 11.8K | 5.21M | 106.43M | 340.20M |

## who

OWNER_NAME by rows
        20  ALLEGHENY COMMONS COMMUNITY PARTNERS LP
        14  CITY OF PITTSBURGH
        13  HRLP FOURTH AVENUE LLC
        11  ALLEGHENY COUNTY
        10  PRODUCE TERMINAL HOLDINGS LLC
         9  CARNEGIE MELLON UNIVERSITY
         9  BURROWS STREET TOWNHOUSES LLC
         9  BUNCHER COMPANY
         7  SPORTS AND EXHIBITION AUTHORITY OFPITTSBURGH AND ALLEGHENY COUNTY
         6  EAST LIBERTY SOUTH LIMITED PARTNERSHIP
         6  1900 FOURPENN LLC
         5  3250 LIBERTY OWNER LLC
         5  CRAWFORD JOHN LLC
         5  UPMC PRESBYTERIAN SHADYSIDE
         5  COSTELLO PROPERTIES LLC
         5  NORTH SHORE DEVELOPERS LP
         5  ACA CONCOURSE EAST UNIT 3 LLC
         4  RIDC MILL 19A
         4  GARDEN THEATER BLOCK LLC
         4  BIBLE CENTER CHURCH INC

OWNER_NAME by dollars
     106.47M        5 rows  UPMC PRESBYTERIAN SHADYSIDE
      27.19M        2 rows  ELIZABETH MAGEE HOSPITAL
      18.36M        1 rows  5803 CENTRE LLC
      18.02M        5 rows  3250 LIBERTY OWNER LLC
      17.93M        4 rows  UPMC MERCY
      12.75M        1 rows  ALLEGHENY COUNTY SANITARY AUTHORITY
       7.65M        4 rows  GARDEN THEATER BLOCK LLC
       7.50M        1 rows  HSRE-RPG FORBES AVENUE LLC
       7.28M        2 rows  810 W NORTH AVE ASSOCIATES LP
       6.39M        3 rows  327 NN LLC
       5.45M        4 rows  MERCY HOSPITAL OF PITTSBURGH
       5.37M        1 rows  INCORP TRUSTEES OF THE SALVATION ARMY INPA
       5.00M        1 rows  1717 FIFTH LLC
       4.73M        9 rows  BUNCHER COMPANY
       4.70M       13 rows  HRLP FOURTH AVENUE LLC
       4.20M        1 rows  MTP - 2700 S WATER STREET LLC
       4.00M        1 rows  PGC QALICB
       3.97M        4 rows  ALLEGHENY GENERAL HOSPITAL
       3.77M        3 rows  CARNEGIE INSTITUTE
       3.43M       14 rows  CITY OF PITTSBURGH

CONTRACTORS_NAME by rows
        61  null
        23  Hampton Mechanical, Inc.
        17  Renewal By Andersen LLC
        17  Window World of Pittsburgh LLC
        14  Richard Brandi
        12  Window Nation, LLC
        11  Gunton Corp
        11  Hanlon Electric Company
        10  Ryco Fire Protection Services LP
        10  William Santoro
        10  PE REAL ESTATE HOLDINGS LLC
        10  Mongiovi & Son Fire Protection
         9  Rycon Construction, Inc
         9  Clista Electric Inc
         9  Lang Electrical Contracting
         9  Grunau Company, Inc.
         8  Mascaro Construction Co LP
         8  Home Depot USA
         7  J.A. Sauer Heating & Air Conditioning
         7  Trinity Solar Inc

CONTRACTORS_NAME by dollars
     106.43M        1 rows  Whiting-Turner / P.J. Dick JV
      42.89M        9 rows  Rycon Construction, Inc
      21.01M        6 rows  Mistick Construction Company
      18.36M        1 rows  Al. Neyer LLC
      17.96M        1 rows  Residential Development & Construction Inc
      17.31M        4 rows  RuthRauff Sauer LLC
      12.75M        1 rows  Mike Coates Construction Co., Inc.
       7.50M        3 rows  Franjo Construction
       6.02M        4 rows  McKamish Inc
       5.47M        8 rows  Mascaro Construction Co LP
       5.37M        1 rows  Sota Construction Services
       4.83M        4 rows  Volpatt Construction Corporation
       4.16M        6 rows  A. Martini & Co Inc
       4.00M        1 rows  The Albert M. Higley Co., LLC
       3.37M        3 rows  Allegheny Construction Group, Inc
       2.44M        2 rows  Lugaila Mechanical Inc
       2.36M        3 rows  Matcon Diamond, Inc.
       2.16M        3 rows  City of Pittsburgh Permits, Licenses and Inspections
       2.03M        5 rows  Shannon Construction Company
       2.00M        2 rows  Burchick Construction Company, Inc.

NEIGHBORHOOD by rows
        64  Central Business District
        62  South Side Flats
        48  Squirrel Hill South
        41  Strip District
        39  Squirrel Hill North
        38  Shadyside
        34  Central Lawrenceville
        33  Bloomfield
        29  null
        28  Allegheny Center
        25  Garfield
        25  Bluff
        25  Greenfield
        25  Brookline
        24  Point Breeze
        24  Central Northside
        23  North Shore
        23  Mount Washington
        22  Hazelwood
        19  South Side Slopes

NEIGHBORHOOD by dollars
     130.08M       29 rows  null
      27.32M       11 rows  South Oakland
      24.30M       25 rows  Bluff
      20.34M       62 rows  South Side Flats
      19.10M       24 rows  Central Northside
      19.03M       19 rows  East Liberty
      18.29M        9 rows  Polish Hill
      17.30M       64 rows  Central Business District
       7.20M       41 rows  Strip District
       6.59M       25 rows  Garfield
       5.74M       11 rows  Crawford-Roberts
       5.21M       38 rows  Shadyside
       4.30M       15 rows  North Oakland
       4.06M        3 rows  Friendship
       2.89M       34 rows  Central Lawrenceville
       2.41M       13 rows  Point Breeze North
       2.15M        1 rows  South Shore
       2.00M       14 rows  Larimer
       1.85M       33 rows  Bloomfield
       1.83M        7 rows  Marshall-Shadeland

SRC_SHA256 by rows
      1.0K  6345fd18c6fe31423d666e8d2a2745f797d3ac002482b0b54c20f18c71925346

SRC_SHA256 by dollars
     340.20M     1.0K rows  6345fd18c6fe31423d666e8d2a2745f797d3ac002482b0b54c20f18c7192

## who x when

OWNER_NAME by ISSUED_DATE, dollars = TOTAL_PROJECT_VALUE
  1717 FIFTH LLC                            2023:5.00M
  1900 FOURPENN LLC                         2023:25.5K
  3250 LIBERTY OWNER LLC                    2023:18.02M
  327 NN LLC                                2023:6.39M
  5803 CENTRE LLC                           2023:18.36M
  810 W NORTH AVE ASSOCIATES LP             2023:7.28M
  ACA CONCOURSE EAST UNIT 3 LLC             2023:105.6K
  ALLEGHENY COMMONS COMMUNITY PARTNERS LP   2023:777.0K
  ALLEGHENY COUNTY                          2023:207.8K
  ALLEGHENY COUNTY SANITARY AUTHORITY       2023:12.75M
  BIBLE CENTER CHURCH INC                   2023:138.6K
  BUNCHER COMPANY                           2023:4.73M
  BURROWS STREET TOWNHOUSES LLC             2023:495.0K
  CARNEGIE MELLON UNIVERSITY                2023:508.6K
  CITY OF PITTSBURGH                        2023:3.43M
  COSTELLO PROPERTIES LLC                   2023:563.5K
  CRAWFORD JOHN LLC                         2023:1.11M
  EAST LIBERTY SOUTH LIMITED PARTNERSHIP    2023:41.7K
  ELIZABETH MAGEE HOSPITAL                  2023:27.19M
  GARDEN THEATER BLOCK LLC                  2023:7.65M
  HRLP FOURTH AVENUE LLC                    2023:4.70M
  HSRE-RPG FORBES AVENUE LLC                2023:7.50M
  INCORP TRUSTEES OF THE SALVATION ARMY IN  2023:5.37M
  MERCY HOSPITAL OF PITTSBURGH              2023:5.45M
  NORTH SHORE DEVELOPERS LP                 2023:665.0K
  PRODUCE TERMINAL HOLDINGS LLC             2023:79.4K
  RIDC MILL 19A                             2023:552.1K
  SPORTS AND EXHIBITION AUTHORITY OFPITTSB  2023:2.96M
  UPMC MERCY                                2023:17.93M
  UPMC PRESBYTERIAN SHADYSIDE               2023:106.47M

CONTRACTORS_NAME by ISSUED_DATE, dollars = TOTAL_PROJECT_VALUE
  Al. Neyer LLC                             2023:18.36M
  Clista Electric Inc                       2023:1.20M
  Franjo Construction                       2023:7.50M
  Grunau Company, Inc.                      2023:169.1K
  Gunton Corp                               2023:199.7K
  Hampton Mechanical, Inc.                  2023:973.9K
  Hanlon Electric Company                   2023:549.9K
  Home Depot USA                            2023:45.7K
  J.A. Sauer Heating & Air Conditioning     2023:208.3K
  Lang Electrical Contracting               2023:6.0K
  Mascaro Construction Co LP                2023:5.47M
  McKamish Inc                              2023:6.02M
  Mike Coates Construction Co., Inc.        2023:12.75M
  Mistick Construction Company              2023:21.01M
  Mongiovi & Son Fire Protection            2023:143.5K
  PE REAL ESTATE HOLDINGS LLC               2023:550.0K
  Renewal By Andersen LLC                   2023:368.1K
  Residential Development & Construction I  2023:17.96M
  Richard Brandi                            2023:27.5K
  RuthRauff Sauer LLC                       2023:17.31M
  Ryco Fire Protection Services LP          2023:277.7K
  Rycon Construction, Inc                   2023:42.89M
  Sota Construction Services                2023:5.37M
  Trinity Solar Inc                         2023:131.8K
  Volpatt Construction Corporation          2023:4.83M
  Whiting-Turner / P.J. Dick JV             2023:106.43M
  William Santoro                           2023:123.9K
  Window Nation, LLC                        2023:88.3K
  Window World of Pittsburgh LLC            2023:104.8K
  null                                      2023:754.0K

## what

WARD: 14 19%, 22 11%, 2 8%, 4 8%, 1 8%, 17 8%, 19 8%, 15 7%, 8 6%, 11 6%, 10 6%, 7 6%

TYPE_OF_WORK_DESCRIPTION: ADDITION / ALTERATION 56%, MINOR ALTERATION 27%, NEW CONSTRUCTION 6%, NEW 3%, NEW SYSTEM 2%, Non-substantial Improvement 2%, TEMPORARY USE 2%, COMPLETE DEMOLITION 1%, Permanent Use 1%, NEW USE 0%, null 0%, ALTERATION TO EXISTING 0%

TYPE_OF_STRUCTURE: Residential - Single Family 44%, Commercial - All other uses 35%, Commercial 7%, Residential 6%, Residential - Two-Family 4%, null 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PERMIT_NUMBER | id | 1.0K | 0 | PLI-LO-2021-10820 6; OOP-2023-03174 6; SP-2023-03166 6; BP-2019-03211 6 |
| ISSUED_DATE | date | 24 | 0 | 2023-04-28T00:00:00 95; 2023-04-20T00:00:00 82; 2023-04-05T00:00:00 79; 2023-04-14T00:00:00 61 |
| PARCEL_NUMBER | other | 792 | 0 | 0008-D-00050-0000-00 24; 0001-H-00030-0000-00 13; 0009-D-00200-0000-00 10; 0002-G-00066-0000-00 9 |
| ADDRESS | other | 777 | 0 | 255 E OHIO ST, Pittsburgh 24; 4 PPG PL, Pittsburgh, PA  13; 1669 SMALLMAN ST, Pittsbu 10; 1027 5TH AVE, Pittsburgh, 9 |
| NEIGHBORHOOD | who | 89 | 0 | Central Business District 64; South Side Flats 62; Squirrel Hill South 48; Strip District 41 |
| WARD | category | 38 | 0 | 14 131; 22 75; 2 57; 4 56 |
| OWNER_NAME | who | 726 | 0 | ALLEGHENY COMMONS COMMUNI 24; CITY OF PITTSBURGH 14; HRLP FOURTH AVENUE LLC 13; ALLEGHENY COUNTY 11 |
| CONTRACTORS_NAME | who | 461 | 0 | null 61; Hampton Mechanical, Inc. 25; Renewal By Andersen LLC 17; Window World of Pittsburg 17 |
| TYPE_OF_WORK_DESCRIPTION | category | 18 | 0 | ADDITION / ALTERATION 576; MINOR ALTERATION 275; NEW CONSTRUCTION 66; NEW 29 |
| TYPE_OF_STRUCTURE | category | 6 | 0 | Residential - Single Fami 464; Commercial - All other us 370; Commercial 76; Residential 58 |
| WORK_DESCRIPTION | other | 691 | 0 | null 291; REPLACEMENT OF EXISTING A 20; COMPLETE DEMOLITION OF EX 5; NEW EXTERIOR VERTICAL PAR 5 |
| TOTAL_PROJECT_VALUE | amount | 448 | 0 | 0.0 59; 5000.0 43; 2000.0 34; 500.0 26 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:24:09.16815 1.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 68ce982a-f2ff-4f85-92c8-b 1.0K |
| SRC_SHA256 | who | 1 | 0 | 6345fd18c6fe31423d666e8d2 1.0K |
