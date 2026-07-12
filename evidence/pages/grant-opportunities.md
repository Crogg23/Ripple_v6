---
title: Grant Opportunities
---

```sql rows
select * from library.grant_opportunities
```

```sql n
select count(*) as row_count from library.grant_opportunities
```

Federal grant opportunities listed on Grants.gov -- agency, category, eligibility, and status (100-row probe so far).

Source: `THE_LIBRARY.GOVERNMENT_SPENDING.GRANT_OPPORTUNITIES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
