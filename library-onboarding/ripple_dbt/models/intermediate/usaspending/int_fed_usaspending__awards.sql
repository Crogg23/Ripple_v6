{{ config(materialized='view') }}

{#
    int_fed_usaspending__awards
    ---------------------------------------------------------------------------
    GRAIN FIX (discovery finding #10): the FED_USASPENDING_CONTRACTS landing
    table is one row per TRANSACTION (base award + every modification action),
    NOT one row per contract. CONTRACT_AWARD_UNIQUE_KEY repeats up to 174x and
    ~9.6% of rows are "excess" against distinct keys (6,325,622 rows ->
    5,719,566 distinct awards). A naive SUM of the cumulative *_to_date columns
    over those duplicate rows overcounts dollars ~90x. This model rolls the
    table up to AWARD grain (one row per CONTRACT_AWARD_UNIQUE_KEY).

    Dollar rules:
      * total_obligation = SUM of FEDERAL_ACTION_OBLIGATION ONLY. That is the
        INCREMENTAL per-transaction field, the only one that legitimately sums.
      * Negative obligations (267,515 rows) are REAL de-obligations and are
        kept -- total_obligation is a NET figure (findings #5/#18/#51).
      * current_total_value_of_award / total_dollars_obligated are CUMULATIVE
        snapshots -- carried via MAX (the award-level value), NEVER summed.

    Entity-resolution caveat (finding #5): recipient_parent_uei is itself
    fragmented (Lockheed Martin spans 26 distinct parent UEIs), so it is NOT a
    clean single rollup key. Any downstream rank/aggregation by parent UEI is a
    FLOOR, not a ceiling -- real concentration is higher than measured.
#}

with source as (

    select * from {{ source('ripple_raw', 'FED_USASPENDING_CONTRACTS') }}

),

transactions as (

    select
        -- award grain key (validated: 0 null/blank keys in landing)
        nullif(trim(CONTRACT_AWARD_UNIQUE_KEY), '')          as contract_award_unique_key,
        nullif(trim(AWARD_ID_PIID), '')                      as award_id_piid,

        -- incremental dollars: the ONLY field that legitimately sums
        try_to_double(trim(FEDERAL_ACTION_OBLIGATION))       as federal_action_obligation,

        -- cumulative dollars: award-level snapshots, NEVER summed (carried via MAX)
        try_to_double(trim(CURRENT_TOTAL_VALUE_OF_AWARD))    as current_total_value_of_award,
        try_to_double(trim(TOTAL_DOLLARS_OBLIGATED))         as total_dollars_obligated,

        -- transaction timing (used for span; cast so bad input -> NULL not error)
        try_to_date(trim(ACTION_DATE))                       as action_date,
        try_to_date(trim(PERIOD_OF_PERFORMANCE_START_DATE))  as pop_start_date,
        try_to_date(trim(PERIOD_OF_PERFORMANCE_CURRENT_END_DATE)) as pop_current_end_date,

        -- recipient identifiers / dimensions
        nullif(trim(RECIPIENT_UEI), '')                      as recipient_uei,
        nullif(trim(RECIPIENT_DUNS), '')                     as recipient_duns,
        nullif(trim(CAGE_CODE), '')                          as cage_code,
        nullif(trim(RECIPIENT_NAME), '')                     as recipient_name,
        nullif(trim(RECIPIENT_PARENT_UEI), '')               as recipient_parent_uei,
        -- parent name normalized (upper + trim) per the build rule
        nullif(upper(trim(RECIPIENT_PARENT_NAME)), '')       as recipient_parent_name,

        -- recipient geography
        nullif(trim(RECIPIENT_CITY_NAME), '')                as recipient_city_name,
        nullif(trim(RECIPIENT_STATE_CODE), '')               as recipient_state_code,
        nullif(trim(RECIPIENT_ZIP_4_CODE), '')               as recipient_zip_4_code,
        nullif(trim(RECIPIENT_COUNTRY_NAME), '')             as recipient_country_name,

        -- place of performance
        nullif(trim(PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE), '') as pop_state_code,
        nullif(trim(PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME), '')  as pop_city_name,

        -- agency
        nullif(trim(AWARDING_AGENCY_NAME), '')               as awarding_agency_name,
        nullif(trim(AWARDING_SUB_AGENCY_NAME), '')           as awarding_sub_agency_name,
        nullif(trim(FUNDING_AGENCY_NAME), '')                as funding_agency_name,

        -- classification
        nullif(trim(AWARD_TYPE), '')                         as award_type,
        nullif(trim(NAICS_CODE), '')                         as naics_code,
        nullif(trim(NAICS_DESCRIPTION), '')                  as naics_description,
        nullif(trim(PRODUCT_OR_SERVICE_CODE_DESCRIPTION), '') as product_or_service_description,

        -- ownership flag (validated enum: exactly 'f' / 't')
        nullif(trim(FOREIGN_OWNED), '')                      as foreign_owned,

        nullif(trim(USASPENDING_PERMALINK), '')              as usaspending_permalink,

        -- pipeline audit columns (_INGESTED_AT lands as a microsecond epoch NUMBER)
        to_timestamp_ntz(_INGESTED_AT, 6)                    as _ingested_at,
        nullif(trim(try_cast(_SOURCE_RUN_ID as text)), '')   as _source_run_id

    from source
    -- guard the rollup key: never aggregate rows we cannot attribute to an award
    where nullif(trim(CONTRACT_AWARD_UNIQUE_KEY), '') is not null

),

awards as (

    select
        contract_award_unique_key,

        -- ===== dollars =====
        -- the ONLY legitimate sum: incremental per-transaction obligation.
        -- NET of de-obligations (negatives kept on purpose).
        sum(federal_action_obligation)                       as total_obligation,
        -- cumulative award snapshots -- MAX, never summed
        max(current_total_value_of_award)                    as current_total_value_of_award,
        max(total_dollars_obligated)                         as total_dollars_obligated,

        -- ===== transaction provenance =====
        count(*)                                             as transaction_count,
        min(action_date)                                     as first_action_date,
        max(action_date)                                     as last_action_date,
        min(pop_start_date)                                  as pop_start_date,
        max(pop_current_end_date)                            as pop_current_end_date,

        -- ===== dimensions (constant per award; MAX is a safe collapse) =====
        max(award_id_piid)                                   as award_id_piid,

        max(recipient_uei)                                   as recipient_uei,
        max(recipient_duns)                                  as recipient_duns,
        max(cage_code)                                       as cage_code,
        max(recipient_name)                                  as recipient_name,
        -- NOTE: recipient_parent_uei is fragmented (Lockheed = 26 parent UEIs);
        -- NOT a clean rollup key -- downstream parent rankings are a floor.
        max(recipient_parent_uei)                            as recipient_parent_uei,
        max(recipient_parent_name)                           as recipient_parent_name,

        max(recipient_city_name)                             as recipient_city_name,
        max(recipient_state_code)                            as recipient_state_code,
        max(recipient_zip_4_code)                            as recipient_zip_4_code,
        max(recipient_country_name)                          as recipient_country_name,

        max(pop_state_code)                                  as pop_state_code,
        max(pop_city_name)                                   as pop_city_name,

        max(awarding_agency_name)                            as awarding_agency_name,
        max(awarding_sub_agency_name)                        as awarding_sub_agency_name,
        max(funding_agency_name)                             as funding_agency_name,

        max(award_type)                                      as award_type,
        max(naics_code)                                      as naics_code,
        max(naics_description)                               as naics_description,
        max(product_or_service_description)                  as product_or_service_description,

        max(foreign_owned)                                   as foreign_owned,
        max(usaspending_permalink)                           as usaspending_permalink,

        -- audit: latest ingest wins
        max(_ingested_at)                                    as _ingested_at,
        max(_source_run_id)                                  as _source_run_id

    from transactions
    group by contract_award_unique_key

)

select * from awards
