# PORTAL_CKA_WPRDC_ALLEGHENY_5B37A5568E

rows 10.0K  columns 21  scan 6.2s

roles: amount 3, audit 2, category 7, date 2, id 1, other 3, who 4

## when

ISSUE_DATE
  2019       728  ###############
  2020      1.3K  ##########################
  2021      1.4K  #############################
  2022      1.4K  #############################
  2023      1.4K  #############################
  2024      1.5K  ##############################
  2025      1.5K  ##############################
  2026       764  ################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| TOTAL_PROJECT_VALUE | 10.0K | 0 | 10.0K | 1.30M | 73.23M | 1.26B |
| LATITUDE | 10.0K | 40.36 | 40.45 | 40.49 | 40.50 | 404.5K |
| LONGITUDE | 10.0K | -80.09 | -79.97 | -79.89 | -79.87 | -799.7K |

## who

OWNER_NAME by rows
       114  CITY OF PITTSBURGH
        66  HOUSING AUTHORITY CITY OF PITTSBURGH
        59  PRESTIGIOUS HILLS LP
        58  CARNEGIE MELLON UNIVERSITY
        45  ALLEGHENY GENERAL HOSPITAL
        43  BUNCHER COMPANY
        39  HRLP FOURTH AVENUE LLC
        37  SHADYSIDE HOSPITAL
        33  COSTELLO PROPERTIES LLC
        32  NORTHSIDE PROPERTIES RESIDENCES III LLC
        30  CEDARWOOD HOMES HOLDINGS LLC
        30  WEST PENN HOSPITAL
        29  MERCY HOSPITAL OF PITTSBURGH
        28  HERTZ GATEWAY CENTER LP
        22  ALLEGHENY COUNTY
        22  HOUSING AUTHORITY OF THE CITY OFPITTSBURGH
        19  PORT AUTHORITY OF ALLEGHENY COUNTY
        17  11 STANWIX OWNER LLC
        17  NORTHSIDE PROPERTIES RESIDENCES II LLC
        17  DUQUESNE UNIVERSITY OF THE HOLY GHOST

OWNER_NAME by dollars
      81.50M       12 rows  OFFICE PARTNERS XXIII BLOCK G1 LLC
      65.00M        1 rows  HSRE-RPG FORBES AVENUE LLC
      63.38M      114 rows  CITY OF PITTSBURGH
      40.36M        2 rows  ALBION LAWRENCEVILLE LLC
      35.00M        1 rows  BAUM HAUS HOLDINGS LLC
      27.12M        6 rows  ARSENAL 201-PHASE II LLC
      16.33M        3 rows  UNIVERSITY OF PITTSBURGH-OF THECOMMONWEALTH SYSTEM OF HIGHER
      15.38M        6 rows  2P110 CARES INC
      15.35M        4 rows  ALMONO LP
      15.23M       58 rows  CARNEGIE MELLON UNIVERSITY
      13.50M       43 rows  BUNCHER COMPANY
      12.91M       29 rows  MERCY HOSPITAL OF PITTSBURGH
      12.86M        5 rows  ELIZABETH MAGEE HOSPITAL
      12.64M        6 rows  THREE CROSSINGS 2.0-G LP
      11.91M        3 rows  HUDSON SMALLMAN LP
       8.67M        2 rows  FAIRFAX-PGH BUILDINGS LLC
       8.38M       16 rows  PGH NATIONAL BANK TRUSTEE
       8.33M       22 rows  ALLEGHENY COUNTY
       7.64M       45 rows  ALLEGHENY GENERAL HOSPITAL
       7.10M        1 rows  810 W NORTH AVE ASSOCIATES LP

CONTRACTOR_NAME by rows
       183  Renewal By Andersen LLC
        83  Window World of Pittsburgh LLC
        72  Mistick Construction Company
        69  Gunton Corp
        65  Thermo Twin Industries
        63  Preferred Fire Protection
        62  Window Nation, LLC
        58  Climatech, Inc
        57  Hatzel & Buehler, Inc
        55  Home Depot USA
        54  Leone Electrical Contractors, LLC
        53  Trinity Solar Inc
        52  Lewis McCullough
        52  Richard Brandi
        52  Ferry Electric Company
        51  M & J Electrical Contracting, Inc
        49  Window World Penn Ohio, LLC
        48  THERMO TWIN INDUSTRIES
        48  William Santoro
        47  Hanlon Electric Company

