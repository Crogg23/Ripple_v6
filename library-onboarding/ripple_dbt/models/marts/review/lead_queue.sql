{{ config(materialized='table', copy_grants=true, schema='REVIEW') }}

-- ============================================================================
-- LEAD_QUEUE â€” the Reading Room triage mart
-- ============================================================================
-- GRAIN:    one row per reviewable lead (REVIEW_STATE pending or needs_work)
-- KEY:      lead_id (from LIBRARY_META."CONNECT".V_LEADS_PUBLISHED â€” the safe
--           view; this model NEVER reads raw LEADS, same rule the viz guard
--           enforces)
-- HEADLINE: every analyst-facing string is a fixed SQL template â€” nothing
--           model-generated anywhere in this model, build time or read time.
--           Templates are DRAFT v1 pending Chris's Checkpoint-1 edit.
-- RECEIPT:  confidence_tier + receipt_verdict port scripts/lead_receipt.py's
--           3-source corroboration and timeline logic to SQL. That script is
--           the spec; tests/test_lead_queue_receipt_parity.py proves parity.
-- CAVEATS:  the caveat column carries the known per-detector data traps
--           (POLICY rows trap_ais_snapshot / trap_usaspending_grain, the
--           dropped facility-affiliation table, the 1,000-row SAM sample).
--           They ship WITH the lead so the analyst never reads a number the
--           warehouse can't back.
-- NULLs:    'text' || NULL is NULL in Snowflake â€” every substituted field is
--           COALESCE-wrapped. Guard tests forbid 'NULL'/'None'/'||' in
--           headlines.
-- ============================================================================

WITH leads AS (

    SELECT
        lead_id,
        rule_name,
        left_key_type,
        left_key_value,
        title,
        score,
        evidence,
        evidence_count,
        first_seen,
        last_seen,
        compiled_sql,
        sql_sha256,
        as_of_date,
        review_state
    FROM {{ source('library_meta_connect', 'V_LEADS_PUBLISHED') }}
    WHERE review_state IN ('pending', 'needs_work')

),

-- ---------------------------------------------------------------------------
-- Key prune lists: every source aggregate below filters to flagged keys FIRST
-- so we never GROUP BY a 40M-row table for the sake of ~1k leads.
-- ---------------------------------------------------------------------------
npi_keys AS (
    SELECT DISTINCT left_key_value AS npi FROM leads WHERE left_key_type = 'NPI'
),
uei_keys AS (
    SELECT DISTINCT left_key_value AS uei FROM leads WHERE left_key_type = 'UEI'
),
imo_keys AS (
    SELECT DISTINCT left_key_value AS imo FROM leads WHERE left_key_type = 'IMO'
),
ein_keys AS (
    SELECT DISTINCT left_key_value AS ein FROM leads WHERE left_key_type = 'EIN'
),

-- SEC financial-statement filers (sec_filer_in_irs_bmf, dormant today â€”
-- 0 active leads â€” but the enrichment is wired so the day it wakes its
-- headlines carry real names, not '[name unavailable]').
sec AS (
    SELECT
        ein,
        MAX(name)                                            AS name,
        MAX(cik)                                             AS cik
    FROM {{ source('ripple_raw', 'FED_SEC_EDGAR_FINANCIALS') }}
    WHERE ein IN (SELECT ein FROM ein_keys)
    GROUP BY 1
),

-- ---------------------------------------------------------------------------
-- [2] OIG-LEIE â€” the ban. Two grains:
--   leie_pair  mirrors lead_receipt.py's CTE exactly (npi, lname, fname) â€”
--              feeds the banned_but_paid receipt join (op ON npi AND lname).
--   leie_npi   one deterministic row per NPI (latest exclusion first) â€” feeds
--              the display fields for the other NPI detectors.
-- Date parsing is explicit YYYYMMDD (POLICY trap_leie_npi_and_dates: TRY_CAST
-- collapses LEIE dates to 1970).
-- ---------------------------------------------------------------------------
leie_pair AS (
    SELECT
        REGEXP_REPLACE(npi, '[^0-9]', '')                    AS npi,
        UPPER(TRIM(lastname))                                AS lname,
        UPPER(TRIM(firstname))                               AS fname,
        MAX(excltype)                                        AS excltype,
        MIN(excldate)                                        AS excldate_raw,
        TRY_TO_DATE(MIN(excldate), 'YYYYMMDD')               AS excl_date,
        MAX(city)                                            AS city,
        MAX(state)                                           AS state,
        MAX(specialty)                                       AS specialty
    FROM {{ source('ripple_raw', 'FED_HHS_OIG_LEIE') }}
    WHERE LENGTH(REGEXP_REPLACE(npi, '[^0-9]', '')) = 10
      AND REGEXP_REPLACE(npi, '[^0-9]', '') <> '0000000000'
      AND REGEXP_REPLACE(npi, '[^0-9]', '') IN (SELECT npi FROM npi_keys)
    GROUP BY 1, 2, 3
),
leie_npi AS (
    SELECT *
    FROM leie_pair
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY npi
        ORDER BY excl_date DESC NULLS LAST, lname, fname
    ) = 1
),

