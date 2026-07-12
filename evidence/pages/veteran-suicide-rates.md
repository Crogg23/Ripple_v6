---
title: Veteran Suicide Rates
---

```sql rows
select * from library.veteran_suicide_rates
```

```sql n
select count(*) as row_count from library.veteran_suicide_rates
```

VA's official veteran suicide death counts and rates by sex, 2001-2023 -- a small summary table.

Source: `THE_LIBRARY.HEALTH.VETERAN_SUICIDE_RATES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
