---
title: Tribal Lands Geo
---

```sql rows
select * from library.tribal_lands_geo
```

```sql n
select count(*) as row_count from library.tribal_lands_geo
```

Bureau of Indian Affairs geospatial records of tribal lands and boundaries (100-row probe).

Source: `THE_LIBRARY.GEOGRAPHY.TRIBAL_LANDS_GEO` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
