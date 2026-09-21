{{ config(materialized='table', schema='JUSTICE') }}
-- Fixed 2026-09-21: ID columns were cast to FLOAT by ripple_num, which drops leading zeros and rounds past 15 digits. Now TEXT via stg_id_text (ruling 2026-09-19: an ID stays text).

-- GRAIN: one row per sanctioned entity (ent_num is unique)
-- Answers: Who is on the US sanctions list, and for what programs?
-- Source: OFAC Specially Designated Nationals (~12K entities)
-- Key joins: imo_number â†’ int_sanctioned_vessels; entity â†’ spine

select
    {{ stg_id_text('ent_num') }} as ent_num,
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
