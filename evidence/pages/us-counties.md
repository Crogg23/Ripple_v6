---
title: Us Counties
---

```sql rows
select * from library.us_counties
```

```sql n
select count(*) as row_count from library.us_counties
```

Every US county (3,222) with FIPS code, name, 2020 population, and center point.

Source: `THE_LIBRARY.GEOGRAPHY.US_COUNTIES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
