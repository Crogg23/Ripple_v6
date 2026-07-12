---
title: Contracts By Agency And State
---

```sql rows
select * from library.contracts_by_agency_and_state
```

```sql n
select count(*) as row_count from library.contracts_by_agency_and_state
```

USASpending federal contracts rolled to AWARDING_AGENCY x recipient STATE x ACTION_YEAR.

Source: `THE_LIBRARY.GOVERNMENT_SPENDING.CONTRACTS_BY_AGENCY_AND_STATE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
