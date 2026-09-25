-- S04 Hospital general info: pull whole (5,432 rows) for type, ownership, readmission measures by CCN
SELECT ccn, facility_name, city_town, state, hospital_type, hospital_ownership, emergency_services, hospital_overall_rating,
       count_of_facility_readm_measures, count_of_readm_measures_better, count_of_readm_measures_worse,
       count_of_facility_mort_measures, count_of_mort_measures_worse, count_of_safety_measures_worse
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL
