WITH pb AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_PURPLE_BOOK),
refs AS (SELECT DISTINCT LOWER(TRIM(ref_product_proper_name)) ref FROM pb WHERE license_type LIKE '351(k)%' AND ref_product_proper_name IS NOT NULL),
kname AS (SELECT LOWER(TRIM(proper_name)) pn, MIN(approval_date) k_first FROM pb WHERE license_type LIKE '351(k)%' GROUP BY 1),
pd AS (SELECT data_year, LOWER(TRIM(generic_name)) g, brand_name b, COUNT(*) prescriber_rows,
              SUM(total_claims) claims, SUM(total_drug_cost) cost
       FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS GROUP BY 1,2,3),
yr AS (SELECT data_year, SUM(prescriber_rows) rows_all, SUM(cost) cost_all FROM pd GROUP BY 1)
SELECT r.ref, pd.data_year, IFF(k.pn IS NOT NULL, 'biosimilar', 'reference/other') role, pd.g, pd.b,
       pd.prescriber_rows, pd.claims, ROUND(pd.cost) cost, k.k_first, yr.rows_all, ROUND(yr.cost_all) cost_all
FROM pd JOIN refs r ON pd.g = r.ref OR pd.g LIKE r.ref || '-%' OR pd.g LIKE r.ref || ',%' OR pd.g LIKE r.ref || ' %'
LEFT JOIN kname k ON k.pn = pd.g
JOIN yr ON yr.data_year = pd.data_year
ORDER BY r.ref, pd.data_year, pd.cost DESC
