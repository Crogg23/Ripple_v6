---
title: Homicide Rate By Country
---

```sql rows
select * from library.homicide_rate_by_country
```

```sql n
select count(*) as row_count from library.homicide_rate_by_country
```

Homicides per 100,000 people, per country per year (UN data) -- the global violence trend line.

Source: `THE_LIBRARY.CRIME_SECURITY.HOMICIDE_RATE_BY_COUNTRY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
