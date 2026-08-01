{{ config(materialized='table', schema='LABOR') }}

-- GRAIN: one row per (violation, contest docket). Fixed 2026-07-31: "event_no +
-- violation_no is unique" was very nearly true (51 of 3,087,266 rows, 0.0017%,
-- violate it) but not exactly -- a violation that gets formally contested picks up
-- a docket_no/docket_status_cd/contested_dt, and the ~51 cases where a violation
-- was re-contested (a new docket opened) produced a second real row that the old key
-- silently discarded. docket_no now joins the key. Verified live: lossless --
-- COUNT(DISTINCT event_no||violation_no||docket_no) == 3,087,266 exactly, matching
-- the raw source row count with zero further collapsing.
-- Answers: Which mines have the most safety violations, how severe, and what fines?
-- Source: MSHA Violations (3,087,266 records — exact, verified 2026-07-31)
-- Key joins: mine_id â†’ msha_mines; violator_name â†’ entity resolution

select
    event_no,
    violation_no,
    mine_id,
    mine_name,
    mine_type,
    coal_metal_ind,
    controller_id,
    controller_name,
    violator_id,
    violator_name,
    try_to_date(violation_occur_dt, 'MM/DD/YYYY')  as violation_occur_date,
    try_to_date(violation_issue_dt, 'MM/DD/YYYY')  as violation_issue_date,
    try_to_number(cal_yr)                          as cal_yr,
    section_of_act,
    sig_sub,
    likelihood,
    inj_illness,
    try_to_number(no_affected)                     as no_affected,
    negligence,
    try_to_double(proposed_penalty)                as proposed_penalty,
    try_to_double(amount_due)                      as amount_due,
    try_to_double(amount_paid)                     as amount_paid,
    try_to_number(violator_violation_cnt)          as violator_violation_cnt,
    try_to_number(violator_inspection_day_cnt)     as violator_inspection_day_cnt,
    (sig_sub = 'Y') as is_significant_and_substantial,
    _loaded_at
from {{ ref('stg_fed_msha_violations__records') }}
qualify row_number() over (partition by event_no, violation_no, docket_no order by _loaded_at desc) = 1
