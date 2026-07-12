---
title: Suicide Death Rates
---

```sql rows
select * from library.suicide_death_rates
```

```sql n
select count(*) as row_count from library.suicide_death_rates
```

US suicide death rates by year, age, sex and race from the CDC -- the national trend line.

Source: `THE_LIBRARY.HEALTH.SUICIDE_DEATH_RATES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
