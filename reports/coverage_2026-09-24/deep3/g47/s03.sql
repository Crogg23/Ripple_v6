-- S03 fertility: REFERENCE copy (text) vs TIMELINE copy (float): row counts, cast failures, value disagreements
WITH r AS (SELECT entity, code, TRY_TO_NUMBER(year) yr, total_fertility_rate tfr_txt,
                  TRY_TO_DOUBLE(total_fertility_rate) tfr
           FROM LIBRARY_MARTS.REFERENCE.REFERENCE__XC_OWID_FERTILITY),
t AS (SELECT entity, code, year yr, total_fertility_rate tfr
      FROM LIBRARY_MARTS.TIMELINE.REFERENCE__XC_OWID_FERTILITY)
SELECT (SELECT COUNT(*) FROM r) r_rows, (SELECT COUNT(*) FROM t) t_rows,
       (SELECT COUNT(*) FROM (SELECT entity, yr FROM r GROUP BY 1,2 HAVING COUNT(*)>1)) r_dup_entity_year,
       (SELECT COUNT_IF(tfr IS NULL) FROM r) r_tfr_nocast,
       (SELECT COUNT_IF(yr IS NULL) FROM r) r_year_nocast,
       (SELECT COUNT_IF(tfr_txt ILIKE 'nan' OR tfr_txt = '') FROM r) r_nan_or_blank,
       (SELECT COUNT(*) FROM r JOIN t ON r.entity=t.entity AND r.yr=t.yr) joined,
       (SELECT COUNT_IF(ABS(r.tfr - t.tfr) > 0.0005) FROM r JOIN t ON r.entity=t.entity AND r.yr=t.yr) value_diff,
       (SELECT MIN(yr)||'-'||MAX(yr) FROM r) r_years
