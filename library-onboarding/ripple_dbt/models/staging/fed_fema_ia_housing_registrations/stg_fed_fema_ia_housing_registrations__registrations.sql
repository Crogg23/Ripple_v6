{{ config(materialized='view') }}

-- GRAIN: one row = one valid FEMA Individual Assistance housing registration
-- (OpenFEMA "Individuals and Households Program - Valid Registrations" large-disasters
-- dataset). registration_id (source ID) is exactly unique: 3,080,000 distinct of
-- 3,080,000 rows (verified). NOTE: that suspiciously round row count suggests this
-- may be a bounded slice of the full OpenFEMA dataset (millions more exist) --
-- pending re-check against the source.

with source as (

    select * from {{ source('ripple_raw', 'FED_FEMA_IA_HOUSING_REGISTRATIONS') }}

),

renamed as (

    select

        -- identifiers
        trim(ID)                                        as registration_id,
        trim(DISASTERNUMBER)                            as disaster_number,

        -- registration / disaster context
        try_to_date(trim(APPLIEDDATE))                  as applied_date,
        try_to_date(trim(DECLARATIONDATE))              as declaration_date,
        trim(INCIDENTTYPECODE)                          as incident_type_code,
        trim(REGISTRATIONMETHOD)                        as registration_method,

        -- location
        trim(COUNTY)                                    as county,
        trim(DAMAGEDCITY)                               as damaged_city,
        trim(DAMAGEDSTATEABBREVIATION)                  as damaged_state_abbreviation,
        trim(DAMAGEDZIPCODE)                            as damaged_zip_code,
        trim(FIPS)                                      as fips,
        trim(CENSUSGEOID)                               as census_geoid,
        trim(CENSUSYEAR)                                as census_year,
        trim(CURRENTLOCATION)                           as current_location,
        trim(HIGHWATERLOCATION)                         as high_water_location,

        -- household
        trim(APPLICANTAGE)                              as applicant_age,
        trim(HOUSEHOLDCOMPOSITION)                      as household_composition,
        try_to_number(trim(OCCUPANTSUNDERTWO))          as occupants_under_two,
        try_to_number(trim(OCCUPANTS2TO5))              as occupants_2_to_5,
        try_to_number(trim(OCCUPANTS6TO18))             as occupants_6_to_18,
        try_to_number(trim(OCCUPANTS19TO64))            as occupants_19_to_64,
        try_to_number(trim(OCCUPANTS65ANDOVER))         as occupants_65_and_over,
        try_to_number(trim(GROSSINCOME))                as gross_income,
        trim(ACCESSFUNCTIONALNEEDS)                     as access_functional_needs,
        trim(OWNRENT)                                   as own_rent,
        trim(PRIMARYRESIDENCE)                          as primary_residence,
        trim(RESIDENCETYPE)                             as residence_type,

        -- needs at registration
        trim(EMERGENCYNEEDS)                            as emergency_needs,
        trim(FOODNEED)                                  as food_need,
        trim(SHELTERNEED)                               as shelter_need,
        trim(UTILITIESOUT)                              as utilities_out,

        -- damage
        trim(HOMEDAMAGE)                                as home_damage,
        trim(AUTODAMAGE)                                as auto_damage,
        trim(DESTROYED)                                 as destroyed,
        trim(REPORTEDDAMAGE)                            as reported_damage,
        trim(FLOODDAMAGE)                               as flood_damage,
        try_to_number(trim(FLOODDAMAGEAMOUNT))          as flood_damage_amount,
        trim(FOUNDATIONDAMAGE)                          as foundation_damage,
        try_to_number(trim(FOUNDATIONDAMAGEAMOUNT))     as foundation_damage_amount,
        trim(ROOFDAMAGE)                                as roof_damage,
        try_to_number(trim(ROOFDAMAGEAMOUNT))           as roof_damage_amount,
        try_to_number(trim(WATERLEVEL))                 as water_level,
        trim(RENTERDAMAGELEVEL)                         as renter_damage_level,
        trim(HABITABILITYREPAIRSREQUIRED)               as habitability_repairs_required,
        trim(INSUFFICIENTDAMAGE)                        as insufficient_damage,
        trim(SELFASSESSMENTINFORMATION)                 as self_assessment_information,

        -- inspection / verification
        trim(INSPNISSUED)                               as inspn_issued,
        trim(INSPNRETURNED)                             as inspn_returned,
        trim(VERIFIEDOCCUPANCY)                         as verified_occupancy,
        trim(VERIFIEDOWNERSHIP)                         as verified_ownership,
        try_to_number(trim(PPFVL))                      as ppfvl,
        try_to_number(trim(RPFVL))                      as rpfvl,

        -- insurance
        trim(FLOODINSURANCE)                            as flood_insurance,
        trim(HOMEOWNERSINSURANCE)                       as homeowners_insurance,
        trim(INELIGIBLEINSURANCE)                       as ineligible_insurance,
        trim(INELIGIBLEREASON)                          as ineligible_reason,

        -- IHP (Individuals and Households Program) totals
        trim(IHPELIGIBLE)                               as ihp_eligible,
        try_to_number(trim(IHPAMOUNT))                  as ihp_amount,
        try_to_number(trim(IHPMAX))                     as ihp_max,
        trim(IHPREFERRAL)                               as ihp_referral,

        -- HA (Housing Assistance)
        trim(HAELIGIBLE)                                as ha_eligible,
        try_to_number(trim(HAAMOUNT))                   as ha_amount,
        try_to_number(trim(HAMAX))                      as ha_max,
        trim(HAREFERRAL)                                as ha_referral,
        trim(HASTATUS)                                  as ha_status,

        -- FIP (Flood Insurance Purchase)
        try_to_number(trim(FIPAMOUNT))                  as fip_amount,

        -- repair / replacement / rental assistance
        trim(REPAIRASSISTANCEELIGIBLE)                  as repair_assistance_eligible,
        try_to_number(trim(REPAIRAMOUNT))               as repair_amount,
        trim(REPLACEMENTASSISTANCEELIGIBLE)             as replacement_assistance_eligible,
        try_to_number(trim(REPLACEMENTAMOUNT))          as replacement_amount,
        trim(RENTALASSISTANCEELIGIBLE)                  as rental_assistance_eligible,
        try_to_number(trim(RENTALASSISTANCEAMOUNT))     as rental_assistance_amount,
        try_to_date(trim(RENTALASSISTANCEENDDATE))      as rental_assistance_end_date,
        trim(RENTALRESOURCECITY)                        as rental_resource_city,
        trim(RENTALRESOURCESTATEABBREV)                 as rental_resource_state_abbrev,
        trim(RENTALRESOURCEZIPCODE)                     as rental_resource_zip_code,

        -- ONA (Other Needs Assistance)
        trim(ONAELIGIBLE)                               as ona_eligible,
        try_to_number(trim(ONAAMOUNT))                  as ona_amount,
        try_to_number(trim(ONAMAX))                     as ona_max,
        trim(ONAREFERRAL)                               as ona_referral,
        trim(ONADENTALASSISTELIGIBLE)                   as ona_dental_assist_eligible,
        try_to_number(trim(ONADENTALASSISTAMOUNT))      as ona_dental_assist_amount,
        trim(ONAFUNERALASSISTELIGIBLE)                  as ona_funeral_assist_eligible,
        try_to_number(trim(ONAFUNERALASSISTAMOUNT))     as ona_funeral_assist_amount,
        trim(ONAMEDICALASSISTELIGIBLE)                  as ona_medical_assist_eligible,
        try_to_number(trim(ONAMEDICALASSISTAMOUNT))     as ona_medical_assist_amount,
        trim(ONAMOVINGASSISTELIGIBLE)                   as ona_moving_assist_eligible,
        try_to_number(trim(ONAMOVINGASSISTAMOUNT))      as ona_moving_assist_amount,
        trim(ONAOTHERASSISTELIGIBLE)                    as ona_other_assist_eligible,
        try_to_number(trim(ONAOTHERASSISTAMOUNT))       as ona_other_assist_amount,

        -- personal property / unmet need
        trim(PERSONALPROPERTYELIGIBLE)                  as personal_property_eligible,
        try_to_number(trim(PERSONALPROPERTYAMOUNT))     as personal_property_amount,
        try_to_number(trim(UNMETNEEDPP))                as unmet_need_pp,
        try_to_number(trim(UNMETNEEDRP))                as unmet_need_rp,

        -- transient accommodation / TSA / SBA
        trim(TRANSIENTACCOMMODELIGIBLE)                 as transient_accommod_eligible,
        try_to_number(trim(TRANSIENTACCOMMODAMOUNT))    as transient_accommod_amount,
        trim(TSAELIGIBLE)                               as tsa_eligible,
        trim(TSACHECKEDIN)                              as tsa_checked_in,
        trim(SBAAPPROVED)                               as sba_approved,

        -- source refresh
        trim(LASTREFRESH)                               as last_refresh,

        -- metadata
        _ingested_at,
        _source_run_id,
        _src_sha256

    from source

)

select * from renamed
where registration_id is not null
