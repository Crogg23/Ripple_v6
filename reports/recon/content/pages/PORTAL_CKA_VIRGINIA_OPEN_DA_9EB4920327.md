# PORTAL_CKA_VIRGINIA_OPEN_DA_9EB4920327

rows 72  columns 51  scan 5.7s

roles: amount 5, audit 2, category 25, date 7, empty 5, other 4, who 4

## when

CREATED_DATE
  2026        72  ##############################

LAST_EDITED_DATE
  2026        72  ##############################

VDOT_RECEIVED_DATE
  2020        13  ######################
  2021         7  ############
  2022        12  ####################
  2023        18  ##############################
  2024         6  ##########
  2025        14  #######################
  2026         2  ###

VDOT_COMMENT_DATE
  2020        13  ######################
  2021         6  ##########
  2022        13  ######################
  2023        18  ##############################
  2024         5  ########
  2025        15  #########################

LOCAL_DUE_DATE
  2021         1  ##
  2022         7  ##############
  2023        12  ########################
  2024         3  ######
  2025        15  ##############################

VDOT_DUE_DATE
  2026         2  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 31 | 36.69 | 37.23 | 38.13 | 38.27 | 1.2K |
| LONGITUDE | 31 | -80 | -77.35 | 80.08 | 80.10 | -1.6K |
| ACREAGE | 22 | 0 | 0 | 65.67 | 71.66 | 210.07 |
| UNIT_SQUARE_FEET | 18 | 0 | 0 | 4.4K | 5.3K | 5.3K |
| SHAPE__LENGTH | 72 | 20.03 | 908.20 | 11.7K | 12.7K | 113.2K |

## who

PROJECT_NAME by rows
        13  Lit Communications
         3  RVBA Fiber Installation on Rte 419
         2  WVWA Commonwealth Drive Sanitary Sewer Replacement
         2  SP-24-13 Redhill Sewer Upgrades
         2  WVWA Thompson Memorial Drive Water Main
         2  Bridgeport Unit 6 Epic Homes
         1  Evergreen Country Club
         1  Cascade Parkway Bike & Ped.
         1  Dominion Energy Virginia¿s Proposed 230 kV Germanna Lines and Germanna
         1  Realigned French Ford Road
         1  WVWA Hollins to Botetourt WL Replacement
         1  S-24-31 Forehand-Jarrell Boundary Line Adjustment
         1  RWSA SFRR to RMR Raw Water Transmission Pipeline
         1  Tony Carollo - Water and Sewer Extension
         1  Victoria Meadows Sanitary Sewer Plans
         1  Sudley Manor Drive Sidewalk Project
         1  Route 7 - Shared Use Path
         1  SP-23-07 River Road Transmission Main
         1  Kessinger Hunter Building VA3, VA4, VA5
         1  Talbots Crossing - Phase 1 Public Water Line Extension

PROJECT_NAME by dollars
        5.3K        1 rows  St. Katharine Drexel Catholic Church
           0        1 rows  WVWA Mount Pleasant Sewer Extension
           0       13 rows  Lit Communications
           0        1 rows  WVWA Sanderson Drive WL Extension
           0        1 rows  WVWA Wildwood Road Skyview Road WL Replacement
           0        1 rows  WVWA Angel Lane WL Interconnection
           0        2 rows  Bridgeport Unit 6 Epic Homes
           0        1 rows  WVWA Iron Gate Waterline Replacement
           0        1 rows  Bristow Crossing PI Plan
           0        1 rows  Waterline Extension to Route 10
           0        1 rows  Cascade Parkway Bike & Ped.
           0        1 rows  Bristow Corner Public Improvement Plan
           0        1 rows  RWSA SFRR to RMR Raw Water Transmission Pipeline
           0        1 rows  SP-23-13 Appomattox River Crossing Water Main
           0        1 rows  Heathcote Marketplace Water and Sewer Plan
           0        1 rows  Smith Farm, off-site intersection improvements
           0        1 rows  GC Raw Water Main Division 2
           0        2 rows  SP-24-13 Redhill Sewer Upgrades
           0        1 rows  Talbots Crossing - Phase 1 Public Water Line Extension
           0        1 rows  Quartz District-West MOT

CREATED_USER by rows
        72  Eric.Hetzer_VDOT

CREATED_USER by dollars
        5.3K       72 rows  Eric.Hetzer_VDOT

