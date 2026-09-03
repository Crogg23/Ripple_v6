# FED_EPA_EGRID_PLANT_2022

rows 12.0K  columns 144  scan 6.2s

roles: amount 94, audit 2, category 24, id 1, other 13, state 1, who 9

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PLANT_LATITUDE | 12.0K | 17.95 | 39.69 | 57.39 | 71.29 | 465.7K |
| PLANT_LONGITUDE | 12.0K | -171.71 | -90.19 | -69.70 | -65.28 | -1.12M |
| PLANT_CAPACITY_FACTOR | 11.7K | 0 | 0.21 | 0.88 | 1.18 | 2.9K |
| PLANT_NAMEPLATE_CAPACITY_MW | 12.0K | 0 | 6.20 | 1.7K | 6.8K | 1.28M |
| NONBASELOAD_FACTOR | 3.4K | 0 | 0.97 | 1 | 1 | 2.5K |
| CHP_PLANT_USEFUL_THERMAL_OUTPUT_MMBTU | 1.0K | 0 | 229.1K | 17.16M | 26.65M | 2.07B |

## who

PLANT_NAME by rows
         2  River Road
         2  Morgantown
         2  Columbia
         2  Harmony Solar
         2  Dover
         2  Bedford Solar
         2  Yuba City Energy Center
         2  Quincy Solar
         2  Jefferson Solar
         2  Franklin Solar
         2  Bear Creek Solar
         2  Bliss
         2  Cascade Dam
         2  Biomass to Energy Facility, Kauai
         2  Smithfield Packaged Meats Corp.
         2  Independence
         2  Indian River
         2  Marshall
         2  Beaver Dam
         2  Bear Creek

PLANT_NAME by dollars
       97.48        2 rows  Marshall
       90.39        2 rows  River Road
       87.62        2 rows  Mystic
       87.44        2 rows  Cascade Dam
       85.45        2 rows  Bliss
       83.92        2 rows  Wilson Solar
       83.73        2 rows  Bear Creek
       82.75        2 rows  Dover
       82.45        2 rows  Columbia
       82.38        2 rows  Franklin Solar
       80.53        2 rows  River Bend Solar, LLC
       79.18        2 rows  Independence
       78.53        2 rows  Morgantown
       78.28        2 rows  Yuba City Energy Center
       78.03        2 rows  Beaver Dam
       76.30        2 rows  Oak Grove
       76.01        2 rows  Jefferson Solar
       74.84        2 rows  Anadarko
       74.71        2 rows  Quincy Solar
       74.45        2 rows  Richland

UTILITY_NAME by rows
       211  AES Distributed Energy
       184  Cypress Creek Renewables
       153  MN8 Energy LLC
       142  Strata Manager, LLC
       121  Greenbacker Renewable Energy Corporation
        98  Altus Power America Management, LLC
        89  Walmart Stores Texas, LLC
        84  Duke Energy Renewables Services
        84  Tesla Inc.
        77  Consolidated Edison Development Inc.
        75  Bloom Energy
        75  Pacific Gas & Electric Co.
        74  Nautilus Solar Solutions
        71  Erie Boulevard Hydropower LP
        70  Florida Power & Light Co
        67  Eagle Creek Renewable Energy, LLC
        64  Avangrid Renewables LLC
        64  Standard Solar
        63  Southern California Edison Co
        62  PacifiCorp

UTILITY_NAME by dollars
        8.0K      211 rows  AES Distributed Energy
        6.7K      184 rows  Cypress Creek Renewables
        5.8K      153 rows  MN8 Energy LLC
        5.1K      142 rows  Strata Manager, LLC
        4.8K      121 rows  Greenbacker Renewable Energy Corporation
        3.9K       98 rows  Altus Power America Management, LLC
        3.3K       84 rows  Tesla Inc.
        3.1K       71 rows  Erie Boulevard Hydropower LP
        3.1K       74 rows  Nautilus Solar Solutions
        3.0K       77 rows  Consolidated Edison Development Inc.
        3.0K       84 rows  Duke Energy Renewables Services
        2.9K       75 rows  Pacific Gas & Electric Co.
        2.8K       67 rows  Eagle Creek Renewable Energy, LLC
        2.8K       75 rows  Bloom Energy
        2.7K       64 rows  Standard Solar
        2.7K       89 rows  Walmart Stores Texas, LLC
        2.7K       62 rows  PacifiCorp
        2.6K       64 rows  Avangrid Renewables LLC
        2.3K       57 rows  U S Bureau of Reclamation
        2.3K       55 rows  MidAmerican Energy Co

PLANT_TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_NAME by rows
       585  Southern California Edison Co
       509  Pacific Gas & Electric Co
       500  Northern States Power Co - Minnesota
       406  Duke Energy Progress - (NC)
       331  Niagara Mohawk Power Corp.
       331  Duke Energy Carolinas, LLC
       298  Massachusetts Electric Co
       231  PacifiCorp
       227  Virginia Electric & Power Co
       194  Public Service Elec & Gas Co
       186  Oncor Electric Delivery Company LLC
       182  NSTAR Electric Company
       179  Commonwealth Edison Co
       176  Georgia Power Co
       171  Pacific Gas & Electric Co.
       147  Public Service Co of Colorado
       139  New York State Elec & Gas Corp
       121  Idaho Power Co
       118  Jersey Central Power & Lt Co
       116  CenterPoint Energy

