{{ config(materialized='view') }}

-- HAND-EDITED 2026-09-19: dedupe is a whole-raw-row hash (_row_hash), see the
-- comment in deduped. The staging generator skips files carrying this marker.

with source as (

    -- _row_hash: hash of every landing column except the load stamps
    select *, hash(* exclude (_INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256)) as _row_hash
    from {{ source('ripple_raw', 'INTL_GR_GEMI') }}

),

renamed as (

    select

        -- key identifiers
        GEMI_NUMBER                                    as gemi_number,
        AFM                                            as afm,

        -- company attributes
        COMPANY_NAME                                   as company_name,
        DISTINCTIVE_TITLE                              as distinctive_title,
        LEGAL_FORM                                     as legal_form,
        STATUS                                         as status,
        REGISTRATION_SUSPENSION                        as registration_suspension,
        SPECIAL_DESIGNATIONS                           as special_designations,
        LOCAL_GEMI_OFFICE                              as local_gemi_office,

        -- dates
        {{ stg_date('FORMATION_DATE') }}                    as formation_date,
        {{ stg_date('CLOSURE_DATE') }}                      as closure_date,
        {{ stg_date('KAK_CHANGE_DATE') }}                   as kak_change_date,

        -- location
        CITY                                           as city,
        POSTAL_CODE                                    as postal_code,

        -- metadata
        _ingested_at,
        _source_run_id,

        -- whole-raw-row hash, carried for the dedupe only
        _row_hash

    from source

),

deduped as (

    -- 2026-09-19: the old partition was gemi_number. It hid 39 of 40 landing
    -- rows on a single load -- gemi_number does not identify a row. The dedupe
    -- is now the whole-raw-row hash, so only exact copies are dropped (33 exact
    -- copies in landing).
    select *,
        row_number() over (
            partition by _row_hash
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where gemi_number is not null

)

select
    gemi_number,
    afm,
    company_name,
    distinctive_title,
    legal_form,
    status,
    registration_suspension,
    special_designations,
    local_gemi_office,
    formation_date,
    closure_date,
    kak_change_date,
    city,
    postal_code,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
