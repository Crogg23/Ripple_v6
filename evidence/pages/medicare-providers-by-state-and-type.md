---
title: Medicare Providers By State And Type
---

```sql rows
select * from library.medicare_providers_by_state_and_type
```

```sql n
select count(*) as row_count from library.medicare_providers_by_state_and_type
```

CMS Medicare provider utilization rolled to rendering-provider STATE x provider TYPE.

Source: `THE_LIBRARY.HEALTH.MEDICARE_PROVIDERS_BY_STATE_AND_TYPE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
