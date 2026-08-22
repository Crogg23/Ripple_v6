{{ config(materialized='table', schema='CONSUMER_SAFETY') }}

-- GRAIN: one row per investigation-vehicle-RECALL combination. Fixed 2026-07-31:
-- was one row per investigation-vehicle, silently keeping only ONE of a possibly-
-- multiple recall_number per investigation (arbitrary, whichever loaded last). A
-- single investigation into one defect commonly maps to SEVERAL recall campaigns
-- (e.g. one HID-headlight defect action tied to 11 distinct recall numbers) -- so
-- COUNT(*) on this mart is not "number of investigations", it's "number of
-- investigation-recall LINKS". Group by nhtsa_action_number for investigation-level
-- counts.
-- Answers: What defect investigations has NHTSA opened, and did they result in recalls?
-- Source: NHTSA ODI Investigations (154,209 records — exact, verified 2026-07-31)
-- Key joins: recall_number â†’ nhtsa_recalls.campno; mfr_name â†’ manufacturer entities

select
    nhtsa_action_number,
    make,
    model,
    {{ ripple_dt('year_txt') }} as model_year,
    compname                             as component,
    mfr_name,
    open_date,
    close_date,
    recall_number,
    subject,
    summary,
    (recall_number is not null and trim(recall_number) != '') as resulted_in_recall,
    (close_date is not null) as is_closed,
    _loaded_at,
    _source_run_id
from {{ ref('stg_fed_nhtsa_investigations__records') }}
