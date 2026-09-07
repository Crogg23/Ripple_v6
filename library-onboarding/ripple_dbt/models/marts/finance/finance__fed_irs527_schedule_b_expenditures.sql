{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per itemized expenditure by a 527 political organization.
-- 8,191,177 rows. Landed 2026-09-06 alongside Schedule A.
--
-- MIRROR OF SCHEDULE A, WITH ONE TRAP. Both records are 18 fields wide in the
-- source and they DIVERGE AT POSITION 15: A holds the year-to-date aggregate
-- there and the date at 16, B holds the date at 15 and the purpose at 16.
-- The loader already untangled that, and this is where it stays untangled.
--
-- PERSON_NAME in the source is the RECIPIENT here, the contributor in A.
--
-- EXPENDITURE_DATE is YYYYMMDD TEXT, filled on 95.8% of rows.

with source as (
    select * from {{ source('ripple_raw', 'IRS527_SCHEDULE_B_EXPENDITURES') }}
)

select
    FORM_ID_NUMBER                                  as form_id_number,
    SCHEDULE_ID                                     as schedule_id,
    ORG_NAME                                        as org_name,
    EIN                                             as ein,
    PERSON_NAME                                     as recipient_name,
    ADDR1                                           as recipient_addr1,
    ADDR2                                           as recipient_addr2,
    CITY                                            as recipient_city,
    STATE                                           as recipient_state,
    ZIP                                             as recipient_zip,
    ZIP_EXT                                         as recipient_zip_ext,
    EMPLOYER                                        as recipient_employer,
    OCCUPATION                                      as recipient_occupation,
    {{ ripple_num('AMOUNT') }}                      as expenditure_amount,
    EXPENDITURE_PURPOSE                             as expenditure_purpose,
    try_to_date(nullif(trim(EXPENDITURE_DATE), ''), 'YYYYMMDD') as expenditure_date,
    EXPENDITURE_DATE                                as expenditure_date_raw,
    'irs527_schedule_b_expenditures'                as source_id,
    INGESTED_AT                                     as _loaded_at
from source
