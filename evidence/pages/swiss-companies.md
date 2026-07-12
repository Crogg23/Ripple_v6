---
title: Swiss Companies
---

```sql rows
select * from library.swiss_companies
```

```sql n
select count(*) as row_count from library.swiss_companies
```

Heads up: thin 18-row sample of Switzerland's official company registry (Zefix) -- shape only, not the full country.

Source: `THE_LIBRARY.COMPANIES.SWISS_COMPANIES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
