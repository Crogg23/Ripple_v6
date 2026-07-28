{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per controlled substance transaction (transaction_id is unique)
-- Answers: Who distributes what controlled substances to whom, where, and how much?
-- Source: DEA ARCOS (Automation of Reports and Consolidated Orders System) — ~178M records
-- Key joins: buyer_county → geography; drug_name/ingredient_name → substance classification;
--   buyer_dea_no → pharmacy/provider entities; reporter_name → manufacturer/distributor entities
-- WARNING: This is 178M rows. Full materialization takes significant compute.

with source as (
    select * from {{ source('ripple_raw', 'FED_DEA_ARCOS_FULL') }}
)

select
    trim("TRANSACTION_ID")                           as transaction_id,
    try_to_date(trim("TRANSACTION_DATE"), 'MMDDYYYY') as transaction_date,
    trim("TRANSACTION_CODE")                         as transaction_code,

    -- Reporter (manufacturer/distributor)
    trim("REPORTER_DEA_NO")                          as reporter_dea_no,
    trim("REPORTER_BUS_ACT")                         as reporter_business_activity,
    trim("REPORTER_NAME")                            as reporter_name,
    trim("REPORTER_CITY")                            as reporter_city,
    trim("REPORTER_STATE")                           as reporter_state,
    trim("REPORTER_ZIP")                             as reporter_zip,
    trim("REPORTER_COUNTY")                          as reporter_county,

    -- Buyer (pharmacy/hospital/practitioner)
    trim("BUYER_DEA_NO")                             as buyer_dea_no,
    trim("BUYER_BUS_ACT")                            as buyer_business_activity,
    trim("BUYER_NAME")                               as buyer_name,
    trim("BUYER_CITY")                               as buyer_city,
    trim("BUYER_STATE")                              as buyer_state,
    trim("BUYER_ZIP")                                as buyer_zip,
    trim("BUYER_COUNTY")                             as buyer_county,

    -- Drug/substance
    trim("DRUG_CODE")                                as drug_code,
    trim("DRUG_NAME")                                as drug_name,
    trim("INGREDIENT_NAME")                          as ingredient_name,
    trim("PRODUCT_NAME")                             as product_name,
    try_to_double("QUANTITY")                        as quantity,
    try_to_double("DOSAGE_UNIT")                     as dosage_units,
    try_to_double("CALC_BASE_WT_IN_GM")              as base_weight_grams,
    try_to_double("MME_CONVERSION_FACTOR")           as mme_conversion_factor,
    try_to_double("DOS_STR")                         as dosage_strength,
    trim("MEASURE")                                  as measure,

    -- Derived: total MME (morphine milligram equivalents)
    try_to_double("DOSAGE_UNIT") * try_to_double("DOS_STR") * try_to_double("MME_CONVERSION_FACTOR") as total_mme,

    -- Corporate
    trim("COMBINED_LABELER_NAME")                    as labeler_name,
    trim("REVISED_COMPANY_NAME")                     as company_name,
    trim("REPORTER_FAMILY")                          as reporter_family,

    "_INGESTED_AT" as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id
from source
