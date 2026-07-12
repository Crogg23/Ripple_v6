---
title: Refugees By Origin Country
---

```sql rows
select * from library.refugees_by_origin_country
```

```sql n
select count(*) as row_count from library.refugees_by_origin_country
```

How many refugees fled each country each year -- the size of every displacement crisis over time.

Source: `THE_LIBRARY.IMMIGRATION.REFUGEES_BY_ORIGIN_COUNTRY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
