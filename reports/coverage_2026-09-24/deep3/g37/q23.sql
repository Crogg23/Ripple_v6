-- NRC main copy: Norfolk Southern (any spelling) calls by month 2018-2021 and by responsible state 2019 vs 2020, with CSX alongside,
-- to see whether the 2020 fall is a one-month switch (practice or data change) or a slide, and whether 2019's peak is one place
with m as (select upper(trim(RESPONSIBLE_COMPANY)) co, DATE_TIME_RECEIVED d, RESPONSIBLE_STATE st
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS where year(DATE_TIME_RECEIVED) between 2018 and 2021),
c as (select d, st, case when co like '%NORFOLK SOUTHERN%' or co like '%NORFOLK SO%' or co like 'NS RAIL%' or co like 'N S RAIL%' or co like 'NSRR%' or co = 'NS' or co like 'NS %' then 'NS'
                         when co like '%CSX%' then 'CSX' else null end fam from m)
select 'month' k, to_char(date_trunc('month', d), 'YYYY-MM') a, count_if(fam = 'NS') ns, count_if(fam = 'CSX') csx, count(*) all_calls from c group by 2
union all
select 'state', st, count_if(fam = 'NS' and year(d) = 2019), count_if(fam = 'NS' and year(d) = 2020), count_if(fam = 'CSX' and year(d) = 2019) from c
where fam is not null group by 2 having count_if(fam = 'NS') >= 10
order by 1, 2;
