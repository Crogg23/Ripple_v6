with s as (
  select DETENTION_FACILITY_CODE code, count(*) stints, count(distinct PERSON_HASH) people, sum(iff(DETENTION_RELEASE_REASON = 'Died',1,0)) deaths,
    round(avg(datediff(day, BOOK_IN_AT, coalesce(BOOK_OUT_AT, current_timestamp()))),1) avg_days
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS where BOOK_IN_AT >= '2022-01-01' group by 1)
select f.TYPE_GROUPED, count(*) facilities, sum(s.stints) stints, sum(s.deaths) deaths, round(1e5*sum(s.deaths)/nullif(sum(s.stints),0),2) deaths_per_100k_stints, round(avg(s.avg_days),1) avg_days
from s left join LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES f on f.DETENTION_FACILITY_CODE = s.code group by 1 order by stints desc;
with s as (
  select DETENTION_FACILITY_CODE code, max(DETENTION_FACILITY) fac, max(STATE) st, count(*) stints, sum(iff(DETENTION_RELEASE_REASON = 'Died',1,0)) deaths,
    round(avg(datediff(day, BOOK_IN_AT, coalesce(BOOK_OUT_AT, current_timestamp()))),1) avg_days
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS where BOOK_IN_AT >= '2022-01-01' group by 1)
select s.*, f.TYPE_GROUPED, f.TYPE_DETAILED, round(1e5*deaths/nullif(stints,0),1) deaths_per_100k from s left join LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES f on f.DETENTION_FACILITY_CODE = s.code where deaths > 0 order by deaths desc, stints;
with cm as (
  select distinct BIOGUIDE, CONGRESS, case COMMITTEE_CODE when 'SSAS' then 'defense' when 'SSBK' then 'banking' when 'SSEG' then 'energy' when 'SSHR' then 'health' when 'SSFI' then 'health' when 'SSEV' then 'energy' end cm_sector
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP where IS_SUBCOMMITTEE in ('False','false','0') and COMMITTEE_CODE in ('SSAS','SSBK','SSEG','SSHR','SSFI','SSEV')),
traders as (select distinct BIOGUIDE, case when TRANSACTION_DATE < '2015-01-03' then '113' when TRANSACTION_DATE < '2017-01-03' then '114' when TRANSACTION_DATE < '2019-01-03' then '115' else '116' end congress from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES)
select sec.sec_sector, count(distinct t.BIOGUIDE||t.congress) trader_congress_pairs, count(distinct iff(cm.BIOGUIDE is not null, t.BIOGUIDE||t.congress, null)) on_cmte, round(100*count(distinct iff(cm.BIOGUIDE is not null, t.BIOGUIDE||t.congress, null))/count(distinct t.BIOGUIDE||t.congress),1) pct_traders_on_cmte
from traders t cross join (select distinct cm_sector sec_sector from cm) sec left join cm on cm.BIOGUIDE = t.BIOGUIDE and cm.CONGRESS = t.congress and cm.cm_sector = sec.sec_sector group by 1 order by 1;
with ex as (
  select upper(regexp_replace(ENTITY_NAME,'[^A-Z0-9 ]','')) k, max(ENTITY_NAME) ename, max(STATE) st, min(ACTIVATION_DATE) first_excl, max(coalesce(TERMINATION_DATE,'2099-12-31')) last_term, max(EXCLUDING_AGENCY) agency, max(EXCLUSION_TYPE) etype
  from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS where IS_ENTITY_NOT_INDIVIDUAL and ENTITY_NAME is not null group by 1),
ppp as (select upper(regexp_replace(BORROWERNAME,'[^A-Z0-9 ]','')) k, BORROWERNAME, BORROWERSTATE, try_to_date(DATEAPPROVED,'MM/DD/YYYY') approved, CURRENTAPPROVALAMOUNT amt, LOANSTATUS from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS)
select ex.ename, ex.st, ex.agency, ex.etype, ex.first_excl, ex.last_term, ppp.BORROWERNAME, ppp.BORROWERSTATE, ppp.approved, ppp.amt, ppp.LOANSTATUS
from ex join ppp on ppp.k = ex.k and ppp.BORROWERSTATE = ex.st
where ppp.approved between ex.first_excl and ex.last_term and length(ex.k) - length(replace(ex.k,' ','')) >= 1
order by ppp.amt desc limit 40;
select DATEAPPROVED, LOANSTATUS, count(*) from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS group by 1,2 order by 3 desc limit 5
