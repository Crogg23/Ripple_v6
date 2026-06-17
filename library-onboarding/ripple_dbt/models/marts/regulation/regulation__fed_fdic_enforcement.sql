{{ config(materialized='table') }}

with base as (

    select *
    from {{ ref('stg_fed_fdic_enforcement__enforcement_orders') }}

)

select
    -- primary key
    enforcement_order_sk,

    -- cross-source join keys
    fdic_cert_number                            as company_id,          -- FDIC cert as company identifier
    fdic_cert_number,
    fdic_cert_number_int,
    docket_number,
    nmls_id,
    nmls_id_int,
    respondent_name                             as person_name,
    respondent_name,

    -- date keys
    issued_date                                 as date,
    issued_date,
    year(issued_date)                           as issued_year,
    month(issued_date)                          as issued_month,

    -- order attributes
    order_title,
    order_category,
    action_type,
    respondent_type,

    -- institution attributes
    bank_name,
    bank_city,
    bank_state,

    -- full text
    order_attachment_text,

    -- lineage
    _ingested_at,
    _source_run_id,
    'fed_fdic_enforcement'                      as source_id

from base
