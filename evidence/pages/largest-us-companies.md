---
title: Largest Us Companies
---

```sql rows
select * from library.largest_us_companies
```

```sql n
select count(*) as row_count from library.largest_us_companies
```

The 100 biggest US companies by revenue -- rank, industry, headcount, HQ.

Source: `THE_LIBRARY.COMPANIES.LARGEST_US_COMPANIES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
