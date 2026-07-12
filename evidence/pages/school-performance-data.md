---
title: School Performance Data
---

```sql rows
select * from library.school_performance_data
```

```sql n
select count(*) as row_count from library.school_performance_data
```

EDFacts K-12 school performance and enrollment data by state, district, and school (33-row probe).

Source: `THE_LIBRARY.EDUCATION.SCHOOL_PERFORMANCE_DATA` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
