---
title: Epstein Files Tracker
---

```sql rows
select * from library.epstein_files_tracker
```

```sql n
select count(*) as row_count from library.epstein_files_tracker
```

```sql trend
select date_trunc('month', "FIRST_OBSERVED_AT") as period, count(*) as records
from library.epstein_files_tracker
where "FIRST_OBSERVED_AT" is not null
group by 1
order by 1
```

A watch-list of Epstein-related document files: which ones exist, and when we first/last saw them.

Source: `THE_LIBRARY.INVESTIGATIONS.EPSTEIN_FILES_TRACKER` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Epstein Files Tracker over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
