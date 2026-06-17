{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_nara_wra_aad__japanese_american_relocation_records') }}

),

final as (

    select

        -- surrogate / natural key
        record_id,

        -- key identifiers exposed for cross-source joins
        person_name,
        date_of_birth,
        fips_code,
        relocation_center                                           as camp_location,
        relocation_center_state                                     as camp_location_state,
        arrival_date,
        departure_date,

        -- person attributes
        gender,
        citizenship_status,
        occupation,
        family_number,

        -- original residence
        original_residence_city,
        original_residence_state,

        -- derived: length of stay in days
        datediff(
            'day',
            arrival_date,
            coalesce(departure_date, current_date())
        )                                                           as days_in_camp,

        -- departure context
        departure_reason,

        -- archival provenance
        series,
        record_group,

        -- source metadata
        'fed_nara_wra_aad'                                          as source_id,
        _ingested_at,
        _source_run_id

    from base

)

select * from final
