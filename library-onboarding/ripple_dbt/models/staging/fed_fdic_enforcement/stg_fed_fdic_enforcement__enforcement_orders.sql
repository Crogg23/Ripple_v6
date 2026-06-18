{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'FED_FDIC_ENFORCEMENT') }}

),

renamed as (

    select
        -- raw fields
        RAW_TEXT                                          as raw_text,
        ORDER_URL                                         as order_url,

        -- parsed / typed fields extracted from raw_text
        -- FDIC certificate number (numeric identifier for the institution)
        try_to_number(
            nullif(trim(regexp_substr(RAW_TEXT, '"fdic_cert_number"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
        )                                                 as fdic_cert_number,

        -- company_id mirrors fdic_cert_number for cross-source keying
        try_to_number(
            nullif(trim(regexp_substr(RAW_TEXT, '"fdic_cert_number"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
        )                                                 as company_id,

        -- docket number
        nullif(trim(regexp_substr(RAW_TEXT, '"docket_number"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as docket_number,

        -- respondent / person name
        nullif(trim(regexp_substr(RAW_TEXT, '"respondent_name"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as respondent_name,

        nullif(trim(regexp_substr(RAW_TEXT, '"person_name"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as person_name,

        -- NMLS ID
        nullif(trim(regexp_substr(RAW_TEXT, '"nmls_id"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as nmls_id,

        -- effective / order date
        try_to_date(
            nullif(trim(regexp_substr(RAW_TEXT, '"date"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
        )                                                 as date,

        -- additional descriptive fields
        nullif(trim(regexp_substr(RAW_TEXT, '"action_type"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as action_type,

        nullif(trim(regexp_substr(RAW_TEXT, '"institution_name"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as institution_name,

        nullif(trim(regexp_substr(RAW_TEXT, '"city"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as city,

        nullif(trim(regexp_substr(RAW_TEXT, '"state"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as state,

        nullif(trim(regexp_substr(RAW_TEXT, '"termination_date"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
                                                          as termination_date_raw,

        try_to_date(
            nullif(trim(regexp_substr(RAW_TEXT, '"termination_date"\s*:\s*"([^"]+)"', 1, 1, 'e', 1)), '')
        )                                                 as termination_date,

        -- ingestion metadata
        current_timestamp()                               as _ingested_at,
        null::varchar                                     as _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by docket_number, fdic_cert_number, coalesce(person_name, respondent_name)
        order by _ingested_at desc
    ) = 1

)

select * from deduped
