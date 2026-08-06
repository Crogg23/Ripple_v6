{{ config(materialized='view') }}

-- GRAIN: one row per 510(k) clearance decision (K_NUMBER is unique)
-- Source: openFDA device/510k bulk JSON, split-loaded into ~2,000-record VARIANT
-- chunks (scripts/fda_bulk_split_load.py). Flatten RAW:results per chunk.

with flattened as (

    select
        f.value:k_number::string                                        as k_number,
        f.value:applicant::string                                       as applicant,
        f.value:device_name::string                                     as device_name,
        f.value:product_code::string                                    as product_code,
        f.value:clearance_type::string                                  as clearance_type,
        f.value:decision_code::string                                   as decision_code,
        f.value:decision_description::string                            as decision_description,
        f.value:statement_or_summary::string                            as statement_or_summary,
        f.value:third_party_flag::string                                as third_party_flag,
        f.value:expedited_review_flag::string                           as expedited_review_flag,
        f.value:advisory_committee::string                               as advisory_committee,
        f.value:advisory_committee_description::string                  as advisory_committee_description,
        f.value:review_advisory_committee::string                       as review_advisory_committee,
        try_to_date(f.value:date_received::string, 'YYYY-MM-DD')        as date_received,
        try_to_date(f.value:decision_date::string, 'YYYY-MM-DD')        as decision_date,
        f.value:address_1::string                                       as address_1,
        f.value:address_2::string                                       as address_2,
        f.value:city::string                                            as city,
        f.value:state::string                                           as state,
        f.value:postal_code::string                                     as postal_code,
        f.value:zip_code::string                                        as zip_code,
        f.value:country_code::string                                    as country_code,
        f.value:openfda                                                 as openfda,
        t._ingested_at                                                  as _ingested_at,
        t._source_run_id                                                as _source_run_id
    from {{ source('ripple_raw', 'FED_FDA_DEVICE_510K') }} t,
         lateral flatten(input => t.RAW:results) f

),

deduped as (

    select *,
        row_number() over (
            partition by k_number
            order by _ingested_at desc
        ) as _row_num
    from flattened
    where k_number is not null

)

select
    k_number,
    applicant,
    device_name,
    product_code,
    clearance_type,
    decision_code,
    decision_description,
    statement_or_summary,
    third_party_flag,
    expedited_review_flag,
    advisory_committee,
    advisory_committee_description,
    review_advisory_committee,
    date_received,
    decision_date,
    address_1,
    address_2,
    city,
    state,
    postal_code,
    zip_code,
    country_code,
    openfda,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
