-- GRAIN: one row per nursing home (CCN) that landed on a PRF payee, at most one
-- payee per home and at most one home per payee. 14,713 homes go in; on the
-- 2026-09-07 run 2,357 came out matched, 2,243 of them on a two-word-or-longer
-- key. No row here means no match, and that is a miss, not a zero payment.
--
-- THE MATCH, in order of trust. Both names go through prf_name_key (upper,
-- punctuation out, legal suffix off), and city + state must agree exactly.
--   exact                  keys identical
--   prf_starts_with_home   payee key begins with the home key plus a space
--                          ('BENJAMIN HEALTHCARE CENTER' <- no; 'THE CARDINAL
--                          AT NORTH HILLS' -> 'THE CARDINAL AT NORTH HILLS HEALTHCARE')
--   home_starts_with_prf   home key begins with the payee key plus a space
--                          ('DYERSBURG HEALTH AND REHABILITATION CENTER' <- 'DYERSBURG HEALTH')
--   prf_contains_home      home key sits inside the payee key as whole words
--                          ('EDGAR P BENJAMIN HEALTHCARE CENTER' contains 'BENJAMIN HEALTHCARE CENTER')
-- Nothing fuzzier. No Levenshtein, no first-N-characters, no stemming.
--
-- is_multiword: the SHORTER of the two keys has two or more words. A one-word
-- key ('RIVERVIEW', 'CREEKSIDE', 'JUDSON') matching a prefix is the 8%-real
-- collision from the traps file: 'RIVERVIEW' the home vs 'RIVERVIEW ENT CENTER
-- OF CENTRAL OHIO' the ear doctor, same city. Those rows are kept so they can
-- be eyeballed, flagged false, and the chain rollup leaves them out.
--
-- Fan-out is cut twice. A home that hits several payees keeps the best method,
-- then the biggest payment. A payee that is then still claimed by several
-- homes (two 'COMMUNITY CARE CENTER's in one town) keeps one home the same
-- way, so a dollar is never counted under two CCNs. matched_prf_rows and
-- prf_shared_by_homes say how many candidates were dropped on each side.
--
-- home_in_hospital is NH411's PROVIDER_RESIDES_IN_HOSPITAL = 'Y': a skilled
-- nursing unit inside a hospital. The name match is RIGHT on those and the
-- money is WRONG: 'THE METHODIST HOSPITAL SNF' lands on 'THE METHODIST
-- HOSPITAL', $133M, which is the hospital's relief, not the 30-bed unit's.
-- 98 such homes carried $985M of the $3.43B matched on 2026-09-07. They stay
-- here flagged; the chain rollup leaves them out of its dollar column.
-- The flag under-catches: 'THE METHODIST HOSPITAL SNF' in Houston is 'N' in
-- NH411 and still took the hospital's $133M under this match. So a second
-- flag, payee_is_hospital, fires when the PAYEE key says HOSPITAL, MEDICAL
-- CENTER, HEALTH SYSTEM or HEALTH NETWORK. The rollup drops both kinds.
--
-- payee_shorter_than_home (added 2026-09-07 after the skeptic pass): true
-- when the PAYEE key has fewer characters than the HOME key. That is the
-- shape of a corporate parent's cheque landing on one building: 'WHITE OAK
-- MANAGEMENT' -> 'WHITE OAK MANOR - SPARTANBURG', $8.3M on one home; 'NHC
-- HEALTHCARE' -> 'NHC HEALTHCARE, FRANKLIN', $18.0M. By construction it is
-- exactly the home_starts_with_prf rows (exact keys are equal in length, the
-- other two methods have the payee longer). Rows stay; the chain rollup
-- counts them and their dollars separately so a reader can subtract.

with homes as (

    select
        cms_certification_number_ccn                            as ccn,
        provider_name                                           as home_name,
        upper(trim(state))                                      as state,
        upper(trim(city_town))                                  as city,
        {{ prf_name_key('provider_name') }}                     as home_key,
        regexp_count({{ prf_name_key('provider_name') }}, ' ') + 1 as home_words,
        nullif(chain_id, '')                                    as chain_id,
        chain_name,
        provider_resides_in_hospital = 'Y'                      as home_in_hospital
    from {{ ref('health__fed_nursinghome411') }}

),

prf as (

    select prf_row_id, provider_name as prf_name, state, city,
           name_key as prf_key, name_words as prf_words, payment_amount
    from {{ ref('stg_fed_hrsa_provider_relief_fund__payments') }}
    where name_key <> ''

),

candidates as (

    select
        h.*,
        p.prf_row_id, p.prf_name, p.prf_key, p.prf_words, p.payment_amount,
        case
            when h.home_key = p.prf_key                          then 'exact'
            when startswith(p.prf_key, h.home_key || ' ')        then 'prf_starts_with_home'
            when startswith(h.home_key, p.prf_key || ' ')        then 'home_starts_with_prf'
            when contains(p.prf_key, ' ' || h.home_key || ' ')
              or endswith(p.prf_key, ' ' || h.home_key)          then 'prf_contains_home'
        end                                                       as match_method,
        least(h.home_words, p.prf_words) >= 2                     as is_multiword,
        regexp_like(p.prf_key, '.*(HOSPITAL|MEDICAL CENTER|HEALTH SYSTEM|HEALTH NETWORK).*')
                                                                  as payee_is_hospital,
        length(p.prf_key) < length(h.home_key)                    as payee_shorter_than_home
    from homes h
    join prf p
      on p.state = h.state
     and p.city  = h.city
    where h.home_key <> ''

),

hits as (

    select * from candidates where match_method is not null

),

ranked as (

    select *,
        case match_method
            when 'exact' then 1 when 'prf_starts_with_home' then 2
            when 'home_starts_with_prf' then 3 else 4 end        as method_rank,
        count(*) over (partition by ccn)                          as matched_prf_rows
    from hits
    qualify row_number() over (partition by ccn
                               order by method_rank, payment_amount desc, prf_row_id) = 1

),

one_home_per_payee as (

    select *,
        count(*) over (partition by prf_row_id)                   as prf_shared_by_homes
    from ranked
    qualify row_number() over (partition by prf_row_id
                               order by method_rank, ccn) = 1

)

select
    ccn, home_name, state, city, chain_id, chain_name,
    prf_row_id, prf_name, payment_amount,
    match_method, is_multiword, home_in_hospital, payee_is_hospital, payee_shorter_than_home,
    home_key, prf_key,
    matched_prf_rows, prf_shared_by_homes
from one_home_per_payee
