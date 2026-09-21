{{ config(materialized='view') }}

-- HAND-EDITED 2026-09-19: dedupe is a whole-raw-row hash (_row_hash), see the
-- comment in deduped. The staging generator skips files carrying this marker.

with source as (

    -- _row_hash: hash of every landing column except the load stamps
    select *, hash(* exclude (_INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256)) as _row_hash
    from {{ source('ripple_raw', 'FED_NARA_WRA_AAD') }}

),

renamed_cast as (

    select

        -- identifiers
        RECORD_ID                                          as record_id,
        SERIES_ID                                         as series_id,

        -- key dimensions
        PERSON_NAME                                       as person_name,
        try_to_date(DATE, 'YYYY-MM-DD')                   as record_date,
        DATE                                              as raw_date,
        CAMP_LOCATION                                     as camp_location,
        FIPS                                              as fips,
        GEO                                               as geo,

        -- person attributes
        {{ stg_int('AGE') }}                                as age,
        upper(trim(SEX))                                  as sex,
        upper(trim(CITIZENSHIP_STATUS))                   as citizenship_status,
        FAMILY_NUMBER                                     as family_number,

        -- supplemental
        NOTES_FIELD                                       as notes_field,

        -- metadata
        _ingested_at,
        _source_run_id,

        -- whole-raw-row hash, carried for the dedupe only
        _row_hash

    from source

),

deduped as (

    -- 2026-09-19: the old partition was record_id. It hid 35 of 36 landing
    -- rows on a single load -- record_id does not identify a row. The dedupe is
    -- now the whole-raw-row hash, so only exact copies are dropped (23 exact
    -- copies in landing).
    select *,
        row_number() over (
            partition by _row_hash
            order by _ingested_at desc
        ) as _row_num
    from renamed_cast

)

select
    record_id,
    series_id,
    person_name,
    record_date,
    raw_date,
    camp_location,
    fips,
    geo,
    age,
    sex,
    citizenship_status,
    family_number,
    notes_field,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
