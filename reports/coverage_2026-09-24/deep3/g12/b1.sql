-- [q01_billstatus_by_congress]
-- BILLSTATUS shape per Congress: rows vs distinct bill keys, law-eligible, laws, naming laws, dates, text-number junk
select CONGRESS,
  count(*) n,
  count(distinct upper(BILL_TYPE)||'-'||regexp_replace(BILL_NUMBER,'[^0-9]','')) n_keys,
  sum(iff(upper(BILL_TYPE) in ('HR','S','HJRES','SJRES'),1,0)) n_law_elig,
  sum(iff(nullif(trim(LAW_NUMBER),'') is not null,1,0)) n_law,
  sum(iff(LAW_TYPE ilike 'public%',1,0)) n_public,
  sum(iff(LAW_TYPE ilike 'private%',1,0)) n_private,
  sum(iff(nullif(trim(LAW_NUMBER),'') is not null and LAW_TYPE ilike 'public%' and TITLE ilike '%Postal Service%',1,0)) n_law_usps,
  sum(iff(nullif(trim(LAW_NUMBER),'') is not null and LAW_TYPE ilike 'public%' and (TITLE ilike 'to designate%' or TITLE ilike 'to name%' or TITLE ilike 'to rename%' or TITLE ilike 'to redesignate%'),1,0)) n_law_naming,
  min(INTRODUCED_DATE) min_intro, max(INTRODUCED_DATE) max_intro,
  sum(iff(nullif(trim(SPONSOR_BIOGUIDE),'') is null,1,0)) n_no_sponsor,
  sum(iff(try_to_number(N_ACTIONS) is null,1,0)) n_actions_not_num,
  sum(iff(try_to_number(N_COSPONSORS) is null,1,0)) n_cosp_not_num,
  sum(iff(ACTION_TYPES ilike '%veto%',1,0)) n_veto_type,
  count(distinct SPONSOR_BIOGUIDE) n_sponsors,
  listagg(distinct upper(BILL_TYPE), ',') types
from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILLSTATUS
group by 1 order by 1;

-- [q02_bills_vs_billstatus]
-- POLITICS__BILLS against BILLSTATUS for the Congresses they share; law flag agreement; staleness
with b as (
  select CONGRESS, upper(BILL_TYPE) bt, regexp_replace(BILL_NUMBER::string,'[^0-9]','') bn, BECAME_LAW, LAW_NUMBER, IS_LAW_ELIGIBLE,
         CONGRESS_PARTIAL, LATEST_STAGE, ADVANCED_PAST_COMMITTEE, INTRODUCED_DATE, LATEST_ACTION_DATE, N_ACTIONS
  from LIBRARY_MARTS.POLITICS.POLITICS__BILLS),
s as (
  select CONGRESS, upper(BILL_TYPE) bt, regexp_replace(BILL_NUMBER,'[^0-9]','') bn, LAW_NUMBER, LATEST_ACTION_DATE, try_to_number(N_ACTIONS) n_act, INTRODUCED_DATE
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILLSTATUS where CONGRESS >= 118)
select coalesce(b.CONGRESS, s.CONGRESS) congress,
  count(b.bt) in_bills, count(s.bt) in_status, sum(iff(b.bt is not null and s.bt is not null,1,0)) in_both,
  sum(iff(b.BECAME_LAW,1,0)) bills_became_law, sum(iff(nullif(trim(b.LAW_NUMBER),'') is not null,1,0)) bills_lawnum,
  sum(iff(nullif(trim(s.LAW_NUMBER),'') is not null,1,0)) status_lawnum,
  sum(iff(s.bt is not null and b.BECAME_LAW and nullif(trim(s.LAW_NUMBER),'') is null,1,0)) law_in_bills_not_status,
  sum(iff(b.bt is not null and not b.BECAME_LAW and nullif(trim(s.LAW_NUMBER),'') is not null,1,0)) law_in_status_not_bills,
  sum(iff(b.bt is not null and s.bt is not null and try_to_date(b.LATEST_ACTION_DATE::string) <> s.LATEST_ACTION_DATE,1,0)) latest_date_differs,
  sum(iff(b.bt is not null and s.bt is not null and b.N_ACTIONS <> s.n_act,1,0)) n_actions_differs,
  max(b.INTRODUCED_DATE) bills_max_intro, max(s.INTRODUCED_DATE) status_max_intro,
  max(try_to_date(b.LATEST_ACTION_DATE::string)) bills_max_latest, max(s.LATEST_ACTION_DATE) status_max_latest,
  sum(iff(b.CONGRESS_PARTIAL,1,0)) partial_true, sum(iff(b.IS_LAW_ELIGIBLE,1,0)) law_eligible,
  sum(iff(b.ADVANCED_PAST_COMMITTEE,1,0)) advanced, sum(iff(b.LATEST_STAGE='became_law',1,0)) stage_law,
  sum(iff(b.BECAME_LAW and not b.IS_LAW_ELIGIBLE,1,0)) law_but_not_eligible
from b full outer join s on b.CONGRESS = s.CONGRESS and b.bt = s.bt and b.bn = s.bn
group by 1 order by 1;