-- ---------------------------------------------------------------------------
-- [1] NPPES â€” the registry (the third source). Single-underscore column name
-- is the LIVE schema after the 2026-07-12 re-land (commit 124f350);
-- lead_receipt.py still holds the old double-underscore name â€” the Python
-- LOGIC is the spec, this column name is the fix.
-- ---------------------------------------------------------------------------
nppes AS (
    SELECT
        npi,
        UPPER(TRIM(provider_last_name_legal_name))           AS lname,
        UPPER(TRIM(provider_first_name))                     AS fname,
        UPPER(TRIM(provider_credential_text))                AS cred,
        entity_type_code                                     AS etype
    FROM {{ source('ripple_raw', 'FED_CMS_NPPES') }}
    WHERE npi IN (SELECT npi FROM npi_keys)
    QUALIFY ROW_NUMBER() OVER (PARTITION BY npi ORDER BY lname, fname) = 1
),

-- ---------------------------------------------------------------------------
-- [3] Open Payments â€” the money. Same grain and normalization as
-- lead_receipt.py's op CTE (npi, lname), against the SAME all-years union the
-- banned_but_paid detector reads. Payment dates parse 'MM/DD/YYYY' explicitly.
-- ---------------------------------------------------------------------------
op_pair AS (
    SELECT
        REGEXP_REPLACE(npi, '[^0-9]', '')                    AS npi,
        UPPER(TRIM(covered_recipient_last_name))             AS lname,
        COUNT(*)                                             AS recs,
        ROUND(SUM(TRY_TO_DECIMAL(total_amount_of_payment_usdollars, 18, 2)), 2)
                                                             AS total_usd,
        MIN(TRY_TO_DATE(date_of_payment, 'MM/DD/YYYY'))      AS min_pay,
        MAX(TRY_TO_DATE(date_of_payment, 'MM/DD/YYYY'))      AS max_pay,
        ARRAY_SLICE(
            ARRAY_AGG(DISTINCT applicable_manufacturer_or_applicable_gpo_making_payment_name)
                WITHIN GROUP (ORDER BY applicable_manufacturer_or_applicable_gpo_making_payment_name),
            0, 3)                                            AS payers
    FROM {{ ref('int_open_payments_all_years') }}
    WHERE LENGTH(REGEXP_REPLACE(npi, '[^0-9]', '')) = 10
      AND REGEXP_REPLACE(npi, '[^0-9]', '') IN (SELECT npi FROM npi_keys)
    GROUP BY 1, 2
),

-- The receipt join, exactly as lead_receipt.py: LEIE â‹ˆ OP on npi AND surname,
-- NPPES LEFT-joined as the corroborating third source. Where one NPI carries
-- several LEIE name variants, keep the row the receipt script prints FIRST
-- (most payments, then most dollars) â€” deterministic tiebreak on lname.
receipt_bbp AS (
    SELECT
        l.npi,
        l.lname                                              AS leie_lname,
        l.fname                                              AS leie_fname,
        l.excltype,
        l.excl_date,
        l.city,
        l.state,
        o.recs,
        o.total_usd,
        o.min_pay,
        o.max_pay,
        o.payers,
        n.lname                                              AS nppes_lname,
        n.fname                                              AS nppes_fname,
        n.cred                                               AS nppes_cred
    FROM leie_pair l
    JOIN op_pair o
      ON o.npi = l.npi AND o.lname = l.lname
    LEFT JOIN nppes n
      ON n.npi = l.npi
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY l.npi
        ORDER BY o.recs DESC, o.total_usd DESC, l.lname, l.fname
    ) = 1
),

