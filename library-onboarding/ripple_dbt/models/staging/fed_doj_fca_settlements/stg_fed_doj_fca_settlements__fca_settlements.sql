{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_DOJ_FCA_SETTLEMENTS') }}

),

renamed as (

    select
        -- identifiers
        {{ dbt_utils.generate_surrogate_key(['DEFENDANT_COMPANY', 'DEFENDANT_PERSON', 'SETTLEMENT_DATE']) }} as fca_settlement_id,
        trim(DEFENDANT_COMPANY)                                         as company_id,
        trim(DEFENDANT_PERSON)                                          as person_name,
        try_to_date(trim(SETTLEMENT_DATE))                              as date,

        -- descriptive fields
        trim(CASE_TITLE)                                                as case_title,
        try_to_number(trim(FISCAL_YEAR))                                as fiscal_year,
        try_to_double(replace(replace(trim(SETTLEMENT_AMOUNT), '$', ''), ',', '')) as settlement_amount,
        case
            when upper(trim(QUI_TAM)) in ('YES', 'Y', 'TRUE', '1') then true
            when upper(trim(QUI_TAM)) in ('NO', 'N', 'FALSE', '0') then false
            else null
        end                                                             as is_qui_tam,
        trim(RELATOR_NAME)                                              as relator_name,
        try_to_double(replace(replace(trim(RELATOR_SHARE), '$', ''), ',', '')) as relator_share,
        trim(FRAUD_TYPE)                                                as fraud_type,
        trim(AGENCY_DEFRAUDED)                                          as agency_defrauded,
        trim(CASE_NUMBER)                                               as case_number,
        trim(DISTRICT)                                                  as district,
        trim(PRESS_RELEASE_URL)                                         as press_release_url,
        trim(SOURCE_URL)                                                as source_url,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by fca_settlement_id
        order by _ingested_at desc
    ) = 1

)

select * from deduped
