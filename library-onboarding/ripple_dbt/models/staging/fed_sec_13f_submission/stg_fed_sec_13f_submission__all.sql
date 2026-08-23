{{ config(tags=['minimal_staging']) }}

-- GRAIN: one row per 13F filing (accession number)
-- Source is the true submission-header landing table (FED_SEC_13F_SUBMISSIONS,
-- mapped via the source identifier). The old target (FED_SEC_13F_SUBMISSION,
-- singular) holds holdings-shaped rows and is queued for retirement.

with source as (

    select * from {{ source('ripple_raw', 'FED_SEC_13F_SUBMISSION_HEADERS') }}

),

cleaned as (

    select
        ACCESSION_NUMBER                as sec_accession_number,
        nullif(trim(CIK), '')           as cik,
        try_to_date(FILING_DATE, 'DD-MON-YYYY')     as filing_date,
        try_to_date(PERIODOFREPORT, 'DD-MON-YYYY')  as period_of_report,
        nullif(trim(SUBMISSIONTYPE), '')            as submission_type,
        _SRC_FILE                       as _src_file,
        _INGESTED_AT                    as _loaded_at,
        _SOURCE_RUN_ID                  as _source_run_id
    from source

)

select *
from cleaned
qualify row_number() over (
    partition by sec_accession_number
    order by _loaded_at desc
) = 1
