{{ config(materialized='view') }}

-- GRAIN: one row per device-level MAUDE record. mdr_report_key (event) can carry
-- MULTIPLE device sub-records (device is an array), so the natural key is
-- (mdr_report_key, device_sequence_number). Scope: 2020Q1-forward (see
-- scripts/sprint_fda_device_specs.py) -- 184 of 362 quarterly parts, a bounded
-- slice of openFDA's full 1993-2026 / 25.3M-record history.
-- Source: openFDA device/event bulk JSON, split-loaded into ~2,000-record VARIANT
-- chunks (grain of the chunk is the top-level EVENT, one event can list several
-- devices -- unnest device here).

with events as (

    select
        f.value                                                          as ev,
        t._ingested_at                                                   as _ingested_at,
        t._source_run_id                                                 as _source_run_id
    from {{ source('ripple_raw', 'FED_FDA_MAUDE') }} t,
         lateral flatten(input => t.RAW:results) f

),

devices as (

    select
        ev:mdr_report_key::string                                        as mdr_report_key,
        ev:report_number::string                                         as report_number,
        ev:event_key::string                                             as event_key,
        ev:event_type::string                                            as event_type,
        ev:date_received::string                                         as date_received_raw,
        ev:date_of_event::string                                         as date_of_event_raw,
        ev:date_report::string                                           as date_report_raw,
        ev:adverse_event_flag::string                                    as adverse_event_flag,
        ev:product_problem_flag::string                                  as product_problem_flag,
        ev:manufacturer_name::string                                     as manufacturer_name,
        ev:manufacturer_city::string                                     as manufacturer_city,
        ev:manufacturer_state::string                                    as manufacturer_state,
        ev:manufacturer_country::string                                  as manufacturer_country,
        dev.value:device_sequence_number::string                         as device_sequence_number,
        dev.value:brand_name::string                                     as brand_name,
        dev.value:generic_name::string                                   as generic_name,
        dev.value:manufacturer_d_name::string                            as manufacturer_d_name,
        dev.value:model_number::string                                   as model_number,
        dev.value:catalog_number::string                                 as catalog_number,
        dev.value:lot_number::string                                     as lot_number,
        dev.value:device_report_product_code::string                    as device_report_product_code,
        dev.value:baseline_510_k__number::string                        as baseline_510k_number,
        dev.value:udi_di::string                                        as udi_di,
        dev.value:udi_public::string                                    as udi_public,
        dev.value:openfda                                               as device_openfda,
        _ingested_at,
        _source_run_id
    from events,
         lateral flatten(input => ev:device, outer => true) dev

),

deduped as (

    select *,
        try_to_date(date_received_raw, 'YYYYMMDD')  as date_received,
        try_to_date(date_of_event_raw, 'YYYYMMDD')  as date_of_event,
        try_to_date(date_report_raw, 'YYYYMMDD')    as date_report,
        row_number() over (
            partition by mdr_report_key, coalesce(device_sequence_number, '0')
            order by _ingested_at desc
        ) as _row_num
    from devices
    where mdr_report_key is not null

)

select
    mdr_report_key,
    report_number,
    event_key,
    device_sequence_number,
    event_type,
    date_received,
    date_of_event,
    date_report,
    adverse_event_flag,
    product_problem_flag,
    manufacturer_name,
    manufacturer_city,
    manufacturer_state,
    manufacturer_country,
    brand_name,
    generic_name,
    manufacturer_d_name,
    model_number,
    catalog_number,
    lot_number,
    device_report_product_code,
    baseline_510k_number,
    udi_di,
    udi_public,
    device_openfda,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
