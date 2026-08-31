-- Q2: Banned providers (OIG LEIE exclusion list) still receiving industry money (CMS Open Payments)
-- Grain: one row per excluded provider NPI x Open Payments program year (2022/2023/2024 vintages unioned).
-- after_exclusion_flag = payment program year >= exclusion year AND not reinstated before that year.
WITH pay AS (
    SELECT NPI, PROGRAM_YEAR, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS AS amt FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
    UNION ALL
    SELECT NPI, PROGRAM_YEAR, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023
    UNION ALL
    SELECT NPI, PROGRAM_YEAR, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022
),
pay_agg AS (
    SELECT NPI,
           TRY_TO_NUMBER(PROGRAM_YEAR) AS pay_year,
           COUNT(*) AS n_payments,
           SUM(TRY_TO_DOUBLE(amt)) AS total_dollars
    FROM pay
    WHERE NPI IS NOT NULL AND NPI NOT IN ('', 'nan')
    GROUP BY 1, 2
),
leie AS (
    -- one row per NPI: earliest exclusion (a provider can appear more than once)
    SELECT NPI,
           MIN(TRY_TO_DATE(EXCLUSION_DATE, 'YYYYMMDD')) AS exclusion_date,
           MAX(TRY_TO_DATE(NULLIF(NULLIF(REINSTATEMENT_DATE,'nan'),''), 'YYYYMMDD')) AS reinstatement_date,
           MAX(EXCLUSION_TYPE) AS exclusion_type,
           MAX(GENERAL_CATEGORY) AS general_category,
           MAX(NULLIF(SPECIALTY,'nan')) AS specialty,
           MAX(STATE) AS state
    FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
    WHERE NPI IS NOT NULL AND NPI NOT IN ('', 'nan', '0000000000')
    GROUP BY NPI
)
SELECT l.NPI AS npi,
       l.exclusion_type,
       l.general_category,
       l.specialty,
       l.state,
       YEAR(l.exclusion_date) AS exclusion_year,
       YEAR(l.reinstatement_date) AS reinstatement_year,
       p.pay_year,
       p.n_payments,
       ROUND(p.total_dollars, 2) AS total_dollars,
       IFF(p.pay_year >= YEAR(l.exclusion_date)
           AND (l.reinstatement_date IS NULL OR p.pay_year <= YEAR(l.reinstatement_date)),
           1, 0) AS after_exclusion_flag
FROM pay_agg p
JOIN leie l ON l.NPI = p.NPI
ORDER BY total_dollars DESC
