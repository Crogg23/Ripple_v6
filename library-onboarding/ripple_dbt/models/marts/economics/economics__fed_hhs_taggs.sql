{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_hhs_taggs__grant_awards') }}

),

final as (

    select

        -- -----------------------------------------------------------------
        -- Primary key
        -- -----------------------------------------------------------------
        award_number,

        -- -----------------------------------------------------------------
        -- Key identifiers for cross-source joins
        -- -----------------------------------------------------------------
        recipient_ein                                               as ein,
        award_date,
        fiscal_year,
        recipient_zip                                               as zip_code,
        recipient_fips                                              as fips_code,
        assistance_listing_number                                   as aln,

        -- -----------------------------------------------------------------
        -- Recipient attributes
        -- -----------------------------------------------------------------
        recipient_name,
        recipient_class,
        recipient_city,
        recipient_state,
        recipient_country,
        metro_nonmetro,

        -- -----------------------------------------------------------------
        -- Award attributes
        -- -----------------------------------------------------------------
        opdiv,
        activity_type,
        award_type,
        award_amount,
        assistance_listing_name,
        project_description,

        -- -----------------------------------------------------------------
        -- Derived / convenience columns
        -- -----------------------------------------------------------------
        date_trunc('year', award_date)                              as award_year,
        date_trunc('month', award_date)                             as award_month,

        case
            when award_amount >= 1000000  then 'large'
            when award_amount >= 100000   then 'medium'
            when award_amount >= 0        then 'small'
            else 'unknown'
        end                                                         as award_size_band,

        -- -----------------------------------------------------------------
        -- Pipeline metadata
        -- -----------------------------------------------------------------
        _ingested_at,
        _source_run_id

    from base

)

select * from final
