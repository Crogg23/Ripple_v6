---
title: House Election Results
---

```sql rows
select * from library.house_election_results
```

```sql n
select count(*) as row_count from library.house_election_results
```

Who won every US House race by district -- votes per candidate per district per year.

Source: `THE_LIBRARY.ELECTIONS.HOUSE_ELECTION_RESULTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
