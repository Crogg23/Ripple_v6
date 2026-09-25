-- NPDES chronic effluent violators by state: permits reporting 2023Q3-2026Q2, how many had effluent violations in 8+ of those 12 quarters,
-- how many of those also did in 8+ of the 12 quarters before, and how many got any formal action (since mid-2021, or ever) or informal action since mid-2021
with q as (
  select NPDES_ID,
    count_if(YEARQTR between '20233' and '20262') rep_a,
    count_if(YEARQTR between '20233' and '20262' and try_to_number(NUME90_Q) > 0) qa,
    sum(iff(YEARQTR between '20233' and '20262', try_to_number(NUME90_Q), 0)) ea,
    count_if(YEARQTR between '20203' and '20232' and try_to_number(NUME90_Q) > 0) qb
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where YEARQTR between '20203' and '20262' group by 1),
fa as (select NPDES_ID, count(*) n_all, count_if(SETTLEMENT_ENTERED_DATE >= '2021-07-01') n_recent,
         sum(coalesce(FED_PENALTY_ASSESSED_AMT, 0) + coalesce(STATE_LOCAL_PENALTY_AMT, 0)) pen
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS group by 1),
ia as (select NPDES_ID, count_if(ACHIEVED_DATE >= '2021-07-01') n_recent
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS group by 1),
f as (select NPDES_ID, STATE_CODE, FACILITY_TYPE_CODE, IMPAIRED_WATERS, substr(NPDES_ID, 3, 1) p3
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
j as (select f.*, q.rep_a, q.qa, q.ea, q.qb, coalesce(fa.n_all, 0) fa_all, coalesce(fa.n_recent, 0) fa_recent, coalesce(fa.pen, 0) pen,
         coalesce(ia.n_recent, 0) ia_recent
      from q left join f on q.NPDES_ID = f.NPDES_ID left join fa on q.NPDES_ID = fa.NPDES_ID left join ia on q.NPDES_ID = ia.NPDES_ID
      where q.rep_a > 0)
select coalesce(STATE_CODE, '(no facility row)') st, count(*) reporting, count_if(qa >= 8) chronic, count_if(qa >= 8 and qb >= 8) chronic6,
  count_if(qa >= 8 and fa_recent > 0) chr_formal_recent, count_if(qa >= 8 and fa_all > 0) chr_formal_ever,
  count_if(qa >= 8 and ia_recent > 0) chr_informal_recent, count_if(qa >= 8 and fa_all = 0 and ia_recent = 0) chr_nothing,
  count_if(qa >= 8 and FACILITY_TYPE_CODE = 'MWD') chr_mwd, count_if(qa >= 8 and p3 = '0') chr_individual,
  count_if(qa >= 8 and IMPAIRED_WATERS is not null) chr_impaired, count_if(IMPAIRED_WATERS is not null) rep_impaired,
  sum(iff(qa >= 8, ea, 0)) chr_e90, count_if(p3 = '0') rep_individual, count_if(p3 = '0' and qa >= 8) ind_chronic
from j group by rollup(coalesce(STATE_CODE, '(no facility row)')) order by chronic desc nulls first;
