-- Cohort-integrity lock: every member lead of one cohort must carry the SAME
-- peer-cohort denominators (cohort_n, cohort_pooled_dart) in its frozen
-- evidence — they were computed once per cohort at detection. Disagreement
-- means mixed detector runs are sharing a cohort_id, and the rollup's MAX()
-- would silently pick one. Also fails if any reviewable OSHA lead has a NULL
-- cohort key (it would fall out of decision inheritance entirely).

WITH members AS (
    SELECT
        evidence[0]:naics::STRING || '|' || evidence[0]:size_band::STRING AS cohort_id,
        evidence[0]:naics::STRING          AS naics,
        evidence[0]:size_band::STRING      AS size_band,
        evidence[0]:cohort_n::NUMBER       AS cohort_n,
        evidence[0]:cohort_pooled_dart::FLOAT AS cohort_pooled_dart,
        lead_id
    FROM {{ source('library_meta_connect', 'V_LEADS_PUBLISHED') }}
    WHERE rule_name = 'osha_cohort_outlier_2024'
      AND review_state IN ('pending', 'needs_work')
)

SELECT 'null_cohort_key' AS problem, lead_id AS detail
FROM members
WHERE naics IS NULL OR size_band IS NULL

UNION ALL

SELECT 'members_disagree', cohort_id
FROM members
GROUP BY cohort_id
HAVING COUNT(DISTINCT cohort_n) > 1
    OR COUNT(DISTINCT cohort_pooled_dart) > 1
