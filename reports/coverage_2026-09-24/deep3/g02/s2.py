from q import run
M = "LIBRARY_MARTS.HEALTH."
OP = f"{M}HEALTH__FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE"

run("S05", "Hospital general: type, ownership, stars for every CCN",
    f"""SELECT CCN, FACILITY_NAME, CITY_TOWN, STATE, HOSPITAL_TYPE, HOSPITAL_OWNERSHIP, HOSPITAL_OVERALL_RATING
        FROM {M}HEALTH__FED_CMS_HOSPITAL_GENERAL""")

run("S06", "HCRIS cost-to-charge and outpatient charges by fiscal year, CCNs in the outpatient file, FY2016+",
    f"""WITH op AS (SELECT DISTINCT RNDRNG_PRVDR_CCN AS CCN FROM {OP})
        SELECT h.PROVIDER_CCN, h.FISCAL_YEAR_BEGIN_DATE, h.FISCAL_YEAR_END_DATE, h.RPT_REC_NUM, h.TYPE_OF_CONTROL, h.PROVIDER_TYPE,
               h.NUMBER_OF_BEDS, h.COST_TO_CHARGE_RATIO, h.OUTPATIENT_TOTAL_CHARGES, h.INPATIENT_TOTAL_CHARGES,
               h.COMBINED_OUTPATIENT_INPATIENT_TOTAL_CHARGES, h.TOTAL_COSTS, h.NET_PATIENT_REVENUE
        FROM {M}HEALTH__FED_CMS_HCRIS h JOIN op ON op.CCN = h.PROVIDER_CCN
        WHERE TRY_TO_DATE(h.FISCAL_YEAR_END_DATE::STRING) >= '2016-01-01'""")

run("S07", "POS: first-participation and termination dates for CCNs in the outpatient file (carbon date)",
    f"""WITH op AS (SELECT DISTINCT RNDRNG_PRVDR_CCN AS CCN FROM {OP})
        SELECT p.CCN, p.FAC_NAME, p.ORGNL_PRTCPTN_DT, p.CRTFCTN_DT, p.TRMNTN_EXPRTN_DT, p.PGM_TRMNTN_CD, p.CHOW_DT
        FROM {M}HEALTH__FED_CMS_POS_OTHER p JOIN op ON op.CCN = p.CCN""")

run("S08", "CDC injury county: all Drug_OD rows (FIPS join target for 2019-2024)",
    f"""SELECT GEOID, NAME, PERIOD, ST_NAME, INTENT, COUNT_SUP, RATE, RATE_M
        FROM {M}HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY WHERE INTENT = 'Drug_OD'""")

P = f"{M}HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT"
run("S09", "PECOS profile: keys, enrollment-id date parse, flags",
    f"""SELECT COUNT(*) n, COUNT(DISTINCT NPI) npis, COUNT(DISTINCT ENRLMT_ID) enrl_ids, COUNT(DISTINCT PECOS_ASCT_CNTL_ID) pac_ids,
               COUNT_IF(NPI IS NULL OR TRIM(NPI) = '') npi_blank, COUNT_IF(LENGTH(NPI) <> 10) npi_not10,
               COUNT_IF(LEFT(ENRLMT_ID,1) = 'I') enrl_I, COUNT_IF(LEFT(ENRLMT_ID,1) = 'O') enrl_O,
               COUNT_IF(TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD') IS NULL) enrl_date_bad,
               MIN(TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD')) enrl_d0, MAX(TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD')) enrl_d1,
               COUNT_IF(MULTIPLE_NPI_FLAG = 'Y') multi_y, COUNT(DISTINCT STATE_CD) states,
               COUNT_IF(ORG_NAME IS NOT NULL AND TRIM(ORG_NAME) <> '') org_rows,
               COUNT(DISTINCT _SOURCE_RUN_ID) runs, MIN(_INGESTED_AT)::STRING ing0, MAX(_INGESTED_AT)::STRING ing1
        FROM {P}""")

run("S10", "PECOS: enrollments by provider type, state and enrollment-id year",
    f"""SELECT PROVIDER_TYPE_CD, PROVIDER_TYPE_DESC, STATE_CD,
               YEAR(TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD')) yr, LEFT(ENRLMT_ID,1) kind,
               COUNT(*) n, COUNT(DISTINCT NPI) npis
        FROM {P} GROUP BY 1,2,3,4,5""")
