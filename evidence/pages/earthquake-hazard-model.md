---
title: Earthquake Hazard Model
---

```sql rows
select * from library.earthquake_hazard_model
```

```sql n
select count(*) as row_count from library.earthquake_hazard_model
```

Global seismic hazard scores (PGA) by location from the GEM OpenQuake mosaic (12-row probe).

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.EARTHQUAKE_HAZARD_MODEL` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
