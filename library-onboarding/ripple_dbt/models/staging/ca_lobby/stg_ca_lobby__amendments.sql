{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2b) from live-verified specs.
  CAL-ACCESS lobbying registration amendments (Form 605): one row per amendment filing version (filing_id + amend_id unique).
  Grain: one row = one amendment filing version.
*/

with source as (
    select * from {{ source('ripple_raw', 'CA_LOBBY_AMENDMENTS') }}
),

renamed as (
    select
        nullif(trim(FILING_ID), '')                                    as filing_id,
        nullif(trim(AMEND_ID), '')                                     as amend_id,
        nullif(trim(REC_TYPE), '')                                     as rec_type,
        nullif(trim(FORM_TYPE), '')                                    as form_type,
        try_to_date(split_part(nullif(trim(EXEC_DATE), ''), ' ', 1), 'MM/DD/YYYY') as exec_date,
        try_to_date(split_part(nullif(trim(FROM_DATE), ''), ' ', 1), 'MM/DD/YYYY') as from_date,
        try_to_date(split_part(nullif(trim(THRU_DATE), ''), ' ', 1), 'MM/DD/YYYY') as thru_date,
        nullif(trim(ADD_L_CB), '')                                     as add_l_cb,
        try_to_date(split_part(nullif(trim(ADD_L_EFF), ''), ' ', 1), 'MM/DD/YYYY') as add_l_eff,
        nullif(trim(A_L_NAML), '')                                     as a_l_naml,
        nullif(trim(A_L_NAMF), '')                                     as a_l_namf,
        nullif(trim(A_L_NAMT), '')                                     as a_l_namt,
        nullif(trim(A_L_NAMS), '')                                     as a_l_nams,
        nullif(trim(DEL_L_CB), '')                                     as del_l_cb,
        try_to_date(split_part(nullif(trim(DEL_L_EFF), ''), ' ', 1), 'MM/DD/YYYY') as del_l_eff,
        nullif(trim(D_L_NAML), '')                                     as d_l_naml,
        nullif(trim(D_L_NAMF), '')                                     as d_l_namf,
        nullif(trim(D_L_NAMT), '')                                     as d_l_namt,
        nullif(trim(D_L_NAMS), '')                                     as d_l_nams,
        nullif(trim(ADD_LE_CB), '')                                    as add_le_cb,
        try_to_date(split_part(nullif(trim(ADD_LE_EFF), ''), ' ', 1), 'MM/DD/YYYY') as add_le_eff,
        nullif(trim(A_LE_NAML), '')                                    as a_le_naml,
        nullif(trim(A_LE_NAMF), '')                                    as a_le_namf,
        nullif(trim(A_LE_NAMT), '')                                    as a_le_namt,
        nullif(trim(A_LE_NAMS), '')                                    as a_le_nams,
        nullif(trim(DEL_LE_CB), '')                                    as del_le_cb,
        try_to_date(split_part(nullif(trim(DEL_LE_EFF), ''), ' ', 1), 'MM/DD/YYYY') as del_le_eff,
        nullif(trim(D_LE_NAML), '')                                    as d_le_naml,
        nullif(trim(D_LE_NAMF), '')                                    as d_le_namf,
        nullif(trim(D_LE_NAMT), '')                                    as d_le_namt,
        nullif(trim(D_LE_NAMS), '')                                    as d_le_nams,
        nullif(trim(ADD_LF_CB), '')                                    as add_lf_cb,
        try_to_date(split_part(nullif(trim(ADD_LF_EFF), ''), ' ', 1), 'MM/DD/YYYY') as add_lf_eff,
        nullif(trim(A_LF_NAME), '')                                    as a_lf_name,
        nullif(trim(DEL_LF_CB), '')                                    as del_lf_cb,
        try_to_date(split_part(nullif(trim(DEL_LF_EFF), ''), ' ', 1), 'MM/DD/YYYY') as del_lf_eff,
        nullif(trim(D_LF_NAME), '')                                    as d_lf_name,
        nullif(trim(OTHER_CB), '')                                     as other_cb,
        try_to_date(split_part(nullif(trim(OTHER_EFF), ''), ' ', 1), 'MM/DD/YYYY') as other_eff,
        nullif(trim(OTHER_DESC), '')                                   as other_desc,
        nullif(trim(F606_YES), '')                                     as f606_yes,
        nullif(trim(F606_NO), '')                                      as f606_no,
        to_timestamp_ntz(INGESTED_AT, 6)                               as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                                as _source_run_id
    from source
)

select * from renamed
