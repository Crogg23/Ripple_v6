-- @vv_rollcall_party_split
-- Voteview 118th-119th: one row per roll call. Yea/nay by party, and three named members' votes, with the question and description
-- (from the small roll-call table, falling back to the long roll-call table), to test whether vote mix explains the party-break drop.
with m as (
  select CONGRESS, CHAMBER, try_to_double(ICPSR)::number icpsr, any_value(PARTY_CODE) party_code, any_value(BIONAME) nm
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS
  where CONGRESS in (118, 119) and CHAMBER in ('House', 'Senate') group by 1, 2, 3),
v as (
  select v.CONGRESS, v.CHAMBER, v.ROLLNUMBER rn, v.CAST_CODE cc, m.nm,
         case when try_to_number(to_varchar(m.party_code)) = 200 then 'R'
              when try_to_number(to_varchar(m.party_code)) in (100, 328) then 'D' else 'O' end p
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v
  left join m on m.CONGRESS = v.CONGRESS and m.CHAMBER = v.CHAMBER and m.icpsr = v.ICPSR),
rc as (
  select CONGRESS, CHAMBER, rn,
    sum(iff(p = 'D' and cc = 1, 1, 0)) dy, sum(iff(p = 'D' and cc = 6, 1, 0)) dn,
    sum(iff(p = 'R' and cc = 1, 1, 0)) ry, sum(iff(p = 'R' and cc = 6, 1, 0)) rnay,
    max(iff(nm ilike 'FETTERMAN%', cc, null)) fett,
    max(iff(nm ilike 'CUELLAR%', cc, null)) cuel,
    max(iff(nm ilike 'FITZPATRICK%', cc, null)) fitz
  from v group by 1, 2, 3),
r as (
  select CONGRESS, CHAMBER, try_to_number(to_varchar(ROLLNUMBER)) rn, VOTE_DATE, VOTE_QUESTION, VOTE_RESULT, BILL_NUMBER, left(VOTE_DESC, 90) descr
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS where CONGRESS in (118, 119)),
mt as (
  select try_to_number(to_varchar(CONGRESS)) cg,
         case when lower(CHAMBER) in ('house', 'rep', 'h') then 'House' when lower(CHAMBER) in ('senate', 'sen', 's') then 'Senate' end ch,
         try_to_number(to_varchar(ROLLNUMBER)) rn, VOTE_QUESTION q2, left(DTL_DESC, 90) dtl
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META where try_to_number(to_varchar(CONGRESS)) in (118, 119))
select rc.*, r.VOTE_DATE, r.VOTE_QUESTION, mt.q2, r.VOTE_RESULT, r.BILL_NUMBER, r.descr, mt.dtl
from rc
left join r on r.CONGRESS = rc.CONGRESS and r.CHAMBER = rc.CHAMBER and r.rn = rc.rn
left join mt on mt.cg = rc.CONGRESS and mt.ch = rc.CHAMBER and mt.rn = rc.rn
order by 1, 2, 3;

-- @fjc_harlan_ids
-- Which FJC ids hold a Harlan? Is Justice Harlan II (born 1899) in the FJC table under another id?
select NID, JID, FULL_NAME, SUFFIX, BIRTH_YEAR, DEATH_YEAR
from LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE where LAST_NAME ilike 'Harlan%';

-- @who_won_president_years
-- Does another table carry 2020 and 2024 presidential results by state?
select OFFICE, YEAR, count(*) n, count(distinct STATE) states
from LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON
where OFFICE ilike '%pres%' group by 1, 2 order by 1, 2;
