-- EE per customer, properly: the 45 biggest utility-state rows by residential customers (all parts of the sales table), with or without an EE row.
-- Residential incentive $ per residential customer, total program $ per customer, first-year savings as % of own sales. Peer = every utility-state row with 500K+ homes (energy-only retailers, part B, left out).
with s as (select UTILITY_NUMBER, STATE, max(UTILITY_NAME) uname, listagg(distinct OWNERSHIP,'|') own, sum(RESIDENTIAL_CUSTOMERS) rc, sum(TOTAL_CUSTOMERS) tc, sum(TOTAL_SALES_MWH) tmwh
           from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST where PART<>'B' group by 1,2),
e as (select UTILITY_NUMBER, STATE, count(*) ee_rows,
        sum(coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) cost_k,
        sum(RESIDENTIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS) rinc_k, sum(TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH) sav
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY group by 1,2),
j as (select s.*, e.ee_rows, e.cost_k, e.rinc_k, e.sav, e.cost_k*1000/nullif(s.tc,0) usd_per_cust, e.rinc_k*1000/nullif(s.rc,0) rinc_per_home, 100*e.sav/nullif(s.tmwh,0) sav_pct
      from s left join e on e.UTILITY_NUMBER=s.UTILITY_NUMBER and e.STATE=s.STATE where s.rc>=500000)
select 'peer' k, null uname, null st, count(*)::text n, count(ee_rows)::text with_ee, round(median(usd_per_cust),2)::text med_usd_cust, round(median(rinc_per_home),2)::text med_rinc_home,
  round(median(sav_pct),3)::text med_sav_pct, null a, null b, null c from j
union all
select * from (select 'row', uname, STATE, round(rc)::text, own, round(cost_k)::text, round(usd_per_cust,2)::text, round(rinc_per_home,2)::text, round(sav_pct,3)::text, round(sav)::text, ee_rows::text
  from j order by usd_per_cust desc nulls last limit 60)
