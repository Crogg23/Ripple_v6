# FED_CDC_DRUG_POISONING_COUNTY

rows 53.4K  columns 11  scan 2.0s

roles: audit 2, category 3, other 3, state 1, who 2

## who

COUNTY by rows
        17  Seneca County, OH
        17  Walker County, GA
        17  Bergen County, NJ
        17  Crook County, WY
        17  Carbon County, MT
        17  Kent County, TX
        17  Waukesha County, WI
        17  Limestone County, TX
        17  Lake County, TN
        17  Harding County, SD
        17  Santa Cruz County, CA
        17  Iron County, UT
        17  Dewey County, OK
        17  Yukon-Koyukuk Census Area, AK
        17  Lauderdale County, AL
        17  Bradley County, AR
        17  Glascock County, GA
        17  Keya Paha County, NE
        17  Polk County, IA
        17  Ouray County, CO

SRC_SHA256 by rows
     53.4K  7a63757d7fb08ce335818e1475a66e03e846632eae1b0e45815970bce8bc5452

## where

ST: TX 4.3K, GA 2.7K, VA 2.3K, KY 2.0K, MO 2.0K, KS 1.8K, IL 1.7K, NC 1.7K, IA 1.7K, TN 1.6K, NE 1.6K, IN 1.6K

## what

YEAR: 2009 8%, 2007 8%, 2003 8%, 2004 8%, 2006 8%, 2005 8%, 2008 8%, 2010 8%, 2011 8%, 2012 8%, 2013 8%, 2014 8%

STATE: Texas 17%, Georgia 11%, Virginia 9%, Kentucky 8%, Missouri 8%, Kansas 7%, Illinois 7%, North Carolina 7%, Iowa 7%, Tennessee 6%, Nebraska 6%, Indiana 6%

ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES: 6.1-8 16%, 4.1-6 16%, 8.1-10 13%, 2.1-4 13%, 10.1-12 10%, 0-2 9%, 12.1-14 8%, 14.1-16 6%, 16.1-18 4%, 18.1-20 3%, 20.1-22 2%, 22.1-24 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| FIPS | other | 3.1K | 0 | 53075 268; 48109 268; 28041 268; 25023 268 |
| YEAR | category | 17 | 0 | 2009 3.1K; 2007 3.1K; 2003 3.1K; 2004 3.1K |
| STATE | category | 50 | 0 | Texas 4.3K; Georgia 2.7K; Virginia 2.3K; Kentucky 2.0K |
| ST | state | 51 | 0 | TX 4.3K; GA 2.7K; VA 2.3K; KY 2.0K |
| FIPS_STATE | other | 51 | 0 | 48 4.3K; 13 2.7K; 51 2.3K; 21 2.0K |
| COUNTY | who | 3.2K | 0 | Whitman County, WA 268; Culberson County, TX 268; Greene County, MS 268; Plymouth County, MA 268 |
| POPULATION | other | 40.8K | 4 | 49702 267; 18929 267; 8811 267; 7786 267 |
| ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES | category | 16 | 0 | 6.1-8 8.2K; 4.1-6 8.1K; 8.1-10 6.9K; 2.1-4 6.5K |
| INGESTED_AT | audit | 1 | 0 | 1782620218518540 53.4K |
| SOURCE_RUN_ID | audit | 1 | 0 | 44c98c9c-dcb8-4a43-8d4c-4 53.4K |
| SRC_SHA256 | who | 1 | 0 | 7a63757d7fb08ce335818e147 53.4K |
