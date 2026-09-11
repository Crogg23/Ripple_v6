{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per controlled substance transaction (transaction_id is unique)
-- Answers: Who distributes what controlled substances to whom, where, and how much?
-- Source: DEA ARCOS (Automation of Reports and Consolidated Orders System) â€” ~178M records
-- Key joins: buyer_county â†’ geography; drug_name/ingredient_name â†’ substance classification;
--   buyer_dea_no â†’ pharmacy/provider entities; reporter_name â†’ manufacturer/distributor entities
-- WARNING: This is 178M rows. Full materialization takes significant compute.

-- 2026-09-10: BUYER_COUNTY_FIPS and REPORTER_COUNTY_FIPS added from the Census 2020 county list.
-- ARCOS spells SAINT out and drops the legal suffix; the key folds St./Saint and strips County/Parish.
-- Measured before the change on the 3,132 distinct buyer state+county pairs: 3,089 matched,
-- 178,338,557 of 178,598,026 rows. Misses are Virginia independent cities without 'city',
-- Dona Ana without the tilde, Juneau, and Puerto Rico municipios.

with source as (
    select * from {{ source('ripple_raw', 'FED_DEA_ARCOS_FULL') }}
),

county_dim as (
    select
        STATE as state_abbr,
        STATEFP || COUNTYFP as county_fips,
        upper(regexp_replace(regexp_replace(regexp_replace(COUNTYNAME,
            '[[:space:]]+(County|Parish|Borough|Census Area|Municipio|Municipality)$', '', 1, 0, 'i'),
            '^(St\.?|Saint)[[:space:]]+', 'SAINT ', 1, 0, 'i'),
            '[^A-Za-z0-9]', '')) as name_key,
        row_number() over (
            partition by STATE, upper(regexp_replace(regexp_replace(regexp_replace(COUNTYNAME,
            '[[:space:]]+(County|Parish|Borough|Census Area|Municipio|Municipality)$', '', 1, 0, 'i'),
            '^(St\.?|Saint)[[:space:]]+', 'SAINT ', 1, 0, 'i'),
            '[^A-Za-z0-9]', ''))
            order by case when CLASSFP in ('H1', 'H4', 'H5') then 0 else 1 end, COUNTYFP
        ) as rn
    from {{ source('ripple_raw', 'FED_CENSUS_COUNTY_2020') }}
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
    rd.county_fips                                   as reporter_county_fips,

    -- Buyer (pharmacy/hospital/practitioner)
    trim("BUYER_DEA_NO")                             as buyer_dea_no,
    trim("BUYER_BUS_ACT")                            as buyer_business_activity,
    trim("BUYER_NAME")                               as buyer_name,
    trim("BUYER_CITY")                               as buyer_city,
    trim("BUYER_STATE")                              as buyer_state,
    trim("BUYER_ZIP")                                as buyer_zip,
    trim("BUYER_COUNTY")                             as buyer_county,
    bd.county_fips                                   as buyer_county_fips,

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
left join county_dim bd
    on bd.rn = 1 and bd.state_abbr = trim("BUYER_STATE")
   and bd.name_key = upper(regexp_replace(regexp_replace(regexp_replace(trim("BUYER_COUNTY"),
            '[[:space:]]+(County|Parish|Borough|Census Area|Municipio|Municipality)$', '', 1, 0, 'i'),
            '^(St\.?|Saint)[[:space:]]+', 'SAINT ', 1, 0, 'i'),
            '[^A-Za-z0-9]', ''))
left join county_dim rd
    on rd.rn = 1 and rd.state_abbr = trim("REPORTER_STATE")
   and rd.name_key = upper(regexp_replace(regexp_replace(regexp_replace(trim("REPORTER_COUNTY"),
            '[[:space:]]+(County|Parish|Borough|Census Area|Municipio|Municipality)$', '', 1, 0, 'i'),
            '^(St\.?|Saint)[[:space:]]+', 'SAINT ', 1, 0, 'i'),
            '[^A-Za-z0-9]', ''))
