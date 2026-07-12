---
title: Fertility Rate By Country
---

```sql rows
select * from library.fertility_rate_by_country
```

```sql n
select count(*) as row_count from library.fertility_rate_by_country
```

Children born per woman, per country per year -- the birth-rate trend behind aging populations.

Source: `THE_LIBRARY.GEOGRAPHY.FERTILITY_RATE_BY_COUNTRY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
