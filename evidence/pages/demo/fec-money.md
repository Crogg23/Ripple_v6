---
title: "84 Million Political Donations"
---

```sql by_cycle
select
    extract(year from TRANSACTION_DATE) as year,
    count(*) as donations,
    sum(TRANSACTION_AMT) as total_usd,
    avg(TRANSACTION_AMT) as avg_donation
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
where TRANSACTION_DATE >= '2004-01-01'
  and TRANSACTION_AMT > 0
  and TRANSACTION_AMT < 100000
group by year
order by year
```

```sql by_state
select
    STATE as state,
    count(*) as donations,
    sum(TRANSACTION_AMT) as total_usd
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
where TRANSACTION_AMT > 0
  and TRANSACTION_AMT < 100000
  and STATE is not null
  and length(STATE) = 2
group by state
order by total_usd desc
limit 20
```

```sql totals
select
    count(*) as total_donations,
    sum(TRANSACTION_AMT) as total_usd
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
where TRANSACTION_AMT > 0
```

# Every itemized political donation in America

84 million individual contributions to federal committees — the raw firehose of who funds American politics.

<BigValue data={totals} value=total_donations title="Individual donations" fmt="#,##0" />
<BigValue data={totals} value=total_usd title="Total dollars" fmt="$#,##0" />

## Donations by year

<LineChart
    data={by_cycle}
    x=year
    y=total_usd
    fmt="$#,##0"
    title="Total individual contributions by year"
    yAxisTitle="Dollars"
/>

<LineChart
    data={by_cycle}
    x=year
    y=donations
    fmt="#,##0"
    title="Number of donations by year"
    yAxisTitle="Donations"
/>

## Average donation size over time

<LineChart
    data={by_cycle}
    x=year
    y=avg_donation
    fmt="$#,##0"
    title="Average donation amount"
/>

## Top 20 states by total contributions

<BarChart
    data={by_state}
    x=state
    y=total_usd
    fmt="$#,##0"
    title="Total contributions by state"
    swapXY=true
/>