CONTRACTOR_NAME by dollars
     157.14M       29 rows  P.J. Dick Incorporated
      63.39M       34 rows  Rycon Construction, Inc
      60.09M       21 rows  Franjo Construction Corporation
      25.35M       28 rows  McKamish Inc
      23.98M       21 rows  Clista Electric Inc
      16.88M       27 rows  Mascaro Construction Co LP
      15.96M       16 rows  Arrow Electric Inc
      15.87M       72 rows  Mistick Construction Company
      14.04M       52 rows  Ferry Electric Company
      11.90M        1 rows  The Hudson Group Inc
      10.60M        7 rows  Jendoco Construction Corporation
       9.93M       24 rows  MBM Contracting, Inc
       8.77M       22 rows  Chris Levitt Electric Inc
       7.88M       47 rows  Hanlon Electric Company
       7.58M        5 rows  MASCARO CONSTRUCTION COMPANY LP
       6.87M       57 rows  Hatzel & Buehler, Inc
       6.55M        3 rows  CA Design Build LLC
       6.50M        5 rows  Kirby Electric Inc
       6.29M        4 rows  Sentinel Construction LLC
       6.27M        6 rows  Westmoreland Electric Services, LLC

NEIGHBORHOOD by rows
       645  Central Business District
       404  Squirrel Hill South
       394  Squirrel Hill North
       383  Shadyside
       340  Bloomfield
       328  South Side Flats
       310  Brookline
       302  Central Lawrenceville
       261  Mount Washington
       256  Strip District
       248  Point Breeze
       241  Central Northside
       229  East Liberty
       208  Highland Park
       195  Greenfield
       188  Carrick
       176  Lower Lawrenceville
       172  Hazelwood
       168  Bluff
       165  Brighton Heights

NEIGHBORHOOD by dollars
     231.57M      168 rows  Bluff
     114.28M      105 rows  Crawford-Roberts
     100.53M      645 rows  Central Business District
      89.34M      256 rows  Strip District
      74.36M      394 rows  Squirrel Hill North
      58.48M      328 rows  South Side Flats
      45.40M      157 rows  Upper Lawrenceville
      42.15M      121 rows  North Shore
      38.20M       72 rows  South Oakland
      36.61M       31 rows  Friendship
      32.59M      383 rows  Shadyside
      31.42M      176 rows  Lower Lawrenceville
      28.67M      172 rows  Hazelwood
      22.02M      130 rows  Lincoln-Lemington-Belmar
      21.70M      241 rows  Central Northside
      21.51M       92 rows  Central Oakland
      20.87M      137 rows  North Oakland
      16.96M      340 rows  Bloomfield
      16.80M      229 rows  East Liberty
      15.16M      302 rows  Central Lawrenceville

SRC_SHA256 by rows
     10.0K  8aa0e704d8b2bb9120ee5386f35484d97a2271ae34c74d7b1edcfd5bd05be666

SRC_SHA256 by dollars
       1.26B    10.0K rows  8aa0e704d8b2bb9120ee5386f35484d97a2271ae34c74d7b1edcfd5bd05b

## who x when

