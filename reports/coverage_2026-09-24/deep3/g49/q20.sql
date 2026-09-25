-- Dull-explanation test: new federal civil cases per month, detention habeas (463) vs general habeas (530) vs everything. Reclassification, or new volume?
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               try_to_date(FILE_DATE::string) fd, NATURE_OF_SUIT::string nos
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by TAPE_YEAR desc) = 1)
select to_char(date_trunc('month', fd),'YYYY-MM') m, count(*) all_civil, sum(iff(nos='463',1,0)) n463, sum(iff(nos='530',1,0)) n530,
  sum(iff(nos in ('510','520','540','550','555','560'),1,0)) other_prisoner, count(distinct iff(nos='463', d, null)) districts_with_463
from civ group by 1 order by 1
