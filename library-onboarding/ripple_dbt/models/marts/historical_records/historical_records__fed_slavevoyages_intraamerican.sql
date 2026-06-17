{{ config(materialized='table') }}

with base as (

    select *
    from {{ ref('stg_fed_slavevoyages_intraamerican__intra_american_voyages') }}

),

enriched as (

    select
        -- primary key
        voyage_id,

        -- temporal identifiers
        date_of_departure,
        year_of_departure,

        -- geographic identifiers
        port_of_departure,
        port_of_arrival,
        country_of_departure,
        country_of_arrival,

        -- person / organisation identifiers
        captain_name                                                         as person_name,
        slave_trade_company,

        -- measures
        num_enslaved_embarked,
        num_enslaved_disembarked,
        coalesce(num_enslaved_embarked, 0)
            - coalesce(num_enslaved_disembarked, 0)                          as num_enslaved_mortality_estimate,

        -- vessel
        vessel_name,

        -- provenance
        source_citation,

        -- cross-source join keys (standardised names)
        voyage_id                                                            as source_voyage_id,
        'fed_slavevoyages_intraamerican'                                     as source_id,
        country_of_departure                                                 as country,
        cast(null as varchar)                                                as fips_code,

        -- audit
        _ingested_at,
        _source_run_id

    from base

)

select *
from enriched
