# ST_CANNABIS_POLICY_BUNDLES

rows 1.5K  columns 106  scan 6.1s

roles: amount 16, audit 2, category 84, empty 2, state 1, who 1

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PHARMAPPSCALE | 1.5K | 0 | 0 | 75 | 83.33 | 24.0K |
| PHARMIMPSCALE | 1.5K | 0 | 0 | 75 | 83.33 | 20.1K |
| PERMISSIVEAPPSCALE | 1.5K | 0 | 0 | 70.84 | 75 | 18.1K |
| PERMISSIVEIMPSCALE | 1.5K | 0 | 0 | 66.67 | 75 | 17.2K |
| FISCALAPPSCALE | 1.5K | 0 | 0 | 83.33 | 91.67 | 16.0K |
| FISCALIMPSCALE | 1.5K | 0 | 0 | 83.33 | 83.33 | 12.6K |

## who

SRC_SHA256 by rows
      1.5K  4980ed1a55d6f65895ac9ea1e675abe520d77ac468bd5de454eabe0d9f764890

SRC_SHA256 by dollars
       24.0K     1.5K rows  4980ed1a55d6f65895ac9ea1e675abe520d77ac468bd5de454eabe0d9f76

## where

STATE_AB: WY 30, WI 30, WV 30, WA 30, VA 30, VT 30, UT 30, TX 30, TN 30, SD 30, SC 30, RI 30

## what

STATE: Wyoming 8%, Wisconsin 8%, West Virginia 8%, Washington 8%, Virginia 8%, Vermont 8%, Utah 8%, Texas 8%, Tennessee 8%, South Dakota 8%, South Carolina 8%, Rhode Island 8%

FIPS: 45 9%, 56 8%, 55 8%, 54 8%, 53 8%, 51 8%, 50 8%, 49 8%, 48 8%, 47 8%, 46 8%, 42 8%

YEAR: 2023 8%, 2022 8%, 2021 8%, 2020 8%, 2019 8%, 2018 8%, 2017 8%, 2016 8%, 2015 8%, 2014 8%, 2013 8%, 2012 8%

MML_APPROVED: 0 67%, 1 33%

MML_IMP: 0 71%, 1 29%

BALLOT_MEASURE: 0 96%, 1 4%

BM_PASSED: 0 97%, 1 3%

LEGISLATIVE_ACTION: 0 84%, 1 16%

STATE_COURT_SIG_ACTION: 0 97%, 1 3%

REC_CANN_APPROVED: 0 92%, 1 8%

PHARMAPP: 0 67%, 7 6%, 6 6%, 8 5%, 9 4%, 3 3%, 4 3%, 5 2%, 2 2%, 1 2%, 10 0%

PHARMIMP: 0 71%, 7 5%, 6 5%, 8 4%, 3 4%, 9 3%, 4 2%, 2 2%, 5 2%, 1 2%, 10 0%

PERMISSIVEAPP: 0 56%, 1 16%, 4 6%, 3 5%, 2 5%, 5 4%, 6 3%, 8 2%, 7 2%, 9 1%

PERMISSIVEIMP: 0 58%, 1 15%, 4 6%, 3 5%, 2 4%, 5 4%, 6 3%, 8 2%, 7 2%, 9 1%

FISCALAPP: 0 74%, 6 4%, 5 4%, 7 3%, 4 3%, 1 3%, 2 3%, 3 2%, 8 2%, 10 2%, 9 1%, 11 0%

FISCALIMP: 0 80%, 5 4%, 6 3%, 7 3%, 4 2%, 1 2%, 2 2%, 3 2%, 10 1%, 8 1%, 9 1%

GROWING_APP: 0 76%, 1 24%

GROWING_IMP: 0 81%, 1 19%

TESTING_APP: 0 80%, 1 20%

TESTING_IMP: 0 84%, 1 16%

DISP_RESTRICTED_MML_APP: 0 85%, 1 15%

DISP_RESTRICTED_MML_IMP: 0 89%, 1 11%

PHARM_MML_DISP_APP: 0 95%, 1 5%

PHARM_MML_DISP_IMP: 0 96%, 1 4%

