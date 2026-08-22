{{ config(materialized='table', schema='JUSTICE') }}

-- GRAIN: one row per sanctioned entity (ent_num is unique)
-- Answers: Who is on the US sanctions list, and for what programs?
-- Source: OFAC Specially Designated Nationals (~12K entities)
-- Key joins: imo_number â†’ int_sanctioned_vessels; entity â†’ spine

select
    {{ ripple_num('ent_num') }} as ent_num,
    sdn_name,
    sdn_type,
    entity_kind,
    program,
    title,
    call_sign,
    vessel_type,
    tonnage,
    gross_registered_tonnage,
    vessel_flag,
    vessel_owner,
    imo_number,
    remarks,
    (entity_kind = 'vessel') as is_vessel,
    (entity_kind = 'individual') as is_individual,
    _ingested_at,
    _source_run_id
from {{ ref('stg_fed_ofac_sdn__sdn_entities') }}
