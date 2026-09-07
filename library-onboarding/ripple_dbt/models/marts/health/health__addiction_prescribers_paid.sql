{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per Part D prescriber of an addiction drug, DY2022.
-- Docket line 4. Built 2026-09-07 from reports/dead_ends_scope_A_bridges_2026-09-07.md.
--
-- The docket had this line as "the two records don't line up": the opioid
-- treatment program file (org NPIs) against Part D (person NPIs). Orgs do not
-- prescribe. The scope report swapped the OTP table for a drug filter on the
-- Part D by-provider-and-drug file, and the join to Open Payments is then
-- NPI = NPI. This mart is that join.
--
-- Left side: LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG, DY2022, one load, one
-- year, no year column (trap 2026-08-31). "Addiction drug" = generic name
-- contains buprenorphine, naltrexone or methadone. Same three words the scope
-- used. Rows with under 11 claims are already gone from the CMS file, so
-- every claim count here is a floor.
-- Right side: HEALTH__FED_CMS_OPEN_PAYMENTS_2022, PY2022, same year. Blank
-- NPI is '' not null (trap 2026-09-05) and is dropped before the join.
--
-- Scope numbers to hold this against: 44,846 prescribers, 26,645 paid (59%).
--
-- STILL TRUE: one year each side. This is targeting, not before/after.
-- "Paid" includes every nature of payment: food, travel, consulting, royalties.
-- Split by nature before naming anyone.

with partd as (

    select
        "Prscrbr_NPI"                                          as npi,
        max("Prscrbr_Last_Org_Name")                           as last_name,
        max("Prscrbr_First_Name")                              as first_name,
        max("Prscrbr_State_Abrvtn")                            as state,
        max("Prscrbr_Type")                                    as prescriber_type,
        sum({{ ripple_num('"Tot_Clms"') }})                    as addiction_claims,
        sum({{ ripple_num('"Tot_Drug_Cst"') }})                as addiction_drug_cost,
        count(distinct "Gnrc_Name")                            as addiction_drug_count,
        listagg(distinct "Gnrc_Name", ' | ') within group (order by "Gnrc_Name")
                                                               as addiction_drugs
    from {{ source('ripple_raw', 'FED_CMS_PARTD_PRESCRIBER_DRUG') }}
    where ("Gnrc_Name" ilike '%buprenorphine%'
       or "Gnrc_Name" ilike '%naltrexone%'
       or "Gnrc_Name" ilike '%methadone%')
      -- not addiction drugs: methylnaltrexone is for constipation,
      -- naltrexone/bupropion is Contrave for weight loss
      and "Gnrc_Name" not ilike '%methylnaltrexone%'
      and "Gnrc_Name" not ilike '%bupropion%'
    group by 1

),

payments as (

    select
        npi,
        sum(total_amount_of_payment_usdollars)                 as total_payments,
        count(*)                                               as payment_count,
        count(distinct applicable_manufacturer_or_applicable_gpo_making_payment_name)
                                                               as manufacturer_count
    from {{ ref('health__fed_cms_open_payments_2022') }}
    where nullif(trim(npi), '') is not null
    group by 1

),

-- the manufacturer that paid the most dollars to this NPI in PY2022.
-- Payer names split on case ('ABBVIE INC.' / 'AbbVie Inc.'); folded to upper.
top_manufacturer as (

    select
        npi,
        upper(trim(applicable_manufacturer_or_applicable_gpo_making_payment_name))
                                                               as top_manufacturer,
        sum(total_amount_of_payment_usdollars)                 as top_manufacturer_payments
    from {{ ref('health__fed_cms_open_payments_2022') }}
    where nullif(trim(npi), '') is not null
    group by 1, 2
    qualify row_number() over (partition by npi order by top_manufacturer_payments desc nulls last, top_manufacturer) = 1

)

select
    p.npi,
    p.last_name,
    p.first_name,
    p.last_name || ', ' || p.first_name                        as prescriber_name,
    p.state,
    p.prescriber_type,
    p.addiction_claims,
    p.addiction_drug_cost,
    p.addiction_drug_count,
    p.addiction_drugs,
    (pay.npi is not null)                                      as was_paid_2022,
    coalesce(pay.total_payments, 0)                            as total_payments,
    coalesce(pay.payment_count, 0)                             as payment_count,
    coalesce(pay.manufacturer_count, 0)                        as manufacturer_count,
    tm.top_manufacturer,
    tm.top_manufacturer_payments,
    2022                                                       as data_year
from partd p
left join payments pay
    on pay.npi = p.npi
left join top_manufacturer tm
    on tm.npi = p.npi
