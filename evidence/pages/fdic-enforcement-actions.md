---
title: Fdic Enforcement Actions
---

```sql rows
select * from library.fdic_enforcement_actions
```

```sql n
select count(*) as row_count from library.fdic_enforcement_actions
```

Heads up: a thin 14-row scrape of FDIC enforcement orders against banks -- shape only, not the full source.

Source: `THE_LIBRARY.JUSTICE.FDIC_ENFORCEMENT_ACTIONS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
