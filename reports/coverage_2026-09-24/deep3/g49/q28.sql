-- Dull-explanation test for the appeal-rate gap: were the low-appeal districts' wins a different kind (consent, other)? Disposition mix of Oct-Dec 2025 detainee wins
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               try_to_date(TERM_DATE::string) td, try_to_date(FILE_DATE::string) fd, JUDGMENT::string j, DISPOSITION::string disp,
               upper(trim(PLAINTIFF)) p, upper(trim(DEFENDANT)) df
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by td desc nulls last, TAPE_YEAR desc) = 1),
wins as (select * from civ where j='1' and td between '2025-10-01' and '2025-12-31' and d in ('22','52','46','70','74','01','81','3G','12')),
ap as (select distinct upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, upper(trim(APPELLANT)) a, upper(trim(APPELLEE)) e
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01')
select wins.d, wins.disp, count(distinct wins.k||'|'||wins.o) wins, median(datediff('day', wins.fd, wins.td)) med_days_to_win,
  count(distinct iff(left(ap.a,5) = left(wins.df,5) or left(ap.e,5) = left(wins.p,5), wins.k||'|'||wins.o, null)) gov_appealed
from wins left join ap on ap.d = wins.d and ap.o = wins.o and ap.k = wins.k
group by 1,2 order by 1, 3 desc
