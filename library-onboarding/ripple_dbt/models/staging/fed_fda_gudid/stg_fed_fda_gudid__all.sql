{{ config(materialized='view') }}

-- GRAIN: one row per device catalog record (public_device_record_key is unique).
-- identifiers is an array of UDIs on the record (primary + package-level secondaries);
-- primary_di pulls the first (Primary type where present, else the first entry) for
-- the join to MAUDE.device.udi_di.
-- Source: openFDA device/udi bulk JSON, split-loaded into ~2,000-record VARIANT chunks.

with flattened as (

    select
        f.value:public_device_record_key::string                        as public_device_record_key,
        f.value:identifiers                                              as identifiers,
        -- most records list the Primary DI first; identifiers[0]:id is the
        -- practical join key to MAUDE.device.udi_di (a full best-match-any-DI
        -- join can unnest `identifiers` at the mart layer if needed).
        f.value:identifiers[0]:id::string                                as primary_di,
        f.value:brand_name::string                                       as brand_name,
        f.value:company_name::string                                     as company_name,
        f.value:labeler_duns_number::string                              as labeler_duns_number,
        f.value:version_or_model_number::string                          as version_or_model_number,
        f.value:catalog_number::string                                   as catalog_number,
        f.value:device_description::string                               as device_description,
        f.value:product_codes                                            as product_codes,
        f.value:product_codes[0]:code::string                            as primary_product_code,
        f.value:record_status::string                                    as record_status,
        f.value:commercial_distribution_status::string                   as commercial_distribution_status,
        f.value:is_kit::boolean                                          as is_kit,
        f.value:is_combination_product::boolean                          as is_combination_product,
        try_to_date(f.value:publish_date::string, 'YYYY-MM-DD')          as publish_date,
        try_to_date(f.value:public_version_date::string, 'YYYY-MM-DD')   as public_version_date,
        t._ingested_at                                                   as _ingested_at,
        t._source_run_id                                                 as _source_run_id
    from {{ source('ripple_raw', 'FED_FDA_GUDID') }} t,
         lateral flatten(input => t.RAW:results) f

),

deduped as (

    select *,
        row_number() over (
            partition by public_device_record_key
            order by _ingested_at desc
        ) as _row_num
    from flattened
    where public_device_record_key is not null

)

select
    public_device_record_key,
    identifiers,
    primary_di,
    brand_name,
    company_name,
    labeler_duns_number,
    version_or_model_number,
    catalog_number,
    device_description,
    product_codes,
    primary_product_code,
    record_status,
    commercial_distribution_status,
    is_kit,
    is_combination_product,
    publish_date,
    public_version_date,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
