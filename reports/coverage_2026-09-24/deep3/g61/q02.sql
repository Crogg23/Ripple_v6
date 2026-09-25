-- OWNER: per generator, do the owner shares add to 100%? by status
WITH g AS (
  SELECT PLANT_CODE, GENERATOR_ID, MAX(STATUS) st, COUNT(DISTINCT STATUS) nst, COUNT(*) n_own,
         SUM(PERCENT_OWNED) s, MIN(PERCENT_OWNED) mn, MAX(PERCENT_OWNED) mx
  FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER GROUP BY 1,2)
SELECT st, COUNT(*) gens, SUM(n_own) rows_, SUM(IFF(ABS(s-1)<0.0051,1,0)) sum_1, SUM(IFF(s<0.9949,1,0)) under_1,
       SUM(IFF(s>1.0051,1,0)) over_1, SUM(IFF(nst>1,1,0)) mixed_status, ROUND(AVG(n_own),2) avg_owners, MAX(n_own) max_owners,
       SUM(IFF(n_own=1,1,0)) single_owner_rows, MIN(mn) min_pct, MAX(mx) max_pct, SUM(IFF(mn IS NULL,1,0)) null_pct
FROM g GROUP BY ROLLUP(st) ORDER BY gens DESC
