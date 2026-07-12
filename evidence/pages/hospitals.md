---
title: Hospitals
---

```sql rows
select * from library.hospitals
```

```sql n
select count(*) as row_count from library.hospitals
```

Every hospital in America -- type, ownership, ER, and overall star rating.

Source: `THE_LIBRARY.HEALTH.HOSPITALS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
