WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_NLM_DAILYMED_SPL_SETID_MAP)
SELECT COUNT(*) n, COUNT(DISTINCT setid) setid_nd, COUNT(DISTINCT zip_file_name) zip_nd,
       (SELECT MAX(c) FROM (SELECT COUNT(*) c FROM t GROUP BY setid)) max_rows_per_setid,
       COUNT_IF(setid = 'f435e79d-dea3-49dc-8268-146c60ba52a1') rows_battery_top_setid,
       MIN(upload_date) d0, MAX(upload_date) d1, COUNT_IF(upload_date > CURRENT_DATE) future,
       MAX(spl_version) max_ver, MEDIAN(spl_version) med_ver, COUNT_IF(spl_version = 1) ver1,
       COUNT_IF(NULLIF(TRIM(title),'') IS NULL) title_blank, COUNT(DISTINCT _source_run_id) runs,
       (SELECT OBJECT_AGG(y::VARCHAR, c) FROM (SELECT YEAR(upload_date) y, COUNT(*) c FROM t GROUP BY 1)) by_year,
       (SELECT ARRAY_AGG(v || ' | ' || d || ' | ' || LEFT(ti, 70)) FROM (SELECT spl_version v, upload_date d, title ti FROM t ORDER BY spl_version DESC LIMIT 6)) top_versions
FROM t
