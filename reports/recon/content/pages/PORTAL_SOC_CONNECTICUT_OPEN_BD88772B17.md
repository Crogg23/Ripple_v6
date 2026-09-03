# PORTAL_SOC_CONNECTICUT_OPEN_BD88772B17

rows 1.4K  columns 111  scan 6.7s

roles: amount 39, audit 2, category 55, date 7, other 4, who 5

## when

CREATED_DATE
  2022       152  ########
  2023        95  #####
  2024       430  #######################
  2025       565  ##############################
  2026       125  #######

APPLICATION_DATE
  2022       153  #########
  2023        95  #####
  2024       364  #####################
  2025       532  ##############################
  2026       125  #######

SUBMITTED_DATE
  2019         1  
  2022       146  #########
  2023       102  ######
  2024       441  ############################
  2025       476  ##############################

APPROVAL_DATE
  2022       121  #######
  2023       121  #######
  2024       387  ######################
  2025       529  ##############################
  2026       145  ########

ENERGIZE_DATE
  2021         2  
  2022        52  ####
  2023       151  ###########
  2024       185  #############
  2025       426  ##############################
  2026       143  ##########

COMPLETED_DATE
  2022         4  
  2023        90  ########
  2024       231  ######################
  2025       318  ##############################
  2026       133  #############

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| LATITUDE | 1.2K | 41.01 | 41.51 | 42.01 | 42.04 | 48.7K |
| LONGITUDE | 1.2K | -73.69 | -72.85 | -71.87 | -71.81 | -85.4K |
| TOTAL_SYSTEM_POWER_KW | 1.3K | 0 | 11.50 | 2.0K | 18.0K | 168.7K |
| TOTAL_SYSTEM_POWER_MW | 1.4K | 0 | 0.01 | 2 | 17.99 | 169.49 |
| TOTAL_SYSTEM_POWER_WATTS | 1.4K | 0 | 11.5K | 2.00M | 17.98M | 168.68M |
| TOTAL_SYSTEM_ENERGY_CAPACITY | 1.3K | 0 | 27 | 6.0K | 36.0K | 401.8K |

## who

PROJECT_NAME by rows
         1  ESS-00066
         1  ESS-00053
         1  ESS-00310
         1  ESS-00265
         1  ESS-00246
         1  ESS-00266
         1  ESS-00292
         1  ESS-00522
         1  ESS-00361
         1  ESS-00551
         1  ESS-00830
         1  ESS-00601
         1  ESS-00394
         1  ESS-00516
         1  ESS-00064
         1  ESS-00014
         1  ESS-00699
         1  ESS-00248
         1  ESS-00289
         1  ESS-00126

PROJECT_NAME by dollars
       17.99        1 rows  ESS-00309
        7.71        1 rows  ESS-01010
           7        1 rows  ESS-00017
        4.98        1 rows  ESS-01039
        4.90        1 rows  ESS-00758
        4.90        1 rows  ESS-00019
        4.90        1 rows  ESS-00014
        3.98        1 rows  ESS-01606
        3.05        1 rows  ESS-00985
           3        1 rows  ESS-00172
           2        1 rows  ESS-01008
           2        1 rows  ESS-01007
           2        1 rows  ESS-03503
           2        1 rows  ESS-00963
           2        1 rows  ESS-00998
           2        1 rows  ESS-01000
           2        1 rows  ESS-00999
           2        1 rows  ESS-01009
           2        1 rows  ESS-01005
           2        1 rows  ESS-01006

CONTRACTOR_NAME by rows
       327  Earthlight Technologies, LLC
       159  Posigen, CT
       139  Tesla
        80  Venture Home Solar, LLC
        76  Earth Smart Solar
        74  SAVKAT, Inc.
        69  Green Power Energy, LLC
        38  Helio Solar LLC
        31  West Electric LLC
        29  Eastern CT Solar LLC
        25  Aegis Solar Energy
        25  Scale Microgrid Solutions LLC
        23  Ion Solar Pros
        23  Tesla Energy Operations, Inc.
        21  CES Danbury LLC DBA Ross Solar Group
        19  EcoSmart Home Services
        18  Infinity Solar Systems
        16  Premier Improvements Solar
        14  Honeywell International, Inc.
        11  EcoSolar Installations, LLC

