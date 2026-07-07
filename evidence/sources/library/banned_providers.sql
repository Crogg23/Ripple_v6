-- OIG-excluded (banned) healthcare providers by exclusion year (LEIE, raw TEXT view — hand-cast).
-- EXCLDATE is YYYYMMDD text; TRY_TO_DATE drops the junk rows.
select
    year(try_to_date(excldate, 'YYYYMMDD')) as excl_year,
    case when coalesce(busname, '') <> '' then 'Business' else 'Individual' end as provider_kind,
    count(*) as exclusions
from THE_LIBRARY.HEALTH.BANNED_HEALTHCARE_PROVIDERS
where try_to_date(excldate, 'YYYYMMDD') is not null
  and year(try_to_date(excldate, 'YYYYMMDD')) between 1977 and 2026
group by 1, 2
order by 1
