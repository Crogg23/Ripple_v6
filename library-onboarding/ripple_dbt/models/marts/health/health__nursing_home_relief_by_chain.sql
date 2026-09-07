{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per nursing-home chain in NURSINGHOME411 (CHAIN_ID, blank
-- excluded: 617 chains covering 10,162 homes), with the Provider Relief Fund
-- money that name-matched to its homes set beside the chain's ratings and fines.
--
-- Read matched_relief_dollars as a FLOOR. Only multi-word name matches on
-- free-standing homes count (int_nursing_home_prf_match, is_multiword and not
-- home_in_hospital and not payee_is_hospital); on the 2026-09-07 run that is
-- 14.4% of all homes and
-- matched_home_share says what it is per chain. Hospital-based units are
-- counted in hospital_based_homes and their payee's money, which is the
-- hospital's, sits in hospital_based_dollars_excluded so nobody has to guess
-- why ADVENTIST HEALTH is not at the top.
-- A chain that took its relief under a parent name ('ENSIGN GROUP INC' in one
-- city) shows nothing here, because the payee name is not the home name and
-- there is no EIN or CCN to bridge on. Zero is 'no name hit', never 'no money'.
--
-- payee_shorter_homes / payee_shorter_dollars (2026-09-07): the subset of
-- matched_homes / matched_relief_dollars where the payee name is SHORTER than
-- the home name (int_nursing_home_prf_match.payee_shorter_than_home). That is
-- a parent's or operator's cheque attributed to one building because the
-- file has no other bridge; the dollars are inside matched_relief_dollars,
-- not added to it. Subtract them for the strict per-building floor.
--
-- Ratings and fine columns are the chain's own snapshot values from NH411
-- (dated 2025-12-01 per the traps file, applied to fines back to 2023-06),
-- copied from any one home in the chain because they repeat on every row.

with matches as (

    select chain_id, ccn, payment_amount, match_method, payee_shorter_than_home,
           (home_in_hospital or payee_is_hospital) as home_in_hospital
    from {{ ref('int_nursing_home_prf_match') }}
    where chain_id is not null
      and is_multiword

),

chains as (

    select
        nullif(chain_id, '')                                          as chain_id,
        max(chain_name)                                               as chain_name,
        count(*)                                                      as homes_in_roster,
        max(number_of_facilities_in_chain)                            as number_of_facilities_in_chain,
        max(try_to_double(chain_average_overall_5_star_rating))       as chain_avg_overall_rating,
        max(try_to_double(chain_average_health_inspection_rating))    as chain_avg_health_inspection_rating,
        max(try_to_double(chain_average_staffing_rating))             as chain_avg_staffing_rating,
        max(try_to_double(chain_average_qm_rating))                   as chain_avg_qm_rating,
        sum(number_of_fines)                                          as total_fines_count,
        sum(total_amount_of_fines_in_dollars)                         as total_fines_dollars,
        sum(number_of_certified_beds)                                 as total_certified_beds,
        sum(iff(special_focus_status is not null and special_focus_status <> '', 1, 0))
                                                                      as special_focus_homes,
        sum(iff(abuse_icon = 'Y', 1, 0))                              as abuse_icon_homes,
        sum(iff(try_to_number(overall_rating) = 1, 1, 0))             as one_star_homes
    from {{ ref('health__fed_nursinghome411') }}
    where nullif(chain_id, '') is not null
    group by 1

),

rolled as (

    select
        chain_id,
        count(distinct iff(not home_in_hospital, ccn, null))          as matched_homes,
        sum(iff(not home_in_hospital, payment_amount, 0))             as matched_relief_dollars,
        count(distinct iff(home_in_hospital, ccn, null))              as hospital_based_homes,
        sum(iff(home_in_hospital, payment_amount, 0))                 as hospital_based_dollars_excluded,
        count(distinct iff(not home_in_hospital and payee_shorter_than_home, ccn, null))
                                                                      as payee_shorter_homes,
        sum(iff(not home_in_hospital and payee_shorter_than_home, payment_amount, 0))
                                                                      as payee_shorter_dollars,
        sum(iff(not home_in_hospital and match_method = 'exact', payment_amount, 0))                 as exact_match_dollars,
        sum(iff(not home_in_hospital and match_method = 'prf_starts_with_home', payment_amount, 0))  as prf_starts_with_home_dollars,
        sum(iff(not home_in_hospital and match_method = 'home_starts_with_prf', payment_amount, 0))  as home_starts_with_prf_dollars,
        sum(iff(not home_in_hospital and match_method = 'prf_contains_home', payment_amount, 0))     as prf_contains_home_dollars
    from matches
    group by 1

)

select
    c.chain_id,
    c.chain_name,
    c.homes_in_roster,
    c.number_of_facilities_in_chain,
    coalesce(r.matched_homes, 0)                                      as matched_homes,
    round(coalesce(r.matched_homes, 0) / c.homes_in_roster, 3)        as matched_home_share,
    coalesce(r.matched_relief_dollars, 0)                             as matched_relief_dollars,
    iff(r.matched_homes > 0, round(r.matched_relief_dollars / r.matched_homes), null)
                                                                      as relief_per_matched_home,
    coalesce(r.exact_match_dollars, 0)                                as exact_match_dollars,
    coalesce(r.prf_starts_with_home_dollars, 0)                       as prf_starts_with_home_dollars,
    coalesce(r.home_starts_with_prf_dollars, 0)                       as home_starts_with_prf_dollars,
    coalesce(r.prf_contains_home_dollars, 0)                          as prf_contains_home_dollars,
    coalesce(r.hospital_based_homes, 0)                               as hospital_based_homes,
    coalesce(r.hospital_based_dollars_excluded, 0)                    as hospital_based_dollars_excluded,
    coalesce(r.payee_shorter_homes, 0)                                as payee_shorter_homes,
    coalesce(r.payee_shorter_dollars, 0)                              as payee_shorter_dollars,
    c.chain_avg_overall_rating,
    c.chain_avg_health_inspection_rating,
    c.chain_avg_staffing_rating,
    c.chain_avg_qm_rating,
    c.total_fines_count,
    c.total_fines_dollars,
    iff(c.total_certified_beds > 0, round(c.total_fines_dollars / c.total_certified_beds), null)
                                                                      as fines_per_bed,
    c.total_certified_beds,
    c.special_focus_homes,
    c.abuse_icon_homes,
    c.one_star_homes
from chains c
left join rolled r on r.chain_id = c.chain_id
