---
title: Federal Prison Stats
---

```sql rows
select * from library.federal_prison_stats
```

```sql n
select count(*) as row_count from library.federal_prison_stats
```

Bureau of Prisons aggregate statistics -- inmate population, staffing, and facilities (50 metric rows).

Source: `THE_LIBRARY.JUSTICE.FEDERAL_PRISON_STATS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
