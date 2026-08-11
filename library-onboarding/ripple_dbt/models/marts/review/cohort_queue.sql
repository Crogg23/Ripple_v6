{{ config(materialized='table', copy_grants=true, schema='REVIEW') }}

-- ============================================================================
-- COHORT_QUEUE -- the Pattern Desk triage mart
-- ============================================================================
-- GRAIN:    one row per peer cohort (NAICS-4 x employer size band) that has at
--           least one reviewable osha_cohort_outlier_2024 lead. The Pattern
--           Desk reviews the COHORT (the pattern); member leads are receipts.
-- KEY:      cohort_id = naics || '|' || size_band -- the detector's natural
--           cohort key (connect/cohort.py builds cohorts on exactly this pair;
--           there is no cohort_id column on LEADS, so it is derived here and
--           in LIBRARY_META.REVIEW.V_LEAD_COHORT_MAP identically).
-- DECISION: TARGET_KIND='cohort', TARGET_ID=cohort_id in REVIEW.DECISIONS.
--           Specific-beats-general: a lead-level decision always wins for that
--           lead; the cohort verdict fills in only for undecided members
--           (LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS).
-- HEADLINE: fixed SQL template, nothing model-generated, every substituted
--           field COALESCE-wrapped. ASCII punctuation only in literals (the
--           mojibake guard test enforces the built output).
-- CAVEATS:  self-reported Form 300A inputs travel on every cohort; a cohort
--           containing physically implausible DART rates (> 50) says so and
--           excludes those rows from its receipts sample.
-- EIN NOTE: n_rejoin_failures counts members whose EIN (normalized exactly
--           like connect/keys.py 'pad 9' -- parity test
--           tests/test_cohort_queue_parity.py) no longer rejoins the raw
--           300A table. Visibility for the key-drift audit finding, not a
--           drop condition.
-- ============================================================================

WITH members AS (

    SELECT
        lead_id,
        left_key_value                                        AS ein_est_key,
        SPLIT_PART(left_key_value, '|', 1)                    AS ein_raw,
        SPLIT_PART(left_key_value, '|', 2)                    AS est_key,
        title,
        first_seen,
        last_seen,
        as_of_date,
        review_state,
        evidence[0]:naics::STRING                             AS naics,
        evidence[0]:industry::STRING                          AS industry,
        evidence[0]:size_band::STRING                         AS size_band,
        evidence[0]:city::STRING                              AS city,
        evidence[0]:state::STRING                             AS state,
        evidence[0]:employees::NUMBER                         AS employees,
        evidence[0]:hours::NUMBER                             AS hours,
        evidence[0]:dart_rate::FLOAT                          AS dart_rate,
        evidence[0]:dart_cases::NUMBER                        AS dart_cases,
        evidence[0]:deaths::NUMBER                            AS deaths,
        evidence[0]:fold_vs_pooled::FLOAT                     AS fold_vs_pooled,
        evidence[0]:cohort_n::NUMBER                          AS cohort_n,
        evidence[0]:cohort_pooled_dart::FLOAT                 AS cohort_pooled_dart,
        -- The detector's establishment name lives in TITLE ("Name (CITY, ST) ...");
        -- keep the whole title for the receipts sample rather than parsing it.
        evidence[0]:dart_rate::FLOAT > 50                     AS implausible_rate
    FROM {{ source('library_meta_connect', 'V_LEADS_PUBLISHED') }}
    WHERE rule_name = 'osha_cohort_outlier_2024'
      AND review_state IN ('pending', 'needs_work')

),

