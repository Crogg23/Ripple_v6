---
title: Fec Committees 2026
---

```sql rows
select * from library.fec_committees_2026
```

```sql n
select count(*) as row_count from library.fec_committees_2026
```

Every FEC-registered political committee for the 2026 cycle -- name, treasurer, type, linked candidate.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FEC_COMMITTEES_2026` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
