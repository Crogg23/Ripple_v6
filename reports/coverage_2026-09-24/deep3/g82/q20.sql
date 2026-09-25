-- FEMA independent source: distinct disaster numbers by declaration year in the FEMA Individual Assistance registrations table (Feb-Aug and full year), to test whether fewer disasters were declared
select year(DECLARATION_DATE) y, count(distinct DISASTER_NUMBER) disasters_all,
  count(distinct iff(month(DECLARATION_DATE) between 2 and 8, DISASTER_NUMBER, null)) disasters_feb_aug,
  count(*) registrations, min(DECLARATION_DATE) first_decl, max(DECLARATION_DATE) last_decl, max(APPLIED_DATE) last_applied
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
where DECLARATION_DATE >= '2019-01-01'
group by 1 order by 1