-- EIN rejoin check (audit F6 visibility). The normalization below is a
-- CHARACTER-FOR-CHARACTER copy of connect/keys.py normalize_sql('EIN', col)
-- ('pad' mode, width 9: digits only, reject empty / longer than 9 / any
-- letter / all-zero, LPAD to 9) -- guarded by
-- tests/test_cohort_queue_parity.py, the repo's copy-with-parity-test
-- convention (the serve_queries normalize_sql drift of 2026-07-31 is why we
-- never re-implement key normalization freehand). The raw side gets the SAME
-- expression so leading-zero drift on either side cannot fake a miss.
raw_eins AS (

    SELECT DISTINCT
        CASE WHEN LENGTH(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', ''))) = 0 OR LENGTH(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', ''))) > 9 OR NOT REGEXP_LIKE(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', '')), '^[0-9]+$') OR LPAD(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', '')), 9, '0') = REPEAT('0', 9) OR (LENGTH(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', ''))) >= 4 AND UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', '')) = REPEAT(LEFT(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', '')), 1), LENGTH(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', ''))))) OR LPAD(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', '')), 9, '0') = REPEAT(LEFT(LPAD(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', '')), 9, '0'), 1), 9) OR UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', '')) IN ('123456789', '987654321', '1234567890', '0987654321', '12345678', '87654321', '123456', '654321') OR LPAD(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', '')), 9, '0') IN ('123456789', '987654321', '1234567890', '0987654321', '12345678', '87654321', '123456', '654321') THEN NULL ELSE LPAD(UPPER(REGEXP_REPLACE(TO_VARCHAR(ein), '[^0-9A-Za-z]', '')), 9, '0') END
                                                              AS ein_norm
    FROM {{ source('ripple_raw', 'FED_OSHA_ITA_300A_SUMMARY_2024') }}

),

members_checked AS (

    SELECT
        m.*,
        CASE WHEN LENGTH(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', ''))) = 0 OR LENGTH(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', ''))) > 9 OR NOT REGEXP_LIKE(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', '')), '^[0-9]+$') OR LPAD(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', '')), 9, '0') = REPEAT('0', 9) OR (LENGTH(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', ''))) >= 4 AND UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', '')) = REPEAT(LEFT(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', '')), 1), LENGTH(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', ''))))) OR LPAD(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', '')), 9, '0') = REPEAT(LEFT(LPAD(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', '')), 9, '0'), 1), 9) OR UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', '')) IN ('123456789', '987654321', '1234567890', '0987654321', '12345678', '87654321', '123456', '654321') OR LPAD(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', '')), 9, '0') IN ('123456789', '987654321', '1234567890', '0987654321', '12345678', '87654321', '123456', '654321') THEN NULL ELSE LPAD(UPPER(REGEXP_REPLACE(TO_VARCHAR(m.ein_raw), '[^0-9A-Za-z]', '')), 9, '0') END
                                                              AS ein_norm
    FROM members m

),

-- One boolean per member: does its normalized EIN still exist in raw 300A?
members_final AS (

    SELECT
        mc.*,
        (mc.ein_norm IS NOT NULL AND re.ein_norm IS NOT NULL) AS ein_rejoins
    FROM members_checked mc
    LEFT JOIN raw_eins re ON re.ein_norm = mc.ein_norm

),

rolled AS (

    SELECT
        naics || '|' || size_band                             AS cohort_id,
        naics,
        MAX(industry)                                         AS industry,
        size_band,
        MAX(cohort_n)                                         AS cohort_n,
        MAX(cohort_pooled_dart)                               AS cohort_pooled_dart,
        COUNT(*)                                              AS n_outliers,
        SUM(IFF(implausible_rate, 1, 0))                      AS n_implausible,
        SUM(COALESCE(deaths, 0))                              AS n_deaths_total,
        MAX(fold_vs_pooled)                                   AS worst_fold,
        MAX(IFF(implausible_rate, NULL, fold_vs_pooled))      AS worst_fold_plausible,
        MEDIAN(fold_vs_pooled)                                AS median_fold,
        SUM(COALESCE(dart_cases, 0))                          AS total_dart_cases,
        SUM(COALESCE(hours, 0))                               AS total_hours,
        ARRAY_SLICE(
            ARRAY_AGG(DISTINCT state) WITHIN GROUP (ORDER BY state),
            0, 5)                                             AS states,
        SUM(IFF(NOT ein_rejoins, 1, 0))                       AS n_rejoin_failures,
        SUM(IFF(review_state = 'needs_work', 1, 0))           AS n_needs_work,
        MIN(first_seen)                                       AS first_seen,
        MAX(last_seen)                                        AS last_seen,
        MAX(as_of_date)                                       AS lead_as_of_date
    FROM members_final
    GROUP BY naics, size_band

),

-- Top receipts per cohort: the 5 worst PLAUSIBLE members by fold. Implausible
-- rows (DART > 50) are excluded here -- an entry error must not front the
-- pattern -- but they stay counted in n_implausible and reviewable per lead.
receipt_rows AS (

    SELECT
        naics || '|' || size_band                             AS cohort_id,
        lead_id, title, city, state, employees, dart_cases, dart_rate,
        fold_vs_pooled, deaths
    FROM members_checked
    WHERE NOT implausible_rate
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY naics, size_band ORDER BY fold_vs_pooled DESC, lead_id) <= 5

),

