-- Reconciliation lock: the Pattern Desk mart must account for EVERY
-- reviewable osha_cohort_outlier_2024 lead — SUM(n_outliers) across cohorts
-- equals the reviewable OSHA population in the safe view. Returns rows on
-- mismatch (test fails), zero rows when reconciled.

WITH cohort_side AS (
    SELECT COALESCE(SUM(n_outliers), 0) AS n FROM {{ ref('cohort_queue') }}
),
view_side AS (
    SELECT COUNT(*) AS n
    FROM {{ source('library_meta_connect', 'V_LEADS_PUBLISHED') }}
    WHERE rule_name = 'osha_cohort_outlier_2024'
      AND review_state IN ('pending', 'needs_work')
)
SELECT
    c.n AS cohort_member_total,
    v.n AS reviewable_osha_leads
FROM cohort_side c
CROSS JOIN view_side v
WHERE c.n <> v.n
