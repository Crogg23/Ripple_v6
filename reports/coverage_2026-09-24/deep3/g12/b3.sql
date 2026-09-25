-- [q17_bills_advanced_flag_trap]
-- Does ADVANCED_PAST_COMMITTEE count a subcommittee referral as "advanced"? 118th, law-eligible bills, by chamber
select iff(upper(BILL_TYPE) in ('HR','HJRES'),'House','Senate') ch, ADVANCED_PAST_COMMITTEE adv, LATEST_STAGE, count(*) n,
  sum(iff(LATEST_ACTION_TEXT ilike 'Referred to the Subcommittee%',1,0)) latest_is_subcmte_referral,
  sum(iff(LATEST_ACTION_TEXT ilike 'Referred to%' or LATEST_ACTION_TEXT ilike 'Read twice and referred%',1,0)) latest_is_any_referral,
  mode(left(LATEST_ACTION_TEXT, 80)) top_latest_text
from LIBRARY_MARTS.POLITICS.POLITICS__BILLS
where CONGRESS = 118 and IS_LAW_ELIGIBLE
group by 1,2,3 order by 1,2,3;

-- [q18_missed_votes_by_month_119_house]
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

-- [q19_laws_by_type_same_point]
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

-- [q20_zero_law_sponsors_companion_test]
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

-- [q21_senate_trades_repeat_rows]
-- Identical rows inside one PTR: how many, whose, and the biggest groups
with g as (
  select BIOGUIDE, SPINE_NAME, TRANSACTION_DATE, OWNER, TICKER, ASSET_DESCRIPTION, TRANSACTION_TYPE, AMOUNT_BAND, PTR_LINK, count(*) copies
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES
  group by BIOGUIDE, SPINE_NAME, TRANSACTION_DATE, OWNER, TICKER, ASSET_DESCRIPTION, TRANSACTION_TYPE, AMOUNT_BAND, PTR_LINK
  having count(*) > 1),
x as (select g.*, count(*) over () n_groups, sum(copies) over () rows_in_groups, sum(copies) over (partition by BIOGUIDE) sen_rows from g)
select SPINE_NAME, TRANSACTION_DATE, OWNER, TICKER, left(ASSET_DESCRIPTION, 50) asset, TRANSACTION_TYPE, AMOUNT_BAND, right(PTR_LINK, 40) ptr, copies, n_groups, rows_in_groups, sen_rows
from x order by sen_rows desc, copies desc, TRANSACTION_DATE desc limit 20;

-- [q22_senate_trades_pdf_rows_sample]
-- What a paper-filer row holds: Burr, Blumenthal, Boozman, Feinstein, 2019-2020
select SPINE_NAME, TRANSACTION_DATE, OWNER, TICKER, left(ASSET_DESCRIPTION, 70) asset, ASSET_TYPE, TRANSACTION_TYPE, AMOUNT_BAND, left(COMMENT, 40) cmt, PTR_LINK
from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES
where BIOGUIDE in ('B001135','B001277','B001236','F000062') and TRANSACTION_DATE >= '2019-10-01'
order by TRANSACTION_DATE limit 20;
