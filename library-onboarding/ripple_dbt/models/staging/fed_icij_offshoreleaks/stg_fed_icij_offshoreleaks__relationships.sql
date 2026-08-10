{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog). ICIJ Offshore Leaks
  relationships: the edges connecting entities, officers, intermediaries and
  addresses (officer_of, registered_address, intermediary_of, etc.).
  Grain: one row = one edge as published. (start, end, type, link) is NOT
  unique: 3,310,451 distinct over 3,339,267 rows — ICIJ republishes the same
  edge from multiple leak investigations. Kept as landed, no dedup.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS') }}
),

renamed as (
    select
        nullif(trim(NODE_ID_START), '')                           as node_id_start,
        nullif(trim(NODE_ID_END), '')                             as node_id_end,
        nullif(trim(REL_TYPE), '')                                as rel_type,
        nullif(trim(LINK), '')                                    as link,
        nullif(trim(STATUS), '')                                  as status,
        try_to_date(trim(START_DATE), 'DD-MON-YYYY')              as start_date,
        try_to_date(trim(END_DATE), 'DD-MON-YYYY')                as end_date,
        nullif(trim(SOURCEID), '')                                as source_leak,
        to_timestamp_ntz(INGESTED_AT)                             as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
