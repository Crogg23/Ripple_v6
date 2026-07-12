---
title: Egypt Statistics
---

```sql rows
select * from library.egypt_statistics
```

```sql n
select count(*) as row_count from library.egypt_statistics
```

Egyptian national statistics -- indicator, year, value (150-row probe).

Source: `THE_LIBRARY.GEOGRAPHY.EGYPT_STATISTICS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
