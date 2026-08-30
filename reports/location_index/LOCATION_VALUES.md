# Location columns, value-verified -- 2026-08-30

2238 columns in 386 marts, measured live (fill, distinct, sentinel share, shape test per kind). Name-scan index: location_columns_all.csv. This file's CSV twin: location_columns_verified.csv. 3 tables failed to scan.

## Verdicts by kind

| kind | verdict | columns |
|---|---|---:|
| address | text place | 207 |
| address | empty | 30 |
| address | coded place (numbers) | 23 |
| address | constant | 5 |
| address | not a place (dates) | 1 |
| address | not measured | 1 |
| airport_port | text place | 5 |
| airport_port | coded place (numbers) | 3 |
| airport_port | empty | 1 |
| census_tract | coded place (numbers) | 28 |
| city | text place | 240 |
| city | empty | 12 |
| city | not measured | 3 |
| city | constant | 2 |
| city | coded place (numbers) | 1 |
| cong_district | coded place (numbers) | 25 |
| cong_district | text place | 18 |
| cong_district | empty | 4 |
| cong_district | not a place (dates) | 1 |
| coordinates | clean coordinate | 139 |
| coordinates | not a coordinate (name-scan false hit) | 36 |
| coordinates | coordinate with 0,0 trap | 19 |
| coordinates | empty | 12 |
| coordinates | coordinate, partly out of range | 6 |
| country | country name | 54 |
| country | country code | 40 |
| country | empty | 25 |
| country | country code (98%+ US) | 13 |
| country | country name (98%+ US) | 13 |
| country | constant | 8 |
| country | empty table | 1 |
| country | not measured | 1 |
| county | county name | 100 |
| county | county code | 16 |
| county | mixed county | 5 |
| county | constant | 4 |
| county | empty | 4 |
| county | not measured | 1 |
| facility_site | text place | 96 |
| facility_site | coded place (numbers) | 32 |
| facility_site | empty | 10 |
| facility_site | not a place (dates) | 3 |
| facility_site | constant | 2 |
| fips | clean FIPS (2-digit) | 31 |
| fips | FIPS with leading zeros lost | 27 |
| fips | empty | 25 |
| fips | clean FIPS (5-digit) | 22 |
| fips | mixed / not FIPS | 6 |
| geometry | text place | 4 |
| geometry | coded place (numbers) | 2 |
| metro | text place | 28 |
| metro | coded place (numbers) | 26 |
| metro | not measured | 1 |
| region | text place | 51 |
| region | coded place (numbers) | 28 |
| region | empty | 10 |
| region | not measured | 2 |
| region | constant | 1 |
| state | clean 2-letter state | 347 |
| state | state names (not codes) | 68 |
| state | mixed / not a state | 23 |
| state | state as a numeric code (FIPS / ICPSR) | 21 |
| state | empty | 18 |
| state | constant | 14 |
| state | not measured | 2 |
| watershed | coded place (numbers) | 3 |
| watershed | text place | 1 |
| zip | clean ZIP | 148 |
| zip | mixed / not a ZIP | 42 |
| zip | empty | 15 |
| zip | ZIP with leading zeros lost | 10 |
| zip | foreign postal code | 7 |
| zip | constant | 3 |
| zip | not measured | 2 |

## Columns that are NOT what their name says (empty, constant, mixed, trapped)

