-- PHMSA gas transmission/gathering accidents 2020-2024 joined to the NRC secondary copy on report number:
-- hours from the accident's local time (shifted to Eastern by TIME_ZONE) to the NRC call; plus operators who wrote "required but not made"
with ph as (select *, row_number() over (partition by REPORT_NUMBER order by SUPPLEMENTAL_NUMBER desc nulls last) rn
            from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS),
p as (select * from ph where rn = 1),
n as (select SEQNOS, DATE_TIME_RECEIVED, RESPONSIBLE_COMPANY from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS),
j as (select p.REPORT_NUMBER, p.OPERATOR_NAME, p.INCIDENT_YEAR, p.LOCAL_DATETIME, p.TIME_ZONE, p.TOTAL_FATALITIES, p.TOTAL_INJURIES, p.COMMODITY_RELEASED_TYPE,
        p.UNINTENTIONAL_RELEASE_VOLUME, p.OPERATOR_STATE, n.DATE_TIME_RECEIVED, n.RESPONSIBLE_COMPANY,
        datediff('minute', dateadd('hour', case upper(p.TIME_ZONE) when 'EASTERN' then 0 when 'CENTRAL' then 1 when 'MOUNTAIN' then 2 when 'PACIFIC' then 3
                    when 'ALASKA' then 4 when 'HAWAII' then 6 else 1 end, p.LOCAL_DATETIME), n.DATE_TIME_RECEIVED) / 60.0 lag_h
      from p join n on trim(p.NRC_REPORT_NUMBER) = n.SEQNOS)
select 'bucket' k, case when lag_h < 0 then 'a <0h' when lag_h <= 1 then 'b 0-1h' when lag_h <= 2 then 'c 1-2h' when lag_h <= 6 then 'd 2-6h'
    when lag_h <= 24 then 'e 6-24h' when lag_h <= 168 then 'f 1-7d' else 'g >7d' end a, count(*)::text b, count_if(TIME_ZONE is null)::text c,
  sum(TOTAL_FATALITIES)::text d, sum(TOTAL_INJURIES)::text e, null f, null g, null h
from j group by 2
union all
select * from (select 'late', REPORT_NUMBER, OPERATOR_NAME, LOCAL_DATETIME::text || ' ' || coalesce(TIME_ZONE, '?'), DATE_TIME_RECEIVED::text, round(lag_h, 1)::text,
  coalesce(TOTAL_FATALITIES, 0)::text || 'd/' || coalesce(TOTAL_INJURIES, 0)::text || 'i', COMMODITY_RELEASED_TYPE, UNINTENTIONAL_RELEASE_VOLUME::text
  from j where lag_h > 24 order by lag_h desc limit 25)
union all
select * from (select 'op', OPERATOR_NAME, count(*)::text, median(lag_h)::text, count_if(lag_h > 6)::text, count_if(lag_h > 24)::text, null, null, null
  from j group by 2 having count(*) >= 5 order by median(lag_h) desc limit 20)
union all
select 'notmade', OPERATOR_NAME, count(*)::text, listagg(distinct INCIDENT_YEAR::text, ',') within group (order by INCIDENT_YEAR::text), sum(TOTAL_FATALITIES)::text, sum(TOTAL_INJURIES)::text,
  listagg(distinct REPORT_NUMBER, ',') within group (order by REPORT_NUMBER), null, null
from p where NRC_REPORT_NUMBER ilike '%NOT MADE%' group by 2
union all
select 'nrcvals', iff(try_to_number(trim(NRC_REPORT_NUMBER)) is null, coalesce(NRC_REPORT_NUMBER, '(null)'), 'numeric'), count(*)::text, null, null, null, null, null, null from p group by 2;
