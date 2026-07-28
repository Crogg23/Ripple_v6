{{ config(tags=['minimal_staging']) }}

-- GRAIN: one row per violation (event_no + violation_no)
-- Fix: strip embedded quote characters from MSHA pipe-delimited source.

with source as (

    select * from {{ source('ripple_raw', 'FED_MSHA_VIOLATIONS') }}

),

cleaned as (

    select
        {{ strip_quotes('EVENT_NO') }}                  as event_no,
        {{ strip_quotes('INSPECTION_BEGIN_DT') }}       as inspection_begin_dt,
        {{ strip_quotes('INSPECTION_END_DT') }}         as inspection_end_dt,
        {{ strip_quotes('VIOLATION_NO') }}              as violation_no,
        {{ strip_quotes('CONTROLLER_ID') }}             as controller_id,
        {{ strip_quotes('CONTROLLER_NAME') }}           as controller_name,
        {{ strip_quotes('VIOLATOR_ID') }}               as violator_id,
        {{ strip_quotes('VIOLATOR_NAME') }}             as violator_name,
        {{ strip_quotes('VIOLATOR_TYPE_CD') }}          as violator_type_cd,
        {{ strip_quotes('MINE_ID') }}                   as mine_id,
        {{ strip_quotes('MINE_NAME') }}                 as mine_name,
        {{ strip_quotes('MINE_TYPE') }}                 as mine_type,
        {{ strip_quotes('COAL_METAL_IND') }}            as coal_metal_ind,
        {{ strip_quotes('CONTRACTOR_ID') }}             as contractor_id,
        {{ strip_quotes('VIOLATION_ISSUE_DT') }}        as violation_issue_dt,
        {{ strip_quotes('VIOLATION_OCCUR_DT') }}        as violation_occur_dt,
        {{ strip_quotes('CAL_YR') }}                    as cal_yr,
        {{ strip_quotes('CAL_QTR') }}                   as cal_qtr,
        {{ strip_quotes('FISCAL_YR') }}                 as fiscal_yr,
        {{ strip_quotes('FISCAL_QTR') }}                as fiscal_qtr,
        {{ strip_quotes('VIOLATION_ISSUE_TIME') }}      as violation_issue_time,
        {{ strip_quotes('SIG_SUB') }}                   as sig_sub,
        {{ strip_quotes('SECTION_OF_ACT') }}            as section_of_act,
        {{ strip_quotes('PART_SECTION') }}              as part_section,
        {{ strip_quotes('SECTION_OF_ACT_1') }}          as section_of_act_1,
        {{ strip_quotes('SECTION_OF_ACT_2') }}          as section_of_act_2,
        {{ strip_quotes('CIT_ORD_SAFE') }}              as cit_ord_safe,
        {{ strip_quotes('ORIG_TERM_DUE_DT') }}          as orig_term_due_dt,
        {{ strip_quotes('ORIG_TERM_DUE_TIME') }}        as orig_term_due_time,
        {{ strip_quotes('LATEST_TERM_DUE_DT') }}        as latest_term_due_dt,
        {{ strip_quotes('LATEST_TERM_DUE_TIME') }}      as latest_term_due_time,
        {{ strip_quotes('TERMINATION_DT') }}            as termination_dt,
        {{ strip_quotes('TERMINATION_TIME') }}          as termination_time,
        {{ strip_quotes('TERMINATION_TYPE') }}          as termination_type,
        {{ strip_quotes('VACATE_DT') }}                 as vacate_dt,
        {{ strip_quotes('VACATE_TIME') }}               as vacate_time,
        {{ strip_quotes('INITIAL_VIOL_NO') }}           as initial_viol_no,
        {{ strip_quotes('REPLACED_BY_ORDER_NO') }}      as replaced_by_order_no,
        {{ strip_quotes('LIKELIHOOD') }}                as likelihood,
        {{ strip_quotes('INJ_ILLNESS') }}               as inj_illness,
        {{ strip_quotes('NO_AFFECTED') }}               as no_affected,
        {{ strip_quotes('NEGLIGENCE') }}                as negligence,
        {{ strip_quotes('WRITTEN_NOTICE') }}            as written_notice,
        {{ strip_quotes('ENFORCEMENT_AREA') }}          as enforcement_area,
        {{ strip_quotes('SPECIAL_ASSESS') }}            as special_assess,
        {{ strip_quotes('PRIMARY_OR_MILL') }}           as primary_or_mill,
        {{ strip_quotes('RIGHT_TO_CONF_DT') }}          as right_to_conf_dt,
        {{ strip_quotes('ASMT_GENERATED_IND') }}        as asmt_generated_ind,
        {{ strip_quotes('FINAL_ORDER_ISSUE_DT') }}      as final_order_issue_dt,
        {{ strip_quotes('PROPOSED_PENALTY') }}          as proposed_penalty,
        {{ strip_quotes('AMOUNT_DUE') }}                as amount_due,
        {{ strip_quotes('AMOUNT_PAID') }}               as amount_paid,
        {{ strip_quotes('BILL_PRINT_DT') }}             as bill_print_dt,
        {{ strip_quotes('LAST_ACTION_CD') }}            as last_action_cd,
        {{ strip_quotes('LAST_ACTION_DT') }}            as last_action_dt,
        {{ strip_quotes('DOCKET_NO') }}                 as docket_no,
        {{ strip_quotes('DOCKET_STATUS_CD') }}          as docket_status_cd,
        {{ strip_quotes('CONTESTED_IND') }}             as contested_ind,
        {{ strip_quotes('CONTESTED_DT') }}              as contested_dt,
        {{ strip_quotes('VIOLATOR_VIOLATION_CNT') }}    as violator_violation_cnt,
        {{ strip_quotes('VIOLATOR_INSPECTION_DAY_CNT') }} as violator_inspection_day_cnt,
        _INGESTED_AT                                    as _loaded_at,
        'https://arlweb.msha.gov/opengovernmentdata/DataSets/Violations.zip' as _source_url

    from source

)

select * from cleaned
