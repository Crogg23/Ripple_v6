---
title: Hospital Quality Ratings
---

```sql rows
select * from library.hospital_quality_ratings
```

```sql n
select count(*) as row_count from library.hospital_quality_ratings
```

CMS Hospital Compare: 5,432 hospitals with type, ownership, emergency services, and quality designations.

Source: `THE_LIBRARY.HEALTH.HOSPITAL_QUALITY_RATINGS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
