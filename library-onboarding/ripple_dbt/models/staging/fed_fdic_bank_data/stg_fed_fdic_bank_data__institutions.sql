{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2d).
  SAMPLE ONLY -- NOT the full dataset. FDIC insured-institution directory: a 10,000-row API slice (cert number unique within it) of the full multi-decade institution universe. Use for shape/testing only; full pull needs an offset-paginated loader.
  Grain: one row = one insured institution (cert unique in the slice).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_FDIC_BANK_DATA') }}
),

renamed as (
    select
        nullif(trim(CERT), '')                                     as cert,
        nullif(trim(NAME), '')                                     as name,
        nullif(trim(CITY), '')                                     as city,
        nullif(trim(STNAME), '')                                   as stname,
        nullif(trim(STALP), '')                                    as stalp,
        nullif(trim(ZIP), '')                                      as zip,
        nullif(trim(FIPS), '')                                     as fips,
        nullif(trim(BKCLASS), '')                                  as bkclass,
        nullif(trim(ACTIVE), '')                                   as active,
        try_to_date(left(nullif(trim(DATEUPDT), ''), 10))          as dateupdt,
        try_to_date(left(nullif(trim(ESTYMD), ''), 10))            as estymd,
        try_to_date(left(nullif(trim(ENDEFYMD), ''), 10))          as endefymd,
        try_to_number(nullif(trim(ASSET), ''), 18, 4)              as asset,
        try_to_number(nullif(trim(DEP), ''), 18, 4)                as dep,
        try_to_number(nullif(trim(DEPDOM), ''), 18, 4)             as depdom,
        try_to_number(nullif(trim(NETINC), ''), 18, 4)             as netinc,
        try_to_date(left(nullif(trim(REPDTE), ''), 10))            as repdte,
        nullif(trim(RSSDID), '')                                   as rssdid,
        nullif(trim(CHRTAGNT), '')                                 as chrtagnt,
        nullif(trim(INSTCAT), '')                                  as instcat,
        nullif(trim(SPECGRP), '')                                  as specgrp,
        nullif(trim(HCTMULT), '')                                  as hctmult,
        try_to_number(nullif(trim(LATITUDE), ''), 18, 4)           as latitude,
        try_to_number(nullif(trim(LONGITUDE), ''), 18, 4)          as longitude,
        to_timestamp_ntz(_INGESTED_AT, 6)                          as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
