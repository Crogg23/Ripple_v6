{{ config(materialized='table', schema='FINANCE') }}

-- Column names below are bare uppercase. The generated model quoted them
-- lowercase and stopped resolving against landing, which is why this mart
-- sat stale at 261,033 rows and four cycles. Checked 2026-09-06.
--
-- GRAIN: one row per independent expenditure transaction, cycles 2018 to 2026.
--
-- DO NOT SUM EXP_AMO WITHOUT THE TWO FLAGS. Raw is $104B across five cycles and
-- about $92B of that is not real [FLAGGED 2026-09-07: this $104B/$92B pair was
-- built off the old wrong $91.0B suspect figure below and is now inconsistent
-- with it -- $129.53B alone exceeds a $104B raw total, which isn't possible.
-- Nobody has re-summed raw EXP_AMO across all five cycles fresh; don't quote
-- $104B or $92B until someone does]:
--
--   IS_SUSPECT_FILING  35 prank rows, $129.53B (CORRECTED 2026-09-07: this
--                      comment said $91.0B, off by $38.5B/42% low -- the
--                      SELECT below just passes the flag through, nothing
--                      here computes the total; see
--                      QA_HANDOFF_AUDIT_2026-09-06.md). Every one is BOTH
--                      web-filed, so TRAN_ID starts 'WFT', AND over $20M. A
--                      $9.98B row from THE COURT OF DIVINE JUSTICE is the
--                      biggest.
--   IS_SUPERSEDED      an amended filing restates its transactions, so the
--                      original sits here too. Food & Water Action's $114M row
--                      appears nine times.
--
-- Filter both to 'False' and 2024 gives $4.44B against the FEC's published
-- ~$4.4B. The other four cycles are internally consistent and unverified.
--
-- The $20M floor is a floor, not a test. Prank filings under it survive: Logan
-- Keener at DODO COMMITTEE takes $20.0M of the 2026 cycle, Kurt Cobain at
-- NIRVANA LLC takes $12.4M of 2022, Jason Kim takes $10.0M of 2020. 2026 is
-- worst hit at 2.7% of its clean total; 2024 is cleanest at 0.1%. Nothing here
-- will warn you when the floor stops holding.

with source as (
    select * from {{ source('ripple_raw', 'FED_FEC_INDEPENDENT_EXPENDITURES') }}
)

select
    CAND_ID as CAND_ID,
    CAND_NAME as CAND_NAME,
    SPE_ID as SPE_ID,
    SPE_NAM as SPE_NAM,
    ELE_TYPE as ELE_TYPE,
    CAN_OFFICE_STATE as CAN_OFFICE_STATE,
    CAN_OFFICE_DIS as CAN_OFFICE_DIS,
    CAN_OFFICE as CAN_OFFICE,
    CAND_PTY_AFF as CAND_PTY_AFF,
    EXP_AMO as EXP_AMO,
    EXP_DATE as EXP_DATE,
    AGG_AMO as AGG_AMO,
    SUP_OPP as SUP_OPP,
    PUR as PUR,
    PAY as PAY,
    {{ ripple_num('FILE_NUM') }} as FILE_NUM,
    AMNDT_IND as AMNDT_IND,
    TRAN_ID as TRAN_ID,
    {{ ripple_num('IMAGE_NUM') }} as IMAGE_NUM,
    RECEIPT_DAT as RECEIPT_DAT,
    FEC_ELECTION_YR as FEC_ELECTION_YR,
    {{ ripple_num('PREV_FILE_NUM') }} as PREV_FILE_NUM,
    DISSEM_DT as DISSEM_DT,
    "CYCLE_FILE" as CYCLE_FILE,
    "IS_SUSPECT_FILING" as IS_SUSPECT_FILING,
    "IS_SUPERSEDED" as IS_SUPERSEDED
from source