-- ---------------------------------------------------------------------------
-- Medicare Part D aggregate (excluded_but_billing). No program-year column in
-- this landing table â†’ no timeline verdict possible; costs recomputed from
-- source rather than trusted from the capped EVIDENCE array.
-- ---------------------------------------------------------------------------
partd_agg AS (
    SELECT
        REGEXP_REPLACE(npi, '[^0-9]', '')                    AS npi,
        COUNT(*)                                             AS recs,
        ROUND(SUM(TRY_TO_DECIMAL(tot_drug_cst, 18, 2)), 2)   AS drug_cost_usd,
        ROUND(SUM(TRY_TO_DECIMAL(opioid_tot_drug_cst, 18, 2)), 2)
                                                             AS opioid_cost_usd
    FROM {{ source('ripple_raw', 'FED_CMS_PART_D_PRESCRIBERS') }}
    WHERE REGEXP_REPLACE(npi, '[^0-9]', '') IN (SELECT npi FROM npi_keys)
    GROUP BY 1
),

-- ---------------------------------------------------------------------------
-- SAM debarments + USASpending awards (debarred_but_funded). Award dollars =
-- SUM(FEDERAL_ACTION_OBLIGATION): transaction-grain increments sum correctly;
-- TOTAL_DOLLARS_OBLIGATED is cumulative and would double-count (POLICY
-- trap_usaspending_grain).
-- ---------------------------------------------------------------------------
sam AS (
    SELECT
        uei,
        MAX(entity_name)                                     AS entity_name,
        MAX(classification)                                  AS classification,
        MAX(exclusion_type)                                  AS exclusion_type,
        MAX(excluding_agency)                                AS excluding_agency
    FROM {{ source('ripple_raw', 'FED_SAM_EXCLUSIONS') }}
    WHERE uei IN (SELECT uei FROM uei_keys)
    GROUP BY 1
),
usasp_agg AS (
    SELECT
        recipient_uei                                        AS uei,
        COUNT(*)                                             AS recs,
        ROUND(SUM(TRY_TO_DECIMAL(federal_action_obligation, 18, 2)), 2)
                                                             AS total_usd,
        MIN(TRY_TO_DATE(action_date, 'YYYY-MM-DD'))          AS min_action,
        MAX(TRY_TO_DATE(action_date, 'YYYY-MM-DD'))          AS max_action,
        MAX(recipient_name)                                  AS recipient_name,
        ARRAY_SLICE(
            ARRAY_AGG(DISTINCT awarding_agency_name)
                WITHIN GROUP (ORDER BY awarding_agency_name),
            0, 3)                                            AS awarding_agencies
    FROM {{ source('ripple_raw', 'FED_USASPENDING_CONTRACTS') }}
    WHERE recipient_uei IN (SELECT uei FROM uei_keys)
    GROUP BY 1
),

-- ---------------------------------------------------------------------------
-- Sanctions lists + the AIS archive (both vessel detectors). The AIS table is
-- a FIXED Jan 1â€“8 2024 US-coastal snapshot (POLICY trap_ais_snapshot) â€” the
-- caveat travels on every vessel row.
-- ---------------------------------------------------------------------------
-- IMO normalization mirrors connect/keys.py: digits only (AIS broadcasts
-- 'IMO9389095', OFAC stores bare '9389095' â€” same hull), exactly 7 digits,
-- never the all-zero placeholder. OFAC's literal null token '-0- ' (POLICY
-- trap_ofac_sdn_type) is scrubbed so 'flag: -0-' can never reach an analyst.
sdn AS (
    SELECT
        REGEXP_REPLACE(UPPER(imo), '[^0-9]', '')             AS imo,
        MAX(NULLIF(NULLIF(TRIM(sdn_name), ''), '-0-'))       AS sdn_name,
        MAX(NULLIF(NULLIF(TRIM(program), ''), '-0-'))        AS program,
        MAX(NULLIF(NULLIF(TRIM(vess_flag), ''), '-0-'))      AS flag
    FROM {{ source('ripple_raw', 'FED_OFAC_SDN') }}
    WHERE LENGTH(REGEXP_REPLACE(UPPER(imo), '[^0-9]', '')) = 7
      AND REGEXP_REPLACE(UPPER(imo), '[^0-9]', '') <> '0000000'
      AND REGEXP_REPLACE(UPPER(imo), '[^0-9]', '') IN (SELECT imo FROM imo_keys)
    GROUP BY 1
),
sanc_vessels AS (
    SELECT
        imo,
        MAX(vessel_name)                                     AS vessel_name,
        MAX(sanction_source)                                 AS sanction_source,
        MAX(program)                                         AS program,
        MAX(flag)                                            AS flag
    FROM {{ ref('int_sanctioned_vessels') }}
    WHERE imo IN (SELECT imo FROM imo_keys)
    GROUP BY 1
),
ais_agg AS (
    SELECT
        REGEXP_REPLACE(UPPER(imo), '[^0-9]', '')             AS imo,
        COUNT(*)                                             AS recs,
        MIN(TRY_TO_TIMESTAMP_NTZ(basedatetime))              AS min_seen,
        MAX(TRY_TO_TIMESTAMP_NTZ(basedatetime))              AS max_seen,
        ARRAY_SLICE(
            ARRAY_AGG(DISTINCT vesselname)
                WITHIN GROUP (ORDER BY vesselname),
            0, 3)                                            AS ais_names
    FROM {{ source('ripple_raw', 'FED_NOAA_AIS') }}
    WHERE LENGTH(REGEXP_REPLACE(UPPER(imo), '[^0-9]', '')) = 7
      AND REGEXP_REPLACE(UPPER(imo), '[^0-9]', '') <> '0000000'
      AND REGEXP_REPLACE(UPPER(imo), '[^0-9]', '') IN (SELECT imo FROM imo_keys)
    GROUP BY 1
),

