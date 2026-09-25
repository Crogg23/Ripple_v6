-- S18 CPI time check: in each year, how many countries scored below every earlier year since 2012 (a new low)? Is 2024 unusual?
WITH t AS (SELECT entity, year, corruption_perceptions_index s FROM LIBRARY_MARTS.POLITICS.POLITICS__XC_OWID_CPI WHERE year >= 2012),
f AS (SELECT entity, MAX(IFF(year = 2012, s, NULL)) s12 FROM t GROUP BY 1),
x AS (SELECT t.entity, t.year, t.s, f.s12,
             MIN(t.s) OVER (PARTITION BY t.entity ORDER BY t.year ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) prior_min,
             MAX(t.s) OVER (PARTITION BY t.entity ORDER BY t.year ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) prior_max,
             t.s - LAG(t.s) OVER (PARTITION BY t.entity ORDER BY t.year) yoy
      FROM t JOIN f USING (entity))
SELECT year, COUNT(*) n, COUNT_IF(s < prior_min) new_low, COUNT_IF(s > prior_max) new_high,
       COUNT_IF(s < prior_min AND s12 >= 60) new_low_s12_60plus, COUNT_IF(s12 >= 60) n_s12_60plus,
       MEDIAN(yoy) med_yoy, MEDIAN(IFF(s12 >= 60, yoy, NULL)) med_yoy_60plus, COUNT_IF(yoy <= -3) drop3plus
FROM x WHERE year >= 2014 GROUP BY 1 ORDER BY 1
