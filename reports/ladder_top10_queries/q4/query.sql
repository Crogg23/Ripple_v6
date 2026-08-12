-- Q4: One doctor, whole footprint — census version.
-- Grain: one row per Part D prescriber specialty (PRSCRBR_TYPE).
-- For every prescriber in Part D: their Part D drug cost, whether/how much industry money they
-- got (Open Payments 2022-2024 summed), their Medicare Part B payments, and LEIE exclusion status.
WITH partd AS (
    SELECT NPI,
           NULLIF(PRSCRBR_TYPE,'nan') AS specialty,
           TRY_TO_DOUBLE(TOT_DRUG_CST) AS drug_cost,
           TRY_TO_DOUBLE(TOT_CLMS)     AS claims
    FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS
    WHERE NPI IS NOT NULL AND NPI NOT IN ('','nan')
),
op AS (  -- industry money per NPI, all three program years
    SELECT NPI, SUM(TRY_TO_DOUBLE(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) AS industry_dollars
    FROM (
        SELECT NPI, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
        UNION ALL SELECT NPI, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023
        UNION ALL SELECT NPI, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022
    )
    WHERE NPI IS NOT NULL AND NPI NOT IN ('','nan')
    GROUP BY NPI
),
mcare AS (  -- Medicare Part B payments per NPI
    SELECT NPI, SUM(TOT_MDCR_PYMT_AMT) AS medicare_pymt
    FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER
    WHERE NPI IS NOT NULL AND NPI NOT IN ('','nan')
    GROUP BY NPI
),
leie AS (
    SELECT DISTINCT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
    WHERE NPI IS NOT NULL AND NPI NOT IN ('','nan','0000000000')
)
SELECT p.specialty,
       COUNT(*)                                   AS n_prescribers,
       ROUND(SUM(p.drug_cost),0)                  AS total_partd_drug_cost,
       ROUND(MEDIAN(p.drug_cost),0)               AS median_partd_drug_cost,
       COUNT_IF(o.NPI IS NOT NULL)                AS n_with_industry_money,
       ROUND(100*COUNT_IF(o.NPI IS NOT NULL)/COUNT(*),1) AS pct_paid,
       ROUND(SUM(o.industry_dollars),0)           AS total_industry_dollars,
       ROUND(MEDIAN(o.industry_dollars),0)        AS median_industry_dollars_paid_only,
       ROUND(MEDIAN(CASE WHEN o.NPI IS NOT NULL THEN p.drug_cost END),0) AS median_drug_cost_paid,
       ROUND(MEDIAN(CASE WHEN o.NPI IS NULL     THEN p.drug_cost END),0) AS median_drug_cost_unpaid,
       COUNT_IF(m.NPI IS NOT NULL)                AS n_in_medicare_partb,
       ROUND(SUM(m.medicare_pymt),0)              AS total_medicare_partb_pymt,
       COUNT_IF(x.NPI IS NOT NULL)                AS n_excluded_leie
FROM partd p
LEFT JOIN op    o ON o.NPI = p.NPI
LEFT JOIN mcare m ON m.NPI = p.NPI
LEFT JOIN leie  x ON x.NPI = p.NPI
GROUP BY p.specialty
HAVING COUNT(*) >= 25
ORDER BY total_partd_drug_cost DESC
