---
title: County Overdose Jail Burden
---

```sql rows
select * from library.county_overdose_jail_burden
```

```sql n
select count(*) as row_count from library.county_overdose_jail_burden
```

Every US county scored on two crises at once: drug overdose deaths and jail incarceration.

Source: `THE_LIBRARY.JUSTICE.COUNTY_OVERDOSE_JAIL_BURDEN` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