| table | column | kind | verdict | note | top values |
|---|---|---|---|---|---|
| CIVIL_RIGHTS__FED_NARA_WRA_AAD | CAMP_LOCATION | facility_site | empty | no real values (blank or sentinel only) | [] |
| CIVIL_RIGHTS__FED_NARA_WRA_AAD | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | ZIP_CODE | zip | mixed / not a ZIP | only 93% look like ZIPs | [["XXXXX", 147953], ["33319", 54827], ["75071", 54191], ["30606", 54186], ["1045 |
| CONSUMER_SAFETY__FED_CPSC_NEISS | LOCATION_CODE | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 4377766], ["0", 2830022], ["9", 1208001], ["5", 627932], ["8", 499424]] |
| CORPORATE_REGISTRY__INTL_ES_BORME | COUNTRY | country | constant | one value for the whole table | [["SPAIN", 3]] |
| CORPORATE_REGISTRY__INTL_ES_BORME | PROVINCE | state | empty | no real values (blank or sentinel only) | [] |
| CORPORATE_REGISTRY__INTL_IE_CRO | COUNTRY | country | constant | one value for the whole table | [["IE", 821693]] |
| CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | ADDRESS_PREMISES | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 245902], ["2", 200205], ["71-75", 184048], ["5", 179612], ["3", 172439]] |
| CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | ADDRESS_POSTAL_CODE | zip | foreign postal code | only 1% look like US ZIPs | [["WC2H 9JQ", 198588], ["N1 7GU", 170297], ["EC1V 2NX", 168292], ["CF14 8LH", 97 |
| ECONOMICS__FED_BLS_QCEW | AREA_FIPS | fips | FIPS with leading zeros lost | 84% have a FIPS length; modal length 5 -- pad before joining | [["C4530", 10093], ["47065", 9988], ["20055", 9940], ["16019", 6791], ["08005",  |
| ECONOMICS__FED_BLS_QCEW | STATE_FIPS | fips | mixed / not FIPS | only 84% have a FIPS length; modal length 2 | [["48", 212671], ["C1", 146470], ["C4", 139462], ["C2", 139040], ["C3", 135996]] |
| ECONOMICS__FED_DOL_FORM5500 | ADMIN_ADDRESS_SAME_SPON_IND | address | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | ADMIN_FOREIGN_ADDRESS1 | address | constant | one value for the whole table | [["836, 16TH MAIN ROAD", 1]] |
| ECONOMICS__FED_DOL_FORM5500 | ADMIN_FOREIGN_ADDRESS2 | address | constant | one value for the whole table | [["BANASHANKARI 2 STAGE", 1]] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_FOREIGN_ADDRESS1 | address | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_FOREIGN_ADDRESS2 | address | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_US_ADDRESS1 | address | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_US_ADDRESS2 | address | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | ADMIN_FOREIGN_CITY | city | constant | one value for the whole table | [["BENGALURU", 1]] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_FOREIGN_CITY | city | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_US_CITY | city | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | ADMIN_FOREIGN_CNTRY | country | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_FOREIGN_CNTRY | country | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | SPONS_DFE_LOC_FOREIGN_CNTRY | country | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | SPONS_DFE_MAIL_FOREIGN_CNTRY | country | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | ADMIN_FOREIGN_PROV_STATE | state | constant | one value for the whole table | [["KARNATAKA", 1]] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_FOREIGN_PROV_STATE | state | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_US_STATE | state | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | SPONS_DFE_LOC_FORGN_PROV_ST | state | constant | one value for the whole table | [["KARNATAKA", 5]] |
| ECONOMICS__FED_DOL_FORM5500 | ADMIN_FOREIGN_POSTAL_CD | zip | constant | one value for the whole table | [["560070", 1]] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_FOREIGN_POSTAL_CD | zip | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_US_ZIP | zip | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_DOL_FORM5500 | SPONS_DFE_LOC_FORGN_POSTAL_CD | zip | constant | one value for the whole table | [["560070", 5]] |
| ECONOMICS__FED_DOL_FORM5500 | SPONS_DFE_MAIL_FORGN_POSTAL_CD | zip | foreign postal code | only 2% look like US ZIPs; only 0.4% of rows filled | [["560070", 106], ["L4G 7L6", 3], ["RG1 1NB", 1], ["R3T 0M8", 1], ["44452", 1]] |
| ECONOMICS__FED_FDIC_FAILED_BANKS | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_FDIC_FAILED_BANKS | STATE_ABBR | state | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_FDIC_FAILED_BANKS | STATE_NAME | state | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_FINCEN_BOI | BENEFICIAL_OWNER_ADDRESS | address | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_FINCEN_BOI | BENEFICIAL_OWNER_ID_ISSUING_JURISDICTION | region | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_FINCEN_BOI | JURISDICTION_OF_FORMATION | region | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_FINCEN_BOI | US_REGISTRATION_STATE | state | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_IRS_990 | STATE | state | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_IRS_990 | ZIP_CODE | zip | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_IRS_AUTO_REVOCATIONS | COUNTRY | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["US", 1205162], ["CA", 619], ["UK", 257], ["FR", 94], ["SC", 89]] |
| ECONOMICS__FED_IRS_EO_PR | STATE | state | constant | one value for the whole table | [["PR", 2587]] |
| ECONOMICS__FED_IRS_PUB78_ELIGIBLE_DONEES | COUNTRY | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 1434673], ["CANADA", 376], ["AFGHANISTAN", 55], ["UNITED KING |
| ECONOMICS__FED_IRS_REVOCATION | COUNTRY | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["US", 1185240], ["CA", 616], ["UK", 256], ["FR", 94], ["SC", 89]] |
| ECONOMICS__FED_IRS_SOI_CHARITIES | STATE | state | mixed / not a state | only 84% are 2-letter US codes (foreign provinces, money, or free text) | [["VI", 568], ["GU", 160], ["MP", 110], ["AE", 93], ["AS", 82]] |
| ECONOMICS__FED_SBA_LOANS | CONGRESSIONAL_DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 282005], ["2", 232469], ["3", 200125], ["4", 163810], ["6", 131746]] |
| ECONOMICS__FED_SBA_LOANS | BORROWER_ZIP | zip | mixed / not a ZIP | only 89% look like ZIPs | [["68127", 5241], ["10016", 5240], ["19128", 5240], ["30312", 4789], ["32701", 4 |
| ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | RECIPIENT_CITY_CODE | city | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["00000", 1139761], ["22000", 171500], ["84452", 169139], ["04000", 167939], [" |
| ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_CODE | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["USA", 17784819], ["GBR", 7217], ["CAN", 4057], ["ZAF", 2731], ["KEN", 2723]] |
| ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_NAME | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 17784819], ["UNITED KINGDOM", 7217], ["CANADA", 4057], ["SOUT |
| ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | RECIPIENT_COUNTRY_CODE | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["USA", 17259333], ["GBR", 7653], ["CAN", 4099], ["CHE", 2508], ["ZAF", 2435]] |
| ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | RECIPIENT_COUNTRY_NAME | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 17259333], ["UNITED KINGDOM", 7653], ["CANADA", 4099], ["SWIT |
| ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE | fips | FIPS with leading zeros lost | 88% have a FIPS length; modal length 5 -- pad before joining | [["06037", 277264], ["06111", 250779], ["06059", 209484], ["26163", 203957], ["2 |
| ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | RECIPIENT_FOREIGN_POSTAL_CODE | zip | ZIP with leading zeros lost | 30% are 1-4 digits (00501 -> 501); only 0.0% of rows filled | [["POSTAL_CODE", 365], ["1202", 180], ["11000", 74], ["1212", 71], ["007700", 71 |
| ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | RECIPIENT_ZIP_LAST_4_CODE | zip | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) | [["0000", 586543], ["0001", 316117], ["1906", 142446], ["3163", 138289], ["4444" |
| ECONOMICS__FED_USASPENDING_CONTRACTS | RECIPIENT_COUNTRY_NAME | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 6201651], ["SWITZERLAND", 25570], ["JAPAN", 14091], ["KUWAIT" |
| ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | STATE_CONTROLLED_INSTITUTION_OF_HIGHER_LEARNING | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["F", 19962205], ["T", 37795]] |
| ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | US_STATE_GOVERNMENT | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["F", 19928696], ["T", 71304]] |
| ECONOMICS__FED_US_USASPENDING_API | PLACE_OF_PERFORMANCE_CITY | city | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_US_USASPENDING_API | PLACE_OF_PERFORMANCE_FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_US_USASPENDING_API | RECIPIENT_LOCATION_FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__FED_US_USASPENDING_API | RECIPIENT_LOCATION_STATE | state | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_3_CITY | city | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_4_CITY | city | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_5_CITY | city | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_CITY | city | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_CITY | city | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_CITY | city | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_3_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_4_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_5_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_3_REGION | region | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_4_REGION | region | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_5_REGION | region | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_REGION | region | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_REGION | region | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_REGION | region | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_HEADQUARTERSADDRESS_POSTALCODE | zip | mixed / not a ZIP | only 41% look like ZIPs | [["VG1110", 24209], ["75008", 22421], ["100000", 15608], ["19808", 12311], ["949 |
| ECONOMICS__INTL_GLEIF | ENTITY_LEGALADDRESS_POSTALCODE | zip | mixed / not a ZIP | only 40% look like ZIPs | [["19801", 64434], ["19808", 53177], ["VG1110", 33386], ["75008", 22104], ["1990 |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_1_POSTALCODE | zip | mixed / not a ZIP | only 19% look like ZIPs; only 1.3% of rows filled | [["104-6228", 6308], ["107-8472", 3888], ["105-8579", 1635], ["100-0004", 1330], |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_2_POSTALCODE | zip | mixed / not a ZIP | only 18% look like ZIPs; only 1.3% of rows filled | [["104-6228", 6305], ["107-8472", 3885], ["105-8579", 1632], ["100-0004", 1320], |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_3_POSTALCODE | zip | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_4_POSTALCODE | zip | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_OTHERADDRESSES_OTHERADDRESS_5_POSTALCODE | zip | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_1_POSTALCODE | zip | ZIP with leading zeros lost | 42% are 1-4 digits (00501 -> 501); only 2.3% of rows filled | [["2100", 730], ["L-2520", 672], ["8230", 508], ["4700", 500], ["3460", 490]] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_2_POSTALCODE | zip | ZIP with leading zeros lost | 43% are 1-4 digits (00501 -> 501); only 2.3% of rows filled | [["2100", 719], ["4700", 537], ["2860", 522], ["2610", 519], ["6000", 499]] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_POSTALCODE | zip | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_POSTALCODE | zip | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_GLEIF | ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_POSTALCODE | zip | empty | no real values (blank or sentinel only) | [] |
| ECONOMICS__INTL_IT_ISTAT | COUNTRY | country | constant | one value for the whole table | [["IT", 213284]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | ASSET_MGR_POSITIONS_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 2598], ["1634", 165], ["65", 115], ["350", 112], ["220", 88]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | CHANGE_IN_ASSET_MGR_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 3881], [".", 659], ["-3", 154], ["2", 154], ["91", 152]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | CHANGE_IN_DEALER_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 3554], [".", 660], ["3", 208], ["-5", 156], ["180", 156]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | CHANGE_IN_LEV_MONEY_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 1101], [".", 660], ["172", 119], ["-17", 119], ["-20", 119]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | CHANGE_IN_NONREPT_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 801], [".", 660], ["2", 249], ["-1", 233], ["1", 208]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | CHANGE_IN_OTHER_REPT_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 7134], [".", 657], ["25", 203], ["-25", 163], ["6", 142]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | CHANGE_IN_TOT_REPT_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [[".", 660], ["-115", 122], ["1147", 122], ["137", 121], ["-864", 121]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | DEALER_POSITIONS_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 2559], ["333", 112], ["1177", 106], ["136", 106], ["272", 104]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | LEV_MONEY_POSITIONS_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 733], ["1033", 121], ["654", 66], ["11788", 66], ["2327", 66]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | NONREPT_POSITIONS_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 379], ["10", 161], ["281", 132], ["392", 131], ["596", 123]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | OTHER_REPT_POSITIONS_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 5602], ["30", 122], ["800", 114], ["25", 111], ["400", 100]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | PCT_OF_OI_ASSET_MGR_LONG_ALL | coordinates | coordinate with 0,0 trap | 8% are exactly 0 (Gulf of Guinea rows) | [["0.0", 2694], ["0.2", 391], ["0.3", 323], ["0.4", 305], ["0.5", 289]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | PCT_OF_OI_DEALER_LONG_ALL | coordinates | coordinate with 0,0 trap | 7% are exactly 0 (Gulf of Guinea rows) | [["0.0", 2574], ["0.4", 282], ["0.5", 272], ["1.9", 267], ["1.2", 267]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | PCT_OF_OI_OTHER_REPT_LONG_ALL | coordinates | coordinate with 0,0 trap | 17% are exactly 0 (Gulf of Guinea rows) | [["0.0", 5727], ["0.8", 502], ["0.5", 486], ["0.6", 461], ["1.1", 453]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | TOT_REPT_POSITIONS_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["1766", 68], ["203649", 68], ["188118", 68], ["188674", 68], ["187566", 68]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | TRADERS_TOT_REPT_LONG_ALL | coordinates | coordinate, partly out of range | 82% parse in range | [["16", 722], ["15", 711], ["14", 699], ["13", 628], ["17", 625]] |
| EDUCATION__FED_CFTC_COT_FINANCIAL | CFTC_REGION_CODE | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["00", 32260], ["01", 2423]] |
| EDUCATION__FED_CFTC_COT_FUTURES | CHANGE_IN_COMMERCIAL_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 15948], [".", 4617], ["60", 1302], ["150", 1123], ["25", 1103]] |
| EDUCATION__FED_CFTC_COT_FUTURES | CHANGE_IN_NONCOMMERCIAL_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 56825], [".", 4614], ["50", 1909], ["-25", 1535], ["25", 1365]] |
| EDUCATION__FED_CFTC_COT_FUTURES | CHANGE_IN_NONREPORTABLE_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 46246], [".", 4627], ["10", 2058], ["-10", 1933], ["-5", 1842]] |
| EDUCATION__FED_CFTC_COT_FUTURES | CHANGE_IN_TOTAL_REPORTABLE_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 10488], [".", 4620], ["220", 1165], ["130", 1161], ["95", 1148]] |
| EDUCATION__FED_CFTC_COT_FUTURES | COMMERCIAL_POSITIONS_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 4044], ["497", 706], ["593", 705], ["379", 705], ["1360", 630]] |
| EDUCATION__FED_CFTC_COT_FUTURES | COMMERCIAL_POSITIONS_LONG_OLD | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 4560], ["3402", 867], ["568", 704], ["380", 704], ["379", 704]] |
| EDUCATION__FED_CFTC_COT_FUTURES | COMMERCIAL_POSITIONS_LONG_OTHER | coordinates | coordinate with 0,0 trap | 87% are exactly 0 (Gulf of Guinea rows) | [["0", 250765], ["1", 137], ["4", 135], ["8", 132], ["12", 119]] |
| EDUCATION__FED_CFTC_COT_FUTURES | NONCOMMERCIAL_POSITIONS_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 27100], ["25", 1099], ["105", 1027], ["90", 883], ["121", 657]] |
| EDUCATION__FED_CFTC_COT_FUTURES | NONCOMMERCIAL_POSITIONS_LONG_OLD | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 27873], ["25", 1096], ["105", 1024], ["90", 882], ["128", 654]] |
| EDUCATION__FED_CFTC_COT_FUTURES | NONCOMMERCIAL_POSITIONS_LONG_OTHER | coordinates | coordinate with 0,0 trap | 89% are exactly 0 (Gulf of Guinea rows) | [["0", 254159], ["100", 138], ["1", 136], ["2", 121], ["25", 119]] |
| EDUCATION__FED_CFTC_COT_FUTURES | NONREPORTABLE_POSITIONS_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 16601], ["315", 1164], ["209", 1070], ["149", 1018], ["336", 898]] |
| EDUCATION__FED_CFTC_COT_FUTURES | NONREPORTABLE_POSITIONS_LONG_OLD | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 16899], ["60", 1621], ["95", 1318], ["343", 1134], ["145", 1126]] |
| EDUCATION__FED_CFTC_COT_FUTURES | NONREPORTABLE_POSITIONS_LONG_OTHER | coordinates | coordinate with 0,0 trap | 84% are exactly 0 (Gulf of Guinea rows) | [["0", 241961], ["1", 600], ["2", 444], ["5", 320], ["3", 277]] |
| EDUCATION__FED_CFTC_COT_FUTURES | OF_OI_COMMERCIAL_LONG_OTHER | coordinates | coordinate with 0,0 trap | 87% are exactly 0 (Gulf of Guinea rows) | [["0.0", 250834], ["100.0", 432], ["53.9", 208], ["63.4", 188], ["40.0", 167]] |
| EDUCATION__FED_CFTC_COT_FUTURES | OF_OI_NONCOMMERCIAL_LONG_ALL | coordinates | coordinate with 0,0 trap | 10% are exactly 0 (Gulf of Guinea rows) | [["0.0", 27735], ["0.2", 2492], ["0.3", 2491], ["0.1", 2452], ["0.6", 2334]] |
| EDUCATION__FED_CFTC_COT_FUTURES | OF_OI_NONCOMMERCIAL_LONG_OLD | coordinates | coordinate with 0,0 trap | 10% are exactly 0 (Gulf of Guinea rows) | [["0.0", 28503], ["0.2", 2486], ["0.3", 2481], ["0.1", 2444], ["0.6", 2327]] |
| EDUCATION__FED_CFTC_COT_FUTURES | OF_OI_NONCOMMERCIAL_LONG_OTHER | coordinates | coordinate with 0,0 trap | 89% are exactly 0 (Gulf of Guinea rows) | [["0.0", 254199], ["32.5", 200], ["13.3", 181], ["27.7", 173], ["24.0", 171]] |
| EDUCATION__FED_CFTC_COT_FUTURES | OF_OI_NONREPORTABLE_LONG_ALL | coordinates | coordinate with 0,0 trap | 7% are exactly 0 (Gulf of Guinea rows) | [["0.0", 20387], ["0.1", 5457], ["0.2", 4983], ["0.3", 4490], ["0.4", 4357]] |
| EDUCATION__FED_CFTC_COT_FUTURES | OF_OI_NONREPORTABLE_LONG_OLD | coordinates | coordinate with 0,0 trap | 7% are exactly 0 (Gulf of Guinea rows) | [["0.0", 20691], ["0.1", 5460], ["0.2", 4984], ["0.3", 4488], ["0.4", 4350]] |
| EDUCATION__FED_CFTC_COT_FUTURES | OF_OI_NONREPORTABLE_LONG_OTHER | coordinates | coordinate with 0,0 trap | 84% are exactly 0 (Gulf of Guinea rows) | [["0.0", 241966], ["100.0", 6813], ["8.8", 298], ["8.5", 287], ["9.7", 284]] |
| EDUCATION__FED_CFTC_COT_FUTURES | OF_OI_TOTAL_REPORTABLE_LONG_OTHER | coordinates | coordinate with 0,0 trap | 86% are exactly 0 (Gulf of Guinea rows) | [["0.0", 248196], ["100.0", 596], ["91.2", 298], ["91.5", 287], ["90.1", 266]] |
| EDUCATION__FED_CFTC_COT_FUTURES | TOTAL_REPORTABLE_POSITIONS_LONG_ALL | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["977", 713], ["1847", 712], ["1029", 712], ["1034", 712], ["435", 393]] |
| EDUCATION__FED_CFTC_COT_FUTURES | TOTAL_REPORTABLE_POSITIONS_LONG_OLD | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["1146", 712], ["953", 712], ["0", 398], ["1384", 394], ["26", 393]] |
| EDUCATION__FED_CFTC_COT_FUTURES | TOTAL_REPORTABLE_POSITIONS_LONG_OTHER | coordinates | coordinate with 0,0 trap | 86% are exactly 0 (Gulf of Guinea rows) | [["0", 248197], ["1", 146], ["8", 138], ["25", 112], ["200", 101]] |
| EDUCATION__FED_CFTC_COT_FUTURES | TRADERS_TOTAL_REPORTABLE_LONG_ALL | coordinates | coordinate, partly out of range | 91% parse in range | [["17", 9376], ["18", 9325], ["16", 9017], ["19", 8830], ["20", 8072]] |
| EDUCATION__FED_CFTC_COT_FUTURES | TRADERS_TOTAL_REPORTABLE_LONG_OLD | coordinates | coordinate, partly out of range | 92% parse in range | [["17", 9378], ["18", 9316], ["16", 9064], ["19", 8826], ["20", 8124]] |
| EDUCATION__FED_CFTC_COT_FUTURES | TRADERS_TOTAL_REPORTABLE_LONG_OTHER | coordinates | coordinate with 0,0 trap | 86% are exactly 0 (Gulf of Guinea rows) | [["0", 248197], ["1", 3329], ["2", 2197], ["3", 1562], ["4", 1307]] |
| EDUCATION__FED_CFTC_COT_FUTURES | CFTC_REGION_CODE | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["01", 187064], ["00", 99989]] |
| EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION | STATE_FIPS | fips | FIPS with leading zeros lost | 82% have a FIPS length; modal length 2 -- pad before joining | [["6", 664], ["36", 417], ["48", 411], ["12", 377], ["42", 317]] |
| EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION | REGION_CODE | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["5", 1585], ["2", 1004], ["3", 918], ["8", 901], ["6", 687]] |
| EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION | TUITION_IN_STATE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["13920", 45], ["9400", 38], ["18484", 37], ["17408", 35], ["17048", 33]] |
| EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION | TUITION_OUT_OF_STATE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["13920", 45], ["18484", 37], ["11120", 37], ["17408", 35], ["17048", 33]] |
| EDUCATION__FED_ED_EDFACTS | STATE_FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_GEO_SPEND | COUNTRY | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["US", 614077], ["GB", 1]] |
| EDUCATION__FED_SENATE_LDA_FILINGS | REGISTRANT_COUNTRY | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["US", 437532], ["CA", 180], ["PR", 112], ["GB", 64], ["AT", 44]] |
| ENERGY__FED_EIA860_1_UTILITY | ZIP | zip | mixed / not a ZIP | only 85% look like ZIPs | [["33408", 396], ["37201", 153], ["2110", 150], ["10017", 149], ["28801", 133]] |
| ENERGY__FED_EIA860_2_PLANT | ZIP | zip | mixed / not a ZIP | only 88% look like ZIPs | [["93210", 122], ["86001", 121], ["12883", 121], ["8721", 120], ["14136", 120]] |
| ENERGY__FED_EIA860_4_OWNER | OWNER_ZIP | zip | mixed / not a ZIP | only 86% look like ZIPs | [["20814", 231], ["27701", 166], ["68154", 126], ["94111", 121], ["8540", 76]] |
| ENERGY__FED_EIA861_DELIVERY_COMPANIES | STATE | state | constant | one value for the whole table | [["TX", 7]] |
| ENVIRONMENT__EPA_PENALTY_GAP | TRI_ON_SITE_RELEASES | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 3.4% of rows filled | [["0", 539], ["1", 78], ["5", 44], ["2", 42], ["10", 41]] |
| ENVIRONMENT__EPA_PENALTY_GAP | EPA_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["05", 13744], ["03", 12748], ["04", 12380], ["06", 11736], ["02", 8633]] |
| ENVIRONMENT__FED_EPA_AQS_SITES | MET_SITE_DISTANCE | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 3.1% of rows filled | [["10", 40], ["20600", 9], ["16000", 8], ["1", 8], ["13877", 7]] |
| ENVIRONMENT__FED_EPA_AQS_SITES | MET_SITE_SITE_NUMBER | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 2.1% of rows filled | [["0001", 28], ["0004", 27], ["0003", 27], ["0002", 22], ["0006", 17]] |
| ENVIRONMENT__FED_EPA_AQS_SITES | SITE_CLOSED_DATE | facility_site | not a place (dates) | name-scan false hit | [["1981-12-31", 493], ["1977-12-31", 458], ["1974-12-31", 430], ["1978-12-31", 4 |
| ENVIRONMENT__FED_EPA_AQS_SITES | SITE_ESTABLISHED_DATE | facility_site | not a place (dates) | name-scan false hit | [["1973-01-01", 1162], ["1972-01-01", 1078], ["1971-01-01", 876], ["1969-01-01", |
| ENVIRONMENT__FED_EPA_AQS_SITES | SITE_NUMBER | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0001", 1902], ["0002", 1412], ["0003", 1091], ["0004", 882], ["1001", 774]] |
| ENVIRONMENT__FED_EPA_AQS_SITES | MET_SITE_STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining; only 2.1% of rows filled | [["21", 88], ["08", 58], ["18", 41], ["42", 35], ["29", 35]] |
| ENVIRONMENT__FED_EPA_AQS_SITES | STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["39", 1061], ["06", 1042], ["12", 965], ["42", 830], ["48", 813]] |
| ENVIRONMENT__FED_EPA_ECHO | TRI_ON_SITE_RELEASES | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 0.4% of rows filled | [["0", 5729], ["1", 584], ["5", 325], ["10", 295], ["2", 285]] |
| ENVIRONMENT__FED_EPA_ECHO | EPA_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["04", 583096], ["05", 405513], ["06", 315392], ["09", 256882], ["03", 224022]] |
| ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | PLANT_FIPS_COUNTY_CODE | fips | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining | [["037", 370], ["001", 340], ["029", 339], ["027", 330], ["013", 324]] |
| ENVIRONMENT__FED_EPA_ENVIROFACTS | LATITUDE | coordinates | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_EPA_ENVIROFACTS | LONGITUDE | coordinates | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_EPA_ENVIROFACTS | SITE_ID | facility_site | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_EPA_ENVIROFACTS | STATE_CODE | state | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_EPA_FRS_FACILITIES | CONGRESSIONAL_DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["01", 422262], ["02", 396730], ["03", 372608], ["04", 291020], ["05", 256364]] |
| ENVIRONMENT__FED_EPA_FRS_FACILITIES | FIPS_CODE | fips | FIPS with leading zeros lost | 85% have a FIPS length; modal length 5 -- pad before joining | [["06037", 171534], ["06059", 75221], ["06073", 65403], ["06085", 41302], ["1703 |
| ENVIRONMENT__FED_EPA_FRS_FACILITIES | EPA_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["04", 861269], ["05", 808975], ["02", 607963], ["09", 604935], ["06", 547648]] |
| ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES | FAC_EPA_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["04", 591164], ["05", 435976], ["06", 331332], ["09", 305567], ["03", 224034]] |
| ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS | COUNTRY_NAME | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 1869505], ["USA", 733766], ["US", 243848], ["UNITED STATES OF |
| ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS | FIPS_CODE | fips | FIPS with leading zeros lost | 66% have a FIPS length; modal length 5 -- pad before joining | [["06037", 180763], ["06059", 80534], ["06073", 71565], ["06085", 43152], ["0600 |
| ENVIRONMENT__FED_EPA_GHGRP_FACILITY | ADDRESS2 | address | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES | EPA_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["06", 51238], ["05", 50408], ["08", 42327], ["03", 35314], ["04", 31596]] |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES | STATE_EPA_FLAG | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["S", 1555853], ["L", 169496], ["E", 53747]] |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS | STATE_EPA_FLAG | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["S", 69340], ["L", 20906], ["E", 15763]] |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS | STATE_EPA_FLAG | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["S", 138921], ["L", 27124], ["E", 9691]] |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS | STATE_EPA_FLAG | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["S", 440329], ["L", 176069], ["E", 3904]] |
| ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS | STATE_EPA_FLAG | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["S", 406212], ["L", 91571], ["E", 1330]] |
| ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS | STATE_LOCAL_PENALTY_AMT | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["1000", 2130], ["500", 1462], ["5000", 1258], ["2000", 1048], ["3000", 991]] |
| ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS | STATE_EPA_FLAG | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["S", 1789658], ["E", 110409]] |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | COUNTRY_CODE | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["US", 424704], ["CA", 21], ["SW", 1]] |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | EPA_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["05", 127401], ["04", 67771], ["03", 45839], ["02", 43695], ["06", 34515]] |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | STATE_MCL | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining; only 3.7% of rows filled | [["0", 1425657], [".08", 145439], [".01", 81702], ["10", 78531], [".06", 62463]] |
| ENVIRONMENT__FED_EPA_SUPERFUND_SITE_BOUNDARIES | SITE_FEATURE_CLASS | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["5", 2108], ["51", 5], ["52", 1]] |
| ENVIRONMENT__FED_EPA_SUPERFUND_SITE_BOUNDARIES | EPA_REGION_CODE | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["5", 372], ["10", 314], ["2", 310], ["4", 285], ["3", 227]] |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_104_OFF_SITE_TREATED_TOTAL | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 66814], ["1", 188], ["5", 137], ["2", 114], ["3", 95]] |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_109_8_1_A_ON_SITE_CONTAINED | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.000", 74869], ["1.000", 64], ["2.000", 39], ["5.000", 38], ["0.100", 29]] |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_110_8_1_B_ON_SITE_OTHER | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.000", 23000], ["10.000", 1043], ["5.000", 1003], ["1.000", 839], ["2.000",  |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_111_8_1_C_OFF_SITE_CONTAIN | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.000", 61940], ["1.000", 382], ["5.000", 332], ["2.000", 221], ["3.000", 139 |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_112_8_1_D_OFF_SITE_OTHER_R | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.000", 60838], ["5.000", 337], ["1.000", 302], ["2.000", 177], ["250.000", 1 |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_115_8_4_RECYCLING_ON_SITE | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.000", 74778], ["118.500", 30], ["7.000", 28], ["500.000", 28], ["5.674", 17 |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_117_8_6_TREATMENT_ON_SITE | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.000", 61863], ["20000.000", 125], ["16000.000", 125], ["12000.000", 124], [ |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_118_8_7_TREATMENT_OFF_SITE | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.000", 66852], ["1.000", 190], ["5.000", 138], ["2.000", 114], ["4.000", 95] |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_65_ON_SITE_RELEASE_TOTAL | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 22486], ["10", 1033], ["5", 1028], ["1", 817], ["2", 534]] |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_88_OFF_SITE_RELEASE_TOTAL | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 52295], ["1", 509], ["5", 509], ["2", 289], ["250", 232]] |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_94_OFF_SITE_RECYCLED_TOTAL | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 59824], ["5", 144], ["1", 142], ["250", 141], ["39.96", 81]] |
| ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_97_OFF_SITE_ENERGY_RECOVERY_T | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.000", 71330], ["1.000", 140], ["2.000", 87], ["3.000", 66], ["5.000", 64]] |
| ENVIRONMENT__FED_EPA_TRI_FACILITY | FAC_LATITUDE | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 2918], ["474045", 364], ["673442", 363], ["474000", 363], ["474141", 363] |
| ENVIRONMENT__FED_EPA_TRI_FACILITY | FAC_LONGITUDE | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 2919], ["1171215", 364], ["1191659", 363], ["1183603", 363], ["1313800",  |
| ENVIRONMENT__FED_EPA_TRI_FACILITY | MAIL_COUNTRY | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis; only 1.1% of rows filled | [["UNITED STATES", 731], ["CANADA", 11]] |
| ENVIRONMENT__FED_EPA_TRI_FACILITY | REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["5", 15508], ["4", 13222], ["6", 7813], ["9", 6514], ["3", 5626]] |
| ENVIRONMENT__FED_NOAA_STORM_EVENTS | CZ_FIPS | fips | FIPS with leading zeros lost | 58% have a FIPS length; modal length 2 -- pad before joining | [["3", 33850], ["1", 30176], ["19", 28588], ["5", 27971], ["13", 26970]] |
| ENVIRONMENT__FED_NOAA_STORM_EVENTS | STATE_FIPS | fips | FIPS with leading zeros lost | 89% have a FIPS length; modal length 2 -- pad before joining | [["48", 131060], ["20", 77995], ["29", 62687], ["40", 62023], ["19", 61067]] |
| ENVIRONMENT__FED_NOAA_STORM_EVENTS | TOR_OTHER_CZ_FIPS | fips | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining; only 0.2% of rows filled | [["017", 72], ["083", 63], ["125", 62], ["089", 56], ["035", 53]] |
| ENVIRONMENT__FED_NOAA_WEATHER_API | LATITUDE | coordinates | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_NOAA_WEATHER_API | LONGITUDE | coordinates | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_NOAA_WEATHER_API | FIPS_CODE | fips | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_NOAA_WEATHER_API | ZIP_CODE | zip | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_USCG_NRC_INCIDENTS | RESPONSIBLE_ZIP | zip | mixed / not a ZIP | only 65% look like ZIPs | [["30303", 4029], ["32202", 3306], ["70357.0", 2792], ["77002", 2752], ["30303.0 |
| ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS | RESPONSIBLE_ZIP | zip | mixed / not a ZIP | only 94% look like ZIPs | [["77002", 1136], ["30308", 408], ["32202", 361], ["77380", 359], ["70669", 317] |
| ENVIRONMENT__FED_USGS_MINERALS | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_USGS_MINERALS | US_STATE | state | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__FED_USGS_WATER | SITE_NO | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["11509500", 25459], ["07104905", 24877], ["14337500", 24312], ["12324200", 189 |
| ENVIRONMENT__FED_USGS_WATER | STATE_CD | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["48", 1450195], ["06", 848281], ["08", 774033], ["12", 696455], ["41", 692953] |
| ENVIRONMENT__FED_USGS_WATER | HUC_CD | watershed | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["12090205", 114489], ["03070103", 110722], ["03090202", 106266], ["03130001",  |
| ENVIRONMENT__FED_USGS_WBD_HUC8 | SHAPE_AREA | geometry | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["130104954.540845", 19], ["139723373.866989", 19], ["154120820.276846", 19], [ |
| ENVIRONMENT__FED_USGS_WBD_HUC8 | SHAPE_LENGTH | geometry | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["40466.60009307", 19], ["42100.038169646", 19], ["44193.23340935", 19], ["6117 |
| ENVIRONMENT__FED_USGS_WBD_HUC8 | HUC8 | watershed | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["22040007", 19], ["22040006", 19], ["22040005", 19], ["22040004", 19], ["22040 |
| ENVIRONMENT__FED_WQP_MONITORING_STATIONS | COUNTRY_CODE | country | constant | one value for the whole table | [["US", 5818]] |
| ENVIRONMENT__FED_WQP_MONITORING_STATIONS | STATE_CODE | state | constant | one value for the whole table | [["44", 5818]] |
| ENVIRONMENT__FED_WQP_MONITORING_STATIONS | HUC_EIGHT_DIGIT_CODE | watershed | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["01090005", 2657], ["01090004", 1922], ["01090003", 785], ["01100001", 51], [" |
| ENVIRONMENT__INTL_GEM_HAZARD | LATITUDE | coordinates | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__INTL_GEM_HAZARD | LONGITUDE | coordinates | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__INTL_GEM_HAZARD | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| ENVIRONMENT__INTL_GLOBAL_WITNESS_DEFENDERS | REGION | region | empty | no real values (blank or sentinel only) | [] |
| FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS | EPA_REGION_CODE | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["08", 43015], ["02", 34977], ["06", 30302], ["04", 27564], ["05", 24122]] |
| FINANCE__FED_FARA | FOREIGN_PRINCIPAL_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| FINANCE__FED_FDIC_BANK_DATA | LATITUDE | coordinates | coordinate with 0,0 trap | 10% are exactly 0 (Gulf of Guinea rows) | [["0.0000", 2854], ["38.7749", 67], ["39.0863", 67], ["38.7033", 67], ["40.4906" |
| FINANCE__FED_FDIC_BANK_DATA | LONGITUDE | coordinates | coordinate with 0,0 trap | 10% are exactly 0 (Gulf of Guinea rows) | [["0.0000", 2854], ["-85.3944", 67], ["-84.4782", 67], ["-90.2953", 67], ["-81.4 |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | FED_DISTRICT_CODE | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["4", 393128], ["5", 391709], ["6", 301122], ["7", 282672], ["12", 253367]] |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | OCC_DISTRICT_CODE | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["3", 567416], ["1", 533959], ["5", 492758], ["4", 374682], ["2", 178963]] |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | BRANCH_COUNTRY | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 2807354], ["PUERTO RICO", 13308], ["GUAM", 878], ["VIRGIN ISL |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | INSTITUTION_COUNTRY | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 2734434], ["CANADA", 18370], ["PUERTO RICO", 13955], ["SPAIN" |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | BRANCH_PLACE_CODE | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 746129], ["91835", 12333], ["91750", 11504], ["14000", 10218], ["44919",  |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | BRANCH_COUNTY_FIPS | fips | FIPS with leading zeros lost | 59% have a FIPS length; modal length 2 -- pad before joining | [["31", 88302], ["3", 86919], ["37", 79380], ["13", 70292], ["1", 65245]] |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | BRANCH_STATE_COUNTY_FIPS | fips | FIPS with leading zeros lost | 85% have a FIPS length; modal length 5 -- pad before joining | [["6037", 53046], ["17031", 43096], ["48201", 28483], ["4013", 23492], ["36061", |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | BRANCH_STATE_FIPS | fips | FIPS with leading zeros lost | 85% have a FIPS length; modal length 2 -- pad before joining | [["6", 212213], ["48", 187975], ["12", 157050], ["36", 155190], ["42", 138987]] |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | INSTITUTION_STATE_COUNTY_FIPS | fips | FIPS with leading zeros lost | 88% have a FIPS length; modal length 5 -- pad before joining | [["37119", 184207], ["46099", 124350], ["39041", 99759], ["39061", 98411], ["100 |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | BRANCH_CBSA_DIVISION_CODE | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 2153507], ["35614", 106537], ["31084", 52991], ["16974", 51324], ["47894" |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | BRANCH_CSA_CODE | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 793070], ["408", 205711], ["348", 94327], ["176", 89439], ["548", 80642]] |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | BRANCH_METRO_FLAG | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 2134645], ["0", 596498]] |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | BRANCH_MSA_CODE | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 615632], ["35620", 168671], ["16980", 84421], ["31080", 73009], ["37980", |
| FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | FDIC_REGION_CODE | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["9", 634724], ["5", 587409], ["2", 499406], ["11", 380383], ["13", 332663]] |
| FINANCE__FED_FEC_CANDIDATES | CAND_OFFICE_DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["00", 8769], ["01", 1895], ["02", 1800], ["03", 1620], ["04", 1329]] |
| FINANCE__FED_IRS_SOI | STATE_FIPS | fips | FIPS with leading zeros lost | 87% have a FIPS length; modal length 2 -- pad before joining | [["48", 10563], ["36", 9977], ["6", 9724], ["42", 9711], ["17", 7764]] |
| FINANCE__FED_IRS_SOI | ZIP_CODE | zip | mixed / not a ZIP | only 92% look like ZIPs | [["40065", 426], ["40062", 426], ["40060", 426], ["40059", 426], ["40057", 426]] |
| FINANCE__FED_NCUA_CHARTER_MERGER_EVENTS | REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["3", 13], ["2", 7], ["1", 7]] |
| FINANCE__FED_NCUA_FEDERALLY_INSURED_CU_LIST | NCUA_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["2", 1499], ["1", 1382], ["3", 1357], ["8", 12]] |
| FINANCE__FED_SEC_13F_FILERS | FILINGMANAGER_ZIPCODE | zip | mixed / not a ZIP | only 87% look like ZIPs | [["10022", 15229], ["10019", 7036], ["10017", 6138], ["02116", 4275], ["10036",  |
| FINANCE__INTL_OSFI_REGULATED_FI | POSTAL_ZIP_CODE | zip | foreign postal code | only 0% look like US ZIPs | [["M5H 1J8", 10], ["L3Y 1K1", 9], ["M5K 0A1", 9], ["M5J 2J5", 7], ["M5H 0B4", 7] |
| GOVERNMENT_RECORDS__FED_NARA_AAD | GEO_LOCATION | facility_site | empty | no real values (blank or sentinel only) | [] |
| GOVERNMENT_RECORDS__FED_NARA_AAD | FIPS_GEO | fips | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CDC_DRUG_POISONING_COUNTY | FIPS_STATE | fips | FIPS with leading zeros lost | 90% have a FIPS length; modal length 2 -- pad before joining | [["48", 4318], ["13", 2703], ["51", 2276], ["21", 2040], ["29", 1955]] |
| HEALTH__FED_CMS_DIALYSIS | LONG_TERM_CATHETER_DATA_AVAILABILITY_CODE | coordinates | coordinate, partly out of range | 93% parse in range | [["1", 7057], ["199", 246], ["256", 129], ["201", 64], ["258", 61]] |
| HEALTH__FED_CMS_DIALYSIS | NUMBER_OF_PATIENT_MONTHS_IN_LONG_TERM_CATHETER_SUMMARY | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["3", 55], ["426", 55], ["659", 55], ["534", 55], ["361", 55]] |
| HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | LONG_STAY_RESIDENTS | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["_", 28336148], ["11", 130760], ["12", 118848], ["13", 113331], ["14", 104727] |
| HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | FIPS_COUNTY_CODE | fips | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining | [["037", 1062089], ["031", 876780], ["003", 718032], ["013", 658196], ["005", 64 |
| HEALTH__FED_CMS_HCRIS | OTHER_LONG_TERM_LIABILITIES | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["NAN", 2035], ["7686922", 31], ["44132958", 31], ["688551", 31], ["10551618",  |
| HEALTH__FED_CMS_HCRIS | TOTAL_LONG_TERM_LIABILITIES | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["NAN", 979], ["15390645", 38], ["49823108", 38], ["57964255", 38], ["89226631" |
| HEALTH__FED_CMS_HCRIS | MEDICARE_CBSA_NUMBER | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["99945", 141], ["99917", 99], ["31084", 98], ["26420", 96], ["19124", 85]] |
| HEALTH__FED_CMS_HCRIS | ZIP_CODE | zip | mixed / not a ZIP | only 80% look like ZIPs | [["02840", 45], ["75001", 45], ["62233", 45], ["72736", 45], ["07094", 45]] |
| HEALTH__FED_CMS_HOME_HEALTH | DENOMINATOR_FOR_HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["-", 3748], ["27", 67], ["60", 66], ["22", 66], ["20", 66]] |
| HEALTH__FED_CMS_HOME_HEALTH | HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["-", 3748], ["100.00", 901], ["93.28", 59], ["99.82", 59], ["98.44", 59]] |
| HEALTH__FED_CMS_HOME_HEALTH | NUMERATOR_FOR_HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["-", 3748], ["43", 72], ["22", 67], ["24", 66], ["21", 66]] |
| HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS | LOCATION_OTHER_TYPE_TEXT | facility_site | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS | PRACTICE_LOCATION_TYPE | facility_site | constant | one value for the whole table | [["HHA BRANCH", 2463]] |
| HEALTH__FED_CMS_HOSPICE | ADDRESS_LINE_2 | address | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_HOSPICE | CMS_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["9", 2502], ["6", 1438], ["5", 755], ["4", 737], ["3", 354]] |
| HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS | SUBGROUP_LONG_TERM | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["N", 8845], ["Y", 330]] |
| HEALTH__FED_CMS_HPT_MRF | HOSPITAL_ADDRESS | address | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_HPT_MRF | HOSPITAL_LOCATION | facility_site | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_IRF | CMS_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["6", 272], ["4", 257], ["5", 205], ["9", 121], ["3", 111]] |
| HEALTH__FED_CMS_LTCH | ADDRESS_LINE_2 | address | empty | no real values (blank or sentinel only) | [["-", 311]] |
| HEALTH__FED_CMS_LTCH | CMS_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["6", 77], ["4", 76], ["5", 43], ["9", 32], ["3", 27]] |
| HEALTH__FED_CMS_MAIN | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_MAIN | ZIP | zip | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER | RFRG_PRVDR_CNTRY | country | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER | RFRG_PRVDR_RUCA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 302510], ["4", 30298], ["7", 14337], ["2", 12692], ["10", 6855]] |
| HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL | SUPLR_PRVDR_CNTRY | country | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL | SUPLR_PRVDR_RUCA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 317231], ["4", 54200], ["7", 27550], ["2", 15378], ["10", 8092]] |
| HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER | RNDRNG_PRVDR_RUCA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 2056], ["4", 482], ["7", 198], ["2", 100], ["1.1", 48]] |
| HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | RNDRNG_PRVDR_RUCA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 127031], ["4", 10265], ["1.1", 2407], ["2", 2243], ["7", 1335]] |
| HEALTH__FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | RNDRNG_PRVDR_RUCA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 88168], ["4", 15951], ["7", 3786], ["2", 2617], ["1.1", 1859]] |
| HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER | RNDRNG_PRVDR_CNTRY | country | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER | RNDRNG_PRVDR_RUCA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 1099283], ["4", 79536], ["2", 36227], ["7", 29064], ["1.1", 17316]] |
| HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI | RNDRNG_PRVDR_CNTRY | country | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI | RNDRNG_PRVDR_RUCA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 8367594], ["4", 599711], ["2", 262994], ["7", 179961], ["1.1", 143953]] |
| HEALTH__FED_CMS_MEDICARE_PROVIDER | RNDRNG_PRVDR_CNTRY | country | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_MEDICARE_PROVIDER | RNDRNG_PRVDR_RUCA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 1099283], ["4", 79536], ["2", 36227], ["7", 29064], ["1.1", 17316]] |
| HEALTH__FED_CMS_NPPES | PROVIDER_BUSINESS_MAILING_ADDRESS_FAX_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["8885882752", 14950], ["8665002186", 12070], ["9732907495", 8884], ["845343447 |
| HEALTH__FED_CMS_NPPES | PROVIDER_BUSINESS_MAILING_ADDRESS_TELEPHONE_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["2484364400", 28498], ["3108560800", 21428], ["8182416780", 14837], ["20652057 |
| HEALTH__FED_CMS_NPPES | PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_FAX_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["8885882752", 16237], ["8453434477", 3391], ["3176149655", 3391], ["8314280101 |
| HEALTH__FED_CMS_NPPES | PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_TELEPHONE_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["2065205000", 17398], ["8335992560", 17241], ["8182416780", 17226], ["31085608 |
| HEALTH__FED_CMS_NPPES | PROVIDER_BUSINESS_MAILING_ADDRESS_COUNTRY_CODE_IF_OUTSIDE_U_S | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["US", 9254031], ["CA", 2031], ["UM", 1318], ["DE", 575], ["JP", 269]] |
| HEALTH__FED_CMS_NPPES | PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_COUNTRY_CODE_IF_OUTSIDE_U_S | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["US", 9254646], ["MX", 1283], ["UM", 912], ["CA", 799], ["DE", 735]] |
| HEALTH__FED_CMS_NURSING_HOME | COUNTY_FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT | COUNTRY_NAME | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 1696590], ["CANADA", 105], ["UNITED STATES MINOR OUTLYING ISL |
| HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT | PROVINCE_NAME | state | mixed / not a state | only 9% are 2-letter US codes (foreign provinces, money, or free text); only 0.0% of rows filled | [["AE", 52], ["ONTARIO", 47], ["PUERTO RICO", 25], ["AP", 24], ["ON", 23]] |
| HEALTH__FED_CMS_PART_D_PRESCRIBERS | PRSCRBR_CNTRY | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["US", 1416728], ["CA", 43], ["DE", 24], ["JP", 19], ["AE", 6]] |
| HEALTH__FED_CMS_PART_D_PRESCRIBERS | PRSCRBR_RUCA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 1203443], ["4", 83295], ["2", 38293], ["7", 33782], ["1.1", 19002]] |
| HEALTH__FED_CMS_POS_OTHER | SSA_CNTY_CD | county | mixed county |  | [["200", 1247], ["0", 968], ["90", 959], ["10", 918], ["120", 885]] |
| HEALTH__FED_CMS_POS_OTHER | FIPS_CNTY_CD | fips | FIPS with leading zeros lost | 59% have a FIPS length; modal length 2 -- pad before joining | [["37", 1132], ["31", 1085], ["1", 1014], ["3", 950], ["19", 907]] |
| HEALTH__FED_CMS_POS_OTHER | CBSA_CD | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["99945", 1484], ["99918", 1167], ["99926", 1000], ["99925", 966], ["35614", 78 |
| HEALTH__FED_CMS_POS_OTHER | SSA_STATE_CD | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["45", 3852], ["05", 3622], ["10", 2052], ["14", 1702], ["19", 1549]] |
| HEALTH__FED_CMS_POS_OTHER | STATE_RGN_CD | state | mixed / not a state | only 3% are 2-letter US codes (foreign provinces, money, or free text) | [["001", 25773], ["TX6", 990], ["AZ", 625], ["GAA", 576], ["2C3", 532]] |
| HEALTH__FED_DEA_ARCOS | BUYER_ZIP | zip | mixed / not a ZIP | only 94% look like ZIPs | [["28601", 329959], ["22801", 327853], ["44109", 327712], ["99508", 167369], ["2 |
| HEALTH__FED_DEA_ARCOS | REPORTER_ZIP | zip | mixed / not a ZIP | only 93% look like ZIPs | [["72756", 9888488], ["43551", 6104297], ["95776", 5030048], ["33478", 4731920], |
| HEALTH__FED_FDA_DEVICE_510K | POSTAL_CODE | zip | mixed / not a ZIP | only 90% look like ZIPs | [["60050", 20189], ["49534", 3585], ["92121", 1354], ["46581", 1303], ["92618",  |
| HEALTH__FED_FDA_DEVICE_510K | ZIP_CODE | zip | mixed / not a ZIP | only 90% look like ZIPs | [["60050", 20189], ["49534", 3585], ["92121", 1354], ["46581", 1303], ["92618",  |
| HEALTH__FED_FDA_DEVICE_PMA | ZIP_EXT | zip | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_FDA_ESTABLISHMENT_REG | POSTAL_CODE | zip | mixed / not a ZIP | only 31% look like ZIPs | [["51310", 4326], ["--", 3186], ["78532", 1817], ["500032", 1734], ["200131", 10 |
| HEALTH__FED_FDA_MAUDE | MANUFACTURER_CITY | city | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_FDA_MAUDE | MANUFACTURER_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_FDA_MAUDE | MANUFACTURER_STATE | state | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_HRSA_HPSA_PRIMARY_CARE | HPSA_GEOGRAPHY_ID | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["POINT", 7874], ["32003005614", 528], ["48147", 266], ["32031002207", 266], [" |
| HEALTH__FED_HRSA_HPSA_PRIMARY_CARE | COUNTY_FIPS_CODE | fips | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining | [["003", 3054], ["031", 2801], ["037", 2697], ["047", 2631], ["013", 2383]] |
| HEALTH__FED_HRSA_NPDB | HOME_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_HRSA_NPDB | WORK_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| HEALTH__FED_HRSA_SHORTAGE_AREAS | HPSA_GEOGRAPHY_IDENTIFICATION_NUMBER | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["POINT", 22708], ["13197", 725], ["12071001401", 724], ["12071080300", 724], [ |
| HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES | CONGRESSIONAL_DISTRICT_NUMBER | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["02", 2576], ["01", 2359], ["03", 1402], ["04", 1363], ["05", 1162]] |
| HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES | FQHC_SITE_MEDICARE_BILLING_NUMBER | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["181817", 63], ["391187", 63], ["111039", 63], ["191041", 63], ["671882", 63]] |
| HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES | FQHC_SITE_NPI_NUMBER | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1134172489", 45], ["1023463510", 45], ["1750903696", 45], ["1972792489", 45], |
| HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES | LOCATION_SETTING_ID | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["7", 13629], ["2", 4755], ["0", 505], ["1", 102], ["4", 24]] |
| HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES | LOCATION_TYPE_ID | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 15235], ["2", 2418], ["5", 1385]] |
| HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES | SITE_ADDED_TO_SCOPE_DATE | facility_site | not a place (dates) | name-scan false hit | [["2021-09-15", 199], ["2009-06-29", 182], ["1998-07-01", 141], ["2016-09-16", 1 |
| HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES | SITE_TYPE_ID | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["2", 16312], ["3", 1484], ["1", 1242]] |
| HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES | STATE_FIPS_CONGRESSIONAL_DISTRICT_CODE | fips | FIPS with leading zeros lost | 0% have a FIPS length; modal length 4 -- pad before joining | [["5401", 346], ["0200", 229], ["2105", 224], ["5402", 196], ["3711", 189]] |
| HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES | HHS_REGION_CODE | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["04", 3886], ["09", 3590], ["05", 2574], ["06", 2136], ["03", 1527]] |
| HEALTH__FED_NLM_DAILYMED_SPL_SETID_MAP | ZIP_FILE_NAME | zip | foreign postal code | only 0% look like US ZIPs | [["20131223_963792A9-4029-4E7B-9759-9AD52E1B0962.ZIP", 603], ["20251109_9D558F96 |
| HEALTH__FED_NURSINGHOME411 | CMS_REGION_NUMBER | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["5", 3184], ["4", 2655], ["6", 2015], ["9", 1412], ["7", 1355]] |
| HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION | STATE | state | mixed / not a state | only 94% are 2-letter US codes (foreign provinces, money, or free text) | [["WY", 39], ["WI", 39], ["WA", 39], ["VT", 39], ["VA", 39]] |
| HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN | SLA1PORT | airport_port | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["31312", 1642], ["21302", 849], ["20699", 649], ["31323", 557], ["42001", 407] |
| HISTORY__FED_DENSHO_DDR | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC | SLA1PORT | airport_port | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["34299", 2193], ["50299", 1894], ["50422", 1873], ["35114", 1631], ["35199", 1 |
| HISTORY__FED_WPA_SLAVE_NARRATIVES | STATE_FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| HOUSING__FED_CFPB_HMDA | CENSUS_TRACT | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["11001001500", 395], ["11001008802", 382], ["11001002101", 348], ["11001009400 |
| HOUSING__FED_CFPB_HMDA | TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.0000", 11136], ["71.0000", 1037], ["62.0000", 812], ["76.0000", 728], ["67. |
| HOUSING__FED_CFPB_HMDA | TRACT_MINORITY_POPULATION_PERCENT | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.0000", 470], ["75.2100", 424], ["25.2400", 395], ["71.3800", 382], ["84.440 |
| HOUSING__FED_CFPB_HMDA | TRACT_ONE_TO_FOUR_FAMILY_HOMES | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.0000", 745], ["1637.0000", 605], ["2098.0000", 395], ["1513.0000", 381], [" |
| HOUSING__FED_CFPB_HMDA | TRACT_OWNER_OCCUPIED_UNITS | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0.0000", 483], ["999.0000", 424], ["876.0000", 396], ["1911.0000", 395], ["91 |
| HOUSING__FED_CFPB_HMDA | TRACT_POPULATION | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["5099.0000", 560], ["4676.0000", 493], ["0.0000", 470], ["3927.0000", 405], [" |
| HOUSING__FED_CFPB_HMDA | TRACT_TO_MSA_INCOME_PERCENTAGE | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["198.0600", 3246], ["0.0000", 742], ["67.5200", 381], ["75.3300", 348], ["119. |
| HOUSING__FED_CFPB_HMDA | COUNTY_CODE | county | constant | one value for the whole table | [["11001", 27836]] |
| HOUSING__FED_CFPB_HMDA | DERIVED_MSA_MD | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["47894", 27841], ["99999", 460]] |
| HOUSING__FED_CFPB_HMDA | FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["139700.0000", 27841], ["0.0000", 460]] |
| HOUSING__FED_CFPB_HMDA | STATE_CODE | state | constant | one value for the whole table | [["DC", 28301]] |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | CENSUS_TRACT | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["11001001500", 395], ["11001008802", 382], ["11001002101", 348], ["11001009400 |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 11136], ["71", 1037], ["62", 812], ["76", 728], ["67", 706]] |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | TRACT_MINORITY_POPULATION_PERCENT | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 470], ["75.21", 424], ["25.24", 395], ["71.38", 382], ["84.44", 348]] |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | TRACT_ONE_TO_FOUR_FAMILY_HOMES | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 745], ["1637", 605], ["2098", 395], ["1513", 381], ["1339", 348]] |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | TRACT_OWNER_OCCUPIED_UNITS | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 483], ["999", 424], ["876", 396], ["1911", 395], ["911", 383]] |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | TRACT_POPULATION | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["5099", 560], ["4676", 493], ["0", 470], ["3927", 405], ["6156", 395]] |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | TRACT_TO_MSA_INCOME_PERCENTAGE | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["198.06", 3246], ["0", 742], ["67.52", 381], ["75.33", 348], ["119.08", 312]] |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | COUNTY_CODE | county | constant | one value for the whole table | [["11001", 27836]] |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | DERIVED_MSA_MD | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["47894", 27841], ["99999", 460]] |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["139700", 27841], ["0", 460]] |
| HOUSING__FED_CFPB_HMDA_DC_ONLY | STATE_CODE | state | constant | one value for the whole table | [["DC", 28301]] |
| HOUSING__FED_CFPB_HMDA_HISTORIC | CENSUS_TRACT_NUMBER | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0203.02", 53299], ["9708.00", 52906], ["0019.00", 52906], ["0105.00", 52860], |
| HOUSING__FED_CFPB_HMDA_HISTORIC | TRACT_TO_MSAMD_INCOME | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["105", 250943], ["100", 247052], ["101", 245996], ["111", 245607], ["107", 244 |
| HOUSING__FED_CFPB_HMDA_HISTORIC | COUNTY_CODE | county | mixed county |  | [["13", 703705], ["37", 688642], ["3", 622148], ["31", 622107], ["59", 498897]] |
| HOUSING__FED_CFPB_HMDA_HISTORIC | STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["6", 2569481], ["48", 1431680], ["12", 1159909], ["17", 748590], ["39", 645307 |
| HOUSING__FED_CFPB_HMDA_LAR | CENSUS_TRACT | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["11001001600", 238], ["11001008802", 235], ["11001003200", 224], ["11001002101 |
| HOUSING__FED_CFPB_HMDA_LAR | TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 6602], ["71", 655], ["70", 526], ["67", 490], ["76", 473]] |
| HOUSING__FED_CFPB_HMDA_LAR | TRACT_MINORITY_POPULATION_PERCENT | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["75.2100", 241], ["71.4200", 238], ["71.3800", 235], ["97.9100", 227], ["69.09 |
| HOUSING__FED_CFPB_HMDA_LAR | TRACT_ONE_TO_FOUR_FAMILY_HOMES | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1637", 430], ["0", 294], ["1265", 242], ["1513", 235], ["1517", 224]] |
| HOUSING__FED_CFPB_HMDA_LAR | TRACT_OWNER_OCCUPIED_UNITS | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["876", 250], ["911", 238], ["999", 238], ["1415", 238], ["666", 235]] |
| HOUSING__FED_CFPB_HMDA_LAR | TRACT_POPULATION | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["5099", 419], ["4676", 278], ["3927", 244], ["4471", 238], ["4360", 235]] |
| HOUSING__FED_CFPB_HMDA_LAR | TRACT_TO_MSA_INCOME_PERCENTAGE | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["198.0600", 1921], ["0.0000", 328], ["158.0200", 238], ["67.5200", 235], ["85. |
| HOUSING__FED_CFPB_HMDA_LAR | COUNTY_CODE | county | constant | one value for the whole table | [["11001", 17349]] |
| HOUSING__FED_CFPB_HMDA_LAR | DERIVED_MSA_MD | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["47894", 17349], ["99999", 125]] |
| HOUSING__FED_CFPB_HMDA_LAR | FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["150100", 17349], ["0", 125]] |
| HOUSING__FED_CFPB_HMDA_LAR | STATE_CODE | state | constant | one value for the whole table | [["DC", 17474]] |
| HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | CENSUS_GEOID | fips | mixed / not FIPS | only 0% have a FIPS length; modal length 12 | [["NO_INTERSECT", 169368], ["220790105003", 45343], ["481576730021", 21808], ["4 |
| HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS | PLACE | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["99999", 1936], ["51000", 1077], ["14000", 635], ["60000", 491], ["07000", 465 |
| HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS | CBSA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["99999", 4020], ["35620", 1881], ["14460", 907], ["16980", 899], ["31080", 737 |
| HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS | STD_ZIP5 | zip | mixed / not a ZIP | only 86% look like ZIPs | [["26003", 285], ["25701", 273], ["54880", 272], ["25387", 268], ["25301", 267]] |
| HOUSING__FED_HUD_DATA | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| HOUSING__FED_HUD_DATA | ZIP | zip | empty | no real values (blank or sentinel only) | [] |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | CENSUS_TRACT | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["950200", 63], ["950300", 59], ["950100", 53], ["950400", 44], ["061102", 44]] |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | TRACT_LEVEL_KEY | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["36091061102", 44], ["55139001400", 29], ["55111000401", 29], ["56019955202",  |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | PLACE_CLASS_CODE | facility_site | empty | no real values (blank or sentinel only) | [] |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | PLACE_INCORPORATED_FLAG | facility_site | empty | no real values (blank or sentinel only) | [] |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | PLACE_LEVEL_KEY | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["3665255", 44], ["2599999", 38], ["3499999", 33], ["4499999", 31], ["5499999", |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | COUNTY_FIPS | fips | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining | [["017", 92], ["003", 87], ["009", 80], ["013", 76], ["001", 76]] |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | CURRENT_COUNTY_FIPS | fips | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining | [["017", 92], ["013", 74], ["003", 69], ["001", 69], ["009", 68]] |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | CBSA_CODE | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["99999", 961], ["35620", 127], ["14460", 95], ["41980", 49], ["12060", 49]] |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | METRO_FLAG | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 2046], ["0", 1738]] |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | MSA_CODE | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["9999", 2196], ["1120", 63], ["2160", 38], ["0520", 35], ["6480", 29]] |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | ZIP_CLASS | zip | foreign postal code | only 0% look like US ZIPs; only 1.2% of rows filled | [["P", 46], ["U", 1]] |
| HOUSING__FED_MAPPING_INEQUALITY | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| IMMIGRATION__FED_DHS_OHSS | REGION_OR_SECTOR | region | empty | no real values (blank or sentinel only) | [] |
| IMMIGRATION__FED_DHS_YEARBOOK | COUNTRY_OF_BIRTH | country | empty | no real values (blank or sentinel only) | [] |
| IMMIGRATION__FED_DHS_YEARBOOK | COUNTRY_OF_LAST_RESIDENCE | country | empty | no real values (blank or sentinel only) | [] |
| IMMIGRATION__FED_DHS_YEARBOOK | STATE | state | empty | no real values (blank or sentinel only) | [] |
| IMMIGRATION__FED_DOL_OFLC | EMPLOYER_COUNTRY | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES OF AMERICA", 636433], ["CANADA", 27], ["INDIA", 3], ["AUSTRALIA |
| IMMIGRATION__FED_DOL_OFLC | AGENT_ATTORNEY_PROVINCE | state | mixed / not a state | only 5% are 2-letter US codes (foreign provinces, money, or free text); only 4.0% of rows filled | [["ONTARIO", 16904], ["NEW YORK", 2960], ["ON", 2688], ["PA", 328], ["SANTA CLAR |
| IMMIGRATION__FED_DOL_OFLC | EMPLOYER_PROVINCE | state | mixed / not a state | only 21% are 2-letter US codes (foreign provinces, money, or free text); only 0.8% of rows filled | [["MIDDLESEX", 974], ["COOK", 480], ["NEW JERSEY", 266], ["USA", 180], ["VA", 14 |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_STATE_1 | state | mixed / not a state | only 13% are 2-letter US codes (foreign provinces, money, or free text) | [["CALIFORNIA", 115467], ["TEXAS", 58399], ["NEW YORK", 50196], ["NEW JERSEY", 3 |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_STATE_2 | state | mixed / not a state | only 11% are 2-letter US codes (foreign provinces, money, or free text) | [["CALIFORNIA", 8889], ["TEXAS", 5158], ["NEW JERSEY", 4246], ["ILLINOIS", 3099] |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_STATE_3 | state | mixed / not a state | only 14% are 2-letter US codes (foreign provinces, money, or free text); only 2.1% of rows filled | [["CALIFORNIA", 1787], ["TEXAS", 1026], ["NEW JERSEY", 892], ["NEW YORK", 871],  |
| IMMIGRATION__FED_DOL_OFLC | AGENT_ATTORNEY_POSTAL_CODE | zip | mixed / not a ZIP | only 83% look like ZIPs | [["2110", 16509], ["10004", 15357], ["75082", 13460], ["60606", 10767], ["95054" |
| IMMIGRATION__FED_DOL_OFLC | EMPLOYER_POSTAL_CODE | zip | mixed / not a ZIP | only 85% look like ZIPs | [["77845", 30012], ["75082", 21252], ["20850", 13105], ["94043", 12742], ["19103 |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_1 | zip | mixed / not a ZIP | only 89% look like ZIPs | [["94043", 8665], ["94105", 7462], ["98052", 7263], ["95054", 5821], ["94085", 5 |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_2 | zip | mixed / not a ZIP | only 87% look like ZIPs | [["94105", 1241], ["98052", 676], ["95131", 608], ["64138", 487], ["32746", 485] |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_3 | zip | mixed / not a ZIP | only 87% look like ZIPs; only 2.1% of rows filled | [["95138", 202], ["32746", 179], ["97124", 162], ["94105", 151], ["60018", 121]] |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_4 | zip | mixed / not a ZIP | only 88% look like ZIPs; only 0.6% of rows filled | [["94403", 77], ["97007", 71], ["32746", 53], ["15213", 38], ["94105", 33]] |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_5 | zip | mixed / not a ZIP | only 91% look like ZIPs; only 0.3% of rows filled | [["10467", 29], ["10025", 19], ["92614", 18], ["77032", 17], ["29425", 16]] |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_6 | zip | mixed / not a ZIP | only 92% look like ZIPs; only 0.2% of rows filled | [["10461", 26], ["17011", 21], ["90045", 16], ["15240", 13], ["15237", 12]] |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_7 | zip | mixed / not a ZIP | only 93% look like ZIPs; only 0.1% of rows filled | [["10065", 22], ["85034", 16], ["77072", 14], ["18411", 13], ["43215", 11]] |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_8 | zip | mixed / not a ZIP | only 91% look like ZIPs; only 0.1% of rows filled | [["18503", 21], ["10462", 21], ["97218", 16], ["2110", 11], ["18235", 9]] |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_9 | zip | mixed / not a ZIP | only 95% look like ZIPs; only 0.1% of rows filled | [["10457", 21], ["18711", 15], ["84790", 12], ["18071", 9], ["44111", 7]] |
| IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES | ZIP | zip | mixed / not a ZIP | only 94% look like ZIPs | [["79772", 12], ["78839", 11], ["85365", 11], ["95901", 11], ["85364", 11]] |
| IMMIGRATION__FED_USCIS_DATA | COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| JUSTICE__FED_ATF_FFL | LIC_DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["59", 4546], ["75", 3860], ["56", 3085], ["74", 2855], ["86", 2607]] |
| JUSTICE__FED_ATF_FFL | LIC_COUNTY | county | mixed county |  | [["13", 2422], ["3", 1811], ["29", 1527], ["5", 1500], ["1", 1488]] |
| JUSTICE__FED_ATF_FFL | LIC_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["5", 21986], ["1", 18214], ["9", 12724], ["4", 9401], ["3", 5918]] |
| JUSTICE__FED_BOP_STATISTICS | STATE_FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| JUSTICE__FED_COURTLISTENER_COURTHOUSES | ADDRESS2 | address | empty | no real values (blank or sentinel only) | [] |
| JUSTICE__FED_COURTLISTENER_COURTHOUSES | COUNTRY_CODE | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["US", 3360], ["GB", 1]] |
| JUSTICE__FED_COURTLISTENER_COURTHOUSES | COUNTY | county | constant | one value for the whole table | [["POLK", 1]] |
| JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED | COUNTY_OF_RESIDENCE | county | mixed county |  | [["88888", 1941207], ["6037", 263829], ["17031", 193938], ["36061", 146156], ["3 |
| JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED | JURISDICTION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["3", 4803765], ["4", 2784687], ["2", 1237814], ["1", 550375], ["5", 5632]] |
| JUSTICE__FED_COURTLISTENER_JUDGES | DOB_COUNTRY | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 16002], ["UNITED KINGDOM", 16], ["CANADA", 15], ["MEXICO", 14 |
| JUSTICE__FED_COURTLISTENER_JUDGES | DOD_COUNTRY | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 16183], ["VIETNAM", 1]] |
| JUSTICE__FED_DOJ_FCA_SETTLEMENTS | DISTRICT | cong_district | empty | no real values (blank or sentinel only) | [] |
| JUSTICE__FED_FBI_NICS_CHECKS | LONG_GUN | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 686], ["1", 134], ["2", 118], ["35", 118], ["443", 118]] |
| JUSTICE__FED_FBI_NICS_CHECKS | PRIVATE_SALE_LONG_GUN | coordinates | coordinate with 0,0 trap | 44% are exactly 0 (Gulf of Guinea rows) | [["0", 2951], ["5", 180], ["2", 174], ["4", 172], ["6", 167]] |
| JUSTICE__FED_FBI_NICS_CHECKS | REDEMPTION_LONG_GUN | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["0", 4339], ["1", 175], ["2", 145], ["4", 99], ["3", 89]] |
| JUSTICE__FED_FJC_IDB_APPELLATE | DISTRICT_CIRCUIT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["-8", 224643], ["9", 136046], ["5", 113025], ["11", 93072], ["4", 72777]] |
| JUSTICE__FED_FJC_IDB_APPELLATE | DISTRICT_COURT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["-8", 224643], ["73", 36509], ["08", 31990], ["41", 28632], ["3A", 25708]] |
| JUSTICE__FED_FJC_IDB_APPELLATE | DISTRICT_DEFENDANT_NUMBER | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["-8", 784833], ["1", 155171], ["2", 18472], ["3", 8498], ["4", 4705]] |
| JUSTICE__FED_FJC_IDB_APPELLATE | DISTRICT_DOCKET | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["-8", 224996], ["9608414", 2404], ["1900461", 1832], ["1800131", 1832], ["1900 |
| JUSTICE__FED_FJC_IDB_APPELLATE | DISTRICT_DOCKET_DATE | cong_district | not a place (dates) | name-scan false hit | [["1996-11-08", 2390], ["2019-08-19", 2288], ["2019-09-09", 2288], ["2019-12-03" |
| JUSTICE__FED_FJC_IDB_APPELLATE | DISTRICT_JUDGE | cong_district | empty | no real values (blank or sentinel only) | [] |
| JUSTICE__FED_FJC_IDB_APPELLATE | DISTRICT_OFFICE | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["-8", 224634], ["1", 217671], ["2", 182893], ["3", 132950], ["4", 81728]] |
| JUSTICE__FED_FJC_IDB_APPELLATE | JURISDICTION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["-9", 462824], ["3", 340424], ["2", 124189], ["4", 54963], ["1", 5770]] |
| JUSTICE__FED_FJC_IDB_CIVIL | DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["13", 550011], ["73", 523496], ["29", 469140], ["08", 423598], ["12", 387188]] |
| JUSTICE__FED_FJC_IDB_CIVIL | JURISDICTION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["3", 5485725], ["4", 3332841], ["2", 1467611], ["1", 565532], ["5", 5686]] |
| JUSTICE__FED_FJC_IDB_CRIMINAL | DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["41", 433623], ["42", 395692], ["70", 282993], ["74", 274694], ["08", 267225]] |
| JUSTICE__FED_FJC_IDB_CRIMINAL | TRANSFER_DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["-8", 6266057], ["23", 5238], ["08", 3402], ["73", 3036], ["45", 2178]] |
| JUSTICE__FED_SCDB | JURISDICTION_CODE | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 68125], ["2", 13358], ["9", 1498], ["6", 188], ["8", 170]] |
| JUSTICE__FED_SCDB | ADMIN_ACTION_STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["37", 582], ["6", 582], ["17", 320], ["41", 315], ["45", 234]] |
| JUSTICE__FED_SCDB | CASE_ORIGIN_STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["6", 2295], ["37", 2080], ["17", 1243], ["12", 1194], ["51", 924]] |
| JUSTICE__FED_SCDB | CASE_SOURCE_STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["6", 2044], ["37", 1567], ["12", 1122], ["17", 1036], ["51", 861]] |
| JUSTICE__FED_SCDB | PETITIONER_STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["6", 1977], ["37", 1119], ["60", 877], ["51", 863], ["17", 813]] |
| JUSTICE__FED_SCDB | RESPONDENT_STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["6", 2203], ["37", 1697], ["51", 1448], ["12", 1185], ["17", 1124]] |
| JUSTICE__FED_USCOURTS_STATS | DISTRICT | cong_district | empty | no real values (blank or sentinel only) | [] |
| JUSTICE__FED_USCOURTS_STATS | COUNTY | county | empty | no real values (blank or sentinel only) | [] |
| JUSTICE__FED_USCOURTS_STATS | FIPS_CODE | fips | empty | no real values (blank or sentinel only) | [] |
| JUSTICE__INTL_AUSTLII | JURISDICTION | region | constant | one value for the whole table | [["AU", 1]] |
| JUSTICE__INTL_EURLEX_CELLAR | COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| JUSTICE__INTL_EU_SANCTIONS | ADDR_LEBA_PUBLICATION_DATE | address | not a place (dates) | name-scan false hit | [["2025-09-29", 198], ["2024-02-23", 100], ["2025-05-20", 96], ["2026-04-23", 95 |
| JUSTICE__INTL_EU_SANCTIONS | ADDR_LOGICAL_ID | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["182605", 18], ["182589", 18], ["182581", 18], ["182537", 18], ["182536", 18]] |
| JUSTICE__INTL_EU_SANCTIONS | ADDR_NUMBER | address | empty | no real values (blank or sentinel only) | [] |
| JUSTICE__INTL_EU_SANCTIONS | ADDR_ZIPCODE | zip | mixed / not a ZIP | only 9% look like ZIPs; only 1.7% of rows filled | [["115184", 8], ["121357", 7], ["119160", 7], ["392000", 6], ["603950", 6]] |
| JUSTICE__INTL_EU_SOCTA_EUROPOL | GEOGRAPHIC_SCOPE | facility_site | constant | one value for the whole table | [["EUROPEAN UNION", 26]] |
| JUSTICE__INTL_UCDP_GED | WHERE_COORDINATES | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["ALEPPO TOWN", 4562], ["DAMASCUS CITY", 3658], ["TIJUANA TOWN", 3300], ["MOGAD |
| JUSTICE__XC_MAPPING_POLICE_VIOLENCE | CENSUS_TRACT_CODE | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["030301", 105], ["000302", 105], ["008704", 105], ["001000", 105], ["011301",  |
| JUSTICE__XC_MAPPING_POLICE_VIOLENCE | MEDIAN_HOUSEHOLD_INCOME_ACS_CENSUS_TRACT | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["96313", 98], ["60250", 97], ["43947", 97], ["26429", 97], ["36620", 97]] |
| JUSTICE__XC_MAPPING_POLICE_VIOLENCE | TOTAL_POPULATION_OF_CENSUS_TRACT_2019_ACS_5_YEAR_ESTIMATES | census_tract | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1235", 105], ["1637", 105], ["1319", 105], ["1178", 105], ["1074", 105]] |
| JUSTICE__XC_MAPPING_POLICE_VIOLENCE | GEOGRAPHY_VIA_TRULIA_METHODOLOGY_BASED_ON_ZIPCODE_POPULATION_DENSITY_HTTP_JEDKOLKO_COM_WP_CONTENT_UPLOADS_2015_05_FULL_ZCTA_URBAN_SUBURBAN_RURAL_CLASSIFICATION_XLSX | zip | foreign postal code | only 0% look like US ZIPs | [["SUBURBAN", 7245], ["URBAN", 3875], ["RURAL", 3440]] |
| JUSTICE__XC_UK_SANCTIONS_LIST | ADDRESS_POSTAL_CODE | zip | mixed / not a ZIP | only 15% look like ZIPs | [["103265", 423], ["103426", 155], ["283001", 139], ["19574", 90], ["119019", 65 |
| JUSTICE__XC_VERA_INCARCERATION_TRENDS | METRO_AREA | metro | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["12060", 1675], ["35620", 1095], ["47900", 913], ["17140", 732], ["33460", 731 |
| JUSTICE__XC_VERA_INCARCERATION_TRENDS | COMMUTING_ZONE | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["141", 969], ["39", 832], ["14", 679], ["87", 669], ["58", 632]] |
| JUSTICE__XC_VERA_INCARCERATION_TRENDS | IS_UNIFIED_STATE | state | constant | one value for the whole table | [["FALSE", 128507]] |
| LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB | SB_ACTUARY_FOREIGN_ADDRESS1 | address | constant | one value for the whole table | [["4 ORINDA WAY", 1]] |
| LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB | SB_ACTUARY_FOREIGN_ADDRESS2 | address | constant | one value for the whole table | [["SUITE 100B", 1]] |
| LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB | SB_PORT_PREFNDNG_FNDNG_CAR_AMT | airport_port | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 2.2% of rows filled | [["0", 36001], ["1", 9], ["1034", 7], ["96", 7], ["1218415", 5]] |
| LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB | SB_ACTUARY_FOREIGN_CITY | city | constant | one value for the whole table | [["ORINDA", 1]] |
| LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB | SB_ACTUARY_FOREIGN_CNTRY | country | constant | one value for the whole table | [["US", 1]] |
| LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB | SB_ACTUARY_FOREIGN_PROV_STATE | state | constant | one value for the whole table | [["CA", 1]] |
| LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB | SB_ACTUARY_FOREIGN_POSTAL_CD | zip | constant | one value for the whole table | [["94563", 1]] |
| LABOR__FED_DOL_OLMS | ADDRESS_ID | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["230457", 773], ["653539", 772], ["12649", 772], ["207861", 772], ["532834", 7 |
| LABOR__FED_DOL_OLMS | ADDRESS_TYPE | address | constant | one value for the whole table | [["201", 617552]] |
| LABOR__FED_MSHA_MINES | FIPS_CNTY_CD | fips | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining | [["195", 3982], ["027", 3144], ["013", 2688], ["005", 2161], ["071", 2000]] |
| LABOR__FED_MSHA_MINES | FIPS_CNTY_NM | fips | mixed / not FIPS | only 0% have a FIPS length; modal length 7 | [["PIKE", 3030], ["BUCHANAN", 2089], ["WISE", 1524], ["LETCHER", 1371], ["MCDOWE |
| LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 | ZIP_CODE | zip | mixed / not a ZIP | only 93% look like ZIPs | [["89106", 1184], ["80214", 1184], ["65807", 1184], ["21801", 1183], ["45215", 1 |
| LABOR__FED_OSHA_ITA_CASE_DETAIL_2024 | ZIP_CODE | zip | mixed / not a ZIP | only 92% look like ZIPs | [["32830", 3295], ["94538", 3150], ["83440", 2222], ["26003", 2220], ["97355", 2 |
| LABOR__FED_OSHA_ITA_CASE_DETAIL_2025 | ZIP_CODE | zip | mixed / not a ZIP | only 92% look like ZIPs | [["92802", 3788], ["92123", 2987], ["19104", 2926], ["80249", 2559], ["60638", 2 |
| LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS | LOCATION_SETTLEMENT_FILED | facility_site | empty | no real values (blank or sentinel only) | [] |
| LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS | OTHER_SINGLE_STATE_SETTLEMENTS | state | empty | no real values (blank or sentinel only) | [] |
| LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS | STATE_COSTS_FEES | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text); only 2.2% of rows filled | [["$0", 10], ["$59,500,000", 1], ["$1,497,500", 1], ["$1,337,500", 1], ["$30,000 |
| OPEN_DATA__INTL_BR_DADOS_GOV | GEOGRAPHIC_COVERAGE | facility_site | empty | no real values (blank or sentinel only) | [] |
| OPEN_DATA__INTL_CH_OPENDATASWISS | STATE | state | constant | one value for the whole table | [["ACTIVE", 5000]] |
| OPEN_DATA__INTL_CL_DATOSGOB | STATE | state | constant | one value for the whole table | [["ACTIVE", 1000]] |
| OPEN_DATA__INTL_GE_DATAGOV | COUNTRY | country | constant | one value for the whole table | [["GEORGIA", 1]] |
| POLITICS__FEC_CANDIDATE | OFFICE_DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["00", 6122], ["01", 1269], ["02", 1124], ["03", 1017], ["04", 808]] |
| POLITICS__FEC_CANDIDATE | OFFICE_STATE | state | mixed / not a state | only 80% are 2-letter US codes (foreign provinces, money, or free text) | [["US", 3630], ["CA", 1392], ["TX", 1145], ["FL", 1072], ["NY", 763]] |
| POLITICS__FED_CONGRESS_LEGISLATORS | DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 1043], ["2", 1014], ["3", 926], ["4", 791], ["5", 723]] |
| POLITICS__FED_EAC_EAVS | FIPSCODE | fips | mixed / not FIPS | only 29% have a FIPS length; modal length 10 | [["5604500000", 48], ["5604300000", 48], ["5604100000", 48], ["5603900000", 48], |
| POLITICS__FED_FCC_LICENSING | FCC_COUNTY_CODE | county | empty | no real values (blank or sentinel only) | [] |
| POLITICS__FED_FEC_API | DISTRICT | cong_district | empty | no real values (blank or sentinel only) | [] |
| POLITICS__FED_FEC_API | STATE | state | empty | no real values (blank or sentinel only) | [] |
| POLITICS__FED_MEDSL_HOUSE_RETURNS | DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["2", 2989], ["1", 2936], ["3", 2481], ["4", 2285], ["5", 2106]] |
| POLITICS__FED_MEDSL_HOUSE_RETURNS | STATE_FIPS | fips | FIPS with leading zeros lost | 82% have a FIPS length; modal length 2 -- pad before joining | [["36", 3605], ["6", 3133], ["48", 1798], ["26", 1483], ["34", 1186]] |
| POLITICS__FED_MEDSL_PRESIDENT_RETURNS | STATE_FIPS | fips | FIPS with leading zeros lost | 85% have a FIPS length; modal length 2 -- pad before joining | [["8", 126], ["36", 121], ["27", 118], ["19", 112], ["49", 100]] |
| POLITICS__FED_MEDSL_SENATE_RETURNS | STATE_FIPS | fips | FIPS with leading zeros lost | 85% have a FIPS length; modal length 2 -- pad before joining | [["36", 161], ["47", 144], ["34", 129], ["27", 120], ["50", 119]] |
| POLITICS__FED_VOTEVIEW_MEMBERS | DISTRICT_CODE | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 9509], ["1", 4292], ["2", 3726], ["3", 3271], ["4", 2996]] |
| POLITICS__FED_VOTEVIEW_MEMBERS | STATE_ICPSR | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["13", 4384], ["14", 3444], ["24", 2430], ["71", 2400], ["21", 2199]] |
| POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS | CONTRIBUTOR_PROVINCE | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["ON", 5737161], ["BC", 2326701], ["AB", 1728966], ["QC", 887664], ["MB", 54897 |
| POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS | CONTRIBUTOR_POSTAL_CODE | zip | foreign postal code | only 0% look like US ZIPs | [["L0G1L0", 26915], ["H7V4A8", 25262], ["K7S3G7", 25123], ["K2A3X4", 23301], ["K |
| POLITICS__IRS527_8872_REPORTS | CHANGE_OF_ADDRESS_IND | address | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 1.5% of rows filled | [["0", 54733], ["1", 846]] |
| POLITICS__IRS527_8872_REPORTS | BUSINESS_ZIP_EXT | zip | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) | [["0031", 329], ["1964", 216], ["5687", 162], ["2110", 142], ["6508", 141]] |
| POLITICS__IRS527_8872_REPORTS | CONTACT_ZIP_EXT | zip | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) | [["0031", 332], ["1964", 219], ["5687", 163], ["2110", 145], ["6508", 142]] |
| POLITICS__IRS527_8872_REPORTS | CUSTODIAN_ZIP_EXT | zip | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) | [["0031", 332], ["1964", 218], ["5687", 163], ["2110", 145], ["6508", 144]] |
| POLITICS__IRS527_8872_REPORTS | MAILING_ZIP_EXT | zip | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) | [["0031", 330], ["1964", 216], ["5687", 162], ["6508", 142], ["2110", 142]] |
| POLITICS__IRS527_DIRECTORS_OFFICERS | ENTITY_ZIP_EXT | zip | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) | [["1724", 1381], ["2220", 500], ["9998", 249], ["1701", 235], ["2185", 231]] |
| POLITICS__IRS527_EAIN | STATE_ISSUED | state | mixed / not a state | only 94% are 2-letter US codes (foreign provinces, money, or free text) | [["CA", 6849], ["FL", 1666], ["FD", 1145], ["TX", 843], ["NY", 713]] |
| POLITICS__IRS527_RELATED_ENTITIES | ENTITY_ZIP_EXT | zip | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) | [["2220", 15628], ["0074", 329], ["0301", 114], ["1724", 88], ["8600", 69]] |
| POLITICS__MEMBER_CROSSWALK | LAST_DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 1043], ["2", 1014], ["3", 926], ["4", 791], ["5", 723]] |
| POLITICS__ST_CANNABIS_POLICY_BUNDLES | LEGISLATIVE_ACTION | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["0", 1267], ["1", 233]] |
| POLITICS__ST_CANNABIS_POLICY_BUNDLES | FIPS | fips | FIPS with leading zeros lost | 86% have a FIPS length; modal length 2 -- pad before joining | [["45", 31], ["56", 30], ["55", 30], ["54", 30], ["53", 30]] |
| POLITICS__ST_CANNABIS_POLICY_BUNDLES | STATE_COURT_SIG_ACTION | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining; only 2.9% of rows filled | [["0", 1457], ["1", 43]] |
| POLITICS__ST_CANNABIS_POLICY_BUNDLES | STATE_SALES_TAX_HIGH_RCL_APP | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["0", 1413], ["1", 87]] |
| POLITICS__ST_CANNABIS_POLICY_BUNDLES | STATE_SALES_TAX_HIGH_RCL_IMP | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining; only 4.0% of rows filled | [["0", 1440], ["1", 60]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION | EMPLOYER_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 3280], ["110", 1412], ["100", 1133], ["2", 1026], ["ONE", 860]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION | INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["123", 439], ["100", 349], ["5", 289], ["570", 238], ["1310", 204]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION | INTERMEDIARY_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 0.2% of rows filled | [["1168-70", 58], ["123", 41], ["605", 38], ["200", 33], ["375", 26]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION | STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["125", 212], ["80", 190], ["26", 173], ["225", 152], ["1", 151]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION | INTERMEDIARY_ZIP | zip | mixed / not a ZIP | only 94% look like ZIPs | [["10021", 960], ["11030", 481], ["11230", 367], ["10128", 357], ["10024", 332]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | EMPLOYER_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 2137], ["250", 804], ["100", 769], ["200", 718], ["2", 638]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 2.4% of rows filled | [["300", 112], ["620", 103], ["3152", 86], ["242-01", 76], ["1", 61]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | INTERMEDIARY_STREET_NAME | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | INTERMEDIARY_STREET_NUMBER | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | STREET_NAME | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | STREET_NUMBER | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION | EMPLOYER_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 3250], ["200", 1289], ["250", 1161], ["100", 1109], ["2", 988]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION | INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 397], ["200", 344], ["250", 290], ["55", 279], ["ONE", 254]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION | INTERMEDIARY_STREET_NAME | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION | INTERMEDIARY_STREET_NUMBER | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION | STREET_NAME | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION | STREET_NUMBER | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS | EMPLOYER_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 7966], ["100", 3382], ["250", 3187], ["200", 2949], ["55", 2746]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS | INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 1.0% of rows filled | [["FEB-39", 248], ["40", 238], ["3602", 110], ["720", 102], ["88", 96]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS | INTERMEDIARY_STREET_NAME | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS | INTERMEDIARY_STREET_NUMBER | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS | STREET_NAME | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS | STREET_NUMBER | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS | ZIP | zip | mixed / not a ZIP | only 95% look like ZIPs | [["11215", 14139], ["10025", 10057], ["11201", 8951], ["10024", 7762], ["11238", |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | EMPLOYER_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 4308], ["200", 1869], ["100", 1842], ["250", 1650], ["111", 1407]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 2.6% of rows filled | [["1412", 337], ["218", 278], ["1", 276], ["60", 231], ["220", 157]] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | INTERMEDIARY_STREET_NAME | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | INTERMEDIARY_STREET_NUMBER | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | STREET_NAME | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | STREET_NUMBER | address | empty | no real values (blank or sentinel only) | [] |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | ZIP | zip | mixed / not a ZIP | only 94% look like ZIPs | [["11215", 7862], ["10025", 5886], ["11238", 5006], ["11201", 4884], ["10024", 4 |
| POLITICS__WHO_WON | DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["STATEWIDE", 1420], ["1", 954], ["2", 954], ["3", 816], ["4", 742]] |
| PROCUREMENT__FED_SAM_EXCLUSIONS | ZIP | zip | mixed / not a ZIP | only 92% look like ZIPs | [["85746", 763], ["76127", 763], ["28146", 512], ["08640", 512], ["11235", 511]] |
| PROCUREMENT__FED_USASPENDING_BULK | RECIPIENT_COUNTRY_CODE | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["USA", 49265], ["CAN", 86], ["GBR", 21], ["BRA", 14], ["CHE", 13]] |
| PROCUREMENT__FED_USASPENDING_BULK | RECIPIENT_COUNTRY_NAME | country | country name (98%+ US) | almost no foreign rows -- weak as a join axis | [["UNITED STATES", 49265], ["CANADA", 86], ["UNITED KINGDOM", 21], ["BRAZIL", 14 |
| PROCUREMENT__FED_USASPENDING_BULK | STATE_CONTROLLED_INSTITUTION_OF_HIGHER_LEARNING | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["F", 49411], ["T", 202]] |
| PROCUREMENT__FED_USASPENDING_BULK | US_STATE_GOVERNMENT | state | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) | [["F", 49380], ["T", 233]] |
| PROCUREMENT__INTL_ADB_DATA | COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_DHS_HIFLD | ADDRESS | address | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_DHS_HIFLD | CITY | city | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_DHS_HIFLD | LATITUDE | coordinates | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_DHS_HIFLD | LONGITUDE | coordinates | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_DHS_HIFLD | COUNTY | county | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_DHS_HIFLD | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_DHS_HIFLD | STATE | state | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_DHS_HIFLD | ZIP | zip | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_USGS_TOPOVIEW | COUNTIES | county | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_USGS_TOPOVIEW | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__FED_USGS_TOPOVIEW | STATE | state | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__INTL_EG_CAPMAS | COUNTRY | country | constant | one value for the whole table | [["EGYPT", 52]] |
| REFERENCE__INTL_GDELT | ACTIONGEO_LAT | coordinates | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__INTL_GDELT | ACTIONGEO_LONG | coordinates | empty | no real values (blank or sentinel only) | [] |
| REFERENCE__INTL_GDELT | ACTOR1GEO_LAT | coordinates | coordinate, partly out of range | 89% parse in range | [["42", 90], ["10", 81], ["51", 78], ["40", 77], ["43", 75]] |
| REFERENCE__INTL_GDELT | ACTOR1GEO_LONG | coordinates | coordinate, partly out of range | 92% parse in range | [["42", 90], ["10", 81], ["51", 78], ["40", 77], ["43", 75]] |
| REF__DIM_GEOGRAPHY | COUNTY_FIPS_SUFFIX | fips | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining | [["005", 100], ["001", 99], ["003", 98], ["009", 97], ["007", 97]] |
| REF__DIM_GEOGRAPHY | FIPS_CODE | fips | mixed / not FIPS | only 54% have a FIPS length; modal length 5 | [["37000", 14], ["CA021", 14], ["MI135", 14], ["ND043", 14], ["NC041", 14]] |
| REF__DIM_GEOGRAPHY | STATE_FIPS | fips | mixed / not FIPS | only 56% have a FIPS length; modal length 2 | [["00", 325], ["48", 255], ["TX", 255], ["13", 160], ["GA", 153]] |
| REF__DIM_GEOGRAPHY | EPA_REGION | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["04", 1477], ["06", 1210], ["05", 1107], ["07", 886], ["08", 656]] |
| SCIENCE__FED_NSF_AWARDS | COUNTRY | country | constant | one value for the whole table | [["US", 115]] |
| SCIENCE__INTL_EMBL_ENSEMBL | SEQ_REGION_NAME | region | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["3", 185], ["17", 151], ["7", 73], ["2", 47], ["13", 42]] |
| SCIENCE_RESEARCH__FED_NIH_REPORTER | ORG_CITY | city | empty | no real values (blank or sentinel only) | [] |
| SCIENCE_RESEARCH__FED_NIH_REPORTER | ORG_COUNTRY | country | empty | no real values (blank or sentinel only) | [] |
| SCIENCE_RESEARCH__FED_NIH_REPORTER | ORG_FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| SCIENCE_RESEARCH__FED_NIH_REPORTER | ORG_STATE | state | empty | no real values (blank or sentinel only) | [] |
| SCIENCE_RESEARCH__FED_NIH_REPORTER | ORG_STATE_NAME | state | empty | no real values (blank or sentinel only) | [] |
| SCIENCE_RESEARCH__FED_NIH_REPORTER | ORG_ZIP | zip | empty | no real values (blank or sentinel only) | [] |
| SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS | ZIP | zip | mixed / not a ZIP | only 95% look like ZIPs | [["-", 8338], ["90501-1510", 1974], ["01810-1022", 1854], ["20855-2814", 1572],  |
| SCIENCE_RESEARCH__XC_OSF_REGISTRATIONS | REVIEWS_STATE | state | constant | one value for the whole table | [["ACCEPTED", 10]] |
| SCIENCE_RESEARCH__XC_OSF_REGISTRATIONS | REVISION_STATE | state | constant | one value for the whole table | [["APPROVED", 10]] |
| TRANSPORT__FED_DOT_BTS | COUNTY_FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| TRANSPORT__FED_DOT_BTS | STATE_FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY | COUNTRY_CODE | country | country code (98%+ US) | almost no foreign rows -- weak as a join axis | [["US", 309363], ["RQ", 485], ["DE", 364], ["AT", 114], ["VI", 93]] |
| TRANSPORT__FED_FAA_DATA_PORTAL | AIRPORT_ID | airport_port | empty | no real values (blank or sentinel only) | [] |
| TRANSPORT__FED_FAA_DATA_PORTAL | LAT | coordinates | empty | no real values (blank or sentinel only) | [] |
| TRANSPORT__FED_FAA_DATA_PORTAL | LON | coordinates | empty | no real values (blank or sentinel only) | [] |
| TRANSPORT__FED_FAA_DATA_PORTAL | GEOGRAPHIC_SCOPE | facility_site | empty | no real values (blank or sentinel only) | [] |
| TRANSPORT__FED_FAA_DATA_PORTAL | FIPS | fips | empty | no real values (blank or sentinel only) | [] |
| TRANSPORT__FED_FRA_CASUALTIES | DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["4", 212823], ["2", 193925], ["1", 167507], ["3", 153168], ["5", 136779]] |
| TRANSPORT__FED_FRA_CASUALTIES | LOCATION_OF_INJURY_ON_BODY | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["6", 314392], ["3", 255664], ["1", 230724], ["5", 208218], ["9", 65732]] |
| TRANSPORT__FED_FRA_CASUALTIES | STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["17", 96613], ["36", 96041], ["48", 76125], ["42", 71884], ["06", 68487]] |
| TRANSPORT__FED_FRA_CROSSING_INCIDENTS | DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["3", 50219], ["5", 45327], ["4", 44898], ["2", 25834], ["6", 24460]] |
| TRANSPORT__FED_FRA_CROSSING_INCIDENTS | CROSSING_WARNING_LOCATION_CODE | facility_site | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["1", 223356], ["2", 13168], ["0", 5580], ["3", 3403], ["4", 2]] |
| TRANSPORT__FED_FRA_CROSSING_INCIDENTS | STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["48", 26352], ["17", 15903], ["18", 14199], ["39", 14172], ["06", 13132]] |
| TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | DISTRICT | cong_district | coded place (numbers) | codes, not names -- needs a lookup to become a place | [["4", 40613], ["5", 37994], ["6", 34990], ["3", 33174], ["2", 29178]] |
| TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | COUNTY_CODE | county | mixed county |  | [["31", 14674], ["37", 5022], ["201", 4883], ["1", 4728], ["95", 4560]] |
| TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | STATE_CODE | state | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining | [["48", 21954], ["17", 21706], ["06", 11495], ["42", 9787], ["39", 9043]] |
| TRANSPORT__FED_FRA_SAFETY | COUNTY_FIPS | fips | empty | no real values (blank or sentinel only) | [["N/A", 1]] |
| TRANSPORT__FED_FRA_SAFETY | STATE_FIPS | fips | empty | no real values (blank or sentinel only) | [["N/A", 1]] |
| TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT | OPER_ADDR_SAME | address | empty | no real values (blank or sentinel only) | [["NONE", 31503]] |
| TRANSPORT__FED_NTSB_AVIATION_EVENTS | LATITUDE | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["NONE", 3352], ["481243N", 205], ["032415N", 205], ["034393N", 205], ["485027N |
| TRANSPORT__FED_NTSB_AVIATION_EVENTS | LONGITUDE | coordinates | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money | [["NONE", 3351], ["0106356W", 205], ["0955859W", 205], ["0963641W", 205], ["0117 |

## Every column

### CIVIL_RIGHTS__FED_NARA_WRA_AAD  (1 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CAMP_LOCATION | facility_site | 0% | 0 | empty | no real values (blank or sentinel only) |
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
### CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS  (17,168,287 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 63 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 36,864 | mixed / not a ZIP | only 93% look like ZIPs |
### CONSUMER_SAFETY__FED_CPSC_NEISS  (9,794,971 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LOCATION_CODE | facility_site | 71% | 9 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS  (2,227,941 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 62,495 | text place |  |
| STATE | state | 100% | 87 | clean 2-letter state |  |
### CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ADDRESSES  (402,246 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 95% | 377,516 | text place |  |
| COUNTRIES | country | 69% | 370 | country name |  |
| COUNTRY_CODES | country | 69% | 226 | country code |  |
### CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES  (814,344 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 37% | 20,077 | text place |  |
| COUNTRIES | country | 62% | 1,093 | country name |  |
| COUNTRY_CODES | country | 62% | 1,106 | country name |  |
| JURISDICTION | region | 99% | 98 | text place |  |
| JURISDICTION_DESCRIPTION | region | 99% | 81 | text place |  |
### CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES  (26,768 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 32% | 8,658 | text place |  |
| COUNTRIES | country | 86% | 287 | country name |  |
| COUNTRY_CODES | country | 86% | 289 | country code |  |
### CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS  (771,315 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRIES | country | 61% | 4,127 | country name |  |
| COUNTRY_CODES | country | 61% | 4,815 | country code |  |
### CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OTHERS  (2,989 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRIES | country | 13% | 63 | country name |  |
| COUNTRY_CODES | country | 13% | 63 | country code |  |
| JURISDICTION | region | 32% | 6 | text place |  |
| JURISDICTION_DESCRIPTION | region | 32% | 6 | text place |  |
### CORPORATE_REGISTRY__FED_IRS_EO_BMF  (1,983,563 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET | address | 100% | 1,351,657 | text place |  |
| CITY | city | 100% | 24,365 | text place |  |
| STATE | state | 100% | 62 | clean 2-letter state |  |
| ZIP | zip | 100% | 1,500,517 | clean ZIP |  |
### CORPORATE_REGISTRY__INTL_ES_BORME  (3 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 100% | 1 | constant | one value for the whole table |
| PROVINCE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
### CORPORATE_REGISTRY__INTL_IE_CRO  (821,693 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| REGISTERED_ADDRESS | address | 100% | 511,015 | text place |  |
| COUNTRY | country | 100% | 1 | constant | one value for the whole table |
### CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE  (5,734,780 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 99% | 2,243,690 | text place |  |
| ADDRESS_LINE_2 | address | 59% | 331,206 | text place |  |
| POST_TOWN | city | 98% | 43,992 | text place |  |
| COUNTRY | country | 84% | 206 | country name |  |
| COUNTRY_OF_ORIGIN | country | 100% | 215 | country name |  |
| COUNTY | county | 29% | 14,890 | county name |  |
### CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC  (15,804,611 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 90% | 1,251,804 | text place |  |
| ADDRESS_PREMISES | address | 92% | 1,822,927 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| ADDRESS_LOCALITY | city | 94% | 139,234 | text place |  |
| ADDRESS_COUNTRY | country | 85% | 1,343 | country name |  |
| COUNTRY_OF_RESIDENCE | country | 87% | 4,488 | country name |  |
| COUNTRY_REGISTERED | country | 6% | 3,442 | country name |  |
| NATIONALITY | country | 87% | 4,732 | country name |  |
| ADDRESS_POSTAL_CODE | zip | 93% | 1,409,767 | foreign postal code | only 1% look like US ZIPs |
### CRIMINAL_JUSTICE__FED_BJS_DATA  (0 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LOCALITY | city | - | 0 | not measured |  |
| MSA | metro | - | 0 | not measured |  |
| REGION | region | - | 0 | not measured |  |
### ECONOMICS__FED_BLS_QCEW  (3,619,437 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| AREA_FIPS | fips | 100% | 4,532 | FIPS with leading zeros lost | 84% have a FIPS length; modal length 5 -- pad before joining |
| STATE_FIPS | fips | 100% | 59 | mixed / not FIPS | only 84% have a FIPS length; modal length 2 |
### ECONOMICS__FED_DOL_FORM5500  (33,484 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADMIN_ADDRESS_SAME_SPON_IND | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| ADMIN_FOREIGN_ADDRESS1 | address | 0% | 1 | constant | one value for the whole table |
| ADMIN_FOREIGN_ADDRESS2 | address | 0% | 1 | constant | one value for the whole table |
| ADMIN_US_ADDRESS1 | address | 3% | 679 | text place | only 3.5% of rows filled |
| ADMIN_US_ADDRESS2 | address | 1% | 70 | text place | only 1.0% of rows filled |
| PREPARER_FOREIGN_ADDRESS1 | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| PREPARER_FOREIGN_ADDRESS2 | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| PREPARER_US_ADDRESS1 | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| PREPARER_US_ADDRESS2 | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| SPONS_DFE_LOC_FOREIGN_ADDRESS1 | address | 0% | 2 | text place | only 0.0% of rows filled |
| SPONS_DFE_LOC_FOREIGN_ADDRESS2 | address | 0% | 2 | text place | only 0.0% of rows filled |
| SPONS_DFE_LOC_US_ADDRESS1 | address | 8% | 2,246 | text place |  |
| SPONS_DFE_LOC_US_ADDRESS2 | address | 1% | 186 | text place | only 0.9% of rows filled |
| SPONS_DFE_MAIL_US_ADDRESS1 | address | 100% | 28,432 | text place |  |
| SPONS_DFE_MAIL_US_ADDRESS2 | address | 17% | 2,186 | text place |  |
| ADMIN_FOREIGN_CITY | city | 0% | 1 | constant | one value for the whole table |
| ADMIN_US_CITY | city | 3% | 470 | text place | only 3.5% of rows filled |
| PREPARER_FOREIGN_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| PREPARER_US_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| SPONS_DFE_LOC_FOREIGN_CITY | city | 0% | 2 | text place | only 0.0% of rows filled |
| SPONS_DFE_LOC_US_CITY | city | 8% | 1,259 | text place |  |
| SPONS_DFE_MAIL_FOREIGN_CITY | city | 0% | 13 | text place | only 0.4% of rows filled |
| SPONS_DFE_MAIL_US_CITY | city | 100% | 5,250 | text place |  |
| ADMIN_FOREIGN_CNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| PREPARER_FOREIGN_CNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| SPONS_DFE_LOC_FOREIGN_CNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| SPONS_DFE_MAIL_FOREIGN_CNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| ADMIN_FOREIGN_PROV_STATE | state | 0% | 1 | constant | one value for the whole table |
| ADMIN_US_STATE | state | 3% | 51 | clean 2-letter state | only 3.5% of rows filled |
| PREPARER_FOREIGN_PROV_STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
| PREPARER_US_STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
| SPONS_DFE_LOC_FORGN_PROV_ST | state | 0% | 1 | constant | one value for the whole table |
| SPONS_DFE_LOC_US_STATE | state | 8% | 52 | clean 2-letter state |  |
| SPONS_DFE_MAIL_FORGN_PROV_ST | state | 0% | 9 | state names (not codes) | only 0.4% of rows filled |
| SPONS_DFE_MAIL_US_STATE | state | 100% | 55 | clean 2-letter state |  |
| ADMIN_FOREIGN_POSTAL_CD | zip | 0% | 1 | constant | one value for the whole table |
| ADMIN_US_ZIP | zip | 3% | 637 | clean ZIP | only 3.5% of rows filled |
| PREPARER_FOREIGN_POSTAL_CD | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
| PREPARER_US_ZIP | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
| SPONS_DFE_LOC_FORGN_POSTAL_CD | zip | 0% | 1 | constant | one value for the whole table |
| SPONS_DFE_LOC_US_ZIP | zip | 8% | 2,147 | clean ZIP |  |
| SPONS_DFE_MAIL_FORGN_POSTAL_CD | zip | 0% | 12 | foreign postal code | only 2% look like US ZIPs; only 0.4% of rows filled |
| SPONS_DFE_MAIL_US_ZIP | zip | 100% | 13,720 | clean ZIP |  |
### ECONOMICS__FED_FAC_SINGLE_AUDIT  (411,638 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| AUDITEE_ADDRESS_LINE_1 | address | 100% | 109,894 | text place |  |
| AUDITEE_CITY | city | 100% | 12,200 | text place |  |
| AUDITOR_CITY | city | 100% | 3,978 | text place |  |
| AUDITEE_STATE | state | 100% | 59 | clean 2-letter state |  |
| AUDITOR_STATE | state | 100% | 58 | clean 2-letter state |  |
| AUDITEE_ZIP | zip | 100% | 31,819 | clean ZIP |  |
| AUDITOR_ZIP | zip | 100% | 8,657 | clean ZIP |  |
### ECONOMICS__FED_FDIC_FAILED_BANKS  (3,584 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 1,862 | text place |  |
| CITY_STATE | city | 100% | 2,073 | text place |  |
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| STATE_ABBR | state | 0% | 0 | empty | no real values (blank or sentinel only) |
| STATE_NAME | state | 0% | 0 | empty | no real values (blank or sentinel only) |
### ECONOMICS__FED_FINCEN_BOI  (1 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| BENEFICIAL_OWNER_ADDRESS | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| BENEFICIAL_OWNER_ID_ISSUING_JURISDICTION | region | 0% | 0 | empty | no real values (blank or sentinel only) |
| JURISDICTION_OF_FORMATION | region | 0% | 0 | empty | no real values (blank or sentinel only) |
| US_REGISTRATION_STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
### ECONOMICS__FED_FOREIGNASSISTANCE  (95,658 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 100% | 259 | country name |  |
### ECONOMICS__FED_IRS_990  (200 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
| ZIP_CODE | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
### ECONOMICS__FED_IRS_AUTO_REVOCATIONS  (1,207,295 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ORGANIZATION_ADDRESS | address | 100% | 912,826 | text place |  |
| CITY | city | 100% | 30,295 | text place |  |
| COUNTRY | country | 100% | 149 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| STATE | state | 100% | 62 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 1,009,584 | clean ZIP |  |
### ECONOMICS__FED_IRS_BMF  (1,974,830 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET | address | 100% | 1,338,840 | text place |  |
| CITY | city | 100% | 24,236 | text place |  |
| STATE | state | 100% | 62 | clean 2-letter state |  |
| ZIP | zip | 100% | 1,494,909 | clean ZIP |  |
### ECONOMICS__FED_IRS_EO_PR  (2,587 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET | address | 100% | 2,443 | text place |  |
| CITY | city | 100% | 114 | text place |  |
| STATE | state | 100% | 1 | constant | one value for the whole table |
| ZIP | zip | 100% | 1,896 | clean ZIP |  |
### ECONOMICS__FED_IRS_PUB78_ELIGIBLE_DONEES  (1,435,544 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 22,237 | text place |  |
| COUNTRY | country | 100% | 104 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| STATE | state | 100% | 61 | clean 2-letter state |  |
### ECONOMICS__FED_IRS_REVOCATION  (1,187,366 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 100% | 911,885 | text place |  |
| CITY | city | 100% | 30,295 | text place |  |
| COUNTRY | country | 100% | 149 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| STATE | state | 100% | 62 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 1,008,024 | clean ZIP |  |
### ECONOMICS__FED_IRS_SOI_CHARITIES  (2,450 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET | address | 100% | 2,224 | text place |  |
| CITY | city | 100% | 208 | text place |  |
| STATE | state | 45% | 10 | mixed / not a state | only 84% are 2-letter US codes (foreign provinces, money, or free text) |
| ZIP | zip | 100% | 859 | clean ZIP |  |
### ECONOMICS__FED_PBGC_DATA  (134,534 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 6% | 80 | state names (not codes) |  |
### ECONOMICS__FED_SBA_LOANS  (2,174,502 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| BORROWER_CITY | city | 100% | 31,783 | text place |  |
| CONGRESSIONAL_DISTRICT | cong_district | 96% | 54 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| PROJECT_COUNTY | county | 100% | 1,954 | county name |  |
| BORROWER_STATE | state | 100% | 61 | clean 2-letter state |  |
| CDC_STATE | state | 10% | 51 | clean 2-letter state |  |
| LENDER_STATE | state | 6% | 61 | clean 2-letter state |  |
| PROJECT_STATE | state | 100% | 60 | clean 2-letter state |  |
| BORROWER_ZIP | zip | 100% | 38,126 | mixed / not a ZIP | only 89% look like ZIPs |
### ECONOMICS__FED_SBA_PPP  (968,524 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| BORROWER_CITY | city | 100% | 16,272 | text place |  |
| CONGRESSIONAL_DISTRICT | cong_district | 100% | 461 | text place |  |
| PROJECT_COUNTY | county | 100% | 1,922 | county name |  |
| RURAL_URBAN_INDICATOR | metro | 100% | 2 | text place |  |
| BORROWER_STATE | state | 100% | 56 | clean 2-letter state |  |
| PROJECT_STATE | state | 100% | 57 | clean 2-letter state |  |
| SERVICING_LENDER_STATE | state | 100% | 55 | clean 2-letter state |  |
| BORROWER_ZIP | zip | 100% | 507,978 | clean ZIP |  |
### ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL  (19,902,879 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RECIPIENT_ADDRESS_LINE_1 | address | 69% | 1,769,893 | text place |  |
| RECIPIENT_ADDRESS_LINE_2 | address | 8% | 125,728 | text place |  |
| PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | city | 65% | 20,399 | text place |  |
| RECIPIENT_CITY_CODE | city | 69% | 26,205 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| RECIPIENT_CITY_NAME | city | 78% | 27,521 | text place |  |
| RECIPIENT_FOREIGN_CITY_NAME | city | 0% | 5,350 | text place | only 0.3% of rows filled |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_CODE | country | 90% | 242 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_NAME | country | 90% | 243 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| RECIPIENT_COUNTRY_CODE | country | 87% | 240 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| RECIPIENT_COUNTRY_NAME | country | 87% | 235 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTY_NAME | county | 87% | 1,964 | county name |  |
| RECIPIENT_COUNTY_NAME | county | 96% | 4,674 | county name |  |
| PRIMARY_PLACE_OF_PERFORMANCE_CODE | facility_site | 98% | 97,132 | text place |  |
| PRIMARY_PLACE_OF_PERFORMANCE_FOREIGN_LOCATION | facility_site | 0% | 2,640 | text place | only 0.4% of rows filled |
| PRIMARY_PLACE_OF_PERFORMANCE_SCOPE | facility_site | 93% | 6 | text place |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_CURRENT | facility_site | 89% | 729 | text place |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_ORIGINAL | facility_site | 90% | 2,065 | text place |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE | fips | 92% | 3,767 | clean FIPS (5-digit) |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_STATE_FIPS_CODE | fips | 96% | 56 | clean FIPS (2-digit) |  |
| PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE | fips | 99% | 7,107 | FIPS with leading zeros lost | 88% have a FIPS length; modal length 5 -- pad before joining |
| PRIME_AWARD_TRANSACTION_RECIPIENT_STATE_FIPS_CODE | fips | 99% | 56 | clean FIPS (2-digit) |  |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_NAME | state | 99% | 642 | state names (not codes) |  |
| RECIPIENT_FOREIGN_PROVINCE_NAME | state | 0% | 697 | state names (not codes) | only 0.1% of rows filled |
| RECIPIENT_STATE_CODE | state | 99% | 75 | clean 2-letter state |  |
| RECIPIENT_STATE_NAME | state | 99% | 59 | state names (not codes) |  |
| PRIMARY_PLACE_OF_PERFORMANCE_ZIP_4 | zip | 65% | 532,000 | clean ZIP |  |
| RECIPIENT_FOREIGN_POSTAL_CODE | zip | 0% | 1,247 | ZIP with leading zeros lost | 30% are 1-4 digits (00501 -> 501); only 0.0% of rows filled |
| RECIPIENT_ZIP_CODE | zip | 78% | 38,859 | clean ZIP |  |
| RECIPIENT_ZIP_LAST_4_CODE | zip | 59% | 10,013 | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) |
### ECONOMICS__FED_USASPENDING_CONTRACTS  (6,325,622 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | city | 97% | 8,466 | text place |  |
| RECIPIENT_CITY_NAME | city | 100% | 10,775 | text place |  |
| RECIPIENT_COUNTRY_NAME | country | 100% | 180 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE | state | 97% | 62 | clean 2-letter state |  |
| RECIPIENT_STATE_CODE | state | 98% | 60 | clean 2-letter state |  |
| RECIPIENT_ZIP_4_CODE | zip | 100% | 92,721 | clean ZIP |  |
### ECONOMICS__FED_USASPENDING_CONTRACTS_FULL  (20,000,000 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RECIPIENT_ADDRESS_LINE_1 | address | 100% | 528,662 | text place |  |
| RECIPIENT_ADDRESS_LINE_2 | address | 2% | 9,734 | text place | only 1.9% of rows filled |
| AIRPORT_AUTHORITY | airport_port | 100% | 2 | text place |  |
| PORT_AUTHORITY | airport_port | 100% | 2 | text place |  |
| CITY_LOCAL_GOVERNMENT | city | 100% | 3 | text place |  |
| MUNICIPALITY_LOCAL_GOVERNMENT | city | 100% | 2 | text place |  |
| PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | city | 90% | 13,971 | text place |  |
| RECIPIENT_CITY_NAME | city | 100% | 20,801 | text place |  |
| SCHOOL_DISTRICT_LOCAL_GOVERNMENT | cong_district | 100% | 2 | text place |  |
| COUNTRY_OF_PRODUCT_OR_SERVICE_ORIGIN | country | 68% | 252 | country name |  |
| COUNTRY_OF_PRODUCT_OR_SERVICE_ORIGIN_CODE | country | 90% | 268 | country code |  |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_CODE | country | 95% | 246 | country code |  |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_NAME | country | 95% | 266 | country name |  |
| RECIPIENT_COUNTRY_CODE | country | 100% | 366 | country code |  |
| RECIPIENT_COUNTRY_NAME | country | 99% | 212 | country name |  |
| COUNTY_LOCAL_GOVERNMENT | county | 100% | 3 | county name |  |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTY_NAME | county | 90% | 2,030 | county name |  |
| RECIPIENT_COUNTY_NAME | county | 74% | 1,903 | county name |  |
| PLACE_OF_MANUFACTURE | facility_site | 86% | 23 | text place |  |
| PLACE_OF_MANUFACTURE_CODE | facility_site | 86% | 17 | text place |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_CURRENT | facility_site | 90% | 545 | text place |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_ORIGINAL | facility_site | 90% | 588 | text place |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE | fips | 90% | 3,289 | clean FIPS (5-digit) |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_STATE_FIPS_CODE | fips | 90% | 56 | clean FIPS (2-digit) |  |
| PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE | fips | 74% | 3,202 | clean FIPS (5-digit) |  |
| PRIME_AWARD_TRANSACTION_RECIPIENT_STATE_FIPS_CODE | fips | 97% | 56 | clean FIPS (2-digit) |  |
| HISTORICALLY_UNDERUTILIZED_BUSINESS_ZONE_HUBZONE_FIRM | region | 100% | 6 | text place |  |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE | state | 90% | 62 | clean 2-letter state |  |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_NAME | state | 90% | 67 | state names (not codes) |  |
| RECIPIENT_STATE_CODE | state | 97% | 71 | clean 2-letter state |  |
| RECIPIENT_STATE_NAME | state | 75% | 1,471 | state names (not codes) |  |
| STATE_CONTROLLED_INSTITUTION_OF_HIGHER_LEARNING | state | 100% | 2 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
| US_STATE_GOVERNMENT | state | 100% | 2 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
| PRIMARY_PLACE_OF_PERFORMANCE_ZIP_4 | zip | 91% | 479,146 | clean ZIP |  |
| RECIPIENT_ZIP_4_CODE | zip | 99% | 426,926 | clean ZIP |  |
### ECONOMICS__FED_USASPENDING_TOPTIER_AGENCIES  (111 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CONGRESSIONAL_JUSTIFICATION_URL | cong_district | 88% | 98 | text place |  |
### ECONOMICS__FED_US_SEC_EDGAR  (48,984 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| BUSINESS_ADDRESS | address | 100% | 25 | text place |  |
| STATE_OF_INCORPORATION | state | 97% | 7 | clean 2-letter state |  |
### ECONOMICS__FED_US_USASPENDING_API  (300 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PLACE_OF_PERFORMANCE_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| PLACE_OF_PERFORMANCE_FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| RECIPIENT_LOCATION_FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| PLACE_OF_PERFORMANCE_STATE | state | 65% | 40 | clean 2-letter state |  |
| RECIPIENT_LOCATION_STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
### ECONOMICS__INTL_GFI_TRADE  (0 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | - | 0 | empty table |  |
### ECONOMICS__INTL_GLEIF  (3,382,301 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ENTITY_HEADQUARTERSADDRESS_CITY | city | 100% | 122,476 | text place |  |
| ENTITY_LEGALADDRESS_CITY | city | 100% | 119,982 | text place |  |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_1_CITY | city | 1% | 3,473 | text place | only 1.4% of rows filled |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_2_CITY | city | 1% | 3,101 | text place | only 1.3% of rows filled |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_3_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_4_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_5_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_1_CITY | city | 2% | 5,443 | text place | only 2.3% of rows filled |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_2_CITY | city | 2% | 5,365 | text place | only 2.3% of rows filled |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_HEADQUARTERSADDRESS_COUNTRY | country | 100% | 240 | country code |  |
| ENTITY_LEGALADDRESS_COUNTRY | country | 100% | 239 | country code |  |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_1_COUNTRY | country | 1% | 101 | country code | only 1.4% of rows filled |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_2_COUNTRY | country | 1% | 81 | country code | only 1.3% of rows filled |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_3_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_4_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_5_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_1_COUNTRY | country | 2% | 60 | country code | only 2.3% of rows filled |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_2_COUNTRY | country | 2% | 46 | country code | only 2.3% of rows filled |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_HEADQUARTERSADDRESS_REGION | region | 66% | 2,827 | text place |  |
| ENTITY_LEGALADDRESS_REGION | region | 66% | 2,845 | text place |  |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_1_REGION | region | 1% | 477 | text place | only 0.8% of rows filled |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_2_REGION | region | 1% | 395 | text place | only 0.7% of rows filled |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_3_REGION | region | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_4_REGION | region | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_5_REGION | region | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_1_REGION | region | 2% | 354 | text place | only 2.1% of rows filled |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_2_REGION | region | 2% | 319 | text place | only 2.0% of rows filled |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_REGION | region | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_REGION | region | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_REGION | region | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_HEADQUARTERSADDRESS_POSTALCODE | zip | 99% | 364,352 | mixed / not a ZIP | only 41% look like ZIPs |
| ENTITY_LEGALADDRESS_POSTALCODE | zip | 99% | 353,494 | mixed / not a ZIP | only 40% look like ZIPs |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_1_POSTALCODE | zip | 1% | 8,359 | mixed / not a ZIP | only 19% look like ZIPs; only 1.3% of rows filled |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_2_POSTALCODE | zip | 1% | 7,881 | mixed / not a ZIP | only 18% look like ZIPs; only 1.3% of rows filled |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_3_POSTALCODE | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_4_POSTALCODE | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_5_POSTALCODE | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_1_POSTALCODE | zip | 2% | 14,671 | ZIP with leading zeros lost | 42% are 1-4 digits (00501 -> 501); only 2.3% of rows filled |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_2_POSTALCODE | zip | 2% | 14,476 | ZIP with leading zeros lost | 43% are 1-4 digits (00501 -> 501); only 2.3% of rows filled |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_POSTALCODE | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_POSTALCODE | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_POSTALCODE | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
### ECONOMICS__INTL_IPC_FOOD_INSECURITY_GLOBAL  (735 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 100% | 50 | country code |  |
| TOTAL_COUNTRY_POPULATION | country | 96% | 49 | country name |  |
### ECONOMICS__INTL_IT_ISTAT  (213,284 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 100% | 1 | constant | one value for the whole table |
### ECONOMICS__XC_OWID_GINI  (2,389 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| WORLD_REGION_ACCORDING_TO_OWID | region | 95% | 6 | text place |  |
### EDUCATION__FED_CFTC_COT_FINANCIAL  (34,683 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ASSET_MGR_POSITIONS_LONG_ALL | coordinates | 93% | 26,051 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| CHANGE_IN_ASSET_MGR_LONG_ALL | coordinates | 87% | 14,299 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| CHANGE_IN_DEALER_LONG_ALL | coordinates | 88% | 14,611 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| CHANGE_IN_LEV_MONEY_LONG_ALL | coordinates | 95% | 17,074 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| CHANGE_IN_NONREPT_LONG_ALL | coordinates | 96% | 11,520 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| CHANGE_IN_OTHER_REPT_LONG_ALL | coordinates | 78% | 10,123 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| CHANGE_IN_TOT_REPT_LONG_ALL | coordinates | 98% | 21,386 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| CONC_GROSS_LE_4_TDR_LONG_ALL | coordinates | 100% | 926 | clean coordinate |  |
| CONC_GROSS_LE_8_TDR_LONG_ALL | coordinates | 100% | 858 | clean coordinate |  |
| CONC_NET_LE_4_TDR_LONG_ALL | coordinates | 100% | 930 | clean coordinate |  |
| CONC_NET_LE_8_TDR_LONG_ALL | coordinates | 100% | 880 | clean coordinate |  |
| DEALER_POSITIONS_LONG_ALL | coordinates | 93% | 25,047 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| LEV_MONEY_POSITIONS_LONG_ALL | coordinates | 98% | 26,576 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| NONREPT_POSITIONS_LONG_ALL | coordinates | 99% | 23,378 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| OTHER_REPT_POSITIONS_LONG_ALL | coordinates | 84% | 17,658 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| PCT_OF_OI_ASSET_MGR_LONG_ALL | coordinates | 100% | 894 | coordinate with 0,0 trap | 8% are exactly 0 (Gulf of Guinea rows) |
| PCT_OF_OI_DEALER_LONG_ALL | coordinates | 100% | 928 | coordinate with 0,0 trap | 7% are exactly 0 (Gulf of Guinea rows) |
| PCT_OF_OI_LEV_MONEY_LONG_ALL | coordinates | 100% | 899 | clean coordinate |  |
| PCT_OF_OI_NONREPT_LONG_ALL | coordinates | 100% | 701 | clean coordinate |  |
| PCT_OF_OI_OTHER_REPT_LONG_ALL | coordinates | 100% | 896 | coordinate with 0,0 trap | 17% are exactly 0 (Gulf of Guinea rows) |
| PCT_OF_OI_TOT_REPT_LONG_ALL | coordinates | 100% | 704 | clean coordinate |  |
| TOT_REPT_POSITIONS_LONG_ALL | coordinates | 100% | 32,346 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| TRADERS_ASSET_MGR_LONG_ALL | coordinates | 78% | 197 | clean coordinate |  |
| TRADERS_DEALER_LONG_ALL | coordinates | 71% | 102 | clean coordinate |  |
| TRADERS_LEV_MONEY_LONG_ALL | coordinates | 83% | 169 | clean coordinate |  |
| TRADERS_OTHER_REPT_LONG_ALL | coordinates | 61% | 368 | clean coordinate |  |
| TRADERS_TOT_REPT_LONG_ALL | coordinates | 100% | 594 | coordinate, partly out of range | 82% parse in range |
| CFTC_REGION_CODE | region | 7% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### EDUCATION__FED_CFTC_COT_FUTURES  (287,053 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CHANGE_IN_COMMERCIAL_LONG_ALL | coordinates | 93% | 44,510 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| CHANGE_IN_NONCOMMERCIAL_LONG_ALL | coordinates | 79% | 32,935 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| CHANGE_IN_NONREPORTABLE_LONG_ALL | coordinates | 82% | 22,317 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| CHANGE_IN_TOTAL_REPORTABLE_LONG_ALL | coordinates | 95% | 50,451 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| COMMERCIAL_POSITIONS_LONG_ALL | coordinates | 99% | 144,301 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| COMMERCIAL_POSITIONS_LONG_OLD | coordinates | 98% | 140,020 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| COMMERCIAL_POSITIONS_LONG_OTHER | coordinates | 13% | 22,340 | coordinate with 0,0 trap | 87% are exactly 0 (Gulf of Guinea rows) |
| CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL | coordinates | 100% | 967 | clean coordinate |  |
| CONCENTRATION_GROSS_LT_4_TDR_LONG_OLD | coordinates | 100% | 977 | clean coordinate |  |
| CONCENTRATION_GROSS_LT_4_TDR_LONG_OTHER | coordinates | 14% | 989 | clean coordinate |  |
| CONCENTRATION_GROSS_LT_8_TDR_LONG_ALL | coordinates | 100% | 955 | clean coordinate |  |
| CONCENTRATION_GROSS_LT_8_TDR_LONG_OLD | coordinates | 100% | 960 | clean coordinate |  |
| CONCENTRATION_GROSS_LT_8_TDR_LONG_OTHER | coordinates | 14% | 989 | clean coordinate |  |
| CONCENTRATION_NET_LT_4_TDR_LONG_ALL | coordinates | 100% | 988 | clean coordinate |  |
| CONCENTRATION_NET_LT_4_TDR_LONG_OLD | coordinates | 100% | 993 | clean coordinate |  |
| CONCENTRATION_NET_LT_4_TDR_LONG_OTHER | coordinates | 13% | 998 | clean coordinate |  |
| CONCENTRATION_NET_LT_8_TDR_LONG_ALL | coordinates | 100% | 992 | clean coordinate |  |
| CONCENTRATION_NET_LT_8_TDR_LONG_OLD | coordinates | 100% | 993 | clean coordinate |  |
| CONCENTRATION_NET_LT_8_TDR_LONG_OTHER | coordinates | 13% | 998 | clean coordinate |  |
| NONCOMMERCIAL_POSITIONS_LONG_ALL | coordinates | 91% | 79,937 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| NONCOMMERCIAL_POSITIONS_LONG_OLD | coordinates | 90% | 79,201 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| NONCOMMERCIAL_POSITIONS_LONG_OTHER | coordinates | 11% | 15,400 | coordinate with 0,0 trap | 89% are exactly 0 (Gulf of Guinea rows) |
| NONREPORTABLE_POSITIONS_LONG_ALL | coordinates | 94% | 59,268 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| NONREPORTABLE_POSITIONS_LONG_OLD | coordinates | 94% | 58,309 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| NONREPORTABLE_POSITIONS_LONG_OTHER | coordinates | 16% | 15,248 | coordinate with 0,0 trap | 84% are exactly 0 (Gulf of Guinea rows) |
| OF_OI_COMMERCIAL_LONG_ALL | coordinates | 100% | 1,018 | clean coordinate |  |
| OF_OI_COMMERCIAL_LONG_OLD | coordinates | 100% | 1,018 | clean coordinate |  |
| OF_OI_COMMERCIAL_LONG_OTHER | coordinates | 100% | 1,014 | coordinate with 0,0 trap | 87% are exactly 0 (Gulf of Guinea rows) |
| OF_OI_NONCOMMERCIAL_LONG_ALL | coordinates | 100% | 998 | coordinate with 0,0 trap | 10% are exactly 0 (Gulf of Guinea rows) |
| OF_OI_NONCOMMERCIAL_LONG_OLD | coordinates | 100% | 1,000 | coordinate with 0,0 trap | 10% are exactly 0 (Gulf of Guinea rows) |
| OF_OI_NONCOMMERCIAL_LONG_OTHER | coordinates | 100% | 993 | coordinate with 0,0 trap | 89% are exactly 0 (Gulf of Guinea rows) |
| OF_OI_NONREPORTABLE_LONG_ALL | coordinates | 100% | 943 | coordinate with 0,0 trap | 7% are exactly 0 (Gulf of Guinea rows) |
| OF_OI_NONREPORTABLE_LONG_OLD | coordinates | 100% | 967 | coordinate with 0,0 trap | 7% are exactly 0 (Gulf of Guinea rows) |
| OF_OI_NONREPORTABLE_LONG_OTHER | coordinates | 100% | 997 | coordinate with 0,0 trap | 84% are exactly 0 (Gulf of Guinea rows) |
| OF_OI_TOTAL_REPORTABLE_LONG_ALL | coordinates | 100% | 948 | clean coordinate |  |
| OF_OI_TOTAL_REPORTABLE_LONG_OLD | coordinates | 100% | 962 | clean coordinate |  |
| OF_OI_TOTAL_REPORTABLE_LONG_OTHER | coordinates | 100% | 996 | coordinate with 0,0 trap | 86% are exactly 0 (Gulf of Guinea rows) |
| TOTAL_REPORTABLE_POSITIONS_LONG_ALL | coordinates | 100% | 161,194 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| TOTAL_REPORTABLE_POSITIONS_LONG_OLD | coordinates | 100% | 157,353 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| TOTAL_REPORTABLE_POSITIONS_LONG_OTHER | coordinates | 14% | 24,371 | coordinate with 0,0 trap | 86% are exactly 0 (Gulf of Guinea rows) |
| TRADERS_COMMERCIAL_LONG_ALL | coordinates | 99% | 370 | clean coordinate |  |
| TRADERS_COMMERCIAL_LONG_OLD | coordinates | 98% | 344 | clean coordinate |  |
| TRADERS_COMMERCIAL_LONG_OTHER | coordinates | 13% | 278 | clean coordinate |  |
| TRADERS_NONCOMMERCIAL_LONG_ALL | coordinates | 91% | 403 | clean coordinate |  |
| TRADERS_NONCOMMERCIAL_LONG_OLD | coordinates | 90% | 394 | clean coordinate |  |
| TRADERS_NONCOMMERCIAL_LONG_OTHER | coordinates | 11% | 229 | clean coordinate |  |
| TRADERS_TOTAL_REPORTABLE_LONG_ALL | coordinates | 100% | 698 | coordinate, partly out of range | 91% parse in range |
| TRADERS_TOTAL_REPORTABLE_LONG_OLD | coordinates | 100% | 685 | coordinate, partly out of range | 92% parse in range |
| TRADERS_TOTAL_REPORTABLE_LONG_OTHER | coordinates | 14% | 497 | coordinate with 0,0 trap | 86% are exactly 0 (Gulf of Guinea rows) |
| CFTC_REGION_CODE | region | 65% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION  (6,273 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 2,286 | text place |  |
| LATITUDE | coordinates | 91% | 5,742 | clean coordinate |  |
| LONGITUDE | coordinates | 91% | 5,745 | clean coordinate |  |
| STATE_FIPS | fips | 100% | 58 | FIPS with leading zeros lost | 82% have a FIPS length; modal length 2 -- pad before joining |
| REGION_CODE | region | 100% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE | state | 100% | 59 | clean 2-letter state |  |
| TUITION_IN_STATE | state | 58% | 2,729 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| TUITION_OUT_OF_STATE | state | 58% | 2,803 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| ZIP | zip | 100% | 5,788 | clean ZIP |  |
### EDUCATION__FED_ED_EDFACTS  (33 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
### EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_DECLARED_STATS  (470 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADVERTISER_DECLARED_PROMOTER_ADDRESS | address | 6% | 28 | text place |  |
| REGION | region | 100% | 2 | text place |  |
### EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_GEO_SPEND  (614,078 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 100% | 2 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| COUNTRY_SUBDIVISION_PRIMARY | country | 98% | 56 | country code |  |
### EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS  (21,211 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| REGIONS | region | 100% | 13 | text place |  |
### EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS  (1,562,870 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| REGIONS | region | 100% | 13 | text place |  |
### EDUCATION__FED_GOOGLE_POLADS_GEO_SPEND  (1,289 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 100% | 12 | country code |  |
| COUNTRY_SUBDIVISION_PRIMARY | country | 99% | 202 | country name |  |
| COUNTRY_SUBDIVISION_SECONDARY | country | 100% | 1,286 | country name |  |
### EDUCATION__FED_SENATE_LDA_FILINGS  (438,132 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| REGISTRANT_CITY | city | 100% | 1,406 | text place |  |
| CLIENT_COUNTRY | country | 99% | 127 | country code |  |
| REGISTRANT_COUNTRY | country | 100% | 18 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| CLIENT_STATE | state | 86% | 57 | clean 2-letter state |  |
| REGISTRANT_STATE | state | 100% | 59 | clean 2-letter state |  |
### ENERGY__FED_EIA860_1_UTILITY  (6,643 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 100% | 3,733 | text place |  |
| CITY | city | 100% | 1,812 | text place |  |
| STATE | state | 100% | 57 | clean 2-letter state |  |
| ZIP | zip | 100% | 2,619 | mixed / not a ZIP | only 85% look like ZIPs |
### ENERGY__FED_EIA860_2_PLANT  (16,132 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 99% | 14,390 | text place |  |
| CITY | city | 100% | 5,800 | text place |  |
| LATITUDE | coordinates | 100% | 45 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 93 | clean coordinate |  |
| COUNTY | county | 100% | 1,477 | county name |  |
| NERC_REGION | region | 98% | 7 | text place |  |
| STATE | state | 100% | 51 | clean 2-letter state |  |
| TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_STATE | state | 94% | 51 | clean 2-letter state |  |
| ZIP | zip | 100% | 8,101 | mixed / not a ZIP | only 88% look like ZIPs |
### ENERGY__FED_EIA860_3_1_GENERATOR  (26,855 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY | county | 100% | 1,417 | county name |  |
| RTO_ISO_LOCATION_DESIGNATION_FOR_REPORTING_WHOLESALE_SALES_DATA_TO_FERC | facility_site | 17% | 2,434 | text place |  |
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__FED_EIA860_3_2_WIND  (1,563 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY | county | 100% | 439 | county name |  |
| STATE | state | 100% | 43 | clean 2-letter state |  |
### ENERGY__FED_EIA860_3_3_SOLAR  (7,154 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY | county | 100% | 876 | county name |  |
| STATE | state | 100% | 50 | clean 2-letter state |  |
### ENERGY__FED_EIA860_3_4_ENERGY_STORAGE  (786 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY | county | 100% | 274 | county name |  |
| STATE | state | 100% | 42 | clean 2-letter state |  |
### ENERGY__FED_EIA860_3_5_MULTIFUEL  (2,893 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY | county | 100% | 500 | county name |  |
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__FED_EIA860_4_OWNER  (5,495 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| OWNER_STREET_ADDRESS | address | 99% | 1,047 | text place |  |
| OWNER_CITY | city | 99% | 550 | text place |  |
| OWNER_STATE | state | 98% | 54 | clean 2-letter state |  |
| STATE | state | 100% | 51 | clean 2-letter state |  |
| OWNER_ZIP | zip | 98% | 759 | mixed / not a ZIP | only 86% look like ZIPs |
### ENERGY__FED_EIA860_6_2_ENVIROEQUIP  (4,428 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__FED_EIA861_ADVANCED_METERS  (2,725 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__FED_EIA861_DELIVERY_COMPANIES  (7 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 1 | constant | one value for the whole table |
### ENERGY__FED_EIA861_DEMAND_RESPONSE  (339 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 49 | clean 2-letter state |  |
### ENERGY__FED_EIA861_DISTRIBUTION_SYSTEMS  (1,353 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__FED_EIA861_DYNAMIC_PRICING  (857 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__FED_EIA861_ENERGY_EFFICIENCY  (458 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 50 | clean 2-letter state |  |
### ENERGY__FED_EIA861_MERGERS  (4 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 100% | 4 | text place |  |
| CITY | city | 100% | 4 | text place |  |
| STATE | state | 100% | 2 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 4 | clean ZIP |  |
### ENERGY__FED_EIA861_NET_METERING  (1,004 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__FED_EIA861_NON_NET_METERING_DISTRIBUTED  (507 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 48 | clean 2-letter state |  |
### ENERGY__FED_EIA861_OPERATIONAL_DATA  (1,711 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| NERC_REGION | region | 81% | 18 | text place |  |
| STATE | state | 100% | 52 | clean 2-letter state |  |
### ENERGY__FED_EIA861_RELIABILITY  (971 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__FED_EIA861_SALES_ULT_CUST  (2,815 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__FED_EIA861_SALES_ULT_CUST_CS  (674 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 38 | clean 2-letter state |  |
### ENERGY__FED_EIA861_SERVICE_TERRITORY  (11,775 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY | county | 100% | 1,851 | county name |  |
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__FED_EIA861_SHORT_FORM  (1,724 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 47 | clean 2-letter state |  |
### ENERGY__FED_EIA861_UTILITY_DATA  (1,701 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| NERC_REGION | region | 81% | 18 | text place |  |
| STATE | state | 100% | 52 | clean 2-letter state |  |
### ENERGY__FED_EIA_861_BALANCING_AUTHORITY  (189 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 51 | clean 2-letter state |  |
### ENERGY__INTL_EMBER_ELEC  (369,264 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 100% | 230 | country name |  |
| EMBER_REGION | region | 94% | 8 | text place |  |
### ENVIRONMENT__EPA_PENALTY_GAP  (93,808 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 78% | 13,973 | text place |  |
| LATITUDE | coordinates | 94% | 69,818 | clean coordinate |  |
| LONGITUDE | coordinates | 94% | 72,148 | clean coordinate |  |
| COUNTY | county | 94% | 3,050 | county name |  |
| TRI_ON_SITE_RELEASES | facility_site | 3% | 2,389 | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 3.4% of rows filled |
| FIPS_CODE | fips | 93% | 3,198 | clean FIPS (5-digit) |  |
| EPA_REGION | region | 93% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE | state | 94% | 60 | clean 2-letter state |  |
### ENVIRONMENT__FED_EPA_AQS_SITES  (20,994 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 100% | 20,619 | text place |  |
| CITY_NAME | city | 100% | 3,844 | text place |  |
| LATITUDE | coordinates | 96% | 47 | clean coordinate |  |
| LONGITUDE | coordinates | 96% | 85 | clean coordinate |  |
| COUNTY_CODE | county | 100% | 249 | county code |  |
| COUNTY_NAME | county | 100% | 1,378 | county name |  |
| MET_SITE_COUNTY_CODE | county | 2% | 71 | county code | only 2.1% of rows filled |
| AQS_SITE_ID | facility_site | 100% | 21,135 | text place |  |
| LOCAL_SITE_NAME | facility_site | 31% | 6,157 | text place |  |
| LOCATION_SETTING | facility_site | 91% | 4 | text place |  |
| MET_SITE_DIRECTION | facility_site | 3% | 16 | text place | only 2.8% of rows filled |
| MET_SITE_DISTANCE | facility_site | 3% | 470 | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 3.1% of rows filled |
| MET_SITE_SITE_NUMBER | facility_site | 2% | 115 | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 2.1% of rows filled |
| MET_SITE_TYPE | facility_site | 10% | 6 | text place |  |
| SITE_CLOSED_DATE | facility_site | 77% | 3,123 | not a place (dates) | name-scan false hit |
| SITE_ESTABLISHED_DATE | facility_site | 100% | 4,221 | not a place (dates) | name-scan false hit |
| SITE_NUMBER | facility_site | 100% | 1,235 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| CBSA_NAME | metro | 87% | 850 | text place |  |
| MET_SITE_STATE_CODE | state | 2% | 33 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining; only 2.1% of rows filled |
| STATE_CODE | state | 100% | 56 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| STATE_NAME | state | 100% | 56 | state names (not codes) |  |
| ZIP_CODE | zip | 52% | 5,824 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_ECHO  (3,135,554 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET | address | 86% | 2,399,126 | text place |  |
| CITY | city | 86% | 48,316 | text place |  |
| LATITUDE | coordinates | 98% | 1,793,262 | clean coordinate |  |
| LONGITUDE | coordinates | 98% | 1,973,514 | clean coordinate |  |
| COUNTY | county | 88% | 4,186 | county name |  |
| TRI_ON_SITE_RELEASES | facility_site | 0% | 7,048 | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 0.4% of rows filled |
| FIPS_CODE | fips | 91% | 3,267 | clean FIPS (5-digit) |  |
| EPA_REGION | region | 81% | 11 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE | state | 98% | 89 | clean 2-letter state |  |
| ZIP | zip | 86% | 42,851 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_EGRID_PLANT_2022  (11,974 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PLANT_LATITUDE | coordinates | 100% | 11,466 | clean coordinate |  |
| PLANT_LONGITUDE | coordinates | 100% | 11,498 | clean coordinate |  |
| PLANT_COUNTY_NAME | county | 100% | 1,402 | county name |  |
| PLANT_FIPS_COUNTY_CODE | fips | 100% | 256 | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining |
| PLANT_FIPS_STATE_CODE | fips | 100% | 53 | clean FIPS (2-digit) |  |
| NERC_REGION_ACRONYM | region | 100% | 10 | text place |  |
| PLANT_ASSOCIATED_ISO_RTO_TERRITORY | region | 64% | 8 | text place |  |
| PLANT_STATE_ABBREVIATION | state | 100% | 53 | clean 2-letter state |  |
### ENVIRONMENT__FED_EPA_ENVIROFACTS  (5,000 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY_NAME | city | 100% | 826 | text place |  |
| LATITUDE | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| LONGITUDE | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| COUNTY_NAME | county | 100% | 138 | county name |  |
| SITE_ID | facility_site | 0% | 0 | empty | no real values (blank or sentinel only) |
| STATE_CODE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
| POSTAL_CODE | zip | 100% | 1,539 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_FRS_FACILITIES  (5,300,149 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 89% | 3,767,673 | text place |  |
| CITY | city | 90% | 63,362 | text place |  |
| CONGRESSIONAL_DISTRICT | cong_district | 76% | 55 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| LATITUDE | coordinates | 79% | 2,447,002 | clean coordinate |  |
| LONGITUDE | coordinates | 79% | 2,855,282 | clean coordinate |  |
| COUNTY | county | 91% | 4,477 | county name |  |
| SITE_TYPE | facility_site | 95% | 13 | text place |  |
| SUPPLEMENTAL_LOCATION | facility_site | 6% | 230,004 | text place |  |
| FIPS_CODE | fips | 80% | 7,643 | FIPS with leading zeros lost | 85% have a FIPS length; modal length 5 -- pad before joining |
| EPA_REGION | region | 90% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_CODE | state | 100% | 60 | clean 2-letter state |  |
| STATE_NAME | state | 96% | 134 | state names (not codes) |  |
| POSTAL_CODE | zip | 89% | 647,702 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES  (3,277,557 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FAC_STREET | address | 85% | 2,459,499 | text place |  |
| FAC_CITY | city | 87% | 50,570 | text place |  |
| LATITUDE_MEASURE | coordinates | 81% | 1,889,794 | clean coordinate |  |
| LONGITUDE_MEASURE | coordinates | 81% | 2,060,512 | clean coordinate |  |
| FAC_COUNTY | county | 88% | 4,330 | county name |  |
| FAC_EPA_REGION | region | 81% | 11 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| FAC_STATE | state | 98% | 88 | clean 2-letter state |  |
| FAC_ZIP | zip | 85% | 43,126 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS  (4,406,498 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LOCATION_ADDRESS | address | 87% | 2,812,360 | text place |  |
| CITY_NAME | city | 88% | 65,516 | text place |  |
| COUNTRY_NAME | country | 66% | 121 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| COUNTY_NAME | county | 65% | 4,192 | county name |  |
| SUPPLEMENTAL_LOCATION | facility_site | 7% | 160,097 | text place |  |
| FIPS_CODE | fips | 66% | 6,750 | FIPS with leading zeros lost | 66% have a FIPS length; modal length 5 -- pad before joining |
| STATE_CODE | state | 90% | 88 | clean 2-letter state |  |
| STATE_NAME | state | 76% | 266 | state names (not codes) |  |
| POSTAL_CODE | zip | 87% | 360,803 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_GHGRP_FACILITY  (136,005 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS1 | address | 92% | 9,813 | text place |  |
| ADDRESS2 | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| CITY | city | 100% | 4,106 | text place |  |
| LATITUDE | coordinates | 100% | 13,797 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 13,335 | clean coordinate |  |
| COUNTY | county | 92% | 2,542 | county name |  |
| COUNTY_FIPS | fips | 92% | 2,155 | clean FIPS (5-digit) |  |
| STATE | state | 100% | 55 | clean 2-letter state |  |
| STATE_NAME | state | 100% | 55 | state names (not codes) |  |
| ZIP | zip | 99% | 6,087 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES  (279,728 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 100% | 251,460 | text place |  |
| CITY | city | 100% | 24,485 | text place |  |
| COUNTY_NAME | county | 100% | 1,882 | county name |  |
| EPA_REGION | region | 100% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| LOCAL_CONTROL_REGION_CODE | region | 4% | 62 | text place | only 4.2% of rows filled |
| LOCAL_CONTROL_REGION_NAME | region | 4% | 61 | text place | only 4.2% of rows filled |
| STATE | state | 100% | 55 | clean 2-letter state |  |
| ZIP_CODE | zip | 98% | 58,175 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES  (1,779,096 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_EPA_FLAG | state | 100% | 3 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS  (106,009 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_EPA_FLAG | state | 100% | 3 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS  (175,736 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_EPA_FLAG | state | 100% | 3 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS  (620,302 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_EPA_FLAG | state | 100% | 3 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS  (499,113 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_EPA_FLAG | state | 100% | 3 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY  (102,037 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_CODE | state | 95% | 54 | clean 2-letter state |  |
### ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES  (1,213,737 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LOCATION_ADDRESS | address | 94% | 885,759 | text place |  |
| SUPPLEMENTAL_ADDRESS_TEXT | address | 10% | 69,154 | text place |  |
| CITY | city | 93% | 33,557 | text place |  |
| GEOCODE_LATITUDE | coordinates | 93% | 731,583 | clean coordinate |  |
| GEOCODE_LONGITUDE | coordinates | 93% | 780,360 | clean coordinate |  |
| COUNTY_CODE | county | 58% | 3,268 | county name |  |
| STATE_CODE | state | 100% | 68 | clean 2-letter state |  |
| ZIP | zip | 92% | 99,654 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS  (112,373 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_LOCAL_PENALTY_AMT | state | 42% | 11,139 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
### ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS  (1,900,067 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_EPA_FLAG | state | 100% | 2 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
### ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS  (383,519 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ACTIVITY_LOCATION | facility_site | 100% | 61 | text place |  |
### ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS  (1,166,410 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ACTIVITY_LOCATION | facility_site | 100% | 63 | text place |  |
### ENVIRONMENT__FED_EPA_RCRA_FACILITIES  (1,613,224 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 100% | 1,418,396 | text place |  |
| CITY_NAME | city | 100% | 23,395 | text place |  |
| ACTIVITY_LOCATION | facility_site | 100% | 66 | text place |  |
| STATE_CODE | state | 100% | 69 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 218,284 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS  (434,734 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ACTIVITY_LOCATION | facility_site | 100% | 57 | text place |  |
### ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS  (708,114 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ACTIVITY_LOCATION | facility_site | 100% | 62 | text place |  |
### ENVIRONMENT__FED_EPA_RCRA_VIOSNC_HISTORY  (2,675,581 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ACTIVITY_LOCATION | facility_site | 100% | 62 | text place |  |
### ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES  (1,554,832 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_FACILITY_ID | state | 70% | 290,378 | state names (not codes) |  |
### ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS  (578,198 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY_SERVED | city | 27% | 18,258 | text place |  |
| COUNTY_SERVED | county | 70% | 1,944 | county name |  |
| STATE_SERVED | state | 27% | 54 | clean 2-letter state |  |
| ZIP_CODE_SERVED | zip | 1% | 1,647 | clean ZIP | only 1.2% of rows filled |
### ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS  (434,040 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE1 | address | 62% | 186,355 | text place |  |
| ADDRESS_LINE2 | address | 43% | 116,394 | text place |  |
| EMAIL_ADDR | address | 24% | 76,175 | text place |  |
| CITY_NAME | city | 97% | 28,628 | text place |  |
| COUNTRY_CODE | country | 98% | 3 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| EPA_REGION | region | 100% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_CODE | state | 97% | 66 | clean 2-letter state |  |
| ZIP_CODE | zip | 94% | 53,785 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT  (15,432,737 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_MCL | state | 4% | 157 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining; only 3.7% of rows filled |
### ENVIRONMENT__FED_EPA_SUPERFUND_SITE_BOUNDARIES  (2,114 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_COMMENT | address | 36% | 539 | text place |  |
| STREET_ADDRESS | address | 100% | 1,908 | text place |  |
| CITY | city | 100% | 1,378 | text place |  |
| COUNTY | county | 100% | 634 | county name |  |
| SITE_CONTACT_EMAIL | facility_site | 98% | 489 | text place |  |
| SITE_CONTACT_NAME | facility_site | 98% | 489 | text place |  |
| SITE_CONTACT_PHONE | facility_site | 98% | 476 | text place |  |
| SITE_FEATURE_CLASS | facility_site | 100% | 3 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| SITE_FEATURE_DESCRIPTION | facility_site | 99% | 1,491 | text place |  |
| SITE_FEATURE_NAME | facility_site | 99% | 1,516 | text place |  |
| SITE_FEATURE_SOURCE | facility_site | 86% | 986 | text place |  |
| SITE_FEATURE_TYPE | facility_site | 100% | 14 | text place |  |
| SITE_NAME | facility_site | 100% | 1,911 | text place |  |
| SITE_URL | facility_site | 100% | 1,920 | text place |  |
| EPA_REGION_CODE | region | 100% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_CODE | state | 100% | 57 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 1,627 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_TRI_BASIC_2023  (78,647 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| C_5_STREET_ADDRESS | address | 100% | 22,411 | text place |  |
| C_6_CITY | city | 100% | 5,401 | text place |  |
| C_12_LATITUDE | coordinates | 100% | 21,054 | clean coordinate |  |
| C_13_LONGITUDE | coordinates | 100% | 21,276 | clean coordinate |  |
| C_7_COUNTY | county | 100% | 1,527 | county name |  |
| C_104_OFF_SITE_TREATED_TOTAL | facility_site | 15% | 7,894 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_109_8_1_A_ON_SITE_CONTAINED | facility_site | 100% | 2,855 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_110_8_1_B_ON_SITE_OTHER | facility_site | 100% | 23,320 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_111_8_1_C_OFF_SITE_CONTAIN | facility_site | 100% | 9,029 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_112_8_1_D_OFF_SITE_OTHER_R | facility_site | 100% | 9,836 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_115_8_4_RECYCLING_ON_SITE | facility_site | 100% | 3,343 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_117_8_6_TREATMENT_ON_SITE | facility_site | 100% | 12,651 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_118_8_7_TREATMENT_OFF_SITE | facility_site | 100% | 7,617 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_65_ON_SITE_RELEASE_TOTAL | facility_site | 71% | 25,055 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_88_OFF_SITE_RELEASE_TOTAL | facility_site | 34% | 14,571 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_94_OFF_SITE_RECYCLED_TOTAL | facility_site | 24% | 14,421 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_97_OFF_SITE_ENERGY_RECOVERY_T | facility_site | 100% | 4,939 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| C_9_ZIP | zip | 100% | 8,931 | clean ZIP |  |
### ENVIRONMENT__FED_EPA_TRI_FACILITY  (64,990 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| MAIL_STREET_ADDRESS | address | 98% | 52,696 | text place |  |
| STREET_ADDRESS | address | 100% | 65,691 | text place |  |
| CITY_NAME | city | 100% | 7,905 | text place |  |
| MAIL_CITY | city | 98% | 7,390 | text place |  |
| FAC_LATITUDE | coordinates | 75% | 27,864 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| FAC_LONGITUDE | coordinates | 75% | 35,246 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| PREF_LATITUDE | coordinates | 57% | 43 | clean coordinate |  |
| PREF_LONGITUDE | coordinates | 57% | 83 | clean coordinate |  |
| MAIL_COUNTRY | country | 1% | 2 | country name (98%+ US) | almost no foreign rows -- weak as a join axis; only 1.1% of rows filled |
| COUNTY_NAME | county | 100% | 1,770 | county name |  |
| STATE_COUNTY_FIPS_CODE | fips | 100% | 2,859 | clean FIPS (5-digit) |  |
| REGION | region | 100% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| MAIL_PROVINCE | state | 0% | 4 | state names (not codes) | only 0.0% of rows filled |
| MAIL_STATE_ABBR | state | 98% | 59 | clean 2-letter state |  |
| STATE_ABBR | state | 100% | 56 | clean 2-letter state |  |
| MAIL_ZIP_CODE | zip | 98% | 19,754 | clean ZIP |  |
| ZIP_CODE | zip | 100% | 18,718 | clean ZIP |  |
### ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST  (248,835 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 100% | 211,049 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 224,368 | clean coordinate |  |
| COUNTY_NAME | county | 100% | 529 | county name |  |
| STATE_NAME | state | 100% | 27 | state names (not codes) |  |
### ENVIRONMENT__FED_FRACFOCUS_REGISTRY  (7,200,550 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 100% | 211,049 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 224,368 | clean coordinate |  |
| COUNTY_NAME | county | 100% | 529 | county name |  |
| STATE_NAME | state | 100% | 27 | state names (not codes) |  |
### ENVIRONMENT__FED_FRACFOCUS_WATER_SOURCE  (23,747 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY_NAME | county | 100% | 280 | county name |  |
| STATE_NAME | state | 100% | 19 | state names (not codes) |  |
### ENVIRONMENT__FED_NID_DAMS  (92,766 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 65% | 14,426 | text place |  |
| CONGRESSIONAL_DISTRICT | cong_district | 100% | 422 | text place |  |
| LATITUDE | coordinates | 100% | 84,620 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 87,206 | clean coordinate |  |
| COUNTY | county | 100% | 1,791 | county name |  |
| IS_STATE_REGULATED | state | 100% | 2 | state names (not codes) |  |
| STATE | state | 100% | 52 | state names (not codes) |  |
| STATE_REGULATORY_AGENCY | state | 75% | 100 | state names (not codes) |  |
### ENVIRONMENT__FED_NOAA_STORM_EVENTS  (1,780,730 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| BEGIN_LAT | coordinates | 59% | 135,995 | clean coordinate |  |
| BEGIN_LON | coordinates | 59% | 185,312 | clean coordinate |  |
| END_LAT | coordinates | 59% | 145,079 | clean coordinate |  |
| END_LON | coordinates | 59% | 204,543 | clean coordinate |  |
| BEGIN_LOCATION | facility_site | 62% | 51,401 | text place |  |
| END_LOCATION | facility_site | 62% | 51,594 | text place |  |
| CZ_FIPS | fips | 100% | 670 | FIPS with leading zeros lost | 58% have a FIPS length; modal length 2 -- pad before joining |
| STATE_FIPS | fips | 100% | 70 | FIPS with leading zeros lost | 89% have a FIPS length; modal length 2 -- pad before joining |
| TOR_OTHER_CZ_FIPS | fips | 0% | 206 | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining; only 0.2% of rows filled |
| STATE | state | 100% | 70 | state names (not codes) |  |
| TOR_OTHER_CZ_STATE | state | 0% | 48 | clean 2-letter state | only 0.2% of rows filled |
### ENVIRONMENT__FED_NOAA_WEATHER_API  (287 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| LONGITUDE | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| FIPS_CODE | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| GEOMETRY | geometry | 11% | 31 | text place |  |
| ZONE_UGC | region | 100% | 225 | text place |  |
| ZIP_CODE | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
### ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS  (2,039 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| OPERATOR_STREET_ADDRESS | address | 100% | 218 | text place |  |
| OPERATOR_CITY | city | 100% | 90 | text place |  |
| LOCATION_LATITUDE | coordinates | 100% | 25 | clean coordinate |  |
| LOCATION_LONGITUDE | coordinates | 100% | 57 | clean coordinate |  |
| TIME_ZONE | region | 42% | 5 | text place |  |
| OPERATOR_STATE | state | 100% | 38 | clean 2-letter state |  |
| OPERATOR_POSTAL_CODE | zip | 100% | 136 | clean ZIP |  |
### ENVIRONMENT__FED_USCG_NRC_INCIDENTS  (1,029,020 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RESPONSIBLE_CITY | city | 63% | 30,595 | text place |  |
| RESPONSIBLE_STATE | state | 65% | 131 | clean 2-letter state |  |
| RESPONSIBLE_ZIP | zip | 48% | 42,763 | mixed / not a ZIP | only 65% look like ZIPs |
### ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS  (116,662 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RESPONSIBLE_CITY | city | 52% | 8,755 | text place |  |
| RESPONSIBLE_STATE | state | 54% | 92 | clean 2-letter state |  |
| RESPONSIBLE_ZIP | zip | 34% | 9,565 | mixed / not a ZIP | only 94% look like ZIPs |
### ENVIRONMENT__FED_USGS_MINERALS  (304,632 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 100% | 221,144 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 239,388 | clean coordinate |  |
| COUNTRY | country | 100% | 163 | country name |  |
| COUNTY | county | 83% | 2,042 | county name |  |
| SITE_NAME | facility_site | 96% | 178,322 | text place |  |
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| REGION | region | 10% | 8 | text place |  |
| STATE | state | 96% | 914 | state names (not codes) |  |
| US_STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
### ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS  (117,672 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 100% | 30 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 57 | clean coordinate |  |
| COUNTY | county | 100% | 792 | county name |  |
| LOCATION_NOTES | facility_site | 47% | 1,318 | text place |  |
| STATE | state | 100% | 27 | state names (not codes) |  |
### ENVIRONMENT__FED_USGS_WATER  (6,456,952 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 100% | 3,717 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 3,768 | clean coordinate |  |
| COUNTY_CD | county | 100% | 734 | county code |  |
| SITE_NAME | facility_site | 100% | 3,767 | text place |  |
| SITE_NO | facility_site | 100% | 3,774 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_CD | state | 100% | 10 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| HUC_CD | watershed | 100% | 1,005 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### ENVIRONMENT__FED_USGS_WBD_HUC8  (2,456 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| SHAPE_AREA | geometry | 100% | 2,430 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| SHAPE_LENGTH | geometry | 100% | 2,483 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| HUC8 | watershed | 100% | 2,452 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| WATERSHED_NAME | watershed | 100% | 2,334 | text place |  |
### ENVIRONMENT__FED_WQP_MONITORING_STATIONS  (5,818 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 95% | 3 | clean coordinate |  |
| LONGITUDE | coordinates | 95% | 3 | clean coordinate |  |
| COUNTRY_CODE | country | 100% | 1 | constant | one value for the whole table |
| COUNTY_CODE | county | 95% | 6 | county code |  |
| MONITORING_LOCATION_DESCRIPTION_TEXT | facility_site | 14% | 379 | text place |  |
| MONITORING_LOCATION_IDENTIFIER | facility_site | 100% | 5,738 | text place |  |
| MONITORING_LOCATION_NAME | facility_site | 100% | 5,213 | text place |  |
| MONITORING_LOCATION_TYPE_NAME | facility_site | 100% | 36 | text place |  |
| STATE_CODE | state | 100% | 1 | constant | one value for the whole table |
| HUC_EIGHT_DIGIT_CODE | watershed | 94% | 7 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### ENVIRONMENT__INTL_GEM_HAZARD  (12 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| LONGITUDE | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| COUNTRY | country | 100% | 12 | country name |  |
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
### ENVIRONMENT__INTL_GLOBAL_WITNESS_DEFENDERS  (232 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 22% | 6 | country name |  |
| REGION | region | 0% | 0 | empty | no real values (blank or sentinel only) |
### FINANCE__FED_EPA_ICIS_FEC_CASE_ENFORCEMENT_CONCLUSION_FACILITIES  (150,866 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FACILITY_CITY | city | 99% | 14,800 | text place |  |
| FACILITY_STATE | state | 100% | 70 | clean 2-letter state |  |
| FACILITY_ZIP | zip | 98% | 36,164 | clean ZIP |  |
### FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES  (204,019 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LOCATION_ADDRESS | address | 99% | 116,636 | text place |  |
| CITY | city | 99% | 15,245 | text place |  |
| STATE_CODE | state | 100% | 70 | clean 2-letter state |  |
| ZIP | zip | 99% | 38,223 | clean ZIP |  |
### FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS  (260,556 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| EPA_REGION_CODE | region | 99% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### FINANCE__FED_FARA  (30 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FOREIGN_PRINCIPAL_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
### FINANCE__FED_FATCA_FFI  (516,298 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY_NAME | country | 100% | 229 | country name |  |
### FINANCE__FED_FDIC_BANK_DATA  (27,836 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 100% | 23,497 | text place |  |
| CITY | city | 100% | 7,140 | text place |  |
| HOLDING_COMPANY_CITY | city | 61% | 3,992 | text place |  |
| OCC_DISTRICT | cong_district | 6% | 4 | text place |  |
| LATITUDE | coordinates | 100% | 21,221 | coordinate with 0,0 trap | 10% are exactly 0 (Gulf of Guinea rows) |
| LONGITUDE | coordinates | 100% | 21,756 | coordinate with 0,0 trap | 10% are exactly 0 (Gulf of Guinea rows) |
| COUNTY | county | 100% | 1,767 | county name |  |
| FIPS | fips | 100% | 2,980 | clean FIPS (5-digit) |  |
| CBSA | metro | 83% | 920 | text place |  |
| CBSA_METRO_NAME | metro | 69% | 389 | text place |  |
| FDIC_REGION | region | 100% | 6 | text place |  |
| ZIP | zip | 100% | 12,700 | clean ZIP |  |
### FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS  (2,822,977 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| BRANCH_ADDRESS | address | 100% | 277,908 | text place |  |
| INSTITUTION_ADDRESS | address | 100% | 25,966 | text place |  |
| BRANCH_CITY | city | 100% | 15,168 | text place |  |
| BRANCH_CITY_ALT | city | 100% | 11,526 | text place |  |
| HOLDING_COMPANY_CITY | city | 87% | 4,502 | text place |  |
| INSTITUTION_CITY | city | 100% | 6,166 | text place |  |
| FED_DISTRICT_CODE | cong_district | 100% | 13 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| FED_DISTRICT_NAME | cong_district | 100% | 13 | text place |  |
| OCC_DISTRICT_CODE | cong_district | 95% | 14 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| OCC_DISTRICT_NAME | cong_district | 95% | 19 | text place |  |
| SIMS_LATITUDE | coordinates | 92% | 522,223 | clean coordinate |  |
| SIMS_LONGITUDE | coordinates | 92% | 525,230 | clean coordinate |  |
| BRANCH_COUNTRY | country | 100% | 15 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| INSTITUTION_COUNTRY | country | 99% | 36 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| BRANCH_COUNTY_NAME | county | 100% | 1,962 | county name |  |
| BRANCH_PLACE_CODE | facility_site | 74% | 21,827 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| BRANCH_COUNTY_FIPS | fips | 100% | 333 | FIPS with leading zeros lost | 59% have a FIPS length; modal length 2 -- pad before joining |
| BRANCH_STATE_COUNTY_FIPS | fips | 100% | 3,329 | FIPS with leading zeros lost | 85% have a FIPS length; modal length 5 -- pad before joining |
| BRANCH_STATE_FIPS | fips | 100% | 58 | FIPS with leading zeros lost | 85% have a FIPS length; modal length 2 -- pad before joining |
| INSTITUTION_STATE_COUNTY_FIPS | fips | 100% | 2,918 | FIPS with leading zeros lost | 88% have a FIPS length; modal length 5 -- pad before joining |
| BRANCH_CBSA_DIVISION_CODE | metro | 24% | 43 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| BRANCH_CBSA_DIVISION_NAME | metro | 24% | 52 | text place |  |
| BRANCH_CSA_CODE | metro | 72% | 209 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| BRANCH_CSA_NAME | metro | 72% | 291 | text place |  |
| BRANCH_METRO_FLAG | metro | 76% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| BRANCH_MSA_CODE | metro | 78% | 407 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| BRANCH_MSA_NAME | metro | 78% | 505 | text place |  |
| FDIC_REGION_CODE | region | 100% | 8 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| FDIC_REGION_NAME | region | 100% | 8 | text place |  |
| BRANCH_STATE | state | 100% | 59 | clean 2-letter state |  |
| BRANCH_STATE_NAME | state | 100% | 61 | state names (not codes) |  |
| HOLDING_COMPANY_STATE | state | 82% | 54 | clean 2-letter state |  |
| INSTITUTION_STATE | state | 100% | 56 | clean 2-letter state |  |
| INSTITUTION_STATE_NAME | state | 100% | 60 | state names (not codes) |  |
| BRANCH_ZIP | zip | 100% | 24,446 | clean ZIP |  |
| INSTITUTION_ZIP | zip | 100% | 10,563 | clean ZIP |  |
### FINANCE__FED_FEC_BULK  (20,938 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CMTE_CITY | city | 100% | 3,786 | text place |  |
| CMTE_ZIP | zip | 100% | 8,604 | clean ZIP |  |
### FINANCE__FED_FEC_BULK_COMMITTEES  (20,007 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CMTE_CITY | city | 100% | 3,632 | text place |  |
| CMTE_ZIP | zip | 100% | 8,404 | clean ZIP |  |
### FINANCE__FED_FEC_CANDIDATES  (27,095 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CAND_CITY | city | 100% | 4,918 | text place |  |
| CAND_OFFICE_DISTRICT | cong_district | 66% | 71 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| CAND_ZIP | zip | 98% | 10,276 | clean ZIP |  |
### FINANCE__FED_FEC_COMMITTEES  (60,031 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CMTE_CITY | city | 100% | 5,475 | text place |  |
| CMTE_ZIP | zip | 100% | 13,637 | clean ZIP |  |
### FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE  (866,730 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 3,129 | text place |  |
| STATE | state | 100% | 58 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 10,279 | clean ZIP |  |
### FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES  (261,033 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CAN_OFFICE_STATE | state | 88% | 61 | clean 2-letter state |  |
### FINANCE__FED_FEC_INDIV_CONTRIBUTIONS  (84,172,112 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 47,537 | text place |  |
| STATE | state | 100% | 78 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 2,869,783 | clean ZIP |  |
### FINANCE__FED_FHFA_FHLB_MEMBERSHIP  (6,327 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 2,920 | text place |  |
| DISTRICT | cong_district | 100% | 11 | text place |  |
| STATE | state | 100% | 54 | clean 2-letter state |  |
| ZIP | zip | 100% | 4,722 | clean ZIP |  |
### FINANCE__FED_FINRA_MPID_LIST  (4,215 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LOCATION | facility_site | 31% | 532 | text place |  |
### FINANCE__FED_IRS_SOI  (179,796 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_FIPS | fips | 100% | 51 | FIPS with leading zeros lost | 87% have a FIPS length; modal length 2 -- pad before joining |
| STATE | state | 100% | 51 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 29,922 | mixed / not a ZIP | only 92% look like ZIPs |
### FINANCE__FED_MSRB_REGISTRANTS  (925 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 49 | clean 2-letter state |  |
### FINANCE__FED_NCUA_CALL_REPORTS  (0 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | - | 0 | not measured |  |
| STATE | state | - | 0 | not measured |  |
| ZIP_CODE | zip | - | 0 | not measured |  |
### FINANCE__FED_NCUA_CALL_REPORTS_FOICU  (4,336 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 54 | clean 2-letter state |  |
| CITY | city | 100% | 1,887 | text place |  |
| ZIP_CODE | zip | 100% | 3,916 | clean ZIP |  |
### FINANCE__FED_NCUA_CHARTER_MERGER_EVENTS  (27 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CONTINUING_LOCATION | facility_site | 100% | 26 | text place |  |
| MERGING_LOCATION | facility_site | 100% | 26 | text place |  |
| REGION | region | 100% | 3 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### FINANCE__FED_NCUA_FEDERALLY_INSURED_CU_LIST  (4,250 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_MAILING_ADDRESS | address | 100% | 4,193 | text place |  |
| CITY_MAILING_ADDRESS | city | 100% | 1,862 | text place |  |
| NCUA_REGION | region | 100% | 4 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_MAILING_ADDRESS | state | 100% | 54 | clean 2-letter state |  |
| ZIP_CODE_MAILING_ADDRESS | zip | 100% | 3,314 | clean ZIP |  |
### FINANCE__FED_OCC_NATIONAL_BANKS  (724 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LOC | address | 100% | 704 | text place |  |
| CITY | city | 100% | 569 | text place |  |
| STATE | state | 100% | 50 | clean 2-letter state |  |
### FINANCE__FED_OCC_THRIFTS  (218 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LOC | address | 100% | 216 | text place |  |
| CITY | city | 100% | 201 | text place |  |
| STATE | state | 100% | 48 | clean 2-letter state |  |
### FINANCE__FED_PCAOB_FORM_AP_FILINGS  (155,384 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| SIGNED_EMAIL_ADDRESS | address | 100% | 2,068 | text place |  |
| FIRM_ISSUING_CITY | city | 100% | 762 | text place |  |
| FIRM_COUNTRY | country | 100% | 55 | country name |  |
| FIRM_ISSUING_COUNTRY | country | 100% | 63 | country name |  |
| FIRM_ISSUING_STATE | state | 90% | 53 | state names (not codes) |  |
### FINANCE__FED_SEC_13F_FILERS  (344,109 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FILINGMANAGER_CITY | city | 100% | 2,288 | text place |  |
| FILINGMANAGER_ZIPCODE | zip | 99% | 5,761 | mixed / not a ZIP | only 87% look like ZIPs |
### FINANCE__FED_SEC_BUSINESS_DEVELOPMENT_COMPANY_REPORT  (212 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_1 | address | 100% | 154 | text place |  |
| ADDRESS_2 | address | 54% | 77 | text place |  |
| CITY | city | 100% | 54 | text place |  |
| STATE | state | 100% | 27 | clean 2-letter state |  |
| ZIP_CODE | zip | 99% | 94 | clean ZIP |  |
### FINANCE__FED_SEC_CLOSED_END_FUND_INFORMATION  (973 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_1 | address | 100% | 459 | text place |  |
| ADDRESS_2 | address | 51% | 207 | text place |  |
| CITY | city | 100% | 133 | text place |  |
| STATE | state | 100% | 40 | clean 2-letter state |  |
| ZIP_CODE | zip | 98% | 237 | clean ZIP |  |
### FINANCE__FED_SEC_INSIDER_REPORTINGOWNER  (1,934,673 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 6,322 | text place |  |
| STATE | state | 100% | 170 | clean 2-letter state |  |
| ZIP_CODE | zip | 99% | 11,010 | clean ZIP |  |
### FINANCE__FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS  (43,123 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_1 | address | 100% | 720 | text place |  |
| ADDRESS_2 | address | 42% | 298 | text place |  |
| CITY | city | 100% | 238 | text place |  |
| STATE | state | 100% | 48 | clean 2-letter state |  |
| ZIP_CODE | zip | 98% | 423 | clean ZIP |  |
### FINANCE__INTL_ISO_MIC_REGISTRY  (2,864 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 360 | text place |  |
| ISO_COUNTRY_CODE_ISO_3166 | country | 100% | 150 | country code |  |
### FINANCE__INTL_OSFI_REGULATED_FI  (343 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 234 | text place |  |
| ADDRESS_LINE_2 | address | 62% | 120 | text place |  |
| CITY | city | 100% | 42 | text place |  |
| PROVINCE_STATE | state | 100% | 10 | state names (not codes) |  |
| POSTAL_ZIP_CODE | zip | 100% | 189 | foreign postal code | only 0% look like US ZIPs |
### FINANCE__INTL_WB_IDS  (62,983 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY_CODE | country | 100% | 136 | country code |  |
| COUNTRY_NAME | country | 100% | 136 | country name |  |
### FOREIGN_INFLUENCE__FED_FARA_BULK  (48,103 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_1 | address | 40% | 7,874 | text place |  |
| ADDRESS_2 | address | 14% | 2,162 | text place |  |
| CITY | city | 29% | 1,192 | text place |  |
| COUNTRY_LOCATION_REPRESENTED | country | 17% | 246 | country name |  |
| FOREIGN_PRINCIPAL_COUNTRY | country | 25% | 251 | country name |  |
| STATE | state | 30% | 51 | clean 2-letter state |  |
| ZIP | zip | 23% | 1,620 | clean ZIP |  |
### GOVERNMENT_RECORDS__FED_NARA_AAD  (9 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| GEO_LOCATION | facility_site | 0% | 0 | empty | no real values (blank or sentinel only) |
| FIPS_GEO | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
### HEALTH__FED_CDC_ANXIETY_DEPRESSION  (16,794 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 52 | state names (not codes) |  |
### HEALTH__FED_CDC_DRUG_POISONING_COUNTY  (53,387 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY | county | 100% | 3,122 | county name |  |
| FIPS | fips | 100% | 3,149 | clean FIPS (5-digit) |  |
| FIPS_STATE | fips | 100% | 51 | FIPS with leading zeros lost | 90% have a FIPS length; modal length 2 -- pad before joining |
| STATE | state | 100% | 51 | state names (not codes) |  |
### HEALTH__FED_CDC_HEALTH_INSURANCE  (16,056 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 52 | state names (not codes) |  |
### HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY  (132,000 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| GEOID | fips | 100% | 3,153 | clean FIPS (5-digit) |  |
| ST_GEOID | fips | 100% | 51 | clean FIPS (2-digit) |  |
### HEALTH__FED_CDC_LEADING_CAUSES_STATE  (10,868 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 52 | state names (not codes) |  |
### HEALTH__FED_CDC_OVERDOSE  (83,790 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 54 | clean 2-letter state |  |
| STATE_NAME | state | 100% | 54 | state names (not codes) |  |
### HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS  (6,637 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 49 | clean 2-letter state |  |
### HEALTH__FED_CMS_DIALYSIS  (7,557 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 7,527 | text place |  |
| ADDRESS_LINE_2 | address | 17% | 617 | text place |  |
| CITY_TOWN | city | 100% | 2,936 | text place |  |
| LONG_TERM_CATHETER_DATA_AVAILABILITY_CODE | coordinates | 100% | 5 | coordinate, partly out of range | 93% parse in range |
| NUMBER_OF_PATIENTS_IN_LONG_TERM_CATHETER_SUMMARY | coordinates | 97% | 270 | clean coordinate |  |
| NUMBER_OF_PATIENT_MONTHS_IN_LONG_TERM_CATHETER_SUMMARY | coordinates | 97% | 1,607 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| PERCENTAGE_OF_ADULT_PATIENTS_WITH_LONG_TERM_CATHETER_IN_USE | coordinates | 93% | 76 | clean coordinate |  |
| COUNTY_PARISH | county | 100% | 1,231 | county name |  |
| STATE | state | 100% | 56 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 5,361 | clean ZIP |  |
### HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY  (31,403,215 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 5,113 | text place |  |
| LONG_STAY_PERCENT | coordinates | 10% | 8,757 | clean coordinate |  |
| LONG_STAY_RESIDENTS | coordinates | 100% | 448 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| COUNTY_NAME | county | 100% | 1,712 | county name |  |
| FIPS_COUNTY_CODE | fips | 100% | 298 | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining |
| STATE | state | 100% | 53 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 9,229 | clean ZIP |  |
### HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS  (11,063 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 10,725 | text place |  |
| ADDRESS_LINE_2 | address | 21% | 891 | text place |  |
| CITY | city | 100% | 3,798 | text place |  |
| ENROLLMENT_STATE | state | 100% | 55 | clean 2-letter state |  |
| INCORPORATION_STATE | state | 83% | 54 | clean 2-letter state |  |
| STATE | state | 100% | 55 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 10,276 | clean ZIP |  |
### HEALTH__FED_CMS_HCRIS  (6,103 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 100% | 5,924 | text place |  |
| CITY | city | 100% | 3,074 | text place |  |
| OTHER_LONG_TERM_LIABILITIES | coordinates | 67% | 3,938 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| TOTAL_LONG_TERM_LIABILITIES | coordinates | 84% | 4,971 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| COUNTY | county | 91% | 1,561 | county name |  |
| MEDICARE_CBSA_NUMBER | metro | 99% | 470 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| RURAL_VERSUS_URBAN | metro | 99% | 3 | text place |  |
| STATE_CODE | state | 100% | 55 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 5,401 | mixed / not a ZIP | only 80% look like ZIPs |
### HEALTH__FED_CMS_HOME_HEALTH  (12,392 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 100% | 12,547 | text place |  |
| DENOMINATOR_FOR_HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | 70% | 2,348 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| FOOTNOTE_FOR_HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | 30% | 5 | text place |  |
| HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | 70% | 2,277 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| NUMERATOR_FOR_HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | 70% | 2,305 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| CITY_TOWN | city | 100% | 2,694 | text place |  |
| STATE | state | 100% | 55 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 4,777 | clean ZIP |  |
### HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS  (11,508 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 9,796 | text place |  |
| ADDRESS_LINE_2 | address | 71% | 1,962 | text place |  |
| CITY | city | 100% | 2,636 | text place |  |
| LOCATION_OTHER_TYPE_TEXT | facility_site | 0% | 0 | empty | no real values (blank or sentinel only) |
| PRACTICE_LOCATION_TYPE | facility_site | 21% | 1 | constant | one value for the whole table |
| ENROLLMENT_STATE | state | 100% | 55 | clean 2-letter state |  |
| INCORPORATION_STATE | state | 81% | 55 | clean 2-letter state |  |
| STATE | state | 100% | 55 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 10,409 | clean ZIP |  |
### HEALTH__FED_CMS_HOSPICE  (6,852 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 6,987 | text place |  |
| ADDRESS_LINE_2 | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| CITY_TOWN | city | 100% | 2,003 | text place |  |
| COUNTY_PARISH | county | 99% | 1,005 | county name |  |
| CMS_REGION | region | 100% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE | state | 100% | 55 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 3,233 | clean ZIP |  |
### HEALTH__FED_CMS_HOSPITAL_COMPARE  (5,432 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 100% | 5,417 | text place |  |
| CITY_TOWN | city | 100% | 3,032 | text place |  |
| COUNTY_PARISH | county | 100% | 1,557 | county name |  |
| STATE | state | 100% | 56 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 4,872 | clean ZIP |  |
### HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS  (9,175 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 6,495 | text place |  |
| ADDRESS_LINE_2 | address | 8% | 594 | text place |  |
| CITY | city | 100% | 3,117 | text place |  |
| SUBGROUP_LONG_TERM | coordinates | 100% | 2 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| LOCATION_OTHER_TYPE_TEXT | facility_site | 8% | 251 | text place |  |
| PRACTICE_LOCATION_TYPE | facility_site | 92% | 6 | text place |  |
| ENROLLMENT_STATE | state | 100% | 56 | clean 2-letter state |  |
| INCORPORATION_STATE | state | 67% | 53 | clean 2-letter state |  |
| STATE | state | 100% | 56 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 6,389 | clean ZIP |  |
### HEALTH__FED_CMS_HOSPITAL_GENERAL  (5,432 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 100% | 5,417 | text place |  |
| CITY_TOWN | city | 100% | 3,032 | text place |  |
| COUNTY_PARISH | county | 100% | 1,557 | county name |  |
| STATE | state | 100% | 56 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 4,872 | clean ZIP |  |
### HEALTH__FED_CMS_HPT_MRF  (1 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| HOSPITAL_ADDRESS | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| HOSPITAL_LOCATION | facility_site | 0% | 0 | empty | no real values (blank or sentinel only) |
### HEALTH__FED_CMS_IRF  (1,222 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 1,239 | text place |  |
| ADDRESS_LINE_2 | address | 6% | 68 | text place |  |
| CITY_TOWN | city | 100% | 837 | text place |  |
| COUNTY_PARISH | county | 100% | 533 | county name |  |
| CMS_REGION | region | 100% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE | state | 100% | 52 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 1,140 | clean ZIP |  |
### HEALTH__FED_CMS_LTCH  (311 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 319 | text place |  |
| ADDRESS_LINE_2 | address | 0% | 1 | empty | no real values (blank or sentinel only) |
| CITY_TOWN | city | 100% | 263 | text place |  |
| COUNTY_PARISH | county | 100% | 221 | county name |  |
| CMS_REGION | region | 100% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE | state | 100% | 47 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 308 | clean ZIP |  |
### HEALTH__FED_CMS_MAIN  (158 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| ZIP | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
### HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM  (1,037 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS_LINE_1 | address | 100% | 1,001 | text place |  |
| STREET_ADDRESS_LINE_2 | address | 30% | 238 | text place |  |
| CITY | city | 100% | 661 | text place |  |
| LOCATION_1 | facility_site | 100% | 1,020 | text place |  |
| LOCATION_NAME | facility_site | 100% | 434 | text place |  |
| STATE | state | 100% | 51 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 870 | clean ZIP |  |
### HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES  (12,456,456 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 3,069 | text place |  |
| STATE | state | 100% | 56 | clean 2-letter state |  |
### HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER  (381,228 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RFRG_PRVDR_CITY | city | 100% | 9,566 | text place |  |
| RFRG_PRVDR_CNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| RFRG_PRVDR_STATE_FIPS | fips | 100% | 60 | clean FIPS (2-digit) |  |
| RFRG_PRVDR_RUCA | metro | 100% | 22 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| RFRG_PRVDR_RUCA_DESC | metro | 100% | 15 | text place |  |
| RFRG_PRVDR_STATE_ABRVTN | state | 100% | 60 | clean 2-letter state |  |
| RFRG_PRVDR_ZIP5 | zip | 100% | 16,802 | clean ZIP |  |
### HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL  (440,670 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| SUPLR_PRVDR_CITY | city | 100% | 6,640 | text place |  |
| SUPLR_PRVDR_CNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| SUPLR_PRVDR_STATE_FIPS | fips | 100% | 55 | clean FIPS (2-digit) |  |
| SUPLR_PRVDR_RUCA | metro | 100% | 22 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| SUPLR_PRVDR_RUCA_CAT | metro | 100% | 3 | text place |  |
| SUPLR_PRVDR_RUCA_DESC | metro | 100% | 15 | text place |  |
| SUPLR_PRVDR_STATE_ABRVTN | state | 100% | 55 | clean 2-letter state |  |
| SUPLR_PRVDR_ZIP5 | zip | 100% | 12,792 | clean ZIP |  |
### HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER  (3,044 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RNDRNG_PRVDR_CITY | city | 100% | 1,846 | text place |  |
| RNDRNG_PRVDR_STATE_FIPS | fips | 100% | 51 | clean FIPS (2-digit) |  |
| RNDRNG_PRVDR_RUCA | metro | 100% | 19 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| RNDRNG_PRVDR_RUCA_DESC | metro | 100% | 15 | text place |  |
| RNDRNG_PRVDR_STATE_ABRVTN | state | 100% | 51 | clean 2-letter state |  |
| RNDRNG_PRVDR_ZIP5 | zip | 100% | 2,863 | clean ZIP |  |
### HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE  (145,879 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RNDRNG_PRVDR_CITY | city | 100% | 1,782 | text place |  |
| RNDRNG_PRVDR_STATE_FIPS | fips | 100% | 51 | clean FIPS (2-digit) |  |
| RNDRNG_PRVDR_RUCA | metro | 100% | 19 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| RNDRNG_PRVDR_RUCA_DESC | metro | 100% | 15 | text place |  |
| RNDRNG_PRVDR_STATE_ABRVTN | state | 100% | 51 | clean 2-letter state |  |
| RNDRNG_PRVDR_ZIP5 | zip | 100% | 2,752 | clean ZIP |  |
### HEALTH__FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE  (116,182 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RNDRNG_PRVDR_CITY | city | 100% | 1,843 | text place |  |
| RNDRNG_PRVDR_STATE_FIPS | fips | 100% | 50 | clean FIPS (2-digit) |  |
| RNDRNG_PRVDR_RUCA | metro | 100% | 18 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| RNDRNG_PRVDR_RUCA_DESC | metro | 100% | 14 | text place |  |
| RNDRNG_PRVDR_STATE_ABRVTN | state | 100% | 50 | clean 2-letter state |  |
| RNDRNG_PRVDR_ZIP5 | zip | 100% | 2,863 | clean ZIP |  |
### HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER  (1,296,739 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RNDRNG_PRVDR_CITY | city | 100% | 12,678 | text place |  |
| RNDRNG_PRVDR_CNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| RNDRNG_PRVDR_STATE_FIPS | fips | 100% | 61 | clean FIPS (2-digit) |  |
| RNDRNG_PRVDR_RUCA | metro | 100% | 22 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| RNDRNG_PRVDR_RUCA_DESC | metro | 100% | 15 | text place |  |
| RNDRNG_PRVDR_STATE_ABRVTN | state | 100% | 62 | clean 2-letter state |  |
| RNDRNG_PRVDR_ZIP5 | zip | 100% | 21,267 | clean ZIP |  |
### HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI  (9,781,673 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RNDRNG_PRVDR_CITY | city | 100% | 12,475 | text place |  |
| RNDRNG_PRVDR_CNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| PLACE_OF_SRVC | facility_site | 100% | 2 | text place |  |
| RNDRNG_PRVDR_STATE_FIPS | fips | 100% | 61 | clean FIPS (2-digit) |  |
| RNDRNG_PRVDR_RUCA | metro | 100% | 22 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| RNDRNG_PRVDR_RUCA_DESC | metro | 100% | 15 | text place |  |
| RNDRNG_PRVDR_STATE_ABRVTN | state | 100% | 62 | clean 2-letter state |  |
| RNDRNG_PRVDR_ZIP5 | zip | 100% | 20,976 | clean ZIP |  |
### HEALTH__FED_CMS_MEDICARE_PROVIDER  (1,296,739 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RNDRNG_PRVDR_CITY | city | 100% | 12,678 | text place |  |
| RNDRNG_PRVDR_CNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| RNDRNG_PRVDR_STATE_FIPS | fips | 100% | 61 | clean FIPS (2-digit) |  |
| RNDRNG_PRVDR_RUCA | metro | 100% | 22 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| RNDRNG_PRVDR_RUCA_DESC | metro | 100% | 15 | text place |  |
| RNDRNG_PRVDR_STATE_ABRVTN | state | 100% | 62 | clean 2-letter state |  |
| RNDRNG_PRVDR_ZIP5 | zip | 100% | 21,267 | clean ZIP |  |
### HEALTH__FED_CMS_NPPES  (9,606,683 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PROVIDER_BUSINESS_MAILING_ADDRESS_FAX_NUMBER | address | 34% | 1,186,604 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| PROVIDER_BUSINESS_MAILING_ADDRESS_TELEPHONE_NUMBER | address | 81% | 3,932,547 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_FAX_NUMBER | address | 37% | 1,339,375 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_TELEPHONE_NUMBER | address | 96% | 3,732,697 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS | address | 96% | 3,828,276 | text place |  |
| PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS | address | 96% | 2,970,929 | text place |  |
| PROVIDER_SECOND_LINE_BUSINESS_MAILING_ADDRESS | address | 13% | 225,375 | text place |  |
| PROVIDER_SECOND_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS | address | 14% | 245,831 | text place |  |
| PROVIDER_BUSINESS_MAILING_ADDRESS_CITY_NAME | city | 96% | 28,020 | text place |  |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME | city | 96% | 28,327 | text place |  |
| PROVIDER_BUSINESS_MAILING_ADDRESS_COUNTRY_CODE_IF_OUTSIDE_U_S | country | 96% | 139 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_COUNTRY_CODE_IF_OUTSIDE_U_S | country | 96% | 143 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| OTHER_PROVIDER_IDENTIFIER_STATE_1 | state | 15% | 59 | clean 2-letter state |  |
| OTHER_PROVIDER_IDENTIFIER_STATE_10 | state | 0% | 57 | clean 2-letter state | only 0.1% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_11 | state | 0% | 58 | clean 2-letter state | only 0.1% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_12 | state | 0% | 57 | clean 2-letter state | only 0.1% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_13 | state | 0% | 55 | clean 2-letter state | only 0.1% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_14 | state | 0% | 56 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_15 | state | 0% | 53 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_16 | state | 0% | 52 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_17 | state | 0% | 52 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_18 | state | 0% | 51 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_19 | state | 0% | 52 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_2 | state | 5% | 59 | clean 2-letter state | only 4.8% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_20 | state | 0% | 51 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_21 | state | 0% | 50 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_22 | state | 0% | 48 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_23 | state | 0% | 49 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_24 | state | 0% | 49 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_25 | state | 0% | 49 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_26 | state | 0% | 47 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_27 | state | 0% | 45 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_28 | state | 0% | 43 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_29 | state | 0% | 46 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_3 | state | 2% | 59 | clean 2-letter state | only 2.2% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_30 | state | 0% | 46 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_31 | state | 0% | 43 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_32 | state | 0% | 46 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_33 | state | 0% | 41 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_34 | state | 0% | 39 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_35 | state | 0% | 38 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_36 | state | 0% | 40 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_37 | state | 0% | 33 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_38 | state | 0% | 34 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_39 | state | 0% | 33 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_4 | state | 1% | 59 | clean 2-letter state | only 1.2% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_40 | state | 0% | 32 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_41 | state | 0% | 29 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_42 | state | 0% | 26 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_43 | state | 0% | 29 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_44 | state | 0% | 27 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_45 | state | 0% | 27 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_46 | state | 0% | 25 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_47 | state | 0% | 23 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_48 | state | 0% | 19 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_49 | state | 0% | 15 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_5 | state | 1% | 59 | clean 2-letter state | only 0.7% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_50 | state | 0% | 12 | clean 2-letter state | only 0.0% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_6 | state | 1% | 58 | clean 2-letter state | only 0.5% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_7 | state | 0% | 58 | clean 2-letter state | only 0.4% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_8 | state | 0% | 56 | clean 2-letter state | only 0.3% of rows filled |
| OTHER_PROVIDER_IDENTIFIER_STATE_9 | state | 0% | 58 | clean 2-letter state | only 0.2% of rows filled |
| PROVIDER_BUSINESS_MAILING_ADDRESS_STATE_NAME | state | 96% | 1,166 | clean 2-letter state |  |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME | state | 96% | 1,089 | clean 2-letter state |  |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_1 | state | 64% | 61 | clean 2-letter state |  |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_10 | state | 0% | 54 | clean 2-letter state | only 0.0% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_11 | state | 0% | 54 | clean 2-letter state | only 0.0% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_12 | state | 0% | 54 | clean 2-letter state | only 0.0% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_13 | state | 0% | 54 | clean 2-letter state | only 0.0% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_14 | state | 0% | 54 | clean 2-letter state | only 0.0% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_15 | state | 0% | 53 | clean 2-letter state | only 0.0% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_2 | state | 13% | 61 | clean 2-letter state |  |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_3 | state | 4% | 59 | clean 2-letter state | only 3.7% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_4 | state | 1% | 58 | clean 2-letter state | only 1.2% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_5 | state | 0% | 57 | clean 2-letter state | only 0.5% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_6 | state | 0% | 56 | clean 2-letter state | only 0.2% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_7 | state | 0% | 57 | clean 2-letter state | only 0.1% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_8 | state | 0% | 56 | clean 2-letter state | only 0.1% of rows filled |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_9 | state | 0% | 54 | clean 2-letter state | only 0.1% of rows filled |
| PROVIDER_BUSINESS_MAILING_ADDRESS_POSTAL_CODE | zip | 96% | 3,216,563 | clean ZIP |  |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE | zip | 96% | 2,079,881 | clean ZIP |  |
### HEALTH__FED_CMS_NURSING_HOME  (14,700 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 100% | 14,755 | text place |  |
| CITY | city | 100% | 5,113 | text place |  |
| LATITUDE | coordinates | 100% | 13,960 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 10,618 | clean coordinate |  |
| LONG_STAY_QM_RATING | coordinates | 96% | 5 | clean coordinate |  |
| COUNTY_PARISH | county | 100% | 1,712 | county name |  |
| PROVIDER_SSA_COUNTY_CODE | county | 98% | 302 | county code |  |
| LOCATION | facility_site | 100% | 14,859 | text place |  |
| COUNTY_FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| URBAN | metro | 100% | 2 | text place |  |
| STATE | state | 100% | 53 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 9,229 | clean ZIP |  |
### HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES  (418,479 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PROVIDER_ADDRESS | address | 100% | 14,720 | text place |  |
| CITY_TOWN | city | 100% | 5,099 | text place |  |
| LOCATION | facility_site | 100% | 14,790 | text place |  |
| STATE | state | 100% | 53 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 9,193 | clean ZIP |  |
### HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES  (200,030 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PROVIDER_ADDRESS | address | 100% | 13,990 | text place |  |
| CITY_TOWN | city | 100% | 4,952 | text place |  |
| LOCATION | facility_site | 100% | 14,036 | text place |  |
| STATE | state | 100% | 53 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 8,876 | clean ZIP |  |
### HEALTH__FED_CMS_NURSING_HOME_PENALTIES  (16,180 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PROVIDER_ADDRESS | address | 100% | 6,849 | text place |  |
| CITY_TOWN | city | 100% | 3,167 | text place |  |
| LOCATION | facility_site | 100% | 6,924 | text place |  |
| STATE | state | 100% | 53 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 5,254 | clean ZIP |  |
### HEALTH__FED_CMS_OPEN_PAYMENTS  (15,385,047 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RECIPIENT_CITY | city | 100% | 13,823 | text place |  |
| APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_STATE | state | 100% | 49 | clean 2-letter state |  |
| RECIPIENT_STATE | state | 100% | 59 | clean 2-letter state |  |
| RECIPIENT_ZIP_CODE | zip | 100% | 268,860 | clean ZIP |  |
### HEALTH__FED_CMS_OPEN_PAYMENTS_2022  (13,306,564 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RECIPIENT_CITY | city | 100% | 13,773 | text place |  |
| APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_STATE | state | 100% | 47 | clean 2-letter state |  |
| RECIPIENT_STATE | state | 100% | 57 | clean 2-letter state |  |
| RECIPIENT_ZIP_CODE | zip | 100% | 258,425 | clean ZIP |  |
### HEALTH__FED_CMS_OPEN_PAYMENTS_2023  (14,700,786 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RECIPIENT_CITY | city | 100% | 13,796 | text place |  |
| APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_STATE | state | 100% | 47 | clean 2-letter state |  |
| RECIPIENT_STATE | state | 100% | 59 | clean 2-letter state |  |
| RECIPIENT_ZIP_CODE | zip | 100% | 277,259 | clean ZIP |  |
### HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT  (1,697,025 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 578,673 | text place |  |
| ADDRESS_LINE_2 | address | 23% | 84,018 | text place |  |
| CITY | city | 100% | 13,680 | text place |  |
| COUNTRY_NAME | country | 100% | 45 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| LICENSE_STATE_CODE_1 | state | 100% | 60 | clean 2-letter state |  |
| LICENSE_STATE_CODE_2 | state | 41% | 60 | clean 2-letter state |  |
| LICENSE_STATE_CODE_3 | state | 16% | 60 | clean 2-letter state |  |
| LICENSE_STATE_CODE_4 | state | 7% | 59 | clean 2-letter state |  |
| LICENSE_STATE_CODE_5 | state | 3% | 58 | clean 2-letter state | only 3.4% of rows filled |
| PROVINCE_NAME | state | 0% | 173 | mixed / not a state | only 9% are 2-letter US codes (foreign provinces, money, or free text); only 0.0% of rows filled |
| STATE | state | 100% | 59 | clean 2-letter state |  |
| ZIPCODE | zip | 100% | 391,910 | clean ZIP |  |
### HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS  (1,558 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 1,536 | text place |  |
| ADDRESS_LINE_2 | address | 36% | 341 | text place |  |
| CITY | city | 100% | 930 | text place |  |
| STATE | state | 100% | 50 | clean 2-letter state |  |
| ZIP | zip | 100% | 1,526 | clean ZIP |  |
### HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS  (57,209 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FIRST_LINE_STREET_ADDRESS | address | 100% | 37,379 | text place |  |
| SECOND_LINE_STREET_ADDRESS | address | 54% | 5,910 | text place |  |
| CITY_NAME | city | 100% | 4,650 | text place |  |
| STATE_CODE | state | 100% | 55 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 35,962 | clean ZIP |  |
### HEALTH__FED_CMS_PARTD_PRESCRIBERS  (25,869,521 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PRESCRIBER_CITY | city | 100% | 11,944 | text place |  |
| PRESCRIBER_STATE_FIPS | fips | 100% | 61 | clean FIPS (2-digit) |  |
| PRESCRIBER_STATE | state | 100% | 61 | clean 2-letter state |  |
### HEALTH__FED_CMS_PART_D_PRESCRIBERS  (1,416,883 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PRSCRBR_CITY | city | 100% | 12,695 | text place |  |
| PRSCRBR_CNTRY | country | 100% | 36 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| PRSCRBR_STATE_FIPS | fips | 100% | 55 | clean FIPS (2-digit) |  |
| PRSCRBR_RUCA | metro | 100% | 22 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| PRSCRBR_RUCA_DESC | metro | 100% | 15 | text place |  |
| PRSCRBR_STATE_ABRVTN | state | 100% | 62 | clean 2-letter state |  |
| PRSCRBR_ZIP5 | zip | 100% | 21,041 | clean ZIP |  |
### HEALTH__FED_CMS_POS_OTHER  (44,429 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY_NAME | city | 100% | 7,755 | text place |  |
| SSA_CNTY_CD | county | 97% | 327 | mixed county |  |
| FIPS_CNTY_CD | fips | 99% | 320 | FIPS with leading zeros lost | 59% have a FIPS length; modal length 2 -- pad before joining |
| FIPS_STATE_CD | fips | 99% | 55 | clean FIPS (2-digit) |  |
| CBSA_CD | metro | 99% | 460 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| CBSA_URBN_RRL_IND | metro | 99% | 2 | text place |  |
| SSA_STATE_CD | state | 100% | 58 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| STATE_CD | state | 100% | 58 | clean 2-letter state |  |
| STATE_RGN_CD | state | 100% | 110 | mixed / not a state | only 3% are 2-letter US codes (foreign provinces, money, or free text) |
| ZIP_CD | zip | 99% | 13,707 | clean ZIP |  |
### HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE  (503,917 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PRACTICE_STATE_OR_US_TERRITORY | state | 100% | 55 | clean 2-letter state |  |
### HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS  (5,530 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 5,401 | text place |  |
| ADDRESS_LINE_2 | address | 21% | 476 | text place |  |
| CITY | city | 100% | 2,949 | text place |  |
| ENROLLMENT_STATE | state | 100% | 45 | clean 2-letter state |  |
| INCORPORATION_STATE | state | 65% | 46 | clean 2-letter state |  |
| STATE | state | 100% | 45 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 5,409 | clean ZIP |  |
### HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS  (14,425 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 14,654 | text place |  |
| ADDRESS_LINE_2 | address | 4% | 585 | text place | only 4.3% of rows filled |
| CITY | city | 100% | 5,098 | text place |  |
| ENROLLMENT_STATE | state | 100% | 53 | clean 2-letter state |  |
| INCORPORATION_STATE | state | 63% | 52 | clean 2-letter state |  |
| STATE | state | 100% | 53 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 14,108 | clean ZIP |  |
### HEALTH__FED_DEA_ARCOS  (178,598,026 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| BUYER_CITY | city | 100% | 10,550 | text place |  |
| REPORTER_CITY | city | 100% | 420 | text place |  |
| BUYER_COUNTY | county | 100% | 1,871 | county name |  |
| REPORTER_COUNTY | county | 100% | 251 | county name |  |
| BUYER_STATE | state | 100% | 59 | clean 2-letter state |  |
| REPORTER_STATE | state | 100% | 50 | clean 2-letter state |  |
| BUYER_ZIP | zip | 100% | 17,623 | mixed / not a ZIP | only 94% look like ZIPs |
| REPORTER_ZIP | zip | 100% | 512 | mixed / not a ZIP | only 93% look like ZIPs |
### HEALTH__FED_FDA_DEVICE_510K  (175,686 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_1 | address | 100% | 34,578 | text place |  |
| ADDRESS_2 | address | 18% | 7,419 | text place |  |
| CITY | city | 100% | 8,459 | text place |  |
| COUNTRY_CODE | country | 100% | 93 | country code |  |
| STATE | state | 83% | 55 | clean 2-letter state |  |
| POSTAL_CODE | zip | 98% | 12,916 | mixed / not a ZIP | only 90% look like ZIPs |
| ZIP_CODE | zip | 98% | 12,910 | mixed / not a ZIP | only 90% look like ZIPs |
### HEALTH__FED_FDA_DEVICE_ENFORCEMENT  (39,635 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_1 | address | 100% | 3,140 | text place |  |
| ADDRESS_2 | address | 6% | 357 | text place |  |
| CITY | city | 100% | 1,361 | text place |  |
| COUNTRY | country | 100% | 38 | country name |  |
| STATE | state | 91% | 52 | clean 2-letter state |  |
| POSTAL_CODE | zip | 91% | 2,236 | clean ZIP |  |
### HEALTH__FED_FDA_DEVICE_PMA  (56,853 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_1 | address | 100% | 869 | text place |  |
| STREET_2 | address | 16% | 174 | text place |  |
| CITY | city | 100% | 488 | text place |  |
| STATE | state | 95% | 37 | clean 2-letter state |  |
| ZIP | zip | 99% | 615 | clean ZIP |  |
| ZIP_EXT | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
### HEALTH__FED_FDA_DRUG_ENFORCEMENT  (17,876 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_1 | address | 100% | 1,576 | text place |  |
| ADDRESS_2 | address | 10% | 191 | text place |  |
| CITY | city | 100% | 870 | text place |  |
| COUNTRY | country | 100% | 24 | country name |  |
| STATE | state | 94% | 50 | clean 2-letter state |  |
| POSTAL_CODE | zip | 94% | 1,379 | clean ZIP |  |
### HEALTH__FED_FDA_ESTABLISHMENT_REG  (263,374 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 24,965 | text place |  |
| ADDRESS_LINE_2 | address | 24% | 5,237 | text place |  |
| CITY | city | 100% | 8,687 | text place |  |
| ISO_COUNTRY_CODE | country | 100% | 108 | country code |  |
| STATE_CODE | state | 46% | 52 | clean 2-letter state |  |
| POSTAL_CODE | zip | 54% | 9,260 | mixed / not a ZIP | only 31% look like ZIPs |
### HEALTH__FED_FDA_FAERS_DEMO  (5,811,086 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| OCCR_COUNTRY | country | 23% | 186 | country code |  |
| REPORTER_COUNTRY | country | 92% | 401 | country name |  |
### HEALTH__FED_FDA_MAUDE  (2,743,561 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| MANUFACTURER_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| MANUFACTURER_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| MANUFACTURER_STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
### HEALTH__FED_HHS_OIG_LEIE  (83,369 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 100% | 76,704 | text place |  |
| CITY | city | 100% | 10,060 | text place |  |
| STATE | state | 100% | 57 | clean 2-letter state |  |
| ZIP | zip | 100% | 18,375 | clean ZIP |  |
### HEALTH__FED_HRSA_HPSA_PRIMARY_CARE  (79,158 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| HPSA_ADDRESS | address | 9% | 6,573 | text place |  |
| HPSA_CITY | city | 10% | 3,444 | text place |  |
| LATITUDE | coordinates | 10% | 7,410 | clean coordinate |  |
| LONGITUDE | coordinates | 10% | 7,340 | clean coordinate |  |
| COMMON_COUNTY_NAME | county | 100% | 3,212 | county name |  |
| COUNTY_EQUIVALENT_NAME | county | 100% | 1,985 | county name |  |
| US_MEXICO_BORDER_COUNTY_INDICATOR | county | 100% | 3 | county name |  |
| HPSA_GEOGRAPHY_ID | facility_site | 100% | 39,929 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| COMMON_STATE_COUNTY_FIPS_CODE | fips | 100% | 3,268 | clean FIPS (5-digit) |  |
| COMMON_STATE_FIPS_CODE | fips | 100% | 59 | clean FIPS (2-digit) |  |
| COUNTY_FIPS_CODE | fips | 100% | 346 | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining |
| PRIMARY_STATE_FIPS_CODE | fips | 100% | 59 | clean FIPS (2-digit) |  |
| STATE_COUNTY_FIPS_CODE | fips | 100% | 3,269 | clean FIPS (5-digit) |  |
| STATE_FIPS_CODE | fips | 100% | 59 | clean FIPS (2-digit) |  |
| METROPOLITAN_INDICATOR | metro | 35% | 4 | text place |  |
| METROPOLITAN_INDICATOR_CODE | metro | 35% | 4 | text place |  |
| COMMON_REGION_NAME | region | 100% | 11 | text place |  |
| COMMON_STATE_ABBREVIATION | state | 100% | 60 | clean 2-letter state |  |
| COMMON_STATE_NAME | state | 100% | 60 | state names (not codes) |  |
| COMPONENT_STATE_ABBREVIATION | state | 90% | 59 | clean 2-letter state |  |
| PRIMARY_STATE_ABBREVIATION | state | 100% | 60 | clean 2-letter state |  |
| PRIMARY_STATE_NAME | state | 100% | 60 | state names (not codes) |  |
| STATE_ABBREVIATION | state | 100% | 60 | clean 2-letter state |  |
| STATE_NAME | state | 100% | 60 | state names (not codes) |  |
| COMMON_POSTAL_CODE | zip | 10% | 4,851 | clean ZIP |  |
| HPSA_POSTAL_CODE | zip | 10% | 6,639 | clean ZIP |  |
### HEALTH__FED_HRSA_NPDB  (1,911,185 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| HOME_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| WORK_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| HOME_STATE | state | 71% | 61 | clean 2-letter state |  |
| LICENSE_STATE | state | 92% | 58 | clean 2-letter state |  |
| WORK_STATE | state | 43% | 61 | clean 2-letter state |  |
### HEALTH__FED_HRSA_SHORTAGE_AREAS  (165,531 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| HPSA_ADDRESS | address | 13% | 7,201 | text place |  |
| HPSA_CITY | city | 13% | 3,536 | text place |  |
| LATITUDE | coordinates | 14% | 8,302 | clean coordinate |  |
| LONGITUDE | coordinates | 14% | 8,377 | clean coordinate |  |
| COMMON_COUNTY_NAME | county | 100% | 3,283 | county name |  |
| COUNTY_EQUIVALENT_NAME | county | 100% | 2,011 | county name |  |
| COUNTY_OR_COUNTY_EQUIVALENT_FEDERAL_INFORMATION_PROCESSING_STANDARD_CODE | county | 100% | 358 | county code |  |
| STATE_AND_COUNTY_FEDERAL_INFORMATION_PROCESSING_STANDARD_CODE | county | 100% | 3,326 | county code |  |
| U_S_MEXICO_BORDER_COUNTY_INDICATOR | county | 100% | 3 | county name |  |
| HPSA_GEOGRAPHY_IDENTIFICATION_NUMBER | facility_site | 100% | 47,035 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| COMMON_STATE_COUNTY_FIPS_CODE | fips | 100% | 3,324 | clean FIPS (5-digit) |  |
| COMMON_STATE_FIPS_CODE | fips | 100% | 59 | clean FIPS (2-digit) |  |
| PRIMARY_STATE_FIPS_CODE | fips | 100% | 59 | clean FIPS (2-digit) |  |
| STATE_FIPS_CODE | fips | 100% | 59 | clean FIPS (2-digit) |  |
| HPSA_METROPOLITAN_INDICATOR_CODE | metro | 27% | 4 | text place |  |
| METROPOLITAN_INDICATOR | metro | 27% | 4 | text place |  |
| COMMON_REGION_NAME | region | 100% | 11 | text place |  |
| COMMON_STATE_ABBREVIATION | state | 100% | 60 | clean 2-letter state |  |
| COMMON_STATE_NAME | state | 100% | 60 | state names (not codes) |  |
| HPSA_COMPONENT_STATE_ABBREVIATION | state | 86% | 59 | clean 2-letter state |  |
| PRIMARY_STATE_ABBREVIATION | state | 100% | 60 | clean 2-letter state |  |
| PRIMARY_STATE_NAME | state | 100% | 60 | state names (not codes) |  |
| STATE_ABBREVIATION | state | 100% | 60 | clean 2-letter state |  |
| STATE_NAME | state | 100% | 60 | state names (not codes) |  |
| COMMON_POSTAL_CODE | zip | 13% | 5,082 | clean ZIP |  |
| HPSA_POSTAL_CODE | zip | 13% | 7,160 | clean ZIP |  |
### HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES  (19,038 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| HEALTH_CENTER_STREET_ADDRESS | address | 100% | 1,516 | text place |  |
| SITE_ADDRESS | address | 99% | 17,373 | text place |  |
| SITE_WEB_ADDRESS | address | 54% | 2,793 | text place |  |
| HEALTH_CENTER_CITY | city | 100% | 968 | text place |  |
| SITE_CITY | city | 99% | 4,395 | text place |  |
| CONGRESSIONAL_DISTRICT_CODE | cong_district | 100% | 449 | text place |  |
| CONGRESSIONAL_DISTRICT_NAME | cong_district | 99% | 443 | text place |  |
| CONGRESSIONAL_DISTRICT_NUMBER | cong_district | 97% | 56 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| LATITUDE | coordinates | 99% | 17,242 | clean coordinate |  |
| LONGITUDE | coordinates | 99% | 16,709 | clean coordinate |  |
| COMPLETE_COUNTY_NAME | county | 100% | 1,516 | county name |  |
| COUNTY_DESCRIPTION | county | 99% | 11 | county name |  |
| COUNTY_EQUIVALENT_NAME | county | 99% | 1,488 | county name |  |
| US_MEXICO_BORDER_COUNTY_INDICATOR | county | 99% | 2 | county name |  |
| FQHC_SITE_MEDICARE_BILLING_NUMBER | facility_site | 45% | 8,438 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| FQHC_SITE_NPI_NUMBER | facility_site | 32% | 6,074 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| LOCATION_SETTING_DESCRIPTION | facility_site | 97% | 8 | text place |  |
| LOCATION_SETTING_ID | facility_site | 97% | 8 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| LOCATION_TYPE_DESCRIPTION | facility_site | 100% | 3 | text place |  |
| LOCATION_TYPE_ID | facility_site | 100% | 3 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| SITE_ADDED_TO_SCOPE_DATE | facility_site | 100% | 4,808 | not a place (dates) | name-scan false hit |
| SITE_NAME | facility_site | 100% | 18,355 | text place |  |
| SITE_TELEPHONE_NUMBER | facility_site | 100% | 11,457 | text place |  |
| SITE_TYPE_DESCRIPTION | facility_site | 100% | 3 | text place |  |
| SITE_TYPE_ID | facility_site | 100% | 3 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_COUNTY_FIPS_CODE | fips | 99% | 2,318 | clean FIPS (5-digit) |  |
| STATE_FIPS_CODE | fips | 99% | 59 | clean FIPS (2-digit) |  |
| STATE_FIPS_CONGRESSIONAL_DISTRICT_CODE | fips | 99% | 444 | FIPS with leading zeros lost | 0% have a FIPS length; modal length 4 -- pad before joining |
| HHS_REGION_CODE | region | 99% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| HHS_REGION_NAME | region | 99% | 10 | text place |  |
| HEALTH_CENTER_STATE | state | 100% | 59 | clean 2-letter state |  |
| SITE_STATE_ABBREVIATION | state | 99% | 60 | clean 2-letter state |  |
| STATE_NAME | state | 100% | 60 | state names (not codes) |  |
| HEALTH_CENTER_ZIP_CODE | zip | 100% | 1,530 | clean ZIP |  |
| SITE_POSTAL_CODE | zip | 99% | 16,338 | clean ZIP |  |
### HEALTH__FED_IHS_FACILITIES  (1,006 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET | address | 95% | 888 | text place |  |
| CITY | city | 100% | 729 | text place |  |
| LATITUDE | coordinates | 100% | 955 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 945 | clean coordinate |  |
| LOCATION_TYPE | facility_site | 100% | 6 | text place |  |
| STATE | state | 100% | 37 | clean 2-letter state |  |
| ZIP | zip | 100% | 720 | clean ZIP |  |
### HEALTH__FED_IHS_SCB_FACILITY  (8,733 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LOCATION_TYPE | facility_site | 32% | 7 | text place |  |
### HEALTH__FED_NLM_DAILYMED_SPL_SETID_MAP  (158,452 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ZIP_FILE_NAME | zip | 100% | 161,574 | foreign postal code | only 0% look like US ZIPs |
### HEALTH__FED_NURSINGHOME411  (14,713 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PROVIDER_ADDRESS | address | 100% | 14,803 | text place |  |
| CITY_TOWN | city | 100% | 5,115 | text place |  |
| LATITUDE | coordinates | 100% | 13,955 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 10,612 | clean coordinate |  |
| COUNTY_PARISH | county | 100% | 1,710 | county name |  |
| LOCATION | facility_site | 100% | 14,870 | text place |  |
| CMS_REGION_NUMBER | region | 100% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE | state | 100% | 53 | clean 2-letter state |  |
### HEALTH__FED_VA_SUICIDE_STATE  (1,196 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| GEOGRAPHIC_REGION | region | 100% | 5 | text place |  |
| STATE | state | 100% | 52 | state names (not codes) |  |
### HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION  (2,040 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 54 | mixed / not a state | only 94% are 2-letter US codes (foreign provinces, money, or free text) |
### HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN  (11,521 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| SLA1PORT | airport_port | 69% | 119 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### HISTORY__FED_DENSHO_DDR  (25 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
### HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC  (36,108 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| SLA1PORT | airport_port | 71% | 264 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### HISTORY__FED_WPA_SLAVE_NARRATIVES  (100 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| STATE | state | 100% | 17 | state names (not codes) |  |
### HOUSING__FED_CFPB_HMDA  (28,301 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CENSUS_TRACT | census_tract | 98% | 207 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | census_tract | 100% | 53 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_MINORITY_POPULATION_PERCENT | census_tract | 100% | 200 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_ONE_TO_FOUR_FAMILY_HOMES | census_tract | 100% | 193 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_OWNER_OCCUPIED_UNITS | census_tract | 100% | 184 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_POPULATION | census_tract | 100% | 201 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_TO_MSA_INCOME_PERCENTAGE | census_tract | 100% | 179 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| COUNTY_CODE | county | 98% | 1 | constant | one value for the whole table |
| DERIVED_MSA_MD | metro | 98% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | metro | 100% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_CODE | state | 100% | 1 | constant | one value for the whole table |
### HOUSING__FED_CFPB_HMDA_DC_ONLY  (28,301 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CENSUS_TRACT | census_tract | 98% | 207 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | census_tract | 61% | 54 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_MINORITY_POPULATION_PERCENT | census_tract | 98% | 192 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_ONE_TO_FOUR_FAMILY_HOMES | census_tract | 97% | 192 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_OWNER_OCCUPIED_UNITS | census_tract | 98% | 184 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_POPULATION | census_tract | 98% | 202 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_TO_MSA_INCOME_PERCENTAGE | census_tract | 97% | 177 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| COUNTY_CODE | county | 98% | 1 | constant | one value for the whole table |
| DERIVED_MSA_MD | metro | 98% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | metro | 98% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_CODE | state | 100% | 1 | constant | one value for the whole table |
### HOUSING__FED_CFPB_HMDA_HISTORIC  (19,136,434 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CENSUS_TRACT_NUMBER | census_tract | 100% | 24,123 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_TO_MSAMD_INCOME | census_tract | 100% | 391 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| COUNTY_CODE | county | 100% | 326 | mixed county |  |
| COUNTY_NAME | county | 100% | 1,975 | county name |  |
| STATE_ABBR | state | 100% | 53 | clean 2-letter state |  |
| STATE_CODE | state | 100% | 53 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| STATE_NAME | state | 100% | 53 | state names (not codes) |  |
### HOUSING__FED_CFPB_HMDA_LAR  (17,474 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CENSUS_TRACT | census_tract | 99% | 203 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | census_tract | 62% | 53 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_MINORITY_POPULATION_PERCENT | census_tract | 100% | 196 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_ONE_TO_FOUR_FAMILY_HOMES | census_tract | 98% | 189 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_OWNER_OCCUPIED_UNITS | census_tract | 99% | 183 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_POPULATION | census_tract | 99% | 198 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_TO_MSA_INCOME_PERCENTAGE | census_tract | 100% | 177 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| COUNTY_CODE | county | 99% | 1 | constant | one value for the whole table |
| DERIVED_MSA_MD | metro | 99% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | metro | 99% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_CODE | state | 100% | 1 | constant | one value for the whole table |
### HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS  (26,250,920 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DAMAGED_CITY | city | 100% | 40,698 | text place |  |
| RENTAL_RESOURCE_CITY | city | 0% | 7,726 | text place | only 0.4% of rows filled |
| COUNTY | county | 100% | 2,055 | county name |  |
| CURRENT_LOCATION | facility_site | 100% | 16 | text place |  |
| HIGH_WATER_LOCATION | facility_site | 14% | 9 | text place |  |
| CENSUS_GEOID | fips | 74% | 230,916 | mixed / not FIPS | only 0% have a FIPS length; modal length 12 |
| FIPS | fips | 74% | 3,379 | clean FIPS (5-digit) |  |
| DAMAGED_STATE_ABBREVIATION | state | 100% | 57 | clean 2-letter state |  |
| RENTAL_RESOURCE_STATE_ABBREV | state | 0% | 57 | clean 2-letter state | only 0.4% of rows filled |
| DAMAGED_ZIP_CODE | zip | 100% | 33,727 | clean ZIP |  |
| RENTAL_RESOURCE_ZIP_CODE | zip | 0% | 10,431 | clean ZIP | only 0.4% of rows filled |
### HOUSING__FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK  (25,122 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY | county | 100% | 2,525 | county name |  |
| STATE | state | 100% | 56 | clean 2-letter state |  |
### HOUSING__FED_FHFA_HPI  (184,807 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PLACE_ID | facility_site | 100% | 467 | text place |  |
| PLACE_NAME | facility_site | 100% | 472 | text place |  |
### HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS  (35,601 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STD_ADDR | address | 96% | 27,658 | text place |  |
| STD_CITY | city | 100% | 5,645 | text place |  |
| LATITUDE | coordinates | 100% | 25,227 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 26,241 | clean coordinate |  |
| PLACE | facility_site | 95% | 6,279 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| CBSA | metro | 89% | 919 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE | state | 100% | 56 | clean 2-letter state |  |
| STD_ZIP5 | zip | 100% | 10,426 | mixed / not a ZIP | only 86% look like ZIPs |
### HOUSING__FED_HUD_DATA  (71 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| ZIP | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
### HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT  (61,647 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PROPERTY_CITY | city | 100% | 7,265 | text place |  |
| PROPERTY_COUNTY | county | 100% | 1,621 | county name |  |
| PROPERTY_STATE | state | 100% | 53 | clean 2-letter state |  |
| PROPERTY_ZIP | zip | 100% | 13,103 | clean ZIP |  |
### HOUSING__FED_HUD_MF_FIRM_COMMITMENTS  (25,557 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PROJECT_CITY | city | 100% | 3,941 | text place |  |
| PROJECT_STATE | state | 100% | 53 | clean 2-letter state |  |
### HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES  (3,787 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_TYPE | address | 94% | 4 | text place |  |
| HA_EMAIL_ADDRESS | address | 97% | 3,415 | text place |  |
| STD_ADDRESS | address | 94% | 3,451 | text place |  |
| CENSUS_TRACT | census_tract | 100% | 1,801 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRACT_LEVEL_KEY | census_tract | 100% | 3,575 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STD_CITY | city | 100% | 2,690 | text place |  |
| LATITUDE | coordinates | 100% | 3,704 | clean coordinate |  |
| LAT_GEOCODED | coordinates | 100% | 3,669 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 3,639 | clean coordinate |  |
| LON_GEOCODED | coordinates | 100% | 3,639 | clean coordinate |  |
| COUNTY_LEVEL_KEY | county | 100% | 2,092 | county code |  |
| COUNTY_NAME | county | 100% | 1,392 | county name |  |
| CURRENT_COUNTY_NAME | county | 100% | 1,395 | county name |  |
| CURRENT_COUNTY_SUBDIVISION | county | 100% | 2,837 | county code |  |
| CURRENT_COUNTY_SUBDIVISION_NAME | county | 100% | 2,591 | county name |  |
| PLACE_CLASS_CODE | facility_site | 0% | 0 | empty | no real values (blank or sentinel only) |
| PLACE_INCORPORATED_FLAG | facility_site | 0% | 0 | empty | no real values (blank or sentinel only) |
| PLACE_LEVEL_KEY | facility_site | 99% | 3,266 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| PLACE_NAME | facility_site | 98% | 3,011 | text place |  |
| COUNTY_FIPS | fips | 100% | 259 | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining |
| CURRENT_COUNTY_FIPS | fips | 100% | 268 | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining |
| PLACE_FIPS | fips | 95% | 2,910 | clean FIPS (5-digit) |  |
| STATE_FIPS | fips | 100% | 55 | clean FIPS (2-digit) |  |
| CBSA_CODE | metro | 75% | 809 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| CBSA_NAME | metro | 75% | 817 | text place |  |
| METRO_FLAG | metro | 54% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| MSA_CODE | metro | 100% | 326 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| MSA_NAME | metro | 42% | 330 | text place |  |
| URBAN_RURAL_FLAG | metro | 99% | 2 | text place |  |
| STD_STATE | state | 100% | 55 | clean 2-letter state |  |
| STD_ZIP5 | zip | 100% | 3,543 | clean ZIP |  |
| ZCTA | zip | 99% | 3,512 | clean ZIP |  |
| ZIP_CLASS | zip | 1% | 2 | foreign postal code | only 0% look like US ZIPs; only 1.2% of rows filled |
### HOUSING__FED_MAPPING_INEQUALITY  (1,155 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 299 | text place |  |
| LAT | coordinates | 100% | 1,146 | clean coordinate |  |
| LON | coordinates | 100% | 1,146 | clean coordinate |  |
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| GEOMETRY | geometry | 100% | 1,156 | text place |  |
| STATE | state | 100% | 42 | clean 2-letter state |  |
### HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS  (13,550 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| MAIN_ADDRESS_LINE1 | address | 100% | 12,933 | text place |  |
| MAIN_ADDRESS_LINE2 | address | 6% | 662 | text place |  |
| MAIN_ADDRESS_LINE3 | address | 1% | 112 | text place | only 0.8% of rows filled |
| CITY | city | 100% | 5,362 | text place |  |
| LATITUDE | coordinates | 100% | 13,202 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 12,639 | clean coordinate |  |
| STATE_COUNTY_FIPS_CODE | fips | 100% | 2,719 | clean FIPS (5-digit) |  |
| STATE_ABBREVIATION | state | 100% | 53 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 7,509 | clean ZIP |  |
### IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS  (6,066 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 100% | 5,570 | text place |  |
| ADDRESS_LINE_2 | address | 69% | 1,166 | text place |  |
| CITY | city | 100% | 1,965 | text place |  |
| ENROLLMENT_STATE | state | 100% | 55 | clean 2-letter state |  |
| INCORPORATION_STATE | state | 80% | 55 | clean 2-letter state |  |
| STATE | state | 100% | 55 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 5,750 | clean ZIP |  |
### IMMIGRATION__FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT  (2,978,925 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_CD | state | 100% | 56 | clean 2-letter state |  |
### IMMIGRATION__FED_DHS_OHSS  (50,740 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| REGION_OR_SECTOR | region | 0% | 0 | empty | no real values (blank or sentinel only) |
### IMMIGRATION__FED_DHS_YEARBOOK  (27 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY_OF_BIRTH | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| COUNTRY_OF_LAST_RESIDENCE | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
### IMMIGRATION__FED_DOL_OFLC  (664,616 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| AGENT_ATTORNEY_ADDRESS1 | address | 67% | 6,517 | text place |  |
| AGENT_ATTORNEY_ADDRESS2 | address | 47% | 2,030 | text place |  |
| EMPLOYER_ADDRESS1 | address | 100% | 63,710 | text place |  |
| EMPLOYER_ADDRESS2 | address | 47% | 8,142 | text place |  |
| WORKSITE_ADDRESS1_1 | address | 95% | 149,398 | text place |  |
| WORKSITE_ADDRESS1_10 | address | 0% | 197 | text place | only 0.0% of rows filled |
| WORKSITE_ADDRESS1_2 | address | 9% | 26,651 | text place |  |
| WORKSITE_ADDRESS1_3 | address | 2% | 7,696 | text place | only 2.1% of rows filled |
| WORKSITE_ADDRESS1_4 | address | 1% | 2,715 | text place | only 0.6% of rows filled |
| WORKSITE_ADDRESS1_5 | address | 0% | 1,454 | text place | only 0.3% of rows filled |
| WORKSITE_ADDRESS1_6 | address | 0% | 865 | text place | only 0.2% of rows filled |
| WORKSITE_ADDRESS1_7 | address | 0% | 599 | text place | only 0.1% of rows filled |
| WORKSITE_ADDRESS1_8 | address | 0% | 412 | text place | only 0.1% of rows filled |
| WORKSITE_ADDRESS1_9 | address | 0% | 285 | text place | only 0.1% of rows filled |
| WORKSITE_ADDRESS2_1 | address | 23% | 24,164 | text place |  |
| WORKSITE_ADDRESS2_10 | address | 0% | 62 | text place | only 0.0% of rows filled |
| WORKSITE_ADDRESS2_2 | address | 3% | 5,426 | text place | only 2.7% of rows filled |
| WORKSITE_ADDRESS2_3 | address | 1% | 1,630 | text place | only 0.5% of rows filled |
| WORKSITE_ADDRESS2_4 | address | 0% | 586 | text place | only 0.2% of rows filled |
| WORKSITE_ADDRESS2_5 | address | 0% | 318 | text place | only 0.1% of rows filled |
| WORKSITE_ADDRESS2_6 | address | 0% | 201 | text place | only 0.1% of rows filled |
| WORKSITE_ADDRESS2_7 | address | 0% | 152 | text place | only 0.0% of rows filled |
| WORKSITE_ADDRESS2_8 | address | 0% | 106 | text place | only 0.0% of rows filled |
| WORKSITE_ADDRESS2_9 | address | 0% | 87 | text place | only 0.0% of rows filled |
| AGENT_ATTORNEY_CITY | city | 67% | 1,011 | text place |  |
| EMPLOYER_CITY | city | 100% | 5,033 | text place |  |
| WORKSITE_CITY_1 | city | 100% | 7,957 | text place |  |
| WORKSITE_CITY_10 | city | 0% | 150 | text place | only 0.0% of rows filled |
| WORKSITE_CITY_2 | city | 9% | 3,159 | text place |  |
| WORKSITE_CITY_3 | city | 2% | 1,927 | text place | only 2.1% of rows filled |
| WORKSITE_CITY_4 | city | 1% | 1,086 | text place | only 0.6% of rows filled |
| WORKSITE_CITY_5 | city | 0% | 746 | text place | only 0.3% of rows filled |
| WORKSITE_CITY_6 | city | 0% | 525 | text place | only 0.2% of rows filled |
| WORKSITE_CITY_7 | city | 0% | 368 | text place | only 0.1% of rows filled |
| WORKSITE_CITY_8 | city | 0% | 275 | text place | only 0.1% of rows filled |
| WORKSITE_CITY_9 | city | 0% | 215 | text place | only 0.1% of rows filled |
| AGENT_ATTORNEY_COUNTRY | country | 67% | 9 | country name |  |
| EMPLOYER_COUNTRY | country | 96% | 8 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| WORKSITE_COUNTY_1 | county | 100% | 3,880 | county name |  |
| WORKSITE_COUNTY_10 | county | 0% | 123 | county name | only 0.0% of rows filled |
| WORKSITE_COUNTY_2 | county | 9% | 1,494 | county name |  |
| WORKSITE_COUNTY_3 | county | 2% | 895 | county name | only 2.1% of rows filled |
| WORKSITE_COUNTY_4 | county | 1% | 583 | county name | only 0.6% of rows filled |
| WORKSITE_COUNTY_5 | county | 0% | 415 | county name | only 0.3% of rows filled |
| WORKSITE_COUNTY_6 | county | 0% | 333 | county name | only 0.2% of rows filled |
| WORKSITE_COUNTY_7 | county | 0% | 235 | county name | only 0.1% of rows filled |
| WORKSITE_COUNTY_8 | county | 0% | 187 | county name | only 0.1% of rows filled |
| WORKSITE_COUNTY_9 | county | 0% | 159 | county name | only 0.1% of rows filled |
| AGENT_ATTORNEY_PROVINCE | state | 4% | 162 | mixed / not a state | only 5% are 2-letter US codes (foreign provinces, money, or free text); only 4.0% of rows filled |
| AGENT_ATTORNEY_STATE | state | 64% | 54 | clean 2-letter state |  |
| EMPLOYER_PROVINCE | state | 1% | 339 | mixed / not a state | only 21% are 2-letter US codes (foreign provinces, money, or free text); only 0.8% of rows filled |
| EMPLOYER_STATE | state | 100% | 57 | clean 2-letter state |  |
| NAME_OF_HIGHEST_STATE_COURT | state | 67% | 54 | state names (not codes) |  |
| STATE_OF_HIGHEST_COURT | state | 67% | 948 | state names (not codes) |  |
| WORKSITE_STATE_1 | state | 100% | 114 | mixed / not a state | only 13% are 2-letter US codes (foreign provinces, money, or free text) |
| WORKSITE_STATE_10 | state | 0% | 44 | state names (not codes) | only 0.0% of rows filled |
| WORKSITE_STATE_2 | state | 9% | 108 | mixed / not a state | only 11% are 2-letter US codes (foreign provinces, money, or free text) |
| WORKSITE_STATE_3 | state | 2% | 99 | mixed / not a state | only 14% are 2-letter US codes (foreign provinces, money, or free text); only 2.1% of rows filled |
| WORKSITE_STATE_4 | state | 1% | 52 | state names (not codes) | only 0.6% of rows filled |
| WORKSITE_STATE_5 | state | 0% | 49 | state names (not codes) | only 0.3% of rows filled |
| WORKSITE_STATE_6 | state | 0% | 48 | state names (not codes) | only 0.2% of rows filled |
| WORKSITE_STATE_7 | state | 0% | 44 | state names (not codes) | only 0.1% of rows filled |
| WORKSITE_STATE_8 | state | 0% | 44 | state names (not codes) | only 0.1% of rows filled |
| WORKSITE_STATE_9 | state | 0% | 41 | state names (not codes) | only 0.1% of rows filled |
| AGENT_ATTORNEY_POSTAL_CODE | zip | 67% | 2,525 | mixed / not a ZIP | only 83% look like ZIPs |
| EMPLOYER_POSTAL_CODE | zip | 100% | 11,278 | mixed / not a ZIP | only 85% look like ZIPs |
| WORKSITE_POSTAL_CODE_1 | zip | 100% | 15,440 | mixed / not a ZIP | only 89% look like ZIPs |
| WORKSITE_POSTAL_CODE_10 | zip | 0% | 180 | clean ZIP | only 0.0% of rows filled |
| WORKSITE_POSTAL_CODE_2 | zip | 9% | 6,438 | mixed / not a ZIP | only 87% look like ZIPs |
| WORKSITE_POSTAL_CODE_3 | zip | 2% | 3,689 | mixed / not a ZIP | only 87% look like ZIPs; only 2.1% of rows filled |
| WORKSITE_POSTAL_CODE_4 | zip | 1% | 1,813 | mixed / not a ZIP | only 88% look like ZIPs; only 0.6% of rows filled |
| WORKSITE_POSTAL_CODE_5 | zip | 0% | 1,143 | mixed / not a ZIP | only 91% look like ZIPs; only 0.3% of rows filled |
| WORKSITE_POSTAL_CODE_6 | zip | 0% | 715 | mixed / not a ZIP | only 92% look like ZIPs; only 0.2% of rows filled |
| WORKSITE_POSTAL_CODE_7 | zip | 0% | 503 | mixed / not a ZIP | only 93% look like ZIPs; only 0.1% of rows filled |
| WORKSITE_POSTAL_CODE_8 | zip | 0% | 364 | mixed / not a ZIP | only 91% look like ZIPs; only 0.1% of rows filled |
| WORKSITE_POSTAL_CODE_9 | zip | 0% | 256 | mixed / not a ZIP | only 95% look like ZIPs; only 0.1% of rows filled |
### IMMIGRATION__FED_ICE_DETAINERS  (609,769 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CRIMINAL_STREET_GANG_YES_NO | address | 28% | 2 | text place |  |
| PORT_OF_DEPARTURE | airport_port | 31% | 189 | text place |  |
| FACILITY_CITY | city | 100% | 3,093 | text place |  |
| BIRTH_COUNTRY | country | 100% | 232 | country name |  |
| CITIZENSHIP_COUNTRY | country | 100% | 210 | country name |  |
| DEPARTURE_COUNTRY | country | 31% | 196 | country name |  |
| TOD_CURRENT_DUTY_SITE | facility_site | 100% | 464 | text place |  |
| FACILITY_STATE | state | 100% | 55 | state names (not codes) |  |
### IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES  (1,490 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 96% | 1,367 | text place |  |
| CITY | city | 99% | 886 | text place |  |
| LATITUDE | coordinates | 99% | 37 | clean coordinate |  |
| LONGITUDE | coordinates | 99% | 74 | clean coordinate |  |
| COUNTY | county | 99% | 621 | county name |  |
| STATE | state | 100% | 56 | clean 2-letter state |  |
| ZIP | zip | 95% | 1,133 | mixed / not a ZIP | only 94% look like ZIPs |
### IMMIGRATION__FED_ICE_DETENTION_FACILITY_LIST  (163 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 151 | text place |  |
| STATE | state | 100% | 45 | clean 2-letter state |  |
### IMMIGRATION__FED_ICE_DETENTION_STINTS  (2,571,975 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 85% | 424 | text place |  |
| BIRTH_COUNTRY | country | 100% | 221 | country name |  |
| CITIZENSHIP_COUNTRY | country | 100% | 207 | country name |  |
| DEPARTURE_COUNTRY | country | 71% | 217 | country name |  |
| COUNTY | county | 85% | 343 | county name |  |
| BOOK_IN_SITE | facility_site | 100% | 220 | text place |  |
| STATE | state | 100% | 55 | clean 2-letter state |  |
### IMMIGRATION__FED_ICE_STATISTICS  (204 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY_OF_CITIZENSHIP | country | 96% | 196 | country name |  |
### IMMIGRATION__FED_USCIS_DATA  (177 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
### IMMIGRATION__XC_OWID_REFUGEES  (7,442 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| REFUGEES_BY_COUNTRY_OF_ORIGIN | country | 97% | 4,229 | country name |  |
| WORLD_REGION_ACCORDING_TO_OWID | region | 97% | 6 | text place |  |
### JUSTICE__COUNTY_DOUBLE_BURDEN  (3,029 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY_NAME | county | 100% | 3,011 | county name |  |
| FIPS | fips | 100% | 3,023 | clean FIPS (5-digit) |  |
| STATE_ABBR | state | 100% | 45 | clean 2-letter state |  |
| STATE_NAME | state | 100% | 45 | state names (not codes) |  |
### JUSTICE__FED_ATF_FFL  (77,514 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| MAIL_STREET | address | 100% | 62,782 | text place |  |
| PREMISE_STREET | address | 100% | 71,927 | text place |  |
| MAIL_CITY | city | 100% | 11,056 | text place |  |
| PREMISE_CITY | city | 100% | 11,141 | text place |  |
| LIC_DISTRICT | cong_district | 100% | 65 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| LATITUDE | coordinates | 100% | 73,344 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 71,091 | clean coordinate |  |
| LIC_COUNTY | county | 100% | 319 | mixed county |  |
| LIC_REGION | region | 100% | 7 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| MAIL_STATE | state | 100% | 55 | clean 2-letter state |  |
| PREMISE_STATE | state | 100% | 55 | clean 2-letter state |  |
| MAIL_ZIP_CODE | zip | 100% | 24,915 | clean ZIP |  |
| PREMISE_ZIP_CODE | zip | 100% | 25,035 | clean ZIP |  |
### JUSTICE__FED_BOP_STATISTICS  (50 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
### JUSTICE__FED_COURTLISTENER_COURTHOUSES  (3,361 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS1 | address | 0% | 2 | text place | only 0.1% of rows filled |
| ADDRESS2 | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| CITY | city | 0% | 7 | text place | only 0.3% of rows filled |
| COUNTRY_CODE | country | 100% | 2 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| COUNTY | county | 0% | 1 | constant | one value for the whole table |
| STATE | state | 100% | 63 | clean 2-letter state |  |
| ZIP_CODE | zip | 0% | 2 | clean ZIP | only 0.1% of rows filled |
### JUSTICE__FED_COURTLISTENER_COURTS  (3,361 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| JURISDICTION | region | 100% | 21 | text place |  |
### JUSTICE__FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS  (33,472 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LOCATION | facility_site | 75% | 4,736 | text place |  |
### JUSTICE__FED_COURTLISTENER_DOCKETS  (71,677,647 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| JURISDICTION_TYPE | region | 14% | 12 | text place |  |
### JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED  (10,323,280 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT_ID | cong_district | 100% | 95 | text place |  |
| COUNTY_OF_RESIDENCE | county | 99% | 3,321 | mixed county |  |
| JURISDICTION | region | 91% | 5 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### JUSTICE__FED_COURTLISTENER_JUDGES  (16,191 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DOB_CITY | city | 27% | 1,826 | text place |  |
| DOD_CITY | city | 9% | 623 | text place |  |
| DOB_COUNTRY | country | 100% | 63 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| DOD_COUNTRY | country | 100% | 2 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| DOB_STATE | state | 26% | 53 | clean 2-letter state |  |
| DOD_STATE | state | 9% | 51 | clean 2-letter state |  |
### JUSTICE__FED_COURTLISTENER_POSITIONS  (51,290 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LOCATION_CITY | city | 20% | 1,973 | text place |  |
| LOCATION_STATE | state | 25% | 54 | clean 2-letter state |  |
### JUSTICE__FED_DOJ_FCA_SETTLEMENTS  (12 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 0% | 0 | empty | no real values (blank or sentinel only) |
### JUSTICE__FED_FBI_CDE  (238,680 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 51 | clean 2-letter state |  |
### JUSTICE__FED_FBI_NICS_CHECKS  (16,445 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LONG_GUN | coordinates | 96% | 10,284 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| PREPAWN_LONG_GUN | coordinates | 48% | 137 | clean coordinate |  |
| PRIVATE_SALE_LONG_GUN | coordinates | 23% | 359 | coordinate with 0,0 trap | 44% are exactly 0 (Gulf of Guinea rows) |
| REDEMPTION_LONG_GUN | coordinates | 62% | 2,450 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| RENTALS_LONG_GUN | coordinates | 1% | 14 | clean coordinate | only 0.9% of rows filled |
| RETURNED_LONG_GUN | coordinates | 20% | 193 | clean coordinate |  |
| RETURN_TO_SELLER_LONG_GUN | coordinates | 11% | 51 | clean coordinate |  |
| STATE | state | 100% | 55 | state names (not codes) |  |
### JUSTICE__FED_FHFA_SUSPENDED_COUNTERPARTIES  (222 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 167 | text place |  |
| STATE | state | 100% | 37 | state names (not codes) |  |
### JUSTICE__FED_FJC_IDB_APPELLATE  (988,183 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT_CIRCUIT | cong_district | 99% | 13 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| DISTRICT_COURT | cong_district | 100% | 94 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| DISTRICT_DEFENDANT_NUMBER | cong_district | 100% | 158 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| DISTRICT_DOCKET | cong_district | 100% | 178,771 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| DISTRICT_DOCKET_DATE | cong_district | 77% | 11,722 | not a place (dates) | name-scan false hit |
| DISTRICT_JUDGE | cong_district | 0% | 0 | empty | no real values (blank or sentinel only) |
| DISTRICT_OFFICE | cong_district | 99% | 14 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| JURISDICTION | region | 100% | 6 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### JUSTICE__FED_FJC_IDB_BANKRUPTCY  (6,965,441 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 100% | 93 | text place |  |
| DEBTOR1_COUNTY | county | 100% | 3,250 | county code |  |
| DEBTOR2_COUNTY | county | 20% | 3,212 | county code |  |
| DEBTOR1_ZIP | zip | 100% | 239,072 | clean ZIP |  |
| DEBTOR2_ZIP | zip | 20% | 72,261 | clean ZIP |  |
### JUSTICE__FED_FJC_IDB_CIVIL  (10,857,396 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 100% | 93 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| COUNTY | county | 99% | 3,264 | county code |  |
| JURISDICTION | region | 100% | 6 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### JUSTICE__FED_FJC_IDB_CRIMINAL  (6,299,908 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 100% | 93 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TRANSFER_DISTRICT | cong_district | 100% | 93 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| COUNTY | county | 100% | 3,233 | county code |  |
### JUSTICE__FED_JPML_PENDING_MDLS  (162 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 100% | 58 | text place |  |
### JUSTICE__FED_SCDB  (83,644 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| JURISDICTION_CODE | region | 100% | 11 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| ADMIN_ACTION_STATE_CODE | state | 7% | 52 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| CASE_ORIGIN_STATE_CODE | state | 27% | 53 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| CASE_SOURCE_STATE_CODE | state | 23% | 53 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| PETITIONER_STATE_CODE | state | 20% | 56 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| RESPONDENT_STATE_CODE | state | 28% | 55 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
### JUSTICE__FED_USCOURTS_STATS  (50 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 0% | 0 | empty | no real values (blank or sentinel only) |
| COUNTY | county | 0% | 0 | empty | no real values (blank or sentinel only) |
| FIPS_CODE | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
### JUSTICE__INTL_AUSTLII  (1 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| JURISDICTION | region | 100% | 1 | constant | one value for the whole table |
### JUSTICE__INTL_EURLEX_CELLAR  (13 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
### JUSTICE__INTL_EU_SANCTIONS  (42,347 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDR_LEBA_NUMTITLE | address | 6% | 369 | text place |  |
| ADDR_LEBA_PUBLICATION_DATE | address | 6% | 320 | not a place (dates) | name-scan false hit |
| ADDR_LEBA_URL | address | 6% | 369 | text place |  |
| ADDR_LOGICAL_ID | address | 6% | 2,457 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| ADDR_NUMBER | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| ADDR_OTHER | address | 2% | 884 | text place | only 2.3% of rows filled |
| ADDR_PROGRAMME | address | 6% | 33 | text place |  |
| ADDR_STREET | address | 4% | 1,704 | text place | only 4.2% of rows filled |
| ADDR_CITY | city | 5% | 673 | text place | only 4.7% of rows filled |
| ADDR_COUNTRY | country | 6% | 89 | country code |  |
| BIRT_COUNTRY | country | 6% | 82 | country code |  |
| CITI_COUNTRY | country | 6% | 85 | country code |  |
| IDEN_COUNTRY | country | 3% | 70 | country code | only 3.4% of rows filled |
| BIRT_PLACE | facility_site | 5% | 1,077 | text place | only 4.9% of rows filled |
| ADDR_ZIPCODE | zip | 2% | 576 | mixed / not a ZIP | only 9% look like ZIPs; only 1.7% of rows filled |
### JUSTICE__INTL_EU_SOCTA_EUROPOL  (26 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| GEOGRAPHIC_SCOPE | facility_site | 100% | 1 | constant | one value for the whole table |
### JUSTICE__INTL_HUDOC  (2,000 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 100% | 48 | country code |  |
### JUSTICE__INTL_NTI_CNS_DPRK_MISSILE_TESTS  (303 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FACILITY_LATITUDE | coordinates | 95% | 46 | clean coordinate |  |
| FACILITY_LONGITUDE | coordinates | 95% | 47 | clean coordinate |  |
| FACILITY_LOCATION | facility_site | 95% | 32 | text place |  |
| LANDING_LOCATION | facility_site | 88% | 6 | text place |  |
### JUSTICE__INTL_OPENSANCTIONS  (71,011 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRIES | country | 81% | 1,412 | country code |  |
### JUSTICE__INTL_OPENSANCTIONS_DEFAULT  (1,281,846 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRIES | country | 92% | 5,089 | country code |  |
### JUSTICE__INTL_UCDP_GED  (385,918 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 100% | 53,320 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 53,733 | clean coordinate |  |
| WHERE_COORDINATES | coordinates | 100% | 54,700 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| COUNTRY | country | 100% | 122 | country name |  |
| COUNTRY_ID | country | 100% | 125 | country name |  |
| GEOM_WKT | geometry | 100% | 55,566 | text place |  |
| REGION | region | 100% | 5 | text place |  |
### JUSTICE__RACIAL_JAIL_DISPARITY  (128,507 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY_NAME | county | 100% | 1,838 | county name |  |
| COUNTY_YEAR_KEY | county | 100% | 126,816 | county name |  |
| FIPS | fips | 100% | 3,069 | clean FIPS (5-digit) |  |
| STATE_FIPS | fips | 100% | 45 | clean FIPS (2-digit) |  |
| REGION | region | 100% | 4 | text place |  |
| STATE_ABBR | state | 100% | 45 | clean 2-letter state |  |
### JUSTICE__STATE_MO_SEX_OFFENDER_REGISTRY  (28,167 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 97% | 16,255 | text place |  |
| CITY | city | 84% | 997 | text place |  |
| COUNTY | county | 83% | 114 | county name |  |
| STATE | state | 100% | 56 | clean 2-letter state |  |
| ZIP | zip | 84% | 1,051 | clean ZIP |  |
### JUSTICE__XC_MAPPING_POLICE_VIOLENCE  (15,476 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS_OF_INCIDENT | address | 97% | 14,795 | text place |  |
| CENSUS_TRACT_CODE | census_tract | 91% | 6,634 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| MEDIAN_HOUSEHOLD_INCOME_ACS_CENSUS_TRACT | census_tract | 85% | 9,734 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| TOTAL_POPULATION_OF_CENSUS_TRACT_2019_ACS_5_YEAR_ESTIMATES | census_tract | 91% | 3,091 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| CITY | city | 100% | 4,497 | text place |  |
| CONGRESSIONAL_DISTRICT | cong_district | 95% | 433 | text place |  |
| CONGRESSIONAL_REPRESENTATIVE_FULL_NAME_HTTPS_BALLOTPEDIA_ORG_UNITED_STATES_HOUSE_OF_REPRESENTATIVES | cong_district | 95% | 449 | text place |  |
| CONGRESSIONAL_REPRESENTATIVE_PARTY_HTTPS_BALLOTPEDIA_ORG_UNITED_STATES_HOUSE_OF_REPRESENTATIVES | cong_district | 95% | 2 | text place |  |
| LATITUDE | coordinates | 94% | 13,953 | clean coordinate |  |
| LONGITUDE | coordinates | 94% | 14,178 | clean coordinate |  |
| COUNTY | county | 100% | 1,396 | county name |  |
| HUD_UPSAI_GEOGRAPHY | facility_site | 65% | 3 | text place |  |
| NCHS_URBAN_RURAL_CLASSIFICATION_SCHEME_CODES_HTTPS_WWW_CDC_GOV_NCHS_DATA_ACCESS_URBAN_RURAL_HTM | metro | 94% | 6 | text place |  |
| STATE | state | 100% | 51 | clean 2-letter state |  |
| GEOGRAPHY_VIA_TRULIA_METHODOLOGY_BASED_ON_ZIPCODE_POPULATION_DENSITY_HTTP_JEDKOLKO_COM_WP_CONTENT_UPLOADS_2015_05_FULL_ZCTA_URBAN_SUBURBAN_RURAL_CLASSIFICATION_XLSX | zip | 94% | 3 | foreign postal code | only 0% look like US ZIPs |
| ZIPCODE | zip | 99% | 8,058 | clean ZIP |  |
### JUSTICE__XC_OWID_HOMICIDE  (4,912 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| WORLD_REGION_ACCORDING_TO_OWID | region | 86% | 6 | text place |  |
### JUSTICE__XC_OWID_TERRORISM_DEATHS  (10,481 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| WORLD_REGION_ACCORDING_TO_OWID | region | 88% | 6 | text place |  |
### JUSTICE__XC_RANSOMWARELIVE_VICTIMS  (30,661 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 74% | 186 | country code |  |
### JUSTICE__XC_UK_SANCTIONS_LIST  (33,828 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE_1 | address | 36% | 1,632 | text place |  |
| ADDRESS_LINE_2 | address | 21% | 954 | text place |  |
| TOWN_OF_BIRTH | city | 56% | 1,516 | text place |  |
| ADDRESS_COUNTRY | country | 66% | 106 | country name |  |
| COUNTRY_OF_BIRTH | country | 60% | 132 | country name |  |
| ADDRESS_POSTAL_CODE | zip | 12% | 657 | mixed / not a ZIP | only 15% look like ZIPs |
### JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST  (1,011 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ENTITY_ADDRESS | address | 27% | 149 | text place |  |
| INDIVIDUAL_ADDRESS | address | 73% | 238 | text place |  |
| NATIONALITY | country | 63% | 77 | country name |  |
| INDIVIDUAL_PLACE_OF_BIRTH | facility_site | 73% | 421 | text place |  |
### JUSTICE__XC_VERA_INCARCERATION_TRENDS  (128,507 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY_CODE | county | 100% | 3,053 | county name |  |
| COUNTY_NAME | county | 100% | 1,838 | county name |  |
| COUNTY_FIPS | fips | 100% | 3,069 | clean FIPS (5-digit) |  |
| STATE_FIPS | fips | 100% | 45 | clean FIPS (2-digit) |  |
| METRO_AREA | metro | 59% | 899 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| COMMUTING_ZONE | region | 100% | 676 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| REGION | region | 100% | 4 | text place |  |
| IS_UNIFIED_STATE | state | 100% | 1 | constant | one value for the whole table |
| STATE_ABBR | state | 100% | 45 | clean 2-letter state |  |
| STATE_CODE | state | 100% | 45 | state names (not codes) |  |
### JUSTICE__XC_WAPO_FATAL_FORCE  (10,430 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 99% | 3,764 | text place |  |
| LATITUDE | coordinates | 89% | 9,248 | clean coordinate |  |
| LONGITUDE | coordinates | 89% | 9,161 | clean coordinate |  |
| COUNTY | county | 55% | 993 | county name |  |
| STATE | state | 100% | 51 | clean 2-letter state |  |
### LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB  (41,802 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| SB_ACTUARY_FOREIGN_ADDRESS1 | address | 0% | 1 | constant | one value for the whole table |
| SB_ACTUARY_FOREIGN_ADDRESS2 | address | 0% | 1 | constant | one value for the whole table |
| SB_ACTUARY_US_ADDRESS1 | address | 100% | 3,150 | text place |  |
| SB_ACTUARY_US_ADDRESS2 | address | 31% | 523 | text place |  |
| SB_PORT_PREFNDNG_FNDNG_CAR_AMT | airport_port | 2% | 868 | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 2.2% of rows filled |
| SB_ACTUARY_FOREIGN_CITY | city | 0% | 1 | constant | one value for the whole table |
| SB_ACTUARY_US_CITY | city | 100% | 637 | text place |  |
| SB_ACTUARY_FOREIGN_CNTRY | country | 0% | 1 | constant | one value for the whole table |
| SB_ACTUARY_FOREIGN_PROV_STATE | state | 0% | 1 | constant | one value for the whole table |
| SB_ACTUARY_US_STATE | state | 100% | 53 | clean 2-letter state |  |
| SB_ACTUARY_FOREIGN_POSTAL_CD | zip | 0% | 1 | constant | one value for the whole table |
| SB_ACTUARY_US_ZIP | zip | 100% | 979 | clean ZIP |  |
### LABOR__FED_DOL_OLMS  (617,710 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_ID | address | 100% | 489,702 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| ADDRESS_TYPE | address | 100% | 1 | constant | one value for the whole table |
| STREET_ADDRESS | address | 80% | 101,054 | text place |  |
| CITY | city | 100% | 14,318 | text place |  |
| STATE | state | 100% | 127 | clean 2-letter state |  |
| ZIP | zip | 100% | 56,870 | clean ZIP |  |
### LABOR__FED_MSHA_ACCIDENTS  (273,623 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FIPS_STATE_CD | fips | 100% | 54 | clean FIPS (2-digit) |  |
### LABOR__FED_MSHA_MINES  (91,906 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| NEAREST_TOWN | city | 59% | 11,870 | text place |  |
| LATITUDE | coordinates | 52% | 29,660 | clean coordinate |  |
| LONGITUDE | coordinates | 52% | 34,139 | clean coordinate |  |
| FIPS_CNTY_CD | fips | 100% | 298 | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining |
| FIPS_CNTY_NM | fips | 100% | 1,768 | mixed / not FIPS | only 0% have a FIPS length; modal length 7 |
| STATE | state | 100% | 55 | clean 2-letter state |  |
### LABOR__FED_OSHA_ITA_300A_SUMMARY_2023  (394,234 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 100% | 347,143 | text place |  |
| CITY | city | 100% | 17,644 | text place |  |
| STATE | state | 100% | 62 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 25,668 | clean ZIP |  |
### LABOR__FED_OSHA_ITA_300A_SUMMARY_2024  (398,620 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 100% | 364,650 | text place |  |
| CITY | city | 100% | 17,241 | text place |  |
| STATE | state | 100% | 61 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 25,055 | mixed / not a ZIP | only 93% look like ZIPs |
### LABOR__FED_OSHA_ITA_300A_SUMMARY_2025  (383,283 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 100% | 350,418 | text place |  |
| CITY | city | 100% | 16,617 | text place |  |
| STATE | state | 100% | 62 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 24,632 | clean ZIP |  |
### LABOR__FED_OSHA_ITA_CASE_DETAIL_2023  (890,934 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 100% | 89,884 | text place |  |
| CITY | city | 100% | 9,425 | text place |  |
| NEW_INCIDENT_LOCATION | facility_site | 99% | 270,217 | text place |  |
| STATE | state | 100% | 56 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 17,331 | clean ZIP |  |
### LABOR__FED_OSHA_ITA_CASE_DETAIL_2024  (688,649 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 100% | 62,976 | text place |  |
| CITY | city | 100% | 7,807 | text place |  |
| NEW_INCIDENT_LOCATION | facility_site | 99% | 216,590 | text place |  |
| STATE | state | 100% | 58 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 17,443 | mixed / not a ZIP | only 92% look like ZIPs |
### LABOR__FED_OSHA_ITA_CASE_DETAIL_2025  (330,447 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET_ADDRESS | address | 100% | 34,963 | text place |  |
| CITY | city | 100% | 6,124 | text place |  |
| NEW_INCIDENT_LOCATION | facility_site | 100% | 122,874 | text place |  |
| STATE | state | 100% | 58 | clean 2-letter state |  |
| ZIP_CODE | zip | 100% | 15,006 | mixed / not a ZIP | only 92% look like ZIPs |
### LABOR__FED_PBGC_TRUSTEED_PLANS  (5,176 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 99% | 1,683 | text place |  |
| STATE | state | 99% | 57 | clean 2-letter state |  |
### LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS  (882 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LOCATION_SETTLEMENT_FILED | facility_site | 0% | 0 | empty | no real values (blank or sentinel only) |
| OTHER_SINGLE_STATE_SETTLEMENTS | state | 0% | 0 | empty | no real values (blank or sentinel only) |
| STATE_COSTS_FEES | state | 2% | 10 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text); only 2.2% of rows filled |
### MARITIME__FED_NOAA_AIS  (58,104,610 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 100% | 2,690,340 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 3,396,652 | clean coordinate |  |
### MONEY__DEBT_REPAYMENT_CLIFF  (938 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY_CODE | country | 100% | 136 | country code |  |
| COUNTRY_NAME | country | 100% | 134 | country name |  |
| COUNTRY_YEAR_ID | country | 100% | 925 | country name |  |
### OPEN_DATA__INTL_BR_DADOS_GOV  (10 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| GEOGRAPHIC_COVERAGE | facility_site | 0% | 0 | empty | no real values (blank or sentinel only) |
### OPEN_DATA__INTL_CH_OPENDATASWISS  (5,000 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 1 | constant | one value for the whole table |
### OPEN_DATA__INTL_CL_DATOSGOB  (1,000 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 1 | constant | one value for the whole table |
### OPEN_DATA__INTL_ES_DATOSGOB  (1,000 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| GEOGRAPHIC_COVERAGE | facility_site | 42% | 73 | text place |  |
### OPEN_DATA__INTL_GE_DATAGOV  (1 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 100% | 1 | constant | one value for the whole table |
### POLITICS__BILL_COSPONSORS  (367,735 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COSPONSOR_STATE | state | 100% | 56 | clean 2-letter state |  |
### POLITICS__CA_LOBBY_CHG_LOG  (85,765 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ENTITY_CITY | city | 2% | 281 | text place | only 2.2% of rows filled |
| FILER_CITY | city | 23% | 964 | text place |  |
| ENTITY_ZIP | zip | 2% | 488 | clean ZIP | only 2.2% of rows filled |
| FILER_ZIP | zip | 23% | 1,938 | clean ZIP |  |
### POLITICS__CA_LOBBY_COVER  (524,828 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FIRM_CITY | city | 100% | 2,546 | text place |  |
### POLITICS__FEC_CANDIDATE  (17,900 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| OFFICE_DISTRICT | cong_district | 63% | 69 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| OFFICE_STATE | state | 100% | 57 | mixed / not a state | only 80% are 2-letter US codes (foreign provinces, money, or free text) |
### POLITICS__FEC_COMMITTEE  (40,945 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CMTE_CITY | city | 100% | 4,483 | text place |  |
| CMTE_ZIP | zip | 100% | 10,365 | clean ZIP |  |
### POLITICS__FED_CONGRESS_LEGISLATORS  (12,767 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 82% | 55 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE | state | 100% | 59 | clean 2-letter state |  |
### POLITICS__FED_EAC_EAVS  (6,460 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| FIPSCODE | fips | 100% | 6,487 | mixed / not FIPS | only 29% have a FIPS length; modal length 10 |
| JURISDICTION_NAME | region | 100% | 5,186 | text place |  |
| STATE_ABBR | state | 100% | 55 | clean 2-letter state |  |
| STATE_FULL | state | 100% | 55 | state names (not codes) |  |
### POLITICS__FED_FCC_LICENSING  (1,689,338 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS_LINE1 | address | 92% | 1,283,244 | text place |  |
| CITY | city | 99% | 29,899 | text place |  |
| FCC_COUNTY_CODE | county | 0% | 0 | empty | no real values (blank or sentinel only) |
| STATE | state | 99% | 60 | clean 2-letter state |  |
| ZIP_CODE | zip | 99% | 228,996 | clean ZIP |  |
### POLITICS__FED_FEC_API  (500 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 0% | 0 | empty | no real values (blank or sentinel only) |
| CONTRIBUTOR_STATE | state | 97% | 45 | clean 2-letter state |  |
| STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
| CONTRIBUTOR_ZIP | zip | 94% | 310 | clean ZIP |  |
### POLITICS__FED_FJC_JUDGES  (4,067 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| BIRTH_CITY | city | 99% | 1,716 | text place |  |
| DEATH_CITY | city | 42% | 688 | text place |  |
| BIRTH_STATE | state | 100% | 107 | clean 2-letter state |  |
| DEATH_STATE | state | 42% | 61 | clean 2-letter state |  |
### POLITICS__FED_MEDSL_HOUSE_RETURNS  (29,636 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 98% | 54 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_FIPS | fips | 100% | 50 | FIPS with leading zeros lost | 82% have a FIPS length; modal length 2 -- pad before joining |
| STATE_ABBR | state | 100% | 50 | clean 2-letter state |  |
| STATE_NAME | state | 100% | 50 | state names (not codes) |  |
### POLITICS__FED_MEDSL_PRESIDENT_RETURNS  (3,740 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_FIPS | fips | 100% | 51 | FIPS with leading zeros lost | 85% have a FIPS length; modal length 2 -- pad before joining |
| STATE_ABBR | state | 100% | 51 | clean 2-letter state |  |
| STATE_NAME | state | 100% | 51 | state names (not codes) |  |
### POLITICS__FED_MEDSL_SENATE_RETURNS  (3,945 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_FIPS | fips | 100% | 50 | FIPS with leading zeros lost | 85% have a FIPS length; modal length 2 -- pad before joining |
| STATE_ABBR | state | 100% | 50 | clean 2-letter state |  |
| STATE_NAME | state | 100% | 50 | state names (not codes) |  |
### POLITICS__FED_VOTEVIEW_MEMBERS  (51,061 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT_CODE | cong_district | 81% | 109 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_ABBREV | state | 100% | 57 | clean 2-letter state |  |
| STATE_ICPSR | state | 100% | 56 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
### POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS  (12,646,465 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CONTRIBUTOR_CITY | city | 100% | 19,842 | text place |  |
| ELECTORAL_DISTRICT | cong_district | 11% | 600 | text place |  |
| CONTRIBUTOR_PROVINCE | state | 100% | 147 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
| CONTRIBUTOR_POSTAL_CODE | zip | 100% | 401,212 | foreign postal code | only 0% look like US ZIPs |
### POLITICS__INTL_FREEDOMHOUSE  (2,723 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY_TERRITORY | country | 100% | 211 | country name |  |
| REGION | region | 100% | 6 | text place |  |
### POLITICS__INTL_OWID_MILSPEND  (9,112 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| WORLD_REGION_ACCORDING_TO_OWID | region | 93% | 6 | text place |  |
### POLITICS__IRS527_8871_ORGS  (77,591 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| EMAIL_ADDRESS | address | 100% | 40,303 | text place |  |
| MAILING_ADDR1 | address | 100% | 48,849 | text place |  |
| MAILING_CITY | city | 100% | 7,664 | text place |  |
| MAILING_STATE | state | 100% | 56 | clean 2-letter state |  |
| MAILING_ZIP | zip | 100% | 15,155 | clean ZIP |  |
### POLITICS__IRS527_8872_REPORTS  (55,579 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CHANGE_OF_ADDRESS_IND | address | 2% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 1.5% of rows filled |
| EMAIL_ADDRESS | address | 100% | 4,170 | text place |  |
| MAILING_ADDR1 | address | 100% | 5,276 | text place |  |
| MAILING_ADDR2 | address | 23% | 906 | text place |  |
| BUSINESS_CITY | city | 100% | 1,558 | text place |  |
| CONTACT_CITY | city | 100% | 1,584 | text place |  |
| CUSTODIAN_CITY | city | 100% | 1,580 | text place |  |
| MAILING_CITY | city | 100% | 1,552 | text place |  |
| BUSINESS_STATE | state | 100% | 53 | clean 2-letter state |  |
| CONTACT_STATE | state | 100% | 53 | clean 2-letter state |  |
| CUSTODIAN_STATE | state | 100% | 53 | clean 2-letter state |  |
| MAILING_STATE | state | 100% | 53 | clean 2-letter state |  |
| PRE_OR_POST_ELECT_STATE | state | 16% | 54 | clean 2-letter state |  |
| BUSINESS_ZIP | zip | 100% | 2,869 | clean ZIP |  |
| BUSINESS_ZIP_EXT | zip | 17% | 893 | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) |
| CONTACT_ZIP | zip | 100% | 2,881 | clean ZIP |  |
| CONTACT_ZIP_EXT | zip | 18% | 987 | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) |
| CUSTODIAN_ZIP | zip | 100% | 2,855 | clean ZIP |  |
| CUSTODIAN_ZIP_EXT | zip | 19% | 1,001 | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) |
| MAILING_ZIP | zip | 100% | 2,809 | clean ZIP |  |
| MAILING_ZIP_EXT | zip | 18% | 879 | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) |
### POLITICS__IRS527_DIRECTORS_OFFICERS  (189,593 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ENTITY_CITY | city | 100% | 9,130 | text place |  |
| ENTITY_STATE | state | 100% | 56 | clean 2-letter state |  |
| ENTITY_ZIP | zip | 100% | 17,241 | clean ZIP |  |
| ENTITY_ZIP_EXT | zip | 15% | 6,481 | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) |
### POLITICS__IRS527_EAIN  (17,853 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_ISSUED | state | 100% | 52 | mixed / not a state | only 94% are 2-letter US codes (foreign provinces, money, or free text) |
### POLITICS__IRS527_RELATED_ENTITIES  (64,835 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ENTITY_CITY | city | 100% | 2,078 | text place |  |
| ENTITY_STATE | state | 100% | 53 | clean 2-letter state |  |
| ENTITY_ZIP | zip | 100% | 4,284 | clean ZIP |  |
| ENTITY_ZIP_EXT | zip | 29% | 1,237 | ZIP with leading zeros lost | 100% are 1-4 digits (00501 -> 501) |
### POLITICS__MEMBER_BILL_RECORD  (1,104 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 56 | clean 2-letter state |  |
### POLITICS__MEMBER_CROSSWALK  (12,794 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LAST_DISTRICT | cong_district | 82% | 55 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| LAST_STATE | state | 100% | 59 | clean 2-letter state |  |
### POLITICS__MEMBER_FEC_ID  (1,715 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 56 | clean 2-letter state |  |
### POLITICS__MEMBER_INDIV_DONATIONS  (1,057 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 56 | clean 2-letter state |  |
### POLITICS__MEMBER_MONEY_RAISED  (1,050 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 56 | clean 2-letter state |  |
### POLITICS__MEMBER_SPINE  (12,794 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 59 | clean 2-letter state |  |
### POLITICS__MEMBER_VOTING_RECORD  (1,105 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE | state | 100% | 56 | clean 2-letter state |  |
### POLITICS__ST_CANNABIS_POLICY_BUNDLES  (1,500 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LEGISLATIVE_ACTION | cong_district | 16% | 2 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| FIPS | fips | 100% | 50 | FIPS with leading zeros lost | 86% have a FIPS length; modal length 2 -- pad before joining |
| STATE | state | 100% | 50 | state names (not codes) |  |
| STATE_AB | state | 100% | 50 | clean 2-letter state |  |
| STATE_COURT_SIG_ACTION | state | 3% | 2 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining; only 2.9% of rows filled |
| STATE_SALES_TAX_HIGH_RCL_APP | state | 6% | 2 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| STATE_SALES_TAX_HIGH_RCL_IMP | state | 4% | 2 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining; only 4.0% of rows filled |
### POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION  (193,741 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| EMPLOYER_STREET_NAME | address | 51% | 15,559 | text place |  |
| EMPLOYER_STREET_NUMBER | address | 50% | 7,644 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| INTERMEDIARY_EMPLOYER_STREET_NAME | address | 7% | 606 | text place |  |
| INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | 7% | 536 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| INTERMEDIARY_STREET_NAME | address | 0% | 28 | text place | only 0.2% of rows filled |
| INTERMEDIARY_STREET_NUMBER | address | 0% | 30 | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 0.2% of rows filled |
| STREET_NAME | address | 6% | 3,221 | text place |  |
| STREET_NUMBER | address | 6% | 1,871 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| CITY | city | 99% | 3,543 | text place |  |
| EMPLOYER_CITY | city | 58% | 1,949 | text place |  |
| INTERMEDIARY_CITY | city | 8% | 222 | text place |  |
| INTERMEDIARY_EMPLOYER_CITY | city | 7% | 116 | text place |  |
| BOROUGH_CODE | county | 99% | 6 | county name |  |
| EMPLOYER_STATE | state | 59% | 83 | clean 2-letter state |  |
| INTERMEDIARY_EMPLOYER_STATE | state | 7% | 13 | clean 2-letter state |  |
| INTERMEDIARY_STATE | state | 8% | 15 | clean 2-letter state |  |
| STATE | state | 99% | 84 | clean 2-letter state |  |
| INTERMEDIARY_ZIP | zip | 7% | 330 | mixed / not a ZIP | only 94% look like ZIPs |
| ZIP | zip | 98% | 3,416 | clean ZIP |  |
### POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION  (146,112 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| EMPLOYER_STREET_NAME | address | 54% | 13,198 | text place |  |
| EMPLOYER_STREET_NUMBER | address | 53% | 7,506 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| INTERMEDIARY_EMPLOYER_STREET_NAME | address | 2% | 231 | text place | only 2.5% of rows filled |
| INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | 2% | 245 | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 2.4% of rows filled |
| INTERMEDIARY_STREET_NAME | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| INTERMEDIARY_STREET_NUMBER | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| STREET_NAME | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| STREET_NUMBER | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| CITY | city | 99% | 3,099 | text place |  |
| EMPLOYER_CITY | city | 64% | 1,862 | text place |  |
| INTERMEDIARY_CITY | city | 3% | 104 | text place | only 3.1% of rows filled |
| INTERMEDIARY_EMPLOYER_CITY | city | 3% | 53 | text place | only 2.8% of rows filled |
| BOROUGH_CODE | county | 99% | 6 | county name |  |
| EMPLOYER_STATE | state | 64% | 73 | clean 2-letter state |  |
| INTERMEDIARY_EMPLOYER_STATE | state | 3% | 8 | clean 2-letter state | only 2.8% of rows filled |
| INTERMEDIARY_STATE | state | 3% | 8 | clean 2-letter state | only 3.1% of rows filled |
| STATE | state | 99% | 82 | clean 2-letter state |  |
| INTERMEDIARY_ZIP | zip | 3% | 186 | clean ZIP | only 3.1% of rows filled |
| ZIP | zip | 99% | 3,652 | clean ZIP |  |
### POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION  (197,968 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| EMPLOYER_STREET_NAME | address | 55% | 17,048 | text place |  |
| EMPLOYER_STREET_NUMBER | address | 55% | 8,527 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| INTERMEDIARY_EMPLOYER_STREET_NAME | address | 7% | 550 | text place |  |
| INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | 7% | 516 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| INTERMEDIARY_STREET_NAME | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| INTERMEDIARY_STREET_NUMBER | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| STREET_NAME | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| STREET_NUMBER | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| CITY | city | 100% | 3,669 | text place |  |
| EMPLOYER_CITY | city | 66% | 2,516 | text place |  |
| INTERMEDIARY_CITY | city | 9% | 207 | text place |  |
| INTERMEDIARY_EMPLOYER_CITY | city | 8% | 120 | text place |  |
| BOROUGH_CODE | county | 99% | 6 | county name |  |
| EMPLOYER_STATE | state | 66% | 79 | clean 2-letter state |  |
| INTERMEDIARY_EMPLOYER_STATE | state | 8% | 12 | clean 2-letter state |  |
| INTERMEDIARY_STATE | state | 9% | 10 | clean 2-letter state |  |
| STATE | state | 100% | 84 | clean 2-letter state |  |
| INTERMEDIARY_ZIP | zip | 9% | 322 | clean ZIP |  |
| ZIP | zip | 99% | 4,990 | clean ZIP |  |
### POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS  (457,521 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| EMPLOYER_STREET_NAME | address | 72% | 62,164 | text place |  |
| EMPLOYER_STREET_NUMBER | address | 70% | 18,272 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| INTERMEDIARY_EMPLOYER_STREET_NAME | address | 1% | 265 | text place | only 1.0% of rows filled |
| INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | 1% | 259 | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 1.0% of rows filled |
| INTERMEDIARY_STREET_NAME | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| INTERMEDIARY_STREET_NUMBER | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| STREET_NAME | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| STREET_NUMBER | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| CITY | city | 100% | 7,323 | text place |  |
| EMPLOYER_CITY | city | 73% | 6,075 | text place |  |
| INTERMEDIARY_CITY | city | 2% | 88 | text place | only 1.9% of rows filled |
| INTERMEDIARY_EMPLOYER_CITY | city | 1% | 56 | text place | only 1.0% of rows filled |
| BOROUGH_CODE | county | 100% | 6 | county name |  |
| EMPLOYER_STATE | state | 73% | 53 | clean 2-letter state |  |
| INTERMEDIARY_EMPLOYER_STATE | state | 1% | 10 | clean 2-letter state | only 1.0% of rows filled |
| INTERMEDIARY_STATE | state | 2% | 11 | clean 2-letter state | only 1.9% of rows filled |
| STATE | state | 100% | 54 | clean 2-letter state |  |
| INTERMEDIARY_ZIP | zip | 2% | 185 | clean ZIP | only 1.9% of rows filled |
| ZIP | zip | 100% | 12,811 | mixed / not a ZIP | only 95% look like ZIPs |
### POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS  (259,537 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| EMPLOYER_STREET_NAME | address | 72% | 34,178 | text place |  |
| EMPLOYER_STREET_NUMBER | address | 71% | 13,824 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| INTERMEDIARY_EMPLOYER_STREET_NAME | address | 3% | 245 | text place | only 2.6% of rows filled |
| INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | 3% | 224 | coded place (numbers) | codes, not names -- needs a lookup to become a place; only 2.6% of rows filled |
| INTERMEDIARY_STREET_NAME | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| INTERMEDIARY_STREET_NUMBER | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| STREET_NAME | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| STREET_NUMBER | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| CITY | city | 100% | 6,219 | text place |  |
| EMPLOYER_CITY | city | 72% | 4,396 | text place |  |
| INTERMEDIARY_CITY | city | 3% | 82 | text place | only 3.1% of rows filled |
| INTERMEDIARY_EMPLOYER_CITY | city | 3% | 51 | text place | only 2.6% of rows filled |
| BOROUGH_CODE | county | 99% | 6 | county name |  |
| EMPLOYER_STATE | state | 72% | 53 | clean 2-letter state |  |
| INTERMEDIARY_EMPLOYER_STATE | state | 3% | 9 | clean 2-letter state | only 2.6% of rows filled |
| INTERMEDIARY_STATE | state | 3% | 11 | clean 2-letter state | only 3.1% of rows filled |
| STATE | state | 100% | 54 | clean 2-letter state |  |
| INTERMEDIARY_ZIP | zip | 3% | 164 | clean ZIP | only 3.1% of rows filled |
| ZIP | zip | 100% | 12,584 | mixed / not a ZIP | only 94% look like ZIPs |
### POLITICS__WHO_WON  (10,976 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 99% | 55 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE | state | 100% | 51 | clean 2-letter state |  |
### POLITICS__XC_OWID_CPI  (2,312 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| WORLD_REGION_ACCORDING_TO_OWID | region | 100% | 6 | text place |  |
### PROCUREMENT__FED_SAM_EXCLUSIONS  (168,328 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 88% | 12,550 | text place |  |
| COUNTRY | country | 100% | 187 | country code |  |
| STATE | state | 78% | 833 | clean 2-letter state |  |
| ZIP | zip | 82% | 24,925 | mixed / not a ZIP | only 92% look like ZIPs |
### PROCUREMENT__FED_USASPENDING_BULK  (49,613 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| RECIPIENT_ADDRESS_LINE_1 | address | 100% | 10,455 | text place |  |
| RECIPIENT_ADDRESS_LINE_2 | address | 7% | 598 | text place |  |
| AIRPORT_AUTHORITY | airport_port | 100% | 2 | text place |  |
| PORT_AUTHORITY | airport_port | 100% | 2 | text place |  |
| CITY_LOCAL_GOVERNMENT | city | 100% | 2 | text place |  |
| MUNICIPALITY_LOCAL_GOVERNMENT | city | 100% | 2 | text place |  |
| PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | city | 89% | 2,288 | text place |  |
| RECIPIENT_CITY_NAME | city | 100% | 2,839 | text place |  |
| SCHOOL_DISTRICT_LOCAL_GOVERNMENT | cong_district | 100% | 2 | text place |  |
| COUNTRY_OF_PRODUCT_OR_SERVICE_ORIGIN | country | 91% | 119 | country name |  |
| COUNTRY_OF_PRODUCT_OR_SERVICE_ORIGIN_CODE | country | 91% | 118 | country code |  |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_CODE | country | 91% | 133 | country code |  |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_NAME | country | 91% | 133 | country name |  |
| RECIPIENT_COUNTRY_CODE | country | 100% | 87 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| RECIPIENT_COUNTRY_NAME | country | 100% | 88 | country name (98%+ US) | almost no foreign rows -- weak as a join axis |
| COUNTY_LOCAL_GOVERNMENT | county | 100% | 2 | county name |  |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTY_NAME | county | 89% | 953 | county name |  |
| RECIPIENT_COUNTY_NAME | county | 99% | 951 | county name |  |
| PLACE_OF_MANUFACTURE | facility_site | 91% | 10 | text place |  |
| PLACE_OF_MANUFACTURE_CODE | facility_site | 91% | 10 | text place |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_CURRENT | facility_site | 89% | 446 | text place |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_ORIGINAL | facility_site | 89% | 446 | text place |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE | fips | 89% | 1,277 | clean FIPS (5-digit) |  |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_STATE_FIPS_CODE | fips | 89% | 56 | clean FIPS (2-digit) |  |
| PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE | fips | 99% | 1,308 | clean FIPS (5-digit) |  |
| PRIME_AWARD_TRANSACTION_RECIPIENT_STATE_FIPS_CODE | fips | 99% | 56 | clean FIPS (2-digit) |  |
| HISTORICALLY_UNDERUTILIZED_BUSINESS_ZONE_HUBZONE_FIRM | region | 100% | 2 | text place |  |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE | state | 89% | 58 | clean 2-letter state |  |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_NAME | state | 89% | 58 | state names (not codes) |  |
| RECIPIENT_STATE_CODE | state | 99% | 56 | clean 2-letter state |  |
| RECIPIENT_STATE_NAME | state | 100% | 88 | state names (not codes) |  |
| STATE_CONTROLLED_INSTITUTION_OF_HIGHER_LEARNING | state | 100% | 2 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
| US_STATE_GOVERNMENT | state | 100% | 2 | mixed / not a state | only 0% are 2-letter US codes (foreign provinces, money, or free text) |
| PRIMARY_PLACE_OF_PERFORMANCE_ZIP_4 | zip | 90% | 7,919 | clean ZIP |  |
| RECIPIENT_ZIP_4_CODE | zip | 100% | 10,065 | clean ZIP |  |
### PROCUREMENT__INTL_ADB_DATA  (41 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
### REFERENCE__FED_DHS_HIFLD  (500 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS | address | 0% | 0 | empty | no real values (blank or sentinel only) |
| CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| LATITUDE | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| LONGITUDE | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| COUNTY | county | 0% | 0 | empty | no real values (blank or sentinel only) |
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
| ZIP | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
### REFERENCE__FED_ITIS_GEOGRAPHIC_DIV  (480,351 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| GEOGRAPHIC_VALUE | facility_site | 100% | 14 | text place |  |
| ITIS_GEOGRAPHIC_DIV_KEY | facility_site | 100% | 484,300 | text place |  |
### REFERENCE__FED_ITIS_JURISDICTION  (161,922 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ITIS_JURISDICTION_KEY | region | 100% | 163,061 | text place |  |
| JURISDICTION_VALUE | region | 100% | 7 | text place |  |
### REFERENCE__FED_ITIS_PUBLICATIONS  (30,772 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| PUB_PLACE | facility_site | 13% | 837 | text place |  |
### REFERENCE__FED_USGS_TOPOVIEW  (250 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTIES | county | 0% | 0 | empty | no real values (blank or sentinel only) |
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
### REFERENCE__INTL_EG_CAPMAS  (52 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRY | country | 100% | 1 | constant | one value for the whole table |
### REFERENCE__INTL_GDELT  (1,015 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ACTIONGEO_LAT | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| ACTIONGEO_LONG | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| ACTOR1GEO_LAT | coordinates | 100% | 76 | coordinate, partly out of range | 89% parse in range |
| ACTOR1GEO_LONG | coordinates | 100% | 66 | coordinate, partly out of range | 92% parse in range |
| ACTOR2GEO_LAT | coordinates | 100% | 19 | clean coordinate |  |
| ACTOR2GEO_LONG | coordinates | 100% | 3 | clean coordinate |  |
### REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS  (135,710 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 100% | 18,698 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 18,781 | clean coordinate |  |
| COUNTRY_CODE | country | 100% | 235 | country code |  |
| COUNTRY_NAME | country | 100% | 232 | country name |  |
| LOCATION_NAME | facility_site | 100% | 16,911 | text place |  |
### REF__DIM_GEOGRAPHY  (6,988 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CENTROID_LATITUDE | coordinates | 100% | 6,939 | clean coordinate |  |
| CENTROID_LONGITUDE | coordinates | 100% | 6,855 | clean coordinate |  |
| COUNTY_NAME | county | 99% | 2,445 | county name |  |
| COUNTY_FIPS_SUFFIX | fips | 99% | 413 | FIPS with leading zeros lost | 0% have a FIPS length; modal length 3 -- pad before joining |
| FIPS_CODE | fips | 100% | 7,056 | mixed / not FIPS | only 54% have a FIPS length; modal length 5 |
| STATE_FIPS | fips | 95% | 120 | mixed / not FIPS | only 56% have a FIPS length; modal length 2 |
| EPA_REGION | region | 99% | 10 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_ABBR | state | 100% | 56 | clean 2-letter state |  |
| STATE_NAME | state | 98% | 58 | state names (not codes) |  |
### REF__DIM_STATE  (56 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STATE_FIPS | fips | 100% | 56 | clean FIPS (2-digit) |  |
| CENSUS_REGION | region | 100% | 5 | text place |  |
| STATE_ABBR | state | 100% | 56 | clean 2-letter state |  |
| STATE_NAME | state | 100% | 56 | state names (not codes) |  |
### SCIENCE__FED_NSF_AWARDS  (115 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY | city | 100% | 81 | text place |  |
| COUNTRY | country | 100% | 1 | constant | one value for the whole table |
| STATE | state | 100% | 40 | clean 2-letter state |  |
| ZIP | zip | 100% | 98 | clean ZIP |  |
### SCIENCE__FED_USGS_EARTHQUAKES  (443,274 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| LATITUDE | coordinates | 100% | 297,636 | clean coordinate |  |
| LONGITUDE | coordinates | 100% | 343,111 | clean coordinate |  |
| PLACE | facility_site | 100% | 177,726 | text place |  |
### SCIENCE__INTL_EMBL_ENSEMBL  (643 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| REGION | region | 100% | 472 | text place |  |
| SEQ_REGION_NAME | region | 100% | 11 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
### SCIENCE_RESEARCH__FED_NIH_REPORTER  (2,122,611 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ORG_CITY | city | 0% | 0 | empty | no real values (blank or sentinel only) |
| ORG_COUNTRY | country | 0% | 0 | empty | no real values (blank or sentinel only) |
| ORG_FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| ORG_STATE | state | 0% | 0 | empty | no real values (blank or sentinel only) |
| ORG_STATE_NAME | state | 0% | 0 | empty | no real values (blank or sentinel only) |
| ORG_ZIP | zip | 0% | 0 | empty | no real values (blank or sentinel only) |
### SCIENCE_RESEARCH__FED_RETRACTION_WATCH  (71,591 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRIES | country | 98% | 3,628 | country name |  |
### SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS  (219,503 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| ADDRESS1 | address | 100% | 32,680 | text place |  |
| ADDRESS2 | address | 17% | 3,913 | text place |  |
| CITY | city | 100% | 4,024 | text place |  |
| STATE | state | 100% | 55 | state names (not codes) |  |
| ZIP | zip | 96% | 22,638 | mixed / not a ZIP | only 95% look like ZIPs |
### SCIENCE_RESEARCH__XC_OSF_REGISTRATIONS  (10 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| REGION_ID | region | 100% | 2 | text place |  |
| REVIEWS_STATE | state | 100% | 1 | constant | one value for the whole table |
| REVISION_STATE | state | 100% | 1 | constant | one value for the whole table |
### SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE  (71,388 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTRIES | country | 99% | 3,628 | country name |  |
### TRANSPORT__FED_DOT_BTS  (21 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY_FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
| STATE_FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
### TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY  (315,447 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET | address | 99% | 173,036 | text place |  |
| CITY | city | 99% | 14,009 | text place |  |
| COUNTRY_CODE | country | 99% | 52 | country code (98%+ US) | almost no foreign rows -- weak as a join axis |
| COUNTY_CODE | county | 98% | 333 | county code |  |
| REGION | region | 99% | 10 | text place |  |
| STATE | state | 98% | 58 | clean 2-letter state |  |
| ZIP_CODE | zip | 98% | 171,161 | clean ZIP |  |
### TRANSPORT__FED_FAA_DATA_PORTAL  (3 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| AIRPORT_ID | airport_port | 0% | 0 | empty | no real values (blank or sentinel only) |
| LAT | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| LON | coordinates | 0% | 0 | empty | no real values (blank or sentinel only) |
| GEOGRAPHIC_SCOPE | facility_site | 0% | 0 | empty | no real values (blank or sentinel only) |
| FIPS | fips | 0% | 0 | empty | no real values (blank or sentinel only) |
### TRANSPORT__FED_FAA_REGISTRY  (0 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| STREET | address | - | 0 | not measured |  |
| CITY | city | - | 0 | not measured |  |
| COUNTRY | country | - | 0 | not measured |  |
| COUNTY | county | - | 0 | not measured |  |
| REGION | region | - | 0 | not measured |  |
| STATE | state | - | 0 | not measured |  |
| ZIP_CODE | zip | - | 0 | not measured |  |
### TRANSPORT__FED_FRA_CASUALTIES  (1,150,788 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 100% | 9 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| LATITUDE | coordinates | 6% | 50,429 | clean coordinate |  |
| LONGITUDE | coordinates | 6% | 48,831 | clean coordinate |  |
| COUNTY_CODE | county | 25% | 277 | county code |  |
| COUNTY_NAME | county | 25% | 1,601 | county name |  |
| GENERAL_LOCATION_OF_PERSON | facility_site | 25% | 22 | text place |  |
| GENERAL_LOCATION_OF_PERSON_CODE | facility_site | 25% | 23 | text place |  |
| LOCATION_OF_INJURY_ON_BODY | facility_site | 97% | 14 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| SPECIFIC_LOCATION | facility_site | 51% | 21 | text place |  |
| SPECIFIC_LOCATION_OF_PERSON | facility_site | 25% | 49 | text place |  |
| SPECIFIC_LOCATION_OF_PERSON_CODE | facility_site | 25% | 49 | text place |  |
| STATE_CODE | state | 100% | 52 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| STATE_NAME | state | 100% | 51 | state names (not codes) |  |
### TRANSPORT__FED_FRA_CROSSING_INCIDENTS  (251,149 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| CITY_NAME | city | 83% | 17,790 | text place |  |
| DISTRICT | cong_district | 90% | 9 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| COUNTY_CODE | county | 99% | 285 | county code |  |
| COUNTY_NAME | county | 100% | 2,302 | county name |  |
| CROSSING_WARNING_LOCATION | facility_site | 96% | 3 | text place |  |
| CROSSING_WARNING_LOCATION_CODE | facility_site | 96% | 6 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| STATE_CODE | state | 100% | 52 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| STATE_NAME | state | 100% | 51 | state names (not codes) |  |
### TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS  (224,941 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| DISTRICT | cong_district | 100% | 8 | coded place (numbers) | codes, not names -- needs a lookup to become a place |
| LATITUDE | coordinates | 17% | 27,680 | clean coordinate |  |
| LONGITUDE | coordinates | 17% | 26,574 | clean coordinate |  |
| COUNTY_CODE | county | 98% | 284 | mixed county |  |
| COUNTY_NAME | county | 98% | 1,653 | county name |  |
| LOCATION | facility_site | 31% | 27,466 | text place |  |
| STATE_ABBREVIATION | state | 100% | 50 | clean 2-letter state |  |
| STATE_CODE | state | 100% | 50 | state as a numeric code (FIPS / ICPSR) | not a 2-letter code -- needs a code translation before joining |
| STATE_NAME | state | 100% | 50 | state names (not codes) |  |
### TRANSPORT__FED_FRA_SAFETY  (1 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| COUNTY_FIPS | fips | 0% | 1 | empty | no real values (blank or sentinel only) |
| STATE_FIPS | fips | 0% | 1 | empty | no real values (blank or sentinel only) |
### TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT  (31,503 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| OPER_ADDR_SAME | address | 0% | 1 | empty | no real values (blank or sentinel only) |
| OPER_STREET | address | 26% | 7,040 | text place |  |
| OWNER_STREET | address | 33% | 8,328 | text place |  |
| DEST_CITY | city | 70% | 6,117 | text place |  |
| DPRT_CITY | city | 78% | 6,552 | text place |  |
| OPER_CITY | city | 81% | 6,360 | text place |  |
| OWNER_CITY | city | 83% | 6,329 | text place |  |
| DEST_COUNTRY | country | 73% | 151 | country code |  |
| DPRT_COUNTRY | country | 80% | 146 | country code |  |
| OPER_COUNTRY | country | 93% | 150 | country code |  |
| OWNER_COUNTRY | country | 94% | 149 | country code |  |
| SITE_SEEING | facility_site | 88% | 3 | text place |  |
| DEST_STATE | state | 65% | 58 | clean 2-letter state |  |
| DPRT_STATE | state | 72% | 58 | clean 2-letter state |  |
| OPER_STATE | state | 80% | 57 | clean 2-letter state |  |
| OWNER_STATE | state | 82% | 57 | clean 2-letter state |  |
| OPER_ZIP | zip | 75% | 16,987 | clean ZIP |  |
| OWNER_ZIP | zip | 79% | 18,473 | clean ZIP |  |
### TRANSPORT__FED_NTSB_AVIATION_EVENTS  (30,968 rows)

| column | kind | real fill | distinct | verdict | note |
|---|---|---:|---:|---|---|
| EV_CITY | city | 100% | 10,571 | text place |  |
| DEC_LATITUDE | coordinates | 89% | 21,980 | clean coordinate |  |
| DEC_LONGITUDE | coordinates | 89% | 23,180 | clean coordinate |  |
| LATITUDE | coordinates | 89% | 20,248 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| LONGITUDE | coordinates | 89% | 22,360 | not a coordinate (name-scan false hit) | the name matched LONG/LAT but the values are counts or money |
| EV_COUNTRY | country | 100% | 185 | country code |  |
| LATLONG_ACQ | geometry | 71% | 3 | text place |  |
| EV_STATE | state | 85% | 58 | clean 2-letter state |  |
| EV_SITE_ZIPCODE | zip | 78% | 9,162 | clean ZIP |  |

## Tables that failed to scan

- CRIMINAL_JUSTICE.CRIMINAL_JUSTICE__FED_BJS_DATA: STALE INDEX: the 3 indexed place columns (LOCALITY, MSA, REGION) no longer exist on this mart
- FINANCE.FINANCE__FED_NCUA_CALL_REPORTS: STALE INDEX: mart no longer exists (replaced by the FOICU file, measured separately)
- TRANSPORT.TRANSPORT__FED_FAA_REGISTRY: STALE INDEX: mart no longer exists in the marts database (aircraft registry lives in landing only)
