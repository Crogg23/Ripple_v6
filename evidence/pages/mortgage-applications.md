---
title: Mortgage Applications
---

```sql rows
select * from library.mortgage_applications
```

```sql n
select count(*) as row_count from library.mortgage_applications
```

Loan-level HMDA mortgage records -- who applied, race/ethnicity/sex, census tract, and what happened (28K-row sample).

Source: `THE_LIBRARY.HOUSING.MORTGAGE_APPLICATIONS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
