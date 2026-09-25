-- FEMA gap verification: join FEMA disaster numbers (IA registrations table) to Federal Register notices by the FEMA-####-DR docket tag; land rate and publication lag by half-year; plus title search across all agencies
with ia as (select regexp_substr(DISASTER_NUMBER::text, '[0-9]+') dn, min(DECLARATION_DATE) dd, max(DAMAGED_STATE_ABBREVIATION) st, max(INCIDENT_TYPE_CODE) typ
            from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS where DECLARATION_DATE >= '2023-01-01' group by 1),
fr as (select d.PUBLICATION_DATE pd, d.TITLE, f.value::string tag
       from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS d,
            lateral flatten(input => regexp_substr_all(d.DOCKET_IDS, 'FEMA-[0-9]{4}-(DR|EM)')) f
       where d.DOCKET_IDS ilike '%FEMA-%' and d.PUBLICATION_DATE >= '2023-01-01'),
frd as (select regexp_substr(tag, '[0-9]{4}') dn, min(pd) first_pub, count(*) notices from fr where tag like '%-DR' group by 1),
j as (select ia.*, frd.first_pub, frd.notices, datediff(day, ia.dd, frd.first_pub) lag from ia left join frd using (dn))
select 'byhalf' k, year(dd) || '-H' || iff(month(dd) <= 6, 1, 2) a, count(*)::text b, count(first_pub)::text c, median(lag)::text d, max(lag)::text e, sum(notices)::text f, null g
from j group by 2
union all
select 'frmonth', to_char(date_trunc(month, pd), 'YYYY-MM'), count(distinct tag)::text, count(*)::text, count_if(TITLE ilike '%Major Disaster%')::text, null, null, null
from fr group by 2
union all
select 'title', year(PUBLICATION_DATE)::text, count(*)::text, count_if(DOCKET_IDS ilike '%FEMA-%')::text, count_if(month(PUBLICATION_DATE) between 2 and 8)::text,
  max(PUBLICATION_DATE)::text, count(distinct AGENCY_NAMES)::text, null
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where (TITLE ilike '%major disaster%' or TITLE ilike '%Emergency and Related Determinations%') and PUBLICATION_DATE >= '2021-01-01'
group by 2
union all
(select 'decl2025', dn, dd::text, st, typ, first_pub::text, lag::text, notices::text from j where dd >= '2025-01-01' order by dd)
