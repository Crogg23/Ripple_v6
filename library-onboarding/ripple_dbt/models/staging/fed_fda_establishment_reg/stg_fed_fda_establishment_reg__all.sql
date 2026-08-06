{{ config(materialized='view') }}

-- GRAIN: one row per establishment-listing record. A facility (one FEI number)
-- registers once but can list MANY device products, so registration.fei_number
-- alone is NOT unique -- grain is (fei_number, k_number, pma_number, proprietary_name)
-- as a practical dedupe key on top of the raw record.
-- Source: openFDA device/registrationlisting bulk JSON, split-loaded into
-- ~2,000-record VARIANT chunks.

with flattened as (

    select
        f.value:registration:fei_number::string                          as fei_number,
        f.value:registration:registration_number::string                 as registration_number,
        f.value:registration:name::string                                as establishment_name,
        f.value:registration:address_line_1::string                      as address_line_1,
        f.value:registration:address_line_2::string                      as address_line_2,
        f.value:registration:city::string                                as city,
        f.value:registration:state_code::string                          as state_code,
        f.value:registration:iso_country_code::string                    as iso_country_code,
        f.value:registration:postal_code::string                         as postal_code,
        f.value:registration:status_code::string                         as status_code,
        f.value:registration:reg_expiry_date_year::string                as reg_expiry_date_year,
        f.value:registration:owner_operator:firm_name::string            as owner_operator_firm_name,
        f.value:registration:owner_operator:owner_operator_number::string as owner_operator_number,
        f.value:establishment_type                                       as establishment_type,
        f.value:proprietary_name::string                                 as proprietary_name,
        f.value:k_number::string                                         as k_number,
        f.value:pma_number::string                                       as pma_number,
        f.value:products                                                 as products,
        t._ingested_at                                                   as _ingested_at,
        t._source_run_id                                                 as _source_run_id
    from {{ source('ripple_raw', 'FED_FDA_ESTABLISHMENT_REG') }} t,
         lateral flatten(input => t.RAW:results) f

),

deduped as (

    select *,
        row_number() over (
            partition by fei_number, coalesce(k_number, ''), coalesce(pma_number, ''),
                         coalesce(proprietary_name, '')
            order by _ingested_at desc
        ) as _row_num
    from flattened
    where fei_number is not null

)

select
    fei_number,
    registration_number,
    establishment_name,
    address_line_1,
    address_line_2,
    city,
    state_code,
    iso_country_code,
    postal_code,
    status_code,
    reg_expiry_date_year,
    owner_operator_firm_name,
    owner_operator_number,
    establishment_type,
    proprietary_name,
    k_number,
    pma_number,
    products,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
