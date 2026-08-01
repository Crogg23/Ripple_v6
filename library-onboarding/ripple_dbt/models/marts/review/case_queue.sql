{{ config(materialized='view', copy_grants=true, schema='REVIEW') }}

-- ============================================================================
-- CASE_QUEUE -- the Case Desk person/entity grouping over LEAD_QUEUE
-- ============================================================================
-- GRAIN:    one row per flagged person or entity (unit) across the hard-ID
--           detectors. The 2026-08-01 audit found 179 people appearing as up
--           to 3 separate leads; the Case Desk reviews the PERSON once, with
--           every claim about them in one case file. Decisions stay per-lead
--           (each lead is a distinct claim) -- this view only groups.
-- KEY:      unit_id = entity_a_key_type || '|' || entity_a_key_value.
-- EXCLUDES: osha_cohort_outlier_2024 (reviewed on the Pattern Desk via
--           COHORT_QUEUE) and the superseded sanctioned_vessel_broadcasting
--           v1 (retired to STATUS='stale' by provision_pattern_desk.sql --
--           the filter here is belt-and-braces until that runs).
-- ============================================================================

WITH units AS (

    SELECT
        entity_a_key_type || '|' || entity_a_key_value        AS unit_id,
        entity_a_key_type,
        entity_a_key_value,
        COUNT(*)                                              AS n_leads,
        ARRAY_AGG(DISTINCT detector)
            WITHIN GROUP (ORDER BY detector)                  AS detectors,
        MAX(priority_score)                                   AS max_priority_score,
        SUM(IFF(review_state = 'needs_work', 1, 0))           AS n_needs_work,
        SUM(IFF(COALESCE(first_name_conflict, FALSE), 1, 0))  AS n_name_conflicts
    FROM {{ ref('lead_queue') }}
    WHERE detector NOT IN ('osha_cohort_outlier_2024',
                           'sanctioned_vessel_broadcasting')
    GROUP BY 1, 2, 3

),

-- The unit's display identity and lead list come from its member leads,
-- ordered by the leads' own priority (best lead fronts the unit).
ranked_leads AS (

    SELECT
        entity_a_key_type || '|' || entity_a_key_value        AS unit_id,
        lead_id,
        detector,
        headline,
        entity_a_name,
        confidence_tier,
        priority_score,
        priority_rank,
        ROW_NUMBER() OVER (
            PARTITION BY entity_a_key_type || '|' || entity_a_key_value
            ORDER BY priority_score DESC, lead_id)            AS lead_seq
    FROM {{ ref('lead_queue') }}
    WHERE detector NOT IN ('osha_cohort_outlier_2024',
                           'sanctioned_vessel_broadcasting')

),

lead_arrays AS (

    SELECT
        unit_id,
        ARRAY_AGG(lead_id) WITHIN GROUP (ORDER BY lead_seq)   AS lead_ids
    FROM ranked_leads
    GROUP BY unit_id

),

top_lead AS (

    SELECT unit_id, lead_id AS top_lead_id, headline AS top_headline,
           entity_a_name AS unit_name, confidence_tier AS best_tier
    FROM ranked_leads
    WHERE lead_seq = 1

)

SELECT
    u.unit_id,
    ROW_NUMBER() OVER (ORDER BY u.max_priority_score DESC, u.unit_id)
                                                              AS unit_rank,
    t.unit_name,
    u.entity_a_key_type,
    u.entity_a_key_value,
    u.n_leads,
    u.detectors,
    t.best_tier,
    u.max_priority_score,
    u.n_needs_work,
    u.n_name_conflicts,
    t.top_lead_id,
    t.top_headline,
    la.lead_ids
FROM units u
JOIN top_lead    t  ON t.unit_id  = u.unit_id
JOIN lead_arrays la ON la.unit_id = u.unit_id
