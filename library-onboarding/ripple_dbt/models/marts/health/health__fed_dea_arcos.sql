{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per ARCOS transaction line; TRANSACTION_ID is NOT unique, 11.7M ids over 178.6M rows, see traps.md 2026-09-10
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

{% set name_key_open = "upper(regexp_replace(regexp_replace(regexp_replace(" -%}
{% set name_key_close = ", '[[:space:]]+(County|Parish|Borough|Census Area|Municipio|Municipality)$', '', 1, 0, 'i'), '^(St\.?|Saint|Ste\.?|Sainte)[[:space:]]+', 'SAINT ', 1, 0, 'i'), '[^A-Za-z0-9]', ''))" -%}

-- ROW KEY (2026-09-21). DEA ships no per-row id: TRANSACTION_ID repeats about 15 times over and the best
-- 7-column compound still collides 3,841 times. So the key is the row itself: a hash of every business
-- column, plus a counter inside each group of fully identical rows. Identical rows are interchangeable,
-- so which one gets 1 and which gets 2 changes nothing. The two load-audit columns stay out of the hash.
with hashed as (
    select *, hash(* exclude ("_INGESTED_AT", "_SOURCE_RUN_ID")) as _row_hash
    from {{ source('ripple_raw', 'FED_DEA_ARCOS_FULL') }}
),

source as (
    select *, to_varchar(_row_hash) || '-' || row_number() over (partition by _row_hash order by "_INGESTED_AT") as _arcos_row_key
    from hashed
),

county_dim as (
    select
        STATE as state_abbr,
        STATEFP || COUNTYFP as county_fips,
        CLASSFP as classfp,
        COUNTYFP as countyfp,
        {{ name_key_open }}COUNTYNAME{{ name_key_close }} as name_key
    from {{ source('ripple_raw', 'FED_CENSUS_COUNTY_2020') }}
),

-- one Census county per state + name key; real counties beat the odd class codes.
county_one as (
    select state_abbr, name_key, county_fips
    from county_dim
    qualify row_number() over (
        partition by state_abbr, name_key
        order by case when classfp in ('H1', 'H4', 'H5') then 0 else 1 end, countyfp
    ) = 1
),

-- 2026-09-18: the regex key used to run inside both join conditions, twice per row, 178M rows.
-- Now it runs once per distinct raw state + county spelling (3,132 buyer pairs, plus the reporter ones), and the
-- big table joins to this lookup on its own raw columns. Plain equality, one hit at most:
-- raw_pairs is distinct and county_one holds one row per key, so the join cannot add rows.
raw_pairs as (
    select "BUYER_STATE" as raw_state, "BUYER_COUNTY" as raw_county from hashed
    union
    select "REPORTER_STATE", "REPORTER_COUNTY" from hashed
),

county_lookup as (
    select rp.raw_state, rp.raw_county, c.county_fips
    from raw_pairs rp
    join county_one c
        on c.state_abbr = trim(rp.raw_state)
       and c.name_key = {{ name_key_open }}trim(rp.raw_county){{ name_key_close }}
)

select
    trim("TRANSACTION_ID")                           as transaction_id,
    {{ stg_date('trim("TRANSACTION_DATE")', 'MMDDYYYY') }} as transaction_date,
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
    {{ stg_float('"QUANTITY"') }}                        as quantity,
    {{ stg_float('"DOSAGE_UNIT"') }}                     as dosage_units,
    {{ stg_float('"CALC_BASE_WT_IN_GM"') }}              as base_weight_grams,
    {{ stg_float('"MME_CONVERSION_FACTOR"') }}           as mme_conversion_factor,
    {{ stg_float('"DOS_STR"') }}                         as dosage_strength,
    trim("MEASURE")                                  as measure,

    -- Derived: total MME (morphine milligram equivalents)
    {{ stg_float('"DOSAGE_UNIT"') }} * {{ stg_float('"DOS_STR"') }} * {{ stg_float('"MME_CONVERSION_FACTOR"') }} as total_mme,

    -- Corporate
    trim("COMBINED_LABELER_NAME")                    as labeler_name,
    trim("REVISED_COMPANY_NAME")                     as company_name,
    trim("REPORTER_FAMILY")                          as reporter_family,

    "_INGESTED_AT" as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id,
    _arcos_row_key as arcos_row_key
from source
left join county_lookup bd
    on bd.raw_state = "BUYER_STATE" and bd.raw_county = "BUYER_COUNTY"
left join county_lookup rd
    on rd.raw_state = "REPORTER_STATE" and rd.raw_county = "REPORTER_COUNTY"
