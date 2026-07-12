---
title: Fed Slavevoyages Transatlantic
---

```sql rows
select * from library.fed_slavevoyages_transatlantic
```

```sql n
select count(*) as row_count from library.fed_slavevoyages_transatlantic
```

Voyage-level dataset of transatlantic slave trading expeditions, including ships, nationalities, ports, dates, and enslaved-person counts embarked/disembarked.

Source: `THE_LIBRARY.HISTORY.FED_SLAVEVOYAGES_TRANSATLANTIC` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
