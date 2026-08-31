-- Q6: Does industry money move prescriptions? (association only, no causal claim)
-- Open Payments has NO drug/product columns in this warehouse, so manufacturer->drug matching is
-- infeasible; fallback shape: prescribers bucketed by industry-money decile vs brand-vs-generic
-- prescribing, within the 15 largest specialties.
-- Grain: specialty x payment bucket ('0: no payment' + paid deciles D1..D10, D10 = most paid).
WITH op AS (  -- industry money per NPI, Open Payments 2022-2024
    SELECT NPI, SUM(TRY_TO_DOUBLE(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) AS ind_dollars
    FROM (
        SELECT NPI, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
        UNION ALL SELECT NPI, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023
        UNION ALL SELECT NPI, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022
    )
    WHERE NPI IS NOT NULL AND NPI NOT IN ('','nan')
    GROUP BY NPI
),
partd AS (
    SELECT NPI,
           NULLIF(PRSCRBR_TYPE,'nan') AS specialty,
           TRY_TO_DOUBLE(TOT_CLMS)          AS tot_clms,
           TRY_TO_DOUBLE(TOT_DRUG_CST)      AS tot_cst,
           TRY_TO_DOUBLE(BRND_TOT_CLMS)     AS brnd_clms,
           TRY_TO_DOUBLE(BRND_TOT_DRUG_CST) AS brnd_cst,
           TRY_TO_DOUBLE(GNRC_TOT_CLMS)     AS gnrc_clms,
           TRY_TO_DOUBLE(GNRC_TOT_DRUG_CST) AS gnrc_cst
    FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS
    WHERE NPI IS NOT NULL AND NPI NOT IN ('','nan')
      AND TRY_TO_DOUBLE(TOT_CLMS) >= 50           -- enough volume for a stable brand share
      AND TRY_TO_DOUBLE(BRND_TOT_CLMS) IS NOT NULL
      AND TRY_TO_DOUBLE(GNRC_TOT_CLMS) IS NOT NULL -- drop suppressed brand/generic cells
),
top_spec AS (
    SELECT specialty FROM partd GROUP BY specialty
    ORDER BY COUNT(*) DESC LIMIT 15
),
joined AS (
    SELECT p.*, COALESCE(o.ind_dollars, 0) AS ind_dollars,
           CASE WHEN COALESCE(o.ind_dollars,0) <= 0 THEN '00: no payment'
                ELSE 'D' || LPAD(NTILE(10) OVER (
                        PARTITION BY IFF(COALESCE(o.ind_dollars,0) > 0, 1, 0)
                        ORDER BY o.ind_dollars), 2, '0')
           END AS pay_bucket
    FROM partd p
    JOIN top_spec t ON t.specialty = p.specialty
    LEFT JOIN op o ON o.NPI = p.NPI
)
SELECT specialty,
       pay_bucket,                                    -- deciles computed across all 15 specialties pooled
       COUNT(*) AS n_prescribers,
       ROUND(MEDIAN(ind_dollars),0)                       AS median_industry_dollars,
       ROUND(MIN(IFF(ind_dollars>0, ind_dollars, NULL)),0) AS bucket_min_dollars,
       ROUND(MAX(ind_dollars),0)                          AS bucket_max_dollars,
       ROUND(100*SUM(brnd_clms)/NULLIF(SUM(brnd_clms)+SUM(gnrc_clms),0),2) AS brand_claim_share_pct,
       ROUND(100*SUM(brnd_cst)/NULLIF(SUM(brnd_cst)+SUM(gnrc_cst),0),2)    AS brand_cost_share_pct,
       ROUND(MEDIAN(brnd_clms/NULLIF(brnd_clms+gnrc_clms,0))*100,2)        AS median_prescriber_brand_share_pct,
       ROUND(AVG(tot_cst),0)   AS avg_total_drug_cost,
       ROUND(MEDIAN(tot_cst),0) AS median_total_drug_cost
FROM joined
GROUP BY specialty, pay_bucket
ORDER BY specialty, pay_bucket
