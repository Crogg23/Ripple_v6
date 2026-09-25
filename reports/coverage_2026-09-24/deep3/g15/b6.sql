-- [q20_judge_timing_age_bands]
-- Dull-explanation test: the same-party pool is 1.5-2 years older. Senior-status rate inside age bands (age on inauguration day), eligible judges only
with pres as (select column1 pname, column2 pparty, column3::date s, column4::date e from values
   ('Bush43','Republican','2001-01-20','2009-01-20'), ('Obama','Democratic','2009-01-20','2017-01-20'), ('Trump1','Republican','2017-01-20','2021-01-20'), ('Biden','Democratic','2021-01-20','2025-01-20')),
s as (select sv.NID, sv.PARTY_OF_APPOINTING_PRESIDENT pa, sv.COMMISSION_DATE cd, sv.SENIOR_STATUS_DATE sd, sv.TERMINATION_DATE td, fj.BIRTH_YEAR by_
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE sv join LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE fj on fj.NID = sv.NID
      where sv.COURT_TYPE ilike '%Appeals%'),
pool as (select p.pname, p.s, iff(s.pa = p.pparty, 'same', 'other') rel, iff(s.sd >= p.s and s.sd < p.e, 1, 0) went, year(p.s) - s.by_ age0
         from pres p join s on s.cd < p.s and coalesce(s.sd, '9999-12-31'::date) >= p.s and coalesce(s.td, '9999-12-31'::date) >= p.s
         where s.pa in ('Republican','Democratic')
           and (year(p.s) - s.by_) >= 65 and (year(p.s) - s.by_) + datediff(year, s.cd, p.s) >= 80)
select pname, min(s) term_start, case when age0 < 70 then 'a 65-69' when age0 < 75 then 'b 70-74' else 'c 75+' end band,
  sum(iff(rel = 'same', 1, 0)) n_same, sum(iff(rel = 'same', went, 0)) went_same,
  sum(iff(rel = 'other', 1, 0)) n_other, sum(iff(rel = 'other', went, 0)) went_other
from pool group by 1, 3 order by 2, 3;
