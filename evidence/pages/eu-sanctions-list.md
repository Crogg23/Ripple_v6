---
title: Eu Sanctions List
---

```sql rows
select * from library.eu_sanctions_list
```

```sql n
select count(*) as row_count from library.eu_sanctions_list
```

```sql trend
select date_trunc('month', "DATE_FILE") as period, count(*) as records
from library.eu_sanctions_list
where "DATE_FILE" is not null
group by 1
order by 1
```

The EU's consolidated financial sanctions list -- 42K records of persons and entities under asset freezes.

Source: `THE_LIBRARY.SANCTIONS.EU_SANCTIONS_LIST` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Eu Sanctions List over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