OWNER_NAME by ISSUE_DATE, dollars = TOTAL_PROJECT_VALUE
  11 STANWIX OWNER LLC                      2020:89.0K 2021:1.34M 2022:88.1K 2023:808.0K
  2P110 CARES INC                           2021:15.36M 2022:14.0K
  ALBION LAWRENCEVILLE LLC                  2024:40.36M
  ALLEGHENY COUNTY                          2019:65.8K 2020:6.33M 2021:27.0K 2022:375.1K 2023:80.0K 2024:1.45M
  ALLEGHENY GENERAL HOSPITAL                2019:2.0K 2020:65.0K 2021:940.3K 2022:849.0K 2023:82.5K 2024:5.59M 2025:115.2K
  ALMONO LP                                 2020:6.5K 2023:15.00M 2024:347.0K
  ARSENAL 201-PHASE II LLC                  2020:26.51M 2021:430.0K 2022:176.0K
  BAUM HAUS HOLDINGS LLC                    2022:35.00M
  BUNCHER COMPANY                           2019:1.35M 2020:3.49M 2021:1.85M 2022:1.42M 2023:3.57M 2024:1.80M 2025:10.5K
  CARNEGIE MELLON UNIVERSITY                2019:641.1K 2020:23.0K 2021:4.91M 2022:1.52M 2023:5.94M 2024:1.93M 2025:260.0K
  CEDARWOOD HOMES HOLDINGS LLC              2022:1.76M 2023:249.0K 2024:0
  CITY OF PITTSBURGH                        2019:305.6K 2020:1.24M 2021:26.12M 2022:3.28M 2023:30.14M 2024:1.89M 2025:403.6K
  COSTELLO PROPERTIES LLC                   2019:26.2K 2020:144.0K 2021:102.2K 2022:238.8K 2023:66.0K 2024:103.0K 2025:25.0K
  DUQUESNE UNIVERSITY OF THE HOLY GHOST     2019:8.0K 2020:378.4K 2021:0 2023:204.2K 2024:1.04M 2025:15.0K
  ELIZABETH MAGEE HOSPITAL                  2021:12.44M 2022:22.0K 2024:400.0K
  HERTZ GATEWAY CENTER LP                   2019:3.5K 2020:44.5K 2021:297.6K 2022:22.0K 2023:1.37M 2024:4.30M 2025:5.0K
  HOUSING AUTHORITY CITY OF PITTSBURGH      2019:37.5K 2020:1.42M 2021:2.09M 2022:124.7K 2023:258.5K 2024:1.59M
  HOUSING AUTHORITY OF THE CITY OFPITTSBUR  2019:43.7K 2020:6.8K 2021:1.07M 2022:524.5K 2023:0 2024:2.84M
  HRLP FOURTH AVENUE LLC                    2019:67.6K 2020:95.9K 2021:84.3K 2022:800.0K 2023:1.23M 2024:1.51M 2025:6.0K
  HSRE-RPG FORBES AVENUE LLC                2024:65.00M
  MERCY HOSPITAL OF PITTSBURGH              2019:12.0K 2020:848.5K 2021:534.5K 2022:6.72M 2023:4.78M 2024:19.0K
  NORTHSIDE PROPERTIES RESIDENCES II LLC    2019:39.0K 2020:221.3K
  NORTHSIDE PROPERTIES RESIDENCES III LLC   2020:820.5K 2021:183.8K 2022:31.5K
  OFFICE PARTNERS XXIII BLOCK G1 LLC        2022:70.33M 2023:2.31M 2024:8.83M 2025:36.5K
  PORT AUTHORITY OF ALLEGHENY COUNTY        2019:511.6K 2020:45.2K 2021:354.5K 2022:3.60M 2023:5.0K 2024:2.00M
  PRESTIGIOUS HILLS LP                      2022:338.5K 2023:107.2K 2024:50.0K
  SHADYSIDE HOSPITAL                        2019:11.6K 2020:476.3K 2021:2.16M 2022:357.2K 2023:115.7K 2024:757.3K
  THREE CROSSINGS 2.0-G LP                  2020:12.63M 2021:15.0K 2022:2.1K
  UNIVERSITY OF PITTSBURGH-OF THECOMMONWEA  2022:12.0K 2023:16.31M
  WEST PENN HOSPITAL                        2019:1.50M 2020:1.03M 2021:890.8K 2022:1.42M 2023:371.5K 2024:655.0K

