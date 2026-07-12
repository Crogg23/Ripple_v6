---
title: Treasury Interest Rates
---

```sql rows
select * from library.treasury_interest_rates
```

```sql n
select count(*) as row_count from library.treasury_interest_rates
```

```sql trend
select date_trunc('month', "RECORD_DATE") as period, count(*) as records
from library.treasury_interest_rates
where "RECORD_DATE" is not null
group by 1
order by 1
```

Monthly average interest rate the US government pays on its debt, by security type.

Source: `THE_LIBRARY.ECONOMY.TREASURY_INTEREST_RATES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Treasury Interest Rates over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
