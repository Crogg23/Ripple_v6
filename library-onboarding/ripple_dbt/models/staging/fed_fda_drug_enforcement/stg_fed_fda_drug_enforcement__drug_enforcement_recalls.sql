{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FDA_DRUG_ENFORCEMENT') }}

),

renamed_cast as (

    select

        -- key identifiers
        recall_number                                    as recall_number,
        event_id                                        as event_id,
        product_ndc                                     as product_ndc,

        -- status / classification
        status                                          as status,
        classification                                  as classification,
        voluntary_mandated                              as voluntary_mandated,
        initial_firm_notification                       as initial_firm_notification,

        -- product details
        product_type                                    as product_type,
        product_description                             as product_description,
        product_quantity                                as product_quantity,
        reason_for_recall                               as reason_for_recall,
        distribution_pattern                            as distribution_pattern,
        code_info                                       as code_info,
        more_code_info                                  as more_code_info,

        -- dates
        try_to_date(recall_initiation_date)             as recall_initiation_date,
        try_to_date(center_classification_date)         as center_classification_date,
        try_to_date(termination_date)                   as termination_date,
        try_to_date(report_date)                        as report_date,

        -- recalling firm
        recalling_firm                                  as recalling_firm,
        address_1                                       as address_1,
        address_2                                       as address_2,
        city                                            as city,
        state                                           as state,
        postal_code                                     as postal_code,
        country                                         as country,

        -- metadata
        _ingested_at                                    as _ingested_at,
        _source_run_id                                  as _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by recall_number
            order by _ingested_at desc
        ) as _row_num
    from renamed_cast

)

select
    recall_number,
    event_id,
    product_ndc,
    status,
    classification,
    voluntary_mandated,
    initial_firm_notification,
    product_type,
    product_description,
    product_quantity,
    reason_for_recall,
    distribution_pattern,
    code_info,
    more_code_info,
    recall_initiation_date,
    center_classification_date,
    termination_date,
    report_date,
    recalling_firm,
    address_1,
    address_2,
    city,
    state,
    postal_code,
    country,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