PLANT_TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_NAME by dollars
       22.4K      500 rows  Northern States Power Co - Minnesota
       20.2K      585 rows  Southern California Edison Co
       19.2K      509 rows  Pacific Gas & Electric Co
       14.3K      331 rows  Niagara Mohawk Power Corp.
       14.3K      406 rows  Duke Energy Progress - (NC)
       12.6K      298 rows  Massachusetts Electric Co
       11.7K      331 rows  Duke Energy Carolinas, LLC
        9.7K      231 rows  PacifiCorp
        8.4K      227 rows  Virginia Electric & Power Co
        7.8K      194 rows  Public Service Elec & Gas Co
        7.6K      182 rows  NSTAR Electric Company
        7.5K      179 rows  Commonwealth Edison Co
        6.3K      171 rows  Pacific Gas & Electric Co.
        6.0K      186 rows  Oncor Electric Delivery Company LLC
        5.9K      139 rows  New York State Elec & Gas Corp
        5.8K      147 rows  Public Service Co of Colorado
        5.8K      176 rows  Georgia Power Co
        5.2K      121 rows  Idaho Power Co
        4.8K      118 rows  Jersey Central Power & Lt Co
        4.4K       97 rows  Bonneville Power Administration

BALANCING_AUTHORITY_NAME by rows
      2.0K  Midcontinent Independent Transmission System Operator, Inc..
      1.6K  PJM Interconnection, LLC
      1.4K  California Independent System Operator
      1.2K  ISO New England Inc.
       791  New York Independent System Operator
       664  Electric Reliability Council of Texas, Inc.
       643  Southwest Power Pool
       424  Duke Energy Carolinas
       420  Duke Energy Progress East
       314  Southern Company Services, Inc. - Trans
       237  No balancing authority
       162  PacifiCorp - East
       156  Public Service Company of Colorado
       132  Western Area Power Administration - Rocky Mountain Region
       128  Bonneville Power Administration
       123  Tennessee Valley Authority
       121  Idaho Power Company
       107  PacifiCorp - West
        93  Los Angeles Department of Water and Power
        93  Nevada Power Company

BALANCING_AUTHORITY_NAME by dollars
       85.2K     2.0K rows  Midcontinent Independent Transmission System Operator, Inc..
       64.2K     1.6K rows  PJM Interconnection, LLC
       51.8K     1.4K rows  California Independent System Operator
       50.1K     1.2K rows  ISO New England Inc.
       33.6K      791 rows  New York Independent System Operator
       24.7K      643 rows  Southwest Power Pool
       20.4K      664 rows  Electric Reliability Council of Texas, Inc.
       15.0K      424 rows  Duke Energy Carolinas
       14.8K      420 rows  Duke Energy Progress East
       10.5K      237 rows  No balancing authority
       10.2K      314 rows  Southern Company Services, Inc. - Trans
        6.6K      162 rows  PacifiCorp - East
        6.2K      156 rows  Public Service Company of Colorado
        5.8K      128 rows  Bonneville Power Administration
        5.3K      132 rows  Western Area Power Administration - Rocky Mountain Region
        5.2K      121 rows  Idaho Power Company
        4.7K      107 rows  PacifiCorp - West
        4.4K      123 rows  Tennessee Valley Authority
        3.8K       84 rows  Portland General Electric Company
        3.5K       93 rows  Nevada Power Company

## where

PLANT_STATE_ABBREVIATION: CA 1.7K, NC 875, NY 821, TX 754, MN 724, MA 600, NJ 368, IL 328, IA 283, MI 266, OR 265, CO 265

## what

DATA_YEAR: 2022 100%, YEAR 0%

PLANT_LEVEL_SECTOR: IPP Non-CHP 61%, Electric Utility 27%, Commercial Non-CHP 4%, Industrial CHP 4%, Commercial CHP 2%, IPP CHP 2%, Industrial Non-CHP 2%, SECTOR 0%

NERC_REGION_ACRONYM: WECC 26%, SERC 20%, NPCC 16%, MRO 15%, RFC 15%, TRE 6%, AK 1%, HI 1%, PR 1%, NERC 0%

EGRID_SUBREGION_ACRONYM: CAMX 16%, MROW 13%, SRVC 12%, NEWE 12%, NWPP 8%, RFCW 8%, RFCE 8%, ERCT 7%, NYUP 6%, AZNM 4%, SRSO 3%, RMPA 3%

EGRID_SUBREGION_NAME: WECC California 16%, MRO West 13%, SERC Virginia/Carolina 12%, NPCC New England 12%, WECC Northwest 8%, RFC West 8%, RFC East 8%, ERCOT All 7%, NPCC Upstate NY 6%, WECC Southwest 4%, SERC South 3%, WECC Rockies 3%

PLANT_ASSOCIATED_ISO_RTO_TERRITORY: MISO 26%, PJM 21%, CAISO 19%, ISONE 15%, NYISO 10%, ERCOT 9%, SPP 0%, ISORTO 0%

CAMD_PROGRAM_FLAG: Yes 100%, CAMDFLAG 0%

