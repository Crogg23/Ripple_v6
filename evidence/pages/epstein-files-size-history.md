---
title: Epstein Files Size History
---

```sql rows
select * from library.epstein_files_size_history
```

```sql n
select count(*) as row_count from library.epstein_files_size_history
```

```sql trend
select date_trunc('month', "CAPTURED_AT") as period, count(*) as records
from library.epstein_files_size_history
where "CAPTURED_AT" is not null
group by 1
order by 1
```

A time-lapse of Epstein document pages: how many files each page held, snapshot by snapshot.

Source: `THE_LIBRARY.INVESTIGATIONS.EPSTEIN_FILES_SIZE_HISTORY` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Epstein Files Size History over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
