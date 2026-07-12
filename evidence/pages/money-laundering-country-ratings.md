---
title: Money Laundering Country Ratings
---

```sql rows
select * from library.money_laundering_country_ratings
```

```sql n
select count(*) as row_count from library.money_laundering_country_ratings
```

FATF ratings of every country's anti-money-laundering regime -- compliance and effectiveness, by recommendation.

Source: `THE_LIBRARY.SANCTIONS.MONEY_LAUNDERING_COUNTRY_RATINGS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
