---
title: Eu Legal Acts
---

```sql rows
select * from library.eu_legal_acts
```

```sql n
select count(*) as row_count from library.eu_legal_acts
```

EU legal acts and case-law records from EUR-Lex -- CELEX ID, type, dates, and in-force status (53-row probe).

Source: `THE_LIBRARY.JUSTICE.EU_LEGAL_ACTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
