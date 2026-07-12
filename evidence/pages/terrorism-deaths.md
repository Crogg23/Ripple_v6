---
title: Terrorism Deaths
---

```sql rows
select * from library.terrorism_deaths
```

```sql n
select count(*) as row_count from library.terrorism_deaths
```

Annual deaths from terrorism by country, from the Global Terrorism Database.

Source: `THE_LIBRARY.CRIME_SECURITY.TERRORISM_DEATHS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
