-- Hostile-editor test: are the government's detention-habeas appeals real fights, or notices filed and then dropped?
-- 463 appeals docketed Oct 2025 - Mar 2026: closed by 31 Mar 2026? on the merits (DISPOSITION 1/2, OUTCOME filled) or without a ruling (4/5)? By side, top-3 trial courts vs rest.
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               upper(trim(PLAINTIFF)) p, upper(trim(DEFENDANT)) df
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by try_to_date(TERM_DATE::string) desc nulls last, TAPE_YEAR desc) = 1),
ap as (select CIRCUIT, DOCKET, REOPEN, upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, upper(trim(APPELLANT)) a, upper(trim(APPELLEE)) e, TAPE_YEAR::string tape,
         DISPOSITION::string disp, OUTCOME::string outc, PROCEDURAL_TERMINATION::string pt,
         datediff('day', try_to_date(DOCKET_DATE::string), try_to_date(JUDGMENT_DATE::string)) days
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01'
       qualify row_number() over (partition by CIRCUIT, DOCKET, REOPEN order by TAPE_YEAR) = 1)
select iff(ap.d in ('22','52','46'), ap.d, 'rest') trial_court,
  case when civ.k is null then 'nomatch' when left(ap.a,5) = left(civ.df,5) or left(ap.e,5) = left(civ.p,5) then 'gov'
       when left(ap.a,5) = left(civ.p,5) or left(ap.e,5) = left(civ.df,5) then 'detainee' else 'unclear' end side,
  count(*) appeals, sum(iff(tape <> '2099',1,0)) closed, sum(iff(disp in ('1','2'),1,0)) closed_merits,
  sum(iff(disp in ('1','2') and outc='1',1,0)) merits_outcome1, sum(iff(disp in ('1','2') and outc<>'1',1,0)) merits_other,
  sum(iff(disp in ('4','5'),1,0)) closed_no_ruling, mode(iff(disp='4', pt, null)) top_proc_code, median(iff(tape <> '2099', days, null)) med_days_open
from ap left join civ on civ.d = ap.d and civ.o = ap.o and civ.k = ap.k
group by 1,2 order by 1,2
