---
title: Ice Enforcement Stats
---

```sql rows
select * from library.ice_enforcement_stats
```

```sql n
select count(*) as row_count from library.ice_enforcement_stats
```

ICE arrests, detentions, removals, and monitoring stats by quarter, country, and criminal history (221 rows).

Source: `THE_LIBRARY.IMMIGRATION.ICE_ENFORCEMENT_STATS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
