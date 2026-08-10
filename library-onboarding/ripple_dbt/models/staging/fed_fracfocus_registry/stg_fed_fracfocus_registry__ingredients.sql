{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FRACFOCUS_REGISTRY') }}

),

renamed as (

    select

        -- identifiers
        {{ dbt_utils.generate_surrogate_key(['DISCLOSUREID', 'PURPOSEID', 'INGREDIENTSID']) }} as ingredient_record_id,
        trim(DISCLOSUREID)                                  as disclosure_id,
        trim(PURPOSEID)                                     as purpose_id,
        trim(INGREDIENTSID)                                 as ingredients_id,
        trim(APINUMBER)                                     as api_number,
        trim(CASNUMBER)                                     as cas_number,

        -- dimensions
        trim(STATENAME)                                     as state_name,
        trim(COUNTYNAME)                                    as county_name,
        trim(OPERATORNAME)                                  as operator_name,
        trim(WELLNAME)                                      as well_name,
        trim(PROJECTION)                                    as projection,
        trim(FFVERSION)                                     as ff_version,
        trim(FEDERALWELL)                                   as federal_well,
        trim(INDIANWELL)                                    as indian_well,
        trim(TRADENAME)                                     as trade_name,
        trim(SUPPLIER)                                      as supplier,
        trim(PURPOSE)                                       as purpose,
        trim(INGREDIENTNAME)                                as ingredient_name,
        trim(INGREDIENTCOMMONNAME)                          as ingredient_common_name,
        trim(INGREDIENTCOMMENT)                             as ingredient_comment,
        trim(INGREDIENTMSDS)                                as ingredient_msds,
        trim(CLAIMANTCOMPANY)                               as claimant_company,

        -- dates
        cast(try_to_timestamp(trim(JOBSTARTDATE)) as date)  as job_start_date,
        cast(try_to_timestamp(trim(JOBENDDATE)) as date)    as job_end_date,

        -- measures
        try_to_number(trim(LATITUDE), 38, 8)                as latitude,
        try_to_number(trim(LONGITUDE), 38, 8)               as longitude,
        try_to_number(trim(TVD), 38, 4)                     as tvd,
        try_to_number(trim(TOTALBASEWATERVOLUME), 38, 4)    as total_base_water_volume,
        try_to_number(trim(TOTALBASENONWATERVOLUME), 38, 4) as total_base_non_water_volume,
        try_to_number(trim(PERCENTHIGHADDITIVE), 38, 8)     as percent_high_additive,
        try_to_number(trim(PERCENTHFJOB), 38, 8)            as percent_hf_job,
        try_to_number(trim(MASSINGREDIENT), 38, 8)          as mass_ingredient,

        -- metadata
        _INGESTED_AT                                        as _ingested_at,
        _SOURCE_RUN_ID                                      as _source_run_id,
        _SRC_FILE                                           as _src_file

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by disclosure_id, purpose_id, ingredients_id
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where disclosure_id is not null

)

select
    ingredient_record_id,
    disclosure_id,
    purpose_id,
    ingredients_id,
    api_number,
    cas_number,
    state_name,
    county_name,
    operator_name,
    well_name,
    projection,
    ff_version,
    federal_well,
    indian_well,
    trade_name,
    supplier,
    purpose,
    ingredient_name,
    ingredient_common_name,
    ingredient_comment,
    ingredient_msds,
    claimant_company,
    job_start_date,
    job_end_date,
    latitude,
    longitude,
    tvd,
    total_base_water_volume,
    total_base_non_water_volume,
    percent_high_additive,
    percent_hf_job,
    mass_ingredient,
    _ingested_at,
    _source_run_id,
    _src_file
from deduped
where _row_num = 1
