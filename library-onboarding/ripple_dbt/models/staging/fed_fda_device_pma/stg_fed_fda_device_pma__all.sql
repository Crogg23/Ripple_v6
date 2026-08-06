{{ config(materialized='view') }}

-- GRAIN: one row per PMA decision. pma_number alone is NOT unique -- PMA supplements
-- (design/labeling changes to an already-approved device) reuse the same pma_number
-- with a different supplement_number, so the natural key is (pma_number, supplement_number).
-- Source: openFDA device/pma bulk JSON, split-loaded into ~2,000-record VARIANT chunks.

with flattened as (

    select
        f.value:pma_number::string                                      as pma_number,
        f.value:supplement_number::string                                as supplement_number,
        f.value:supplement_type::string                                  as supplement_type,
        f.value:supplement_reason::string                                as supplement_reason,
        f.value:applicant::string                                        as applicant,
        f.value:trade_name::string                                       as trade_name,
        f.value:generic_name::string                                     as generic_name,
        f.value:product_code::string                                     as product_code,
        f.value:docket_number::string                                    as docket_number,
        f.value:decision_code::string                                    as decision_code,
        f.value:ao_statement::string                                     as ao_statement,
        f.value:expedited_review_flag::string                            as expedited_review_flag,
        f.value:advisory_committee::string                               as advisory_committee,
        f.value:advisory_committee_description::string                   as advisory_committee_description,
        try_to_date(f.value:date_received::string, 'YYYY-MM-DD')         as date_received,
        try_to_date(f.value:decision_date::string, 'YYYY-MM-DD')         as decision_date,
        f.value:street_1::string                                         as street_1,
        f.value:street_2::string                                         as street_2,
        f.value:city::string                                             as city,
        f.value:state::string                                            as state,
        f.value:zip::string                                              as zip,
        f.value:zip_ext::string                                          as zip_ext,
        f.value:openfda                                                  as openfda,
        t._ingested_at                                                   as _ingested_at,
        t._source_run_id                                                 as _source_run_id
    from {{ source('ripple_raw', 'FED_FDA_DEVICE_PMA') }} t,
         lateral flatten(input => t.RAW:results) f

),

deduped as (

    select *,
        row_number() over (
            partition by pma_number, supplement_number
            order by _ingested_at desc
        ) as _row_num
    from flattened
    where pma_number is not null

)

select
    pma_number,
    supplement_number,
    supplement_type,
    supplement_reason,
    applicant,
    trade_name,
    generic_name,
    product_code,
    docket_number,
    decision_code,
    ao_statement,
    expedited_review_flag,
    advisory_committee,
    advisory_committee_description,
    date_received,
    decision_date,
    street_1,
    street_2,
    city,
    state,
    zip,
    zip_ext,
    openfda,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
