-- @vv_senate119_close_and_warpowers
-- 119th Senate: every war-powers roll call ("Armed Forces from hostilities") and every party vote decided by 3 or fewer,
-- with the tally by party, who crossed their party's majority, and who did not vote.
with m as (
  select try_to_double(ICPSR)::number icpsr, any_value(PARTY_CODE) party_code, any_value(BIONAME) nm, any_value(STATE_ABBREV) st
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS
  where CONGRESS = 119 and CHAMBER = 'Senate' group by 1),
v as (
  select v.ROLLNUMBER rn, v.CAST_CODE cc, m.nm, m.st,
         case when try_to_number(to_varchar(m.party_code)) = 200 then 'R'
              when try_to_number(to_varchar(m.party_code)) in (100, 328) then 'D' else 'O' end p
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v
  left join m on m.icpsr = v.ICPSR
  where v.CONGRESS = 119 and v.CHAMBER = 'Senate'),
rc as (
  select rn,
    sum(iff(p = 'D' and cc = 1, 1, 0)) dy, sum(iff(p = 'D' and cc = 6, 1, 0)) dn,
    sum(iff(p = 'R' and cc = 1, 1, 0)) ry, sum(iff(p = 'R' and cc = 6, 1, 0)) rnay
  from v group by 1),
rc2 as (
  select rc.*, iff(dy > dn, 1, iff(dn > dy, 6, null)) dpos, iff(ry > rnay, 1, iff(rnay > ry, 6, null)) rpos from rc),
r as (
  select try_to_number(to_varchar(ROLLNUMBER)) rn, VOTE_DATE, VOTE_QUESTION, VOTE_RESULT, BILL_NUMBER, left(VOTE_DESC, 200) descr
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS where CONGRESS = 119 and CHAMBER = 'Senate'),
sel as (
  select rc2.*, r.VOTE_DATE, r.VOTE_QUESTION, r.VOTE_RESULT, r.BILL_NUMBER, r.descr
  from rc2 join r on r.rn = rc2.rn
  where r.descr ilike '%Armed Forces from hostilities%'
     or (dpos is not null and rpos is not null and dpos <> rpos and abs((dy + ry) - (dn + rnay)) <= 3))
select sel.rn, sel.VOTE_DATE, sel.VOTE_QUESTION, sel.VOTE_RESULT, sel.BILL_NUMBER, sel.descr, sel.dy, sel.dn, sel.ry, sel.rnay, sel.dpos, sel.rpos,
  listagg(case when v.cc in (1, 6) and v.cc <> iff(v.p = 'R', sel.rpos, sel.dpos) then v.nm || ' (' || v.p || '-' || v.st || ')' end, '; ') crossers,
  listagg(case when v.cc = 9 then v.nm || ' (' || v.p || ')' end, '; ') not_voting
from sel join v on v.rn = sel.rn
group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
order by 1;
