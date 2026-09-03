# FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES

rows 279.7K  columns 22  scan 3.1s

roles: audit 2, category 7, id 1, other 6, state 1, who 5

## who

FACILITY_NAME by rows
       226  SANDRIDGE EXPLORATION AND PRODUCTION LLC
       166  SHELL
       158  CEMEX CONSTRUCTION MATERIALS FLORIDA LLC
       146  CITGO
       144  BP
       139  VERIZON WIRELESS
       134  EXXON
       127  NICOR GAS
       112  ANADARKO GATHERING COMPANY LLC
        99  EVERGREEN NATURAL RESOURCES - PORTABLE E
        91  US POSTAL SERVICE
        80  BP GAS STATION
        79  FISHER SAND & GRAVEL COMPANY
        76  MARATHON
        72  EXXON GAS STATION
        69  SHELL GAS STATION
        66  CENTRAL VALLEY AG
        60  ARGOS USA
        60  NEW CINGULAR WIRELESS PCS, LLC DBA AT&T MOBILITY
        60  KEYROCK ENVIRONMENT LLC

LOCAL_CONTROL_REGION_NAME by rows
      1.9K  Polk County
      1.4K  Allegheny County Health Department
      1.0K  City Of Albuquerque
       794  South Coast Air Quality Management District (Grantee)
       667  San Joaquin Valley Air Pollution Control District (Grantee)
       648  Philadelphia Air Management Services
       588  Linn County
       560  Nashville-Davidson County
       460  Jefferson County (AL)
       428  City Of Omaha
       423  Puget Sound Clean Air Agency
       404  Lincoln - Lancaster County
       275  Memphis-Shelby County
       210  Knox County
       169  Bay Area Air Quality Management District (Grantee)
       155  Mecklenburg County
       153  Chattanooga-Hamilton County
       136  Santa Barbara County Air Pollution Control District (Grantee)
       115  Forsyth County
       111  Maricopa County Air Pollution Control Agency (Grantee)

COUNTY_NAME by rows
     13.7K  Undetermined
     11.1K  Weld
      8.9K  Cook
      5.4K  Uintah
      3.5K  Montgomery
      2.8K  Jefferson
      2.5K  Garfield
      2.5K  Polk
      2.3K  Adams
      2.3K  Bronx
      2.0K  Baltimore (city)
      1.9K  Washington
      1.9K  Middlesex
      1.9K  Eddy
      1.8K  Jackson
      1.8K  Douglas
      1.7K  Lake
      1.7K  DuPage
      1.6K  Denver
      1.6K  Prince George's

CITY by rows
      3.6K  CHICAGO
      3.1K  VERNAL
      2.0K  BALTIMORE
      2.0K  NEW YORK
      1.7K  BONANZA
      1.6K  DENVER                        
      1.6K  PORTABLE
      1.5K  BROOKLYN
      1.4K  ALBUQUERQUE
      1.3K  NEW MEXICO
      1.2K  FLORIDA
      1.1K  DES MOINES
      1.0K  MARYLAND
       970  OMAHA
       887  WASHINGTON
       867  CLEVELAND
       853  SPRINGFIELD
       828  BRONX
       781  COLORADO SPRINGS              
       755  KANSAS CITY

## where

STATE: CO 32.4K, IL 28.5K, OK 18.4K, LA 13.8K, NY 12.6K, PA 11.4K, MD 11.1K, OH 11.0K, VA 10.3K, NM 8.8K, TX 7.8K, KS 7.5K

## what

EPA_REGION: 06 18%, 05 18%, 08 15%, 03 13%, 04 11%, 07 10%, 02 7%, 01 5%, 09 1%, 10 1%

FACILITY_TYPE_CODE: POF 72%, NON 18%, COR 6%, CNG 2%, CTG 1%, FDF 1%, STF 1%, DIS 0%, TRB 0%, MWD 0%, SDT 0%, MXO 0%

AIR_POLLUTANT_CLASS_CODE: MIN 74%, SMI 14%, MAJ 7%, UNK 3%, NAP 1%, OTH 0%

AIR_POLLUTANT_CLASS_DESC: Minor Emissions 74%, Synthetic Minor Emissions 14%, Major Emissions 7%, Emissions classification unkno 3%, Not applicable 1%, Other 0%

