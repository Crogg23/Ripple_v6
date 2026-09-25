-- g26 deep pass 3, 2026-09-24. Every statement run, in order, numbered.
-- Door: Python (connect/db.py). Read-only. Session setup on each connection (not counted):
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- [1] ncua_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_CHARTER_MERGER_EVENTS;

-- [2] fec_cmte_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES;

-- [3] fatca_all
select giin, institution_name, country_name from LIBRARY_MARTS.FINANCE.FINANCE__FED_FATCA_FFI;

-- [4] fatca_copy_check
select 'FINANCE' src, count(*) n, count(distinct giin) giins, hash_agg(giin, institution_name, country_name) h,
       min(_ingested_at)::string min_ing, max(_ingested_at)::string max_ing, count(distinct _source_run_id) runs
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FATCA_FFI
union all
select 'ECONOMICS', count(*), count(distinct giin), hash_agg(giin, finm, countrynm), null, null, null
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_FATCA_FFI_LIST;

-- [5] f13_quarters
select try_to_date(reportcalendarorquarter, 'DD-MON-YYYY') q, count(*) n, count(distinct accession_number) acc,
       count_if(isamendment = 'Y') amend, count_if(isamendment is null or isamendment = '') amend_blank,
       count_if(reporttype ilike '%NOTICE%') notices, count_if(confdeniedexpired = 'Y') conf,
       count(distinct src_file) files, count(distinct form13_ffilenumber) mgrs
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS
group by 1 order by 1;

-- [6] f13_profile
select reporttype, isamendment, amendmenttype, confdeniedexpired, reasonfornonconfidentiality, count(*) n
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS
group by all order by n desc;

-- [7] f13_dupes
with a as (
  select accession_number, count(*) c, count(distinct src_file) f
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS group by 1)
select count(*) accs, count_if(c > 1) dup_accs, sum(c) - count(*) extra_rows, max(c) max_c, count_if(f > 1) multi_file
from a;

-- [8] icis_top_registry
select registry_id, any_value(facility_name) nm, any_value(city) city, any_value(state_code) st,
       any_value(primary_sic_code) sic, any_value(primary_naics_code) naics,
       count(*) n, count(distinct case_number) cases, count(distinct activity_id) acts
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
group by 1 order by n desc limit 25;

-- [9] icis_shape
select regexp_replace(case_number, '[0-9]', '9') pat, count(*) n, count(distinct case_number) cases,
       min(case_number) ex_min, max(case_number) ex_max,
       count(distinct registry_id) regs, count(distinct activity_id) acts
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
group by 1 order by n desc limit 25;

-- [10] icis_placeholder
select coalesce(registry_id, '(null)') reg, facility_name, city, state_code, count(*) n,
       min(case_number) mn, max(case_number) mx
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
where registry_id = '110009327022' or registry_id is null
group by all order by n desc limit 30;

-- [11] icis_years
select 'case' src, left(case_number, 2) pfx, try_to_number(substr(case_number, 4, 4)) yr,
       count(distinct case_number) n, count(distinct registry_id) regs
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
group by all
union all
select 'insp', agency, year(actual_begin_date), count(distinct activity_id), count(distinct registry_id)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS
group by all
order by 1, 2, 3;

-- [12] icis_fac_echo
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

-- [13] f13_files
select 'FILERS' t, src_file f, count(*) n,
       min(try_to_date(reportcalendarorquarter, 'DD-MON-YYYY')) q0, max(try_to_date(reportcalendarorquarter, 'DD-MON-YYYY')) q1
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS group by 1, 2
union all
select 'SUBS', _src_file, count(*), min(coalesce(try_to_date(periodofreport, 'DD-MON-YYYY'), try_to_date(periodofreport))),
       max(coalesce(try_to_date(periodofreport, 'DD-MON-YYYY'), try_to_date(periodofreport)))
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS group by 1, 2
order by 1, 4;

-- [14] f13_mgr
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

-- [15] f13_denied
select f.filingmanager_name, f.filingmanager_city, f.reportcalendarorquarter, f.datedeniedexpired, f.datereported,
       f.reasonfornonconfidentiality, f.reporttype, f.amendmentno, s.filing_date, s.cik, f.accession_number
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS f
left join LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS s on s.accession_number = f.accession_number
where f.reasonfornonconfidentiality = 'Denied'
order by f.datedeniedexpired;

