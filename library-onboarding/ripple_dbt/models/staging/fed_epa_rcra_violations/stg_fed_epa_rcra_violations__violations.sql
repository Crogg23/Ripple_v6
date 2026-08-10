{{ config(materialized='view') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo violations: one row = one violation record. Composite near-unique; provenance tiebreaker on the key (same violation type can be re-determined).

with

source as (

    select * from {{ source('ripple_raw', 'FED_EPA_RCRA_VIOLATIONS') }}

),

renamed as (

    select

        -- composite is near-unique in the published flat file; row_number
        -- provenance tiebreaker makes the key unique (documented, not hidden)
        {{ dbt_utils.generate_surrogate_key(['id_number', 'activity_location', 'violation_type', 'date_violation_determined']) }} || '-' ||
            row_number() over (
                partition by id_number, activity_location, violation_type, date_violation_determined
                order by hash(*)
            )                                               as violation_record_id,

        trim(ID_NUMBER)                                         as id_number,
        trim(ACTIVITY_LOCATION)                                 as activity_location,
        trim(VIOLATION_TYPE)                                    as violation_type,
        trim(VIOLATION_TYPE_DESC)                               as violation_type_desc,
        trim(VIOL_DETERMINED_BY_AGENCY)                         as viol_determined_by_agency,
        try_to_date(trim(DATE_VIOLATION_DETERMINED))            as date_violation_determined,
        try_to_date(trim(ACTUAL_RTC_DATE))                      as actual_rtc_date,
        try_to_date(trim(SCHEDULED_COMPLIANCE_DATE))            as scheduled_compliance_date,

        -- metadata
        ingested_at as _ingested_at,
        source_run_id as _source_run_id

    from source

)

select * from renamed
