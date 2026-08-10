{{ config(materialized='view') }}

-- Built 2026-08-10 (backlog wave 3). EPA RCRAInfo compliance evaluations (inspections): one row = one evaluation record. Composite near-unique; provenance tiebreaker on the key (multiple agency rows can share an identifier).

with

source as (

    select * from {{ source('ripple_raw', 'FED_EPA_RCRA_EVALUATIONS') }}

),

renamed as (

    select

        -- composite is near-unique in the published flat file; row_number
        -- provenance tiebreaker makes the key unique (documented, not hidden)
        {{ dbt_utils.generate_surrogate_key(['id_number', 'activity_location', 'evaluation_identifier', 'evaluation_type', 'evaluation_start_date']) }} || '-' ||
            row_number() over (
                partition by id_number, activity_location, evaluation_identifier, evaluation_type, evaluation_start_date
                order by hash(*)
            )                                               as evaluation_record_id,

        trim(ID_NUMBER)                                         as id_number,
        trim(ACTIVITY_LOCATION)                                 as activity_location,
        trim(EVALUATION_IDENTIFIER)                             as evaluation_identifier,
        trim(EVALUATION_TYPE)                                   as evaluation_type,
        trim(EVALUATION_DESC)                                   as evaluation_desc,
        trim(EVALUATION_AGENCY)                                 as evaluation_agency,
        try_to_date(trim(EVALUATION_START_DATE))                as evaluation_start_date,
        trim(FOUND_VIOLATION)                                   as found_violation,

        -- metadata
        ingested_at as _ingested_at,
        source_run_id as _source_run_id

    from source

)

select * from renamed