NUMBER_OF_UNITS: 1 62%, 2 15%, 3 9%, 4 6%, 5 3%, 6 2%, 8 1%, 7 1%, 9 0%, 10 0%, 12 0%, 11 0%

NUMBER_OF_GENERATORS: 1 62%, 2 14%, 3 9%, 4 6%, 5 3%, 6 2%, 8 1%, 7 1%, 9 1%, 10 0%, 12 0%, 11 0%

PLANT_PRIMARY_FUEL: SUN 44%, NG 17%, WAT 13%, WND 11%, DFO 7%, LFG 3%, MWH 2%, SUB 1%, WDS 1%, BIT 1%, OBG 1%, BLQ 1%

PLANT_PRIMARY_FUEL_CATEGORY: SOLAR 42%, GAS 17%, HYDRO 12%, WIND 11%, OIL 7%, BIOMASS 5%, COAL 2%, OTHF 2%, GEOTHERMAL 1%, NUCLEAR 0%, OFSL 0%, PLFUELCT 0%

FLAG_INDICATING_IF_THE_PLANT_BURNED_OR_GENERATED_ANY_AMOUNT_OF_COAL: Yes 100%, COALFLAG 0%

BIOGAS_BIOMASS_PLANT_ADJUSTMENT_FLAG: Yes 100%, RMBMFLAG 0%

COMBINED_HEAT_AND_POWER_CHP_PLANT_ADJUSTMENT_FLAG: Yes 100%, CHPFLAG 0%

PLANT_PUMPED_STORAGE_FLAG: Yes 98%, PSFLAG 2%

PLANT_UNADJUSTED_ANNUAL_NOX_EMISSIONS_SOURCE: EIA 63%, EPA/CAMD 35%, EPA/CAMD; EIA 2%, UNNOXSRC 0%

PLANT_UNADJUSTED_OZONE_SEASON_NOX_EMISSIONS_SOURCE: EIA 63%, EPA/CAMD 36%, EPA/CAMD; EIA 1%, UNNOZSRC 0%

PLANT_UNADJUSTED_ANNUAL_SO2_EMISSIONS_SOURCE: EIA 64%, EPA/CAMD 34%, EPA/CAMD; EIA 1%, UNSO2SRC 0%

PLANT_UNADJUSTED_ANNUAL_CO2_EMISSIONS_SOURCE: EIA 66%, EPA/CAMD 33%, EPA/CAMD; EIA 1%, UNCO2SRC 0%

PLANT_UNADJUSTED_ANNUAL_CH4_EMISSIONS_SOURCE: EIA 100%, UNCH4SRC 0%

PLANT_UNADJUSTED_ANNUAL_N2O_EMISSIONS_SOURCE: EIA 100%, UNN2OSRC 0%

PLANT_UNADJUSTED_ANNUAL_HG_EMISSIONS_SOURCE: -- 100%, UNHGSRC 0%

PLANT_UNADJUSTED_ANNUAL_HEAT_INPUT_SOURCE: EIA 89%, EPA/CAMD 11%, EPA/CAMD; EIA 1%, UNHTISRC 0%

