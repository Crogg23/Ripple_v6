---
title: Military Spending By Country
---

```sql rows
select * from library.military_spending_by_country
```

```sql n
select count(*) as row_count from library.military_spending_by_country
```

Military spending per country per year in constant USD (SIPRI data) -- the arms-race trend line.

Source: `THE_LIBRARY.GOVERNMENT.MILITARY_SPENDING_BY_COUNTRY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
