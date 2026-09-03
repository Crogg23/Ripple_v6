# PORTAL_CKA_OKLAHOMA_OPEN_DA_BB949BD77E

rows 48  columns 17  scan 3.0s

roles: amount 3, audit 2, category 10, date 2, who 1

## when

PUBLIC_POSTING
  2013         8  ############
  2014        20  ##############################
  2021         3  ####
  2022         1  ##
  2025         6  #########
  2026        10  ###############

INGESTED_AT
  2026        48  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| COST | 48 | 461.86 | 23.2K | 1.81M | 2.15M | 8.45M |
| COMPARABLE_ITEM_1_COST | 30 | 8.6K | 31.4K | 592.4K | 675.0K | 2.19M |
| COMPARABLE_ITEM_1_SAVINGS | 30 | 4.6K | 11.6K | 260.2K | 295.0K | 972.2K |

## who

SRC_SHA256 by rows
        48  708a39d440de0f84cfcbb29dbb5729fb40842c61b78bf0464fd75c95bb1fb8d9

SRC_SHA256 by dollars
       8.45M       48 rows  708a39d440de0f84cfcbb29dbb5729fb40842c61b78bf0464fd75c95bb1f

## who x when

SRC_SHA256 by PUBLIC_POSTING, dollars = COST
  708a39d440de0f84cfcbb29dbb5729fb40842c61  2013:631.2K 2014:341.4K 2021:3.20M 2022:99.0K 2025:742.1K 2026:3.44M

## what

STATE_ENTITY_NAME: Department of Corrections Agri 31%, Department of Corrections 23%, Department of Veterans Affairs 21%, Department of Corrections Agri 4%, OMES 4%, Department of Transportation 4%, Oklahoma Bureau of Narcotics 2%, CLEET 2%, OMES Print shop 2%, Workers' Compensation Commissi 2%, Department of Public Safety 2%, DHS 2%

STATE_ENTITY_NUMBER: 13100 58%, 650 21%, 90000 6%, 34500 4%, 47700 2%, 41500 2%, 865 2%, 58500 2%, 83000 2%

ACQUISITION_DESCRIPTIONS: Green Beans 17%, Service Implementation 17%, Diced Tomatoes 11%, Whole Kernel Corn 11%, 1979 King Air C90 6%, Broccoli Mini Florets 6%, Breaded Chicken Breast Fillet 6%, Frozen Cut Spinach 6%, Apple Sauce 6%, Soup Base 6%, Diced Carrots 6%, Sliced Beets 6%

SUPPLIER_NAME: LA Foods 28%, Saker Mechanical 18%, Global Foods Inc. 15%, National Food Group 15%, Boston Consulting Group Inc. 5%, Winair 5%, Stanaero, LLC 2%, Global Foods 2%, K. Rhynes Surplus 2%, Goal Line Foods 2%, Image Works  2%, FAIR Health, Inc. 2%

EXEMPTION_REASON: To utilize the grant funding b 48%, Pricing is 26% less than marke 5%, Pricing is 43.4% less than SW  5%, Price is 40.4% less than SW co 5%,  Pricing is 53.2% less than co 5%, Pricing is 35% less than contr 5%, Pricing is 43.9% less than con 5%, Pricing is 45% Less  than cont 5%, Pricing is 41% Less than contr 5%, Pricing is 47% Less than contr 5%, Price is 35.4% less than contr 5%, Price is 47.6% less than contr 5%

COMPARABLE_ITEM_1: N/A 50%, Green Beans 11%, Diced Tomatoes 7%, Whole Kernel Corn 7%, Airplane 4%, Broccoli 4%, Chicken Breast Tender 4%, Frozen Spinach 4%, Apple Sauce 4%, Soup Base 4%, Diced Carrots 4%

COMPARABLE_ITEM_2: N/A 89%, Denied 7%, Mad City Outdoor 2%, Van Keppel (new) 2%

COMPARABLE_ITEM_2_COST: N/A 93%, 695000 2%, 65198.91 2%, 365882 2%

COMPARABLE_ITEM_2_SAVINGS: N/A 93%, 195000 2%, 15198.91 2%, 270882 2%

APPROVAL_DENIAL: Approved 93%, Denied 7%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| PUBLIC_POSTING | date | 34 | 0 | 2025-09-12T00:00:00 5; 2014-02-18T00:00:00 3; 2014-03-17T00:00:00 3; 2014-04-18T00:00:00 3 |
| STATE_ENTITY_NAME | category | 12 | 0 | Department of Corrections 15; Department of Corrections 11; Department of Veterans Af 10; Department of Corrections 2 |
| STATE_ENTITY_NUMBER | category | 9 | 0 | 13100 28; 650 10; 90000 3; 34500 2 |
| ACQUISITION_DESCRIPTIONS | category | 42 | 0 | Green Beans 3; Service Implementation 3; Diced Tomatoes 2; Whole Kernel Corn 2 |
| SUPPLIER_NAME | category | 20 | 0 | LA Foods 11; Saker Mechanical 7; Global Foods Inc. 6; National Food Group 6 |
| COST | amount | 45 | 0 | 12189 3; 15993.6 2; 500000 1; 18612 1 |
| EXEMPTION_REASON | category | 39 | 0 | To utilize the grant fund 10; Pricing is 26% less than  1; Pricing is 43.4% less tha 1; Price is 40.4% less than  1 |
| COMPARABLE_ITEM_1 | category | 29 | 3 | N/A 14; Green Beans 3; Diced Tomatoes 2; Whole Kernel Corn 2 |
| COMPARABLE_ITEM_1_COST | amount | 32 | 3 | N/A 15; 675000 1; 32868 1; 35343 1 |
| COMPARABLE_ITEM_1_SAVINGS | amount | 32 | 3 | N/A 15; 175000 1; 14256 1; 14280 1 |
| COMPARABLE_ITEM_2 | category | 5 | 4 | N/A 39; Denied 3; Mad City Outdoor 1; Van Keppel (new) 1 |
| COMPARABLE_ITEM_2_COST | category | 5 | 4 | N/A 41; 695000 1; 65198.91 1; 365882 1 |
| COMPARABLE_ITEM_2_SAVINGS | category | 5 | 4 | N/A 41; 195000 1; 15198.91 1; 270882 1 |
| APPROVAL_DENIAL | category | 3 | 4 | Approved 41; Denied 3 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:12:34.36324 48 |
| SOURCE_RUN_ID | audit | 1 | 0 | 3e3fba31-cbeb-4b89-9122-9 48 |
| SRC_SHA256 | who | 1 | 0 | 708a39d440de0f84cfcbb29db 48 |