-- ---------------------------------------------------------------------------
-- Assemble: one enriched row per lead. Every analyst-facing string is
-- COALESCE-guarded; every join above is pre-aggregated to its key, so this
-- stays exactly 1:1 with leads (proven by the unique lead_id test).
-- ---------------------------------------------------------------------------
enriched AS (

    SELECT
        ld.lead_id,
        ld.rule_name                                         AS detector,
        ld.left_key_type                                     AS entity_a_key_type,
        ld.left_key_value                                    AS entity_a_key_value,
        ld.title                                             AS detector_title,
        ld.score                                             AS detector_score,
        ld.evidence,
        ld.evidence_count,
        ld.first_seen,
        ld.last_seen,
        ld.compiled_sql                                      AS evidence_sql,
        ld.sql_sha256,
        ld.as_of_date                                        AS lead_as_of_date,
        ld.review_state,

        -- ------- flagged-entity display fields (per detector family) -------
        CASE ld.rule_name
            WHEN 'banned_but_paid' THEN
                NULLIF(INITCAP(TRIM(COALESCE(r.leie_fname, ln.fname, '') || ' ' || COALESCE(r.leie_lname, ln.lname, ''))), '')
            WHEN 'excluded_but_billing' THEN
                NULLIF(INITCAP(TRIM(COALESCE(ln.fname, '') || ' ' || COALESCE(ln.lname, ''))), '')
            WHEN 'banned_but_operating' THEN
                NULLIF(INITCAP(TRIM(COALESCE(ln.fname, '') || ' ' || COALESCE(ln.lname, ''))), '')
            WHEN 'debarred_but_funded' THEN s.entity_name
            WHEN 'sanctioned_vessel_broadcasting' THEN v1.sdn_name
            WHEN 'sanctioned_vessel_broadcasting_v2' THEN v2.vessel_name
            WHEN 'sec_filer_in_irs_bmf' THEN sec.name
        END                                                  AS entity_a_name,

        CASE ld.rule_name
            WHEN 'banned_but_paid'                  THEN 'LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE'
            WHEN 'excluded_but_billing'             THEN 'LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE'
            WHEN 'banned_but_operating'             THEN 'LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE'
            WHEN 'debarred_but_funded'              THEN 'LIBRARY_RAW.LANDING.FED_SAM_EXCLUSIONS'
            WHEN 'sanctioned_vessel_broadcasting'   THEN 'LIBRARY_RAW.LANDING.FED_OFAC_SDN'
            WHEN 'sanctioned_vessel_broadcasting_v2' THEN 'LIBRARY_STAGING.DBT_CROGERS.INT_SANCTIONED_VESSELS'
            WHEN 'sec_filer_in_irs_bmf'             THEN 'LIBRARY_RAW.LANDING.FED_SEC_EDGAR_FINANCIALS'
        END                                                  AS entity_a_source,

        CASE ld.rule_name
            WHEN 'banned_but_paid' THEN
                NULLIF(TRIM(COALESCE(r.city, ln.city, '') || ' ' || COALESCE(r.state, ln.state, '')), '')
            WHEN 'excluded_but_billing' THEN ln.state
            WHEN 'banned_but_operating' THEN
                NULLIF(TRIM(COALESCE(ln.city, '') || ' ' || COALESCE(ln.state, '')), '')
            WHEN 'debarred_but_funded' THEN NULL
            WHEN 'sanctioned_vessel_broadcasting' THEN 'flag: ' || COALESCE(v1.flag, '[unknown]')
            WHEN 'sanctioned_vessel_broadcasting_v2' THEN 'flag: ' || COALESCE(v2.flag, '[unknown]')
        END                                                  AS entity_a_location,

        -- ------- activity-side (entity B) display fields -------
        CASE ld.rule_name
            WHEN 'banned_but_paid' THEN
                NULLIF(ARRAY_TO_STRING(r.payers, ', '), '')
            WHEN 'excluded_but_billing' THEN 'Medicare Part D prescriber file'
            WHEN 'banned_but_operating' THEN
                COALESCE(ld.evidence[0]:facility::STRING, '[facility name unavailable]')
                || COALESCE(' (' || ld.evidence[0]:facility_type::STRING || ')', '')
            WHEN 'debarred_but_funded' THEN
                NULLIF(ARRAY_TO_STRING(u.awarding_agencies, ', '), '')
            WHEN 'sanctioned_vessel_broadcasting' THEN
                NULLIF(ARRAY_TO_STRING(a.ais_names, ', '), '')
            WHEN 'sanctioned_vessel_broadcasting_v2' THEN
                NULLIF(ARRAY_TO_STRING(a.ais_names, ', '), '')
            WHEN 'sec_filer_in_irs_bmf' THEN ld.evidence[0]:irs_name::STRING
        END                                                  AS entity_b_name,

        CASE ld.rule_name
            WHEN 'banned_but_paid'                  THEN 'LIBRARY_STAGING.DBT_CROGERS.INT_OPEN_PAYMENTS_ALL_YEARS'
            WHEN 'excluded_but_billing'             THEN 'LIBRARY_RAW.LANDING.FED_CMS_PART_D_PRESCRIBERS'
            WHEN 'banned_but_operating'             THEN 'FED_CMS_FACILITY_AFFILIATION (DROPPED â€” evidence frozen)'
            WHEN 'debarred_but_funded'              THEN 'LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS'
            WHEN 'sanctioned_vessel_broadcasting'   THEN 'LIBRARY_RAW.LANDING.FED_NOAA_AIS'
            WHEN 'sanctioned_vessel_broadcasting_v2' THEN 'LIBRARY_RAW.LANDING.FED_NOAA_AIS'
            WHEN 'sec_filer_in_irs_bmf'             THEN 'LIBRARY_RAW.LANDING.FED_IRS_BMF'
        END                                                  AS entity_b_source,

        -- ------- corroborating registry (NPPES, the third source) -------
        CASE
            WHEN ld.left_key_type = 'NPI' THEN
                NULLIF(INITCAP(TRIM(COALESCE(np.fname, '') || ' ' || COALESCE(np.lname, ''))), '')
        END                                                  AS nppes_legal_name,

        -- ------- recomputed activity numbers (never the capped EVIDENCE) ---
        CASE ld.rule_name
            WHEN 'banned_but_paid'                  THEN r.recs
            WHEN 'excluded_but_billing'             THEN p.recs
            WHEN 'banned_but_operating'             THEN ld.evidence_count  -- one item per facility; source dropped
            WHEN 'debarred_but_funded'              THEN u.recs
            WHEN 'sanctioned_vessel_broadcasting'   THEN a.recs
            WHEN 'sanctioned_vessel_broadcasting_v2' THEN a.recs
        END                                                  AS n_activity_records,

        CASE ld.rule_name
            WHEN 'banned_but_paid'      THEN r.total_usd
            WHEN 'excluded_but_billing' THEN p.drug_cost_usd
            WHEN 'debarred_but_funded'  THEN u.total_usd
        END                                                  AS activity_total_usd,

        p.opioid_cost_usd                                    AS opioid_cost_usd,

        CASE ld.rule_name
            WHEN 'banned_but_paid'                  THEN r.min_pay
            WHEN 'debarred_but_funded'              THEN u.min_action
            WHEN 'sanctioned_vessel_broadcasting'   THEN a.min_seen::DATE
            WHEN 'sanctioned_vessel_broadcasting_v2' THEN a.min_seen::DATE
        END                                                  AS activity_min_date,

        CASE ld.rule_name
            WHEN 'banned_but_paid'                  THEN r.max_pay
            WHEN 'debarred_but_funded'              THEN u.max_action
            WHEN 'sanctioned_vessel_broadcasting'   THEN a.max_seen::DATE
            WHEN 'sanctioned_vessel_broadcasting_v2' THEN a.max_seen::DATE
        END                                                  AS activity_max_date,

        -- ------- SAM debarment display fields -------
        s.excluding_agency                                   AS debar_agency,
        s.classification                                     AS debar_classification,

        -- ------- the exclusion (LEIE) fields -------
        COALESCE(r.excl_date, ln.excl_date)                  AS excl_date,
        COALESCE(r.excltype, ln.excltype)                    AS excl_reason_code,

        -- lead_receipt.py's EXCL dict, ported verbatim
        CASE LOWER(COALESCE(r.excltype, ln.excltype, ''))
            WHEN '1128a1' THEN 'Conviction of a Medicare/Medicaid program-related crime'
            WHEN '1128a2' THEN 'Conviction relating to patient abuse or neglect'
            WHEN '1128a3' THEN 'Felony conviction relating to health-care fraud'
            WHEN '1128a4' THEN 'Felony conviction relating to controlled substances'
            WHEN '1128b1' THEN 'Misdemeanor conviction relating to health-care fraud'
            WHEN '1128b4' THEN 'License revoked, suspended, or surrendered'
            WHEN '1128b5' THEN 'Exclusion/suspension under a federal/state health program'
            WHEN '1128b7' THEN 'Fraud, kickbacks, or other prohibited activities'
            WHEN '1128b8' THEN 'Entities controlled by a sanctioned individual'
            ELSE COALESCE(r.excltype, ln.excltype)
        END                                                  AS excl_reason_plain,

        -- ------- confidence tier: the 3-source corroboration verdict -------
        -- Port of lead_receipt.py receipt() lines 117-133. NPI detectors only;
        -- hard-ID-only detectors carry HARD_ID_ONLY (fact_vs_lead: the key IS
        -- the identity; there is no third registry to corroborate against).
        CASE
            WHEN ld.left_key_type <> 'NPI'                     THEN 'HARD_ID_ONLY'
            -- LEIE row vanished since detection (monthly OIG refresh removes
            -- reinstated providers) â€” no surname to compare; never mislabel
            -- this as a conflict.
            WHEN COALESCE(r.leie_lname, ln.lname) IS NULL      THEN 'LEIE_ROW_MISSING'
            WHEN np.npi IS NULL OR COALESCE(np.lname, '') = '' THEN 'TWO_SOURCE'
            WHEN np.lname = COALESCE(r.leie_lname, ln.lname)   THEN 'FACT_GRADE_3_SOURCE'
            ELSE 'NPPES_CONFLICT'
        END                                                  AS confidence_tier,

        -- ------- receipt verdict: the timeline -------
        -- Port of lead_receipt.py line 121. Evaluated only where the activity
        -- side carries real dates (banned_but_paid). TIMELINE_UNKNOWN is the
        -- honest extra state for a missing date (the receipt script lumps it
        -- into "predate"; the parity test maps both to the weaker verdict).
        CASE
            WHEN ld.rule_name <> 'banned_but_paid'             THEN 'NOT_EVALUATED'
            WHEN r.max_pay IS NULL OR r.excl_date IS NULL      THEN 'TIMELINE_UNKNOWN'
            WHEN r.max_pay >= r.excl_date                      THEN 'PAID_ON_OR_AFTER_EXCLUSION'
            ELSE 'PAYMENTS_PREDATE_EXCLUSION'
        END                                                  AS receipt_verdict,

        -- ------- the known data traps, travelling with the lead -------
        CASE ld.rule_name
            WHEN 'banned_but_operating' THEN
                'Source table FED_CMS_FACILITY_AFFILIATION was dropped from LANDING (verified 2026-07-12): the stored evidence_sql cannot be re-run; facility evidence is frozen in the lead''s EVIDENCE payload.'
            WHEN 'sanctioned_vessel_broadcasting' THEN
                'SUPERSEDED by sanctioned_vessel_broadcasting_v2. AIS activity is a Jan 1-8 2024 US-coastal archive snapshot that PRE-DATES most 2025-26 sanctions listings â€” never read as current behavior.'
            WHEN 'sanctioned_vessel_broadcasting_v2' THEN
                'AIS activity is a Jan 1-8 2024 US-coastal archive snapshot that PRE-DATES most 2025-26 sanctions listings â€” an appearance is historical presence, never current broadcasting.'
            WHEN 'debarred_but_funded' THEN
                'FED_SAM_EXCLUSIONS holds exactly 1,000 rows (suspected capped sample load) and ACTIVATION_DATE is blank â€” breadth is a floor and no debarment-date timeline is possible.'
            WHEN 'excluded_but_billing' THEN
                'Part D landing table carries no program-year column â€” no billing-date timeline is possible.'
        END                                                  AS caveat

    FROM leads ld
    LEFT JOIN receipt_bbp r  ON ld.left_key_type = 'NPI' AND r.npi  = ld.left_key_value
                             AND ld.rule_name = 'banned_but_paid'
    LEFT JOIN leie_npi   ln  ON ld.left_key_type = 'NPI' AND ln.npi = ld.left_key_value
    LEFT JOIN nppes      np  ON ld.left_key_type = 'NPI' AND np.npi = ld.left_key_value
    LEFT JOIN partd_agg  p   ON ld.left_key_type = 'NPI' AND p.npi  = ld.left_key_value
    LEFT JOIN sam        s   ON ld.left_key_type = 'UEI' AND s.uei  = ld.left_key_value
    LEFT JOIN usasp_agg  u   ON ld.left_key_type = 'UEI' AND u.uei  = ld.left_key_value
    LEFT JOIN sdn        v1  ON ld.left_key_type = 'IMO' AND v1.imo = ld.left_key_value
    LEFT JOIN sanc_vessels v2 ON ld.left_key_type = 'IMO' AND v2.imo = ld.left_key_value
    LEFT JOIN ais_agg    a   ON ld.left_key_type = 'IMO' AND a.imo  = ld.left_key_value
    LEFT JOIN sec            ON ld.left_key_type = 'EIN' AND sec.ein = ld.left_key_value

),

