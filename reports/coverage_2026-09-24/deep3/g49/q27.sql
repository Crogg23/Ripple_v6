-- JOIN, cleaner rate: detainee wins (JUDGMENT 1) closed Oct-Dec 2025 -- 90+ days before the data ends -- and how many drew a government appeal, by district
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               try_to_date(TERM_DATE::string) td, JUDGMENT::string j, upper(trim(PLAINTIFF)) p, upper(trim(DEFENDANT)) df
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by td desc nulls last, TAPE_YEAR desc) = 1),
wins as (select * from civ where j='1' and td between '2025-10-01' and '2025-12-31'),
ap as (select distinct CIRCUIT, DOCKET, REOPEN, upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, upper(trim(APPELLANT)) a, upper(trim(APPELLEE)) e
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01'),
w as (select wins.d, wins.k, wins.o,
        max(iff(ap.k is not null and (left(ap.a,5) = left(wins.df,5) or left(ap.e,5) = left(wins.p,5)),1,0)) gov_appealed,
        max(iff(ap.k is not null,1,0)) any_appeal
      from wins left join ap on ap.d = wins.d and ap.o = wins.o and ap.k = wins.k group by 1,2,3)
select coalesce(d,'ALL') district, count(*) wins_oct_dec, sum(gov_appealed) gov_appealed, sum(any_appeal) any_appeal,
  round(sum(gov_appealed)/count(*),3) gov_rate
from w group by rollup(d) having count(*) >= 40 order by wins_oct_dec desc
