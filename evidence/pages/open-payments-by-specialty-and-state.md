---
title: Open Payments By Specialty And State
---

```sql rows
select * from library.open_payments_by_specialty_and_state
```

```sql n
select count(*) as row_count from library.open_payments_by_specialty_and_state
```

CMS Open Payments 2022-2024 rolled to recipient SPECIALTY x PROGRAM_YEAR x recipient STATE.

Source: `THE_LIBRARY.HEALTH.OPEN_PAYMENTS_BY_SPECIALTY_AND_STATE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
