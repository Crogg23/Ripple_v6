-- NRC secondary copy: company-by-year counts for the 30 companies with most reports 2020-2024 (names cleaned of punctuation),
-- plus 2019 and 2025 from the main copy for the before/after; biggest one-year jumps
with s as (select regexp_replace(upper(trim(RESPONSIBLE_COMPANY)), '[^A-Z0-9 ]', '') co, year(DATE_TIME_RECEIVED) y, RESPONSIBLE_ORG_TYPE ot
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS where nullif(trim(RESPONSIBLE_COMPANY), '') is not null),
m as (select regexp_replace(upper(trim(RESPONSIBLE_COMPANY)), '[^A-Z0-9 ]', '') co, year(DATE_TIME_RECEIVED) y
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS where year(DATE_TIME_RECEIVED) in (2019, 2025) and nullif(trim(RESPONSIBLE_COMPANY), '') is not null),
sc as (select co, count(*) tot, count_if(y = 2020) y20, count_if(y = 2021) y21, count_if(y = 2022) y22, count_if(y = 2023) y23, count_if(y = 2024) y24, any_value(ot) ot from s group by 1),
mc as (select co, count_if(y = 2019) y19, count_if(y = 2025) y25 from m group by 1),
k as (select sc.*, coalesce(mc.y19, 0) y19, coalesce(mc.y25, 0) y25,
        greatest(y20, y21, y22, y23, y24) mx, least(y20, y21, y22, y23, y24) mn from sc left join mc on sc.co = mc.co)
select * from (select 'top' t, * from k order by tot desc limit 30)
union all
select * from (select 'jump' t, * from k where tot >= 60 order by mx / (mn + 1) desc limit 15);
