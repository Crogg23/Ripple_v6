---
title: Redlining Maps
---

```sql rows
select * from library.redlining_maps
```

```sql n
select count(*) as row_count from library.redlining_maps
```

1930s federal redlining grades (A-D) for ~200 US cities, with the racist reasons written down.

Source: `THE_LIBRARY.HOUSING.REDLINING_MAPS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
