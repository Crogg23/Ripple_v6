-- EPA informal: where the Region 6 SDWA/ICIS well set sits (FRS program links: state + county), and what its case numbers look like
with w as (select distinct REGISTRY_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
           where left(ENF_IDENTIFIER,2) = '06' and STATUTE = 'SDWA' and PGM_SYS_ACRNM = 'ICIS'),
g as (select REGISTRY_ID, max(STATE_CODE) st, max(upper(COUNTY_NAME)) cty from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS
      where REGISTRY_ID in (select REGISTRY_ID from w) group by 1)
select 'county' k, coalesce(g.st, '(no FRS row)') a, g.cty b, count(*) n, null c
from w left join g on g.REGISTRY_ID = w.REGISTRY_ID group by 2, 3 qualify row_number() over (order by count(*) desc) <= 10
union all
select 'idfmt', regexp_replace(ENF_IDENTIFIER, '[0-9]', '9'), max(ENF_IDENTIFIER), count(*), max(PGM_SYS_ID)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS where REGISTRY_ID in (select REGISTRY_ID from w) group by 2
qualify row_number() over (order by count(*) desc) <= 6
order by 1, 4 desc
