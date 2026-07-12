---
title: Australasian Case Law
---

```sql rows
select * from library.australasian_case_law
```

```sql n
select count(*) as row_count from library.australasian_case_law
```

AustLII/WorldLII legal database records (1-row stub -- schema probe only).

Source: `THE_LIBRARY.JUSTICE.AUSTRALASIAN_CASE_LAW` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
