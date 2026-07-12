---
title: Ai Incidents Annual Count
---

```sql rows
select * from library.ai_incidents_annual_count
```

```sql n
select count(*) as row_count from library.ai_incidents_annual_count
```

Count of reported AI incidents and controversies per year -- one number a year, the trend line.

Source: `THE_LIBRARY.SCIENCE.AI_INCIDENTS_ANNUAL_COUNT` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