NONPROFIT_MML_DISP_APP: 0 91%, 1 9%

NONPROFIT_MML_DISP_IMP: 0 93%, 1 7%

LOCAL_OPTION_MML_APP: 0 91%, 1 9%

LOCA_OPTION_MML_IMP: 0 92%, 1 8%

MML_REGISTRATION_MAND_APP: 0 72%, 1 28%

MML_REGISTRATION_MAND_IMP: 0 75%, 1 25%

RENEW_ANNUAL_MML_APP: 0 73%, 1 27%

RENEW_ANNUAL_MML_IMP: 0 77%, 1 23%

BONA_FIDE_DOC_MML_APP: 0 79%, 1 21%

BONA_FIDE_DOC_MML_IMP: 0 82%, 1 18%

CAREGIVER_LIMIT_MML_APP: 0 77%, 1 23%

CAREGIVER_LIMIT_MML_IMP: 0 80%, 1 20%

MML_TAX_EXEMPT_APP: 0 92%, 1 8%

MML_TAX_EXEMPT_IMP: 0 93%, 1 7%

NO_SMOKING_MML_APP: 0 96%, 1 4%

NO_SMOKING_MML_IMP: 0 97%, 1 3%

SUPPLY_GRAY_APP: 0 93%, 1 7%

SUPPLY_GRAY_IMP: 0 93%, 1 7%

COOPERATIVES_APP: 0 93%, 1 7%

COOPERATIVES_IMP: 0 93%, 1 7%

HOME_CULT_APP: 0 77%, 1 23%

HOME_CULT_IMP: 0 78%, 1 22%

HIGH_PLANTS_MML_APP: 0 94%, 1 6%

HIGH_PLANTS_MML_IMP: 0 94%, 1 6%

CAREGIVER_MML_NO_LIMIT_APP: 0 90%, 1 10%

CAREGIVER_MML_NO_LIMIT_IMP: 0 91%, 1 9%

ALLFORMS_LEGAL_MML_APP: 0 71%, 1 29%

ALLFORMS_LEGAL_MML_IMP: 0 73%, 1 27%

HIGH_USABLE_MML_APP: 0 91%, 1 9%

HIGH_USABLE_MML_IMP: 0 92%, 1 8%

REC_CULT_APP: 0 92%, 1 8%

REC_CULT_IMP: 0 93%, 1 7%

HIGH_RCL_OUNCES_APP: 0 97%, 1 3%

HIGH_RCL_OUNCES_IMP: 0 98%, 1 2%

HOME_CULT_RCL_APP: 0 93%, 1 7%

HOME_CULT_RCL_IMP: 0 93%, 1 7%

HIGH_PLANT_RCL_APP: 0 97%, 1 3%

HIGH_PLANT_RCL_IMP: 0 97%, 1 3%

POSSESSION_NO_JAIL_NO_FELON_APP: 0 66%, 1 34%

POSSESSION_NO_JAIL_NO_FELON_IMP: 0 67%, 1 33%

DISP_APP: 0 76%, 1 24%

DISP_IMP: 0 81%, 1 19%

NO_DISP_LIMIT_MML_APP: 0 93%, 1 7%, 4 0%

NO_DISP_LIMIT_MML_IMP: 0 94%, 1 6%

COMMERCIAL_MML_DISP_APP: 0 85%, 1 15%

COMMERCIAL_MML_DISP_IMP: 0 88%, 1 12%

MML_TAX_APP: 0 87%, 1 13%

MML_TAX_IMP: 0 90%, 1 10%

HI_MML_TAX_APP: 0 89%, 1 11%

HI_MML_TAX_IMP: 0 91%, 1 9%

OTHER_STATES_MML_APP: 0 89%, 1 11%

OTHER_STATES_MML_IMP: 0 91%, 1 9%

REC_CANN_DISP_APP: 0 92%, 1 8%

REC_CANN_DISP_IMP: 0 94%, 1 6%

WHOLESALE_TAX_HIGH_RCL_APP: 0 96%, 1 4%

WHOLESALE_TAX_HIGH_RCL_IMP: 0 97%, 1 3%

