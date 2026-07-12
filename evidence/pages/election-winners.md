---
title: Election Winners
---

```sql rows
select * from library.election_winners
```

```sql n
select count(*) as row_count from library.election_winners
```

Who won every federal election -- office, year, state, vote share, and the margin over the runner-up.

Source: `THE_LIBRARY.ELECTIONS.ELECTION_WINNERS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
