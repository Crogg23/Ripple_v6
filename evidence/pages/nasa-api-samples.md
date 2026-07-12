---
title: Nasa Api Samples
---

```sql rows
select * from library.nasa_api_samples
```

```sql n
select count(*) as row_count from library.nasa_api_samples
```

Sample responses from NASA's open APIs -- imagery, asteroids, space weather (54 rows).

Source: `THE_LIBRARY.SCIENCE.NASA_API_SAMPLES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
