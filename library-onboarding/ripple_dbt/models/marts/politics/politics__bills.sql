{{ config(materialized='table', schema='POLITICS') }}

-- One row per bill (congress, bill_type, bill_number). The objective bill facts that
-- the member box-score aggregates from. Mirrors politics/loaders/build_bills_leg.py.
--
-- DEFINITIONS (documented, definition-bound where noted):
--   is_law_eligible          bill_type in HR/S/HJRES/SJRES (can become law). HRES/SRES/
--                            HCONRES/SCONRES are resolutions -- they CANNOT become law and
--                            are NEVER in the enacted-rate denominator.
--   became_law               a <laws> element was present (public-law number) -- the clean
--                            enacted signal, NOT a status-string match.
--   advanced_past_committee  DOCUMENTED RULE: the action history carries any action type beyond
--                            the introduce-and-refer stage, i.e. type in {Committee, Calendars,
--                            Discharge, Floor, President, ResolvingDifferences, Veto, BecameLaw}.
--                            Counts a committee report/markup/hearing OR any later floor/calendar/
--                            presidential/enactment action. (IntroReferral alone = died in committee.)
--                            Slightly generous (includes hearings, not strictly reported-out).
--   latest_stage             coarse stage ladder derived from the GPO action-type taxonomy.

with base as (

    select * from {{ ref('stg_fed_govinfo_billstatus__bills') }}

),

-- DISTINCT cosponsors per bill (the deduped cosponsor staging is already one row per
-- (bill, cosponsor_bioguide)), so a count here matches POLITICS__BILL_COSPONSORS exactly --
-- unlike the raw landing N_COSPONSORS, which double-counts a member listed twice on a bill.
cosp_n as (

    select congress, bill_type, bill_number, count(*) as n_cosponsors
    from {{ ref('stg_fed_govinfo_bill_cosponsors__cosponsors') }}
    group by 1, 2, 3

)

select
    congress,
    bill_type,
    bill_number,
    sponsor_bioguide,
    sponsor_name,
    title,
    (bill_type in ('HR','S','HJRES','SJRES'))                      as is_law_eligible,
    case when bill_type in ('HR','S')            then 'bill'
         when bill_type in ('HJRES','SJRES')     then 'joint_resolution'
         when bill_type in ('HCONRES','SCONRES') then 'concurrent_resolution'
         when bill_type in ('HRES','SRES')       then 'simple_resolution'
         else 'other' end                                          as bill_class,
    (law_number is not null)                                       as became_law,
    law_number,
    (array_size(array_intersection(action_types,
        array_construct('Committee','Calendars','Discharge','Floor','President',
                        'ResolvingDifferences','Veto','BecameLaw'))) > 0) as advanced_past_committee,
    case
        when law_number is not null then 'became_law'
        when array_contains('President'::variant, action_types)
          or array_contains('Veto'::variant, action_types)
          or array_contains('ResolvingDifferences'::variant, action_types) then 'passed_both_to_president'
        when array_contains('Floor'::variant, action_types)            then 'reached_floor'
        when array_contains('Calendars'::variant, action_types)
          or array_contains('Discharge'::variant, action_types)
          or array_contains('Committee'::variant, action_types)        then 'committee_action'
        when array_contains('IntroReferral'::variant, action_types)    then 'introduced'
        else 'unknown'
    end                                                            as latest_stage,
    introduced_date,
    latest_action_date,
    latest_action_text,
    coalesce(cosp_n.n_cosponsors, 0)                              as n_cosponsors,  -- DISTINCT cosponsors
    n_actions,
    (congress = 119)                                               as congress_partial
from base
left join cosp_n using (congress, bill_type, bill_number)
