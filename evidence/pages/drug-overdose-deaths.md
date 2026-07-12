---
title: Drug Overdose Deaths
---

```sql rows
select * from library.drug_overdose_deaths
```

```sql n
select count(*) as row_count from library.drug_overdose_deaths
```

CDC provisional drug-overdose death counts by state, month, and drug type -- the epidemic in numbers.

Source: `THE_LIBRARY.HEALTH.DRUG_OVERDOSE_DEATHS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
