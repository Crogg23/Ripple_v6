{{ config(materialized='table', schema='HEALTH') }}

-- Source: FED_CMS_HOME_HEALTH_OWNERS (101,188 rows, landed 2026-09-07 for docket E74)
-- Grain: one row per (enrollment, owner, role); checked unique on landing 2026-09-07.
-- CCN comes from FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS on ENROLLMENT_ID (unique there,
-- so the join cannot fan out). 11,224 of 11,494 owner-file enrollments hit; the rest are
-- agencies not in the current enrollment snapshot and carry a null ccn.
-- REIT_OWNER is 'N' on every org row in this vintage: a constant, not a signal.
-- Flags are NULL on individual (type_owner = 'I') rows; only orgs carry them.

with owners as (
    select * from {{ ref('stg_fed_cms_home_health_owners__records') }}
),

enrollments as (
    select enrollment_id, ccn, npi, state as agency_state
    from {{ ref('stg_fed_cms_home_health_agency_enrollments__records') }}
),

flagged as (
    select
        o.enrollment_id,
        o.associate_id,
        o.organization_name,
        e.ccn,
        e.npi,
        e.agency_state,
        o.associate_id_owner,
        o.type_owner,
        iff(o.type_owner = 'O', 'organization', 'individual') as owner_kind,
        o.role_code_owner,
        o.role_text_owner,
        try_to_date(o.association_date_owner, 'MM/DD/YYYY') as association_date_owner,
        o.first_name_owner,
        o.middle_name_owner,
        o.last_name_owner,
        o.title_owner,
        o.organization_name_owner,
        o.doing_business_as_name_owner,
        -- Snowflake concat_ws returns NULL when ANY part is NULL; most people have no
        -- middle name, so each part is coalesced to '' first. (First build lost 49,827 names.)
        coalesce(o.organization_name_owner,
                 nullif(trim(regexp_replace(concat_ws(' ',
                     coalesce(o.first_name_owner, ''),
                     coalesce(o.middle_name_owner, ''),
                     coalesce(o.last_name_owner, '')), ' +', ' ')), '')
        ) as owner_name,
        o.address_line_1_owner,
        o.address_line_2_owner,
        o.city_owner,
        o.state_owner,
        o.zip_code_owner,
        try_to_double(o.percentage_ownership) as percentage_ownership,
        o.created_for_acquisition_owner = 'Y' as is_created_for_acquisition,
        o.corporation_owner = 'Y' as is_corporation,
        o.llc_owner = 'Y' as is_llc,
        o.medical_provider_supplier_owner = 'Y' as is_medical_provider_supplier,
        o.management_services_company_owner = 'Y' as is_management_services_company,
        o.medical_staffing_company_owner = 'Y' as is_medical_staffing_company,
        o.holding_company_owner = 'Y' as is_holding_company,
        o.investment_firm_owner = 'Y' as is_investment_firm,
        o.financial_institution_owner = 'Y' as is_financial_institution,
        o.consulting_firm_owner = 'Y' as is_consulting_firm,
        o.for_profit_owner = 'Y' as is_for_profit,
        o.non_profit_owner = 'Y' as is_non_profit,
        o.private_equity_company_owner = 'Y' as is_private_equity,
        o.reit_owner = 'Y' as is_reit,
        o.chain_home_office_owner = 'Y' as is_chain_home_office,
        o.other_type_owner = 'Y' as is_other_type,
        o.other_type_text_owner,
        o.owned_by_another_org_or_ind_owner = 'Y' as is_owned_by_another,
        o._loaded_at,
        o._source_run_id
    from owners o
    left join enrollments e on e.enrollment_id = o.enrollment_id
)

select * from flagged
