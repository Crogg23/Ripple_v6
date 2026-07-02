{{ config(materialized='table') }}

with base as (

    select *
    from {{ ref('stg_fed_us_usaspending_api__federal_awards') }}

),

final as (

    select

        -- -------------------------------------------------------
        -- Key identifiers (exposed for cross-source joins)
        -- -------------------------------------------------------
        award_id,
        generated_unique_award_id,
        recipient_uei,
        recipient_duns,
        recipient_ein,
        naics_code,
        cfda_number,
        treasury_account_symbol,
        federal_account_code,
        awarding_agency_code                                    as toptier_agency_code,
        place_of_performance_fips,
        recipient_location_fips,

        -- -------------------------------------------------------
        -- Recipient & agency descriptors
        -- -------------------------------------------------------
        recipient_name,
        awarding_agency_name,
        funding_agency_name,
        naics_description,
        cfda_title,

        -- -------------------------------------------------------
        -- Award classification
        -- -------------------------------------------------------
        award_type,
        def_code,
        fiscal_year,

        -- -------------------------------------------------------
        -- Geography
        -- -------------------------------------------------------
        place_of_performance_state,
        place_of_performance_city,
        recipient_location_state,

        -- -------------------------------------------------------
        -- Financials
        -- -------------------------------------------------------
        total_obligation,
        total_outlay,
        award_amount,

        -- -------------------------------------------------------
        -- Counts
        -- -------------------------------------------------------
        transaction_count,
        subaward_count,

        -- -------------------------------------------------------
        -- Dates
        -- -------------------------------------------------------
        start_date,
        end_date,
        last_modified_date,

        -- -------------------------------------------------------
        -- Derived helper columns
        -- -------------------------------------------------------
        datediff('day', start_date, end_date)                   as award_duration_days,
        case
            when award_amount >= 10000000  then 'Large (>=10M)'
            when award_amount >= 1000000   then 'Medium (1M-10M)'
            when award_amount >= 100000    then 'Small (100K-1M)'
            when award_amount >= 0         then 'Micro (<100K)'
            else 'Unknown'
        end                                                      as award_size_band,

        -- -------------------------------------------------------
        -- Metadata
        -- -------------------------------------------------------
        _ingested_at,
        _source_run_id

    from base

)

select * from final
