select FILING_YEAR, count(*) n, count(distinct CLIENT_NAME) clients from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS group by 1 order by 1;
select year(ACTION_DATE) yr, count(*) n, round(sum(FEDERAL_ACTION_OBLIGATION)/1e9,1) bn, count(distinct RECIPIENT_PARENT_NAME) parents from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS group by 1 order by 1;
with lob as (
  select upper(regexp_replace(CLIENT_NAME,'[^A-Z0-9 ]','')) k, CLIENT_NAME, FILING_YEAR::int yr, sum(try_to_number(INCOME)) income, count(*) filings
  from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS where FILING_TYPE like 'Q%' and FILING_YEAR between '2019' and '2024' group by 1,2,3),
con as (
  select upper(regexp_replace(RECIPIENT_PARENT_NAME,'[^A-Z0-9 ]','')) k, year(ACTION_DATE) yr, sum(FEDERAL_ACTION_OBLIGATION) obligated, count(*) actions
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS where ACTION_DATE between '2019-01-01' and '2024-12-31' group by 1,2)
select count(distinct lob.k) lob_names, count(distinct con.k) con_names_hit from lob join con on con.k = lob.k and con.yr = lob.yr where length(lob.k) - length(replace(lob.k,' ','')) >= 1;
