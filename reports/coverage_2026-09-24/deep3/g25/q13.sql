-- FHLB: peer test. FDIC-supervised active banks (BKCLASS NM), FHLB member or not, by asset band: share with any FDIC order dated 2020 on
with b as (select try_to_number(CERT) c, max(ASSET) asset, max(BKCLASS) cls from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA where ACTIVE = '1' group by 1),
m as (select distinct try_to_number(CERT) c from LIBRARY_MARTS.FINANCE.FINANCE__FED_FHFA_FHLB_MEMBERSHIP where nullif(trim(CERT),'') is not null),
o as (select CERT_NUMBER c, count(*) n_orders, count_if(ORDER_TYPE ilike '%consent%' or ORDER_TYPE ilike '%cease%') n_cd, max(ORDER_DATE) last_order
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS where ORDER_DATE >= '2020-01-01' group by 1),
j as (select b.*, (m.c is not null) member, o.n_orders, o.n_cd,
  case when b.asset < 100000 then 'a <100M' when b.asset < 500000 then 'b 100-500M' when b.asset < 2000000 then 'c 500M-2B' else 'd 2B+' end band
  from b left join m on m.c = b.c left join o on o.c = b.c)
select 'rate' k, band, member::text mem, count(*) banks, count_if(n_orders > 0) any_order, count_if(n_cd > 0) cd_order,
  round(100 * count_if(n_orders > 0) / count(*), 1) pct_any, round(100 * count_if(n_cd > 0) / count(*), 1) pct_cd
from j where cls = 'NM' group by 2, 3
union all
select 'otype', ORDER_TYPE, ORDER_CATEGORY, count(*), count(distinct CERT_NUMBER), null, null, null
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS where ORDER_DATE >= '2020-01-01' group by 2, 3
order by 1, 2, 3
