-- KEY WIDENED 2026-09-22 (row sweep): facility_name alone hid 2 real facilities.
-- BUTLER COUNTY JAIL is one in OH and one in another state; EDEN DETENTION CENTER sits in two AORs.
{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_ICE_DETENTION_FACILITY_LIST') }}

),

renamed as (

    select

        -- identifiers
        FACILITY_NAME                                    as facility_name,

        -- dimensions
        AOR                                              as aor,
        CITY                                             as city,
        STATE                                            as state,
        FACILITY_TYPE_DETAILED                           as facility_type_detailed,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by facility_name, city, state, aor
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    aor,
    facility_name,
    city,
    state,
    facility_type_detailed,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
