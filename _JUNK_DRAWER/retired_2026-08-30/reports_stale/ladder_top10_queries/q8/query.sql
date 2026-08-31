-- Q8: EINs on IRS Pub 78 eligible-donee list that also appear on the IRS auto-revocation list
-- Revocation source: ECONOMICS__FED_IRS_REVOCATION (1.19M rows, deduped by EIN, has WAS_REINSTATED)
-- chosen over FED_IRS_AUTO_REVOCATIONS (1.21M, has ~19k dup EINs, same content)
-- EINs normalized by stripping non-digits. Neither table hit a 500k cap (both >1.1M).

-- by revocation year (result.csv):

WITH p AS (SELECT DISTINCT REGEXP_REPLACE(EIN,'[^0-9]','') ein FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_PUB78_ELIGIBLE_DONEES),
r AS (SELECT REGEXP_REPLACE(EIN,'[^0-9]','') ein, WAS_REINSTATED, YEAR(TRY_TO_DATE(REVOCATION_DATE,'DD-MON-YYYY')) rev_year
      FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_REVOCATION)
SELECT rev_year,
       SUM(IFF(WAS_REINSTATED,1,0)) reinstated_still_listed,
       SUM(IFF(NOT WAS_REINSTATED,1,0)) never_reinstated_still_listed,
       COUNT(*) total_overlap
FROM p JOIN r ON p.ein=r.ein
GROUP BY 1 ORDER BY 1


-- by state (by_state.csv):

WITH p AS (SELECT DISTINCT REGEXP_REPLACE(EIN,'[^0-9]','') ein FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_PUB78_ELIGIBLE_DONEES),
r AS (SELECT REGEXP_REPLACE(EIN,'[^0-9]','') ein, WAS_REINSTATED, STATE
      FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_REVOCATION)
SELECT COALESCE(NULLIF(STATE,''),'(none)') state,
       SUM(IFF(WAS_REINSTATED,1,0)) reinstated_still_listed,
       SUM(IFF(NOT WAS_REINSTATED,1,0)) never_reinstated_still_listed,
       COUNT(*) total_overlap
FROM p JOIN r ON p.ein=r.ein
GROUP BY 1 ORDER BY total_overlap DESC
