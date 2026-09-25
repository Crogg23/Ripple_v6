WITH pos AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1),
irf AS (SELECT ccn, certification_date FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF)
SELECT IFF(TRY_TO_NUMBER(SUBSTR(pos.ccn,3,4)) BETWEEN 3025 AND 3099, 'rehab_hospital_ccn', 'parent_with_unit') what,
       pos.ccn, LEFT(pos.fac_name, 40) fac_name, pos.city_name, pos.orgnl_prtcptn_dt, pos.pgm_trmntn_cd, pos.trmntn_exprtn_dt,
       pos.rehab_unit_efctv_dt, pos.rehab_unit_trmntn_dt, pos.rehab_unit_trmntn_cd, pos.rehab_unit_bed_cnt, pos.bed_cnt,
       COALESCE(i1.certification_date, i2.certification_date) irf_cert, pos.chow_dt
FROM pos
LEFT JOIN irf i1 ON i1.ccn = pos.ccn
LEFT JOIN irf i2 ON SUBSTR(i2.ccn,3,1) = 'T' AND SUBSTR(i2.ccn,1,2) || '0' || SUBSTR(i2.ccn,4,3) = pos.ccn
WHERE pos.state_cd = 'FL' AND pos.prvdr_ctgry_cd = '01'
  AND (TRY_TO_NUMBER(SUBSTR(pos.ccn,3,4)) BETWEEN 3025 AND 3099 OR pos.rehab_unit_efctv_dt IS NOT NULL OR pos.rehab_unit_trmntn_dt IS NOT NULL)
ORDER BY what DESC, COALESCE(pos.rehab_unit_efctv_dt, pos.orgnl_prtcptn_dt)
