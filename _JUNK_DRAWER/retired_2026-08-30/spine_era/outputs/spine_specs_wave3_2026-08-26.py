    "FED_SAM_EXCLUSIONS": {
        # UEI -- 3,210 distinct / 3,482 rows (34.82% survive norm), +5 new to spine. len 12-12. e.g. GRX8CJ2ZCNL5
        "key": "UEI", "key_col": "UEI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "org": "ENTITY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP",
        "authority": 6,
    },
    "IRS527_8871_ORGS": {
        # EIN -- 58,915 distinct / 77,590 rows (100.0% survive norm), +0 new to spine. len 9-9. e.g. 912082049
        "key": "EIN", "key_col": "EIN",
        "org": "ORGANIZATION_NAME",
        "city": "MAILING_CITY", "state": "MAILING_STATE", "zip": "MAILING_ZIP",
        "authority": 6,
    },
    "FED_US_SEC_EDGAR": {
        # CIK -- 25 distinct / 48,990 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0000320193
        "key": "CIK", "key_col": "CIK",
        "org": "ENTITY_NAME",
        # extra: EIN -- 24 distinct, +0 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_EDGAR": {
        # CIK -- 20 distinct / 200 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0001318605
        "key": "CIK", "key_col": "CIK",
        # extra: EIN -- 19 distinct, +0 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
