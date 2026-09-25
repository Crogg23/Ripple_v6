-- [q19_judge_timing_robustness]
-- Robustness for the senior-status gap: per-circuit spread, age and service of the eligible pools, and what the "waiters" did once the White House changed party
with pres as (select column1 pname, column2 pparty, column3::date s, column4::date e from values
   ('Obama','Democratic','2009-01-20','2017-01-20'), ('Trump1','Republican','2017-01-20','2021-01-20'), ('Biden','Democratic','2021-01-20','2025-01-20'), ('Trump2','Republican','2025-01-20','2026-09-01')),
s as (select sv.NID, sv.COURT_NAME, sv.PARTY_OF_APPOINTING_PRESIDENT pa, sv.COMMISSION_DATE cd, sv.SENIOR_STATUS_DATE sd, sv.TERMINATION_DATE td, sv.TERMINATION term, fj.BIRTH_YEAR by_, fj.FULL_NAME fname
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE sv join LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE fj on fj.NID = sv.NID
      where sv.COURT_TYPE ilike '%Appeals%'),
pool as (select p.pname, p.pparty, p.s, p.e, s.*, iff(s.pa = p.pparty, 'same', 'other') rel,
           iff(s.sd >= p.s and s.sd < p.e, 1, 0) went, year(p.s) - s.by_ age0, datediff(year, s.cd, p.s) svc0
         from pres p join s on s.cd < p.s and coalesce(s.sd, '9999-12-31'::date) >= p.s and coalesce(s.td, '9999-12-31'::date) >= p.s
         where s.pa in ('Republican','Democratic')
           and (year(p.s) - s.by_) >= 65 and (year(p.s) - s.by_) + datediff(year, s.cd, p.s) >= 80)
select 'circuit' k, pname, rel, regexp_replace(COURT_NAME, 'U.S. Court of Appeals for the ', '') c1, count(*)::string c2, sum(went)::string c3, null c4
from pool where pname in ('Trump1','Biden') group by 2,3,4
union all
select 'age', pname, rel, 'median age / service yrs / n', median(age0)::string, median(svc0)::string, count(*)::string from pool group by 2,3
union all
select 'waiters', pname, rel, 'stayed through term, still active at next inauguration',
  count(*)::string,
  sum(iff(sd >= e and sd < dateadd(month, 17, e),1,0))::string,
  sum(iff(sd >= e,1,0))::string || ' went senior after; ' || sum(iff(sd is null and td >= e,1,0))::string || ' left another way; ' || sum(iff(sd is null and td is null,1,0))::string || ' still active'
from pool where went = 0 and rel = 'other' and pname in ('Obama','Trump1','Biden')
  and coalesce(sd, '9999-12-31'::date) >= e and coalesce(td, '9999-12-31'::date) >= e
group by 2,3
union all
select 'waiter_names_biden', pname, rel, fname, regexp_replace(COURT_NAME, 'U.S. Court of Appeals for the ', ''), by_::string,
  coalesce('senior ' || sd::string, 'left ' || td::string || ' ' || term, 'active')
from pool where pname = 'Biden' and rel = 'other' and went = 0
order by 1, 2, 3, 5 desc;
