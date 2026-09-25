-- g12: deep pass 3, 2026-09-24. Python door, QUERY_TAG deep3-2026-09-24. Read-only: SELECT/WITH only.
-- Tables: POLITICS__FED_GOVINFO_BILLSTATUS, POLITICS__FED_VOTEVIEW_MEMBERS, POLITICS__BILLS, POLITICS__MEMBER_SPINE, POLITICS__SENATE_TRADES.
-- Every statement run is below, in order, with its runtime.

-- ===== connection: b1.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q01_billstatus_by_congress] (0.7s)
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

-- [q02_bills_vs_billstatus] (0.9s)
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

-- [q03_voteview_members_profile] (0.5s)
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

-- [q04_member_spine_profile] (0.5s)
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

-- [q05_senate_trades_by_year] (0.6s)
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

-- [q06_voteview_votes_coverage] (1.0s)
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

-- ===== connection: b2.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q07_billstatus_same_point_by_congress] (0.6s)
-- Laws and post-office naming laws at the same point of each Congress (day 539 = 2026-06-26 for the 119th); does LATEST_ACTION_DATE mark enactment?
with s as (
  select CONGRESS, to_date((1787 + 2*CONGRESS)::string || '-01-03') cstart, upper(BILL_TYPE) bt, TITLE, LAW_TYPE,
         nullif(trim(LAW_NUMBER),'') law, LATEST_ACTION_DATE, LATEST_ACTION_TEXT, INTRODUCED_DATE
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILLSTATUS),
f as (
  select *, dateadd(day, 539, cstart) cut,
    (TITLE ilike '%Postal Service%' and (TITLE ilike 'to designate%' or TITLE ilike 'to redesignate%' or TITLE ilike '%post office%')) usps_name,
    (TITLE ilike 'to designate%' or TITLE ilike 'to name%' or TITLE ilike 'to rename%' or TITLE ilike 'to redesignate%') any_name,
    (law is not null and LAW_TYPE ilike 'public%') pl
  from s)
select CONGRESS, max(cut) cut,
  sum(iff(pl,1,0)) pl_final,
  sum(iff(pl and LATEST_ACTION_DATE <= cut,1,0)) pl_by_cut,
  sum(iff(pl and LATEST_ACTION_TEXT ilike 'became public law%',1,0)) pl_latest_is_enactment,
  sum(iff(pl and usps_name,1,0)) usps_pl_final,
  sum(iff(pl and usps_name and LATEST_ACTION_DATE <= cut,1,0)) usps_pl_by_cut,
  sum(iff(pl and any_name,1,0)) anyname_pl_final,
  sum(iff(pl and any_name and LATEST_ACTION_DATE <= cut,1,0)) anyname_pl_by_cut,
  sum(iff(usps_name,1,0)) usps_bills_all,
  sum(iff(usps_name and INTRODUCED_DATE <= cut,1,0)) usps_bills_by_cut,
  sum(iff(INTRODUCED_DATE <= cut,1,0)) all_bills_by_cut,
  sum(iff(bt in ('HR','S','HJRES','SJRES') and INTRODUCED_DATE <= cut,1,0)) elig_bills_by_cut
from f group by 1 order by 1;

-- [q08_billstatus_career_zero_law_sponsors] (0.8s)
-- Sponsors 113th-118th (complete Congresses): law-eligible bills vs public laws, peer = same chamber and party
with b as (
  select SPONSOR_BIOGUIDE bio, CONGRESS, upper(BILL_TYPE) bt, SPONSOR_NAME, nullif(trim(LAW_NUMBER),'') law, LAW_TYPE
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILLSTATUS
  where CONGRESS between 113 and 118 and upper(BILL_TYPE) in ('HR','HJRES','S','SJRES') and nullif(trim(SPONSOR_BIOGUIDE),'') is not null),
