---
title: Appeals Judge Ideology
---

```sql rows
select * from library.appeals_judge_ideology
```

```sql n
select count(*) as row_count from library.appeals_judge_ideology
```

Ideology score for every US Court of Appeals judge, by circuit -- how left/right they lean.

Source: `THE_LIBRARY.GOVERNMENT.APPEALS_JUDGE_IDEOLOGY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