-- [q03_voteview_members_profile]
-- Voteview members: blanks, sentinel log-likelihood, votes counted, per Congress (113+) and older lumped
select iff(CONGRESS >= 113, CONGRESS::string, 'pre113') c, CHAMBER, count(*) n, count(distinct ICPSR) n_icpsr,
  sum(iff(nullif(trim(BIOGUIDE_ID),'') is null,1,0)) no_bioguide,
  sum(iff(try_to_double(NOMINATE_DIM1) is null,1,0)) no_dim1,
  sum(iff(try_to_double(NOKKEN_POOLE_DIM1) is null,1,0)) no_np1,
  sum(iff(try_to_double(NOMINATE_LOG_LIKELIHOOD) = 0,1,0)) ll_zero,
  median(NOMINATE_NUMBER_OF_VOTES) med_votes, max(NOMINATE_NUMBER_OF_VOTES) max_votes,
  sum(iff(NOMINATE_NUMBER_OF_VOTES is null,1,0)) votes_null,
  listagg(distinct PARTY_CODE, ',') parties,
  count(distinct CONDITIONAL) n_conditional_vals
from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS
group by 1,2 order by 1,2;

-- [q04_member_spine_profile]
-- Spine: is it a lookup? keys, stand-ins, match flags, label spread
select IDEOLOGY_LABEL, HAS_VOTEVIEW_MATCH, HAS_IDEOLOGY, count(*) n,
  sum(count(*)) over () total,
  sum(sum(iff(MEMBER_KEY like 'gt:%',1,0))) over () gt_keys,
  sum(sum(iff(BIOGUIDE is null or trim(BIOGUIDE)='',1,0))) over () no_bioguide,
  sum(count(distinct MEMBER_KEY)) over () distinct_keys_sum,
  min(DW_NOMINATE_DIM1) min_d1, max(DW_NOMINATE_DIM1) max_d1,
  sum(iff(LAST_TERM_TYPE='sen',1,0)) sen, sum(iff(LAST_TERM_TYPE='rep',1,0)) rep,
  sum(iff(LEGISLATOR_SET='current',1,0)) current_set
from LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE
group by 1,2,3 order by 4 desc;

-- [q05_senate_trades_by_year]
-- Senate trades per year: senators, PTRs, PDF-only rows, buys/sells, same trade under two PTR links (amendments)
with t as (
  select *, count(distinct PTR_LINK) over (partition by BIOGUIDE, TRANSACTION_DATE, OWNER, TICKER, ASSET_DESCRIPTION, TRANSACTION_TYPE, AMOUNT_BAND) n_ptrs_same_trade,
         count(*) over (partition by BIOGUIDE, TRANSACTION_DATE, OWNER, TICKER, ASSET_DESCRIPTION, TRANSACTION_TYPE, AMOUNT_BAND, PTR_LINK) same_ptr_copies
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES)
select year(TRANSACTION_DATE) y, count(*) n, count(distinct BIOGUIDE) senators, count(distinct PTR_LINK) ptrs,
  sum(iff(ASSET_TYPE ilike 'PDF%',1,0)) pdf_rows,
  sum(iff(TRANSACTION_TYPE ilike 'purchase%',1,0)) buys, sum(iff(TRANSACTION_TYPE ilike 'sale%',1,0)) sells,
  sum(iff(BIOGUIDE is null or trim(BIOGUIDE)='',1,0)) no_bioguide,
  sum(iff(n_ptrs_same_trade > 1,1,0)) rows_trade_in_2plus_ptrs,
  sum(iff(same_ptr_copies > 1,1,0)) rows_repeated_in_same_ptr,
  listagg(distinct MATCH_METHOD, ',') match_methods
from t group by 1 order by 1;

-- [q06_voteview_votes_coverage]
-- Roll-call votes table: which Congresses, how many roll calls, cast-code mix; roll-call date range
with v as (
  select CONGRESS, CHAMBER, count(*) n, count(distinct ROLLNUMBER) rolls, count(distinct ICPSR) members,
    sum(iff(CAST_CODE = 0,1,0)) c0, sum(iff(CAST_CODE between 1 and 6,1,0)) voted,
    sum(iff(CAST_CODE in (7,8),1,0)) present, sum(iff(CAST_CODE = 9,1,0)) not_voting, max(ROLLNUMBER) max_roll
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES group by 1,2),
r as (
  select CONGRESS, CHAMBER, count(*) rc_rows, min(VOTE_DATE) first_vote, max(VOTE_DATE) last_vote, max(ROLLNUMBER) rc_max_roll
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS group by 1,2)
select coalesce(v.CONGRESS, r.CONGRESS) congress, coalesce(v.CHAMBER, r.CHAMBER) chamber, v.n, v.rolls, v.members, v.c0, v.voted, v.present, v.not_voting, v.max_roll,
  r.rc_rows, r.first_vote, r.last_vote, r.rc_max_roll
from v full outer join r on v.CONGRESS = r.CONGRESS and v.CHAMBER = r.CHAMBER
order by 1,2;
