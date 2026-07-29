{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per FDA drug recall (RECALL_NUMBER is unique)
-- Answers: who recalled what drug, why, how serious, and where it was distributed
-- Source: openFDA drug/enforcement API
-- Key: RECALL_NUMBER (STEEL). NDC codes live in the openFDA sub-object.
--
-- BUG FIXED 2026-07-29: this model used to read RAW:recall_number directly off the
-- landing row. The landing table holds ONE row whose RAW is the whole openFDA API
-- envelope -- {"meta": {...}, "results": [ ...17,816 recalls... ]} -- so every
-- top-level key it asked for was null. The mart was a single all-null row and it
-- discarded 100% of the data. It still passed a zero-row check because 1 != 0, and
-- the registry had it marked STEEL-tier connectable on a key that was always null.
-- The fix is to FLATTEN RAW:results, which is where the records actually are.

with recalls as (

    select f.value as rec
    from {{ source('ripple_raw', 'FED_FDA_DRUG_ENFORCEMENT') }} t,
         lateral flatten(input => t.RAW:results) f

)

select
    rec:recall_number::string                as recall_number,
    rec:event_id::string                     as event_id,
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

    -- drug identifiers: arrays in the source, joined to a scalar for easy filtering.
    -- OPENFDA is kept whole so nothing is lost to this flattening.
    array_to_string(rec:openfda:product_ndc, ', ')                   as product_ndc_list,
    array_to_string(rec:openfda:brand_name, ', ')                    as brand_name_list,
    array_to_string(rec:openfda:generic_name, ', ')                  as generic_name_list,
    array_to_string(rec:openfda:manufacturer_name, ', ')             as manufacturer_name_list,
    array_to_string(rec:openfda:application_number, ', ')            as application_number_list,
    rec:openfda                                                      as openfda

from recalls
where rec:recall_number is not null