-- ---------------------------------------------------------------------------
-- Headlines â€” six fixed templates (DRAFT v1, Checkpoint-1 approval pending),
-- one per detector, plus the dormant sec_filer branch. Pure SQL string
-- concatenation; every field COALESCE-guarded so one missing value can never
-- NULL-poison the sentence. Dollar amounts are whole-dollar rounded (the
-- receipt script prints cents; the case-file view carries the exact figure).
-- ---------------------------------------------------------------------------
headlined AS (

    SELECT
        e.*,

        CASE e.detector

            WHEN 'banned_but_paid' THEN
                COALESCE(e.entity_a_name, '[name unavailable]')
                || ', excluded from federal health programs '
                || COALESCE(TO_CHAR(e.excl_date, 'YYYY-MM-DD'), '[date unavailable]')
                || ' (' || COALESCE(e.excl_reason_plain, '[reason unavailable]') || '), appears in '
                || COALESCE(TRIM(TO_CHAR(e.n_activity_records, '999,999,990')), '[count unavailable]')
                || ' drug/device industry payment records totaling $'
                || COALESCE(TRIM(TO_CHAR(e.activity_total_usd, '999,999,999,990')), '[amount unavailable]')
                || ' â€” latest payment '
                || COALESCE(TO_CHAR(e.activity_max_date, 'YYYY-MM-DD'), '[date unavailable]') || '.'

            WHEN 'excluded_but_billing' THEN
                COALESCE(e.entity_a_name, '[name unavailable]')
                || ', excluded from federal health programs '
                || COALESCE(TO_CHAR(e.excl_date, 'YYYY-MM-DD'), '[date unavailable]')
                || ' (' || COALESCE(e.excl_reason_plain, '[reason unavailable]')
                || '), appears in the Medicare Part D prescriber file with $'
                || COALESCE(TRIM(TO_CHAR(e.activity_total_usd, '999,999,999,990')), '[amount unavailable]')
                || ' in prescription drug costs.'

            WHEN 'banned_but_operating' THEN
                COALESCE(e.entity_a_name, '[name unavailable]')
                || ', excluded from federal health programs '
                || COALESCE(TO_CHAR(e.excl_date, 'YYYY-MM-DD'), '[date unavailable]')
                || ' (' || COALESCE(e.excl_reason_plain, '[reason unavailable]')
                || '), was listed as affiliated with '
                || COALESCE(TRIM(TO_CHAR(e.n_activity_records, '999,990')), '[count unavailable]')
                || ' CMS-registered facilities, e.g. '
                || COALESCE(e.entity_b_name, '[facility unavailable]') || '.'

            WHEN 'debarred_but_funded' THEN
                COALESCE(e.entity_a_name, '[name unavailable]')
                || ', federally debarred by '
                || COALESCE(NULLIF(TRIM(e.debar_agency), ''), '[agency unavailable]')
                || ', appears on '
                || COALESCE(TRIM(TO_CHAR(e.n_activity_records, '999,999,990')), '[count unavailable]')
                || ' federal contract transaction records ('
                -- net obligation can be NEGATIVE (de-obligated/terminated
                -- awards â€” exactly what happens to a debarred contractor)
                || COALESCE(
                       IFF(e.activity_total_usd < 0, '-$', '$')
                       || TRIM(TO_CHAR(ABS(e.activity_total_usd), '999,999,999,990')),
                       '[amount unavailable]')
                || ' net obligated), most recently '
                || COALESCE(TO_CHAR(e.activity_max_date, 'YYYY-MM-DD'), '[date unavailable]') || '.'

            WHEN 'sanctioned_vessel_broadcasting' THEN
                'Vessel '
                || COALESCE(e.entity_a_name, '[name unavailable]')
                || ' (IMO ' || COALESCE(e.entity_a_key_value, '[unavailable]')
                || '), OFAC-sanctioned, appeared in '
                || COALESCE(TRIM(TO_CHAR(e.n_activity_records, '999,999,990')), '[count unavailable]')
                || ' AIS position reports in the Jan 2024 US-coastal archive'
                || COALESCE(', broadcasting as ' || NULLIF(e.entity_b_name, ''), '')
                || ' â€” archive snapshot, not current activity.'

            WHEN 'sanctioned_vessel_broadcasting_v2' THEN
                'Vessel '
                || COALESCE(e.entity_a_name, '[name unavailable]')
                || ' (IMO ' || COALESCE(e.entity_a_key_value, '[unavailable]')
                || '), on OFAC/OpenSanctions sanction lists, appeared in '
                || COALESCE(TRIM(TO_CHAR(e.n_activity_records, '999,999,990')), '[count unavailable]')
                || ' AIS position reports in the Jan 2024 US-coastal archive'
                || COALESCE(', broadcasting as ' || NULLIF(e.entity_b_name, ''), '')
                || ' â€” archive snapshot, not current activity.'

            WHEN 'sec_filer_in_irs_bmf' THEN
                COALESCE(e.entity_a_name, '[name unavailable]')
                || ' files financials with the SEC and its EIN also appears on the IRS tax-exempt roster'
                || ' â€” co-occurrence to examine, not a violation claim.'

            ELSE
                COALESCE(e.detector_title, '[headline unavailable]')

        END                                                  AS headline

    FROM enriched e

),

