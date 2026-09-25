WITH n AS (SELECT ccn, state, certification_date cd, SUBSTR(ccn,1,2) || '0' || SUBSTR(ccn,4,3) pccn
           FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF WHERE SUBSTR(ccn,3,1) = 'T' AND certification_date >= '2019-07-01'),
pos AS (SELECT ccn, rehab_unit_bed_cnt ub, IFF(psych_unit_trmntn_dt IS NULL, psych_unit_bed_cnt, 0) pb
        FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1),
h AS (SELECT provider_ccn, fiscal_year_end_date fye, number_of_beds_total_all_subproviders - number_of_beds sub
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS WHERE provider_ccn IN (SELECT pccn FROM n))
SELECT n.state, n.ccn, n.cd, pos.ub unit_beds, pos.pb psych_beds,
       COUNT(h.fye) hcris_reports, MAX(h.fye) last_fye,
       ROUND(AVG(IFF(h.fye < n.cd AND h.fye >= DATEADD(year, -3, n.cd), h.sub, NULL)), 1) sub_beds_3y_before,
       ROUND(AVG(IFF(h.fye >= DATEADD(year, 1, n.cd), h.sub, NULL)), 1) sub_beds_after_1y
FROM n LEFT JOIN pos ON pos.ccn = n.pccn LEFT JOIN h ON h.provider_ccn = n.pccn
GROUP BY 1,2,3,4,5 ORDER BY n.state, n.cd