CONTRACTOR_NAME by dollars
       81.10       25 rows  Scale Microgrid Solutions LLC
          25       14 rows  Honeywell International, Inc.
       22.70        8 rows  CPower
       11.14        6 rows  Kinsley Group, Inc.
        7.85      327 rows  Earthlight Technologies, LLC
        6.16        7 rows  RWE Clean Energy, LLC
        1.59      159 rows  Posigen, CT
        1.29        1 rows  EPC Energy Inc
        1.16       76 rows  Earth Smart Solar
        1.16      139 rows  Tesla
        0.98        2 rows  Waldron Engineering & Construction, Inc.
        0.95       80 rows  Venture Home Solar, LLC
        0.83       74 rows  SAVKAT, Inc.
        0.72       69 rows  Green Power Energy, LLC
        0.64        5 rows  Daisy Solutions, LLC
        0.62       31 rows  West Electric LLC
        0.56        1 rows  DownEast Renewable Energy LLC
        0.50        2 rows  HQCA Energy Solutions, LLC
        0.47       38 rows  Helio Solar LLC
        0.44       29 rows  Eastern CT Solar LLC

HOST_CITY by rows
        31  Stamford
        28  Waterbury
        24  Glastonbury
        24  Bridgeport
        23  Madison
        23  Fairfield
        23  Westport
        23  Newtown
        22  Stonington
        21  Greenwich
        21  West Hartford
        21  Monroe
        20  Ridgefield
        20  Manchester
        19  Mansfield
        18  New Haven
        17  Danbury
        17  Meriden
        17  Guilford
        17  Middletown

HOST_CITY by dollars
       18.04        6 rows  Suffield
        9.77       10 rows  Rocky Hill
        9.06       15 rows  Windsor
        8.61       17 rows  Middletown
        8.60       14 rows  Southington
        8.13       20 rows  Manchester
        5.86        7 rows  Windsor Locks
        5.51       17 rows  Danbury
        5.39       15 rows  Cheshire
        5.06       17 rows  Meriden
        4.75       13 rows  Enfield
        4.55       12 rows  Hamden
        3.92        5 rows  Plainfield
        3.10        4 rows  Seymour
        2.99        7 rows  Newington
        2.91       16 rows  Bristol
        2.41       14 rows  New Canaan
        2.31       31 rows  Stamford
        2.13       14 rows  Shelton
        2.12       13 rows  Stratford

STATE_HOUSE_DISTRICT by rows
       194  nan
        27  State House District 101
        26  State House District 112
        25  State House District 50
        25  State House District 64
        24  State House District 36
        22  State House District 41
        20  State House District 135
        20  State House District 53
        19  State House District 37
        18  State House District 111
        17  State House District 66
        16  State House District 19
        16  State House District 136
        15  State House District 114
        15  State House District 52
        15  State House District 23
        15  State House District 134
        15  State House District 60
        15  State House District 43

STATE_HOUSE_DISTRICT by dollars
       23.92       13 rows  State House District 61
       13.77      194 rows  nan
        9.76       15 rows  State House District 60
        8.50        4 rows  State House District 81
        7.93        5 rows  State House District 11
        7.04        5 rows  State House District 5
        5.96        9 rows  State House District 59
        5.88       10 rows  State House District 47
        5.58        7 rows  State House District 103
        5.40       15 rows  State House District 2
        4.98        9 rows  State House District 82
        4.95        6 rows  State House District 33
        3.13        6 rows  State House District 105
        3.10        9 rows  State House District 100
        3.07       10 rows  State House District 51
        2.74        6 rows  State House District 27
        2.44       12 rows  State House District 125
        2.33       25 rows  State House District 50
        2.15        9 rows  State House District 32
        2.12        8 rows  State House District 45

## who x when

PROJECT_NAME by ENERGIZE_DATE, dollars = TOTAL_SYSTEM_POWER_MW
  ESS-00053                                 2022:0
  ESS-00064                                 2022:0.01
  ESS-00066                                 2022:0.01
  ESS-00246                                 2022:0.01
  ESS-00248                                 2022:0.01
  ESS-00265                                 2022:0.01
  ESS-00266                                 2022:0.01
  ESS-00289                                 2022:0.01
  ESS-00292                                 2022:0.02
  ESS-00310                                 2023:0.01
  ESS-00361                                 2022:0.01
  ESS-00516                                 2023:0.01
  ESS-00551                                 2023:0.01
  ESS-00601                                 2023:0.01
  ESS-00699                                 2023:0.01
  ESS-01606                                 2025:3.98

