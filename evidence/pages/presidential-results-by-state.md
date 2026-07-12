---
title: Presidential Results By State
---

```sql rows
select * from library.presidential_results_by_state
```

```sql n
select count(*) as row_count from library.presidential_results_by_state
```

Who got how many votes for president in each state, each election year.

Source: `THE_LIBRARY.ELECTIONS.PRESIDENTIAL_RESULTS_BY_STATE` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
