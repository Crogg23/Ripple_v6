-- JOIN eyeball: 12 detention-habeas appeals with the trial case they came from (names, dates, judgment code)
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               FILE_DATE, TERM_DATE, JUDGMENT::string j, DISPOSITION::string disp, PLAINTIFF, DEFENDANT, TAPE_YEAR
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2025-01-01'
             qualify row_number() over (partition by d, o, k order by try_to_date(TERM_DATE::string) desc nulls last, TAPE_YEAR desc) = 1)
select ap.CIRCUIT, ap.DOCKET, ap.DOCKET_DATE, ap.APPELLANT, ap.APPELLEE, ap.US_APPELLANT, ap.DISTRICT_COURT, ap.DISTRICT_DOCKET,
  civ.PLAINTIFF, civ.DEFENDANT, civ.FILE_DATE, civ.TERM_DATE, civ.j judgment, civ.disp disposition
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE ap
left join civ on civ.d = upper(trim(ap.DISTRICT_COURT::string)) and civ.o = try_to_number(ap.DISTRICT_OFFICE::string) and civ.k = try_to_number(ap.DISTRICT_DOCKET::string)
where ap.NATURE_OF_SUIT::string='463' and try_to_date(ap.DOCKET_DATE::string) >= '2025-10-01'
  and upper(trim(ap.DISTRICT_COURT::string)) in ('22','52','46','12','70','81')
qualify row_number() over (partition by ap.DISTRICT_COURT order by ap.DOCKET) <= 2
order by ap.DISTRICT_COURT, ap.DOCKET
