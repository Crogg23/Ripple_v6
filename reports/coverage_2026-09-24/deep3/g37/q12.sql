-- NPDES individual permits only (3rd character 0; the permits every state must report DMRs for):
-- per state, chronic (8+ of 12 quarters with effluent violations, 2023Q3-2026Q2), six-year chronic, formal action ever / since mid-2021, median violations;
-- plus the 40 six-year chronic individual permits with the most effluent violations and no formal action ever
with q as (
  select NPDES_ID,
    count_if(YEARQTR between '20233' and '20262') rep_a,
    count_if(YEARQTR between '20233' and '20262' and try_to_number(NUME90_Q) > 0) qa,
    sum(iff(YEARQTR between '20233' and '20262', try_to_number(NUME90_Q), 0)) ea,
    count_if(YEARQTR between '20203' and '20232' and try_to_number(NUME90_Q) > 0) qb
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where YEARQTR between '20203' and '20262' and substr(NPDES_ID, 3, 1) = '0' group by 1),
fa as (select NPDES_ID, count(*) n_all, count_if(SETTLEMENT_ENTERED_DATE >= '2021-07-01') n_recent, max(SETTLEMENT_ENTERED_DATE) last_dt,
         sum(coalesce(FED_PENALTY_ASSESSED_AMT, 0) + coalesce(STATE_LOCAL_PENALTY_AMT, 0)) pen
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS group by 1),
ia as (select NPDES_ID, count_if(ACHIEVED_DATE >= '2021-07-01') n_recent from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS group by 1),
f as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
j as (select q.*, f.STATE_CODE, f.FACILITY_NAME, f.CITY, f.FACILITY_TYPE_CODE, f.IMPAIRED_WATERS, f.FACILITY_UIN,
        coalesce(fa.n_all, 0) fa_all, coalesce(fa.n_recent, 0) fa_recent, fa.last_dt, coalesce(fa.pen, 0) pen, coalesce(ia.n_recent, 0) ia_recent
      from q left join f on q.NPDES_ID = f.NPDES_ID left join fa on q.NPDES_ID = fa.NPDES_ID left join ia on q.NPDES_ID = ia.NPDES_ID where q.rep_a > 0)
select 'state' k, coalesce(STATE_CODE, 'ALL') a, count(*)::text b, count_if(qa >= 8)::text c, count_if(qa >= 8 and qb >= 8)::text d,
  count_if(qa >= 8 and fa_all > 0)::text e, count_if(qa >= 8 and fa_recent > 0)::text f, count_if(qa >= 8 and qb >= 8 and fa_all = 0)::text g,
  count_if(qa >= 8 and FACILITY_TYPE_CODE = 'MWD')::text h, median(iff(qa >= 8, ea, null))::text i, count_if(qa >= 8 and ia_recent > 0)::text m,
  count_if(ia_recent > 0)::text n2
from j group by rollup(STATE_CODE)
union all
select * from (select 'top', NPDES_ID, FACILITY_NAME, CITY || ', ' || STATE_CODE, coalesce(FACILITY_TYPE_CODE, '-') || ' / ' || coalesce(IMPAIRED_WATERS, '-'),
  qa::text || '+' || qb::text, ea::text, ia_recent::text, FACILITY_UIN, null, null, null
  from j where qa >= 8 and qb >= 8 and fa_all = 0 order by ea desc limit 40);