CONTRACTOR_NAME by ENERGIZE_DATE, dollars = TOTAL_SYSTEM_POWER_MW
  Aegis Solar Energy                        2023:0.04 2024:0.04 2025:0.19 2026:0.02
  CES Danbury LLC DBA Ross Solar Group      2022:0.11 2023:0.10 2024:0.01
  Daisy Solutions, LLC                      2025:0.16
  Earth Smart Solar                         2022:0.01 2023:0.03 2024:0.12 2025:0.39 2026:0.36
  Earthlight Technologies, LLC              2022:0.08 2023:0.42 2024:0.96 2025:3.48 2026:0.87
  Eastern CT Solar LLC                      2022:0.01 2023:0.05 2024:0.13 2025:0.19
  EcoSmart Home Services                    2022:0.01 2023:0.03 2024:0.06 2025:0.08 2026:0.08
  EcoSolar Installations, LLC               2023:0.02 2024:0.02 2025:0.04 2026:0.05
  Green Power Energy, LLC                   2022:0.05 2023:0.15 2024:0.09 2025:0.20 2026:0.16
  HQCA Energy Solutions, LLC                2023:0.25 2024:0.25
  Helio Solar LLC                           2022:0.01 2023:0.09 2024:0.10 2025:0.06 2026:0.13
  Infinity Solar Systems                    2023:0 2024:0.01 2025:0.06 2026:0.06
  Ion Solar Pros                            2024:0.02 2025:0.12 2026:0.04
  Kinsley Group, Inc.                       2025:3.98
  Posigen, CT                               2024:0.07 2025:0.73
  Premier Improvements Solar                2024:0.01 2025:0.09 2026:0.05
  SAVKAT, Inc.                              2022:0.11 2023:0.26 2024:0.13 2025:0.10 2026:0.02
  Tesla                                     2021:0.02 2022:0.02 2023:0.33 2024:0.25 2025:0.21
  Tesla Energy Operations, Inc.             2025:0.02 2026:0.09
  Venture Home Solar, LLC                   2023:0.01 2024:0.03 2025:0.26 2026:0.22
  West Electric LLC                         2024:0.08 2025:0.29 2026:0.23

## what

PROJECT_COUNTER: 1 100%, 161 0%

STAGE: Project Complete 59%, Installation in Progress 23%, Pending DERMS 11%, Pending Payment 3%, Application Submitted 2%, Completion Rejected 1%, Completion Submitted 1%, Unenrolled 1%, Inspection Pass 0%, In Inspection 0%, Customer Unavailable 0%

PROJECT_STATUS: Completed 62%, Approved 36%, Submitted 2%, Inspection 0%

COUNTY: Capitol Planning Region 22%, nan 15%, Western Connecticut Planning R 14%, South Central Connecticut Plan 9%, Naugatuck Valley Planning Regi 8%, Greater Bridgeport Planning Re 7%, Southeastern Connecticut Plann 6%, Lower Connecticut River Valley 6%, Northwest Hills Planning Regio 4%, Northeastern Connecticut Plann 3%, Fairfield County 2%, Hartford County 2%

COG_NAME: Capitol 26%, Western CT 19%, South Central CT 12%, Naugatuck Valley 10%, Greater Bridgeport 8%, Southeastern CT 8%, Lower CT River Valley 7%, Northwest Hills 6%, Northeastern CT 4%, nan 0%

STATE_SENATE_DISTRICT: nan 25%, State Senate District 30 9%, State Senate District 33 8%, State Senate District 28 8%, State Senate District 12 8%, State Senate District 26 7%, State Senate District 35 7%, State Senate District 18 7%, State Senate District 7 6%, State Senate District 8 6%, State Senate District 4 5%, State Senate District 21 5%

CONGRESSIONAL_DISTRICT: CT2 24%, CT5 19%, CT4 17%, CT1 15%, nan 14%, CT3 12%

USDA_RURALITY: Eligible 71%, Not Eligible 29%, nan 0%

COST_MEMBERSHIP: True 58%, False 42%

VINTAGE_MSA_AMI_BAND: 120+ 51%, 100-120 15%, nan 15%, 80-100 10%, 60-80 6%, -60 3%, Unknown 0%

