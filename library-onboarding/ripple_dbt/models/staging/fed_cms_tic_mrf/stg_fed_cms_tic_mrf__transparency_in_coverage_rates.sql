{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_CMS_TIC_MRF') }}

),

renamed_cast as (

    select

        -- identifiers
        npi                                                          as npi,
        plan_id                                                      as plan_id,
        plan_id_type                                                 as plan_id_type,
        billing_code                                                 as billing_code,
        billing_code_type                                            as billing_code_type,
        billing_code_type_version                                    as billing_code_type_version,
        tin_type                                                     as tin_type,
        tin_value                                                    as tin_value,
        service_code                                                 as service_code,

        -- payer / plan attributes
        reporting_entity_name                                        as reporting_entity_name,
        reporting_entity_type                                        as reporting_entity_type,
        plan_name                                                    as plan_name,
        plan_market_type                                             as plan_market_type,

        -- rate attributes
        description                                                  as description,
        negotiation_arrangement                                      as negotiation_arrangement,
        negotiated_type                                              as negotiated_type,
        try_to_double(negotiated_rate)                               as negotiated_rate,
        billing_class                                                as billing_class,

        -- dates
        try_to_date(effective_date,  'YYYY-MM-DD')                   as effective_date,
        try_to_date(expiration_date, 'YYYY-MM-DD')                   as expiration_date,
        try_to_date(last_updated_on, 'YYYY-MM-DD')                   as last_updated_on,

        -- provenance
        source_file_url                                              as source_file_url,
        try_to_timestamp(ingested_at)                                as _ingested_at,

        -- surrogate / dedup key (SHA2 over all business columns)
        sha2(
            coalesce(npi,                   '') ||
            coalesce(plan_id,               '') ||
            coalesce(billing_code,          '') ||
            coalesce(billing_code_type,     '') ||
            coalesce(negotiation_arrangement,'') ||
            coalesce(negotiated_type,       '') ||
            coalesce(negotiated_rate,       '') ||
            coalesce(effective_date,        '') ||
            coalesce(expiration_date,       '') ||
            coalesce(tin_value,             '') ||
            coalesce(service_code,          '')
        )                                                            as _row_hash

    from source

),

deduped as (

    select *
    from renamed_cast
    qualify row_number() over (
        partition by _row_hash
        order by _ingested_at desc nulls last
    ) = 1

)

select * from deduped
