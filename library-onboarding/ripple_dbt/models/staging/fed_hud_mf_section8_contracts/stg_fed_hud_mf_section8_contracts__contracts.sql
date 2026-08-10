{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_HUD_MF_SECTION8_CONTRACTS') }}

),

keyed as (

    -- CONTRACT_NUMBER is NEAR-unique (24,308 distinct of 24,309 rows). The
    -- single collision is a genuinely distinct record, so a row_number() over
    -- the full-row hash is appended as a deterministic tiebreaker to make
    -- contract_record_id fully unique.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['CONTRACT_NUMBER']) }}
            || '-'
            || row_number() over (
                   partition by CONTRACT_NUMBER
                   order by hash(*)
               ) as contract_record_id
    from source

),

renamed as (

    select

        -- identifiers
        contract_record_id,
        trim(CONTRACT_NUMBER)                            as contract_number,
        trim(PROPERTY_ID)                                as property_id,
        trim(PROPERTY_NAME_TEXT)                         as property_name,

        -- contract dates / status
        try_to_date(left(trim(TRACS_EFFECTIVE_DATE), 10), 'YYYY-MM-DD')          as tracs_effective_date,
        try_to_date(left(trim(TRACS_OVERALL_EXPIRATION_DATE), 10), 'YYYY-MM-DD') as tracs_overall_expiration_date,
        try_to_number(trim(TRACS_OVERALL_EXP_FISCAL_YEAR))                       as tracs_overall_exp_fiscal_year,
        trim(TRACS_OVERALL_EXPIRE_QUARTER)               as tracs_overall_expire_quarter,
        try_to_date(left(trim(TRACS_CURRENT_EXPIRATION_DATE), 10), 'YYYY-MM-DD') as tracs_current_expiration_date,
        trim(TRACS_STATUS_NAME)                          as tracs_status_name,
        try_to_number(trim(CONTRACT_TERM_MONTHS_QTY))    as contract_term_months_qty,

        -- program
        trim(IS_HUD_ADMINISTERED_IND)                    as is_hud_administered_ind,
        trim(IS_ACC_OLD_IND)                             as is_acc_old_ind,
        trim(IS_ACC_PERFORMANCE_BASED_IND)               as is_acc_performance_based_ind,
        trim(CONTRACT_DOC_TYPE_CODE)                     as contract_doc_type_code,
        trim(PROGRAM_TYPE_NAME)                          as program_type_name,
        trim(PROGRAM_TYPE_GROUP_CODE)                    as program_type_group_code,
        trim(PROGRAM_TYPE_GROUP_NAME)                    as program_type_group_name,

        -- units / rents
        try_to_number(trim(ASSISTED_UNITS_COUNT))        as assisted_units_count,
        try_to_number(trim(RENT_TO_FMR_RATIO), 20, 8)    as rent_to_fmr_ratio,
        trim(RENT_TO_FMR_DESCRIPTION)                    as rent_to_fmr_description,
        try_to_number(trim(C_0BR_COUNT))                 as units_0br_count,
        try_to_number(trim(C_1BR_COUNT))                 as units_1br_count,
        try_to_number(trim(C_2BR_COUNT))                 as units_2br_count,
        try_to_number(trim(C_3BR_COUNT))                 as units_3br_count,
        try_to_number(trim(C_4BR_COUNT))                 as units_4br_count,
        try_to_number(trim(C_5PLUSBR_COUNT))             as units_5plusbr_count,
        try_to_number(trim(C_0BR_FMR))                   as fmr_0br,
        try_to_number(trim(C_1BR_FMR))                   as fmr_1br,
        try_to_number(trim(C_2BR_FMR))                   as fmr_2br,
        try_to_number(trim(C_3BR_FMR))                   as fmr_3br,
        try_to_number(trim(C_4BR_FMR))                   as fmr_4br,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                 as _ingested_at,
        SOURCE_RUN_ID                                    as _source_run_id,
        SRC_SHA256                                       as _src_sha256

    from keyed

)

select * from renamed
