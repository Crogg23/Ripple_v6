-- @rcra_la_ids_evaluated_since_2021_07
select f.id_number, f.facility_name, f.street_address, f.city_name, f.zip_code, f.hreport_universe_record,
  max(e.evaluation_start_date) last_ev, count(*) n_ev
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES f
join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS e on e.id_number = f.id_number
where f.activity_location = 'LA' and e.evaluation_start_date between '2021-07-01' and '2026-09-24'
group by 1, 2, 3, 4, 5, 6;
