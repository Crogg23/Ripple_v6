WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_UNII_GSRS_SUBSTANCES)
SELECT COUNT(*) n, COUNT(DISTINCT unii) unii_nd, COUNT(DISTINCT gsrs_uuid) uuid_nd, COUNT(DISTINCT display_name) name_nd,
       (SELECT MAX(c) FROM (SELECT COUNT(*) c FROM t GROUP BY unii)) max_rows_per_unii,
       COUNT_IF(unii = 'XTN6536VE6') rows_battery_top_unii,
       COUNT_IF(NULLIF(TRIM(cas_rn),'') IS NOT NULL) cas_filled,
       (SELECT MAX(c) FROM (SELECT COUNT(*) c FROM t WHERE NULLIF(TRIM(cas_rn),'') IS NOT NULL GROUP BY cas_rn)) max_rows_per_cas,
       COUNT_IF(cas_rn = '48126-51-8') rows_battery_top_cas,
       COUNT(ec_number) ec_nn, COUNT_IF(NULLIF(TRIM(rxcui),'') IS NOT NULL) rxcui_filled,
       COUNT_IF(NULLIF(TRIM(dailymed_name),'') IS NOT NULL) dailymed_name_filled, MAX(dailymed_name) dailymed_name_max,
       COUNT(DISTINCT _source_run_id) runs,
       (SELECT OBJECT_AGG(COALESCE(substance_type,'(null)'), c) FROM (SELECT substance_type, COUNT(*) c FROM t GROUP BY 1)) by_type
FROM t
