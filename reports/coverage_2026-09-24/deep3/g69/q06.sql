-- EOIR: identify the 39 tab fields on a 2% row sample (38-tab rows only). Per field: filled share, distinct, top values
with s as (select CASE_TYPE from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA sample bernoulli (2)
           where regexp_count(CASE_TYPE, '\t') = 38),
f as (select x.index + 1 fld, trim(replace(x.value::string, char(0), '')) v from s, lateral flatten(input => split(s.CASE_TYPE, '\t')) x)
select fld, count(*) n, count_if(v <> '') filled, approx_count_distinct(nullif(v,'')) nd,
  approx_top_k(nullif(v,''), 8) top, min(nullif(v,'')) mn, max(nullif(v,'')) mx
from f group by 1 order by 1