m as (
  select bio, iff(bt in ('HR','HJRES'),'House','Senate') ch, max(SPONSOR_NAME) nm,
    mode(regexp_substr(SPONSOR_NAME, '\\[([A-Z]+)-', 1, 1, 'e', 1)) party,
    count(*) bills, count(distinct CONGRESS) congresses,
    sum(iff(law is not null and LAW_TYPE ilike 'public%',1,0)) laws
  from b group by 1,2),
p as (
  select ch, party, count(*) members, median(bills) med_bills, median(laws) med_laws,
    median(bills/congresses) med_bills_per_cong, sum(iff(laws=0,1,0)) zero_law_members,
    sum(iff(laws=0 and bills>=100,1,0)) zero_law_100plus, sum(iff(bills>=100,1,0)) members_100plus,
    percentile_cont(0.9) within group (order by bills) p90_bills
  from m group by 1,2),
r as (
  select m.*, rank() over (partition by m.ch order by m.bills desc) rk from m where m.laws = 0)
select 'a_peer' kind, ch, party, null bio, null nm, members n_members, med_bills bills, med_laws laws, med_bills_per_cong per_cong,
  zero_law_members, zero_law_100plus, members_100plus, p90_bills, null congresses, null rk
from p where members >= 3
union all
select 'b_zero_law', ch, party, bio, nm, null, bills, laws, round(bills/congresses,1), null, null, null, null, congresses, rk
from r where rk <= 12
order by kind, ch, rk, party;

-- [q09_bills_118_sponsor_peer] (0.5s)
-- 118th Congress, law-eligible bills only: who sponsored the most and got none past committee, against same chamber+party medians
with m as (
  select SPONSOR_BIOGUIDE bio, iff(upper(BILL_TYPE) in ('HR','HJRES'),'House','Senate') ch, max(SPONSOR_NAME) nm,
    mode(regexp_substr(SPONSOR_NAME, '\\[([A-Z]+)-', 1, 1, 'e', 1)) party,
    count(*) bills, sum(iff(ADVANCED_PAST_COMMITTEE,1,0)) adv, sum(iff(BECAME_LAW,1,0)) laws, sum(N_COSPONSORS) cosp
  from LIBRARY_MARTS.POLITICS.POLITICS__BILLS where CONGRESS = 118 and IS_LAW_ELIGIBLE group by 1,2),
p as (
  select ch, party, count(*) members, median(bills) med_bills, median(adv) med_adv, median(laws) med_laws,
    round(median(adv/bills),3) med_adv_rate, sum(bills) tot_bills, sum(adv) tot_adv, sum(iff(adv=0,1,0)) zero_adv_members
  from m group by 1,2),
r as (
  select m.*, rank() over (partition by m.ch, m.party order by m.bills desc) rk from m where m.adv = 0)
select 'a_peer' kind, ch, party, null bio, null nm, members, med_bills bills, med_adv adv, med_laws laws, med_adv_rate, tot_bills, tot_adv, zero_adv_members, null rk
from p where members >= 3
union all
select 'b_zero_adv', ch, party, bio, nm, null, bills, adv, laws, null, cosp, null, null, rk from r where rk <= 5
order by kind, ch, party, rk;

-- [q10_missed_votes_118_119] (1.0s)
-- Missed roll calls (cast code 9) per member, only over roll calls held while they served; peer = same chamber, same Congress
with v as (
  select CONGRESS, CHAMBER, ICPSR, count(*) rolls, sum(iff(CAST_CODE = 9,1,0)) missed, min(ROLLNUMBER) first_roll, max(ROLLNUMBER) last_roll
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES group by 1,2,3),
mm as (
  select CONGRESS, CHAMBER, try_to_double(ICPSR)::number icpsr, BIONAME, BIOGUIDE_ID, STATE_ABBREV, PARTY_CODE, OCCUPANCY, LAST_MEANS, DIED
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS where CONGRESS in (118,119) and CHAMBER in ('House','Senate')),
t as (select CONGRESS, CHAMBER, count(*) total_rolls from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS group by 1,2),
j as (
  select v.*, t.total_rolls, v.missed / v.rolls rate, mm.BIONAME, mm.BIOGUIDE_ID, mm.STATE_ABBREV, mm.PARTY_CODE, mm.OCCUPANCY, mm.DIED, (mm.icpsr is null) unmatched
  from v join t on t.CONGRESS = v.CONGRESS and t.CHAMBER = v.CHAMBER
  left join mm on mm.CONGRESS = v.CONGRESS and mm.CHAMBER = v.CHAMBER and mm.icpsr = v.ICPSR),
