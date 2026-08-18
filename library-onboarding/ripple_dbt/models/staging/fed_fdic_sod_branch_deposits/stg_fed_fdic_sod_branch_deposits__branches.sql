{{ config(materialized='view') }}

/*
  Generated 2026-08-10 (backlog wave 4).
  FDIC Summary of Deposits (SOD): full annual survey history 1994-2025 of every
  FDIC-insured bank branch and its deposits. 2,823,000 rows.
  Grain (verified live by orchestrator): one row = one branch (CERT + BRNUM)
  in one survey YEAR. Concatenated branch_year_key is tested unique.
  Columns with a *BR suffix in the source describe the BRANCH; unsuffixed
  counterparts describe the parent INSTITUTION.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_FDIC_SOD_BRANCH_DEPOSITS') }}
),

renamed as (
    select
        -- surrogate key: survey year + FDIC cert + branch number (verified unique)
        nullif(trim(YEAR), '') || '-' || nullif(trim(CERT), '') || '-' || nullif(trim(BRNUM), '')
                                                                   as branch_year_key,

        -- identifiers
        try_to_number(nullif(trim(YEAR), ''))                      as survey_year,
        nullif(trim(CERT), '')                                     as fdic_cert,
        nullif(trim(BRNUM), '')                                    as branch_number,
        nullif(trim(UNINUMBR), '')                                 as branch_uninum,
        nullif(trim(ID), '')                                       as record_id,
        nullif(trim(RSSDID), '')                                   as rssd_id,
        nullif(trim(RSSDHCR), '')                                  as holding_company_rssd,
        nullif(trim(DOCKET), '')                                   as ots_docket,

        -- branch attributes (*BR-suffixed source columns)
        nullif(trim(NAMEBR), '')                                   as branch_name,
        nullif(trim(ADDRESBR), '')                                 as branch_address,
        nullif(trim(CITYBR), '')                                   as branch_city,
        nullif(trim(CITY2BR), '')                                  as branch_city_alt,
        nullif(trim(STALPBR), '')                                  as branch_state,
        nullif(trim(STNAMEBR), '')                                 as branch_state_name,
        nullif(trim(ZIPBR), '')                                    as branch_zip,
        nullif(trim(STNUMBR), '')                                  as branch_state_fips,
        nullif(trim(CNTYNUMB), '')                                 as branch_county_fips,
        nullif(trim(CNTYNAMB), '')                                 as branch_county_name,
        nullif(trim(STCNTYBR), '')                                 as branch_state_county_fips,
        nullif(trim(CNTRYNAB), '')                                 as branch_country,
        nullif(trim(PLACENUM), '')                                 as branch_place_code,
        nullif(trim(MSABR), '')                                    as branch_msa_code,
        nullif(trim(MSANAMB), '')                                  as branch_msa_name,
        nullif(trim(CSABR), '')                                    as branch_csa_code,
        nullif(trim(CSANAMBR), '')                                 as branch_csa_name,
        nullif(trim(DIVISIONB), '')                                as branch_cbsa_division_code,
        nullif(trim(CBSA_DIV_NAMB), '')                            as branch_cbsa_division_name,
        nullif(trim(NECTABR), '')                                  as branch_necta_code,
        nullif(trim(NECNAMB), '')                                  as branch_necta_name,
        nullif(trim(METROBR), '')                                  as branch_metro_flag,
        nullif(trim(MICROBR), '')                                  as branch_micro_flag,
        nullif(trim(BRSERTYP), '')                                 as branch_service_type,
        nullif(trim(BRCENM), '')                                   as branch_deposit_reporting_method,
        nullif(trim(BKMO), '')                                     as main_office_flag,
        try_to_number(nullif(trim(DEPSUMBR), ''))                  as branch_deposits_thousands,

        -- branch geocoding (FDIC SIMS)
        -- NOT A BUG (epoch-1970 investigation, 2026-08-18): sims_established_date
        -- already uses an explicit 'MM/DD/YYYY' format, so it never fell into the
        -- bare-try_to_date epoch trap. Its 26,581-of-2.82M (0.9%) 1970 rows
        -- (confirmed live) spread across many distinct 1970 days -- real bank
        -- branches established that year, not sentinel garbage. Left as-is.
        try_to_double(nullif(trim(SIMS_LATITUDE), ''))             as sims_latitude,
        try_to_double(nullif(trim(SIMS_LONGITUDE), ''))            as sims_longitude,
        nullif(trim(SIMS_PROJECTION), '')                          as sims_projection,
        nullif(trim(SIMS_DESCRIPTION), '')                         as sims_description,
        try_to_date(split_part(nullif(trim(SIMS_ACQUIRED_DATE), ''), ' ', 1), 'MM/DD/YYYY')
                                                                   as sims_acquired_date,
        try_to_date(split_part(nullif(trim(SIMS_ESTABLISHED_DATE), ''), ' ', 1), 'MM/DD/YYYY')
                                                                   as sims_established_date,

        -- parent institution attributes (unsuffixed source columns)
        nullif(trim(NAMEFULL), '')                                 as institution_name,
        nullif(trim(ADDRESS), '')                                  as institution_address,
        nullif(trim(CITY), '')                                     as institution_city,
        nullif(trim(STALP), '')                                    as institution_state,
        nullif(trim(STNAME), '')                                   as institution_state_name,
        nullif(trim(ZIP), '')                                      as institution_zip,
        nullif(trim(STCNTY), '')                                   as institution_state_county_fips,
        nullif(trim(CNTRYNA), '')                                  as institution_country,
        try_to_number(nullif(trim(ASSET), ''))                     as institution_assets_thousands,
        try_to_number(nullif(trim(DEPSUM), ''))                    as institution_deposits_thousands,
        try_to_number(nullif(trim(DEPDOM), ''))                    as institution_domestic_deposits_thousands,
        try_to_number(nullif(trim(INSBRDD), ''))                   as insured_branch_demand_deposits_thousands,
        try_to_number(nullif(trim(INSBRTS), ''))                   as insured_branch_time_savings_deposits_thousands,
        try_to_number(nullif(trim(ESCROW), ''))                    as escrow_deposits_thousands,
        nullif(trim(BKCLASS), '')                                  as bank_class,
        nullif(trim(CLCODE), '')                                   as class_code,
        nullif(trim(CHARTER), '')                                  as charter_type,
        nullif(trim(CHRTAGNT), '')                                 as charter_agency,
        nullif(trim(CHRTAGNN), '')                                 as charter_agency_name,
        nullif(trim(CB), '')                                       as community_bank_flag,
        nullif(trim(INSURED), '')                                  as insured_status,
        nullif(trim(INSAGNT1), '')                                 as insurance_agency,
        nullif(trim(REGAGNT), '')                                  as regulator,
        nullif(trim(CALL), '')                                     as call_report_code,
        nullif(trim(FED), '')                                      as fed_district_code,
        nullif(trim(FEDNAME), '')                                  as fed_district_name,
        nullif(trim(FDICDBS), '')                                  as fdic_region_code,
        nullif(trim(FDICNAME), '')                                 as fdic_region_name,
        nullif(trim(OCCDIST), '')                                  as occ_district_code,
        nullif(trim(OCCNAME), '')                                  as occ_district_name,
        nullif(trim(SPECGRP), '')                                  as specialization_group_code,
        nullif(trim(SPECDESC), '')                                 as specialization_group_desc,
        nullif(trim(HCTMULT), '')                                  as multibank_holding_flag,
        nullif(trim(NAMEHCR), '')                                  as holding_company_name,
        nullif(trim(CITYHCR), '')                                  as holding_company_city,
        nullif(trim(STALPHCR), '')                                 as holding_company_state,
        nullif(trim(DENOVO), '')                                   as denovo_flag,
        nullif(trim(CONSOLD), '')                                  as consolidated_reporting_code,
        nullif(trim(UNIT), '')                                     as unit_bank_flag,
        nullif(trim(USA), '')                                      as domestic_flag,

        -- metadata
        try_to_timestamp(nullif(trim(_INGESTED_AT), ''))           as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                           as _source_run_id,
        nullif(trim(_SRC_SHA256), '')                              as _src_sha256
    from source
)

select * from renamed
