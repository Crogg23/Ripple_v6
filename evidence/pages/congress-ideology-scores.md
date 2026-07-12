---
title: Congress Ideology Scores
---

```sql rows
select * from library.congress_ideology_scores
```

```sql n
select count(*) as row_count from library.congress_ideology_scores
```

A liberal-conservative score for every member of Congress, every Congress -- the DW-NOMINATE stat.

Source: `THE_LIBRARY.GOVERNMENT.CONGRESS_IDEOLOGY_SCORES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