p as (
  select CONGRESS, CHAMBER, count(*) members, sum(iff(unmatched,1,0)) unmatched, max(total_rolls) total_rolls,
    round(median(iff(rolls >= 100, rate, null)),4) med_rate, round(percentile_cont(0.9) within group (order by iff(rolls >= 100, rate, null)),4) p90_rate,
    sum(iff(rolls >= 100 and rate >= 0.2,1,0)) n_20pct_plus
  from j group by 1,2),
r as (select j.*, rank() over (partition by CONGRESS, CHAMBER order by rate desc) rk from j where rolls >= 100)
select 'a_peer' kind, CONGRESS, CHAMBER, null nm, null bio, null st, null party, members rolls, unmatched missed, med_rate rate, p90_rate, n_20pct_plus, total_rolls, null first_roll, null last_roll, null died, null rk from p
union all
select 'b_top', CONGRESS, CHAMBER, BIONAME, BIOGUIDE_ID, STATE_ABBREV, PARTY_CODE, rolls, missed, round(rate,4), null, null, total_rolls, first_roll, last_roll, DIED, rk from r where rk <= 15
order by kind, CONGRESS, CHAMBER, rk;

-- [q11_missed_votes_vs_senate_runs_2026] (1.4s)
-- Dull-explanation test: 119th House members who filed for Senate/President 2026+ (FEC id via crosswalk, or surname+state) vs the rest
with h as (
  select ICPSR, count(*) rolls, sum(iff(CAST_CODE = 9,1,0)) missed
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES where CONGRESS = 119 and CHAMBER = 'House' group by 1),
mm as (
  select try_to_double(ICPSR)::number icpsr, BIOGUIDE_ID, BIONAME, STATE_ABBREV
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS where CONGRESS = 119 and CHAMBER = 'House'),
fi as (
  select c.BIOGUIDE, f.value::string fec_id
  from LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK c, lateral flatten(input => c.FEC_IDS) f),
cand as (
  select CAND_ID, CAND_NAME, OFFICE, OFFICE_STATE, CAND_ELECTION_YR
  from LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE where OFFICE in ('S','P') and CAND_ELECTION_YR >= 2026),
idhit as (select distinct fi.BIOGUIDE from fi join cand on cand.CAND_ID = fi.fec_id),
namehit as (
  select distinct mm.BIOGUIDE_ID from mm join cand
    on cand.OFFICE_STATE = mm.STATE_ABBREV and trim(split_part(cand.CAND_NAME, ',', 1)) = upper(trim(split_part(mm.BIONAME, ',', 1)))),
x as (
  select mm.*, h.rolls, h.missed, h.missed / h.rolls rate, (i.BIOGUIDE is not null) id_hit, (n.BIOGUIDE_ID is not null) name_hit
  from mm join h on h.ICPSR = mm.icpsr
  left join idhit i on i.BIOGUIDE = mm.BIOGUIDE_ID left join namehit n on n.BIOGUIDE_ID = mm.BIOGUIDE_ID)
select id_hit, name_hit, count(*) members, round(median(rate),4) med_rate, round(sum(missed)/sum(rolls),4) pooled_rate,
  round(percentile_cont(0.9) within group (order by rate),4) p90_rate,
  (select count(*) from cand) cand_rows_2026plus,
  (select count(*) from cand where OFFICE = 'S' and CAND_ELECTION_YR = 2026) senate_2026_rows,
  left(listagg(iff(id_hit or name_hit, BIONAME || ' ' || STATE_ABBREV || ' ' || round(100*rate,1), null), '; ') within group (order by rate desc), 1500) who
