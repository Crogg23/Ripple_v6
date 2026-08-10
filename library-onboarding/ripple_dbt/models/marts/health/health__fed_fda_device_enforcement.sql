{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per FDA device recall (RECALL_NUMBER is unique -- verified live)
-- Answers: who recalled what device, why, how serious, and where it was distributed
-- Source: openFDA device/enforcement API
-- Key: RECALL_NUMBER. PRODUCT_CODE joins to health__fed_fda_device_classification.
--
-- The landing table holds 20 VARIANT chunk rows whose RAW is a whole openFDA API
-- envelope -- {"meta": {...}, "results": [ ... ]} -- 39,635 recall records in
-- total -- so the records must be FLATTENed out of RAW:results (same shape and
-- fix as health__fed_fda_drug_enforcement).

with recalls as (

    select f.value as rec
    from {{ source('ripple_raw', 'FED_FDA_DEVICE_ENFORCEMENT') }} t,
         lateral flatten(input => t.RAW:results) f

)

select
    rec:recall_number::string                as recall_number,
    rec:event_id::string                     as event_id,
    rec:product_code::string                 as product_code,
    rec:status::string                       as status,
    rec:classification::string               as classification,
    rec:product_type::string                 as product_type,

    rec:recalling_firm::string               as recalling_firm,
    rec:address_1::string                    as address_1,
    rec:address_2::string                    as address_2,
    rec:city::string                         as city,
    rec:state::string                        as state,
    rec:postal_code::string                  as postal_code,
    rec:country::string                      as country,

    rec:product_description::string          as product_description,
    rec:product_quantity::string             as product_quantity,
    rec:reason_for_recall::string            as reason_for_recall,
    rec:code_info::string                    as code_info,
    rec:more_code_info::string               as more_code_info,
    rec:distribution_pattern::string         as distribution_pattern,
    rec:voluntary_mandated::string           as voluntary_mandated,
    rec:initial_firm_notification::string    as initial_firm_notification,

    -- openFDA dates arrive as YYYYMMDD strings
    try_to_date(rec:recall_initiation_date::string, 'YYYYMMDD')      as recall_initiation_date,
    try_to_date(rec:center_classification_date::string, 'YYYYMMDD')  as center_classification_date,
    try_to_date(rec:report_date::string, 'YYYYMMDD')                 as report_date,
    try_to_date(rec:termination_date::string, 'YYYYMMDD')            as termination_date,

    -- device identifiers: arrays in the source, joined to a scalar for easy
    -- filtering. OPENFDA is kept whole so nothing is lost to this flattening.
    array_to_string(rec:openfda:registration_number, ', ')           as registration_number_list,
    array_to_string(rec:openfda:k_number, ', ')                      as k_number_list,
    array_to_string(rec:openfda:fei_number, ', ')                    as fei_number_list,
    rec:openfda                                                      as openfda

from recalls
where rec:recall_number is not null
