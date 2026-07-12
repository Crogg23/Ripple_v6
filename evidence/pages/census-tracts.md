---
title: Census Tracts
---

```sql rows
select * from library.census_tracts
```

```sql n
select count(*) as row_count from library.census_tracts
```

All 85,391 US census tracts with 2020 population and a center point -- the geographic backbone.

Source: `THE_LIBRARY.GEOGRAPHY.CENSUS_TRACTS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
