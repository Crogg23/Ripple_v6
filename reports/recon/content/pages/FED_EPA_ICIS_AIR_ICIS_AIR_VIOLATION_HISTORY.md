# FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY

rows 102.0K  columns 19  scan 3.0s

roles: audit 2, category 2, id 2, other 3, state 1, who 9

## who

POLLUTANT_DESCS by rows
     41.6K  FACIL
      9.0K  VOLATILE ORGANIC COMPOUNDS (VOCS)
      4.2K  TOTAL PARTICULATE MATTER
      3.6K  ADMIN
      2.6K  NITROGEN OXIDES NO2
      2.3K  PARTICULATE MATTER < 10 UM
      2.2K  Sulfur dioxide
      2.0K  TOTAL HAZARDOUS AIR POLLUTANTS (HAPS)
      1.7K  Carbon monoxide
      1.5K  VISIBLE EMISSIONS
       962  Particulate matter
       953  OTHER
       871  NITROGEN OXIDES
       673  FACIL VOLATILE ORGANIC COMPOUNDS (VOCS)
       432  Tetrachloroethylene
       372  CFC (CHLOROFLUOROCARBONS)
       362  Hydrogen sulfide
       347  TOTAL HAZARDOUS AIR POLLUTANTS (HAPS) VOLATILE ORGANIC COMPOUNDS (VOCS
       338  Lead
       295  Particulate matter - PM10

PROGRAM_DESCS by rows
     39.1K  State Implementation Plan for National Primary and Secondary Ambient A
     28.8K  Title V Permits
      6.7K  State Implementation Plan for National Primary and Secondary Ambient A
      3.5K  New Source Performance Standards
      3.5K  MACT Standards (40 CFR Part 63)
      2.5K  Federally-Enforceable State Operating Permit - Non Title V
      1.8K  New Source Performance Standards State Implementation Plan for Nationa
      1.3K  Federally-Enforceable State Operating Permit - Non Title V State Imple
      1.2K  MACT Standards (40 CFR Part 63) State Implementation Plan for National
      1.0K  Prevention of Significant Deterioration of Air Quality
      1.0K  New Source Review Permit Requirements
       959  New Source Performance Standards State Implementation Plan for Nationa
       801  MACT Standards (40 CFR Part 63) New Source Performance Standards State
       798  MACT Standards (40 CFR Part 63) State Implementation Plan for National
       719  New Source Review Permit Requirements State Implementation Plan for Na
       573  MACT Standards (40 CFR Part 63) Title V Permits
       530  National Emission Standards for Hazardous Air Pollutants (40 CFR Part 
       377  Stratospheric Ozone Protection
       330  New Source Performance Standards Title V Permits
       322  Federally-Enforceable State Operating Permit - Non Title V New Source 

HPV_DAYZERO_DATE by rows
       125  01-28-2000
        64  10-30-1993
        62  06-17-2002
        61  07-03-2001
        46  09-21-2023
        45  09-18-2023
        42  03-22-2001
        41  07-25-2022
        36  10-17-2023
        36  09-26-2023
        36  02-16-2022
        35  02-26-2016
        34  03-30-2016
        33  07-12-2003
        32  05-01-2006
        32  10-02-1998
        32  03-17-2016
        32  10-07-2024
        31  06-21-2000
        30  05-01-2025

HPV_RESOLVED_DATE by rows
       465  06-27-2023
       168  08-01-2024
       159  04-26-2002
       113  04-04-2025
        98  09-29-2025
        89  07-10-2002
        74  05-12-2016
        74  03-03-2022
        69  06-30-2016
        68  02-21-2003
        66  12-29-2021
        61  04-04-2023
        59  07-27-2016
        57  05-31-2016
        56  09-30-1998
        54  11-16-2009
        53  05-06-2016
        53  05-31-2023
        52  10-12-2016
        51  07-29-2016

## where

STATE_CODE: CA 15.1K, PA 9.2K, TX 5.5K, OK 4.7K, MI 4.7K, IN 4.1K, OH 3.7K, CO 3.5K, NC 3.5K, NJ 3.5K, IL 3.4K, NY 3.0K

## what

AGENCY_TYPE_DESC: State 77%, Local 19%, U.S. EPA 5%, Tribal 0%, County 0%, Other Federal 0%, Other - State 0%, State Contractor 0%

ENF_RESPONSE_POLICY_CODE: FRV 56%, HPV 44%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PGM_SYS_ID | other | 36.5K | 0 | CABAA00006013A0010 1.0K; CASJV00006029S0037 564; MI00000000000B2816 519; MI00000000000A9831 511 |
| ACTIVITY_ID | id | 101.0K | 0 | 3400445082 511; 3400438970 511; 3400429407 511; 3400453159 511 |
| AGENCY_TYPE_DESC | category | 8 | 0 | State 78.1K; Local 19.1K; U.S. EPA 4.8K; Tribal 7 |
| STATE_CODE | state | 54 | 4.8K | CA 15.1K; PA 9.2K; TX 5.5K; OK 4.7K |
| AIR_LCON_CODE | other | 56 | 83.0K | SJV 7.5K; BAA 4.4K; SCA 1.8K; PAM 961 |
| COMP_DETERMINATION_UID | id | 103.0K | 0 | 05000F000003166CO1 511; PA000A00000350MFORM7 511; MA000A00000683MTHAPW 511; MI000A000N8265FFACILW 511 |
| ENF_RESPONSE_POLICY_CODE | category | 2 | 0 | FRV 57.2K; HPV 44.8K |
| PROGRAM_CODES | who | 299 | 0 | CAASIP 39.1K; CAATVP 28.8K; CAASIP CAATVP 6.7K; CAANSPS 3.5K |
| PROGRAM_DESCS | who | 292 | 0 | State Implementation Plan 39.1K; Title V Permits 28.8K; State Implementation Plan 6.7K; New Source Performance St 3.5K |
| POLLUTANT_CODES | who | 1.9K | 13.2K | 300000329 41.6K; 300000243 9.0K; 300000322 4.2K; 300000328 3.6K |
| POLLUTANT_DESCS | who | 1.9K | 13.2K | FACIL 41.6K; VOLATILE ORGANIC COMPOUND 9.0K; TOTAL PARTICULATE MATTER 4.2K; ADMIN 3.6K |
| EARLIEST_FRV_DETERM_DATE | who | 7.8K | 38.3K | 03-24-2021 511; 06-17-2016 429; 07-11-2024 324; 11-18-2024 320 |
| HPV_DAYZERO_DATE | who | 10.6K | 57.3K | 07-11-2024 230; 01-30-2024 226; 03-17-2025 226; 06-22-2009 225 |
| HPV_RESOLVED_DATE | who | 9.2K | 32.4K | 06-27-2023 477; 10-19-2014 378; 08-22-2016 360; 08-13-2015 356 |
| DSCV_PATHWAY_DATE | who | 8.4K | 63.2K | 03-24-2021 473; 04-08-2025 199; 01-30-2024 195; 04-01-2008 194 |
| NFTC_PATHWAY_DATE | who | 8.8K | 47.7K | 07-11-2024 278; 09-14-1994 275; 03-17-2025 274; 06-12-2009 273 |
| _INGESTED_AT | audit | 1 | 0 | 1785966255208062 102.0K |
| _SOURCE_RUN_ID | audit | 1 | 0 | bfe7330e-97af-4186-a157-9 102.0K |
| _SRC_SHA256 | other | 1 | 0 | 7f3c0f59891d933c5bf7b6482 102.0K |
