{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per independent expenditure transaction

with source as (
    select * from {{ source('ripple_raw', 'FED_FEC_INDEPENDENT_EXPENDITURES') }}
)

select
    "cand_id" as CAND_ID,
    "cand_name" as CAND_NAME,
    "spe_id" as SPE_ID,
    "spe_nam" as SPE_NAM,
    "ele_type" as ELE_TYPE,
    "can_office_state" as CAN_OFFICE_STATE,
    "can_office_dis" as CAN_OFFICE_DIS,
    "can_office" as CAN_OFFICE,
    "cand_pty_aff" as CAND_PTY_AFF,
    "exp_amo" as EXP_AMO,
    "exp_date" as EXP_DATE,
    "agg_amo" as AGG_AMO,
    "sup_opp" as SUP_OPP,
    "pur" as PUR,
    "pay" as PAY,
    "file_num" as FILE_NUM,
    "amndt_ind" as AMNDT_IND,
    "tran_id" as TRAN_ID,
    "image_num" as IMAGE_NUM,
    "receipt_dat" as RECEIPT_DAT,
    "fec_election_yr" as FEC_ELECTION_YR,
    "prev_file_num" as PREV_FILE_NUM,
    "dissem_dt" as DISSEM_DT
from source
