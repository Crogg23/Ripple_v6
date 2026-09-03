# FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS

rows 3.34M  columns 11  scan 4.1s

roles: audit 2, category 3, date 2, other 4

## when

START_DATE
  1900       153  
  1930         5  
  1931        23  
  1932         2  
  1937         2  
  1939         1  
  1940         2  
  1942         1  
  1950        33  
  1969         1  
  1970         2  
  1971         1  
  1972         1  
  1973         1  
  1974         1  
  1975         5  
  1976         1  
  1977         4  
  1979         1  
  1980        22  
  1981         5  
  1982         8  
  1983         5  
  1984        12  
  1985        18  
  1986        28  
  1987        84  
  1988       179  
  1989       211  
  1990       338  
  1991       603  
  1992      1.0K  #
  1993      1.1K  #
  1994      1.9K  #
  1995      2.0K  ##
  1996      3.7K  ###
  1997      5.6K  ####
  1998      5.4K  ####
  1999      6.2K  #####
  2000      8.9K  #######
  2001      8.6K  #######
  2002     15.4K  ############
  2003     14.6K  ###########
  2004     19.0K  ###############
  2005     28.6K  ######################
  2006     35.3K  ###########################
  2007     39.1K  ##############################
  2008     23.8K  ##################
  2009      7.6K  ######
  2010       355  
  2011         4  
  2012         7  
  2013        10  
  2014        10  
  2015        10  
  2016        12  
  2017        23  
  2018        15  
  2019        15  
  2020        41  
  2021         6  
  2022        13  
  2023        34  
  2024        19  
  2025        13  
  2026         6  
  2027         9  
  2028        12  
  2029        19  

END_DATE
  1899         6  
  1930         3  
  1931         9  
  1932         1  
  1940         8  
  1952         1  
  1959         2  
  1965         1  
  1968         1  
  1969         1  
  1971         2  
  1972         1  
  1973         3  
  1974         9  
  1975         5  
  1976         5  
  1977        10  
  1978        35  
  1979        35  
  1980        31  
  1981        32  
  1982        32  
  1983        35  
  1984        44  
  1985       108  
  1986       121  
  1987       179  
  1988       216  
  1989       253  
  1990       322  
  1991       344  
  1992       391  #
  1993       495  #
  1994       664  #
  1995       584  #
  1996      1.1K  ##
  1997      2.4K  ###
  1998      5.0K  #######
  1999      7.2K  ##########
  2000      8.9K  ############
  2001     10.2K  ##############
  2002     11.6K  ################
  2003     11.2K  ################
  2004     12.5K  #################
  2005     12.6K  #################
  2006     15.3K  #####################
  2007     15.4K  #####################
  2008     14.4K  ####################
  2009     19.4K  ###########################
  2010     15.0K  #####################
  2011     13.6K  ###################
  2012     21.7K  ##############################
  2013     12.3K  #################
  2014     15.6K  ######################
  2015      7.0K  ##########
  2016      1.6K  ##
  2017        46  
  2018       101  
  2019        22  
  2020         6  
  2021        10  
  2022         5  
  2023        27  
  2024         5  
  2025         1  
  2026         1  
  2028         3  

## what

REL_TYPE: officer_of 52%, registered_address 25%, intermediary_of 18%, same_name_as 3%, similar 1%, same_company_as 0%, connected_to 0%, same_as 0%, same_id_as 0%, underlying 0%, similar_company_as 0%, probably_same_officer_as 0%

STATUS: Resigned 75%, Appointed 25%

SOURCEID: Paradise Papers - Malta corpor 28%, Panama Papers 24%, Offshore Leaks 20%, Paradise Papers - Appleby 14%, Bahamas Leaks 9%, Paradise Papers - Aruba corpor 5%, Paradise Papers - Bahamas corp 1%, Paradise Papers - Samoa corpor 1%, Paradise Papers - Cook Islands 0%, Paradise Papers - Barbados cor 0%, Paradise Papers - Lebanon corp 0%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| NODE_ID_START | other | 1.13M | 0 | 230000018 38.3K; 54662 37.5K; 23000136 16.7K; 23000147 11.5K |
| NODE_ID_END | other | 1.32M | 0 | 236724 40.2K; 240000001 15.5K; 81027146 11.6K; 81027090 10.3K |
| REL_TYPE | category | 14 | 0 | officer_of 1.72M; registered_address 832.7K; intermediary_of 598.5K; same_name_as 104.2K |
| LINK | other | 1.0K | 389 | shareholder of 589.9K; registered address 566.9K; intermediary of 512.8K; director of 457.9K |
| STATUS | category | 3 | 3.16M | Resigned 131.4K; Appointed 43.5K |
| START_DATE | date | 23.9K | 2.39M | 31-DEC-1969 2.2K; 2007-07-20 1.7K; 1999-12-21 1.7K; 2007-06-27 1.7K |
| END_DATE | date | 13.1K | 3.07M | 30-SEP-2012 9.8K; 31-AUG-2006 891; 15-JUN-2010 886; 15-JAN-2009 886 |
| SOURCEID | category | 12 | 519.0K | Paradise Papers - Malta c 776.3K; Panama Papers 674.1K; Offshore Leaks 561.4K; Paradise Papers - Appleby 391.0K |
| INGESTED_AT | audit | 1 | 0 | 1785965377933493 3.34M |
| SOURCE_RUN_ID | audit | 1 | 0 | 6ae1f747-3ad9-4f19-ad12-c 3.34M |
| SRC_SHA256 | other | 1 | 0 | 91f9500153df3d072ef32d258 3.34M |