CONTRACTOR_NAME by ISSUE_DATE, dollars = TOTAL_PROJECT_VALUE
  Arrow Electric Inc                        2019:27.5K 2021:45.0K 2022:322.7K 2023:27.5K 2024:15.45M 2025:66.6K 2026:18.3K
  Climatech, Inc                            2020:114.8K 2021:124.8K 2022:183.9K 2023:575.9K 2024:1.34M 2025:326.5K 2026:276.0K
  Clista Electric Inc                       2020:2.33M 2021:12.50M 2022:2.29M 2023:2.74M 2024:18.0K 2025:1.20M 2026:2.90M
  Ferry Electric Company                    2020:85.0K 2021:298.7K 2022:2.22M 2023:425.9K 2024:1.51M 2025:8.09M 2026:1.42M
  Franjo Construction Corporation           2020:24.50M 2022:1.50M 2024:34.09M
  Gunton Corp                               2019:74.9K 2020:131.0K 2021:61.1K 2022:196.6K 2023:193.4K 2024:127.1K
  Hanlon Electric Company                   2019:18.0K 2020:15.8K 2021:882.0K 2022:2.52M 2023:272.5K 2024:3.34M 2025:733.2K 2026:100.0K
  Hatzel & Buehler, Inc                     2020:210.9K 2021:2.16M 2022:1.47M 2023:726.0K 2024:1.02M 2025:364.3K 2026:920.2K
  Home Depot USA                            2019:21.3K 2020:33.1K 2021:60.3K 2022:24.3K 2023:59.9K 2024:30.8K
  Jendoco Construction Corporation          2021:6.52M 2023:630.0K 2024:3.20M 2026:250.0K
  Leone Electrical Contractors, LLC         2019:99.7K 2020:19.3K 2021:2.89M 2022:1.15M 2023:13.6K 2024:6.6K 2025:665.2K
  Lewis McCullough                          2019:3.0K 2020:5.0K 2021:3.0K 2022:6.0K 2023:49.5K 2024:11.0K 2025:8.4K 2026:9.0K
  M & J Electrical Contracting, Inc         2020:150.0K 2021:365.0K 2022:124.7K 2023:762.0K 2024:301.8K 2025:385.4K 2026:708.7K
  MBM Contracting, Inc                      2019:453.2K 2020:3.69M 2021:2.36M 2022:1.43M 2023:1.65M 2024:350.0K
  Mascaro Construction Co LP                2020:170.0K 2021:1.62M 2022:7.74M 2023:3.49M 2024:2.79M 2025:1.05M 2026:22.0K
  McKamish Inc                              2021:290.6K 2022:1.33M 2023:20.64M 2024:776.7K 2025:1.45M 2026:853.9K
  Mistick Construction Company              2020:900.2K 2021:298.4K 2022:9.45M 2023:218.0K 2024:3.91M 2025:1.10M
  P.J. Dick Incorporated                    2019:1.05M 2020:1.78M 2021:39.64M 2022:78.72M 2023:33.06M 2024:2.46M 2025:426.0K
  Preferred Fire Protection                 2019:702.5K 2020:789.1K 2021:401.6K 2022:649.2K 2023:63.5K
  Renewal By Andersen LLC                   2019:159.6K 2020:434.4K 2021:922.6K 2022:647.6K 2023:632.1K 2024:567.4K
  Richard Brandi                            2019:3.0K 2020:27.8K 2021:6.5K 2022:37.0K 2023:21.7K 2024:36.0K 2025:61.8K 2026:2.0K
  Rycon Construction, Inc                   2019:18.7K 2020:12.57M 2021:1.85M 2022:35.93M 2023:6.03M 2024:6.87M 2025:125.0K 2026:0
  THERMO TWIN INDUSTRIES                    2019:43.3K 2020:116.2K 2021:126.6K
  The Hudson Group Inc                      2024:11.90M
  Thermo Twin Industries                    2021:126.0K 2022:247.6K 2023:242.0K 2024:22.1K
  Trinity Solar Inc                         2021:88.9K 2022:621.3K 2023:364.4K 2024:69.0K
  William Santoro                           2020:81.7K 2021:6.6K 2022:39.9K 2023:38.0K 2024:218.4K 2025:91.4K 2026:7.5K
  Window Nation, LLC                        2021:112.7K 2022:188.5K 2023:196.9K 2024:65.9K
  Window World Penn Ohio, LLC               2019:64.8K 2020:80.7K 2021:38.7K 2023:6.9K 2024:5.8K
  Window World of Pittsburgh LLC            2019:5.8K 2020:29.1K 2021:125.2K 2022:135.7K 2023:110.9K 2024:25.6K

## what

PERMIT_TYPE: ELECTRICAL 31%, BUILDING 28%, Building & Development Applica 13%, MECHANICAL 13%, Suppression System Permit 4%, Fire Alarm Permit 4%, Demolition Permit 2%, Occupancy Only Permit 1%, Sign Permit 1%, Floodplain Permit 1%, Occupant Load Placard Permit 1%, Land Operations Permit 0%

WORK_TYPE: ADDITION / ALTERATION 46%, MINOR ALTERATION 28%, Existing (alteration/addition) 13%, NEW CONSTRUCTION 5%, NEW 2%, NEW SYSTEM 2%, COMPLETE DEMOLITION 1%, TEMPORARY USE 1%, CITY FUNDED DEMOLITION 1%, Non-substantial Improvement 1%, New Construction 0%, NEW USE 0%

