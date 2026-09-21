{{ config(materialized='view') }}

-- HAND-EDITED 2026-09-19: dedupe is a whole-raw-row hash (_row_hash), see the
-- comment in deduped. The staging generator skips files carrying this marker.

with source as (

    -- _row_hash: hash of every landing column except the load stamps
    select *, hash(* exclude (_INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256)) as _row_hash
    from {{ source('ripple_raw', 'FED_MAPPING_INEQUALITY') }}

),

renamed as (

    select
        -- identifiers
        holc_id                                                        as holc_id,
        city                                                           as city,
        state                                                          as state,
        fips                                                           as fips,
        holc_grade                                                     as holc_grade,

        -- attributes
        holc_color                                                     as holc_color,
        area_description_data                                          as area_description_data,
        residential_description                                        as residential_description,
        {{ stg_int('year_mapped') }}                                     as year_mapped,
        geometry                                                       as geometry,
        {{ stg_float('lat') }}                                             as lat,
        {{ stg_float('lon') }}                                             as lon,

        -- derived composite key for deduplication / joins
        -- 2026-09-19: the five parts alone repeat across real rows, so the
        -- whole-raw-row hash is appended to keep the key one-per-row. Parts are
        -- coalesced because concat_ws returns NULL when any argument is NULL.
        concat_ws('|', coalesce(holc_id, ''), coalesce(fips, ''), coalesce(city, ''),
                  coalesce(state, ''), coalesce(holc_grade, ''))
            || '|' || _row_hash                                        as holc_neighborhood_key,

        -- metadata
        _ingested_at,
        _source_run_id,

        -- whole-raw-row hash, carried for the dedupe only
        _row_hash

    from source

),

deduped as (

    -- 2026-09-19: the old partition was holc_neighborhood_key
    -- (holc_id|fips|city|state|holc_grade). It hid 8,999 of 10,154 landing rows
    -- on a single load -- that key does not identify a row. The dedupe is now
    -- the whole-raw-row hash, so only exact copies are dropped (0 exact copies
    -- in landing).
    select *,
        row_number() over (
            partition by _row_hash
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    holc_id,
    city,
    state,
    fips,
    holc_grade,
    holc_color,
    area_description_data,
    residential_description,
    year_mapped,
    geometry,
    lat,
    lon,
    holc_neighborhood_key,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
