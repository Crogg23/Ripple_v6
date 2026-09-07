-- GRAIN: one row per (object_id, person_seq), the Part VII Section A line of
-- one Form 990. Newest INGESTED_AT per object_id wins, so a re-run that lands
-- a return twice does not double its people.
--
-- Landing is all text. The XML writes dollars as whole numbers, hours as
-- '40.00' or '1', and the position checkboxes as 'X' or absent. ein here is
-- the filer EIN from the XML ReturnHeader, which the loader matched to the
-- index EIN by OBJECT_ID; both are 9 digits, unpadded in BMF too.

with source as (

    select * from {{ source('ripple_raw', 'FED_IRS_990_OFFICER_PAY') }}

),

newest as (

    select *
    from source
    qualify INGESTED_AT = max(INGESTED_AT) over (partition by OBJECT_ID)

)

select
    OBJECT_ID                                                   as object_id,
    lpad(trim(EIN), 9, '0')                                     as ein,
    TAX_YEAR                                                    as tax_year,
    try_to_date(TAX_PERIOD_END)                                 as tax_period_end,
    TAX_PERIOD                                                  as tax_period,
    RETURN_TYPE                                                 as return_type,
    FILER_NAME                                                  as filer_name,
    try_to_number(PERSON_SEQ)                                   as person_seq,
    PERSON_NAME                                                 as person_name,
    TITLE                                                       as title,
    {{ ripple_num('AVG_HOURS_PER_WEEK') }}                      as avg_hours_per_week,
    {{ ripple_num('AVG_HOURS_PER_WEEK_RELATED_ORG') }}          as avg_hours_per_week_related_org,
    (nullif(trim(IS_TRUSTEE_OR_DIRECTOR), '') is not null)      as is_trustee_or_director,
    (nullif(trim(IS_INSTITUTIONAL_TRUSTEE), '') is not null)    as is_institutional_trustee,
    (nullif(trim(IS_OFFICER), '') is not null)                  as is_officer,
    (nullif(trim(IS_KEY_EMPLOYEE), '') is not null)             as is_key_employee,
    (nullif(trim(IS_HIGHEST_COMPENSATED), '') is not null)      as is_highest_compensated,
    (nullif(trim(IS_FORMER), '') is not null)                   as is_former,
    {{ ripple_num('REPORTABLE_COMP_FROM_ORG') }}                as reportable_comp_from_org,
    {{ ripple_num('REPORTABLE_COMP_FROM_RELATED_ORGS') }}       as reportable_comp_from_related_orgs,
    {{ ripple_num('OTHER_COMPENSATION') }}                      as other_compensation,
    SCHEMA_VERSION                                              as schema_version,
    SOURCE_ZIP                                                  as source_zip,
    INGESTED_AT                                                 as _loaded_at,
    _SOURCE_RUN_ID                                              as _source_run_id,
    'https://www.irs.gov/charities-non-profits/form-990-series-downloads' as _source_url
from newest