VINTAGE_MSA_SMI_BAND: 120+ 49%, 100-120 17%, nan 15%, 80-100 9%, 60-80 7%, -60 3%, Unknown 0%

VINTAGE_MSA_CRA_AMI_BAND: 120+ 41%, 80-120 34%, nan 15%, 50-80 8%, -50 2%

VINTAGE_MSA_CRA_SMI_BAND: 120+ 41%, 80-120 34%, nan 15%, 50-80 8%, -50 2%

VINTAGE_DISTRESSED: Not Distressed 77%, Distressed 20%, nan 2%

VINTAGE_VULNERABLE_COMMUNITY: Not Vulnerable 72%, Vulnerable 28%

VULNERABLE_COMMUNITY_CATEGORY: None 72%, Distressed 9%, LMI,CRA,Distressed 8%, LMI 6%, LMI,Distressed 4%, LMI,CRA 2%, CRA,Distressed 0%

VINTAGEEJCOMMUNITY: Not EJ Community 79%, EJ Community 20%, Unknown 0%

VINTAGEJUSTICE40: Not Justice 40 95%, Justice 40 5%

CRA_QUALIFIED: Not CRA 90%, CRA 10%

LMI_QUALIFIED: Not LMI 81%, LMI 19%

CRA_QUALIFIED_SMI: Not CRA 90%, CRA 10%

LMI_QUALIFIED_SMI: Not LMI 81%, LMI 19%

ELIGIBLE_SYSTEM_OWNER: Customer 82%, TPO 16%, nan 2%

THIRD_PARTY_OWNER: Home Owner 82%, Posigen 12%, nan 2%, Scale Microgrid Solutions LLC 2%, CPower 1%, ConEdison Clean Energy Busines 1%, Palmetto LightReach 0%, Sunwealth Power, Inc. 0%, SunPower 0%, HQCA Energy Solutions, LLC 0%, DownEast Renewable Energy LLC 0%

EDC: Eversource 86%, UI 14%

UTILITY_RATE_CODE: Rate 1 69%, nan 11%, Rate R 8%, Rate 5 4%, Rate RT 3%, Rate 56 2%, Rate 30 1%, Rate GST 1%, Rate 57 1%, Rate 37 1%, Rate 55 0%, Rate LPT 0%

SECTOR: Residential 94%, C&I 6%

CUSTOMER_TYPE: 1-4 Residential Units 94%, Large C&I 3%, Medium C&I 2%, Small C&I 1%, 5+ Residential Units 0%

CUSTOMER_CLASS: nan 94%, Large C&I 3%, Medium C&I 2%, Small C&I 1%, NULL 0%

NAICS_CODE: nan 94%, "44-45	Retail Trade" 2%, "31-33	Manufacturing" 1%, "61	Educational Services" 1%, "53	Real Estate Rental and Lea 1%, "48-49	Transportation and Ware 1%, "81	Other Services (except Pub 0%, "54	Professional, Scientific,  0%, "92	Public Administration" 0%, "42	Wholesale Trade" 0%, "71	Arts, Entertainment, and R 0%, "11	Agriculture, Forestry, Fis 0%

RESI_CUSTOMER_TYPE: Resi Standard 72%, Resi Underserved 15%, N/A 6%, Resi Low Income and Underserve 4%, Resi Low Income 3%

PRIORITY_CUSTOMER_INDICATOR: True 59%, False 41%

