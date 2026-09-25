from q import run
M = "LIBRARY_MARTS.HEALTH."
P = f"{M}HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT"
run("S10", "PECOS profile (retry of S09 without lineage columns): keys, enrollment-id date parse, flags",
    f"""SELECT COUNT(*) n, COUNT(DISTINCT NPI) npis, COUNT(DISTINCT ENRLMT_ID) enrl_ids, COUNT(DISTINCT PECOS_ASCT_CNTL_ID) pac_ids,
               COUNT_IF(NPI IS NULL OR TRIM(NPI) = '') npi_blank, COUNT_IF(LENGTH(NPI) <> 10) npi_not10,
               COUNT_IF(LEFT(ENRLMT_ID,1) = 'I') enrl_I, COUNT_IF(LEFT(ENRLMT_ID,1) = 'O') enrl_O,
               COUNT_IF(TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD') IS NULL) enrl_date_bad,
               MIN(TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD')) enrl_d0, MAX(TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD')) enrl_d1,
               COUNT_IF(MULTIPLE_NPI_FLAG = 'Y') multi_y, COUNT(DISTINCT STATE_CD) states,
               COUNT_IF(ORG_NAME IS NOT NULL AND TRIM(ORG_NAME) <> '') org_rows
        FROM {P}""")

run("S11", "PECOS: enrollments by provider type, state and enrollment-id year",
    f"""SELECT PROVIDER_TYPE_CD, PROVIDER_TYPE_DESC, STATE_CD,
               YEAR(TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD')) yr, LEFT(ENRLMT_ID,1) kind,
               COUNT(*) n, COUNT(DISTINCT NPI) npis
        FROM {P} GROUP BY 1,2,3,4,5""")
