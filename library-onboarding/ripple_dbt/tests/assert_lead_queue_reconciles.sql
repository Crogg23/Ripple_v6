-- Reconciliation lock: LEAD_QUEUE row count must EXACTLY equal the reviewable
-- population in the safe view. Returns rows on mismatch (test fails), zero
-- rows when reconciled. A mismatch is a defect, not a rounding error — see
-- the failure playbook ("queue count != lead count") before touching anything.

WITH queue_side AS (
    SELECT COUNT(*) AS n FROM {{ ref('lead_queue') }}
),
view_side AS (
    SELECT COUNT(*) AS n
    FROM {{ source('library_meta_connect', 'V_LEADS_PUBLISHED') }}
    WHERE review_state IN ('pending', 'needs_work')
)
SELECT
    q.n AS queue_rows,
    v.n AS reviewable_leads
FROM queue_side q
CROSS JOIN view_side v
WHERE q.n <> v.n
