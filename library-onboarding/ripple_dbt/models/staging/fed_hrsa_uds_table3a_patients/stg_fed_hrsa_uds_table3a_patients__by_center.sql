{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2c) from live-verified specs.
  HRSA UDS Table 3A: federally-funded health center patient counts by age/sex line (bhcmisid unique). Column pairs are (male, female) per age line.
  Grain: one row = one health center's Table 3A.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_HRSA_UDS_TABLE3A_PATIENTS') }}
    -- One landed row is an embedded HEADER row (blank center id, cell values
    -- are the column labels like 'Under age 1-Male Patients (a)') -- excluded.
    where nullif(trim(BHCMISID), '') is not null
),

renamed as (
    select
        nullif(trim(BHCMISID), '')                                 as bhcmisid,
        nullif(trim(GRANTNUMBER), '')                              as grantnumber,
        nullif(trim(T3A_L1_CA), '')                                as t3a_l1_ca,
        nullif(trim(T3A_L1_CB), '')                                as t3a_l1_cb,
        nullif(trim(T3A_L2_CA), '')                                as t3a_l2_ca,
        nullif(trim(T3A_L2_CB), '')                                as t3a_l2_cb,
        nullif(trim(T3A_L3_CA), '')                                as t3a_l3_ca,
        nullif(trim(T3A_L3_CB), '')                                as t3a_l3_cb,
        nullif(trim(T3A_L4_CA), '')                                as t3a_l4_ca,
        nullif(trim(T3A_L4_CB), '')                                as t3a_l4_cb,
        nullif(trim(T3A_L5_CA), '')                                as t3a_l5_ca,
        nullif(trim(T3A_L5_CB), '')                                as t3a_l5_cb,
        nullif(trim(T3A_L6_CA), '')                                as t3a_l6_ca,
        nullif(trim(T3A_L6_CB), '')                                as t3a_l6_cb,
        nullif(trim(T3A_L7_CA), '')                                as t3a_l7_ca,
        nullif(trim(T3A_L7_CB), '')                                as t3a_l7_cb,
        nullif(trim(T3A_L8_CA), '')                                as t3a_l8_ca,
        nullif(trim(T3A_L8_CB), '')                                as t3a_l8_cb,
        nullif(trim(T3A_L9_CA), '')                                as t3a_l9_ca,
        nullif(trim(T3A_L9_CB), '')                                as t3a_l9_cb,
        nullif(trim(T3A_L10_CA), '')                               as t3a_l10_ca,
        nullif(trim(T3A_L10_CB), '')                               as t3a_l10_cb,
        nullif(trim(T3A_L11_CA), '')                               as t3a_l11_ca,
        nullif(trim(T3A_L11_CB), '')                               as t3a_l11_cb,
        nullif(trim(T3A_L12_CA), '')                               as t3a_l12_ca,
        nullif(trim(T3A_L12_CB), '')                               as t3a_l12_cb,
        nullif(trim(T3A_L13_CA), '')                               as t3a_l13_ca,
        nullif(trim(T3A_L13_CB), '')                               as t3a_l13_cb,
        nullif(trim(T3A_L14_CA), '')                               as t3a_l14_ca,
        nullif(trim(T3A_L14_CB), '')                               as t3a_l14_cb,
        nullif(trim(T3A_L15_CA), '')                               as t3a_l15_ca,
        nullif(trim(T3A_L15_CB), '')                               as t3a_l15_cb,
        nullif(trim(T3A_L16_CA), '')                               as t3a_l16_ca,
        nullif(trim(T3A_L16_CB), '')                               as t3a_l16_cb,
        nullif(trim(T3A_L17_CA), '')                               as t3a_l17_ca,
        nullif(trim(T3A_L17_CB), '')                               as t3a_l17_cb,
        nullif(trim(T3A_L18_CA), '')                               as t3a_l18_ca,
        nullif(trim(T3A_L18_CB), '')                               as t3a_l18_cb,
        nullif(trim(T3A_L19_CA), '')                               as t3a_l19_ca,
        nullif(trim(T3A_L19_CB), '')                               as t3a_l19_cb,
        nullif(trim(T3A_L20_CA), '')                               as t3a_l20_ca,
        nullif(trim(T3A_L20_CB), '')                               as t3a_l20_cb,
        nullif(trim(T3A_L21_CA), '')                               as t3a_l21_ca,
        nullif(trim(T3A_L21_CB), '')                               as t3a_l21_cb,
        nullif(trim(T3A_L22_CA), '')                               as t3a_l22_ca,
        nullif(trim(T3A_L22_CB), '')                               as t3a_l22_cb,
        nullif(trim(T3A_L23_CA), '')                               as t3a_l23_ca,
        nullif(trim(T3A_L23_CB), '')                               as t3a_l23_cb,
        nullif(trim(T3A_L24_CA), '')                               as t3a_l24_ca,
        nullif(trim(T3A_L24_CB), '')                               as t3a_l24_cb,
        nullif(trim(T3A_L25_CA), '')                               as t3a_l25_ca,
        nullif(trim(T3A_L25_CB), '')                               as t3a_l25_cb,
        nullif(trim(T3A_L26_CA), '')                               as t3a_l26_ca,
        nullif(trim(T3A_L26_CB), '')                               as t3a_l26_cb,
        nullif(trim(T3A_L27_CA), '')                               as t3a_l27_ca,
        nullif(trim(T3A_L27_CB), '')                               as t3a_l27_cb,
        nullif(trim(T3A_L28_CA), '')                               as t3a_l28_ca,
        nullif(trim(T3A_L28_CB), '')                               as t3a_l28_cb,
        nullif(trim(T3A_L29_CA), '')                               as t3a_l29_ca,
        nullif(trim(T3A_L29_CB), '')                               as t3a_l29_cb,
        nullif(trim(T3A_L30_CA), '')                               as t3a_l30_ca,
        nullif(trim(T3A_L30_CB), '')                               as t3a_l30_cb,
        nullif(trim(T3A_L31_CA), '')                               as t3a_l31_ca,
        nullif(trim(T3A_L31_CB), '')                               as t3a_l31_cb,
        nullif(trim(T3A_L32_CA), '')                               as t3a_l32_ca,
        nullif(trim(T3A_L32_CB), '')                               as t3a_l32_cb,
        nullif(trim(T3A_L33_CA), '')                               as t3a_l33_ca,
        nullif(trim(T3A_L33_CB), '')                               as t3a_l33_cb,
        nullif(trim(T3A_L34_CA), '')                               as t3a_l34_ca,
        nullif(trim(T3A_L34_CB), '')                               as t3a_l34_cb,
        nullif(trim(T3A_L35_CA), '')                               as t3a_l35_ca,
        nullif(trim(T3A_L35_CB), '')                               as t3a_l35_cb,
        nullif(trim(T3A_L36_CA), '')                               as t3a_l36_ca,
        nullif(trim(T3A_L36_CB), '')                               as t3a_l36_cb,
        nullif(trim(T3A_L37_CA), '')                               as t3a_l37_ca,
        nullif(trim(T3A_L37_CB), '')                               as t3a_l37_cb,
        nullif(trim(T3A_L38_CA), '')                               as t3a_l38_ca,
        nullif(trim(T3A_L38_CB), '')                               as t3a_l38_cb,
        nullif(trim(T3A_L39_CA), '')                               as t3a_l39_ca,
        nullif(trim(T3A_L39_CB), '')                               as t3a_l39_cb,
        to_timestamp_ntz(_INGESTED_AT, 6)                          as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
