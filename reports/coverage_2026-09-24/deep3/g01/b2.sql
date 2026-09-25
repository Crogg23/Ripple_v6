-- @estab_sample2
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
where establishment_name ilike 'sterigenics%' limit 2
-- @estab_profile
select count(*) n, count(distinct fei_number) fei, count(distinct registration_number) reg,
  count(distinct owner_operator_number) owners,
  count(distinct fei_number || '|' || coalesce(k_number,'') || '|' || coalesce(pma_number,'') || '|' || coalesce(proprietary_name,'')) fei_prod_combos,
  count_if(status_code = '1') s1, count_if(status_code = '5') s5, count(distinct status_code) n_status,
  count(distinct reg_expiry_date_year) n_expiry,
  count_if(establishment_type::string ilike '%steril%') steril_rows,
  count(distinct iff(establishment_type::string ilike '%steril%', fei_number, null)) steril_fei,
  count(distinct iff(establishment_type::string ilike '%steril%' and iso_country_code = 'US', fei_number, null)) steril_fei_us,
  count_if(k_number is not null and k_number <> '') k_filled,
  count(distinct _source_run_id) runs
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
-- @vasuicide_national_all
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_NATIONAL