from x where rolls >= 100 group by 1,2 order by 1,2;

-- [q12_senate_trades_covid_window] (0.4s)
-- Trades 24 Jan - 20 Feb (after the 24 Jan 2020 Senate coronavirus briefing, before the crash), 2020 vs the same weeks 2015-2019; per year and per senator
with t as (
  select BIOGUIDE, SPINE_NAME, TRANSACTION_DATE d, TRANSACTION_TYPE tt, OWNER,
    try_to_number(replace(regexp_substr(AMOUNT_BAND, '[0-9,]+'), ',', '')) lo
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES where ASSET_TYPE not ilike 'PDF%'),
w as (select *, year(d) y, (d between date_from_parts(year(d),1,24) and date_from_parts(year(d),2,20)) in_win from t)
select 'a_year' kind, y::string k, null nm,
  sum(iff(in_win and tt ilike 'sale%',1,0)) win_sells, sum(iff(in_win and tt ilike 'purchase%',1,0)) win_buys,
  sum(iff(in_win and tt ilike 'sale%',lo,0)) win_sell_lo_usd, count(distinct iff(in_win and tt ilike 'sale%', BIOGUIDE, null)) win_sellers,
  count(distinct BIOGUIDE) senators_year, sum(iff(tt ilike 'sale%',1,0)) year_sells, sum(iff(tt ilike 'purchase%',1,0)) year_buys
from w where y between 2014 and 2020 group by 1,2,3
union all
select 'b_senator', BIOGUIDE, max(SPINE_NAME),
  sum(iff(y=2020 and in_win and tt ilike 'sale%',1,0)), sum(iff(y=2020 and in_win and tt ilike 'purchase%',1,0)),
  sum(iff(y=2020 and in_win and tt ilike 'sale%',lo,0)),
  round(sum(iff(y between 2015 and 2019 and in_win and tt ilike 'sale%',1,0))/5, 1),
  round(sum(iff(y between 2015 and 2019 and in_win and tt ilike 'purchase%',1,0))/5, 1),
  sum(iff(y=2020 and tt ilike 'sale%',1,0)), sum(iff(y=2020 and tt ilike 'purchase%',1,0))
from w group by 1,2 having sum(iff(y=2020 and in_win,1,0)) > 0
order by 1, 4 desc;

-- [q13_senate_trades_paper_filers] (0.3s)
-- Per senator: how many PTRs are scanned paper (PDF-only rows), and when
select BIOGUIDE, max(SPINE_NAME) nm, count(distinct PTR_LINK) ptrs,
  count(distinct iff(ASSET_TYPE ilike 'PDF%', PTR_LINK, null)) pdf_ptrs,
  count(distinct iff(ASSET_TYPE ilike 'PDF%' and year(TRANSACTION_DATE) >= 2015, PTR_LINK, null)) pdf_ptrs_2015plus,
  count(*) rows_all, min(TRANSACTION_DATE) first_d, max(TRANSACTION_DATE) last_d,
  max(iff(ASSET_TYPE ilike 'PDF%', TRANSACTION_DATE, null)) last_pdf_d
from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES
group by 1 order by pdf_ptrs desc, ptrs desc;

-- [q14_senate_trades_repeat_rows_sample] (0.1s, ERROR)
-- Identical rows inside one PTR: real multiple lots or a doubled load? top groups
select BIOGUIDE, SPINE_NAME, TRANSACTION_DATE, OWNER, TICKER, left(ASSET_DESCRIPTION, 60) asset, TRANSACTION_TYPE, AMOUNT_BAND, right(PTR_LINK, 45) ptr, count(*) copies,
  sum(count(*)) over () rows_in_groups, count(*) over () n_groups
from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES
group by all having count(*) > 1 order by copies desc, TRANSACTION_DATE desc limit 25;

