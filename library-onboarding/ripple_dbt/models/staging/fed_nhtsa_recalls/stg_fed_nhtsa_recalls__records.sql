{{ config(materialized='view', tags=['spine_generated']) }}

-- GRAIN: one row per recall-record (record_id is unique)
-- SPINE_ENTITY: not determined (recall campaigns, not a single entity)
-- Source: NHTSA ODI Recalls — ~243K recall records
-- Key joins: campno → links to investigations/complaints; mfr_name → manufacturer entities

with source as (
    select * from {{ source('ripple_raw', 'FED_NHTSA_RECALLS') }}
),

renamed as (
    select
        trim(C1)                               as record_id,
        trim(C2)                               as campno,
        trim(C3)                               as maketxt,
        trim(C4)                               as modeltxt,
        trim(C5)                               as yeartxt,
        trim(C6)                               as mfgcampno,
        trim(C7)                               as compname,
        trim(C8)                               as mfg_name,
        try_to_date(trim(C9), 'YYYYMMDD')      as bgman,
        try_to_date(trim(C10), 'YYYYMMDD')     as endman,
        trim(C11)                              as rcl_type_cd,
        try_to_number(C12)                     as potaff,
        try_to_date(trim(C13), 'YYYYMMDD')     as odate,
        trim(C14)                              as influenced_by,
        trim(C15)                              as mfgtxt,
        try_to_date(trim(C16), 'YYYYMMDD')     as rcdate,
        try_to_date(trim(C17), 'YYYYMMDD')     as datea,
        trim(C18)                              as rpno,
        trim(C19)                              as fmvss,
        C20                                    as desc_defect,
        C21                                    as consequence_defect,
        C22                                    as corrective_action,
        C23                                    as notes,
        trim(C24)                              as rcl_cmpt_id,
        trim(C25)                              as mfr_comp_name,
        trim(C26)                              as mfr_comp_desc,
        trim(C27)                              as mfr_comp_ptno,
        trim(C28)                              as recall_report,
        trim(C29)                              as recall_report_yn,
        "_INGESTED_AT"                         as _loaded_at,
        "_SOURCE_RUN_ID"                       as _source_run_id
    from source
)

select * from renamed
qualify row_number() over (
    partition by record_id
    order by _loaded_at desc
) = 1
