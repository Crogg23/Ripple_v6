    "FED_FEC_INDIV_CONTRIBUTIONS": {
        # FEC_CMTE_ID -- 12,291 distinct / 84,172,112 rows (100.0% survive norm), +12,291 new to spine. len 9-9. e.g. C00458000
        "key": "FEC_CMTE_ID", "key_col": "CMTE_ID",
        "org": "NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_MSHA_VIOLATIONS": {
        # MINE_ID -- 31,277 distinct / 3,087,266 rows (100.0% survive norm), +31,277 new to spine. len 7-7. e.g. 0101552
        "key": "MINE_ID", "key_col": "MINE_ID",
        "org": "MINE_NAME",
        "authority": 3,
    },
    "FED_EPA_FRS_FULL": {
        # FRS_ID -- 5,300,149 distinct / 5,300,149 rows (100.0% survive norm), +5,300,149 new to spine. len 12-12. e.g. 110006098310
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "org": "PRIMARY_NAME",
        "city": "CITY_NAME", "state": "STATE_CODE", "zip": "POSTAL_CODE",
        "authority": 2,
    },
    "FED_EPA_ECHO": {
        # FRS_ID -- 3,135,553 distinct / 3,135,553 rows (99.29% survive norm), +3,135,553 new to spine. len 12-12. e.g. 110051925538
        "key": "FRS_ID", "key_col": "FRS_ID",
        "org": "FAC_NAME",
        "city": "FAC_CITY", "state": "FAC_STATE",
        "authority": 6,
    },
    "FED_FEC_COMMITTEE_TO_CANDIDATE": {
        # FEC_CMTE_ID -- 6,270 distinct / 866,730 rows (100.0% survive norm), +6,270 new to spine. len 9-9. e.g. C00325324
        "key": "FEC_CMTE_ID", "key_col": "CMTE_ID",
        "org": "NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_MSHA_ACCIDENTS": {
        # MINE_ID -- 13,489 distinct / 273,623 rows (100.0% survive norm), +13,489 new to spine. len 7-7. e.g. 1400413
        "key": "MINE_ID", "key_col": "MINE_ID",
        "authority": 4,
    },
    "FED_EPA_SDWA_SDWA_FACILITIES": {
        # PWSID -- 139,527 distinct / 500,000 rows (100.0% survive norm), +139,527 new to spine. len 9-9. e.g. 020010464
        "key": "PWSID", "key_col": "PWSID",
        "org": "FACILITY_NAME",
        "authority": 2,
    },
    "FED_EPA_FRS_FRS_SIC_CODES": {
        # FRS_ID -- 367,837 distinct / 500,000 rows (100.0% survive norm), +367,837 new to spine. len 12-12. e.g. 110000307739
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS": {
        # FRS_ID -- 27,372 distinct / 500,000 rows (100.0% survive norm), +27,372 new to spine. len 12-12. e.g. 110000314936
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_SITE_VISITS": {
        # PWSID -- 44,779 distinct / 500,000 rows (100.0% survive norm), +44,779 new to spine. len 9-9. e.g. 020000001
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS": {
        # FRS_ID -- 100,507 distinct / 499,984 rows (100.0% survive norm), +100,507 new to spine. len 12-12. e.g. 110006791187
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT": {
        # PWSID -- 15,282 distinct / 500,000 rows (100.0% survive norm), +15,282 new to spine. len 9-9. e.g. 010307001
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_EPA_FRS_FRS_PROGRAM_LINKS": {
        # FRS_ID -- 464,049 distinct / 500,000 rows (100.0% survive norm), +464,049 new to spine. len 12-12. e.g. 110001930386
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "org": "PRIMARY_NAME",
        "city": "CITY_NAME", "state": "STATE_CODE", "zip": "POSTAL_CODE",
        "authority": 6,
    },
    "FED_EPA_FRS_FRS_NAICS_CODES": {
        # FRS_ID -- 356,856 distinct / 499,904 rows (99.98% survive norm), +356,856 new to spine. len 12-12. e.g. 110000460117
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_EPA_NPDES_NPDES_INSPECTIONS": {
        # FRS_ID -- 132,341 distinct / 499,970 rows (99.99% survive norm), +132,341 new to spine. len 12-12. e.g. 110020436125
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_LCR_SAMPLES": {
        # PWSID -- 47,068 distinct / 500,000 rows (100.0% survive norm), +47,068 new to spine. len 9-9. e.g. 020000012
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_FEC_BULK_COMMITTEES": {
        # FEC_CMTE_ID -- 20,007 distinct / 20,007 rows (100.0% survive norm), +20,007 new to spine. len 9-9. e.g. C00017681
        "key": "FEC_CMTE_ID", "key_col": "FEC_CMTE_ID",
        "org": "CMTE_NM",
        "city": "CMTE_CITY", "state": "CMTE_ST", "zip": "CMTE_ZIP",
        "authority": 6,
    },
    "FED_FEC_BULK_CANDIDATES": {
        # FEC_CAND_ID -- 13,240 distinct / 17,900 rows (100.0% survive norm), +13,240 new to spine. len 9-9. e.g. H0AK00105
        "key": "FEC_CAND_ID", "key_col": "CAND_ID",
        "org": "CAND_NAME",
        "authority": 6,
    },
    "FED_FEC_BULK_SUMMARY": {
        # FEC_CAND_ID -- 5,754 distinct / 7,933 rows (100.0% survive norm), +5,754 new to spine. len 9-9. e.g. H2AK01083
        "key": "FEC_CAND_ID", "key_col": "CAND_ID",
        "org": "CAND_NAME",
        "authority": 6,
    },
