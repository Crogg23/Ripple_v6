---
title: Inpatient Rehab Facilities
---

```sql rows
select * from library.inpatient_rehab_facilities
```

```sql n
select count(*) as row_count from library.inpatient_rehab_facilities
```

```sql trend
select date_trunc('month', "CERTIFICATION_DATE") as period, count(*) as records
from library.inpatient_rehab_facilities
where "CERTIFICATION_DATE" is not null
group by 1
order by 1
```

Every inpatient rehab facility in America -- name, address, owner type.

Source: `THE_LIBRARY.HEALTH.INPATIENT_REHAB_FACILITIES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Inpatient Rehab Facilities over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
