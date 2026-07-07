-- FARA foreign-agent registrations by country represented (typed curated mart).
-- NB: FOREIGN_PRINCIPAL_COUNTRY is blank on most rows; COUNTRY_LOCATION_REPRESENTED
-- is the populated column (251 countries).
select
    country_location_represented as country,
    count(distinct registration_number) as registrations,
    count(distinct case when is_active_registration then registration_number end) as active_registrations
from THE_LIBRARY.INVESTIGATIONS.FOREIGN_AGENTS
where coalesce(country_location_represented, '') <> ''
group by 1
having count(distinct registration_number) >= 5
order by 2 desc
