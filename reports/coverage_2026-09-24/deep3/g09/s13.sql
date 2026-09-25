WITH irf AS (
  SELECT i.*, CASE WHEN SUBSTR(i.ccn,3,1) IN ('T','R') THEN 'unit'
                   WHEN TRY_TO_NUMBER(SUBSTR(i.ccn,3,4)) BETWEEN 3025 AND 3099 THEN 'fs' ELSE 'other' END kind
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF i WHERE i.state IN ('FL','NC') AND i.certification_date >= '2019-07-01'),
pos AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1)
SELECT irf.state, irf.certification_date, irf.kind, irf.ccn, irf.ownership_type, LEFT(irf.provider_name, 55) name, irf.city_town,
       pos.mlt_fac_org_name chain_in_pos, IFF(irf.kind = 'unit', pos.rehab_unit_bed_cnt, pos.bed_cnt) beds,
       pos.chow_dt last_chow
FROM irf LEFT JOIN pos ON pos.ccn = IFF(irf.kind = 'unit', SUBSTR(irf.ccn,1,2) || '0' || SUBSTR(irf.ccn,4,3), irf.ccn)
ORDER BY irf.state, irf.certification_date
