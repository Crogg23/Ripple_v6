---
title: North Korea Missile Tests
---

```sql rows
select * from library.north_korea_missile_tests
```

```sql n
select count(*) as row_count from library.north_korea_missile_tests
```

```sql trend
select date_trunc('month', "DATE") as period, count(*) as records
from library.north_korea_missile_tests
where "DATE" is not null
group by 1
order by 1
```

Every North Korean missile test since 1984 -- date, missile, range, launch site, outcome.

Source: `THE_LIBRARY.CRIME_SECURITY.NORTH_KOREA_MISSILE_TESTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="North Korea Missile Tests over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
