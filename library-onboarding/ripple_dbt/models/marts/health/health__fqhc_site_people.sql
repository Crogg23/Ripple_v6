{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per (person NPI, FQHC site) pair.
-- Docket line 7. Built 2026-09-07 from reports/dead_ends_scope_A_bridges_2026-09-07.md.
--
-- The docket had this line as "can't currently tell which doctor works where."
-- No landed table puts a person inside an FQHC: FACILITY_AFFILIATION stops at
-- hospitals and post-acute, PECOS never pairs a person with an org, and the
-- UDS site NPI is the clinic's own org NPI. What is landed is the NPPES
-- practice address. This mart is an ADDRESS BRIDGE: an NPPES person whose
-- practice street line and 5-digit ZIP equal a UDS site's street line and ZIP.
--
-- Then each pair is flagged against LEIE (by NPI, real NPIs only; LEIE carries
-- a real NPI on 10% of rows, so every hit count is a floor) and against the
-- opt-out affidavit file (by NPI; the file is a live snapshot with duplicate
-- NPI rows, collapsed to one per NPI here).
--
-- Scope numbers to hold this against: 173,813 people at 11,110 of 19,038
-- sites; 90 LEIE people at 114 sites. The scope's opt-out figure (75) was an
-- address join from the opt-out file's own address, not an NPI flag; this
-- mart flags by NPI, so the number will differ.
--
-- STILL TRUE, marked as bad news in the scope: every NPPES address predates
-- its exclusion. match_note says so, row by row. This is "listed an FQHC as
-- their practice when NPPES was last updated", a lead list, never a headline.
-- Address-leak trap: shared campuses (hospitals, county buildings) fan out
-- to hundreds of people. people_at_site is on every row so a reader can cap it;
-- 142 sites carry 200+ people, median is 5.

with sites as (

    select
        bphc_assigned_number,
        site_name,
        health_center_name,
        site_address,
        site_city,
        site_state_abbreviation                                as site_state,
        left(trim(site_postal_code), 5)                        as site_zip5,
        upper(trim(site_address))                              as addr_key
    from {{ ref('health__fed_hrsa_uds_service_delivery_sites') }}
    where nullif(trim(site_address), '') is not null
      and nullif(trim(site_postal_code), '') is not null

),

people as (

    select
        npi,
        provider_last_name_legal_name                          as last_name,
        provider_first_name                                    as first_name,
        provider_credential_text                               as credential,
        healthcare_provider_taxonomy_code_1                    as taxonomy_code_1,
        provider_first_line_business_practice_location_address as practice_address,
        provider_business_practice_location_address_city_name  as practice_city,
        provider_business_practice_location_address_state_name as practice_state,
        left(trim(provider_business_practice_location_address_postal_code), 5)
                                                               as practice_zip5,
        last_update_date                                       as nppes_last_update_date,
        npi_deactivation_date,
        upper(trim(provider_first_line_business_practice_location_address))
                                                               as addr_key
    from {{ ref('health__fed_cms_nppes') }}
    where entity_type_code = '1'
      and nullif(trim(provider_first_line_business_practice_location_address), '') is not null

),

pairs as (

    select
        p.*,
        s.bphc_assigned_number,
        s.site_name,
        s.health_center_name,
        s.site_address,
        s.site_city,
        s.site_state,
        s.site_zip5,
        count(*) over (partition by s.bphc_assigned_number)    as people_at_site
    from people p
    join sites s
        on s.addr_key  = p.addr_key
       and s.site_zip5 = p.practice_zip5

),

-- one LEIE row per real NPI: the earliest exclusion still on the list.
leie as (

    select
        npi,
        exclusion_date,
        exclusion_type,
        specialty                                              as leie_specialty
    from {{ ref('health__fed_hhs_oig_leie') }}
    where npi_is_real
    qualify row_number() over (partition by npi order by exclusion_date nulls last) = 1

),

-- one opt-out row per NPI: the latest end date.
opt_out as (

    select
        npi,
        optout_effective_date,
        optout_end_date
    from {{ ref('health__fed_cms_opt_out_affidavits') }}
    where nullif(trim(npi), '') is not null
    qualify row_number() over (partition by npi order by optout_end_date desc nulls last) = 1

)

select
    pr.npi,
    pr.last_name,
    pr.first_name,
    pr.credential,
    pr.taxonomy_code_1,
    pr.bphc_assigned_number,
    pr.site_name,
    pr.health_center_name,
    pr.site_address,
    pr.site_city,
    pr.site_state,
    pr.site_zip5,
    pr.people_at_site,
    pr.nppes_last_update_date,
    pr.npi_deactivation_date,
    (l.npi is not null)                                        as is_excluded,
    l.exclusion_date,
    l.exclusion_type,
    l.leie_specialty,
    (o.npi is not null)                                        as is_opted_out,
    o.optout_effective_date,
    o.optout_end_date,
    case
        when l.npi is null
            then 'address match only: street line + 5-digit ZIP'
        when pr.nppes_last_update_date is null
            then 'excluded; NPPES last update unknown, address may predate the exclusion'
        when pr.nppes_last_update_date < l.exclusion_date
            then 'excluded; NPPES address predates the exclusion (last update '
                 || to_varchar(pr.nppes_last_update_date) || ', excluded '
                 || to_varchar(l.exclusion_date) || ')'
        else 'excluded; NPPES address updated on or after the exclusion (last update '
                 || to_varchar(pr.nppes_last_update_date) || ', excluded '
                 || to_varchar(l.exclusion_date) || ')'
    end                                                        as match_note
from pairs pr
left join leie l
    on l.npi = pr.npi
left join opt_out o
    on o.npi = pr.npi
