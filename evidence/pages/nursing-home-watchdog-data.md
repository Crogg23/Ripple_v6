---
title: Nursing Home Watchdog Data
---

```sql rows
select * from library.nursing_home_watchdog_data
```

```sql n
select count(*) as row_count from library.nursing_home_watchdog_data
```

```sql trend
select date_trunc('month', "DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES") as period, count(*) as records
from library.nursing_home_watchdog_data
where "DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES" is not null
group by 1
order by 1
```

LTCCC's compiled nursing-home data -- staffing, inspections, penalties, and ownership for 14.7K facilities.

Source: `THE_LIBRARY.HEALTH.NURSING_HOME_WATCHDOG_DATA` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Nursing Home Watchdog Data over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
