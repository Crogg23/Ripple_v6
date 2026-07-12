---
title: Federal Judges
---

```sql rows
select * from library.federal_judges_federal_judges
```

```sql n
select count(*) as row_count from library.federal_judges_federal_judges
```

Every federal judge in U.S. history -- name, birth/death, gender, race -- the who's-who of the bench.

Source: `THE_LIBRARY.JUSTICE.FEDERAL_JUDGES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
