{{ config(materialized='table') }}

with

base as (

    select * from {{ ref('stg_fed_fda_drug_enforcement__drug_enforcement_recalls') }}

),

enriched as (

    select

        -- primary key
        recall_number,

        -- cross-source join keys
        event_id,
        product_ndc,

        -- status & classification
        status,
        classification,

        -- derived severity rank for analytics
        case classification
            when 'Class I'   then 1
            when 'Class II'  then 2
            when 'Class III' then 3
            else null
        end                                                         as classification_severity_rank,

        voluntary_mandated,
        initial_firm_notification,

        -- product
        product_type,
        product_description,
        product_quantity,
        reason_for_recall,
        distribution_pattern,
        code_info,
        more_code_info,

        -- dates
        recall_initiation_date,
        center_classification_date,
        termination_date,
        report_date,

        -- days open metric
        case
            when termination_date is not null and recall_initiation_date is not null
                then datediff('day', recall_initiation_date, termination_date)
            when recall_initiation_date is not null
                then datediff('day', recall_initiation_date, current_date)
            else null
        end                                                         as days_open,

        -- is active flag
        (status ilike '%ongoing%')::boolean                         as is_active,

        -- recalling firm
        recalling_firm,
        address_1,
        address_2,
        city,
        state,
        postal_code,
        country,

        -- full address for convenience
        trim(
            coalesce(address_1, '') || ' ' ||
            coalesce(address_2, '') || ', ' ||
            coalesce(city, '') || ', ' ||
            coalesce(state, '') || ' ' ||
            coalesce(postal_code, '') || ', ' ||
            coalesce(country, '')
        )                                                           as recalling_firm_full_address,

        -- source metadata
        'fed_fda_drug_enforcement'                                  as source_id,
        _ingested_at,
        _source_run_id

    from base

)

select * from enriched
