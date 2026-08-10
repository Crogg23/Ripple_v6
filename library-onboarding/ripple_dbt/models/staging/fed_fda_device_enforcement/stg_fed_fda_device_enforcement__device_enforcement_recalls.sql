{{ config(materialized='view') }}

-- The loader (scripts/server_side_load.py, "UPGRADE 3") lands openFDA JSON as
-- VARIANT rows holding whole API response docs, by design -- its docstring
-- says "dbt flattens RAW:results downstream". This landing table holds 20
-- VARIANT chunk rows whose RAW:results arrays together carry 39,635 device
-- recall records. This model does the flatten the loader always expected,
-- mirroring stg_fed_fda_drug_enforcement__drug_enforcement_recalls.

with

source as (

    select * from {{ source('ripple_raw', 'FED_FDA_DEVICE_ENFORCEMENT') }}

),

flattened as (

    select
        rec.value as r,
        source._ingested_at,
        source._source_run_id
    from source,
    lateral flatten(input => source.raw:results) as rec

),

renamed_cast as (

    select

        -- key identifiers
        r:recall_number::string                          as recall_number,
        r:event_id::string                               as event_id,
        r:product_code::string                           as product_code,

        -- status / classification
        r:status::string                                 as status,
        r:classification::string                         as classification,
        r:voluntary_mandated::string                     as voluntary_mandated,
        r:initial_firm_notification::string              as initial_firm_notification,

        -- product details
        r:product_type::string                           as product_type,
        r:product_description::string                    as product_description,
        r:product_quantity::string                       as product_quantity,
        r:reason_for_recall::string                      as reason_for_recall,
        r:distribution_pattern::string                   as distribution_pattern,
        r:code_info::string                              as code_info,
        r:more_code_info::string                         as more_code_info,

        -- dates (openFDA carries these as YYYYMMDD strings)
        {{ parse_yyyymmdd('r:recall_initiation_date::string') }}     as recall_initiation_date,
        {{ parse_yyyymmdd('r:center_classification_date::string') }} as center_classification_date,
        {{ parse_yyyymmdd('r:termination_date::string') }}           as termination_date,
        {{ parse_yyyymmdd('r:report_date::string') }}                as report_date,

        -- recalling firm
        r:recalling_firm::string                         as recalling_firm,
        r:address_1::string                              as address_1,
        r:address_2::string                              as address_2,
        r:city::string                                   as city,
        r:state::string                                  as state,
        r:postal_code::string                            as postal_code,
        r:country::string                                as country,

        -- openFDA enrichment sub-object, kept whole
        r:openfda                                        as openfda,

        -- metadata
        _ingested_at                                     as _ingested_at,
        _source_run_id                                   as _source_run_id

    from flattened

),

deduped as (

    select *,
        row_number() over (
            partition by recall_number
            order by _ingested_at desc
        ) as _row_num
    from renamed_cast

)

select
    recall_number,
    event_id,
    product_code,
    status,
    classification,
    voluntary_mandated,
    initial_firm_notification,
    product_type,
    product_description,
    product_quantity,
    reason_for_recall,
    distribution_pattern,
    code_info,
    more_code_info,
    recall_initiation_date,
    center_classification_date,
    termination_date,
    report_date,
    recalling_firm,
    address_1,
    address_2,
    city,
    state,
    postal_code,
    country,
    openfda,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
