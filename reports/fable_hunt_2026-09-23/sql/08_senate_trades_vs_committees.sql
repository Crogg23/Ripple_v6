with tk as (select upper(TICKER) ticker, max(CIK) cik from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1),
sic as (select try_to_number(CIK) cik, max(SIC) sic from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_FINANCIALS group by 1),
tr as (
  select t.BIOGUIDE, t.SENATOR, t.TRANSACTION_DATE, upper(t.TICKER) ticker, t.TRANSACTION_TYPE, t.AMOUNT_BAND, sic.sic,
    case when sic.sic between '3720' and '3769' or sic.sic in ('3812','3795','3480','3483') then 'defense'
         when sic.sic between '6000' and '6199' or sic.sic in ('6211','6282','6770') then 'banking'
         when sic.sic between '1300' and '1399' or sic.sic between '2900' and '2999' or sic.sic in ('4922','4923','4924','4911','4931','4932') then 'energy'
         when sic.sic in ('2834','2835','2836','8000','8011','8050','8051','8060','8062','8071','8082','8090','8093','6324','5122','5047','3841','3842','3845','3851') then 'health'
         when sic.sic between '4800' and '4899' or sic.sic in ('7370','7371','7372','7373','7374','7379','3674','3670','3672','3576','3577','3578','3661','3663') then 'tech_telecom'
         when sic.sic between '4000' and '4599' or sic.sic in ('3711','3713','3714','3716','3721','3730','3743') then 'transport'
         when sic.sic between '0100' and '0999' or sic.sic in ('2000','2011','2013','2015','2020','2030','2033','2040','2050','2060','2070','2080','2086','2090','5140','5141','5150') then 'agriculture'
         else 'other' end sector,
    case when t.TRANSACTION_DATE < '2015-01-03' then '113' when t.TRANSACTION_DATE < '2017-01-03' then '114' when t.TRANSACTION_DATE < '2019-01-03' then '115' else '116' end congress
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES t left join tk on tk.ticker = upper(t.TICKER) left join sic on sic.cik = tk.cik
  where t.TICKER is not null and t.TICKER not in ('--','N/A','')),
cm as (
  select distinct BIOGUIDE, CONGRESS, COMMITTEE_CODE,
    case COMMITTEE_CODE when 'SSAS' then 'defense' when 'SSBK' then 'banking' when 'SSEG' then 'energy' when 'SSHR' then 'health' when 'SSCM' then 'tech_telecom' when 'SSAF' then 'agriculture' when 'SSFI' then 'health' when 'SSEV' then 'energy' end cm_sector
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP where IS_SUBCOMMITTEE in ('False','false','0') and COMMITTEE_CODE in ('SSAS','SSBK','SSEG','SSHR','SSCM','SSAF','SSFI','SSEV'))
select tr.sector, count(*) trades, sum(iff(cm.BIOGUIDE is not null,1,0)) by_member_of_overseeing_cmte, round(100*sum(iff(cm.BIOGUIDE is not null,1,0))/count(*),1) pct
from tr left join cm on cm.BIOGUIDE = tr.BIOGUIDE and cm.CONGRESS = tr.congress and cm.cm_sector = tr.sector
where tr.sic is not null group by 1 order by trades desc;
with tk as (select upper(TICKER) ticker, max(CIK) cik from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1),
sic as (select try_to_number(CIK) cik, max(SIC) sic from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_FINANCIALS group by 1)
select count(*) trades, count(tk.cik) with_cik, count(sic.sic) with_sic from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES t left join tk on tk.ticker = upper(t.TICKER) left join sic on sic.cik = tk.cik
where t.TICKER is not null and t.TICKER not in ('--','N/A','');
with tk as (select upper(TICKER) ticker, max(CIK) cik from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1),
sic as (select try_to_number(CIK) cik, max(SIC) sic from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_FINANCIALS group by 1),
tr as (
  select t.BIOGUIDE, t.SENATOR, t.TRANSACTION_DATE, upper(t.TICKER) ticker, t.TRANSACTION_TYPE, t.AMOUNT_BAND, sic.sic,
    case when sic.sic between '3720' and '3769' or sic.sic in ('3812','3795','3480','3483') then 'defense'
         when sic.sic between '6000' and '6199' or sic.sic in ('6211','6282','6770') then 'banking'
         when sic.sic between '1300' and '1399' or sic.sic between '2900' and '2999' or sic.sic in ('4922','4923','4924','4911','4931','4932') then 'energy'
         when sic.sic in ('2834','2835','2836','8000','8011','8050','8051','8060','8062','8071','8082','8090','8093','6324','5122','5047','3841','3842','3845','3851') then 'health'
         else 'other' end sector,
    case when t.TRANSACTION_DATE < '2015-01-03' then '113' when t.TRANSACTION_DATE < '2017-01-03' then '114' when t.TRANSACTION_DATE < '2019-01-03' then '115' else '116' end congress
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES t left join tk on tk.ticker = upper(t.TICKER) left join sic on sic.cik = tk.cik
  where t.TICKER is not null and t.TICKER not in ('--','N/A','')),
cm as (
  select distinct BIOGUIDE, CONGRESS, COMMITTEE_CODE, MEMBER_NAME,
    case COMMITTEE_CODE when 'SSAS' then 'defense' when 'SSBK' then 'banking' when 'SSEG' then 'energy' when 'SSHR' then 'health' when 'SSFI' then 'health' when 'SSEV' then 'energy' end cm_sector
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP where IS_SUBCOMMITTEE in ('False','false','0') and COMMITTEE_CODE in ('SSAS','SSBK','SSEG','SSHR','SSFI','SSEV'))
select tr.SENATOR, cm.COMMITTEE_CODE, tr.sector, count(*) trades, min(tr.TRANSACTION_DATE) first_t, max(tr.TRANSACTION_DATE) last_t, listagg(distinct tr.ticker, ',') tickers
from tr join cm on cm.BIOGUIDE = tr.BIOGUIDE and cm.CONGRESS = tr.congress and cm.cm_sector = tr.sector
group by 1,2,3 order by trades desc limit 30
