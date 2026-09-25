WITH fs AS (SELECT ccn, state, UPPER(TRIM(city_town)) city, certification_date cd, provider_name, ownership_type
            FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF
            WHERE TRY_TO_NUMBER(SUBSTR(ccn,3,4)) BETWEEN 3025 AND 3099 AND certification_date >= '2019-07-01'),
pos AS (SELECT ccn, state_cd, UPPER(TRIM(city_name)) city, fac_name, rehab_unit_trmntn_dt, rehab_unit_bed_cnt
        FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER
        WHERE rehab_unit_trmntn_dt IS NOT NULL
        QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1),
m AS (SELECT fs.*, pos.ccn unit_parent, pos.fac_name unit_parent_name, pos.rehab_unit_trmntn_dt unit_closed, pos.rehab_unit_bed_cnt unit_beds
      FROM fs LEFT JOIN pos ON pos.state_cd = fs.state AND pos.city = fs.city AND ABS(DATEDIFF(day, pos.rehab_unit_trmntn_dt, fs.cd)) <= 180)
SELECT state = 'FL' is_fl, COUNT(DISTINCT ccn) new_fs, COUNT(DISTINCT IFF(unit_parent IS NOT NULL, ccn, NULL)) with_same_city_unit_close_180d,
       ARRAY_AGG(IFF(unit_parent IS NOT NULL, state || ' ' || cd || ' ' || LEFT(provider_name,35) || ' <- ' || unit_closed || ' ' || LEFT(unit_parent_name,30) || ' ' || unit_beds || 'b', NULL)) pairs
FROM m GROUP BY 1 ORDER BY 1
