-- FRA casualties (the source file): do fatalities reconcile with the deaths table by year, and are suicides flagged?
-- Fatality rows by year x COVERED_DATA_REASON x CASUALTY_OCCURRENCE_CODE for trespassers, 2008-2025
select INCIDENT_YEAR, TYPE_OF_PERSON ilike 'Trespass%' tresp, COVERED_DATA_CODE, COVERED_DATA_REASON, CASUALTY_OCCURRENCE_CODE, count(*) n
from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
where FATALITY = 'Yes' and INCIDENT_YEAR between 2008 and 2025
group by 1,2,3,4,5 order by 1,2,3,4,5;
