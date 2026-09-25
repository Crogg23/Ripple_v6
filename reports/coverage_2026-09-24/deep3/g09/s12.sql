WITH irfp AS (SELECT DISTINCT SUBSTR(ccn,1,2) || '0' || SUBSTR(ccn,4,3) pccn FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF WHERE SUBSTR(ccn,3,1) = 'T'),
pos AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1),
p AS (SELECT pos.*, irfp.pccn IS NOT NULL in_irf FROM pos LEFT JOIN irfp ON irfp.pccn = pos.ccn
      WHERE pos.rehab_unit_sw = 'Y' OR pos.rehab_unit_efctv_dt IS NOT NULL OR pos.rehab_unit_trmntn_dt IS NOT NULL)
SELECT state_cd = 'FL' is_fl, COUNT(*) any_rehab_unit_history,
       COUNT_IF(rehab_unit_sw = 'Y') sw_y, COUNT_IF(rehab_unit_sw = 'Y' AND pgm_trmntn_cd = '00') sw_y_hosp_active,
       COUNT_IF(rehab_unit_trmntn_dt IS NOT NULL) unit_term_dated, COUNT_IF(rehab_unit_sw = 'Y' AND rehab_unit_trmntn_dt IS NOT NULL) sw_y_but_term_dated,
       COUNT_IF(rehab_unit_efctv_dt < '2021-01-01') eff_pre2021, COUNT_IF(rehab_unit_efctv_dt < '2021-01-01' AND rehab_unit_sw = 'Y') eff_pre2021_sw_y,
       COUNT_IF(in_irf) in_irf_list,
       COUNT_IF(rehab_unit_sw = 'Y' AND pgm_trmntn_cd = '00' AND rehab_unit_trmntn_dt IS NULL AND NOT in_irf) active_unit_missing_from_irf,
       (SELECT OBJECT_AGG(COALESCE(v::VARCHAR,'null'), c) FROM (SELECT rehab_unit_trmntn_cd v, COUNT(*) c FROM p GROUP BY 1)) term_codes_all_states,
       ARRAY_SLICE(ARRAY_AGG(IFF(NOT in_irf AND rehab_unit_sw = 'Y' AND pgm_trmntn_cd = '00', ccn || ' ' || COALESCE(rehab_unit_efctv_dt::VARCHAR,'-') || ' term:' || COALESCE(rehab_unit_trmntn_dt::VARCHAR,'-') || ' beds:' || COALESCE(rehab_unit_bed_cnt::VARCHAR,'-') || ' ' || LEFT(fac_name,30), NULL)), 0, 8) sample_missing,
       (SELECT OBJECT_AGG(y::VARCHAR, c) FROM (SELECT YEAR(rehab_unit_trmntn_dt) y, COUNT(*) c FROM p WHERE rehab_unit_trmntn_dt >= '2010-01-01' GROUP BY 1)) unit_terms_by_year_all_states
FROM p GROUP BY 1 ORDER BY 1
