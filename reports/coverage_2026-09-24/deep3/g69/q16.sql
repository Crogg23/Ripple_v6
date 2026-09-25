-- Join: EOIR address ZIP (field 4) of Jan-May 2026 old-band detainees (custody D) -> ICE detention facility code list by 5-digit ZIP.
-- Aggregate EOIR to ZIP first. Land rate, then top 15 ZIPs with facility name(s) and type.
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, left(split_part(CASE_TYPE, '\t', 4), 5) zip, split_part(CASE_TYPE, '\t', 9) cust,
    try_to_date(left(split_part(CASE_TYPE, '\t', 11), 10), 'YYYY-MM-DD') e28d,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
z as (select zip, count(*) n, count_if(e28d < det) lawyer_before from p
      where idn >= 10441284 and idn < 13639610 and det between '2026-01-01' and '2026-05-31' and cust = 'D' group by 1),
f as (select left(trim(ZIP::string), 5) zip, count(*) nfac, listagg(distinct DETENTION_FACILITY_NAME, ' | ') names, listagg(distinct TYPE_GROUPED, '|') types
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES group by 1),
j as (select z.*, f.nfac, f.names, f.types from z left join f on f.zip = z.zip)
select 'land' k, null zip, sum(n) n, sum(iff(nfac is not null, n, 0)) landed, count(*) zips, count_if(nfac is not null) zips_landed, null names, null types, sum(lawyer_before) lawyer_before from j
union all
select * from (select 'top', zip, n, lawyer_before, null, nfac, left(names, 150), types, null from j order by n desc limit 15)