receipts AS (

    SELECT
        cohort_id,
        ARRAY_AGG(
            OBJECT_CONSTRUCT(
                'lead_id',    lead_id,
                'title',      title,
                'city',       city,
                'state',      state,
                'employees',  employees,
                'dart_cases', dart_cases,
                'dart_rate',  dart_rate,
                'fold',       fold_vs_pooled,
                'deaths',     deaths
            )
        ) WITHIN GROUP (ORDER BY fold_vs_pooled DESC)         AS receipts_sample
    FROM receipt_rows
    GROUP BY cohort_id

),

assembled AS (

    SELECT
        r.*,
        rc.receipts_sample,

        -- Fixed headline template (ASCII punctuation only).
        COALESCE(TRIM(TO_CHAR(r.n_outliers, '999,990')), '[count unavailable]')
        || ' of '
        || COALESCE(TRIM(TO_CHAR(r.cohort_n, '999,990')), '[count unavailable]')
        || ' establishments in NAICS-'
        || COALESCE(r.naics, '[code unavailable]')
        || COALESCE(' (' || r.industry || ')', '')
        || ', '
        || COALESCE(r.size_band, '[size unavailable]')
        || '-employee band, report DART injury rates at least 2x the cohort pooled rate of '
        || COALESCE(TRIM(TO_CHAR(r.cohort_pooled_dart, '990.00')), '[rate unavailable]')
        || ' - worst plausible case '
        || COALESCE(TRIM(TO_CHAR(r.worst_fold_plausible, '990.0')), '[fold unavailable]')
        || 'x.'                                               AS headline,

        -- The caveat travels with the cohort, like lead_queue's per-lead ones.
        'All inputs are self-reported by employers on OSHA Form 300A (2024 filing year): '
        || 'DART cases, hours worked, and employee counts are unaudited. '
        || 'Cohort membership (NAICS x size band) is also self-reported. '
        || 'A cohort verdict covers only member leads with no individual decision; '
        || 'individual lead decisions always win.'
        || IFF(r.n_implausible > 0,
               ' ' || TRIM(TO_CHAR(r.n_implausible, '999,990'))
               || ' member establishment(s) report a DART rate above 50, which is '
               || 'physically implausible and almost certainly a filing error; those '
               || 'rows are excluded from the receipts sample and from the worst-case '
               || 'figure, but remain individually reviewable.',
               '')
        || IFF(r.n_rejoin_failures > 0,
               ' ' || TRIM(TO_CHAR(r.n_rejoin_failures, '999,990'))
               || ' member lead key(s) no longer rejoin the raw 300A table on EIN '
               || '(normalization drift, see audit F6) - establishment identity for '
               || 'those rests on the frozen evidence.',
               '')                                            AS caveat,

        -- ------- priority: deterministic formula, weights DRAFT v1 -------
        -- (Checkpoint-1 approval pending, documented in _review__models.yml.)
        -- severity: log-scaled worst plausible fold, saturating at 64x
        -- breadth:  log-scaled outlier count, saturating at 100
        -- fatality: flat bump when any member reported a death
        -- density:  share of the cohort flagged, capped at 25%
        ROUND(
            LEAST(LN(1 + COALESCE(r.worst_fold_plausible, 0)) / LN(65), 1.0) * 3.0
            + LEAST(LN(1 + r.n_outliers) / LN(101), 1.0) * 1.5
            + IFF(r.n_deaths_total > 0, 1.0, 0.0)
            + LEAST(r.n_outliers / NULLIF(r.cohort_n, 0), 0.25) * 2.0
        , 3)                                                  AS priority_score

    FROM rolled r
    LEFT JOIN receipts rc ON rc.cohort_id = r.cohort_id

)

SELECT
    cohort_id,
    ROW_NUMBER() OVER (ORDER BY priority_score DESC, cohort_id)
                                                              AS priority_rank,
    priority_score,
    headline,
    naics,
    industry,
    size_band,
    cohort_n,
    cohort_pooled_dart,
    n_outliers,
    n_implausible,
    n_deaths_total,
    worst_fold,
    worst_fold_plausible,
    median_fold,
    total_dart_cases,
    total_hours,
    states,
    n_rejoin_failures,
    n_needs_work,
    receipts_sample,
    caveat,
    first_seen,
    last_seen,
    lead_as_of_date
FROM assembled
