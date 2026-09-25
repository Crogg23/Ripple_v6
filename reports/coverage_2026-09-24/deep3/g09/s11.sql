WITH irf AS (
  SELECT i.*, k.kind, IFF(k.kind = 'unit', SUBSTR(i.ccn,1,2) || '0' || SUBSTR(i.ccn,4,3), i.ccn) pos_ccn
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF i,
       LATERAL (SELECT CASE WHEN SUBSTR(i.ccn,3,1) IN ('T','R') THEN 'unit'
                            WHEN TRY_TO_NUMBER(SUBSTR(i.ccn,3,4)) BETWEEN 3025 AND 3099 THEN 'freestanding' ELSE 'other' END kind) k),
posall AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER),
scope AS (SELECT COUNT(*) pos_rows, COUNT(DISTINCT ccn) pos_ccns, COUNT_IF(prvdr_ctgry_cd = '01') pos_hosp_rows,
                 COUNT_IF(rehab_unit_sw = 'Y') pos_rehab_sw_y, MAX(crtfctn_dt) pos_max_cert, MAX(rehab_unit_efctv_dt) pos_max_rehab_eff,
                 MAX(chow_dt) pos_max_chow FROM posall),
pos AS (SELECT * FROM posall QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1)
SELECT irf.kind, irf.state = 'FL' is_fl, irf.certification_date >= '2019-07-01' is_new, COUNT(*) n, COUNT(pos.ccn) landed,
       COUNT_IF(pos.pgm_trmntn_cd = '00') pos_active,
       COUNT_IF(irf.certification_date = pos.orgnl_prtcptn_dt) eq_orig_particip,
       COUNT_IF(irf.certification_date = pos.crtfctn_dt) eq_pos_cert,
       COUNT_IF(irf.certification_date = pos.rehab_unit_efctv_dt) eq_rehab_unit_eff,
       COUNT_IF(pos.rehab_unit_sw = 'Y') parent_rehab_sw_y,
       COUNT_IF(pos.chow_cnt > 0) chow_any, COUNT_IF(pos.chow_dt >= '2019-07-01') chow_since_2019h2,
       SUM(IFF(irf.kind = 'unit', pos.rehab_unit_bed_cnt, NULL)) unit_rehab_beds, SUM(IFF(irf.kind = 'freestanding', pos.bed_cnt, NULL)) fs_beds,
       ANY_VALUE(scope.pos_rows) pos_rows, ANY_VALUE(scope.pos_ccns) pos_ccns, ANY_VALUE(scope.pos_hosp_rows) pos_hosp_rows,
       ANY_VALUE(scope.pos_rehab_sw_y) pos_rehab_sw_y, ANY_VALUE(scope.pos_max_cert) pos_max_cert, ANY_VALUE(scope.pos_max_rehab_eff) pos_max_rehab_eff,
       ANY_VALUE(scope.pos_max_chow) pos_max_chow,
       ARRAY_SLICE(ARRAY_AGG(irf.ccn || ' ' || irf.certification_date || ' pos:' || COALESCE(pos.orgnl_prtcptn_dt::VARCHAR,'-') || '/' || COALESCE(pos.crtfctn_dt::VARCHAR,'-') || '/' || COALESCE(pos.rehab_unit_efctv_dt::VARCHAR,'-') || ' ' || LEFT(COALESCE(pos.fac_name, irf.provider_name),30)), 0, 3) eyeball
FROM irf LEFT JOIN pos ON pos.ccn = irf.pos_ccn CROSS JOIN scope
GROUP BY 1,2,3 ORDER BY 1,2,3