-- [q15_spine_unmatched_vs_voteview] (0.9s)
-- Spine rows flagged no Voteview match: are they in Voteview members by bioguide anyway?
with s as (select * from LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE where not HAS_VOTEVIEW_MATCH),
vv as (
  select BIOGUIDE_ID, max(CONGRESS) last_c, count(*) n
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS where nullif(trim(BIOGUIDE_ID),'') is not null group by 1)
select s.LEGISLATOR_SET, s.LAST_TERM_TYPE, count(*) n, sum(iff(vv.BIOGUIDE_ID is not null,1,0)) in_voteview_by_bioguide,
  sum(iff(s.ICPSR is null,1,0)) spine_icpsr_null, max(vv.last_c) max_vv_congress,
  min(s.FIRST_TERM_START) min_first, max(s.FIRST_TERM_START) max_first,
  left(listagg(iff(vv.BIOGUIDE_ID is not null, s.FULL_NAME || ' (' || s.BIOGUIDE || ')', null), '; ') within group (order by s.FULL_NAME), 600) sample_in_vv
from s left join vv on vv.BIOGUIDE_ID = s.BIOGUIDE
group by 1,2 order by 3 desc;

-- [q16_bills_usps_naming_stage] (0.4s)
-- Post-office naming bills in POLITICS__BILLS: how far each got, 118th vs 119th
select CONGRESS, LATEST_STAGE, count(*) n, sum(iff(upper(BILL_TYPE) = 'HR',1,0)) house_bills, sum(iff(upper(BILL_TYPE) = 'S',1,0)) senate_bills
from LIBRARY_MARTS.POLITICS.POLITICS__BILLS
where TITLE ilike '%Postal Service%' and (TITLE ilike 'to designate%' or TITLE ilike 'to redesignate%' or TITLE ilike '%post office%')
group by 1,2 order by 1,2;

-- ===== connection: b3.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q17_bills_advanced_flag_trap] (0.5s)
-- Does ADVANCED_PAST_COMMITTEE count a subcommittee referral as "advanced"? 118th, law-eligible bills, by chamber
select iff(upper(BILL_TYPE) in ('HR','HJRES'),'House','Senate') ch, ADVANCED_PAST_COMMITTEE adv, LATEST_STAGE, count(*) n,
  sum(iff(LATEST_ACTION_TEXT ilike 'Referred to the Subcommittee%',1,0)) latest_is_subcmte_referral,
  sum(iff(LATEST_ACTION_TEXT ilike 'Referred to%' or LATEST_ACTION_TEXT ilike 'Read twice and referred%',1,0)) latest_is_any_referral,
  mode(left(LATEST_ACTION_TEXT, 80)) top_latest_text
from LIBRARY_MARTS.POLITICS.POLITICS__BILLS
where CONGRESS = 118 and IS_LAW_ELIGIBLE
group by 1,2,3 order by 1,2,3;

-- [q18_missed_votes_by_month_119_house] (0.8s)
-- Time check: when did the top 119th House absentees start missing? missed/held per month, plus the whole House
with mm as (
  select try_to_double(ICPSR)::number icpsr, BIOGUIDE_ID, BIONAME
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS where CONGRESS = 119 and CHAMBER = 'House'),
r as (select ROLLNUMBER, VOTE_DATE from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS where CONGRESS = 119 and CHAMBER = 'House'),
v as (
  select v.ICPSR, v.CAST_CODE, to_char(r.VOTE_DATE, 'YYYY-MM') mo, r.VOTE_DATE
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v join r on r.ROLLNUMBER = v.ROLLNUMBER
  where v.CONGRESS = 119 and v.CHAMBER = 'House'),
all_m as (select mo, sum(iff(CAST_CODE = 9,1,0)) missed, count(*) n from v group by 1),
sel as (
  select mm.BIONAME, v.mo, sum(iff(CAST_CODE = 9,1,0)) missed, count(*) n, max(v.VOTE_DATE) last_d
  from v join mm on mm.icpsr = v.ICPSR
  where mm.BIOGUIDE_ID in ('H001095','S001193','K000398','W000808','M000194','S001196','P000620','S001207','G000583','C001131')
  group by 1,2)
