-- Washington Post fatal police shootings, by year and armed status (raw TEXT view — hand-cast).
select
    year(try_to_date("DATE")) as year,
    case
        when armed_with = 'gun' then 'Gun'
        when armed_with = 'knife' then 'Knife'
        when armed_with in ('unarmed', '') or armed_with is null then 'Unarmed / unknown'
        else 'Other'
    end as armed_with,
    count(*) as deaths
from THE_LIBRARY.CRIME_SECURITY.POLICE_FATAL_SHOOTINGS
where try_to_date("DATE") is not null
  and year(try_to_date("DATE")) < 2027
group by 1, 2
order by 1
