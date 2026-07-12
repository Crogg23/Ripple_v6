---
title: Home Health Agencies
---

```sql rows
select * from library.home_health_agencies
```

```sql n
select count(*) as row_count from library.home_health_agencies
```

Every Medicare home health agency -- services, ownership, quality ratings.

Source: `THE_LIBRARY.HEALTH.HOME_HEALTH_AGENCIES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
