# FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS

rows 457.6K  columns 10  scan 2.5s

roles: audit 2, category 4, date 2, other 2

## when

BEGIN_DATE
  1940         1  
  1943         1  
  1953         1  
  1956         1  
  1959         1  
  1965         2  
  1968         2  
  1969      4.0K  #
  1970       109  
  1972         1  
  1973         1  
  1975         3  
  1976         1  
  1977        14  
  1979         3  
  1980         9  
  1981         4  
  1982         9  
  1983         8  
  1984         8  
  1985        12  
  1986        22  
  1987        15  
  1988         9  
  1989        13  
  1990        30  
  1991        14  
  1992         8  
  1993        13  
  1994        27  
  1995        32  
  1996       126  
  1997       288  
  1998       149  
  1999       417  
  2000       435  
  2001      1.3K  
  2002       442  
  2003       895  
  2004       522  
  2005      4.7K  #
  2006       729  
  2007       522  
  2008       780  
  2009       977  
  2010      1.3K  
  2011      2.8K  
  2012      2.0K  
  2013      2.7K  
  2014    230.5K  ##############################
  2015     47.1K  ######
  2016     15.7K  ##
  2017     15.9K  ##
  2018     14.8K  ##
  2019     11.4K  #
  2020      9.3K  #
  2021      8.5K  #
  2022     13.1K  ##
  2023     13.3K  ##
  2024     13.2K  ##
  2025     24.8K  ###
  2026     14.3K  ##
  2027        13  
  2028        17  

UPDATED_DATE
  2014    211.1K  ##############################
  2015     48.3K  #######
  2016     20.8K  ###
  2017     24.3K  ###
  2018     18.3K  ###
  2019     17.7K  ###
  2020      9.8K  #
  2021     17.6K  ##
  2022     14.7K  ##
  2023     14.5K  ##
  2024     15.6K  ##
  2025     27.6K  ####
  2026     17.2K  ##

## what

PROGRAM_CODE: CAASIP 53%, CAAMACT 13%, CAANSPS 13%, CAATVP 6%, CAAGACTM 4%, CAAFESOP 3%, CAANSR 3%, CAACFC 2%, CAAPSD 2%, CAANESH 1%, CAANSPSM 1%, CAANFRP 0%

PROGRAM_DESC: State Implementation Plan for  53%, MACT Standards (40 CFR Part 63 13%, New Source Performance Standar 13%, Title V Permits 6%, 40 CFR Part 63 Area Sources 4%, Federally-Enforceable State Op 3%, New Source Review Permit Requi 3%, Stratospheric Ozone Protection 2%, Prevention of Significant Dete 2%, National Emission Standards fo 1%, New Source Performance Standar 1%, Not defined as federally-repor 0%

AIR_OPERATING_STATUS_CODE: OPR 70%, CLS 29%, TMP 1%, PLN 0%, CNS 0%, SEA 0%

AIR_OPERATING_STATUS_DESC: Operating 70%, Permanently Closed 29%, Temporarily Closed 1%, Planned Facility 0%, Under Construction 0%, Seasonal 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PGM_SYS_ID | other | 274.5K | 0 | NY0000008262200202 2.3K; NC0000003704101292 2.3K; NM0000003501503265 2.3K; NM0000003501503262 2.3K |
| PROGRAM_CODE | category | 31 | 0 | CAASIP 240.9K; CAAMACT 57.5K; CAANSPS 57.3K; CAATVP 28.9K |
| PROGRAM_DESC | category | 29 | 0 | State Implementation Plan 240.9K; MACT Standards (40 CFR Pa 57.5K; New Source Performance St 57.3K; Title V Permits 28.9K |
| AIR_OPERATING_STATUS_CODE | category | 6 | 0 | OPR 318.2K; CLS 130.6K; TMP 5.1K; PLN 2.1K |
| AIR_OPERATING_STATUS_DESC | category | 6 | 0 | Operating 318.2K; Permanently Closed 130.6K; Temporarily Closed 5.1K; Planned Facility 2.1K |
| BEGIN_DATE | date | 7.1K | 0 | 10/19/2014 213.8K; 10/27/2015 9.5K; 09/29/2025 8.6K; 03/31/2015 8.3K |
| UPDATED_DATE | date | 3.5K | 0 | 10/19/2014 203.6K; 10/27/2015 9.5K; 09/29/2025 8.6K; 03/31/2015 8.2K |
| _INGESTED_AT | audit | 1 | 0 | 1785966128993556 457.6K |
| _SOURCE_RUN_ID | audit | 1 | 0 | ece55c96-83d9-43f4-9295-0 457.6K |
| _SRC_SHA256 | other | 1 | 0 | 58c76a2eab49c79b75ffd0897 457.6K |
