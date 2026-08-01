{{ config(materialized='view', tags=['spine_generated']) }}

-- GRAIN: one row per (committee, reporting-cycle coverage period). Fixed 2026-07-31:
-- the "CMTE_ID is unique" claim was false -- this file spans MULTIPLE election
-- cycles (cvg_end_dt of 2018, 2020, 2022, 2024 all appear for the same committee),
-- and deduping on cmte_id alone kept only the most-recently-loaded cycle, silently
-- discarding a committee's entire finance history from every earlier cycle. Found
-- via tests/test_mart_duplication.py: this mart (22,899 rows) disagreed with an
-- auto-generated raw duplicate (48,395 rows) that happened to expose the loss.
--
-- cvg_end_dt now joins the key. Verified live: the handful of residual (cmte_id,
-- cvg_end_dt) collisions are rows where BOTH the date AND every financial column are
-- blank -- fully degenerate rows with nothing to lose by collapsing. Real cycle data
-- is never dropped.
-- SPINE_ENTITY: organization
-- Source: FEC PAC and Party Summary — ~48K committee-cycle records
-- Key joins: cmte_id → FEC committee linkage tables; spine_entity_id → ENTITY_GOLDEN

with source as (
    select * from {{ source('ripple_raw', 'FED_FEC_PAC_SUMMARY') }}
),

renamed as (
    select
        trim(C1)                          as cmte_id,
        trim(C2)                          as cmte_nm,
        trim(C3)                          as cmte_tp,
        trim(C4)                          as cmte_dsgn,
        trim(C5)                          as cmte_filing_freq,
        try_to_double(C6)                 as ttl_receipts,
        try_to_double(C7)                 as trans_from_aff,
        try_to_double(C8)                 as indv_contrib,
        try_to_double(C9)                 as other_pol_cmte_contrib,
        try_to_double(C10)                as cand_contrib,
        try_to_double(C11)                as cand_loans,
        try_to_double(C12)                as ttl_loans_received,
        try_to_double(C13)                as ttl_disb,
        try_to_double(C14)                as tranf_to_aff,
        try_to_double(C15)                as indv_refunds,
        try_to_double(C16)                as other_pol_cmte_refunds,
        try_to_double(C17)                as cand_loan_repay,
        try_to_double(C18)                as loan_repay,
        try_to_double(C19)                as coh_bop,
        try_to_double(C20)                as coh_cop,
        try_to_double(C21)                as debts_owed_by,
        try_to_double(C22)                as nonfed_trans_received,
        try_to_double(C23)                as contrib_to_other_cmte,
        try_to_double(C24)                as ind_exp,
        try_to_double(C25)                as pty_coord_exp,
        try_to_double(C26)                as nonfed_share_exp,
        try_to_date(trim(C27), 'MM/DD/YYYY') as cvg_end_dt,
        "_INGESTED_AT"                    as _loaded_at,
        "_SOURCE_RUN_ID"                  as _source_run_id
    from source
)

select * from renamed
qualify row_number() over (
    partition by cmte_id, cvg_end_dt
    order by _loaded_at desc
) = 1
