{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_nara_wra_aad__japanese_american_relocation_records') }}

)

select

    -- surrogate / natural key
    record_id,
    series_id,

    -- cross-source join keys
    person_name,
    record_date,
    raw_date,
    camp_location,
    fips,
    geo,

    -- person attributes
    age,
    sex,
    citizenship_status,
    family_number,

    -- supplemental
    notes_field,

    -- source lineage
    'fed_nara_wra_aad'                         as source_id,
    'japanese_american_relocation_records'      as entity_type,
    _ingested_at,
    _source_run_id

from base