-- [16] ofac_entities
select ent_num, sdn_name, sdn_type, entity_kind, program, remarks
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN
where not coalesce(is_individual, false) and not coalesce(is_vessel, false);

-- [17] opensanctions_orgs
select id, schema, name, aliases, countries, dataset, program_ids, first_seen, last_change
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS
where schema <> 'Person';

-- [18] ficu_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_FEDERALLY_INSURED_CU_LIST;

-- [19] pac_summary_all
select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY;

-- [20] f13_late_by_filing_q
with s as (
  select accession_number, cik, submissiontype,
         coalesce(try_to_date(filing_date, 'DD-MON-YYYY'), try_to_date(filing_date)) fd
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS),
f as (
  select accession_number, try_to_date(reportcalendarorquarter, 'DD-MON-YYYY') q
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS)
select date_trunc('quarter', s.fd) fq, count(*) orig, count(distinct s.cik) mgrs,
       count_if(datediff(day, f.q, s.fd) > 48) late,
       count_if(datediff(day, f.q, s.fd) > 365) late_1y,
       count(distinct iff(datediff(day, f.q, s.fd) > 365, s.cik, null)) mgrs_late_1y,
       count_if(datediff(day, f.q, s.fd) > 1825) late_5y
from f join s on s.accession_number = f.accession_number
where s.submissiontype = '13F-HR'
group by 1 order by 1;

-- [21] f13_catchup_detail
with s as (
  select accession_number, cik, submissiontype,
         coalesce(try_to_date(filing_date, 'DD-MON-YYYY'), try_to_date(filing_date)) fd
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS),
f as (
  select accession_number, filingmanager_name, filingmanager_city, filingmanager_stateorcountry, reporttype,
         try_to_date(reportcalendarorquarter, 'DD-MON-YYYY') q
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS),
j as (
  select f.*, s.cik, s.submissiontype, s.fd, datediff(day, f.q, s.fd) dl
  from f join s on s.accession_number = f.accession_number),
m as (
  select cik, count_if(submissiontype = '13F-HR' and dl > 365) late1y
  from j group by 1 having late1y >= 8)
select j.cik, any_value(j.filingmanager_name) nm, any_value(j.filingmanager_city) city,
       any_value(j.filingmanager_stateorcountry) st, any_value(m.late1y) late1y,
       count_if(j.submissiontype = '13F-HR') orig,
       count_if(j.submissiontype = '13F-NT') nt_filed,
       count_if(j.reporttype ilike '%COMBINATION%') combo,
       min(iff(j.submissiontype = '13F-HR' and j.dl > 365, j.fd, null)) first_late_fd,
       max(iff(j.submissiontype = '13F-HR' and j.dl > 365, j.fd, null)) last_late_fd,
       count(distinct iff(j.submissiontype = '13F-HR' and j.dl > 365, j.fd, null)) late_days,
       min(iff(j.submissiontype = '13F-HR', j.q, null)) earliest_q,
       min(iff(j.submissiontype = '13F-HR' and j.dl <= 48, j.fd, null)) first_ontime_fd,
       max(j.dl) max_dl
from j join m on m.cik = j.cik
group by 1 order by late1y desc;

-- [22] f13_denied_holdings
with d as (
  select accession_number, filingmanager_name, reportcalendarorquarter, datedeniedexpired
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS
  where reasonfornonconfidentiality = 'Denied'),
h as (
  select h.accession_number, h.nameofissuer, h.titleofclass, h.cusip, h.value_usd, h.sshprnamt, h.putcall
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS h
  where h.accession_number in (select accession_number from d))
select d.filingmanager_name, d.reportcalendarorquarter, d.datedeniedexpired, h.nameofissuer, h.titleofclass,
       h.cusip, h.value_usd, h.sshprnamt, h.putcall,
       count(*) over (partition by d.accession_number) n_lines
from d left join h on h.accession_number = d.accession_number
qualify row_number() over (partition by d.accession_number order by h.value_usd desc nulls last) <= 4
order by d.datedeniedexpired, d.filingmanager_name, h.value_usd desc;

