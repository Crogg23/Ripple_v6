{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per organization (EIN is unique)
-- Answers: Which tax-exempt orgs lost their status, when, and were they reinstated?
-- Source: IRS Automatic Revocation List (~1.2M revoked orgs)
-- Key joins: spine_entity_id â†’ ENTITY_GOLDEN; ein â†’ IRS 990/BMF

select
    ein,
    trim(legal_name)                               as legal_name,
    trim(dba_name)                                 as dba_name,
    trim(org_address)                              as address,
    trim(city)                                     as city,
    trim(state)                                    as state,
    trim(zip_code)                                 as zip_code,
    trim(country)                                  as country,
    trim(exemption_type)                           as exemption_type,
    trim(revocation_date)                          as revocation_date,
    trim(revocation_posting_date)                  as revocation_posting_date,
    trim(exemption_reinstatement_date)             as reinstatement_date,
    (exemption_reinstatement_date is not null
     and trim(exemption_reinstatement_date) != '') as was_reinstated,
    spine_entity_id,
    _loaded_at,
    _source_url
from {{ ref('stg_fed_irs_revocation__organizations') }}
