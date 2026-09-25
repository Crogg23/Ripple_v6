-- RERUN of q13 without _INGESTED_AT (this table has no lineage column; q13 failed on it)
-- Slave voyages: trap check. Fill rates of the columns a story would lean on, totals of the editors' estimates,
-- impossible values (more landed than embarked, death share outside 0-1), non-numeric text in number columns
with t as (select * from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC)
select count(*) n,
  count_if(try_to_number(SLAXIMP) is not null) slaximp_n, sum(try_to_number(SLAXIMP)) slaximp_sum,
  count_if(try_to_number(SLAMIMP) is not null) slamimp_n, sum(try_to_number(SLAMIMP)) slamimp_sum,
  count_if(try_to_number(TSLAVESD) is not null) tslavesd_n, count_if(try_to_number(SLAARRIV) is not null) slaarriv_n,
  count_if(try_to_double(VYMRTRAT) is not null) vymrtrat_n, count_if(try_to_double(VYMRTRAT) < 0 or try_to_double(VYMRTRAT) > 1) vymrtrat_bad,
  count_if(try_to_number(SLAMIMP) > try_to_number(SLAXIMP)) landed_gt_embarked,
  count_if(nullif(trim(SLAXIMP),'') is not null and try_to_number(SLAXIMP) is null) slaximp_nonnum,
  listagg(distinct iff(nullif(trim(SLAXIMP),'') is not null and try_to_number(SLAXIMP) is null, SLAXIMP, null), '|') slaximp_nonnum_vals,
  count_if(nullif(trim(PTDEPIMP),'') is not null) ptdep_n, count_if(nullif(trim(MJSLPTIMP),'') is not null) mjslpt_n,
  count_if(nullif(trim(NATINIMP),'') is not null) natinimp_n, count_if(nullif(trim(OWNERA),'') is not null) ownera_n,
  count_if(nullif(trim(YEARDEP),'') is not null) yeardep_n, count_if(nullif(trim(YEARAM),'') is not null) yearam_n,
  count_if(try_to_number(YEARAM) >= 1808) yearam_1808on,
  listagg(distinct FATE4, ',') fate4_vals, listagg(distinct XMIMPFLAG, ',') xmimpflag_vals
from t;
