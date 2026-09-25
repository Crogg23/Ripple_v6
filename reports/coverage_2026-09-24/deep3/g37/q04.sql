-- NRC secondary copy vs main copy: per-year counts, SEQNOS overlap, duplicate reports, the empty extra columns, blanks
with s as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS),
m as (select SEQNOS, DATE_TIME_RECEIVED, RESPONSIBLE_COMPANY from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS),
sy as (select year(DATE_TIME_RECEIVED) y, count(*) n, count(distinct SEQNOS) d, count_if(RESPONSIBLE_COMPANY is null or trim(RESPONSIBLE_COMPANY)='') blank from s group by 1),
my as (select year(DATE_TIME_RECEIVED) y, count(*) n, count(distinct SEQNOS) d, count_if(RESPONSIBLE_COMPANY is null or trim(RESPONSIBLE_COMPANY)='') blank from m group by 1)
select 'year' k, coalesce(sy.y,my.y)::text a, sy.n b, sy.d c, sy.blank d, my.n e, my.d f, my.blank g from sy full outer join my on sy.y=my.y
union all select 'overlap', 'secondary seqnos in main', count(distinct s.SEQNOS), count(distinct m.SEQNOS), count_if(s.DATE_TIME_RECEIVED=m.DATE_TIME_RECEIVED), count_if(coalesce(s.RESPONSIBLE_COMPANY,'')=coalesce(m.RESPONSIBLE_COMPANY,'')), null, null
  from s left join m on s.SEQNOS=m.SEQNOS
union all select 'extras', 'nonnull 1-5', count(EXTRA_COL_1), count(EXTRA_COL_2), count(EXTRA_COL_3), count(EXTRA_COL_4), count(EXTRA_COL_5), count(distinct _SOURCE_RUN_ID) from s
union all select 'calltype', CALL_TYPE||' / '||SOURCE, count(*), count(distinct SEQNOS), median(datediff('minute',DATE_TIME_RECEIVED,DATE_TIME_COMPLETE)), null, null, null from s group by 2
union all select 'orgtype', RESPONSIBLE_ORG_TYPE, count(*), count_if(RESPONSIBLE_COMPANY is null or trim(RESPONSIBLE_COMPANY)=''), null, null, null, null from s group by 2
order by 1, 2;
