{{ config(materialized='view') }}

-- GRAIN: one row per CAERS cosmetic adverse event report (REPORT_NUMBER is unique)
-- Source: openFDA cosmetic/event bulk JSON. Landing table holds N VARIANT rows
-- (one per ~2,000-record chunk, see scripts/fda_bulk_split_load.py); each row's
-- RAW is {"results": [...]}. Flatten RAW:results to get one row per report.

with flattened as (

    select
        f.value:report_number::string                                        as report_number,
        f.value:report_type::string                                          as report_type,
        f.value:report_version::string                                       as report_version,
        try_to_date(f.value:initial_received_date::string, 'YYYYMMDD')       as initial_received_date,
        try_to_date(f.value:latest_received_date::string, 'YYYYMMDD')        as latest_received_date,
        f.value:meddra_version::string                                       as meddra_version,
        f.value:patient                                                      as patient,
        f.value:products                                                     as products,
        f.value:reactions                                                    as reactions,
        f.value:outcomes                                                     as outcomes,
        f.value:products[0]:name_brand::string                               as product_brand_name,
        f.value:products[0]:industry_code::string                            as product_industry_code,
        f.value:products[0]:industry_name::string                            as product_industry_name,
        f.value:reactions[0]:text::string                                    as primary_reaction_text,
        t._ingested_at                                                       as _ingested_at,
        t._source_run_id                                                     as _source_run_id
    from {{ source('ripple_raw', 'FED_FDA_CAERS') }} t,
         lateral flatten(input => t.RAW:results) f

),

deduped as (

    select *,
        row_number() over (
            partition by report_number
            order by _ingested_at desc
        ) as _row_num
    from flattened
    where report_number is not null

)

select
    report_number,
    report_type,
    report_version,
    initial_received_date,
    latest_received_date,
    meddra_version,
    patient,
    products,
    reactions,
    outcomes,
    product_brand_name,
    product_industry_code,
    product_industry_name,
    primary_reaction_text,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
