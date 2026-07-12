---
title: Sanctions Targets
---

```sql rows
select * from library.sanctions_targets
```

```sql n
select count(*) as row_count from library.sanctions_targets
```

Everyone and everything under sanctions worldwide -- 71K people, companies, and vessels, consolidated.

Source: `THE_LIBRARY.SANCTIONS.SANCTIONS_TARGETS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
