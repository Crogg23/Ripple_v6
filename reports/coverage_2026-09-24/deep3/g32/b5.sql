-- @boca_shell_reporting_owners
select try_to_number(s.issuer_cik) issuer_cik, s.issuer_name, r.owner_name, r.relationship, r.city, r.state, count(*) filings, min(s.filing_date) first_f, max(s.filing_date) last_f
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s
join LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER r on r.accession_number = s.accession_number
where try_to_number(s.issuer_cik) in (1900520, 1918080, 1918102)
group by 1,2,3,4,5,6 order by 1, filings desc
