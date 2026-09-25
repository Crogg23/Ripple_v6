select 'prof' k, max(FILE_DATE)::varchar a, count_if(FILE_DATE>='2025-01-01')::varchar b, count_if(nullif(trim(DEFENDANT_NAME),'') is not null)::varchar c, count(*)::varchar d, null e, null f
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL
union all
select * from (select 'sample', DISTRICT, OFFICE, DOCKET, DEFENDANT_NAME, FILE_DATE::varchar, FILING_TITLE_1 from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL where FILE_DATE >= '2025-06-20' and FILING_TITLE_1 ilike '%1347%' limit 8)
