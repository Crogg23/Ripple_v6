    "INTL_GLEIF_REPEX": {
        # LEI -- 3,142,660 distinct / 6,259,489 rows (100.0% survive norm), +2,288 new to spine. len 20-20. e.g. 549300WO7OWX61PJ9L13
        "key": "LEI", "key_col": "LEI",
        "authority": 6,
    },
    "FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY": {
        # CCN -- 232 distinct / 495,726 rows (99.15% survive norm), +0 new to spine. len 6-6. e.g. 015015
        "key": "CCN", "key_col": "CCN",
        "org": "PROVIDER_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_CMS_ORDER_AND_REFERRING": {
        # NPI -- 2,018,350 distinct / 2,018,354 rows (100.0% survive norm), +1,439 new to spine. len 10-10. e.g. 1427676618
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS": {
        # PWSID -- 413,877 distinct / 578,198 rows (100.0% survive norm), +264,183 new to spine. len 9-9. e.g. NH1835020
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT": {
        # NPI -- 2,541,258 distinct / 2,978,925 rows (100.0% survive norm), +322 new to spine. len 10-10. e.g. 1407802119
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "org": "ORG_NAME",
        "state": "STATE_CD",
        "authority": 6,
    },
    "FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING": {
        # NPI -- 2,047,826 distinct / 2,047,828 rows (100.0% survive norm), +1,525 new to spine. len 10-10. e.g. 1639656747
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "authority": 6,
    },
    "FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI": {
        # NPI -- 61,879 distinct / 500,000 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1003000126
        "key": "NPI", "key_col": "RNDRNG_NPI",
        "person": ["RNDRNG_PRVDR_LAST_ORG_NAME", "RNDRNG_PRVDR_FIRST_NAME"],
        "city": "RNDRNG_PRVDR_CITY", "state": "RNDRNG_PRVDR_STATE_ABRVTN", "zip": "RNDRNG_PRVDR_ZIP5",
        "authority": 6,
    },
    "FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE": {
        # NPI -- 453,202 distinct / 503,917 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1295197580
        "key": "NPI", "key_col": "NPI",
        "authority": 6,
    },
    "FED_CMS_MEDICARE_DIALYSIS_FACILITIES": {
        # CCN -- 335 distinct / 500,000 rows (100.0% survive norm), +34 new to spine. len 6-6. e.g. 012501
        "key": "CCN", "key_col": "CCN",
        "org": "PROVIDER_NAME",
        "city": "CITY", "state": "STATE",
        # extra: NPI -- 332 distinct, +1 new to spine
        "extra_keys": [{"key": "NPI", "key_col": "NPI"}],
        "authority": 6,
    },
    "FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER": {
        # NPI -- 1,296,739 distinct / 1,296,739 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1003008095
        "key": "NPI", "key_col": "RNDRNG_NPI",
        "person": ["RNDRNG_PRVDR_LAST_ORG_NAME", "RNDRNG_PRVDR_FIRST_NAME"],
        "city": "RNDRNG_PRVDR_CITY", "state": "RNDRNG_PRVDR_STATE_ABRVTN", "zip": "RNDRNG_PRVDR_ZIP5",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS": {
        # PWSID -- 434,040 distinct / 434,040 rows (100.0% survive norm), +280,388 new to spine. len 9-9. e.g. MN1640004
        "key": "PWSID", "key_col": "PWSID",
        "org": "ORG_NAME",
        "city": "CITY_NAME", "state": "STATE_CODE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_SERVICE_AREAS": {
        # PWSID -- 378,450 distinct / 422,464 rows (100.0% survive norm), +243,657 new to spine. len 9-9. e.g. 020011103
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_CMS_NURSING_HOME_DEFICIENCIES": {
        # CCN -- 14,384 distinct / 413,370 rows (98.78% survive norm), +0 new to spine. len 6-6. e.g. 015012
        "key": "CCN", "key_col": "CMS_CERTIFICATION_NUMBER_CCN",
        "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_EVENTS_MILESTONES": {
        # PWSID -- 98,555 distinct / 394,075 rows (100.0% survive norm), +55,599 new to spine. len 9-9. e.g. MO6036128
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_PN_VIOLATION_ASSOC": {
        # PWSID -- 42,034 distinct / 387,627 rows (100.0% survive norm), +29,148 new to spine. len 9-9. e.g. 020000004
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES": {
        # FRS_ID -- 266,026 distinct / 279,541 rows (99.93% survive norm), +57 new to spine. len 12-12. e.g. 110007133654
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "org": "FACILITY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_FEC_INDEPENDENT_EXPENDITURES": {
        # FEC_CAND_ID -- 2,014 distinct / 228,643 rows (87.59% survive norm), +607 new to spine. len 9-9. e.g. P80000722
        "key": "FEC_CAND_ID", "key_col": "cand_id",
        "org": "cand_name",
        "authority": 6,
    },
    "FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS": {
        # FRS_ID -- 156,326 distinct / 259,137 rows (99.46% survive norm), +2,486 new to spine. len 12-12. e.g. 110070715963
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "org": "FACILITY_NAME",
        "authority": 6,
    },
    "FED_EPA_ICIS_FEC_CASE_FACILITIES": {
        # FRS_ID -- 113,854 distinct / 203,232 rows (99.61% survive norm), +70 new to spine. len 12-12. e.g. 110000318193
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "org": "FACILITY_NAME",
        "city": "CITY", "state": "STATE_CODE", "zip": "ZIP",
        "authority": 6,
    },
    "FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES": {
        # CCN -- 13,687 distinct / 197,027 rows (98.5% survive norm), +0 new to spine. len 6-6. e.g. 015009
        "key": "CCN", "key_col": "CMS_CERTIFICATION_NUMBER_CCN",
        "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_MSHA_MINES": {
        # MINE_ID -- 91,906 distinct / 91,906 rows (100.0% survive norm), +60,478 new to spine. len 7-7. e.g. 0100099
        "key": "MINE_ID", "key_col": "MINE_ID",
        "state": "STATE",
        "authority": 6,
    },
    "FED_SEC_EDGAR_INSIDERS": {
        # CIK -- 5,306 distinct / 69,259 rows (100.0% survive norm), +190 new to spine. len 10-10. e.g. 0001825079
        "key": "CIK", "key_col": "CIK",
        "authority": 6,
    },
    "FED_CMS_OPT_OUT_AFFIDAVITS": {
        # NPI -- 56,455 distinct / 57,209 rows (100.0% survive norm), +19 new to spine. len 10-10. e.g. 1699854034
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "city": "CITY_NAME", "state": "STATE_CODE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_US_SEC_EDGAR": {
        # CIK -- 25 distinct / 48,990 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0001652044
        "key": "CIK", "key_col": "CIK",
        "org": "ENTITY_NAME",
        # extra: EIN -- 24 distinct, +11 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS": {
        # FRS_ID -- 14,606 distinct / 21,930 rows (100.0% survive norm), +8 new to spine. len 12-12. e.g. 110000308569
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_FEC_BULK": {
        # FEC_CMTE_ID -- 20,938 distinct / 20,938 rows (100.0% survive norm), +5,166 new to spine. len 9-9. e.g. C00003764
        "key": "FEC_CMTE_ID", "key_col": "FEC_CMTE_ID",
        "org": "CMTE_NM",
        "city": "CMTE_CITY", "state": "CMTE_ST", "zip": "CMTE_ZIP",
        "authority": 6,
    },
    "FED_FEC_LEADERSHIP_PAC": {
        # FEC_CMTE_ID -- 8,338 distinct / 8,619 rows (100.0% survive norm), +3,464 new to spine. len 9-9. e.g. C00708867
        "key": "FEC_CMTE_ID", "key_col": "FEC_COMMITTEE_ID",
        "authority": 6,
    },
    "FED_FEC_BULK_LINKAGES": {
        # FEC_CMTE_ID -- 11,427 distinct / 16,327 rows (100.0% survive norm), +3,493 new to spine. len 9-9. e.g. C00708867
        "key": "FEC_CMTE_ID", "key_col": "CMTE_ID",
        "authority": 6,
    },
    "FED_CMS_NURSING_HOME_PENALTIES": {
        # CCN -- 6,771 distinct / 16,032 rows (99.09% survive norm), +0 new to spine. len 6-6. e.g. 015019
        "key": "CCN", "key_col": "CMS_CERTIFICATION_NUMBER_CCN",
        "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2024Q2": {
        # CIK -- 6,250 distinct / 7,675 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0000038725
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,745 distinct, +3,714 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS": {
        # NPI -- 7,240 distinct / 7,240 rows (100.0% survive norm), +361 new to spine. len 10-10. e.g. 1215687991
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2025Q2": {
        # CIK -- 6,081 distinct / 7,009 rows (100.0% survive norm), +41 new to spine. len 10-10. e.g. 0001034054
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,509 distinct, +3,523 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS": {
        # NPI -- 6,880 distinct / 6,880 rows (100.0% survive norm), +453 new to spine. len 10-10. e.g. 1245159342
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2024Q3": {
        # CIK -- 6,008 distinct / 6,699 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0000002178
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,687 distinct, +3,671 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS": {
        # NPI -- 6,510 distinct / 6,637 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1003046806
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "state": "STATE",
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2025Q3": {
        # CIK -- 5,909 distinct / 6,541 rows (100.0% survive norm), +57 new to spine. len 10-10. e.g. 0000010795
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,495 distinct, +3,511 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2024Q4": {
        # CIK -- 5,833 distinct / 6,491 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0001315257
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,664 distinct, +3,650 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2025Q4": {
        # CIK -- 5,786 distinct / 6,304 rows (100.0% survive norm), +88 new to spine. len 10-10. e.g. 0000002969
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,502 distinct, +3,517 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2025Q1": {
        # CIK -- 5,672 distinct / 6,231 rows (100.0% survive norm), +18 new to spine. len 10-10. e.g. 0000015615
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,306 distinct, +3,316 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2026Q1": {
        # CIK -- 5,750 distinct / 6,169 rows (100.0% survive norm), +95 new to spine. len 10-10. e.g. 0000015847
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,237 distinct, +3,281 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2024Q1": {
        # CIK -- 5,506 distinct / 6,028 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0000316888
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,239 distinct, +3,234 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_IRS_EO_PR": {
        # EIN -- 2,587 distinct / 2,587 rows (100.0% survive norm), +29 new to spine. len 9-9. e.g. 660356920
        "key": "EIN", "key_col": "EIN",
        "org": "NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP",
        "authority": 6,
    },
    "FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS": {
        # NPI -- 1,287 distinct / 1,502 rows (96.41% survive norm), +0 new to spine. len 10-10. e.g. 1003008301
        "key": "NPI", "key_col": "NPI",
        "org": "PROVIDER_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP",
        "authority": 6,
    },
    "FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM": {
        # NPI -- 307 distinct / 1,037 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1619988144
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_SEC_CLOSED_END_FUND_INFORMATION": {
        # CIK -- 973 distinct / 973 rows (100.0% survive norm), +650 new to spine. len 10-10. e.g. 0000879361
        "key": "CIK", "key_col": "CIK",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_SEC_BUSINESS_DEVELOPMENT_COMPANY_REPORT": {
        # CIK -- 212 distinct / 212 rows (100.0% survive norm), +72 new to spine. len 10-10. e.g. 0001287032
        "key": "CIK", "key_col": "CIK",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_SEC_EDGAR": {
        # CIK -- 20 distinct / 200 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0001652044
        "key": "CIK", "key_col": "CIK",
        # extra: EIN -- 19 distinct, +9 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_USASPENDING_CONTRACTS_FULL": {
        # UEI -- 420,990 distinct / 19,999,806 rows (100.0% survive norm), +316,786 new to spine. len 12-12. e.g. KB1EKZ5BXVL8
        "key": "UEI", "key_col": "recipient_uei",
        "org": "recipient_name",
        "authority": 6,
    },
