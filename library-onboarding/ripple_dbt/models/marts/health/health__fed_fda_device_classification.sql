{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per FDA device product code (PRODUCT_CODE is unique -- verified live)
-- Answers: what device categories exist, how risky FDA rates them, and which
--          specialty/review panel owns them
-- Source: openFDA device/classification API
-- Key: PRODUCT_CODE. openFDA enrichment (registration/k/pma numbers) lives in
--      the openfda sub-object, joined to scalar lists here.
--
-- The landing table holds VARIANT rows whose RAW is the whole openFDA API
-- envelope -- {"meta": {...}, "results": [ ...7,085 classifications... ]} --
-- so the records must be FLATTENed out of RAW:results (same shape and fix as
-- health__fed_fda_drug_enforcement).

with classifications as (

    select f.value as rec
    from {{ source('ripple_raw', 'FED_FDA_DEVICE_CLASSIFICATION') }} t,
         lateral flatten(input => t.RAW:results) f

)

select
    rec:product_code::string                 as product_code,
    rec:device_name::string                  as device_name,
    rec:device_class::string                 as device_class,
    rec:regulation_number::string            as regulation_number,

    rec:medical_specialty::string            as medical_specialty,
    rec:medical_specialty_description::string as medical_specialty_description,
    rec:review_panel::string                 as review_panel,
    rec:submission_type_id::string           as submission_type_id,
    rec:unclassified_reason::string          as unclassified_reason,
    rec:definition::string                   as definition,

    rec:gmp_exempt_flag::string              as gmp_exempt_flag,
    rec:implant_flag::string                 as implant_flag,
    rec:life_sustain_support_flag::string    as life_sustain_support_flag,
    rec:third_party_flag::string             as third_party_flag,

    -- device identifiers: arrays in the source, joined to a scalar for easy
    -- filtering. OPENFDA is kept whole so nothing is lost to this flattening.
    array_to_string(rec:openfda:registration_number, ', ')   as registration_number_list,
    array_to_string(rec:openfda:k_number, ', ')              as k_number_list,
    array_to_string(rec:openfda:pma_number, ', ')            as pma_number_list,
    array_to_string(rec:openfda:fei_number, ', ')            as fei_number_list,
    rec:openfda                                              as openfda

from classifications
where rec:product_code is not null