COMMERCIAL_OR_RESIDENTIAL: Residential 62%, Commercial 38%

COUNCIL_DISTRICT: 1 17%, 7 15%, 9 13%, 6 13%, 5 9%, 8 9%, 3 9%, 2 8%, 4 7%

WARD: 14 20%, 19 11%, 2 10%, 10 9%, 11 7%, 1 7%, 9 6%, 15 6%, 7 6%, 8 6%, 4 6%, 22 5%

ZIP_CODE: 15212 14%, 15206 13%, 15217 11%, 15201 10%, 15219 10%, 15222 9%, 15213 7%, 15210 6%, 15224 6%, 15203 5%, 15207 5%, 15208 4%

STATUS: Completed 67%, Issued 24%, Expired 7%, Revoked 1%, Application Finalization 0%, Amendment Applicant Revisions 0%, Amendment Application Incomple 0%, Amendment Review 0%, Applicant Revisions 0%, Stop Work 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PERMIT_ID | id | 9.9K | 0 | OOP-2022-11358 50; BDA-2026-00873 50; BP-2020-02034 50; BP-2019-10278 50 |
| PERMIT_TYPE | category | 14 | 0 | ELECTRICAL 3.1K; BUILDING 2.8K; Building & Development Ap 1.3K; MECHANICAL 1.3K |
| OWNER_NAME | who | 2.1K | 5.6K | CITY OF PITTSBURGH 114; HOUSING AUTHORITY CITY OF 66; PRESTIGIOUS HILLS LP 59; CARNEGIE MELLON UNIVERSIT 58 |
| CONTRACTOR_NAME | who | 1.9K | 1.8K | Renewal By Andersen LLC 183; Window World of Pittsburg 84; Mistick Construction Comp 72; Gunton Corp 69 |
| WORK_DESCRIPTION | other | 5.9K | 3.5K | INTERIOR RENOVATIONS LOWE 33; INSTALLATION OF VENTILATI 33; REMOVE AND BUILD NEW 1ST  33; replace furnace 33 |
| WORK_TYPE | category | 20 | 28 | ADDITION / ALTERATION 4.5K; MINOR ALTERATION 2.8K; Existing (alteration/addi 1.3K; NEW CONSTRUCTION 523 |
| COMMERCIAL_OR_RESIDENTIAL | category | 3 | 20 | Residential 6.2K; Commercial 3.8K |
| TOTAL_PROJECT_VALUE | amount | 3.1K | 0 | 0 347; 5000 324; 10000 293; 1000 251 |
| ISSUE_DATE | date | 1.7K | 0 | 2022-08-10 52; 2025-07-18 52; 2022-03-18 52; 2026-02-09 51 |
| PARCEL_NUM | other | 7.1K | 0 | 0001H00030000000 57; 0023M00012000000 54; 0008L00008000000 51; 0002B00051000000 51 |
| ADDRESS | other | 7.2K | 0 | No primary address specif 196; 6 PPG PL #830, Pittsburgh 57; 320 E NORTH AVE, Pittsbur 54; 600 GRANT ST #5382, Pitts 51 |
| LATITUDE | amount | 7.2K | 0 | 40.4399201571 57; 40.4570531973 54; 40.4469510116 51; 40.4413703466 51 |
| LONGITUDE | amount | 7.3K | 0 | -80.0035680945 57; -80.0036108523 54; -80.0056724909 51; -79.994859348 51 |
| COUNCIL_DISTRICT | category | 9 | 0 | 1 1.7K; 7 1.5K; 9 1.3K; 6 1.3K |
| NEIGHBORHOOD | who | 91 | 0 | Central Business District 645; Squirrel Hill South 404; Squirrel Hill North 394; Shadyside 383 |
| WARD | category | 32 | 0 | 14 1.2K; 19 681; 2 582; 10 510 |
| ZIP_CODE | category | 28 | 0 | 15212 1.0K; 15206 998; 15217 805; 15201 786 |
| STATUS | category | 10 | 0 | Completed 6.7K; Issued 2.4K; Expired 723; Revoked 99 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:00:26.00636 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | c0d7c5c9-d465-479e-9908-9 10.0K |
| SRC_SHA256 | who | 1 | 0 | 8aa0e704d8b2bb9120ee5386f 10.0K |
