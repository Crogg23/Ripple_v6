{{ config(materialized='view') }}

-- The loader (scripts/server_side_load.py, "UPGRADE 3") lands openFDA JSON as
-- VARIANT rows holding the whole API response doc, by design -- its docstring
-- says "dbt flattens RAW:results downstream". This landing table holds one
-- VARIANT row whose RAW:results array carries 7,085 device classification
-- records. This model does the flatten the loader always expected, mirroring
-- stg_fed_fda_drug_enforcement__drug_enforcement_recalls.

with

source as (

    select * from {{ source('ripple_raw', 'FED_FDA_DEVICE_CLASSIFICATION') }}

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
        r:product_code::string                           as product_code,
        r:device_name::string                            as device_name,
        r:regulation_number::string                      as regulation_number,

        -- classification
        r:device_class::string                           as device_class,
        r:medical_specialty::string                      as medical_specialty,
        r:medical_specialty_description::string          as medical_specialty_description,
        r:review_panel::string                           as review_panel,
        r:submission_type_id::string                     as submission_type_id,
        r:unclassified_reason::string                    as unclassified_reason,
        r:definition::string                             as definition,

        -- regulatory flags (openFDA carries these as 'Y'/'N' strings)
        r:gmp_exempt_flag::string                        as gmp_exempt_flag,
        r:implant_flag::string                           as implant_flag,
        r:life_sustain_support_flag::string              as life_sustain_support_flag,
        r:third_party_flag::string                       as third_party_flag,

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
            partition by product_code
            order by _ingested_at desc
        ) as _row_num
    from renamed_cast

)

select
    product_code,
    device_name,
    regulation_number,
    device_class,
    medical_specialty,
    medical_specialty_description,
    review_panel,
    submission_type_id,
    unclassified_reason,
    definition,
    gmp_exempt_flag,
    implant_flag,
    life_sustain_support_flag,
    third_party_flag,
    openfda,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
