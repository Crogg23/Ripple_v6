-- [a1_nuke_all]
select entity, code, year, number_of_nuclear_warheads
from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_OWID_NUCLEAR_WARHEADS
order by entity, year

-- [a2_jpml_all]
select *
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_JPML_PENDING_MDLS

-- [a3_eopr_all]
select *
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_EO_PR

-- [a4_soi_all]
select *
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_SOI_CHARITIES

-- [a5_istat_flows]
select dataflow_id, freq, count(*) n, count(distinct series_key) series,
  count(distinct series_key, date) series_dates, min(date) d0, max(date) d1,
  count(distinct date) dates, count_if(is_missing_value) missing, count_if(obs_value is null) null_val,
  count_if(obs_status is not null and obs_status <> '') status_set, listagg(distinct obs_status, ',') statuses,
  count(distinct country) countries, any_value(country) a_country, count(distinct _source_run_id) runs,
  count(distinct istat_obs_id) ids, count_if(unit_mult is not null) unit_mult_set,
  count_if(unit_measure is not null and unit_measure <> '') unit_set, count_if(is_normal_value) normal_true,
  count_if(obs_value_absolute <> abs(obs_value)) abs_mismatch, count_if(obs_value < 0) negatives,
  any_value(dimension_keys) sample_dims, any_value(series_key) sample_series
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_IT_ISTAT
group by 1, 2
order by n desc

-- [a6_istat_years]
select dataflow_id, obs_year, count(*) n, count(distinct series_key) series, count(distinct date) dates,
  min(date) d0, max(date) d1, round(median(obs_value), 2) med_val
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_IT_ISTAT
group by 1, 2
order by 1, 2

-- [a7_fjc_mdl_probe]
select count(*) n, count_if(mdl_docket is not null and trim(mdl_docket) <> '') mdl_set,
  count(distinct mdl_docket) mdl_vals, count(distinct case_record_id) ids,
  count(distinct district, office, docket, file_date) case_keys,
  min(file_date) f0, max(file_date) f1, max(tape_year) max_tape, min(tape_year) min_tape,
  count(distinct tape_year) tapes,
  (select listagg(v || ':' || c, ' | ') from (select mdl_docket v, count(*) c from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
     where mdl_docket is not null and trim(mdl_docket) <> '' group by 1 order by 2 desc limit 25)) top_mdl,
  (select listagg(l || ':' || c, ' | ') from (select length(mdl_docket) l, count(*) c from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
     where mdl_docket is not null group by 1 order by 1)) mdl_lengths,
  (select listagg(t || ':' || c, ' | ') from (select tape_year t, count(*) c from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
     group by 1 order by 1 desc limit 8)) tapes_top
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL

-- [a8_bmf_pr_presence]
select 'ECON_BMF' src, count(*) n, count_if(state = 'PR') pr_rows, count(distinct ein) eins,
  max(try_to_number(tax_period)) max_tax_period, max(ruling_date) max_ruling, count(distinct _source_url) urls,
  listagg(distinct _source_url, ' ; ') within group (order by _source_url) url_list
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF
union all
select 'CR_EO_BMF', count(*), count_if(state = 'PR'), count(distinct ein),
  max(try_to_number(tax_period_yyyymm)), max(ruling_yyyymm), count(distinct _source_run_id), null
from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF
