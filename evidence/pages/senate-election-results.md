---
title: Senate Election Results
---

```sql rows
select * from library.senate_election_results
```

```sql n
select count(*) as row_count from library.senate_election_results
```

Who won every US Senate race, 1976-2024 -- votes per candidate per state per year.

Source: `THE_LIBRARY.ELECTIONS.SENATE_ELECTION_RESULTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
