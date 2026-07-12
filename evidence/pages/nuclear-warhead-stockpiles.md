---
title: Nuclear Warhead Stockpiles
---

```sql rows
select * from library.nuclear_warhead_stockpiles
```

```sql n
select count(*) as row_count from library.nuclear_warhead_stockpiles
```

How many nuclear warheads each nuclear-armed country holds, year by year.

Source: `THE_LIBRARY.CRIME_SECURITY.NUCLEAR_WARHEAD_STOCKPILES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
