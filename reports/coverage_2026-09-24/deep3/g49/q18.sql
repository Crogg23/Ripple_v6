-- JOIN, peer view by trial court: detention-habeas (463) filings and who won (Oct 2025 - Mar 2026), vs appeals docketed and which side appealed.
-- Side = appellant name matched to the trial case's DEFENDANT (government) or PLAINTIFF (detainee), first 5 letters; appellee checked the other way.
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k, CIRCUIT::string cir,
               try_to_date(FILE_DATE::string) fd, try_to_date(TERM_DATE::string) td, JUDGMENT::string j,
               upper(trim(PLAINTIFF)) p, upper(trim(DEFENDANT)) df
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by td desc nulls last, TAPE_YEAR desc) = 1),
ap as (select distinct CIRCUIT, DOCKET, REOPEN, upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, upper(trim(APPELLANT)) a, upper(trim(APPELLEE)) e
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01'),
js as (select ap.d, civ.j,
         case when civ.k is null then 'nomatch'
              when left(ap.a,5) = left(civ.df,5) or left(ap.e,5) = left(civ.p,5) then 'gov'
              when left(ap.a,5) = left(civ.p,5) or left(ap.e,5) = left(civ.df,5) then 'detainee' else 'unclear' end side
       from ap left join civ on civ.d = ap.d and civ.o = ap.o and civ.k = ap.k),
dist as (select d, max(cir) cir, sum(iff(fd >= '2025-10-01',1,0)) filed,
           sum(iff(td >= '2025-10-01' and j='1',1,0)) pet_won, sum(iff(td >= '2025-10-01' and j='2',1,0)) gov_won
         from civ group by 1),
apps as (select d, count(*) appeals, sum(iff(side='gov',1,0)) gov_app, sum(iff(side='detainee',1,0)) det_app,
           sum(iff(side='unclear',1,0)) unclear, sum(iff(side='nomatch',1,0)) nomatch,
           sum(iff(side='gov' and j='1',1,0)) gov_app_after_pet_won, sum(iff(side='detainee' and j='2',1,0)) det_app_after_gov_won
         from js group by 1)
select coalesce(dist.d, apps.d) district, dist.cir, dist.filed, dist.pet_won, dist.gov_won, coalesce(apps.appeals,0) appeals,
  apps.gov_app, apps.det_app, apps.unclear, apps.nomatch, apps.gov_app_after_pet_won, apps.det_app_after_gov_won
from dist full outer join apps on apps.d = dist.d
order by appeals desc, filed desc limit 40
