-- One join: CourtListener 4th Cir dockets (YY-NNNN) to FJC 4th Cir appeals (YY0NNNN); label agreement and coverage both ways
with cl0 as (
  select regexp_substr(d.DOCKET_NUMBER, '(\d{2})-(\d{4})', 1, 1, 'e', 1) yy,
         regexp_substr(d.DOCKET_NUMBER, '(\d{2})-(\d{4})', 1, 1, 'e', 2) nn,
         c.PRECEDENTIAL_STATUS st, year(c.DATE_FILED) yr
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS c
  join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS d on d.ID = c.DOCKET_ID
  where d.COURT_ID = 'ca4' and c.DATE_FILED >= '2018-07-01' and c.DATE_FILED < '2026-07-01'),
cl as (
  select yy || '0' || nn dk, max(iff(st = 'Published', 1, 0)) cl_pub, max(iff(st = 'Unpublished', 1, 0)) cl_unpub, min(yr) cl_yr
  from cl0 where yy is not null and nn is not null group by 1),
f as (
  select DOCKET dk, max(TAPE_YEAR) ty,
    max(case when PUBLICATION_STATUS in ('1','2','4') then 2 when PUBLICATION_STATUS in ('3','5') then 1 else 0 end) fclass
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
  where CIRCUIT = '4' and TAPE_YEAR between '2019' and '2026'
  group by 1)
select 'fjc_base' side, f.ty yr,
  case f.fclass when 2 then 'FJC pub' when 1 then 'FJC unpub' else 'FJC none' end fjc,
  case when cl.dk is null then 'no CL' when cl.cl_pub = 1 then 'CL pub' when cl.cl_unpub = 1 then 'CL unpub' else 'CL other' end clx,
  count(*) n
from f left join cl on cl.dk = f.dk
group by 1,2,3,4
union all
select 'cl_base' side, to_char(cl.cl_yr) yr,
  case when f.dk is null then 'no FJC' when f.fclass = 2 then 'FJC pub' when f.fclass = 1 then 'FJC unpub' else 'FJC none' end fjc,
  case when cl.cl_pub = 1 then 'CL pub' when cl.cl_unpub = 1 then 'CL unpub' else 'CL other' end clx,
  count(*) n
from cl left join f on f.dk = cl.dk
group by 1,2,3,4
order by 1,2,3,4;
