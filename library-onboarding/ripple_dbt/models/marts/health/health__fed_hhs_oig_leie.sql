{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per exclusion record (exclusion_sk is unique)
-- Answers: Which healthcare providers/entities have been excluded from federal programs?
-- Source: HHS OIG List of Excluded Individuals/Entities (LEIE)
-- Key joins: npi â†’ CMS NPPES provider; business_name â†’ entity resolution

select
    exclusion_sk,
    trim(last_name)                                as last_name,
    trim(first_name)                               as first_name,
    trim(middle_name)                              as middle_name,
    trim(business_name)                            as business_name,
    trim(general_category)                         as general_category,
    trim(specialty)                                as specialty,
    trim(npi)                                      as npi,
    trim(upin)                                     as upin,
    trim(exclusion_type)                           as exclusion_type,
    -- TYPED 2026-08-22: values are YYYYMMDD (sampled live); explicit format,
    -- range-guarded like every typing-layer date
    case when try_to_date(nullif(trim(exclusion_date_raw), ''), 'YYYYMMDD')
              between '1800-01-01' and '2100-01-01'
         then try_to_date(nullif(trim(exclusion_date_raw), ''), 'YYYYMMDD') end
                                                   as exclusion_date,
    trim(reinstatement_date)                       as reinstatement_date,
    trim(address)                                  as address,
    trim(city)                                     as city,
    trim(state)                                    as state,
    trim(zip)                                      as zip,
    npi_is_real,
    has_waiver,
    (reinstatement_date is not null
     and trim(reinstatement_date) != '') as was_reinstated,
    (business_name is not null
     and trim(business_name) != '') as is_entity_not_individual,
    _ingested_at,
    _source_run_id
from {{ ref('stg_fed_hhs_oig_leie__exclusions') }}