select 'ALL HOUSE (member-votes)' nm, listagg(mo || ' ' || round(100*missed/n,1) || '%', ' | ') within group (order by mo) months, null last_vote from all_m
union all
select BIONAME, listagg(mo || ' ' || missed || '/' || n, ' | ') within group (order by mo), max(last_d) from sel group by 1
order by 1;

-- [q19_laws_by_type_same_point] (0.3s)
-- Dull-explanation test for the law count: how many of the day-539 laws were CRA disapprovals, naming bills, spending bills
with f as (
  select CONGRESS, upper(BILL_TYPE) bt, LATEST_ACTION_DATE, TITLE,
    dateadd(day, 539, to_date((1787 + 2*CONGRESS)::string || '-01-03')) cut
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILLSTATUS
  where nullif(trim(LAW_NUMBER),'') is not null and LAW_TYPE ilike 'public%'),
g as (
  select *, LATEST_ACTION_DATE <= cut in_cut,
    TITLE ilike '%congressional disapproval%' cra,
    (TITLE ilike 'to designate%' or TITLE ilike 'to name%' or TITLE ilike 'to rename%' or TITLE ilike 'to redesignate%') naming,
    (TITLE ilike '%appropriations%' or TITLE ilike '%continuing%' or TITLE ilike '%extension%' or TITLE ilike '%to extend%') money_or_ext
  from f)
select CONGRESS, count(*) pl_final, sum(iff(in_cut,1,0)) by_cut,
  sum(iff(in_cut and bt = 'HR',1,0)) hr, sum(iff(in_cut and bt = 'S',1,0)) s,
  sum(iff(in_cut and bt = 'HJRES',1,0)) hjres, sum(iff(in_cut and bt = 'SJRES',1,0)) sjres,
  sum(iff(in_cut and cra,1,0)) cra_by_cut, sum(iff(cra,1,0)) cra_final,
  sum(iff(in_cut and naming,1,0)) naming_by_cut,
  sum(iff(in_cut and money_or_ext and not naming and not cra,1,0)) money_ext_by_cut,
  sum(iff(in_cut and not cra and not naming and not money_or_ext,1,0)) other_by_cut
from g group by 1 order by 1;

-- [q20_zero_law_sponsors_companion_test] (0.5s)
-- Dull-explanation test: zero-law sponsors 113th-118th whose bill title exactly matches a bill that became law in the same Congress (companion passed under another name)
with b as (
  select CONGRESS, upper(BILL_TYPE) bt, SPONSOR_BIOGUIDE bio, SPONSOR_NAME, lower(trim(TITLE)) tl, nullif(trim(LAW_NUMBER),'') law, LAW_TYPE
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILLSTATUS
  where CONGRESS between 113 and 118 and upper(BILL_TYPE) in ('HR','HJRES','S','SJRES') and nullif(trim(SPONSOR_BIOGUIDE),'') is not null),
laws as (select distinct CONGRESS, tl from b where law is not null and LAW_TYPE ilike 'public%'),
m as (
  select bio, iff(bt in ('HR','HJRES'),'House','Senate') ch, max(SPONSOR_NAME) nm, count(*) bills,
    sum(iff(law is not null and LAW_TYPE ilike 'public%',1,0)) own_laws,
    sum(iff(law is null and l.tl is not null,1,0)) companion_hits,
    sum(iff(bt in ('HJRES','SJRES'),1,0)) joint_res,
    sum(iff(b.tl ilike '%disapproval%',1,0)) disapproval_titles,
    sum(iff(b.tl ilike '%amend the internal revenue code%',1,0)) tax_code_titles
  from b left join laws l on l.CONGRESS = b.CONGRESS and l.tl = b.tl
  group by 1,2),
