-- FBI NICS firearm background checks, national monthly totals (raw TEXT view — hand-cast).
select
    try_to_date(month || '-01', 'YYYY-MM-DD') as month,
    sum(try_to_number(totals)) as total_checks,
    sum(try_to_number(handgun)) as handgun_checks,
    sum(try_to_number(long_gun)) as long_gun_checks
from THE_LIBRARY.CRIME_SECURITY.GUN_BACKGROUND_CHECKS
where try_to_date(month || '-01', 'YYYY-MM-DD') is not null
group by 1
order by 1
