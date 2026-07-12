---
title: Federal Agency Budgets
---

```sql rows
select * from library.federal_agency_budgets
```

```sql n
select count(*) as row_count from library.federal_agency_budgets
```

The top 111 federal agencies with their budget, obligations, and actual outlays this fiscal year.

Source: `THE_LIBRARY.GOVERNMENT_SPENDING.FEDERAL_AGENCY_BUDGETS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
