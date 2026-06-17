{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_NARA_WRA_AAD') }}

),

renamed as (

    select

        -- primary identifier
        record_id                                               as record_id,

        -- person attributes
        person_name                                             as person_name,
        try_to_date(date_of_birth, 'YYYY-MM-DD')               as date_of_birth,
        gender                                                  as gender,
        citizenship_status                                      as citizenship_status,
        occupation                                              as occupation,
        family_number                                           as family_number,

        -- original residence
        original_residence_city                                 as original_residence_city,
        original_residence_state                                as original_residence_state,
        fips_code                                               as fips_code,

        -- relocation center
        relocation_center                                       as relocation_center,
        relocation_center_state                                 as relocation_center_state,

        -- relocation dates / reason
        try_to_date(arrival_date, 'YYYY-MM-DD')                 as arrival_date,
        try_to_date(departure_date, 'YYYY-MM-DD')               as departure_date,
        departure_reason                                        as departure_reason,

        -- archival metadata
        series                                                  as series,
        record_group                                            as record_group,

        -- pipeline metadata
        _ingested_at                                            as _ingested_at,
        _source_run_id                                          as _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by record_id
        order by _ingested_at desc
    ) = 1

)

select * from deduped
