-- Delivery companies x 2024 reliability (same utility number, TX): what each wires company charges per customer vs outage minutes per customer,
-- with and without major events (Hurricane Beryl hit Houston July 2024 - outside knowledge). Plus the Texas median of every other reliability reporter.
with d as (select UTILITY_NUMBER, UTILITY_NAME, RESIDENTIAL_CUSTOMERS rc, TOTAL_CUSTOMERS tc, RESIDENTIAL_REVENUES_THOUSAND_DOLLARS rrev_k, TOTAL_REVENUES_THOUSAND_DOLLARS trev_k
           from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DELIVERY_COMPANIES),
r as (select UTILITY_NUMBER, STATE, coalesce(IEEE_SAIDI_WITH_MED_MINUTES, OTHER_SAIDI_WITH_MED_MINUTES) saidi_med, coalesce(IEEE_SAIDI_WITHOUT_MED_MINUTES, OTHER_SAIDI_WITHOUT_MED_MINUTES) saidi_nomed,
        coalesce(IEEE_SAIFI_WITH_MED, OTHER_SAIFI_WITH_MED) saifi_med, coalesce(IEEE_NUMBER_OF_CUSTOMERS, OTHER_NUMBER_OF_CUSTOMERS) rel_cust,
        iff(IEEE_SAIDI_WITH_MED_MINUTES is not null,'IEEE','other') std
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_RELIABILITY where STATE='TX')
select 'tdsp' k, d.UTILITY_NAME, d.tc::text tc, round(d.rrev_k*1000/nullif(d.rc,0))::text res_usd_cust, round(d.trev_k*1000/nullif(d.tc,0))::text all_usd_cust,
  round(r.saidi_med)::text saidi_with_major, round(r.saidi_nomed)::text saidi_without_major, round(r.saifi_med,2)::text saifi, round(r.rel_cust)::text rel_cust, r.std
from d left join r on r.UTILITY_NUMBER=d.UTILITY_NUMBER
union all
select 'tx_others', 'median of TX reporters not in the delivery table', count(*)::text, null, null, round(median(saidi_med))::text, round(median(saidi_nomed))::text, round(median(saifi_med),2)::text, round(sum(rel_cust))::text, null
from r where UTILITY_NUMBER not in (select UTILITY_NUMBER from d)
