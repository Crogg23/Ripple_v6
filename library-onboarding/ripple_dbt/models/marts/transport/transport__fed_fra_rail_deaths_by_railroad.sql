{{ config(materialized='table', schema='TRANSPORT') }}

-- Built 2026-08-09: rail deaths by railroad and year from FRA Form 55a
-- casualty reports (1975-present). Built on the casualty table, NOT the
-- equipment-accident table, because casualties are one row per person per
-- report key (verified unique) — no multi-railroad double-counting.
-- Each death is attributed to the railroad that reported it.
-- 12 rows carry a two-digit report year ('20'); normalized to 2020, inside
-- the landed range.
-- Grain: one row = railroad x year x type of person killed.

with staged as (
    select * from {{ ref('stg_fed_fra_casualties__all') }}
    where fatality = 'Yes'
)

select
    railroad_code,
    max(railroad_name)                                       as railroad_name,
    max(reporting_parent_railroad_code)                      as parent_railroad_code,
    max(reporting_parent_railroad_name)                      as parent_railroad_name,
    max(reporting_railroad_holding_company)                  as holding_company,
    case when incident_year < 100 then incident_year + 2000
         else incident_year end                              as incident_year,
    type_of_person,
    count(*)                                                 as deaths,
    max(_ingested_at)                                        as _ingested_at
from staged
group by railroad_code,
         case when incident_year < 100 then incident_year + 2000
              else incident_year end,
         type_of_person
