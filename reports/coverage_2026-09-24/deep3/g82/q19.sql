-- Federal Register mechanism check: for the offices that went quiet, what kind of notice disappeared. Feb-Aug, 2021-2026, by title pattern
with d as (select PUBLICATION_YEAR y, TITLE,
             coalesce(try_parse_json(AGENCY_NAMES)[array_size(try_parse_json(AGENCY_NAMES))-1]::string, AGENCY) ag
           from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
           where PUBLICATION_MONTH between 2 and 8 and PUBLICATION_YEAR >= 2021)
select ag,
  case when ag = 'Federal Emergency Management Agency' and TITLE ilike '%Amendment No%' then 'fema amendment'
       when ag = 'Federal Emergency Management Agency' and TITLE ilike '%Major Disaster and Related Determinations%' then 'fema NEW major disaster'
       when ag = 'Federal Emergency Management Agency' and TITLE ilike '%Emergency and Related Determinations%' then 'fema NEW emergency'
       when ag = 'Federal Emergency Management Agency' and TITLE ilike '%flood%' then 'fema flood map'
       when TITLE ilike '%meeting%' then 'meeting'
       when TITLE ilike '%information collection%' or TITLE ilike '%data collection%' or TITLE ilike '%paperwork%' or TITLE ilike '%submission for OMB%' then 'info collection'
       else 'other' end cat,
  count_if(y=2021) y21, count_if(y=2022) y22, count_if(y=2023) y23, count_if(y=2024) y24, count_if(y=2025) y25, count_if(y=2026) y26
from d
where ag in ('Federal Emergency Management Agency','National Institutes of Health','Centers for Disease Control and Prevention','Environmental Protection Agency',
             'Education Department','Fish and Wildlife Service','Veterans Affairs Department','National Science Foundation')
group by 1, 2 order by 1, 2
