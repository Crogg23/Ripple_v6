-- NPDES Missouri and Ohio eyeball: six-year chronic individual permits with no formal action on that permit.
-- Robustness: formal actions on ANY permit sharing the same FRS ID; informal actions ever; compliance-schedule or permit-schedule records; facility type
with q as (
  select NPDES_ID,
    count_if(YEARQTR between '20233' and '20262' and try_to_number(NUME90_Q) > 0) qa,
    sum(iff(YEARQTR between '20233' and '20262', try_to_number(NUME90_Q), 0)) ea,
    count_if(YEARQTR between '20203' and '20232' and try_to_number(NUME90_Q) > 0) qb,
    sum(iff(YEARQTR between '20203' and '20232', try_to_number(NUME90_Q), 0)) eb
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where YEARQTR between '20203' and '20262' and substr(NPDES_ID, 3, 1) = '0' group by 1 having qa >= 8 and qb >= 8),
fac as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
fa as (select NPDES_ID, count(*) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS group by 1),
fa_uin as (select f2.FACILITY_UIN, count(*) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS a
           join fac f2 on a.NPDES_ID = f2.NPDES_ID where f2.FACILITY_UIN is not null group by 1),
ia as (select NPDES_ID, count(*) n, max(ACHIEVED_DATE) last_ia from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS group by 1),
cs as (select NPDES_ID, count(*) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_CS_VIOLATIONS group by 1),
ps as (select NPDES_ID, count(*) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_PS_VIOLATIONS group by 1),
j as (select q.*, f.STATE_CODE st, f.FACILITY_NAME, f.CITY, f.FACILITY_TYPE_CODE ft, f.IMPAIRED_WATERS imp, f.FACILITY_UIN,
        coalesce(fa.n, 0) fa_n, coalesce(fu.n, 0) fa_uin_n, coalesce(ia.n, 0) ia_n, ia.last_ia, coalesce(cs.n, 0) cs_n, coalesce(ps.n, 0) ps_n
      from q join fac f on q.NPDES_ID = f.NPDES_ID left join fa on q.NPDES_ID = fa.NPDES_ID left join fa_uin fu on f.FACILITY_UIN = fu.FACILITY_UIN
        left join ia on q.NPDES_ID = ia.NPDES_ID left join cs on q.NPDES_ID = cs.NPDES_ID left join ps on q.NPDES_ID = ps.NPDES_ID)
select 'sum' k, st a, count(*)::text b, count_if(fa_n = 0)::text c, count_if(fa_n = 0 and fa_uin_n = 0)::text d, count_if(fa_n = 0 and ia_n = 0)::text e,
  count_if(fa_n = 0 and (cs_n > 0 or ps_n > 0))::text g, count_if(fa_n = 0 and ft = 'MWD')::text h, count_if(fa_n = 0 and ft in ('CTG', 'MWD', 'STF', 'FDF'))::text i,
  median(iff(fa_n = 0, ea + eb, null))::text m
from j group by rollup(st) having count(*) >= 40 or st is null
union all
select * from (select 'row', NPDES_ID, FACILITY_NAME || ' / ' || CITY, coalesce(ft, '-') || ' / ' || coalesce(imp, '-'), qa::text || '+' || qb::text || ' q; ' || ea::text || '+' || eb::text || ' viol',
  'fa_uin=' || fa_uin_n::text, 'ia=' || ia_n::text || ' last ' || coalesce(last_ia::text, '-'), 'cs=' || cs_n::text || ' ps=' || ps_n::text, st, null
  from j where st in ('MO', 'OH') and fa_n = 0 order by st, ea + eb desc limit 30);
