{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_cms_nursing_home__nursing_home_facilities') }}

)

select

    -- -----------------------------------------------------------------------
    -- Key identifiers (exposed for cross-source joins)
    -- -----------------------------------------------------------------------
    cms_certification_number_ccn,
    provider_number,
    npi,
    county_fips,
    provider_ssa_county_code,
    state,
    zip_code,

    -- -----------------------------------------------------------------------
    -- Provider identity
    -- -----------------------------------------------------------------------
    provider_name,
    legal_business_name,
    provider_type,
    ownership_type,

    -- -----------------------------------------------------------------------
    -- Address / geography
    -- -----------------------------------------------------------------------
    coalesce(provider_address, address)                                     as address,
    coalesce(city_town, city)                                               as city,
    county_parish,
    urban,
    location,
    latitude,
    longitude,
    geocoding_footnote,

    -- -----------------------------------------------------------------------
    -- Contact
    -- -----------------------------------------------------------------------
    coalesce(telephone_number, phone_number)                                as phone_number,

    -- -----------------------------------------------------------------------
    -- Certification / key dates
    -- -----------------------------------------------------------------------
    date_first_approved_to_provide_medicare_and_medicaid_services,
    date_of_most_recent_health_inspection,
    processing_date,

    -- -----------------------------------------------------------------------
    -- Facility flags
    -- -----------------------------------------------------------------------
    provider_resides_in_hospital,
    continuing_care_retirement_community,
    special_focus_status,
    abuse_icon,
    most_recent_health_inspection_more_than_2_years_ago,
    provider_changed_ownership_in_last_12_months,
    with_a_resident_and_family_council,
    automatic_sprinkler_systems_in_all_required_areas,

    -- -----------------------------------------------------------------------
    -- Capacity / census
    -- -----------------------------------------------------------------------
    number_of_certified_beds,
    average_number_of_residents_per_day,
    number_of_residents_in_certified_beds,

    -- -----------------------------------------------------------------------
    -- Chain
    -- -----------------------------------------------------------------------
    chain_name,
    chain_id,
    number_of_facilities_in_chain,
    chain_average_overall_5_star_rating,
    chain_average_health_inspection_rating,
    chain_average_staffing_rating,
    chain_average_qm_rating,

    -- -----------------------------------------------------------------------
    -- Star ratings
    -- -----------------------------------------------------------------------
    overall_rating,
    health_inspection_rating,
    quality_measure_rating,
    long_stay_qm_rating,
    short_stay_qm_rating,
    staffing_rating,

    -- -----------------------------------------------------------------------
    -- Staffing hours (reported)
    -- -----------------------------------------------------------------------
    reported_nurse_aide_staffing_hours_per_resident_per_day,
    reported_lpn_staffing_hours_per_resident_per_day,
    reported_rn_staffing_hours_per_resident_per_day,
    reported_licensed_staffing_hours_per_resident_per_day,
    reported_total_nurse_staffing_hours_per_resident_per_day,
    total_number_of_nurse_staff_hours_per_resident_per_day_on_the_weekend,
    registered_nurse_hours_per_resident_per_day_on_the_weekend,
    reported_physical_therapist_staffing_hours_per_resident_per_day,

    -- -----------------------------------------------------------------------
    -- Staffing hours (case-mix adjusted)
    -- -----------------------------------------------------------------------
    nursing_case_mix_index,
    nursing_case_mix_index_ratio,
    case_mix_nurse_aide_staffing_hours_per_resident_per_day,
    case_mix_lpn_staffing_hours_per_resident_per_day,
    case_mix_rn_staffing_hours_per_resident_per_day,
    case_mix_total_nurse_staffing_hours_per_resident_per_day,
    case_mix_weekend_total_nurse_staffing_hours_per_resident_per_day,
    adjusted_nurse_aide_staffing_hours_per_resident_per_day,
    adjusted_lpn_staffing_hours_per_resident_per_day,
    adjusted_rn_staffing_hours_per_resident_per_day,
    adjusted_total_nurse_staffing_hours_per_resident_per_day,
    adjusted_weekend_total_nurse_staffing_hours_per_resident_per_day,

    -- -----------------------------------------------------------------------
    -- Turnover
    -- -----------------------------------------------------------------------
    total_nursing_staff_turnover,
    registered_nurse_turnover,
    number_of_administrators_who_have_left_the_nursing_home,

    -- -----------------------------------------------------------------------
    -- Health survey scores
    -- -----------------------------------------------------------------------
    rating_cycle_1_standard_survey_health_date,
    rating_cycle_1_total_number_of_health_deficiencies,
    rating_cycle_1_number_of_standard_health_deficiencies,
    rating_cycle_1_number_of_complaint_health_deficiencies,
    rating_cycle_1_health_deficiency_score,
    rating_cycle_1_number_of_health_revisits,
    rating_cycle_1_health_revisit_score,
    rating_cycle_1_total_health_score,
    rating_cycle_2_standard_health_survey_date,
    rating_cycle_2_3_total_number_of_health_deficiencies,
    rating_cycle_2_number_of_standard_health_deficiencies,
    rating_cycle_2_3_number_of_complaint_health_deficiencies,
    rating_cycle_2_3_health_deficiency_score,
    rating_cycle_2_3_number_of_health_revisits,
    rating_cycle_2_3_health_revisit_score,
    rating_cycle_2_3_total_health_score,
    total_weighted_health_survey_score,

    -- -----------------------------------------------------------------------
    -- Deficiencies & penalties
    -- -----------------------------------------------------------------------
    number_of_citations_from_infection_control_inspections,
    total_number_of_health_deficiencies,
    total_number_of_fire_safety_deficiencies,
    number_of_fines,
    total_amount_of_fines_in_dollars,
    number_of_payment_denials,
    total_number_of_penalties,

    -- -----------------------------------------------------------------------
    -- Derived convenience fields
    -- -----------------------------------------------------------------------
    case
        when overall_rating >= 4 then 'High (4-5 stars)'
        when overall_rating = 3  then 'Average (3 stars)'
        when overall_rating <= 2 then 'Low (1-2 stars)'
        else 'Not Rated'
    end                                                                     as overall_rating_band,

    case
        when total_amount_of_fines_in_dollars > 0 then true
        else false
    end                                                                     as has_financial_penalty,

    -- -----------------------------------------------------------------------
    -- Metadata
    -- -----------------------------------------------------------------------
    _ingested_at,
    _source_run_id

from base