-- [23] icis_case_mix_by_year
select try_to_number(substr(case_number, 4, 4)) yr,
       count(distinct case_number) cases,
       count(distinct iff(state_code = 'XX' or registry_id is null, case_number, null)) foreign_or_noid,
       count(distinct iff(facility_name ilike any ('%PORT OF ENTRY%', '%CUSTOMS%', '%BORDER PROTECTION%'), case_number, null)) port,
       count(distinct iff(nullif(primary_sic_code, '') is null and nullif(primary_naics_code, '') is null, case_number, null)) no_code,
       count(distinct iff(left(primary_sic_code, 1) in ('2', '3') or left(primary_naics_code, 2) in ('31', '32', '33'), case_number, null)) mfg,
       count(distinct iff(left(primary_sic_code, 2) in ('13', '29', '49') or left(primary_naics_code, 2) in ('21', '22'), case_number, null)) energy_util,
       count(distinct iff(left(case_number, 2) = 'HQ', case_number, null)) hq
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
where try_to_number(substr(case_number, 4, 4)) between 2010 and 2026
group by 1 order by 1;

-- [24] icis_sector_by_year
with c as (
  select case_number, try_to_number(substr(case_number, 4, 4)) yr,
         case
           when left(primary_sic_code, 2) = '13' or left(primary_naics_code, 3) = '211' then 'oil_gas_extraction'
           when left(primary_sic_code, 2) = '29' or left(primary_naics_code, 3) = '324' then 'refining'
           when left(primary_sic_code, 3) = '491' or left(primary_naics_code, 4) = '2211' then 'power'
           when left(primary_sic_code, 3) in ('494', '495') or left(primary_naics_code, 4) in ('2213', '5622') then 'water_sewer_waste'
           when left(primary_sic_code, 2) = '28' or left(primary_naics_code, 3) = '325' then 'chemicals'
           when left(primary_sic_code, 1) in ('2', '3') or left(primary_naics_code, 2) in ('31', '32', '33') then 'other_mfg'
           when nullif(primary_sic_code, '') is null and nullif(primary_naics_code, '') is null then 'no_code'
           else 'other'
         end sector
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
  where try_to_number(substr(case_number, 4, 4)) between 2012 and 2026)
select yr, sector, count(distinct case_number) cases
from c group by 1, 2 order by 2, 1;

-- [25] f13_backfill_holdings_check
with s as (
  select accession_number, cik, submissiontype,
         coalesce(try_to_date(filing_date, 'DD-MON-YYYY'), try_to_date(filing_date)) fd
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS
  where cik in ('0000883597', '0001600177', '0002009396', '0001993485', '0002033536', '0002057421', '0001637689', '0002022297')),
f as (
  select accession_number, filingmanager_name, try_to_date(reportcalendarorquarter, 'DD-MON-YYYY') q
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS),
j as (
  select f.accession_number, f.filingmanager_name, f.q, s.cik, s.fd, datediff(day, f.q, s.fd) dl
  from f join s on s.accession_number = f.accession_number
  where s.submissiontype = '13F-HR'),
h as (
  select accession_number, count(*) lines, sum(value_usd) val
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS
  where accession_number in (select accession_number from j)
  group by 1)
select j.cik, any_value(j.filingmanager_name) nm,
       count(*) reports, count_if(j.dl > 365) backfilled,
       count_if(j.dl > 365 and coalesce(h.lines, 0) = 0) backfilled_no_lines,
       min(iff(j.dl > 365, j.q, null)) oldest_q_backfilled,
       max_by(h.val, j.q) latest_val, max_by(j.q, j.q) latest_q,
       min_by(h.val, j.q) oldest_val, median(iff(j.dl > 365, h.lines, null)) med_lines_backfilled
from j left join h on h.accession_number = j.accession_number
group by 1 order by backfilled desc;

-- Local work, no warehouse statements:
--   g26/fatca_sdn_match.py  FATCA name (legal-form words stripped) x OpenSanctions SDN-sourced org names/aliases, country must agree.
--   FEC committees x PAC summary, NCUA mergers x insured CU list, ICIS peer ranks: pandas-free Python over the pulled files in g26/.
-- Total: 25 statements of 35.
