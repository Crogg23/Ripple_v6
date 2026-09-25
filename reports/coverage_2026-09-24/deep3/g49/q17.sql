-- JOIN: 463 appeals (Oct 2025 - Mar 2026) -> FJC civil trial-court case (district + office + docket). Land rate, and who won below, by who appealed.
-- Plus: 463 filings per month in the trial courts (the pipeline feeding the appeals). Civil cases repeat across tapes: keep one row per case.
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               try_to_date(FILE_DATE::string) fd, try_to_date(TERM_DATE::string) td, JUDGMENT::string j, DISPOSITION::string disp
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2023-10-01'
             qualify row_number() over (partition by d, o, k order by td desc nulls last, TAPE_YEAR desc) = 1),
ap as (select distinct CIRCUIT, DOCKET, REOPEN, upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, US_APPELLANT::string usa
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01')
select 'join' section, ap.usa k1, coalesce(civ.j,'(no match)') k2, coalesce(civ.disp,'') k3, count(*) n
from ap left join civ on civ.d = ap.d and civ.o = ap.o and civ.k = ap.k
group by 1,2,3,4
union all
select 'filings_by_month', to_char(date_trunc('month', fd),'YYYY-MM'), '', '', count(*) from civ group by 1,2,3,4
union all
select 'terminations_by_month_judgment', to_char(date_trunc('month', td),'YYYY-MM'), j, '', count(*) from civ where td is not null and td >= '2025-06-01' group by 1,2,3,4
order by 1,2,3,4
