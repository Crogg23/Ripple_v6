---
title: Appeals Judge Ideology Scores
---

```sql rows
select * from library.appeals_judge_ideology_scores
```

```sql n
select count(*) as row_count from library.appeals_judge_ideology_scores
```

Ideology scores for 703 federal appeals-court judges -- how liberal or conservative each one leans.

Source: `THE_LIBRARY.JUSTICE.APPEALS_JUDGE_IDEOLOGY_SCORES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
