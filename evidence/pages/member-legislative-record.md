---
title: Member Legislative Record
---

```sql rows
select * from library.member_legislative_record
```

```sql n
select count(*) as row_count from library.member_legislative_record
```

Each member of Congress's lawmaking scorecard -- bills sponsored, passed, and how far they got.

Source: `THE_LIBRARY.GOVERNMENT.MEMBER_LEGISLATIVE_RECORD` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
