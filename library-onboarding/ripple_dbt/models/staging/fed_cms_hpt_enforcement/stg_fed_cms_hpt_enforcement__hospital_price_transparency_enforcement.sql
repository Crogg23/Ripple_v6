{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_CMS_HPT_ENFORCEMENT') }}

),

renamed_cast as (

    select
        -- identifiers
        trim(hospital_name)                                      as hospital_name,
        trim(npi)                                                as npi,

        -- location
        trim(state)                                              as state,
        trim(city)                                               as city,

        -- enforcement details
        trim(enforcement_action_type)                            as enforcement_action_type,
        try_to_date(trim(action_date), 'YYYY-MM-DD')            as action_date,
        trim(outcome)                                            as outcome,
        try_to_double(replace(trim(penalty_amount), ',', ''))   as penalty_amount,
        trim(corrective_action_plan)                             as corrective_action_plan,
        trim(compliance_status)                                  as compliance_status,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed_cast
    qualify row_number() over (
        partition by npi, hospital_name, action_date, enforcement_action_type
        order by _ingested_at desc
    ) = 1

)

select * from deduped