PRIORITY_CUSTOMER: N/A 41%, Grid Edge (C&I and Residential 39%, Underserved Community 13%, LMI 6%, Small Business 1%, Critical Facility 1%

CRITICAL_FACILITIES: nan 94%, No 5%, Yes 1%

GRID_EDGE: False 56%, True 44%

SMALL_BUSINESS: False 99%, True 1%

UNDERSERVED: No 79%, Yes 21%, nan 0%

FCM_PARTICIPANT: nan 97%, No 3%, Yes 0%

ON_SITE_FOSSIL_FUEL: nan 94%, No 6%

PROGRAM_DISPATCH: Active and Passive 85%, Only Active 12%, Construct 5 2%

INSTALLED_LOCATION: Outdoors 50%, Indoors 18%, Garage 14%, nan 11%, Basement 8%

SYSTEM_PAIRING_ORIGINAL: Paired with new on-site genera 49%, Paired with existing on-site g 35%, nan 11%, Standalone (not paired with an 6%

SYSTEM_PAIRING: Paired with solar PV 84%, N/A 11%, Standalone 6%

SALESTAXESGENERATED: 0.00 95%, nan 5%

COMMERCIAL_PROPORTION: 0.0 61%, nan 39%, 52.0 0%

RESIDENTIAL_SECTOR: 1-4 Units 94%, nan 6%, 5+ Units 0%

LOW_INCOME: No 76%, nan 17%, Yes 8%

PRE_EXISTING_STORAGE_SYSTEM: False 85%, True 15%

HYBRID_SECTOR_PROJECT: False 100%, True 0%

OPPORTUNITY_ZONE: nan 99%, Eligible 1%

MULTIFAMILY_AFFORDABLE_HOUSING: nan 100%, No 0%, Yes 0%

RESIDENTIAL_PROPORTION: nan 100%, 48.0 0%

NUMBER_OF_RESIDENTIAL_UNITS: nan 100%, 1.0 0%, 161.0 0%

COMMERCIAL_INCENTIVE_FOR: nan 100%, 955500.00 0%

RESIDENTIAL_INCENTIVE_FOR: nan 100%, 882000.00 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PROJECT_NAME | who | 1.4K | 0 | ESS-05050 7; ESS-05049 7; ESS-05048 7; ESS-05047 7 |
| PROJECT_COUNTER | category | 2 | 0 | 1 1.4K; 161 1 |
| STAGE | category | 11 | 0 | Project Complete 803; Installation in Progress 308; Pending DERMS 151; Pending Payment 38 |
| PROJECT_STATUS | category | 4 | 0 | Completed 851; Approved 486; Submitted 26; Inspection 4 |
| HOST_CITY | who | 161 | 0 | Stamford 31; Waterbury 28; Bridgeport 24; Glastonbury 24 |
| HOST_ZIP | other | 237 | 0 | 06443 23; 06880 23; 06468 21; 06877 20 |
| LATITUDE | amount | 120 | 0 | nan 194; 41.3300000000 34; 41.3100000000 26; 41.3000000000 24 |
| LONGITUDE | amount | 201 | 0 | nan 194; -72.6600000000 17; -72.7600000000 14; -72.8900000000 14 |
| CENSUS_TRACT_CODE | other | 512 | 0 | nan 197; 194201.0 11; 100300.0 10; 707100.0 9 |
| COUNTY | category | 17 | 0 | Capitol Planning Region 284; nan 199; Western Connecticut Plann 185; South Central Connecticut 121 |
| COG_NAME | category | 10 | 0 | Capitol 356; Western CT 253; South Central CT 158; Naugatuck Valley 139 |
| STATE_HOUSE_DISTRICT | who | 146 | 0 | nan 194; State House District 101 27; State House District 112 26; State House District 64 25 |
| STATE_SENATE_DISTRICT | category | 37 | 0 | nan 194; State Senate District 30 67; State Senate District 33 59; State Senate District 28 58 |
| CONGRESSIONAL_DISTRICT | category | 6 | 0 | CT2 333; CT5 253; CT4 226; CT1 201 |
| USDA_RURALITY | category | 3 | 0 | Eligible 964; Not Eligible 400; nan 3 |
| COST_MEMBERSHIP | category | 3 | 3 | True 792; False 572 |
| VINTAGE_MSA_AMI_BAND | category | 7 | 0 | 120+ 693; 100-120 211; nan 201; 80-100 133 |
| VINTAGE_MSA_SMI_BAND | category | 7 | 0 | 120+ 666; 100-120 239; nan 201; 80-100 120 |
| VINTAGE_MSA_CRA_AMI_BAND | category | 5 | 0 | 120+ 565; 80-120 468; nan 201; 50-80 104 |
| VINTAGE_MSA_CRA_SMI_BAND | category | 5 | 0 | 120+ 565; 80-120 468; nan 201; 50-80 104 |
| VINTAGE_DISTRESSED | category | 3 | 0 | Not Distressed 1.1K; Distressed 279; nan 29 |
| VINTAGE_EJ_POVERTY_LEVEL | other | 1 | 0 | False 1.4K |
| VINTAGE_VULNERABLE_COMMUNITY | category | 2 | 0 | Not Vulnerable 988; Vulnerable 379 |
| VULNERABLE_COMMUNITY_CATEGORY | category | 7 | 0 | None 988; Distressed 119; LMI,CRA,Distressed 109; LMI 77 |
| VINTAGEEJCOMMUNITY | category | 3 | 0 | Not EJ Community 1.1K; EJ Community 279; Unknown 3 |
| VINTAGEJUSTICE40 | category | 2 | 0 | Not Justice 40 1.3K; Justice 40 72 |
| CRA_QUALIFIED | category | 2 | 0 | Not CRA 1.2K; CRA 133 |
| LMI_QUALIFIED | category | 2 | 0 | Not LMI 1.1K; LMI 258 |
| CRA_QUALIFIED_SMI | category | 2 | 0 | Not CRA 1.2K; CRA 133 |
| LMI_QUALIFIED_SMI | category | 2 | 0 | Not LMI 1.1K; LMI 257 |
| CONTRACTOR_NAME | who | 69 | 0 | Earthlight Technologies,  327; Posigen, CT 159; Tesla 139; Venture Home Solar, LLC 80 |
| ELIGIBLE_SYSTEM_OWNER | category | 3 | 0 | Customer 1.1K; TPO 213; nan 32 |
| THIRD_PARTY_OWNER | category | 11 | 0 | Home Owner 1.1K; Posigen 159; nan 32; Scale Microgrid Solutions 27 |
| EDC | category | 2 | 0 | Eversource 1.2K; UI 190 |
| UTILITY_RATE_CODE | category | 19 | 0 | Rate 1 933; nan 145; Rate R 114; Rate 5 48 |
| SECTOR | category | 2 | 0 | Residential 1.3K; C&I 81 |
| CUSTOMER_TYPE | category | 5 | 0 | 1-4 Residential Units 1.3K; Large C&I 39; Medium C&I 27; Small C&I 15 |
| CUSTOMER_CLASS | category | 5 | 0 | nan 1.3K; Large C&I 39; Medium C&I 27; Small C&I 15 |
| NAICS_CODE | category | 13 | 0 | nan 1.3K; "44-45	Retail Trade" 22; "31-33	Manufacturing" 15; "61	Educational Services" 14 |
| RESI_CUSTOMER_TYPE | category | 5 | 0 | Resi Standard 981; Resi Underserved 202; N/A 81; Resi Low Income and Under 61 |
| PRIORITY_CUSTOMER_INDICATOR | category | 2 | 0 | True 806; False 561 |
| PRIORITY_CUSTOMER | category | 6 | 0 | N/A 561; Grid Edge (C&I and Reside 532; Underserved Community 172; LMI 77 |
| CRITICAL_FACILITIES | category | 3 | 0 | nan 1.3K; No 73; Yes 12 |
| GRID_EDGE | category | 3 | 148 | False 685; True 534 |
| SMALL_BUSINESS | category | 2 | 0 | False 1.4K; True 15 |
| UNDERSERVED | category | 3 | 0 | No 1.1K; Yes 282; nan 1 |
| FCM_PARTICIPANT | category | 3 | 0 | nan 1.3K; No 36; Yes 5 |
| ON_SITE_FOSSIL_FUEL | category | 2 | 0 | nan 1.3K; No 82 |
| PROGRAM_DISPATCH | category | 3 | 0 | Active and Passive 1.2K; Only Active 167; Construct 5 34 |
| TOTAL_SYSTEM_POWER_KW | amount | 91 | 0 | 20.00000000 210; 10.00000000 178; 7.60000000 165; 11.50000000 108 |
| TOTAL_SYSTEM_POWER_MW | amount | 90 | 0 | 0.0200000000000 210; 0.0100000000000 178; 0.0076000000000 165; 0.0115000000000 108 |
| TOTAL_SYSTEM_POWER_WATTS | amount | 90 | 0 | 20000.00000000 210; 10000.00000000 178; 7600.00000000 165; 11500.00000000 108 |
| TOTAL_SYSTEM_ENERGY_CAPACITY | amount | 100 | 0 | 30.00000000 209; 18.00000000 180; 27.00000000 111; 15.00000000 87 |
| TOTAL_SYSTEM_MAX_CONT | amount | 61 | 0 | 0E-8 366; 9.00000000 172; 10.00000000 146; 20.00000000 145 |
| TOTAL_SYSTEM_QUANTITY | amount | 21 | 0 | 2.00000000 589; 4.00000000 361; 6.00000000 109; 1.00000000 105 |
| ANNUAL_PEAK_DEMAND_KW | amount | 79 | 0 | nan 1.3K; 3823.00000000 2; 60.00000000 2; 322.00000000 2 |
| INSTALLED_LOCATION | category | 5 | 0 | Outdoors 677; Indoors 241; Garage 191; nan 147 |
| SYSTEM_PAIRING_ORIGINAL | category | 4 | 0 | Paired with new on-site g 664; Paired with existing on-s 479; nan 145; Standalone (not paired wi 79 |
| SYSTEM_PAIRING | category | 3 | 0 | Paired with solar PV 1.1K; N/A 145; Standalone 79 |
| UP_FRONT_INCENTIVE | amount | 230 | 0 | nan 165; 7500.00 81; 16000.00 70; 10800.00 64 |
| BATTERIES_STORAGE_COST | amount | 572 | 0 | 0.00000000 188; 22416.00000000 132; 11941.00000000 29; 30000.00000000 22 |
| ENGINEERING_AND_DESIGN_COST | amount | 145 | 0 | 1000.00000000 381; 0.00000000 344; 300.00000000 136; 500.00000000 120 |
| INSTALLATION_LABOR_COST | amount | 392 | 0 | 0.00000000 320; 2400.00000000 132; 3000.00000000 67; 4000.00000000 49 |
| INTERCONNECTION_COST | amount | 151 | 0 | 0.00000000 346; 200.00000000 184; 500.00000000 166; 663.00000000 94 |
| INVERTER_COST | amount | 8 | 0 | 0.00000000 1.3K; nan 20; 10000.00000000 1; 2500.00000000 1 |
| MONITORING_COST | amount | 7 | 0 | 0.00000000 1.3K; nan 19; 500.00000000 2; 16200.00000000 1 |
| PERMITTING_COST | amount | 219 | 0 | 0.00000000 345; 800.00000000 308; 550.00000000 100; 500.00000000 85 |
| SOLAR_PV_INVERTER_S_COST | amount | 6 | 0 | 0.00000000 1.3K; nan 26; 2500.00000000 1; 1800.00000000 1 |
| BALANCE_OF_SYSTEM_COST | amount | 425 | 0 | 0.00000000 452; 2000.00000000 174; nan 47; 5000.00000000 28 |
| TOTAL_BATTERY_COST | amount | 750 | 0 | 0.00000000 153; 27866.00000000 82; 31975.00000000 19; 35995.00000000 18 |
| TOTAL_CONTRACT_PRICE | amount | 1.0K | 0 | 0.00000000 154; 27866.00000000 83; 11355.24000000 13; 5660460.00000000 12 |
| GROSS_COST | amount | 750 | 0 | 0.00000000 153; 27866.00000000 82; 31975.00000000 19; 35995.00000000 18 |
| TOTAL_CAPITAL_DEPLOYED | amount | 750 | 0 | 0.00000000 153; 27866.00000000 82; 31975.00000000 19; 35995.00000000 18 |
| CGB_INCENTIVE_AMOUNT | amount | 230 | 0 | nan 165; 7500.00 81; 16000.00 70; 10800.00 64 |
| TOTAL_CGB_INVESTMENT | amount | 230 | 0 | nan 165; 7500.00 81; 16000.00 70; 10800.00 64 |
| TOTAL_PRIVATE_INVESTMENT | amount | 916 | 0 | 0.00000000 153; 17066.00000000 43; 19766.00000000 37; 10905.24000000 13 |
| TOTAL_INVESTMENT | amount | 750 | 0 | 0.00000000 153; 27866.00000000 82; 31975.00000000 19; 35995.00000000 18 |
| INCENTIVE_STEP | amount | 5 | 0 | 1.00 889; 1.20 330; nan 82; 2.00 35 |
| CREATED_DATE | date | 1.3K | 0 | 2025-12-05T16:43:37.000 37; 2025-06-06T16:33:00.000 35; 2024-10-02T17:46:41.000 32; 2024-09-25T15:55:18.000 29 |
| APPLICATION_DATE | date | 542 | 0 | nan 99; 2025-06-06T00:00:00.000 38; 2025-09-26T00:00:00.000 30; 2024-10-18T00:00:00.000 20 |
| SUBMITTED_DATE | date | 497 | 0 | nan 203; 2025-09-26T00:00:00.000 29; 2024-09-05T00:00:00.000 23; 2024-10-18T00:00:00.000 20 |
| APPROVAL_DATE | date | 383 | 0 | nan 65; 2026-03-31T00:00:00.000 32; 2024-09-20T00:00:00.000 27; 2025-11-26T00:00:00.000 23 |
| INDIVIDUALINCOMETAXESGENERATED | amount | 735 | 0 | 0.00 110; 406.04 82; nan 66; 465.91 19 |
| CORPORATETAXESGENERATED | amount | 738 | 0 | 0.00 110; 610.18 82; nan 66; 700.16 19 |
| SALESTAXESGENERATED | category | 2 | 0 | 0.00 1.3K; nan 66 |
| TOTALTAXREVENUEGENERATED | amount | 734 | 0 | 0.00 175; 1016.22 82; 1166.07 19; 1312.66 18 |
| DIRECT_JOBS | amount | 77 | 0 | 0.07 208; 0.08 168; 0.09 166; 0.05 116 |
| INDIRECT_AND_INDUCED_JOBS | amount | 79 | 0 | 0.09 205; 0.10 171; 0.11 130; 0.00 110 |
| TOTAL_JOBS | amount | 94 | 0 | 0.00 176; 0.16 150; 0.18 112; 0.20 108 |
| EXPECTEDUSEFULLIFE | other | 1 | 0 | 25 1.4K |
| KWH_KW | amount | 89 | 0 | 1.50 310; 2.37 162; 2.72 150; 1.17 88 |
| COST_KW | amount | 793 | 0 | 0.00 155; 3666.58 82; 1598.75 19; 1799.75 18 |
| COST_KWH | amount | 785 | 0 | 0.00 154; 1548.11 82; 1065.83 19; 1199.83 18 |
| COMMERCIAL_PROPORTION | category | 3 | 0 | 0.0 838; nan 527; 52.0 2 |
| RESIDENTIAL_SECTOR | category | 3 | 0 | 1-4 Units 1.3K; nan 81; 5+ Units 1 |
| LOW_INCOME | category | 3 | 0 | No 1.0K; nan 227; Yes 104 |
| PAIRED_PV_SYSTEM_SIZE | amount | 165 | 0 | nan 259; 8.00 94; 10.00 89; 7.00 81 |
| TOTAL_SOLAR_PV_COST | amount | 658 | 0 | 0.00000000 409; nan 281; 852720.00000000 5; 11000.00000000 5 |
| ENERGIZE_DATE | date | 534 | 0 | nan 408; 2025-06-26T00:00:00.000 13; 2025-12-31T00:00:00.000 11; 2025-06-27T00:00:00.000 10 |
| COMPLETED_DATE | date | 215 | 0 | nan 591; 2026-03-31T00:00:00.000 69; 2025-11-04T00:00:00.000 62; 2025-12-10T00:00:00.000 50 |
| PRE_EXISTING_STORAGE_SYSTEM | category | 3 | 40 | False 1.1K; True 195 |
| HYBRID_SECTOR_PROJECT | category | 3 | 728 | False 637; True 2 |
| OPPORTUNITY_ZONE | category | 2 | 0 | nan 1.3K; Eligible 18 |
| MULTIFAMILY_AFFORDABLE_HOUSING | category | 3 | 0 | nan 1.4K; No 4; Yes 2 |
| RESIDENTIAL_PROPORTION | category | 2 | 0 | nan 1.4K; 48.0 2 |
| NUMBER_OF_RESIDENTIAL_UNITS | category | 3 | 0 | nan 1.4K; 1.0 2; 161.0 2 |
| COMMERCIAL_INCENTIVE_FOR | category | 2 | 0 | nan 1.4K; 955500.00 2 |
| RESIDENTIAL_INCENTIVE_FOR | category | 2 | 0 | nan 1.4K; 882000.00 2 |
| INGESTED_AT | audit date | 1 | 0 | 2026-06-24 05:47:43.58715 1.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 576edd76-879d-4a7a-961d-2 1.4K |
| SRC_SHA256 | who | 1 | 0 | 82dbe6d7521b171b2142372d1 1.4K |
