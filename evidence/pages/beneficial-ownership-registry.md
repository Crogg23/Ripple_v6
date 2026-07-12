---
title: Beneficial Ownership Registry
---

```sql rows
select * from library.beneficial_ownership_registry
```

```sql n
select count(*) as row_count from library.beneficial_ownership_registry
```

FinCEN beneficial ownership registry (1-row stub -- and domestic US companies were exempted in 2025).

Source: `THE_LIBRARY.COMPANIES.BENEFICIAL_OWNERSHIP_REGISTRY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
