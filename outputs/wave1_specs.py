    "FED_USASPENDING_ASSISTANCE_FULL": {
        # UEI -- 223,721 distinct / 7,788,545 rows (39.13% survive norm), +175,699 new to spine. len 12-12. e.g. Z9Z8L67WXJ85
        "key": "UEI", "key_col": "recipient_uei",
        "org": "recipient_name",
        "authority": 6,
    },
    "FED_OSHA_ITA_CASE_DETAIL_2024": {
        # EIN -- 15,659 distinct / 455,271 rows (91.05% survive norm), +12,243 new to spine. len 9-9. e.g. 742489930
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_IRS_AUTO_REVOCATIONS": {
        # EIN -- 488,994 distinct / 500,000 rows (100.0% survive norm), +15 new to spine. len 9-9. e.g. 002028280
        "key": "EIN", "key_col": "EIN",
        "org": "LEGAL_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_OSHA_ITA_CASE_DETAIL_2023": {
        # EIN -- 24,931 distinct / 445,616 rows (89.12% survive norm), +20,908 new to spine. len 9-9. e.g. 240837325
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_IRS_PUB78_ELIGIBLE_DONEES": {
        # EIN -- 500,000 distinct / 500,000 rows (100.0% survive norm), +3,301 new to spine. len 9-9. e.g. 000587764
        "key": "EIN", "key_col": "EIN",
        "org": "LEGAL_NAME",
        "city": "CITY", "state": "STATE",
        "authority": 6,
    },
    "FED_OSHA_ITA_300A_SUMMARY_2024": {
        # EIN -- 114,605 distinct / 355,358 rows (89.15% survive norm), +101,536 new to spine. len 9-9. e.g. 823106264
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_OSHA_ITA_300A_SUMMARY_2023": {
        # EIN -- 123,210 distinct / 353,304 rows (89.62% survive norm), +109,301 new to spine. len 9-9. e.g. 340892675
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_OSHA_ITA_300A_SUMMARY_2025": {
        # EIN -- 106,219 distinct / 339,964 rows (88.7% survive norm), +93,993 new to spine. len 9-9. e.g. 205134864
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_OSHA_ITA_CASE_DETAIL_2025": {
        # EIN -- 13,387 distinct / 293,328 rows (88.77% survive norm), +10,322 new to spine. len 9-9. e.g. 430652671
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS": {
        # NPI -- 14,421 distinct / 14,425 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1477576346
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 14,251 distinct, +15 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS": {
        # NPI -- 11,467 distinct / 11,508 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1457434003
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 11,413 distinct, +197 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS": {
        # NPI -- 10,269 distinct / 11,063 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1700888542
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 9,955 distinct, +149 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_CMS_HOSPITAL_ENROLLMENTS": {
        # NPI -- 8,717 distinct / 9,175 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1114984671
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 5,966 distinct, +14 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_CMS_HOSPICE_ENROLLMENTS": {
        # NPI -- 6,056 distinct / 6,066 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1548201957
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 4,798 distinct, +43 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS": {
        # NPI -- 5,320 distinct / 5,530 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1497791511
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 5,313 distinct, +45 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_IRS_SOI_CHARITIES": {
        # EIN -- 2,450 distinct / 2,450 rows (100.0% survive norm), +16 new to spine. len 9-9. e.g. 010880225
        "key": "EIN", "key_col": "EIN",
        "org": "NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP",
        "authority": 6,
    },
