{{ config(materialized='view') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo enforcement actions with penalty amounts (proposed/final monetary penalties, supplemental project and cost-recovery amounts): one row = one enforcement record. Composite near-unique; provenance tiebreaker on the key.

with

source as (

    select * from {{ source('ripple_raw', 'FED_EPA_RCRA_ENFORCEMENTS') }}

),

renamed as (

    select

        -- composite is near-unique in the published flat file; row_number
        -- provenance tiebreaker makes the key unique (documented, not hidden)
        {{ dbt_utils.generate_surrogate_key(['id_number', 'activity_location', 'enforcement_identifier', 'enforcement_type', 'enforcement_action_date']) }} || '-' ||
            row_number() over (
                partition by id_number, activity_location, enforcement_identifier, enforcement_type, enforcement_action_date
                order by hash(*)
            )                                               as enforcement_record_id,

        trim(ID_NUMBER)                                         as id_number,
        trim(ACTIVITY_LOCATION)                                 as activity_location,
        trim(ENFORCEMENT_IDENTIFIER)                            as enforcement_identifier,
        trim(ENFORCEMENT_TYPE)                                  as enforcement_type,
        trim(ENFORCEMENT_DESC)                                  as enforcement_desc,
        trim(ENFORCEMENT_AGENCY)                                as enforcement_agency,
        try_to_date(trim(ENFORCEMENT_ACTION_DATE))              as enforcement_action_date,
        try_to_number(trim(PMP_AMOUNT))                         as pmp_amount,
        try_to_number(trim(FMP_AMOUNT))                         as fmp_amount,
        try_to_number(trim(FSC_AMOUNT))                         as fsc_amount,
        try_to_number(trim(SCR_AMOUNT))                         as scr_amount,

        -- metadata
        ingested_at as _ingested_at,
        source_run_id as _source_run_id

    from source

)

select * from renamed
