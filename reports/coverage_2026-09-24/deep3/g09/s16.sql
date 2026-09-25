WITH fs AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF WHERE TRY_TO_NUMBER(SUBSTR(ccn,3,4)) BETWEEN 3025 AND 3099),
pos AS (SELECT ccn, bed_cnt FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1)
SELECT fs.state, COUNT_IF(fs.certification_date < '2019-07-01') fs_before, COUNT_IF(fs.certification_date >= '2019-07-01') fs_new,
       COUNT_IF(fs.certification_date >= '2014-07-01' AND fs.certification_date < '2019-07-01') fs_new_5y_before,
       SUM(IFF(fs.certification_date < '2019-07-01', pos.bed_cnt, 0)) beds_before, SUM(IFF(fs.certification_date >= '2019-07-01', pos.bed_cnt, 0)) beds_new,
       ROUND(COUNT_IF(fs.certification_date >= '2019-07-01') / NULLIF(COUNT_IF(fs.certification_date < '2019-07-01'), 0), 2) growth
FROM fs LEFT JOIN pos ON pos.ccn = fs.ccn
GROUP BY 1 ORDER BY fs_new DESC, growth DESC
