{{ config(materialized='table') }}

with

staging as (

    select * from {{ ref('stg_fed_cms_tic_mrf__transparency_in_coverage_rates') }}

),

final as (

    select

        -- surrogate primary key
        _row_hash                                                    as transparency_in_coverage_rate_key,

        -- cross-source join identifiers (kept at top for discoverability)
        npi,
        plan_id,
        plan_id_type,
        billing_code,
        billing_code_type,
        billing_code_type_version,
        tin_type,
        tin_value,
        service_code,

        -- payer / plan dimensions
        reporting_entity_name                                        as payer_name,
        reporting_entity_type,
        plan_name,
        plan_market_type,

        -- rate facts
        description                                                  as billing_code_description,
        negotiation_arrangement,
        negotiated_type,
        negotiated_rate,
        billing_class,

        -- date dimensions
        effective_date,
        expiration_date,
        last_updated_on,

        -- derived helpers
        datediff('day', effective_date, expiration_date)             as rate_validity_days,
        case
            when expiration_date >= current_date() then true
            else false
        end                                                          as is_rate_active,

        -- provenance
        source_file_url,
        _ingested_at

    from staging

)

select * from final
