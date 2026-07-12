---
title: Federal Register Documents
---

```sql rows
select * from library.federal_register_documents
```

```sql n
select count(*) as row_count from library.federal_register_documents
```

US Federal Register documents -- rules, notices, proclamations, executive orders with agencies, citations, dates, URLs.

Source: `THE_LIBRARY.GOVERNMENT.FEDERAL_REGISTER_DOCUMENTS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