LAST_EDITED_USER by rows
        72  Eric.Hetzer_VDOT

LAST_EDITED_USER by dollars
        5.3K       72 rows  Eric.Hetzer_VDOT

SRC_SHA256 by rows
        72  f2a057c795e5313e895e86d04d305ed2d194ca33ea3421240f632a91329e9d2a

SRC_SHA256 by dollars
        5.3K       72 rows  f2a057c795e5313e895e86d04d305ed2d194ca33ea3421240f632a91329e

## who x when

PROJECT_NAME by VDOT_RECEIVED_DATE, dollars = UNIT_SQUARE_FEET
  Bridgeport Unit 6 Epic Homes              2022:2
  Bristow Corner Public Improvement Plan    2025:1
  Bristow Crossing PI Plan                  2025:1
  Cascade Parkway Bike & Ped.               2026:1
  Dominion Energy Virginia¿s Proposed 230   2023:1
  Evergreen Country Club                    2023:1
  Kessinger Hunter Building VA3, VA4, VA5   2024:1
  Lit Communications                        2020:0
  RVBA Fiber Installation on Rte 419        2021:3
  RWSA SFRR to RMR Raw Water Transmission   2025:1
  Realigned French Ford Road                2025:1
  Route 7 - Shared Use Path                 2026:1
  S-24-31 Forehand-Jarrell Boundary Line A  2024:1
  SP-23-07 River Road Transmission Main     2025:1
  SP-23-13 Appomattox River Crossing Water  2023:1
  SP-24-13 Redhill Sewer Upgrades           2024:1 2025:1
  St. Katharine Drexel Catholic Church      2023:5.3K
  Sudley Manor Drive Sidewalk Project       2023:1
  Talbots Crossing - Phase 1 Public Water   2024:1
  Tony Carollo - Water and Sewer Extension  2023:1
  Victoria Meadows Sanitary Sewer Plans     2021:1
  WVWA Angel Lane WL Interconnection        2023:0
  WVWA Commonwealth Drive Sanitary Sewer R  2023:2
  WVWA Hollins to Botetourt WL Replacement  2022:1
  WVWA Iron Gate Waterline Replacement      2023:1
  WVWA Mount Pleasant Sewer Extension       2021:0
  WVWA Sanderson Drive WL Extension         2023:0
  WVWA Thompson Memorial Drive Water Main   2022:2
  WVWA Wildwood Road Skyview Road WL Repla  2022:0
  Waterline Extension to Route 10           2021:1

CREATED_USER by VDOT_RECEIVED_DATE, dollars = UNIT_SQUARE_FEET
  Eric.Hetzer_VDOT                          2020:0 2021:0 2022:0 2023:5.3K 2024:6 2025:14 2026:2

## what

SUBMISSION_NUMBER: 1 35%, 2 32%, 5 19%, 4 8%, 3 6%

SUBMISSION_TYPE: Letter confirming previously a 95%, Drainage - Flood Plain Study 5%

LOCAL_PROJECT_ID: SP-24-13 Redhill Sewer Upgrade 15%, CP2022000 15%, FLPL-2026-0010 8%, Construction Plan Review 8%, Dinwiddie Industrial Park - Of 8%, SPR 2026-00101 8%, SPR25-004 8%, SPR 2026-00137 8%, spr 2025-00073 8%, SPR 2025-00129 8%, Picture Lake Campground Waterl 8%

LAND_USE_AREA: SL_SL 40%, NV_PW 21%, RIC_S 19%, HMT_F 7%, Loudoun 3%, CUL_C 3%, STN_C 3%, HMT_W 1%, SL_BF 1%, CUL_CN 1%

VDOT_DISTRICT: Salem 42%, Northern Virginia 24%, Richmond 19%, Hampton Roads 8%, Culpeper 4%, Staunton 3%

JURISDICTION: County Of Botetourt 24%, County Of Prince William 23%, County Of Roanoke 20%, County Of Prince George 17%, Loudoun 3%, County Of Dinwiddie 3%, Couny of Augusta 3%, County Of Greene 2%, County of Albemarle 2%, County of York 2%, County Of Southampton 2%, County Of Bedford 2%

PROJECT_GROUP_ID: Talbots Crossing 11%, SPR 2024-00092 11%, SPR 2024-00105 11%, SPR 2024-00053 11%, SPR 2024-00013 11%, SDR 2024-00010 11%, SPR 2023-00427 11%, SPR 2024-00016 11%, Mallory Point 11%

