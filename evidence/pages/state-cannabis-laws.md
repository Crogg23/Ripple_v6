---
title: State Cannabis Laws
---

```sql rows
select * from library.state_cannabis_laws
```

```sql n
select count(*) as row_count from library.state_cannabis_laws
```

State-by-year cannabis law details -- what each state approved and actually implemented, medical and rec.

Source: `THE_LIBRARY.GOVERNMENT.STATE_CANNABIS_LAWS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