PLANT_UNADJUSTED_OZONE_SEASON_HEAT_INPUT_SOURCE: EIA 89%, EPA/CAMD 11%, EPA/CAMD; EIA 0%, UNHOZSRC 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PLANT_FILE_SEQUENCE_NUMBER | id | 11.9K | 0 | 11973 60; 11972 60; 11971 60; 11970 60 |
| DATA_YEAR | category | 2 | 0 | 2022 12.0K; YEAR 1 |
| PLANT_STATE_ABBREVIATION | state | 53 | 0 | CA 1.7K; NC 875; NY 821; TX 754 |
| PLANT_NAME | who | 11.9K | 0 | Wyodak 60; Wygen III 60; Wygen II 60; Wygen I 60 |
| DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE | who | 11.8K | 0 | 6101 60; 56596 60; 56319 60; 55479 60 |
| PLANT_TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_NAME | who | 1.0K | 60 | Southern California Ediso 585; Pacific Gas & Electric Co 509; Northern States Power Co  505; Duke Energy Progress - (N 413 |
| PLANT_TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_ID | who | 1.0K | 0 | 14328 687; 17609 585; 13781 505; 3046 416 |
| UTILITY_NAME | who | 5.2K | 0 | AES Distributed Energy 211; Cypress Creek Renewables 198; Strata Manager, LLC 163; MN8 Energy LLC 153 |
| UTILITY_ID | other | 5.1K | 0 | 61012 211; 61060 198; 64778 163; 61944 153 |
| PLANT_LEVEL_SECTOR | category | 8 | 60 | IPP Non-CHP 7.2K; Electric Utility 3.2K; Commercial Non-CHP 484; Industrial CHP 429 |
| BALANCING_AUTHORITY_NAME | who | 68 | 0 | Midcontinent Independent  2.0K; PJM Interconnection, LLC 1.6K; California Independent Sy 1.4K; ISO New England Inc. 1.2K |
| BALANCING_AUTHORITY_CODE | other | 68 | 237 | MISO 2.0K; PJM 1.6K; CISO 1.4K; ISNE 1.2K |
| NERC_REGION_ACRONYM | category | 10 | 0 | WECC 3.1K; SERC 2.4K; NPCC 2.0K; MRO 1.9K |
| EGRID_SUBREGION_ACRONYM | category | 28 | 0 | CAMX 1.6K; MROW 1.3K; SRVC 1.2K; NEWE 1.2K |
| EGRID_SUBREGION_NAME | category | 28 | 0 | WECC California 1.6K; MRO West 1.3K; SERC Virginia/Carolina 1.2K; NPCC New England 1.2K |
| PLANT_ASSOCIATED_ISO_RTO_TERRITORY | category | 8 | 4.3K | MISO 2.0K; PJM 1.6K; CAISO 1.4K; ISONE 1.2K |
| PLANT_FIPS_STATE_CODE | other | 53 | 0 | 06 1.7K; 37 875; 36 821; 48 754 |
| PLANT_FIPS_COUNTY_CODE | other | 256 | 35 | 037 370; 001 340; 029 339; 027 330 |
| PLANT_COUNTY_NAME | who | 1.4K | 24 | Los Angeles 235; Kern 205; Worcester 184; San Bernardino 133 |
| PLANT_LATITUDE | amount | 11.5K | 0 | 44.2919 61; 38.0878 61; 44.290128 60; 44.2858 60 |
| PLANT_LONGITUDE | amount | 11.5K | 0 | -105.3833 61; -80.4925 61; -105.381482 60; -105.3806 60 |
| CAMD_PROGRAM_FLAG | category | 2 | 10.6K | Yes 1.3K; CAMDFLAG 1 |
| NUMBER_OF_UNITS | category | 37 | 0 | 1 7.4K; 2 1.8K; 3 1.1K; 4 683 |
| NUMBER_OF_GENERATORS | category | 37 | 0 | 1 7.4K; 2 1.7K; 3 1.1K; 4 669 |
| PLANT_PRIMARY_FUEL | category | 35 | 14 | SUN 5.1K; NG 2.0K; WAT 1.5K; WND 1.3K |
| PLANT_PRIMARY_FUEL_CATEGORY | category | 12 | 14 | SOLAR 5.1K; GAS 2.0K; HYDRO 1.5K; WIND 1.3K |
| FLAG_INDICATING_IF_THE_PLANT_BURNED_OR_GENERATED_ANY_AMOUNT_OF_COAL | category | 2 | 11.7K | Yes 305; COALFLAG 1 |
| PLANT_CAPACITY_FACTOR | amount | 9.3K | 269 | 0 588; 0.00025 57; 0.45535 56; 0.7924 56 |
| PLANT_NAMEPLATE_CAPACITY_MW | amount | 2.1K | 0 | 1 749; 2 741; 5 694; 3 323 |
| NONBASELOAD_FACTOR | amount | 1.6K | 8.5K | 1 1.7K; 0 193; 0.574418459913337 8; 0.0126620479714479 8 |
| BIOGAS_BIOMASS_PLANT_ADJUSTMENT_FLAG | category | 2 | 11.3K | Yes 693; RMBMFLAG 1 |
| COMBINED_HEAT_AND_POWER_CHP_PLANT_ADJUSTMENT_FLAG | category | 2 | 10.9K | Yes 1.1K; CHPFLAG 1 |
| CHP_PLANT_USEFUL_THERMAL_OUTPUT_MMBTU | amount | 769 | 10.9K | 0 276; 2631797.6 4; 2803236.8 4; 4106150.4 4 |
| CHP_PLANT_POWER_TO_HEAT_RATIO | amount | 588 | 11.2K | 0 17; 0.092 8; 0.089 7; 0.387 5 |
| CHP_PLANT_ELECTRIC_ALLOCATION_FACTOR | amount | 757 | 10.9K | 1 277; 0 17; 0.010279 4; 0.125367 4 |
| PLANT_PUMPED_STORAGE_FLAG | category | 2 | 11.9K | Yes 40; PSFLAG 1 |
| PLANT_ANNUAL_HEAT_INPUT_FROM_COMBUSTION_MMBTU | amount | 3.3K | 8.3K | 0 287; 22439431.386 18; 9356403.092 18; 9142186.679 18 |
| PLANT_OZONE_SEASON_HEAT_INPUT_FROM_COMBUSTION_MMBTU | amount | 3.2K | 8.3K | 0 384; 54 18; 8792764.642 17; 3968849.424 17 |
| PLANT_TOTAL_ANNUAL_HEAT_INPUT_MMBTU | amount | 10.6K | 611 | 0 225; 22439431.386 56; 9356403.092 56; 9142186.679 56 |
| PLANT_TOTAL_OZONE_SEASON_HEAT_INPUT_MMBTU | amount | 10.3K | 660 | 0 442; 8792764.642 55; 3968849.424 55; 4017410.992 55 |
| PLANT_ANNUAL_NET_GENERATION_MWH | amount | 10.0K | 269 | 0 364; 1604717 57; 805208 57; 720573 57 |
| PLANT_OZONE_SEASON_NET_GENERATION_MWH | amount | 8.9K | 269 | 0 587; 2107 57; 527151 56; 341673 56 |
| PLANT_ANNUAL_NOX_EMISSIONS_TONS | amount | 2.9K | 8.5K | 0 372; 2628.93 16; 211.694 16; 280.386 16 |
| PLANT_OZONE_SEASON_NOX_EMISSIONS_TONS | amount | 2.8K | 8.5K | 0 447; 1018.158 16; 88.927 16; 117.764 16 |
| PLANT_ANNUAL_SO2_EMISSIONS_TONS | amount | 2.3K | 8.5K | 0 91; 0.006 39; 0.007 38; 0.008 36 |
| PLANT_ANNUAL_CO2_EMISSIONS_TONS | amount | 3.0K | 8.5K | 0 340; 0.001 57; 0.002 17; 2353445.109 16 |
| PLANT_ANNUAL_CH4_EMISSIONS_LBS | amount | 3.0K | 8.5K | 0 337; 465693.963 16; 223000.606 16; 211985.513 16 |
| PLANT_ANNUAL_N2O_EMISSIONS_LBS | amount | 3.1K | 8.5K | 0 337; 67750.052 16; 32434.061 16; 30832.595 16 |
| PLANT_ANNUAL_CO2_EQUIVALENT_EMISSIONS_TONS | amount | 3.1K | 8.5K | 0 270; 0.001 51; 0.002 17; 2369361.041 16 |
| PLANT_ANNUAL_HG_EMISSIONS_LBS | other | 1 | 12.0K | PLHGAN 1 |
| PLANT_ANNUAL_NOX_TOTAL_OUTPUT_EMISSION_RATE_LB_MWH | amount | 2.4K | 8.4K | 0 570; 0.001 27; 3.277 16; 0.526 16 |
| PLANT_OZONE_SEASON_NOX_TOTAL_OUTPUT_EMISSION_RATE_LB_MWH | amount | 2.3K | 8.5K | 0 546; 0.001 26; 0.075 17; 0.04 17 |
| PLANT_ANNUAL_SO2_TOTAL_OUTPUT_EMISSION_RATE_LB_MWH | amount | 1.3K | 8.4K | 0 307; 0.004 243; 0.005 151; 0.007 142 |
| PLANT_ANNUAL_CO2_TOTAL_OUTPUT_EMISSION_RATE_LB_MWH | amount | 2.9K | 8.4K | 0 610; 88.8 26; 2933.159 15; 2437.374 15 |
| PLANT_ANNUAL_CH4_TOTAL_OUTPUT_EMISSION_RATE_LB_MWH | amount | 443 | 8.4K | 0 547; 0.016 181; 0.012 148; 0.024 95 |
| PLANT_ANNUAL_N2O_TOTAL_OUTPUT_EMISSION_RATE_LB_MWH | amount | 161 | 8.4K | 0.002 768; 0 576; 0.001 403; 0.003 398 |
| PLANT_ANNUAL_CO2_EQUIVALENT_TOTAL_OUTPUT_EMISSION_RATE_LB_MWH | amount | 2.9K | 8.4K | 0 540; 88.8 26; 2952.996 16; 2456.301 16 |
| PLANT_ANNUAL_HG_TOTAL_OUTPUT_EMISSION_RATE_LB_MWH | other | 1 | 12.0K | PLHGRTA 1 |
| PLANT_ANNUAL_NOX_INPUT_EMISSION_RATE_LB_MMBTU | amount | 906 | 8.6K | 0 305; 2.306 57; 2.307 55; 0.006 50 |
| PLANT_OZONE_SEASON_NOX_INPUT_EMISSION_RATE_LB_MMBTU | amount | 858 | 8.7K | 0 303; 0.006 54; 0.008 44; 0.01 43 |
| PLANT_ANNUAL_SO2_INPUT_EMISSION_RATE_LB_MMBTU | amount | 387 | 8.6K | 0.001 854; 0.003 677; 0.29 432; 0.034 148 |
| PLANT_ANNUAL_CO2_INPUT_EMISSION_RATE_LB_MMBTU | amount | 984 | 8.6K | 116.889 647; 0 359; 163.326 301; 118.857 264 |
| PLANT_ANNUAL_CH4_INPUT_EMISSION_RATE_LB_MMBTU | amount | 68 | 8.6K | 0.002 1.6K; 0.007 657; 0 307; 0.003 159 |
| PLANT_ANNUAL_N2O_INPUT_EMISSION_RATE_LB_MMBTU | amount | 15 | 8.6K | 0 2.1K; 0.001 818; 0.003 148; 0.009 139 |
| PLANT_ANNUAL_CO2_EQUIVALENT_INPUT_EMISSION_RATE_LB_MMBTU | amount | 1.2K | 8.6K | 117.01 540; 0 279; 163.885 263; 118.978 73 |
| PLANT_ANNUAL_HG_INPUT_EMISSION_RATE_LB_MMBTU | other | 1 | 12.0K | PLHGRA 1 |
| PLANT_ANNUAL_NOX_COMBUSTION_OUTPUT_EMISSION_RATE_LB_MWH | amount | 2.4K | 8.3K | 0 646; 1.436 16; 0.07 16; 0.071 16 |
| PLANT_OZONE_SEASON_NOX_COMBUSTION_OUTPUT_EMISSION_RATE_LB_MWH | amount | 2.3K | 8.7K | 0 388; 0.131 16; 0.081 16; 0.06 16 |
| PLANT_ANNUAL_SO2_COMBUSTION_OUTPUT_EMISSION_RATE_LB_MWH | amount | 1.3K | 8.3K | 0 355; 0.004 244; 0.005 151; 0.007 142 |
| PLANT_ANNUAL_CO2_COMBUSTION_OUTPUT_EMISSION_RATE_LB_MWH | amount | 2.9K | 8.3K | 0 687; 2933.159 15; 2437.374 15; 2661.293 15 |
| PLANT_ANNUAL_CH4_COMBUSTION_OUTPUT_EMISSION_RATE_LB_MWH | amount | 445 | 8.3K | 0 633; 0.016 182; 0.012 146; 0.024 97 |
| PLANT_ANNUAL_N2O_COMBUSTION_OUTPUT_EMISSION_RATE_LB_MWH | amount | 163 | 8.3K | 0.002 771; 0 644; 0.003 398; 0.001 393 |
| PLANT_ANNUAL_CO2_EQUIVALENT_COMBUSTION_OUTPUT_EMISSION_RATE_LB_MWH | amount | 2.9K | 8.3K | 0 617; 2952.996 16; 2456.301 16; 2681.398 16 |
| PLANT_ANNUAL_HG_COMBUSTION_OUTPUT_EMISSION_RATE_LB_MWH | other | 1 | 12.0K | PLHGCRT 1 |
| PLANT_UNADJUSTED_ANNUAL_NOX_EMISSIONS_TONS | amount | 3.3K | 8.5K | 0 60; 2628.93 18; 211.694 18; 280.386 18 |
| PLANT_UNADJUSTED_OZONE_SEASON_NOX_EMISSIONS_TONS | amount | 3.1K | 8.5K | 0 138; 1018.158 17; 88.927 17; 117.764 17 |
| PLANT_UNADJUSTED_ANNUAL_SO2_EMISSIONS_TONS | amount | 2.4K | 8.5K | 0 75; 0.006 39; 0.007 38; 0.008 36 |
| PLANT_UNADJUSTED_ANNUAL_CO2_EMISSIONS_TONS | amount | 3.4K | 8.5K | 0 58; 2353445.109 18; 981296.516 18; 958827.771 18 |
| PLANT_UNADJUSTED_ANNUAL_CH4_EMISSIONS_LBS | amount | 3.3K | 8.5K | 0 56; 465693.963 18; 223000.606 18; 211985.513 18 |
| PLANT_UNADJUSTED_ANNUAL_N2O_EMISSIONS_LBS | amount | 3.3K | 8.5K | 0 56; 67750.052 18; 32434.061 18; 30832.595 18 |
| PLANT_UNADJUSTED_ANNUAL_HG_EMISSIONS_LBS | other | 1 | 12.0K | UNHG 1 |
| PLANT_UNADJUSTED_ANNUAL_HEAT_INPUT_FROM_COMBUSTION_MMBTU | amount | 3.4K | 8.3K | 0 278; 22439431.386 18; 9356403.092 18; 9142186.679 18 |
| PLANT_UNADJUSTED_OZONE_SEASON_HEAT_INPUT_FROM_COMBUSTION_MMBTU | amount | 3.2K | 8.3K | 0 378; 54 18; 8792764.642 17; 3968849.424 17 |
| PLANT_UNADJUSTED_TOTAL_ANNUAL_HEAT_INPUT_MMBTU | amount | 10.8K | 611 | 0 216; 22439431.386 57; 9356403.092 57; 9142186.679 57 |
| PLANT_UNADJUSTED_TOTAL_OZONE_SEASON_HEAT_INPUT_MMBTU | amount | 10.2K | 612 | 0 437; 9695 56; 8792764.642 55; 3968849.424 55 |
| PLANT_UNADJUSTED_ANNUAL_NOX_EMISSIONS_SOURCE | category | 4 | 8.5K | EIA 2.2K; EPA/CAMD 1.2K; EPA/CAMD; EIA 59; UNNOXSRC 1 |
| PLANT_UNADJUSTED_OZONE_SEASON_NOX_EMISSIONS_SOURCE | category | 4 | 8.5K | EIA 2.2K; EPA/CAMD 1.3K; EPA/CAMD; EIA 28; UNNOZSRC 1 |
| PLANT_UNADJUSTED_ANNUAL_SO2_EMISSIONS_SOURCE | category | 4 | 8.6K | EIA 2.2K; EPA/CAMD 1.2K; EPA/CAMD; EIA 39; UNSO2SRC 1 |
| PLANT_UNADJUSTED_ANNUAL_CO2_EMISSIONS_SOURCE | category | 4 | 8.5K | EIA 2.3K; EPA/CAMD 1.1K; EPA/CAMD; EIA 48; UNCO2SRC 1 |
| PLANT_UNADJUSTED_ANNUAL_CH4_EMISSIONS_SOURCE | category | 2 | 8.5K | EIA 3.5K; UNCH4SRC 1 |
| PLANT_UNADJUSTED_ANNUAL_N2O_EMISSIONS_SOURCE | category | 2 | 8.5K | EIA 3.5K; UNN2OSRC 1 |
| PLANT_UNADJUSTED_ANNUAL_HG_EMISSIONS_SOURCE | category | 2 | 0 | -- 12.0K; UNHGSRC 1 |
| PLANT_UNADJUSTED_ANNUAL_HEAT_INPUT_SOURCE | category | 4 | 694 | EIA 10.0K; EPA/CAMD 1.2K; EPA/CAMD; EIA 58; UNHTISRC 1 |
| PLANT_UNADJUSTED_OZONE_SEASON_HEAT_INPUT_SOURCE | category | 4 | 691 | EIA 10.0K; EPA/CAMD 1.2K; EPA/CAMD; EIA 36; UNHOZSRC 1 |
| PLANT_ANNUAL_NOX_BIOMASS_EMISSIONS_TONS | amount | 304 | 11.7K | 0 13; 41.414 2; 86.6 2; 78.395 2 |
| PLANT_OZONE_SEASON_NOX_BIOMASS_EMISSIONS_TONS | amount | 305 | 11.7K | 0 15; 16.846 2; 35.1 2; 29.721 2 |
| PLANT_ANNUAL_SO2_BIOMASS_EMISSIONS_TONS | amount | 291 | 11.7K | 0 14; 0.687 3; 0.248 2; 1.517 2 |
| PLANT_ANNUAL_CO2_BIOMASS_EMISSIONS_TONS | amount | 636 | 11.3K | 0 62; 2742.174 4; 7585.113 4; 16749.467 4 |
| PLANT_ANNUAL_CH4_BIOMASS_EMISSIONS_LBS | amount | 302 | 11.7K | 0 13; 100.446 2; 277.843 2; 613.534 2 |
| PLANT_ANNUAL_N2O_BIOMASS_EMISSIONS_LBS | amount | 305 | 11.7K | 0 13; 10.045 2; 27.784 2; 61.353 2 |
| PLANT_COMBUSTION_HEAT_INPUT_CHP_ADJUSTMENT_VALUE_MMBTU | amount | 747 | 11.0K | 0 203; 3325508.986 4; 3380625.341 4; 5514961.486 4 |
| PLANT_COMBUSTION_ANNUAL_OZONE_SEASON_HEAT_INPUT_CHP_ADJUSTMENT_VALUE_MMBTU | amount | 726 | 11.0K | 0 229; 1195762.431 4; 1761519.202 4; 2104044.891 4 |
| PLANT_ANNUAL_NOX_EMISSIONS_CHP_ADJUSTMENT_VALUE_TONS | amount | 739 | 11.0K | 0 214; 262.698 4; 130.263 4; 550.912 4 |
| PLANT_OZONE_SEASON_NOX_EMISSIONS_CHP_ADJUSTMENT_VALUE_TONS | amount | 723 | 11.0K | 0 221; 86.288 4; 90.79 4; 209.945 4 |
| PLANT_ANNUAL_SO2_EMISSIONS_CHP_ADJUSTMENT_VALUE_TONS | amount | 697 | 11.0K | 0 206; 0.027 5; 0.002 5; 1.35 4 |
| PLANT_ANNUAL_CO2_EMISSIONS_CHP_ADJUSTMENT_VALUE_TONS | amount | 745 | 11.0K | 0 220; 194472.455 4; 197579.055 4; 322319.327 4 |
| PLANT_ANNUAL_CH4_EMISSIONS_CHP_ADJUSTMENT_VALUE_LBS | amount | 739 | 11.0K | 0 223; 7344.941 4; 7453.008 4; 12159.218 4 |
| PLANT_ANNUAL_N2O_EMISSIONS_CHP_ADJUSTMENT_VALUE_LBS | amount | 752 | 11.0K | 0 224; 734.673 4; 745.301 4; 1214.858 4 |
| PLANT_NOMINAL_HEAT_RATE_BTU_KWH | amount | 3.4K | 8.6K | 0 18; 13983.420174 17; 11619.858557 17; 12687.38442 17 |
| PLANT_ANNUAL_COAL_NET_GENERATION_MWH | amount | 301 | 268 | 0 11.4K; 1601771.3 2; 803131.12 2; 719219.11 2 |
| PLANT_ANNUAL_OIL_NET_GENERATION_MWH | amount | 1.3K | 268 | 0 10.2K; 8 10; 25 10; -2 9 |
| PLANT_ANNUAL_GAS_NET_GENERATION_MWH | amount | 2.2K | 268 | 0 9.4K; 2076.882 12; 1353.892 12; 448.984 12 |
| PLANT_ANNUAL_NUCLEAR_NET_GENERATION_MWH | who | 56 | 268 | 0 11.7K; 10077018 1; 9851535 1; 13926441 1 |
| PLANT_ANNUAL_HYDRO_NET_GENERATION_MWH | other | 1.4K | 268 | 0 10.3K; 6262 7; 7554 7; 15778 7 |
| PLANT_ANNUAL_BIOMASS_NET_GENERATION_MWH | amount | 649 | 268 | 0 11.1K; 10202 4; 9493 4; 17078.061 4 |
| PLANT_ANNUAL_WIND_NET_GENERATION_MWH | other | 1.2K | 268 | 0 10.4K; 5368 9; 5351 9; 341330 7 |
| PLANT_ANNUAL_SOLAR_NET_GENERATION_MWH | other | 4.2K | 268 | 0 6.7K; 2270 26; 5821 26; 29301 26 |
| PLANT_ANNUAL_GEOTHERMAL_NET_GENERATION_MWH | other | 63 | 268 | 0 11.6K; 54570 1; 146431 1; 262129 1 |
| PLANT_ANNUAL_OTHER_FOSSIL_NET_GENERATION_MWH | amount | 159 | 268 | 0 11.5K; 5003.26 1; 315929.59 1; 7689 1 |
| PLANT_ANNUAL_OTHER_UNKNOWN_PURCHASED_FUEL_NET_GENERATION_MWH | amount | 287 | 268 | 0 11.4K; -1 6; -7 3; -46 3 |
| PLANT_ANNUAL_TOTAL_NONRENEWABLES_NET_GENERATION_MWH | amount | 3.1K | 268 | 0 8.2K; -2 19; 4 19; 1604716.951 18 |
| PLANT_ANNUAL_TOTAL_RENEWABLES_NET_GENERATION_MWH | amount | 7.3K | 268 | 0 3.4K; 341330 42; 404226 42; 1488986 42 |
| PLANT_ANNUAL_TOTAL_NONHYDRO_RENEWABLES_NET_GENERATION_MWH | amount | 6.0K | 268 | 0 4.8K; 5821 36; 341330 35; 404226 35 |
| PLANT_ANNUAL_TOTAL_COMBUSTION_NET_GENERATION_MWH | amount | 3.4K | 268 | 0 7.9K; 1604716.951 20; 805208.002 20; 720573.002 20 |
| PLANT_ANNUAL_TOTAL_NONCOMBUSTION_NET_GENERATION_MWH | amount | 6.7K | 268 | 0 4.0K; 341330 39; 404226 39; 1488986 39 |
| PLANT_COAL_GENERATION_PERCENT_RESOURCE_MIX | amount | 281 | 856 | 0 10.8K; 1 16; 0.998164379706861 2; 0.997420688822216 2 |
| PLANT_OIL_GENERATION_PERCENT_RESOURCE_MIX | amount | 777 | 856 | 0 9.7K; 1 607; 0.00183562029313916 4; 0.0169859136168371 4 |
| PLANT_GAS_GENERATION_PERCENT_RESOURCE_MIX | amount | 929 | 856 | 0 8.9K; 1 1.3K; 0.00257931117778435 5; 0.00187891025092833 5 |
| PLANT_NUCLEAR_GENERATION_PERCENT_RESOURCE_MIX | amount | 5 | 856 | 0 11.1K; 1 53; 0.999930507223722 1; 0.696306529836148 1 |
| PLANT_HYDRO_GENERATION_PERCENT_RESOURCE_MIX | amount | 26 | 856 | 0 9.8K; 1 1.3K; 0.129923447578883 1; 0.139367301276386 1 |
| PLANT_BIOMASS_GENERATION_PERCENT_RESOURCE_MIX | amount | 278 | 856 | 0 10.5K; 1 355; 0.369659000638535 2; 0.948583822797944 2 |
| PLANT_WIND_GENERATION_PERCENT_RESOURCE_MIX | amount | 20 | 856 | 0 9.8K; 1 1.3K; 0.167426054394528 1; 0.999014460488019 1 |
| PLANT_SOLAR_GENERATION_PERCENT_RESOURCE_MIX | amount | 68 | 856 | 0 6.1K; 1 4.9K; 0.00160415169660679 1; 0.918541505042669 1 |
| PLANT_GEOTHERMAL_GENERATION_PERCENT_RESOURCE_MIX | amount | 6 | 856 | 0 11.1K; 1 59; 0.942368497623743 1; 0.703909783384908 1 |
| PLANT_OTHER_FOSSIL_GENERATION_PERCENT_RESOURCE_MIX | amount | 156 | 856 | 0 11.0K; 1 7; 0.833071364347797 1; 0.385916750443109 1 |
| PLANT_OTHER_UNKNOWN_PURCHASED_FUEL_GENERATION_PERCENT_RESOURCE_MIX | amount | 26 | 856 | 0 11.1K; 1 40; 0.85953347477394 1; 0.113812030917441 1 |
| PLANT_TOTAL_NONRENEWABLES_GENERATION_PERCENT_RESOURCE_MIX | amount | 351 | 856 | 0 7.9K; 1 2.8K; 0.998395848303393 2; 0.462914944966937 2 |
| PLANT_TOTAL_RENEWABLES_GENERATION_PERCENT_RESOURCE_MIX | amount | 347 | 856 | 1 7.9K; 0 2.8K; 0.00160415169660679 2; 0.537085055033063 2 |
| PLANT_TOTAL_NONHYDRO_RENEWABLES_GENERATION_PERCENT_RESOURCE_MIX | amount | 332 | 856 | 1 6.6K; 0 4.2K; 0.00160415169660679 2; 0.537085055033063 2 |
| PLANT_TOTAL_COMBUSTION_GENERATION_PERCENT_RESOURCE_MIX | amount | 86 | 856 | 0 7.6K; 1 3.4K; 0.998395848303393 1; 0.832573945605472 1 |
| PLANT_TOTAL_NONCOMBUSTION_GENERATION_PERCENT_RESOURCE_MIX | amount | 87 | 856 | 1 7.6K; 0 3.4K; 0.00160415169660679 1; 0.167426054394528 1 |
| INGESTED_AT | audit | 1 | 0 | 1785099338941109 12.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 5ae95d27-100b-443f-b474-3 12.0K |
| SRC_SHA256 | who | 1 | 0 | c73fdc561aa402d0f6ed3cc35 12.0K |
