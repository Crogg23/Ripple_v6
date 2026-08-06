{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_CONSOLIDATED_SCREENING_LIST') }}

),

renamed as (

    select
        -- primary identifiers
        ID                                                        as _id,
        ENTITY_NUMBER                                             as entity_number,

        -- descriptive attributes
        SOURCE                                                    as source_name,
        TYPE                                                      as entity_type,
        NAME                                                      as party_name,
        TITLE                                                     as party_title,

        -- semi-structured / list columns (kept as text; parsed downstream if needed)
        PROGRAMS                                                  as programs,
        ADDRESSES                                                 as addresses,
        ALT_NAMES                                                 as alt_names,
        IDS                                                       as ids,
        CITIZENSHIPS                                              as citizenships,
        NATIONALITIES                                             as nationalities,
        PLACES_OF_BIRTH                                           as places_of_birth,
        DATES_OF_BIRTH                                            as dates_of_birth,

        -- regulatory / order details
        FEDERAL_REGISTER_NOTICE                                   as federal_register_notice,
        try_to_date(START_DATE)                                   as start_date,
        try_to_date(END_DATE)                                     as end_date,
        STANDARD_ORDER                                            as standard_order,
        LICENSE_REQUIREMENT                                       as license_requirement,
        LICENSE_POLICY                                            as license_policy,

        -- vessel attributes
        CALL_SIGN                                                 as call_sign,
        VESSEL_TYPE                                               as vessel_type,
        try_to_number(GROSS_TONNAGE)                              as gross_tonnage,
        try_to_number(GROSS_REGISTERED_TONNAGE)                   as gross_registered_tonnage,
        VESSEL_FLAG                                               as vessel_flag,
        VESSEL_OWNER                                              as vessel_owner,

        -- supplemental
        REMARKS                                                   as remarks,
        SOURCE_LIST_URL                                           as source_list_url,
        SOURCE_INFORMATION_URL                                    as source_information_url,

        -- pipeline metadata
        _INGESTED_AT                                              as _ingested_at,
        _SOURCE_RUN_ID                                            as _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by _id
        order by _ingested_at desc
    ) = 1

)

select * from deduped
