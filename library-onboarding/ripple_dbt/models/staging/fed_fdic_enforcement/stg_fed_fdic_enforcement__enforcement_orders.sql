{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'FED_FDIC_ENFORCEMENT') }}

),

renamed as (

    select
        -- identifiers
        DOCKET_NUMBER                                   as docket_number,
        NMLS_ID                                         as nmls_id,
        FDIC_CERT_NUMBER                                as fdic_cert_number,
        RESPONDENT_NAME                                 as respondent_name,

        -- dates
        try_to_date(ISSUED_DATE, 'YYYY-MM-DD')          as issued_date,

        -- descriptive fields
        ORDER_TITLE                                     as order_title,
        ORDER_CATEGORY                                  as order_category,
        ACTION_TYPE                                     as action_type,
        RESPONDENT_TYPE                                 as respondent_type,
        BANK_NAME                                       as bank_name,
        BANK_CITY                                       as bank_city,
        BANK_STATE                                      as bank_state,
        ORDER_ATTACHMENT_TEXT                           as order_attachment_text,

        -- numeric casting
        try_to_number(FDIC_CERT_NUMBER)                 as fdic_cert_number_int,
        try_to_number(NMLS_ID)                          as nmls_id_int,

        -- ingestion metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by docket_number, respondent_name, issued_date
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    -- surrogate / primary key
    {{ dbt_utils.generate_surrogate_key(['docket_number', 'respondent_name', 'issued_date']) }}
                                                        as enforcement_order_sk,

    docket_number,
    nmls_id,
    fdic_cert_number,
    fdic_cert_number_int,
    nmls_id_int,
    respondent_name,
    issued_date,
    order_title,
    order_category,
    action_type,
    respondent_type,
    bank_name,
    bank_city,
    bank_state,
    order_attachment_text,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
