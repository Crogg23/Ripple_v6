-- @f13_late_by_filing_q
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

-- @f13_catchup_detail
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

-- @f13_denied_holdings
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

-- @icis_case_mix_by_year
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