AIR_OPERATING_STATUS_CODE: OPR 69%, CLS 29%, TMP 1%, PLN 0%, CNS 0%, SEA 0%

AIR_OPERATING_STATUS_DESC: Operating 69%, Permanently Closed 29%, Temporarily Closed 1%, Planned Facility 0%, Under Construction 0%, Seasonal 0%

CURRENT_HPV: No Violation Identified 99%, Violation w/in 1 Year 1%, Unaddressed-State 0%, Violation-Unresolved 0%, Addressed-State 0%, Unaddressed-Local 0%, Addressed-Local 0%, Addressed-EPA 0%, Violation Identified 0%, Unaddressed-EPA 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PGM_SYS_ID | id | 287.9K | 0 | KS0000002017300047 764; KS0000002017300045 764; KS0000002017300044 764; KS0000002017300041 764 |
| REGISTRY_ID | other | 263.1K | 187 | 110038945504 787; 110038298936 764; 110000446615 764; 110016705653 764 |
| FACILITY_NAME | who | 245.5K | 0 | SANDRIDGE EXPLORATION AND 895; ANADARKO GATHERING COMPAN 812; MESA OPERATING CO.        775; TAPSTONE ENERGY 765 |
| STREET_ADDRESS | other | 255.0K | 133 | NO STREET ADDRESS 1.9K; PORTABLE SOURCE 1.5K; RURAL 815; DOWNTOWN 772 |
| CITY | who | 25.0K | 15 | CHICAGO 4.1K; VERNAL 3.2K; NEW YORK 2.1K; BALTIMORE 2.0K |
| COUNTY_NAME | who | 1.9K | 0 | Undetermined 13.7K; Weld 11.2K; Cook 9.1K; Uintah 5.4K |
| STATE | state | 55 | 0 | CO 32.4K; IL 28.5K; OK 18.4K; LA 13.8K |
| ZIP_CODE | other | 60.4K | 1 | 00000 5.8K; 84078 3.2K; 70000     2.5K; 70000 2.1K |
| EPA_REGION | category | 10 | 0 | 06 51.2K; 05 50.4K; 08 42.3K; 03 35.3K |
| SIC_CODES | other | 3.9K | 65.0K | 1311 34.2K; 7216 11.3K; 5541 10.1K; 1321 9.7K |
| NAICS_CODES | who | 4.4K | 4 | 999999 25.5K; 211111 15.5K; 812320 12.2K; 211112 211130 10.8K |
| FACILITY_TYPE_CODE | category | 12 | 47.4K | POF 166.9K; NON 40.8K; COR 13.8K; CNG 3.6K |
| AIR_POLLUTANT_CLASS_CODE | category | 6 | 15.5K | MIN 196.5K; SMI 37.5K; MAJ 19.1K; UNK 7.3K |
| AIR_POLLUTANT_CLASS_DESC | category | 6 | 15.5K | Minor Emissions 196.5K; Synthetic Minor Emissions 37.5K; Major Emissions 19.1K; Emissions classification  7.3K |
| AIR_OPERATING_STATUS_CODE | category | 6 | 12.6K | OPR 184.1K; CLS 77.5K; TMP 4.0K; PLN 757 |
| AIR_OPERATING_STATUS_DESC | category | 6 | 12.6K | Operating 184.1K; Permanently Closed 77.5K; Temporarily Closed 4.0K; Planned Facility 757 |
| CURRENT_HPV | category | 10 | 0 | No Violation Identified 276.9K; Violation w/in 1 Year 1.5K; Unaddressed-State 361; Violation-Unresolved 311 |
| LOCAL_CONTROL_REGION_CODE | other | 62 | 268.0K | PLK 1.9K; ACH 1.4K; COA 1.0K; SCA 794 |
| LOCAL_CONTROL_REGION_NAME | who | 62 | 268.0K | Polk County 1.9K; Allegheny County Health D 1.4K; City Of Albuquerque 1.0K; South Coast Air Quality M 794 |
| _INGESTED_AT | audit | 1 | 0 | 1785966097775743 279.7K |
| _SOURCE_RUN_ID | audit | 1 | 0 | bf4586fa-31b3-4ed8-bb01-d 279.7K |
| _SRC_SHA256 | other | 1 | 0 | 8477d3fc1d2c6074907f2c003 279.7K |
