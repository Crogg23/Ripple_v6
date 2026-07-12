---
title: North Korea Missile Tests Xc Nagix Dprk Missile Tests
---

```sql rows
select * from library.north_korea_missile_tests_xc_nagix_dprk_missile_tests
```

```sql n
select count(*) as row_count from library.north_korea_missile_tests_xc_nagix_dprk_missile_tests
```

```sql trend
select date_trunc('month', "DATE") as period, count(*) as records
from library.north_korea_missile_tests_xc_nagix_dprk_missile_tests
where "DATE" is not null
group by 1
order by 1
```

Every known North Korean missile test -- date, missile, apogee, distance, and outcome.

Source: `THE_LIBRARY.CRIME_SECURITY.NORTH_KOREA_MISSILE_TESTS_XC_NAGIX_DPRK_MISSILE_TESTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="North Korea Missile Tests Xc Nagix Dprk Missile Tests over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
