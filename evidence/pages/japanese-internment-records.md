---
title: Japanese Internment Records
---

```sql rows
select * from library.japanese_internment_records
```

```sql n
select count(*) as row_count from library.japanese_internment_records
```

Records of Japanese Americans interned in WWII camps -- person, age, camp, county.

Source: `THE_LIBRARY.HISTORY.JAPANESE_INTERNMENT_RECORDS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
