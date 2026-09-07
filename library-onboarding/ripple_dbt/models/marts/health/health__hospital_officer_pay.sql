{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per person per hospital Form 990 return (object_id, person_seq).
-- Docket line 124. Built 2026-09-07 from reports/dead_ends_scope_B_parsers_2026-09-07.md.
--
-- Left side: Part VII Section A rows parsed from the IRS e-file XML for
-- every full-form 990 in the index whose EIN sits in BMF with NTEE E2x
-- (hospitals). Right side: BMF, one row per EIN, for the hospital's name,
-- city, state and the org-level asset / revenue figures. BMF is a current
-- snapshot, so name and totals are today's, not the return year's.
--
-- Reachable returns only. The IRS hosts XML for object-id years 2019 on;
-- 2016-2018 index rows (7,847 hospital returns) have no download any more,
-- so tax years before roughly 2017 are thin or absent here.
--
-- total_compensation = from org + from related orgs + other. Part VII lists
-- every director and trustee too, most at $0; filter is_officer / is_key_employee
-- / is_highest_compensated or total_compensation > 0 before ranking anyone.
-- Names are as typed on the return: case varies, DR and MD get mixed in.

with pay as (

    select * from {{ ref('stg_fed_irs_990_officer_pay__people') }}

),

bmf as (

    select
        lpad(trim(ein), 9, '0')                                as ein,
        name                                                   as hospital_name,
        city                                                   as hospital_city,
        state                                                  as hospital_state,
        ntee_cd                                                as ntee_code,
        {{ ripple_num('asset_amt') }}                          as bmf_asset_amt,
        {{ ripple_num('revenue_amt') }}                        as bmf_revenue_amt
    from {{ ref('stg_fed_irs_bmf__organizations') }}

)

select
    p.object_id,
    p.person_seq,
    p.ein,
    coalesce(b.hospital_name, p.filer_name)                    as hospital_name,
    p.filer_name,
    b.hospital_city,
    b.hospital_state,
    b.ntee_code,
    p.tax_year,
    p.tax_period_end,
    p.person_name,
    p.title,
    -- A second Part VII line for the same person whose title points at
    -- Schedule J ("SEE SCH J, PART III"). Its dollars restate a payout, not a
    -- second job. 239 person-returns carry one; rank on rows where this is
    -- false or the top figure is the pointer line (skeptic, 2026-09-07).
    regexp_like(upper(coalesce(p.title, '')), '.*(SEE SCH|SCH J|SCHEDULE J).*') as is_schedule_j_pointer,
    regexp_like(upper(coalesce(p.person_name, '')), '.*GROUP RETURN.*')          as is_group_return,
    p.avg_hours_per_week,
    p.avg_hours_per_week_related_org,
    p.is_trustee_or_director,
    p.is_institutional_trustee,
    p.is_officer,
    p.is_key_employee,
    p.is_highest_compensated,
    p.is_former,
    p.reportable_comp_from_org,
    p.reportable_comp_from_related_orgs,
    p.other_compensation,
    coalesce(p.reportable_comp_from_org, 0)
      + coalesce(p.reportable_comp_from_related_orgs, 0)
      + coalesce(p.other_compensation, 0)                      as total_compensation,
    b.bmf_asset_amt,
    b.bmf_revenue_amt,
    p.schema_version,
    p.source_zip,
    p._loaded_at,
    p._source_url
from pay p
left join bmf b
    on b.ein = p.ein
