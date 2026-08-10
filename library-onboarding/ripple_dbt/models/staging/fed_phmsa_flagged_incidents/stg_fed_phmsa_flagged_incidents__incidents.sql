{{ config(materialized='view') }}

-- The landing table is 624 columns wide (the full PHMSA incident form).
-- This staging model selects a curated core: report identity, dates, operator
-- identity, location, commodity, release volumes, casualties, and incident
-- status. The full 624-column width stays in landing for anyone who needs the
-- long tail of form fields.

with

source as (

    select * from {{ source('ripple_raw', 'FED_PHMSA_FLAGGED_INCIDENTS') }}

),

renamed as (

    select

        -- identifiers
        trim(REPORT_NUMBER)                            as report_number,
        trim(SUPPLEMENTAL_NUMBER)                      as supplemental_number,
        trim(REPORT_TYPE)                              as report_type,
        trim(NRC_RPT_NUM)                              as nrc_report_number,

        -- dates
        try_to_date(trim(REPORT_RECEIVED_DATE))        as report_received_date,
        try_to_number(trim(IYEAR))                     as incident_year,
        try_to_timestamp(trim(LOCAL_DATETIME))         as local_datetime,
        trim(TIME_ZONE)                                as time_zone,

        -- operator identity (PHMSA_OPERATOR_ID is the operator join key)
        trim(PHMSA_OPERATOR_ID)                        as phmsa_operator_id,
        trim(NAME)                                     as operator_name,
        trim(OPERATOR_STREET_ADDRESS)                  as operator_street_address,
        trim(OPERATOR_CITY_NAME)                       as operator_city,
        trim(OPERATOR_STATE_ABBREVIATION)              as operator_state,
        trim(OPERATOR_POSTAL_CODE)                     as operator_postal_code,

        -- location
        try_to_number(trim(LOCATION_LATITUDE))         as location_latitude,
        try_to_number(trim(LOCATION_LONGITUDE))        as location_longitude,

        -- commodity and release
        trim(COMMODITY_RELEASED_TYPE)                  as commodity_released_type,
        trim(COMMODITY_DETAILS)                        as commodity_details,
        try_to_number(trim(UNINTENTIONAL_RELEASE))     as unintentional_release_volume,
        try_to_number(trim(INTENTIONAL_RELEASE))       as intentional_release_volume,

        -- fatalities
        trim(FATALITY_IND)                             as fatality_ind,
        try_to_number(trim(NUM_EMP_FATALITIES))        as num_employee_fatalities,
        try_to_number(trim(NUM_CONTR_FATALITIES))      as num_contractor_fatalities,
        try_to_number(trim(NUM_ER_FATALITIES))         as num_emergency_responder_fatalities,
        try_to_number(trim(NUM_WORKER_FATALITIES))     as num_worker_fatalities,
        try_to_number(trim(NUM_GP_FATALITIES))         as num_public_fatalities,
        try_to_number(trim(FATAL))                     as total_fatalities,

        -- injuries
        trim(INJURY_IND)                               as injury_ind,
        try_to_number(trim(NUM_EMP_INJURIES))          as num_employee_injuries,
        try_to_number(trim(NUM_CONTR_INJURIES))        as num_contractor_injuries,
        try_to_number(trim(NUM_ER_INJURIES))           as num_emergency_responder_injuries,
        try_to_number(trim(NUM_WORKER_INJURIES))       as num_worker_injuries,
        try_to_number(trim(NUM_GP_INJURIES))           as num_public_injuries,
        try_to_number(trim(INJURE))                    as total_injuries,

        -- incident status
        trim(STATUS_WHEN_IDENTIFIED)                   as status_when_identified,
        trim(SHUTDOWN_DUE_ACCIDENT_IND)                as shutdown_due_accident_ind,

        -- metadata
        _INGESTED_AT                                   as _loaded_at,
        _SOURCE_RUN_ID                                 as _source_run_id,
        _SRC_SHA256                                    as _src_sha256

    from source

)

select * from renamed
