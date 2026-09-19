{{ config(materialized='view') }}

-- HAND-EDITED 2026-09-19: dedupe is a whole-raw-row hash (_row_hash), see the
-- comment in deduped. The staging generator skips files carrying this marker.

with source as (

    -- _row_hash: hash of every landing column except the load stamps
    select *, hash(* exclude (_INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256)) as _row_hash
    from {{ source('ripple_raw', 'INTL_ES_BORME') }}

),

renamed as (

    select
        -- key identifiers
        COMPANY_ID                                         as company_id,
        COUNTRY                                            as country,
        try_to_date(DATE, 'YYYY-MM-DD')                    as date,

        -- descriptive attributes
        BORME_ISSUE_NUMBER                                 as borme_issue_number,
        SECTION                                            as section,
        COMPANY_NAME                                       as company_name,
        ACT_TYPE                                           as act_type,
        ACT_DESCRIPTION                                    as act_description,
        PROVINCE                                           as province,
        CVE                                                as cve,
        PDF_URL                                            as pdf_url,

        -- metadata
        _ingested_at,
        _source_run_id,

        -- whole-raw-row hash, carried for the dedupe only
        _row_hash

    from source

),

deduped as (

    -- 2026-09-19: the old partition was (company_id, country, date, act_type,
    -- cve). It hid 22 of 25 landing rows on a single load -- those five columns
    -- do not identify a row. The dedupe is now the whole-raw-row hash, so only
    -- exact copies are dropped (10 exact copies in landing).
    select * exclude (_row_hash)
    from renamed
    qualify row_number() over (
        partition by _row_hash
        order by _ingested_at desc
    ) = 1

)

select * from deduped
