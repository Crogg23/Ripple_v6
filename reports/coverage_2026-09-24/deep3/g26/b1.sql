-- @ncua_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_CHARTER_MERGER_EVENTS;

-- @fec_cmte_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES;

-- @fatca_all
select giin, institution_name, country_name from LIBRARY_MARTS.FINANCE.FINANCE__FED_FATCA_FFI;

-- @fatca_copy_check
select 'FINANCE' src, count(*) n, count(distinct giin) giins, hash_agg(giin, institution_name, country_name) h,
       min(_ingested_at)::string min_ing, max(_ingested_at)::string max_ing, count(distinct _source_run_id) runs
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FATCA_FFI
union all
select 'ECONOMICS', count(*), count(distinct giin), hash_agg(giin, finm, countrynm), null, null, null
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_FATCA_FFI_LIST;

-- @f13_quarters
select try_to_date(reportcalendarorquarter, 'DD-MON-YYYY') q, count(*) n, count(distinct accession_number) acc,
       count_if(isamendment = 'Y') amend, count_if(isamendment is null or isamendment = '') amend_blank,
       count_if(reporttype ilike '%NOTICE%') notices, count_if(confdeniedexpired = 'Y') conf,
       count(distinct src_file) files, count(distinct form13_ffilenumber) mgrs
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS
group by 1 order by 1;

-- @f13_profile
select reporttype, isamendment, amendmenttype, confdeniedexpired, reasonfornonconfidentiality, count(*) n
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS
group by all order by n desc;

-- @f13_dupes
with a as (
  select accession_number, count(*) c, count(distinct src_file) f
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS group by 1)
select count(*) accs, count_if(c > 1) dup_accs, sum(c) - count(*) extra_rows, max(c) max_c, count_if(f > 1) multi_file
from a;

-- @icis_top_registry
select registry_id, any_value(facility_name) nm, any_value(city) city, any_value(state_code) st,
       any_value(primary_sic_code) sic, any_value(primary_naics_code) naics,
       count(*) n, count(distinct case_number) cases, count(distinct activity_id) acts
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
group by 1 order by n desc limit 25;

-- @icis_shape
select regexp_replace(case_number, '[0-9]', '9') pat, count(*) n, count(distinct case_number) cases,
       min(case_number) ex_min, max(case_number) ex_max,
       count(distinct registry_id) regs, count(distinct activity_id) acts
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
group by 1 order by n desc limit 25;
