-- @f13_backfill_holdings_check
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
