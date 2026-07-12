---
title: Hospices
---

```sql rows
select * from library.hospices
```

```sql n
select count(*) as row_count from library.hospices
```

```sql trend
select date_trunc('month', "CERTIFICATION_DATE") as period, count(*) as records
from library.hospices
where "CERTIFICATION_DATE" is not null
group by 1
order by 1
```

Every Medicare-certified hospice in America -- name, address, owner type.

Source: `THE_LIBRARY.HEALTH.HOSPICES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Hospices over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
