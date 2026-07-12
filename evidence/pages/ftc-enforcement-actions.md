---
title: Ftc Enforcement Actions
---

```sql rows
select * from library.ftc_enforcement_actions
```

```sql n
select count(*) as row_count from library.ftc_enforcement_actions
```

FTC enforcement actions and cases -- respondent, date filed, case type, and status (1,200 rows).

Source: `THE_LIBRARY.JUSTICE.FTC_ENFORCEMENT_ACTIONS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
