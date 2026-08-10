{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_WQP_MONITORING_STATIONS') }}

),

renamed as (

    select

        trim(ORGANIZATIONIDENTIFIER)                   as organization_identifier,
        trim(ORGANIZATIONFORMALNAME)                   as organization_formal_name,
        trim(MONITORINGLOCATIONIDENTIFIER)             as monitoring_location_identifier,
        trim(MONITORINGLOCATIONNAME)                   as monitoring_location_name,
        trim(MONITORINGLOCATIONTYPENAME)               as monitoring_location_type_name,
        trim(MONITORINGLOCATIONDESCRIPTIONTEXT)        as monitoring_location_description_text,
        trim(HUCEIGHTDIGITCODE)                        as huc_eight_digit_code,
        try_to_number(trim(DRAINAGEAREAMEASURE_MEASUREVALUE)) as drainage_area_measure_value,
        trim(DRAINAGEAREAMEASURE_MEASUREUNITCODE)      as drainage_area_measure_unit_code,
        try_to_number(trim(CONTRIBUTINGDRAINAGEAREAMEASURE_MEASUREVALUE)) as contributing_drainage_area_measure_value,
        trim(CONTRIBUTINGDRAINAGEAREAMEASURE_MEASUREUNITCODE) as contributing_drainage_area_measure_unit_code,
        try_to_number(trim(LATITUDEMEASURE))           as latitude,
        try_to_number(trim(LONGITUDEMEASURE))          as longitude,
        try_to_number(trim(SOURCEMAPSCALENUMERIC))     as source_map_scale_numeric,
        try_to_number(trim(HORIZONTALACCURACYMEASURE_MEASUREVALUE)) as horizontal_accuracy_measure_value,
        trim(HORIZONTALACCURACYMEASURE_MEASUREUNITCODE) as horizontal_accuracy_measure_unit_code,
        trim(HORIZONTALCOLLECTIONMETHODNAME)           as horizontal_collection_method_name,
        trim(HORIZONTALCOORDINATEREFERENCESYSTEMDATUMNAME) as horizontal_datum_name,
        try_to_number(trim(VERTICALMEASURE_MEASUREVALUE)) as vertical_measure_value,
        trim(VERTICALMEASURE_MEASUREUNITCODE)          as vertical_measure_unit_code,
        try_to_number(trim(VERTICALACCURACYMEASURE_MEASUREVALUE)) as vertical_accuracy_measure_value,
        trim(VERTICALACCURACYMEASURE_MEASUREUNITCODE)  as vertical_accuracy_measure_unit_code,
        trim(VERTICALCOLLECTIONMETHODNAME)             as vertical_collection_method_name,
        trim(VERTICALCOORDINATEREFERENCESYSTEMDATUMNAME) as vertical_datum_name,
        trim(COUNTRYCODE)                              as country_code,
        trim(STATECODE)                                as state_code,
        trim(COUNTYCODE)                               as county_code,
        trim(AQUIFERNAME)                              as aquifer_name,
        LOCALAQFRNAME                                  as local_aquifer_name,
        trim(FORMATIONTYPETEXT)                        as formation_type_text,
        trim(AQUIFERTYPENAME)                          as aquifer_type_name,
        trim(CONSTRUCTIONDATETEXT)                     as construction_date_text,
        try_to_number(trim(WELLDEPTHMEASURE_MEASUREVALUE)) as well_depth_measure_value,
        trim(WELLDEPTHMEASURE_MEASUREUNITCODE)         as well_depth_measure_unit_code,
        try_to_number(trim(WELLHOLEDEPTHMEASURE_MEASUREVALUE)) as well_hole_depth_measure_value,
        trim(WELLHOLEDEPTHMEASURE_MEASUREUNITCODE)     as well_hole_depth_measure_unit_code,
        trim(PROVIDERNAME)                             as provider_name,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by monitoring_location_identifier
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where monitoring_location_identifier is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
