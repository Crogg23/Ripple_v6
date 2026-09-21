{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_CMS_NURSING_HOME') }}

),

renamed as (

    select

        -- primary & key identifiers
        CMS_CERTIFICATION_NUMBER__CCN                                        as cms_certification_number_ccn,
        PROVIDER_NUMBER                                                       as provider_number,
        -- NPI intentionally excluded: CMS Provider Information source has no NPI
        -- field (verified live against the CMS provider-data API, 2026-08-08);
        -- the landing column is 100% empty strings. Use the CMS facility
        -- affiliation mart for the NPI<->CCN bridge instead.
        COUNTY_FIPS                                                           as county_fips,
        PROVIDER_SSA_COUNTY_CODE                                              as provider_ssa_county_code,

        -- provider identity
        PROVIDER_NAME                                                         as provider_name,
        LEGAL_BUSINESS_NAME                                                   as legal_business_name,
        PROVIDER_TYPE                                                         as provider_type,
        OWNERSHIP_TYPE                                                        as ownership_type,

        -- address / geography
        PROVIDER_ADDRESS                                                      as provider_address,
        ADDRESS                                                               as address,
        CITY_TOWN                                                             as city_town,
        CITY                                                                  as city,
        STATE                                                                 as state,
        ZIP_CODE                                                              as zip_code,
        COUNTY_PARISH                                                         as county_parish,
        URBAN                                                                 as urban,
        LOCATION                                                              as location,
        {{ stg_float('LATITUDE') }}                                               as latitude,
        {{ stg_float('LONGITUDE') }}                                              as longitude,
        GEOCODING_FOOTNOTE                                                    as geocoding_footnote,

        -- contact
        TELEPHONE_NUMBER                                                      as telephone_number,
        PHONE_NUMBER                                                          as phone_number,

        -- certification / dates
        try_to_date(nullif(trim(DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES), ''), 'YYYY-MM-DD') as date_first_approved_to_provide_medicare_and_medicaid_services,
        try_to_date(DATE_OF_MOST_RECENT_HEALTH_INSPECTION, 'MM/DD/YYYY')     as date_of_most_recent_health_inspection,
        try_to_date(nullif(trim(PROCESSING_DATE), ''), 'YYYY-MM-DD')                           as processing_date,

        -- facility flags
        PROVIDER_RESIDES_IN_HOSPITAL                                         as provider_resides_in_hospital,
        CONTINUING_CARE_RETIREMENT_COMMUNITY                                 as continuing_care_retirement_community,
        SPECIAL_FOCUS_STATUS                                                 as special_focus_status,
        ABUSE_ICON                                                           as abuse_icon,
        MOST_RECENT_HEALTH_INSPECTION_MORE_THAN_2_YEARS_AGO                  as most_recent_health_inspection_more_than_2_years_ago,
        PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS                         as provider_changed_ownership_in_last_12_months,
        WITH_A_RESIDENT_AND_FAMILY_COUNCIL                                   as with_a_resident_and_family_council,
        AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS                    as automatic_sprinkler_systems_in_all_required_areas,

        -- capacity / census
        {{ stg_int('NUMBER_OF_CERTIFIED_BEDS') }}                              as number_of_certified_beds,
        {{ stg_float('AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY') }}                  as average_number_of_residents_per_day,
        AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY_FOOTNOTE                         as average_number_of_residents_per_day_footnote,
        {{ stg_int('NUMBER_OF_RESIDENTS_IN_CERTIFIED_BEDS') }}                 as number_of_residents_in_certified_beds,

        -- chain info
        CHAIN_NAME                                                            as chain_name,
        CHAIN_ID                                                              as chain_id,
        {{ stg_int('NUMBER_OF_FACILITIES_IN_CHAIN') }}                         as number_of_facilities_in_chain,
        {{ stg_float('CHAIN_AVERAGE_OVERALL_5_STAR_RATING') }}                   as chain_average_overall_5_star_rating,
        {{ stg_float('CHAIN_AVERAGE_HEALTH_INSPECTION_RATING') }}                as chain_average_health_inspection_rating,
        {{ stg_float('CHAIN_AVERAGE_STAFFING_RATING') }}                         as chain_average_staffing_rating,
        {{ stg_float('CHAIN_AVERAGE_QM_RATING') }}                               as chain_average_qm_rating,

        -- overall ratings
        {{ stg_int('OVERALL_RATING') }}                                        as overall_rating,
        OVERALL_RATING_FOOTNOTE                                              as overall_rating_footnote,
        {{ stg_int('HEALTH_INSPECTION_RATING') }}                              as health_inspection_rating,
        HEALTH_INSPECTION_RATING_FOOTNOTE                                    as health_inspection_rating_footnote,
        {{ stg_int('QUALITY_MEASURE_RATING') }}                                as quality_measure_rating,
        QM_RATING_FOOTNOTE                                                   as qm_rating_footnote,
        {{ stg_int('LONG_STAY_QM_RATING') }}                                   as long_stay_qm_rating,
        LONG_STAY_QM_RATING_FOOTNOTE                                         as long_stay_qm_rating_footnote,
        {{ stg_int('SHORT_STAY_QM_RATING') }}                                  as short_stay_qm_rating,
        SHORT_STAY_QM_RATING_FOOTNOTE                                        as short_stay_qm_rating_footnote,
        {{ stg_int('STAFFING_RATING') }}                                       as staffing_rating,
        STAFFING_RATING_FOOTNOTE                                             as staffing_rating_footnote,
        REPORTED_STAFFING_FOOTNOTE                                           as reported_staffing_footnote,
        PHYSICAL_THERAPIST_STAFFING_FOOTNOTE                                 as physical_therapist_staffing_footnote,

        -- reported staffing hours
        {{ stg_float('REPORTED_NURSE_AIDE_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}    as reported_nurse_aide_staffing_hours_per_resident_per_day,
        {{ stg_float('REPORTED_LPN_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}           as reported_lpn_staffing_hours_per_resident_per_day,
        {{ stg_float('REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}            as reported_rn_staffing_hours_per_resident_per_day,
        {{ stg_float('REPORTED_LICENSED_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}      as reported_licensed_staffing_hours_per_resident_per_day,
        {{ stg_float('REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}   as reported_total_nurse_staffing_hours_per_resident_per_day,
        {{ stg_float('TOTAL_NUMBER_OF_NURSE_STAFF_HOURS_PER_RESIDENT_PER_DAY_ON_THE_WEEKEND') }} as total_number_of_nurse_staff_hours_per_resident_per_day_on_the_weekend,
        {{ stg_float('REGISTERED_NURSE_HOURS_PER_RESIDENT_PER_DAY_ON_THE_WEEKEND') }} as registered_nurse_hours_per_resident_per_day_on_the_weekend,
        {{ stg_float('REPORTED_PHYSICAL_THERAPIST_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }} as reported_physical_therapist_staffing_hours_per_resident_per_day,

        -- turnover
        {{ stg_float('TOTAL_NURSING_STAFF_TURNOVER') }}                          as total_nursing_staff_turnover,
        TOTAL_NURSING_STAFF_TURNOVER_FOOTNOTE                                as total_nursing_staff_turnover_footnote,
        {{ stg_float('REGISTERED_NURSE_TURNOVER') }}                             as registered_nurse_turnover,
        REGISTERED_NURSE_TURNOVER_FOOTNOTE                                   as registered_nurse_turnover_footnote,
        {{ stg_int('NUMBER_OF_ADMINISTRATORS_WHO_HAVE_LEFT_THE_NURSING_HOME') }} as number_of_administrators_who_have_left_the_nursing_home,
        ADMINISTRATOR_TURNOVER_FOOTNOTE                                      as administrator_turnover_footnote,

        -- case mix
        {{ stg_float('NURSING_CASE_MIX_INDEX') }}                                as nursing_case_mix_index,
        {{ stg_float('NURSING_CASE_MIX_INDEX_RATIO') }}                          as nursing_case_mix_index_ratio,
        {{ stg_float('CASE_MIX_NURSE_AIDE_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}    as case_mix_nurse_aide_staffing_hours_per_resident_per_day,
        {{ stg_float('CASE_MIX_LPN_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}           as case_mix_lpn_staffing_hours_per_resident_per_day,
        {{ stg_float('CASE_MIX_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}            as case_mix_rn_staffing_hours_per_resident_per_day,
        {{ stg_float('CASE_MIX_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}   as case_mix_total_nurse_staffing_hours_per_resident_per_day,
        {{ stg_float('CASE_MIX_WEEKEND_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }} as case_mix_weekend_total_nurse_staffing_hours_per_resident_per_day,

        -- adjusted staffing
        {{ stg_float('ADJUSTED_NURSE_AIDE_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}    as adjusted_nurse_aide_staffing_hours_per_resident_per_day,
        {{ stg_float('ADJUSTED_LPN_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}           as adjusted_lpn_staffing_hours_per_resident_per_day,
        {{ stg_float('ADJUSTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}            as adjusted_rn_staffing_hours_per_resident_per_day,
        {{ stg_float('ADJUSTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }}   as adjusted_total_nurse_staffing_hours_per_resident_per_day,
        {{ stg_float('ADJUSTED_WEEKEND_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY') }} as adjusted_weekend_total_nurse_staffing_hours_per_resident_per_day,

        -- health survey cycle 1
        try_to_date(nullif(trim(RATING_CYCLE_1_STANDARD_SURVEY_HEALTH_DATE), ''), 'YYYY-MM-DD')     as rating_cycle_1_standard_survey_health_date,
        {{ stg_int('RATING_CYCLE_1_TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES') }}         as rating_cycle_1_total_number_of_health_deficiencies,
        {{ stg_int('RATING_CYCLE_1_NUMBER_OF_STANDARD_HEALTH_DEFICIENCIES') }}      as rating_cycle_1_number_of_standard_health_deficiencies,
        {{ stg_int('RATING_CYCLE_1_NUMBER_OF_COMPLAINT_HEALTH_DEFICIENCIES') }}     as rating_cycle_1_number_of_complaint_health_deficiencies,
        {{ stg_float('RATING_CYCLE_1_HEALTH_DEFICIENCY_SCORE') }}                     as rating_cycle_1_health_deficiency_score,
        {{ stg_int('RATING_CYCLE_1_NUMBER_OF_HEALTH_REVISITS') }}                   as rating_cycle_1_number_of_health_revisits,
        {{ stg_float('RATING_CYCLE_1_HEALTH_REVISIT_SCORE') }}                        as rating_cycle_1_health_revisit_score,
        {{ stg_float('RATING_CYCLE_1_TOTAL_HEALTH_SCORE') }}                          as rating_cycle_1_total_health_score,

        -- health survey cycle 2-3
        try_to_date(nullif(trim(RATING_CYCLE_2_STANDARD_HEALTH_SURVEY_DATE), ''), 'YYYY-MM-DD')     as rating_cycle_2_standard_health_survey_date,
        {{ stg_int('RATING_CYCLE_2_3_TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES') }}       as rating_cycle_2_3_total_number_of_health_deficiencies,
        {{ stg_int('RATING_CYCLE_2_NUMBER_OF_STANDARD_HEALTH_DEFICIENCIES') }}      as rating_cycle_2_number_of_standard_health_deficiencies,
        {{ stg_int('RATING_CYCLE_2_3_NUMBER_OF_COMPLAINT_HEALTH_DEFICIENCIES') }}   as rating_cycle_2_3_number_of_complaint_health_deficiencies,
        {{ stg_float('RATING_CYCLE_2_3_HEALTH_DEFICIENCY_SCORE') }}                   as rating_cycle_2_3_health_deficiency_score,
        {{ stg_int('RATING_CYCLE_2_3_NUMBER_OF_HEALTH_REVISITS') }}                 as rating_cycle_2_3_number_of_health_revisits,
        {{ stg_float('RATING_CYCLE_2_3_HEALTH_REVISIT_SCORE') }}                      as rating_cycle_2_3_health_revisit_score,
        {{ stg_float('RATING_CYCLE_2_3_TOTAL_HEALTH_SCORE') }}                        as rating_cycle_2_3_total_health_score,
        {{ stg_float('TOTAL_WEIGHTED_HEALTH_SURVEY_SCORE') }}                         as total_weighted_health_survey_score,

        -- deficiencies / penalties
        {{ stg_int('NUMBER_OF_CITATIONS_FROM_INFECTION_CONTROL_INSPECTIONS') }}     as number_of_citations_from_infection_control_inspections,
        {{ stg_int('TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES') }}                        as total_number_of_health_deficiencies,
        {{ stg_int('TOTAL_NUMBER_OF_FIRE_SAFETY_DEFICIENCIES') }}                   as total_number_of_fire_safety_deficiencies,
        {{ stg_int('NUMBER_OF_FINES') }}                                            as number_of_fines,
        {{ stg_float('TOTAL_AMOUNT_OF_FINES_IN_DOLLARS') }}                           as total_amount_of_fines_in_dollars,
        {{ stg_int('NUMBER_OF_PAYMENT_DENIALS') }}                                  as number_of_payment_denials,
        {{ stg_int('TOTAL_NUMBER_OF_PENALTIES') }}                                  as total_number_of_penalties,

        -- metadata
        current_timestamp()                                                       as _ingested_at,
        _SOURCE_RUN_ID                                                             as _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by coalesce(cms_certification_number_ccn, provider_number)
        order by processing_date desc nulls last
    ) = 1

)

select * from deduped
