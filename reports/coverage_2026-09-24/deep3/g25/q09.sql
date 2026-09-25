-- FHLB: future and stand-in member dates, and CERT join to FDIC bank data (active flag) and FDIC failed-bank list
with m as (select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FHFA_FHLB_MEMBERSHIP where nullif(trim(CERT),'') is not null),
b as (select try_to_number(CERT) c, max(ACTIVE) active, max(ENDEFYMD) endd, max(NAME) bname, max(ASSET) asset from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA group by 1),
f as (select try_to_number(FDIC_CERT) c, max(FAIL_DATE) fail_date, max(BANK_NAME) fname, max(TOTAL_ASSETS_THOUSANDS) fassets from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS group by 1)
select 'sum' k, count(*)::text a, count(b.c)::text b_, count_if(b.active='1')::text c_, count_if(b.active='0')::text d_,
  count(f.c)::text e_, count_if(m.MEM_DATE > current_date())::text f_, count_if(m.APPR_DATE > current_date())::text g_, null h_
from m left join b on b.c = try_to_number(m.CERT) left join f on f.c = try_to_number(m.CERT)
union all
select 'failed', m.MEMBER_NAME, m.CERT, m.DISTRICT, m.MEM_DATE::text, f.fail_date::text, f.fname, b.active, round(f.fassets/1e3)::text
from m join f on f.c = try_to_number(m.CERT)
union all
select 'future', m.MEMBER_NAME, m.CERT, m.MEM_TYPE, m.MEM_DATE::text, m.APPR_DATE::text, b.bname, b.active, b.endd::text
from m left join b on b.c = try_to_number(m.CERT) where m.MEM_DATE > current_date()
order by 1, 6
