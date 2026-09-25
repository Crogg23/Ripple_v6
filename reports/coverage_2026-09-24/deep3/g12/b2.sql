-- [q07_billstatus_same_point_by_congress]
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

-- [q08_billstatus_career_zero_law_sponsors]
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

-- [q09_bills_118_sponsor_peer]
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

-- [q10_missed_votes_118_119]
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

-- [q11_missed_votes_vs_senate_runs_2026]
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

-- [q12_senate_trades_covid_window]
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

-- [q13_senate_trades_paper_filers]
-- Per senator: how many PTRs are scanned paper (PDF-only rows), and when
select BIOGUIDE, max(SPINE_NAME) nm, count(distinct PTR_LINK) ptrs,
  count(distinct iff(ASSET_TYPE ilike 'PDF%', PTR_LINK, null)) pdf_ptrs,
  count(distinct iff(ASSET_TYPE ilike 'PDF%' and year(TRANSACTION_DATE) >= 2015, PTR_LINK, null)) pdf_ptrs_2015plus,
  count(*) rows_all, min(TRANSACTION_DATE) first_d, max(TRANSACTION_DATE) last_d,
  max(iff(ASSET_TYPE ilike 'PDF%', TRANSACTION_DATE, null)) last_pdf_d
from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES
group by 1 order by pdf_ptrs desc, ptrs desc;

-- [q14_senate_trades_repeat_rows_sample]
-- Identical rows inside one PTR: real multiple lots or a doubled load? top groups
select BIOGUIDE, SPINE_NAME, TRANSACTION_DATE, OWNER, TICKER, left(ASSET_DESCRIPTION, 60) asset, TRANSACTION_TYPE, AMOUNT_BAND, right(PTR_LINK, 45) ptr, count(*) copies,
  sum(count(*)) over () rows_in_groups, count(*) over () n_groups
from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES
group by all having count(*) > 1 order by copies desc, TRANSACTION_DATE desc limit 25;

-- [q15_spine_unmatched_vs_voteview]
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

-- [q16_bills_usps_naming_stage]
-- Post-office naming bills in POLITICS__BILLS: how far each got, 118th vs 119th
select CONGRESS, LATEST_STAGE, count(*) n, sum(iff(upper(BILL_TYPE) = 'HR',1,0)) house_bills, sum(iff(upper(BILL_TYPE) = 'S',1,0)) senate_bills
from LIBRARY_MARTS.POLITICS.POLITICS__BILLS
where TITLE ilike '%Postal Service%' and (TITLE ilike 'to designate%' or TITLE ilike 'to redesignate%' or TITLE ilike '%post office%')
group by 1,2 order by 1,2;