s as (
  select count(*) zero_members, sum(iff(companion_hits > 0,1,0)) zero_with_companion,
    sum(iff(bills >= 100,1,0)) zero_100plus, sum(iff(bills >= 100 and companion_hits > 0,1,0)) zero_100plus_with_companion
  from m where own_laws = 0)
select 'a_summary' kind, null ch, null bio, null nm, zero_members bills, zero_with_companion own_laws, zero_100plus companion_hits, zero_100plus_with_companion joint_res, null disapproval_titles, null tax_code_titles from s
union all
select 'b_member', ch, bio, nm, bills, own_laws, companion_hits, joint_res, disapproval_titles, tax_code_titles
from m where own_laws = 0 and bills >= 100
order by kind, bills desc;

-- [q21_senate_trades_repeat_rows] (0.4s)
-- Identical rows inside one PTR: how many, whose, and the biggest groups
with g as (
  select BIOGUIDE, SPINE_NAME, TRANSACTION_DATE, OWNER, TICKER, ASSET_DESCRIPTION, TRANSACTION_TYPE, AMOUNT_BAND, PTR_LINK, count(*) copies
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES
  group by BIOGUIDE, SPINE_NAME, TRANSACTION_DATE, OWNER, TICKER, ASSET_DESCRIPTION, TRANSACTION_TYPE, AMOUNT_BAND, PTR_LINK
  having count(*) > 1),
x as (select g.*, count(*) over () n_groups, sum(copies) over () rows_in_groups, sum(copies) over (partition by BIOGUIDE) sen_rows from g)
select SPINE_NAME, TRANSACTION_DATE, OWNER, TICKER, left(ASSET_DESCRIPTION, 50) asset, TRANSACTION_TYPE, AMOUNT_BAND, right(PTR_LINK, 40) ptr, copies, n_groups, rows_in_groups, sen_rows
from x order by sen_rows desc, copies desc, TRANSACTION_DATE desc limit 20;

-- [q22_senate_trades_pdf_rows_sample] (0.1s)
-- What a paper-filer row holds: Burr, Blumenthal, Boozman, Feinstein, 2019-2020
select SPINE_NAME, TRANSACTION_DATE, OWNER, TICKER, left(ASSET_DESCRIPTION, 70) asset, ASSET_TYPE, TRANSACTION_TYPE, AMOUNT_BAND, left(COMMENT, 40) cmt, PTR_LINK
from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES
where BIOGUIDE in ('B001135','B001277','B001236','F000062') and TRANSACTION_DATE >= '2019-10-01'
order by TRANSACTION_DATE limit 20;

-- ===== connection: b4.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q23_absence_streaks_118_119] (1.5s)
-- Longest unbroken run of missed roll calls per member (cast code 9), with dates, and whether it runs to the member's last roll; peer = median over all members, same chamber and Congress
with v as (
  select v.CONGRESS, v.CHAMBER, v.ICPSR, v.ROLLNUMBER, r.VOTE_DATE, iff(v.CAST_CODE = 9,1,0) m
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v
  join LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS r on r.CONGRESS = v.CONGRESS and r.CHAMBER = v.CHAMBER and r.ROLLNUMBER = v.ROLLNUMBER),
g as (
  select *, row_number() over (partition by CONGRESS, CHAMBER, ICPSR order by ROLLNUMBER)
          - row_number() over (partition by CONGRESS, CHAMBER, ICPSR, m order by ROLLNUMBER) grp
  from v),
runs as (
  select CONGRESS, CHAMBER, ICPSR, grp, count(*) len, min(VOTE_DATE) d0, max(VOTE_DATE) d1, max(ROLLNUMBER) end_roll
  from g where m = 1 group by 1,2,3,4),
best as (select * from runs qualify row_number() over (partition by CONGRESS, CHAMBER, ICPSR order by len desc, end_roll desc) = 1),
mem as (
  select CONGRESS, CHAMBER, ICPSR, max(ROLLNUMBER) last_row_roll, count(*) rolls, sum(m) missed, max(iff(m = 0, VOTE_DATE, null)) last_cast_date
  from v group by 1,2,3),
