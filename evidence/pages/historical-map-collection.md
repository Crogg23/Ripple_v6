---
title: Historical Map Collection
---

```sql rows
select * from library.historical_map_collection
```

```sql n
select count(*) as row_count from library.historical_map_collection
```

Metadata for digitized historical maps from the David Rumsey collection -- title, date, author, and IIIF image links (10-item probe).

Source: `THE_LIBRARY.HISTORY.HISTORICAL_MAP_COLLECTION` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
