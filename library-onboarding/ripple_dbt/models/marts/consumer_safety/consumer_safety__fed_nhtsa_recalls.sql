{{ config(materialized='table', schema='CONSUMER_SAFETY') }}

-- GRAIN: one row per recall record (record_id is unique)
-- Answers: What recalls have been issued, by whom, for what defect?
-- Source: NHTSA ODI Recalls (~243K records)
-- Key joins: campno â†’ nhtsa_investigations; mfg_name â†’ manufacturer entities

select
    record_id,
    campno,
    maketxt                              as make,
    modeltxt                             as model,
    {{ ripple_dt('yeartxt') }} as model_year,
    compname                             as component,
    mfg_name,
    mfgcampno                            as mfg_recall_number,
    bgman                                as begin_manufacture_date,
    endman                               as end_manufacture_date,
    rcl_type_cd,
    potaff                               as potentially_affected_units,
    odate                                as notification_date,
    influenced_by,
    desc_defect,
    consequence_defect,
    corrective_action,
    case
        when influenced_by = 'ODI' then 'investigation'
        when influenced_by = 'MFR' then 'manufacturer'
        when influenced_by = 'OVSC' then 'ovsc'
        else 'unknown'
    end as recall_trigger,
    _loaded_at,
    _source_run_id
from {{ ref('stg_fed_nhtsa_recalls__records') }}
