---
title: Immigration Application Stats
---

```sql rows
select * from library.immigration_application_stats
```

```sql n
select count(*) as row_count from library.immigration_application_stats
```

USCIS application volumes by form type -- receipts, approvals, denials, backlogs, and processing times (3,204 rows).

Source: `THE_LIBRARY.IMMIGRATION.IMMIGRATION_APPLICATION_STATS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
