---
title: Border Enforcement Monthly
---

```sql rows
select * from library.border_enforcement_monthly
```

```sql n
select count(*) as row_count from library.border_enforcement_monthly
```

51K monthly DHS enforcement records -- CBP encounters, ICE arrests/detentions/removals, by citizenship and region.

Source: `THE_LIBRARY.IMMIGRATION.BORDER_ENFORCEMENT_MONTHLY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