RETAIL_TAX_RCL_HIGH_APP: 0 93%, 1 7%

RETAIL_TAX_RCL_HIGH_IMP: 0 95%, 1 5%

STATE_SALES_TAX_HIGH_RCL_APP: 0 94%, 1 6%

STATE_SALES_TAX_HIGH_RCL_IMP: 0 96%, 1 4%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| STATE | category | 49 | 0 | Wyoming 30; Wisconsin 30; West Virginia 30; Washington 30 |
| STATE_AB | state | 50 | 0 | WY 30; WI 30; WV 30; WA 30 |
| FIPS | category | 50 | 0 | 45 31; 56 30; 55 30; 54 30 |
| YEAR | category | 30 | 0 | 2023 50; 2022 50; 2021 50; 2020 50 |
| MML_APPROVED | category | 2 | 0 | 0 1.0K; 1 499 |
| MML_IMP | category | 2 | 0 | 0 1.1K; 1 439 |
| BALLOT_MEASURE | category | 2 | 0 | 0 1.4K; 1 58 |
| BM_PASSED | category | 2 | 0 | 0 1.5K; 1 41 |
| LEGISLATIVE_ACTION | category | 2 | 0 | 0 1.3K; 1 233 |
| STATE_COURT_SIG_ACTION | category | 2 | 0 | 0 1.5K; 1 43 |
| REC_CANN_APPROVED | category | 2 | 0 | 0 1.4K; 1 127 |
| PHARMAPP | category | 11 | 0 | 0 1.0K; 7 92; 6 87; 8 70 |
| PHARMIMP | category | 11 | 0 | 0 1.1K; 7 76; 6 74; 8 55 |
| PERMISSIVEAPP | category | 10 | 0 | 0 837; 1 234; 4 94; 3 76 |
| PERMISSIVEIMP | category | 10 | 0 | 0 867; 1 228; 4 90; 3 79 |
| FISCALAPP | category | 12 | 0 | 0 1.1K; 6 61; 5 60; 7 46 |
| FISCALIMP | category | 11 | 0 | 0 1.2K; 5 55; 6 51; 7 39 |
| PHARMAPPSCALE | amount | 11 | 0 | 0 1.0K; 58.333333333333336 92; 50 87; 66.66666666666666 70 |
| PHARMIMPSCALE | amount | 11 | 0 | 0 1.1K; 58.333333333333336 76; 50 74; 66.66666666666666 55 |
| PERMISSIVEAPPSCALE | amount | 10 | 0 | 0 837; 8.333333333333332 234; 33.33333333333333 94; 25 76 |
| PERMISSIVEIMPSCALE | amount | 10 | 0 | 0 867; 8.333333333333332 228; 33.33333333333333 90; 25 79 |
| FISCALAPPSCALE | amount | 12 | 0 | 0 1.1K; 50 61; 41.66666666666667 60; 58.333333333333336 46 |
| FISCALIMPSCALE | amount | 11 | 0 | 0 1.2K; 41.66666666666667 55; 50 51; 58.333333333333336 39 |
| PHARMAPPSCALEZ | amount | 11 | 0 | 0 1.0K; 58.333333333333336 92; 50 88; 66.66666666666666 69 |
| PHARMIMPSCALEZ | amount | 11 | 0 | 0 1.1K; 58.333333333333336 76; 50 74; 66.66666666666666 55 |
| PERMISSIVEAPPSCALEZ | amount | 10 | 0 | 0 837; 8.333333333333332 234; 33.33333333333333 94; 25 76 |
| PERMISSIVEIMPSCALEZ | amount | 10 | 0 | 0 867; 8.333333333333332 228; 33.33333333333333 90; 25 79 |
| FISCALAPPSCALEZ | amount | 12 | 0 | 0 1.1K; 50 61; 41.66666666666667 60; 58.333333333333336 46 |
| FISCALIMPSCALEZ | amount | 11 | 0 | 0 1.2K; 41.66666666666667 55; 50 51; 58.333333333333336 39 |
| GROWING_APP | category | 2 | 0 | 0 1.1K; 1 358 |
| GROWING_IMP | category | 2 | 0 | 0 1.2K; 1 283 |
| TESTING_APP | category | 2 | 0 | 0 1.2K; 1 304 |
| TESTING_IMP | category | 2 | 0 | 0 1.3K; 1 242 |
| DISP_RESTRICTED_MML_APP | category | 2 | 0 | 0 1.3K; 1 229 |
| DISP_RESTRICTED_MML_IMP | category | 2 | 0 | 0 1.3K; 1 171 |
| PHARM_MML_DISP_APP | category | 2 | 0 | 0 1.4K; 1 73 |
| PHARM_MML_DISP_IMP | category | 2 | 0 | 0 1.4K; 1 59 |
| NONPROFIT_MML_DISP_APP | category | 2 | 0 | 0 1.4K; 1 136 |
| NONPROFIT_MML_DISP_IMP | category | 2 | 0 | 0 1.4K; 1 103 |
| LOCAL_OPTION_MML_APP | category | 2 | 0 | 0 1.4K; 1 136 |
| LOCA_OPTION_MML_IMP | category | 2 | 0 | 0 1.4K; 1 122 |
| MML_REGISTRATION_MAND_APP | category | 2 | 0 | 0 1.1K; 1 417 |
| MML_REGISTRATION_MAND_IMP | category | 2 | 0 | 0 1.1K; 1 369 |
| RENEW_ANNUAL_MML_APP | category | 2 | 0 | 0 1.1K; 1 403 |
| RENEW_ANNUAL_MML_IMP | category | 2 | 0 | 0 1.1K; 1 352 |
| BONA_FIDE_DOC_MML_APP | category | 2 | 0 | 0 1.2K; 1 311 |
| BONA_FIDE_DOC_MML_IMP | category | 2 | 0 | 0 1.2K; 1 272 |
| CAREGIVER_LIMIT_MML_APP | category | 2 | 0 | 0 1.2K; 1 344 |
| CAREGIVER_LIMIT_MML_IMP | category | 2 | 0 | 0 1.2K; 1 298 |
| MML_TAX_EXEMPT_APP | category | 2 | 0 | 0 1.4K; 1 113 |
| MML_TAX_EXEMPT_IMP | category | 2 | 0 | 0 1.4K; 1 98 |
| NO_SMOKING_MML_APP | category | 2 | 0 | 0 1.4K; 1 62 |
| NO_SMOKING_MML_IMP | category | 2 | 0 | 0 1.5K; 1 38 |
| COL_53 | empty | 1 | 1.5K |  |
| SUPPLY_GRAY_APP | category | 2 | 0 | 0 1.4K; 1 109 |
| SUPPLY_GRAY_IMP | category | 2 | 0 | 0 1.4K; 1 104 |
| COOPERATIVES_APP | category | 2 | 0 | 0 1.4K; 1 103 |
| COOPERATIVES_IMP | category | 2 | 0 | 0 1.4K; 1 103 |
| HOME_CULT_APP | category | 2 | 0 | 0 1.2K; 1 339 |
| HOME_CULT_IMP | category | 2 | 0 | 0 1.2K; 1 328 |
| HIGH_PLANTS_MML_APP | category | 2 | 0 | 0 1.4K; 1 97 |
| HIGH_PLANTS_MML_IMP | category | 2 | 0 | 0 1.4K; 1 93 |
| CAREGIVER_MML_NO_LIMIT_APP | category | 2 | 0 | 0 1.4K; 1 143 |
| CAREGIVER_MML_NO_LIMIT_IMP | category | 2 | 0 | 0 1.4K; 1 132 |
| ALLFORMS_LEGAL_MML_APP | category | 2 | 0 | 0 1.1K; 1 437 |
| ALLFORMS_LEGAL_MML_IMP | category | 2 | 0 | 0 1.1K; 1 403 |
| HIGH_USABLE_MML_APP | category | 2 | 0 | 0 1.4K; 1 130 |
| HIGH_USABLE_MML_IMP | category | 2 | 0 | 0 1.4K; 1 121 |
| REC_CULT_APP | category | 2 | 0 | 0 1.4K; 1 116 |
| REC_CULT_IMP | category | 2 | 0 | 0 1.4K; 1 105 |
| HIGH_RCL_OUNCES_APP | category | 2 | 0 | 0 1.5K; 1 40 |
| HIGH_RCL_OUNCES_IMP | category | 2 | 0 | 0 1.5K; 1 37 |
| HOME_CULT_RCL_APP | category | 2 | 0 | 0 1.4K; 1 108 |
| HOME_CULT_RCL_IMP | category | 2 | 0 | 0 1.4K; 1 98 |
| HIGH_PLANT_RCL_APP | category | 2 | 0 | 0 1.5K; 1 46 |
| HIGH_PLANT_RCL_IMP | category | 2 | 0 | 0 1.5K; 1 39 |
| POSSESSION_NO_JAIL_NO_FELON_APP | category | 2 | 0 | 0 991; 1 509 |
| POSSESSION_NO_JAIL_NO_FELON_IMP | category | 2 | 0 | 0 998; 1 502 |
| COL_78 | empty | 1 | 1.5K |  |
| DISP_APP | category | 2 | 0 | 0 1.1K; 1 357 |
| DISP_IMP | category | 2 | 0 | 0 1.2K; 1 278 |
| DISP_FEE_HIGH_APP | amount | 2 | 0 | 0 1.4K; 1 136 |
| DISP_FEE_HIGH_IMP | amount | 2 | 0 | 0 1.4K; 1 116 |
| NO_DISP_LIMIT_MML_APP | category | 3 | 0 | 0 1.4K; 1 110; 4 1 |
| NO_DISP_LIMIT_MML_IMP | category | 2 | 0 | 0 1.4K; 1 94 |
| COMMERCIAL_MML_DISP_APP | category | 2 | 0 | 0 1.3K; 1 227 |
| COMMERCIAL_MML_DISP_IMP | category | 2 | 0 | 0 1.3K; 1 186 |
| GROW_FEE_HIGH_APP | amount | 2 | 0 | 0 1.3K; 1 180 |
| GROW_FEE_HIGH_IMP | amount | 2 | 0 | 0 1.4K; 1 147 |
| MML_TAX_APP | category | 2 | 0 | 0 1.3K; 1 188 |
| MML_TAX_IMP | category | 2 | 0 | 0 1.3K; 1 154 |
| HI_MML_TAX_APP | category | 2 | 0 | 0 1.3K; 1 171 |
| HI_MML_TAX_IMP | category | 2 | 0 | 0 1.4K; 1 139 |
| OTHER_STATES_MML_APP | category | 2 | 0 | 0 1.3K; 1 170 |
| OTHER_STATES_MML_IMP | category | 2 | 0 | 0 1.4K; 1 132 |
| REC_CANN_DISP_APP | category | 2 | 0 | 0 1.4K; 1 121 |
| REC_CANN_DISP_IMP | category | 2 | 0 | 0 1.4K; 1 87 |
| WHOLESALE_TAX_HIGH_RCL_APP | category | 2 | 0 | 0 1.4K; 1 55 |
| WHOLESALE_TAX_HIGH_RCL_IMP | category | 2 | 0 | 0 1.5K; 1 39 |
| RETAIL_TAX_RCL_HIGH_APP | category | 2 | 0 | 0 1.4K; 1 112 |
| RETAIL_TAX_RCL_HIGH_IMP | category | 2 | 0 | 0 1.4K; 1 78 |
| STATE_SALES_TAX_HIGH_RCL_APP | category | 2 | 0 | 0 1.4K; 1 87 |
| STATE_SALES_TAX_HIGH_RCL_IMP | category | 2 | 0 | 0 1.4K; 1 60 |
| INGESTED_AT | audit | 1 | 0 | 1782616954638468 1.5K |
| SOURCE_RUN_ID | audit | 1 | 0 | e9e7dbf4-dc5b-410d-8c26-2 1.5K |
| SRC_SHA256 | who | 1 | 0 | 4980ed1a55d6f65895ac9ea1e 1.5K |
