-- FEMA gap, peer check: every disaster-declaration notice by month and issuing agency list, Jul 2024 - Sep 2026. Does SBA keep publishing while FEMA stops?
select to_char(date_trunc(month, PUBLICATION_DATE), 'YYYY-MM') m, AGENCY_NAMES ag, count(*) n, count_if(DOCKET_IDS ilike '%FEMA-%') fema_docket,
  count(distinct PUBLICATION_DATE) pub_days, min(TITLE) sample_title
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where (TITLE ilike '%major disaster%' or TITLE ilike '%Emergency and Related Determinations%' or TITLE ilike '%emergency declaration%'
       or TITLE ilike '%Declaration of a Disaster%' or TITLE ilike '%Declaration of an Economic Injury Disaster%')
  and PUBLICATION_DATE >= '2024-07-01'
group by 1, 2 order by 1, 2
