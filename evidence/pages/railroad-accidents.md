---
title: Railroad Accidents
---

```sql rows
select * from library.railroad_accidents
```

```sql n
select count(*) as row_count from library.railroad_accidents
```

FRA railroad accident and incident records (1-row stub -- needs a real pour).

Source: `THE_LIBRARY.TRANSPORT.RAILROAD_ACCIDENTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
