-- S22 UDS site Medicare billing numbers -> CMS Provider of Services (POS other) on CCN: category, termination code and date, name, state
WITH s AS (SELECT DISTINCT TRIM(fqhc_site_medicare_billing_number) ccn FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES
           WHERE NULLIF(TRIM(fqhc_site_medicare_billing_number),'') IS NOT NULL)
SELECT s.ccn, p.prvdr_ctgry_cd, p.prvdr_ctgry_sbtyp_cd, p.pgm_trmntn_cd, p.trmntn_exprtn_dt, p.fac_name, p.city_name, p.state_cd,
       p.crtfctn_dt, p.orgnl_prtcptn_dt, p.fed_fundd_fqhc_sw
FROM s LEFT JOIN LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER p ON p.ccn = s.ccn
