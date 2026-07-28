{{ config(tags=['minimal_staging']) }}

-- GRAIN: one row per accident document (document_no)
-- Fix: strip embedded quote characters from MSHA pipe-delimited source.

with source as (

    select * from {{ source('ripple_raw', 'FED_MSHA_ACCIDENTS') }}

),

cleaned as (

    select
        {{ strip_quotes('MINE_ID') }}                   as mine_id,
        {{ strip_quotes('CONTROLLER_ID') }}             as controller_id,
        {{ strip_quotes('CONTROLLER_NAME') }}           as controller_name,
        {{ strip_quotes('OPERATOR_ID') }}               as operator_id,
        {{ strip_quotes('OPERATOR_NAME') }}             as operator_name,
        {{ strip_quotes('CONTRACTOR_ID') }}             as contractor_id,
        {{ strip_quotes('DOCUMENT_NO') }}               as document_no,
        {{ strip_quotes('SUBUNIT_CD') }}                as subunit_cd,
        {{ strip_quotes('SUBUNIT') }}                   as subunit,
        {{ strip_quotes('ACCIDENT_DT') }}               as accident_dt,
        {{ strip_quotes('CAL_YR') }}                    as cal_yr,
        {{ strip_quotes('CAL_QTR') }}                   as cal_qtr,
        {{ strip_quotes('FISCAL_YR') }}                 as fiscal_yr,
        {{ strip_quotes('FISCAL_QTR') }}                as fiscal_qtr,
        {{ strip_quotes('ACCIDENT_TIME') }}             as accident_time,
        {{ strip_quotes('DEGREE_INJURY_CD') }}          as degree_injury_cd,
        {{ strip_quotes('DEGREE_INJURY') }}             as degree_injury,
        {{ strip_quotes('FIPS_STATE_CD') }}             as fips_state_cd,
        {{ strip_quotes('UG_LOCATION_CD') }}            as ug_location_cd,
        {{ strip_quotes('UG_LOCATION') }}               as ug_location,
        {{ strip_quotes('UG_MINING_METHOD_CD') }}       as ug_mining_method_cd,
        {{ strip_quotes('UG_MINING_METHOD') }}          as ug_mining_method,
        {{ strip_quotes('MINING_EQUIP_CD') }}           as mining_equip_cd,
        {{ strip_quotes('MINING_EQUIP') }}              as mining_equip,
        {{ strip_quotes('EQUIP_MFR_CD') }}              as equip_mfr_cd,
        {{ strip_quotes('EQUIP_MFR_NAME') }}            as equip_mfr_name,
        {{ strip_quotes('EQUIP_MODEL_NO') }}            as equip_model_no,
        {{ strip_quotes('SHIFT_BEGIN_TIME') }}          as shift_begin_time,
        {{ strip_quotes('CLASSIFICATION_CD') }}         as classification_cd,
        {{ strip_quotes('CLASSIFICATION') }}            as classification,
        {{ strip_quotes('ACCIDENT_TYPE_CD') }}          as accident_type_cd,
        {{ strip_quotes('ACCIDENT_TYPE') }}             as accident_type,
        {{ strip_quotes('NO_INJURIES') }}               as no_injuries,
        {{ strip_quotes('TOT_EXPER') }}                 as tot_exper,
        {{ strip_quotes('MINE_EXPER') }}                as mine_exper,
        {{ strip_quotes('JOB_EXPER') }}                 as job_exper,
        {{ strip_quotes('OCCUPATION_CD') }}             as occupation_cd,
        {{ strip_quotes('OCCUPATION') }}                as occupation,
        {{ strip_quotes('ACTIVITY_CD') }}               as activity_cd,
        {{ strip_quotes('ACTIVITY') }}                  as activity,
        {{ strip_quotes('INJURY_SOURCE_CD') }}          as injury_source_cd,
        {{ strip_quotes('INJURY_SOURCE') }}             as injury_source,
        {{ strip_quotes('NATURE_INJURY_CD') }}          as nature_injury_cd,
        {{ strip_quotes('NATURE_INJURY') }}             as nature_injury,
        {{ strip_quotes('INJ_BODY_PART_CD') }}          as inj_body_part_cd,
        {{ strip_quotes('INJ_BODY_PART') }}             as inj_body_part,
        {{ strip_quotes('SCHEDULE_CHARGE') }}           as schedule_charge,
        {{ strip_quotes('DAYS_RESTRICT') }}             as days_restrict,
        {{ strip_quotes('DAYS_LOST') }}                 as days_lost,
        {{ strip_quotes('TRANS_TERM') }}                as trans_term,
        {{ strip_quotes('RETURN_TO_WORK_DT') }}         as return_to_work_dt,
        {{ strip_quotes('IMMED_NOTIFY_CD') }}           as immed_notify_cd,
        {{ strip_quotes('IMMED_NOTIFY') }}              as immed_notify,
        {{ strip_quotes('INVEST_BEGIN_DT') }}           as invest_begin_dt,
        {{ strip_quotes('NARRATIVE') }}                 as narrative,
        {{ strip_quotes('CLOSED_DOC_NO') }}             as closed_doc_no,
        {{ strip_quotes('COAL_METAL_IND') }}            as coal_metal_ind,
        _INGESTED_AT                                    as _loaded_at,
        'https://arlweb.msha.gov/opengovernmentdata/DataSets/Accidents.zip' as _source_url

    from source

)

select * from cleaned
