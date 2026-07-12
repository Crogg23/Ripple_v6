---
title: Drug Overdose Death Rates By County
---

```sql rows
select * from library.drug_overdose_death_rates_by_county
```

```sql n
select count(*) as row_count from library.drug_overdose_death_rates_by_county
```

Drug-poisoning (overdose) death rates for every US county, year by year, from the CDC.

Source: `THE_LIBRARY.HEALTH.DRUG_OVERDOSE_DEATH_RATES_BY_COUNTY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