mm as (
  select CONGRESS, CHAMBER, try_to_double(ICPSR)::number icpsr, BIONAME, BIOGUIDE_ID, STATE_ABBREV, PARTY_CODE
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS where CONGRESS in (118,119) and CHAMBER in ('House','Senate')),
x as (
  select mem.*, coalesce(b.len,0) max_streak, b.d0, b.d1, (b.end_roll = mem.last_row_roll) trailing,
    mm.BIONAME, mm.BIOGUIDE_ID, mm.STATE_ABBREV, mm.PARTY_CODE
  from mem left join best b on b.CONGRESS = mem.CONGRESS and b.CHAMBER = mem.CHAMBER and b.ICPSR = mem.ICPSR
  left join mm on mm.CONGRESS = mem.CONGRESS and mm.CHAMBER = mem.CHAMBER and mm.icpsr = mem.ICPSR
  where coalesce(mm.STATE_ABBREV,'') not in ('AS','GU','PR','MP','VI','DC')),
y as (
  select x.*, median(max_streak) over (partition by CONGRESS, CHAMBER) med_streak,
    percentile_cont(0.9) within group (order by max_streak) over (partition by CONGRESS, CHAMBER) p90_streak,
    count(*) over (partition by CONGRESS, CHAMBER) n_members,
    rank() over (partition by CONGRESS, CHAMBER order by max_streak desc) rk
  from x)
select CONGRESS, CHAMBER, rk, BIONAME, BIOGUIDE_ID, STATE_ABBREV, PARTY_CODE, max_streak, d0, d1, trailing, rolls, missed, last_cast_date, med_streak, p90_streak, n_members
from y where rk <= 10 order by CONGRESS, CHAMBER, rk;

-- [q24_bills_118_floor_peer] (0.5s)
-- 118th, law-eligible: real advancement = LATEST_STAGE reached_floor or later; flag vs stage; peer = chamber + party
with m as (
  select SPONSOR_BIOGUIDE bio, iff(upper(BILL_TYPE) in ('HR','HJRES'),'House','Senate') ch, max(SPONSOR_NAME) nm,
    mode(regexp_substr(SPONSOR_NAME, '\\[([A-Z]+)-', 1, 1, 'e', 1)) party, count(*) bills,
    sum(iff(LATEST_STAGE in ('reached_floor','passed_both_to_president','became_law'),1,0)) floor,
    sum(iff(ADVANCED_PAST_COMMITTEE,1,0)) adv_flag, sum(iff(BECAME_LAW,1,0)) laws
  from LIBRARY_MARTS.POLITICS.POLITICS__BILLS where CONGRESS = 118 and IS_LAW_ELIGIBLE group by 1,2),
p as (
  select ch, party, count(*) members, median(bills) med_bills, median(floor) med_floor, round(sum(floor)/sum(bills),4) pooled_floor_rate,
    median(adv_flag) med_adv_flag, round(sum(adv_flag)/sum(bills),4) pooled_adv_flag_rate, sum(iff(floor = 0,1,0)) zero_floor,
    sum(iff(floor = 0 and bills >= 40,1,0)) zero_floor_40plus
  from m group by 1,2),
r as (select m.*, rank() over (partition by ch order by bills desc) rk from m where floor = 0)
select 'a_peer' kind, ch, party, null bio, null nm, members, med_bills bills, med_floor floor, pooled_floor_rate, med_adv_flag adv_flag, pooled_adv_flag_rate, zero_floor, zero_floor_40plus, null laws, null rk
from p where members >= 3
union all
select 'b_zero_floor', ch, party, bio, nm, null, bills, floor, null, adv_flag, null, null, null, laws, rk from r where rk <= 8
order by kind, ch, rk, party;

-- ===== totals: 24 SELECT/WITH statements (q14 failed to compile, rerun as q21) + 8 session-setup ALTER SESSION statements (2 per connection, 4 connections) = 32 of the 35 budget.
