-- S14 SEC_EDGAR vs the bigger ECONOMICS__FED_US_SEC_EDGAR: do the 200 sample filings and 20 companies already sit in the 49K-row table; state of incorporation agreement
with s as (
  select replace(ACCESSIONNUMBER, '-', '') acc, try_to_number(CIK) cik, ENTITYNAME, STATEOFINCORPORATION inc, EIN
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SEC_EDGAR),
b as (
  select replace(ACCESSION_NUMBER, '-', '') acc, try_to_number(CIK) cik, max(STATE_OF_INCORPORATION) over (partition by try_to_number(CIK)) inc_b,
    max(EIN) over (partition by try_to_number(CIK)) ein_b, FILED_AT
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_US_SEC_EDGAR),
bc as (select cik, max(inc_b) inc_b, max(ein_b) ein_b, count(*) n_b, min(FILED_AT) b_min, max(FILED_AT) b_max from b group by 1)
select s.cik, max(s.ENTITYNAME) name, count(*) n_sample, sum(iff(b.acc is not null, 1, 0)) n_acc_in_big,
  max(bc.n_b) n_big_rows, max(bc.b_min) big_min, max(bc.b_max) big_max, max(s.inc) inc_sample, max(bc.inc_b) inc_big, max(s.EIN) ein_sample, max(bc.ein_b) ein_big
from s
left join (select distinct acc from b) b on b.acc = s.acc
left join bc on bc.cik = s.cik
group by 1 order by 1;

-- S15 EMBER raw rows behind the lead: US and World coal, gas, total generation and power CO2, 2023-2025, straight from the table
select COUNTRY, YEAR, CATEGORY, SUBCATEGORY, VARIABLE, UNIT, VALUE, YOY_ABSOLUTE_CHANGE, YOY_PCT_CHANGE
from LIBRARY_MARTS.ENERGY.ENERGY__INTL_EMBER_ELEC
where COUNTRY in ('United States of America', 'World') and YEAR between 2023 and 2025
  and ((CATEGORY = 'Electricity generation' and VARIABLE in ('Coal', 'Gas', 'Total Generation', 'Wind and Solar') and UNIT = 'TWh')
    or (CATEGORY = 'Power sector emissions' and VARIABLE = 'Total emissions'))
order by COUNTRY, VARIABLE, YEAR;
