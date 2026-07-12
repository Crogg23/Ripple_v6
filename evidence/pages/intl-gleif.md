---
title: Intl Gleif
---

```sql rows
select * from library.intl_gleif
```

```sql n
select count(*) as row_count from library.intl_gleif
```

Global registry of Legal Entity Identifiers (LEI) mapping companies and legal entities worldwide to standardized 20-character codes with legal name, address, jurisdiction, and registration status.

Source: `THE_LIBRARY.COMPANIES.INTL_GLEIF` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