-- ---------------------------------------------------------------------------
-- Priority â€” deterministic, no model anywhere. Formula (documented in the
-- model YAML, weights DRAFT v1 pending Checkpoint-1 approval):
--   tier weight + receipt weight + detector weight + detector-score tiebreak
-- ---------------------------------------------------------------------------
scored AS (

    SELECT
        h.*,

        ROUND(
            CASE h.confidence_tier
                WHEN 'FACT_GRADE_3_SOURCE' THEN 3.0
                WHEN 'TWO_SOURCE'          THEN 2.0
                WHEN 'HARD_ID_ONLY'        THEN 1.5
                WHEN 'NPPES_CONFLICT'      THEN 0.75
                WHEN 'LEIE_ROW_MISSING'    THEN 0.5
                ELSE 0.0
            END
            +
            CASE h.receipt_verdict
                WHEN 'PAID_ON_OR_AFTER_EXCLUSION' THEN 2.0
                WHEN 'NOT_EVALUATED'              THEN 0.75
                WHEN 'TIMELINE_UNKNOWN'           THEN 0.75
                WHEN 'PAYMENTS_PREDATE_EXCLUSION' THEN 0.5
                ELSE 0.0
            END
            +
            CASE h.detector
                WHEN 'banned_but_operating'             THEN 1.5
                WHEN 'excluded_but_billing'             THEN 1.25
                WHEN 'banned_but_paid'                  THEN 1.0
                WHEN 'debarred_but_funded'              THEN 1.0
                WHEN 'sanctioned_vessel_broadcasting_v2' THEN 0.75
                WHEN 'sec_filer_in_irs_bmf'             THEN 0.5
                WHEN 'sanctioned_vessel_broadcasting'   THEN 0.25
                ELSE 0.5
            END
            +
            LEAST(COALESCE(h.detector_score, 0), 1.0) * 0.5
        , 3)                                                 AS priority_score

    FROM headlined h

),

final AS (

    SELECT
        lead_id,
        detector,
        ROW_NUMBER() OVER (ORDER BY priority_score DESC, lead_id)
                                                             AS priority_rank,
        priority_score,
        headline,
        confidence_tier,
        receipt_verdict,
        entity_a_name,
        entity_a_key_type,
        entity_a_key_value,
        entity_a_source,
        entity_a_location,
        entity_b_name,
        entity_b_source,
        nppes_legal_name,
        n_activity_records,
        activity_total_usd,
        opioid_cost_usd,
        activity_min_date,
        activity_max_date,
        excl_date,
        excl_reason_code,
        excl_reason_plain,
        caveat,
        detector_title,
        detector_score,
        evidence_count,
        first_seen,
        last_seen,
        review_state,
        evidence_sql,
        sql_sha256,
        lead_as_of_date
    FROM scored

)

SELECT * FROM final
