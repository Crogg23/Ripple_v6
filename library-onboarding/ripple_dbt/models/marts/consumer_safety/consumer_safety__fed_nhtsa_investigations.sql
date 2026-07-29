{{ config(materialized='table', schema='CONSUMER_SAFETY') }}

-- GRAIN: one row per investigation-vehicle combination
-- Answers: What defect investigations has NHTSA opened, and did they result in recalls?
-- Source: NHTSA ODI Investigations (~154K records)
-- Key joins: recall_number â†’ nhtsa_recalls.campno; mfr_name â†’ manufacturer entities

select
    nhtsa_action_number,
    make,
    model,
    year_txt                             as model_year,
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
