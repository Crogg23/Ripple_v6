-- @icis_placeholder
select coalesce(registry_id, '(null)') reg, facility_name, city, state_code, count(*) n,
       min(case_number) mn, max(case_number) mx
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
where registry_id = '110009327022' or registry_id is null
group by all order by n desc limit 30;

-- @icis_years
select 'case' src, left(case_number, 2) pfx, try_to_number(substr(case_number, 4, 4)) yr,
       count(distinct case_number) n, count(distinct registry_id) regs
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
group by all
union all
select 'insp', agency, year(actual_begin_date), count(distinct activity_id), count(distinct registry_id)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS
group by all
order by 1, 2, 3;

-- @icis_fac_echo
with f as (
  select registry_id, any_value(facility_name) nm, any_value(city) city, any_value(state_code) st,
         mode(primary_sic_code) sic, mode(primary_naics_code) naics,
         count(distinct case_number) cases,
         count(distinct iff(try_to_number(substr(case_number, 4, 4)) >= 2015, case_number, null)) cases15,
         min(try_to_number(substr(case_number, 4, 4))) y0, max(try_to_number(substr(case_number, 4, 4))) y1,
         count(distinct iff(left(case_number, 2) = 'HQ', case_number, null)) hq_cases
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
  where registry_id is not null
  group by 1),
e as (
  select frs_id, count(*) erows, max(quarters_with_noncompliance) qnc, max(formal_action_count) fac,
         max(total_inspection_count) insp, max(last_penalty_amt_allocated) lpa, max(date_last_penalty) dlp,
         max(compliance_status) cs, max(is_active::int) act
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO
  where frs_id in (select registry_id from f)
  group by 1)
select f.*, e.erows, e.qnc, e.fac, e.insp, e.lpa, e.dlp, e.cs, e.act
from f left join e on e.frs_id = f.registry_id;

-- @f13_files
select 'FILERS' t, src_file f, count(*) n,
       min(try_to_date(reportcalendarorquarter, 'DD-MON-YYYY')) q0, max(try_to_date(reportcalendarorquarter, 'DD-MON-YYYY')) q1
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS group by 1, 2
union all
select 'SUBS', _src_file, count(*), min(coalesce(try_to_date(periodofreport, 'DD-MON-YYYY'), try_to_date(periodofreport))),
       max(coalesce(try_to_date(periodofreport, 'DD-MON-YYYY'), try_to_date(periodofreport)))
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS group by 1, 2
order by 1, 4;

-- @f13_mgr
with s as (
  select accession_number, cik, submissiontype,
         coalesce(try_to_date(filing_date, 'DD-MON-YYYY'), try_to_date(filing_date)) fd
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS),
f as (
  select accession_number, filingmanager_name, reporttype, amendmenttype, reasonfornonconfidentiality,
         try_to_date(reportcalendarorquarter, 'DD-MON-YYYY') q
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS),
j as (
  select f.*, s.cik, s.submissiontype, s.fd, datediff(day, f.q, s.fd) dl
  from f left join s on s.accession_number = f.accession_number),
d as (
  select cik, fd, count(*) same_day from j where submissiontype = '13F-HR' group by 1, 2),
dm as (select cik, max(same_day) max_same_day from d group by 1)
select j.cik, any_value(j.filingmanager_name) nm, count(*) n, count(j.fd) landed,
       count_if(j.submissiontype = '13F-HR') orig_hr,
       count_if(j.submissiontype = '13F-HR' and j.dl > 48) late_hr,
       count_if(j.submissiontype = '13F-HR' and j.dl > 100) vlate_hr,
       max(iff(j.submissiontype = '13F-HR', j.dl, null)) max_dl,
       median(iff(j.submissiontype = '13F-HR', j.dl, null)) med_dl,
       count_if(j.amendmenttype = 'RESTATEMENT') restate, count_if(j.amendmenttype = 'NEW HOLDINGS') newh,
       count_if(j.reasonfornonconfidentiality = 'Denied') denied,
       count_if(j.reasonfornonconfidentiality ilike '%expired%') expired,
       count_if(j.reporttype ilike '%NOTICE%') notices,
       min(j.q) q0, max(j.q) q1, count(distinct j.q) nq, any_value(dm.max_same_day) max_same_day
from j left join dm on dm.cik = j.cik group by 1;

-- @f13_denied
select f.filingmanager_name, f.filingmanager_city, f.reportcalendarorquarter, f.datedeniedexpired, f.datereported,
       f.reasonfornonconfidentiality, f.reporttype, f.amendmentno, s.filing_date, s.cik, f.accession_number
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS f
left join LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS s on s.accession_number = f.accession_number
where f.reasonfornonconfidentiality = 'Denied'
order by f.datedeniedexpired;

-- @ofac_entities
select ent_num, sdn_name, sdn_type, entity_kind, program, remarks
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN
where not coalesce(is_individual, false) and not coalesce(is_vessel, false);

-- @opensanctions_orgs
select id, schema, name, aliases, countries, dataset, program_ids, first_seen, last_change
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS
where schema <> 'Person';

-- @ficu_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_FEDERALLY_INSURED_CU_LIST;

-- @pac_summary_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY;
