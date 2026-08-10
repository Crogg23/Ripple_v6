{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  CAL-ACCESS firm-employer billing lines: one row per firm-filing-employer-period (unique with employer name + period start).
  Grain: one row = one firm-filing-employer-period.
*/

with source as (
    select * from {{ source('ripple_raw', 'CA_LOBBY_FIRM_EMPLOYER') }}
),

renamed as (
    select
        nullif(trim(FIRM_ID), '')                                      as firm_id,
        nullif(trim(FILING_ID), '')                                    as filing_id,
        nullif(trim(FILING_SEQUENCE), '')                              as filing_sequence,
        nullif(trim(FIRM_NAME), '')                                    as firm_name,
        nullif(trim(EMPLOYER_NAME), '')                                as employer_name,
        try_to_date(split_part(nullif(trim(RPT_START), ''), ' ', 1), 'MM/DD/YYYY') as rpt_start,
        try_to_date(split_part(nullif(trim(RPT_END), ''), ' ', 1), 'MM/DD/YYYY') as rpt_end,
        try_to_number(nullif(trim(PER_TOTAL), ''), 18, 2)              as per_total,
        try_to_number(nullif(trim(CUM_TOTAL), ''), 18, 2)              as cum_total,
        nullif(trim(LBY_ACTVTY), '')                                   as lby_actvty,
        nullif(trim(EXT_LBY_ACTVTY), '')                               as ext_lby_actvty,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