GROUP_NAME: S 97%, M 3%

GROUP_DESCRIPTION: Talbots Crossing 100%

FACILITY_TYPE: Commercial - Other 33%, Commercial - Industrial 29%, Residential - Single Family 15%, Government - Other (Not School 15%, Government PI Plan - Shared Us 2%, Commercial - Mixed Type 2%, Commercial - Office 2%, Commercial - Shopping Center 2%

VDOT_CONTACT: Ashley C Smith 23%, Hinson, Paul 12%, Paul Hinson 12%, Joshua Norris 9%, Brian K. Blevins, P.E. 9%, Shrestha, Ravi 7%, Jeremy Sanders 5%, Erik Spencer 5%, Steven B. Mullins, PE 5%, Brian K. Blevins, PE 5%, Clyde A. Wallace 4%, Hiren Joshi 4%

ROUTE: 1794 50%, Route 7 50%

STREET: Cascade Parkway 50%, Leesburg Pike 50%

C_527_SUBMISSION: 0 100%

PARCEL_ID: 22-33 9%, 33-6-a 9%, 350(0A)00-005-C 9%, 120(01)00-003-0 9%, 280(0A)00-008-B 9%, 134 A 14 9%, 7596-65-1125 9%, 8192-93-1868 9%, 050(0A)00-013-E 9%, 80A1-8-8 9%, 8292-84-1372 9%

IS_PRINCIPLE_PARCEL: 1 58%, 0 42%

IS_INVALID_PARCEL: Yes 92%, No 8%

LOCAL_CONTACT_NAME: Denise Sowder 29%, Nicole Pendleton 29%, Tim Graves 10%, Bill Westerman (wwesterman@pwc 10%, Mark Bassett 4%, Jack Greenstein 4%, Andre Greene 4%, Michele Astarb 4%, Maggie Auer 2%, Randy Steele 2%, Al Al-Obaidi (AAlObaidi@pwcgov 2%

UNIT_COUNT: 0 90%, 26 5%, 1 5%

VEHICLES_PER_DAY: 0 94%, 755 6%

VEHICLES_PER_HOUR: 0 100%

SCOPE_MEETING_HELD: No 100%

REVIEW_MEETING_REQUESTED: No 100%

PRIMARY_ROUTE: 1 100%

PROJECT_STATUS: Review Complete - Acceptable 59%, Review Complete - Revision Req 41%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| OBJECTID | other | 73 | 0 | 16657 1; 16641 1; 15041 1; 14722 1 |
| CREATED_USER | who | 1 | 0 | Eric.Hetzer_VDOT 72 |
| CREATED_DATE | date | 1 | 0 | 6/16/2026 1:33:36 PM 72 |
| LAST_EDITED_USER | who | 1 | 0 | Eric.Hetzer_VDOT 72 |
| LAST_EDITED_DATE | date | 1 | 0 | 6/16/2026 1:33:36 PM 72 |
| PROJECT_ID | other | 55 | 0 | 11-Various-20201204-63366 13; 80-419-20210712-71104 3; 80-1723-20230421-93582 2; 80-311-20220414-80910 2 |
| MASTER_ID | other | 54 | 2 | 63366 13; 71104 3; 93582 2; 80910 2 |
| PROJECT_NAME | who | 53 | 0 | Lit Communications 13; RVBA Fiber Installation o 3; SP-24-13 Redhill Sewer Up 2; WVWA Commonwealth Drive S 2 |
| SUBMISSION_NUMBER | category | 5 | 0 | 1 25; 2 23; 5 14; 4 6 |
| SUBMISSION_TYPE | category | 3 | 50 | Letter confirming previou 21; Drainage - Flood Plain St 1 |
| LOCAL_PROJECT_ID | category | 34 | 37 | SP-24-13 Redhill Sewer Up 2; CP2022000 2; FLPL-2026-0010 1; Construction Plan Review 1 |
| LAND_USE_AREA | category | 10 | 0 | SL_SL 29; NV_PW 15; RIC_S 14; HMT_F 5 |
| VDOT_DISTRICT | category | 6 | 0 | Salem 30; Northern Virginia 17; Richmond 14; Hampton Roads 6 |
| JURISDICTION | category | 18 | 0 | County Of Botetourt 16; County Of Prince William 15; County Of Roanoke 13; County Of Prince George 11 |
| PROJECT_GROUP_ID | category | 10 | 63 | Talbots Crossing 1; SPR 2024-00092 1; SPR 2024-00105 1; SPR 2024-00053 1 |
| GROUP_NAME | category | 3 | 2 | S 68; M 2 |
| GROUP_DESCRIPTION | category | 2 | 71 | Talbots Crossing 1 |
| FACILITY_TYPE | category | 9 | 20 | Commercial - Other 17; Commercial - Industrial 15; Residential - Single Fami 8; Government - Other (Not S 8 |
| VDOT_RECEIVED_DATE | date | 54 | 0 | 12/4/2020 12:00:00 AM 13; 7/12/2021 12:00:00 AM 3; 9/5/2023 12:00:00 AM 2; 4/21/2023 12:00:00 AM 2 |
| VDOT_COMMENT_DATE | date | 53 | 2 | 12/8/2020 12:00:00 AM 13; 7/14/2021 12:00:00 AM 3; 5/31/2023 12:00:00 AM 2; 6/6/2022 12:00:00 AM 2 |
| LOCALITY_APPROVAL_DATE | empty | 1 | 72 |  |
| LOCAL_DUE_DATE | date | 37 | 34 | 10/10/2023 12:00:00 AM 2; 4/25/2022 12:00:00 AM 2; 12/30/2025 12:00:00 AM 1; 12/18/2025 12:00:00 AM 1 |
| VDOT_CONTACT | category | 24 | 0 | Ashley C Smith 13; Hinson, Paul 7; Paul Hinson 7; Joshua Norris 5 |
| ROUTE | category | 3 | 70 | 1794 1; Route 7 1 |
| STREET | category | 3 | 70 | Cascade Parkway 1; Leesburg Pike 1 |
| C_527_SUBMISSION | category | 2 | 2 | 0 70 |
| STATUS_CODE | empty | 1 | 72 |  |
| IS_PUBLIC | other | 1 | 0 | Yes 72 |
| LATITUDE | amount | 29 | 41 | 37.2598 2; 37.20597 2; 37.32737 2; 37.196455 1 |
| LONGITUDE | amount | 29 | 41 | -77.35178 2; -79.99798 2; 80.04131 2; -77.455026 1 |
| PARCEL_ID | category | 13 | 60 | 22-33 1; 33-6-a 1; 350(0A)00-005-C 1; 120(01)00-003-0 1 |
| IS_PRINCIPLE_PARCEL | category | 3 | 60 | 1 7; 0 5 |
| IS_INVALID_PARCEL | category | 3 | 60 | Yes 11; No 1 |
| LOCAL_CONTACT_NAME | category | 28 | 7 | Denise Sowder 14; Nicole Pendleton 14; Tim Graves 5; Bill Westerman (wwesterma 5 |
| TIA_PREPARER | empty | 1 | 72 |  |
| ACREAGE | amount | 8 | 50 | 0 16; 7 1; 43.15 1; 22 1 |
| UNIT_COUNT | category | 4 | 52 | 0 18; 26 1; 1 1 |
| UNIT_SQUARE_FEET | amount | 3 | 54 | 0 17; 5336 1 |
| VEHICLES_PER_DAY | category | 3 | 55 | 0 16; 755 1 |
| VEHICLES_PER_HOUR | category | 2 | 54 | 0 18 |
| SCOPE_MEETING_HELD | category | 2 | 2 | No 70 |
| REVIEW_MEETING_REQUESTED | category | 2 | 2 | No 70 |
| LOCAL_RECEIVED_DATE | empty | 1 | 72 |  |
| VDOT_DUE_DATE | date | 3 | 70 | 6/10/2026 12:00:00 AM 1; 5/27/2026 12:00:00 AM 1 |
| COMPLETED_DATE | empty | 1 | 72 |  |
| PRIMARY_ROUTE | category | 2 | 10 | 1 62 |
| PROJECT_STATUS | category | 3 | 2 | Review Complete - Accepta 41; Review Complete - Revisio 29 |
| SHAPE__LENGTH | amount | 73 | 0 | 2557.58720773352 1; 2619.1510529464 1; 873.110338467405 1; 369.739238135453 1 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 21:29:17.36938 72 |
| SOURCE_RUN_ID | audit | 1 | 0 | e512a871-36e2-4417-9126-5 72 |
| SRC_SHA256 | who | 1 | 0 | f2a057c795e5313e895e86d04 72 |
