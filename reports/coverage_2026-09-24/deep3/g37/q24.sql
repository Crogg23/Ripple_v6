-- NPDES sensitivity: does the Missouri/Ohio share of chronic-with-no-formal-action survive other thresholds?
-- Individual permits; thresholds 6, 8, 10 of 12 quarters in both windows; share of no-formal-action permits in MO, OH, rest; plus MO/OH/all impaired and MWD counts at 8
with q as (
  select NPDES_ID, substr(NPDES_ID, 1, 2) st,
    count_if(YEARQTR between '20233' and '20262' and try_to_number(NUME90_Q) > 0) qa,
    count_if(YEARQTR between '20203' and '20232' and try_to_number(NUME90_Q) > 0) qb
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where YEARQTR between '20203' and '20262' and substr(NPDES_ID, 3, 1) = '0' group by 1, 2),
fa as (select distinct NPDES_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS),
f as (select NPDES_ID, FACILITY_TYPE_CODE ft, IMPAIRED_WATERS imp from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
j as (select q.*, iff(fa.NPDES_ID is null, 1, 0) nofa, f.ft, f.imp from q left join fa on q.NPDES_ID = fa.NPDES_ID left join f on q.NPDES_ID = f.NPDES_ID),
t as (select 6 thr union all select 8 union all select 10 union all select 12)
select t.thr, iff(j.st in ('MO', 'OH'), j.st, 'REST') grp, count(*) chronic_both, sum(nofa) no_formal, round(sum(nofa) / count(*), 3) share_no_formal,
  count_if(nofa = 1 and imp is not null) no_formal_impaired, count_if(nofa = 1 and ft = 'MWD') no_formal_mwd
from j join t on j.qa >= t.thr and j.qb >= t.thr
group by 1, 2 order by 1, 2;
