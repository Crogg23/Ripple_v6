---
title: Contracts By Agency And Naics
---

```sql rows
select * from library.contracts_by_agency_and_naics
```

```sql n
select count(*) as row_count from library.contracts_by_agency_and_naics
```

USASpending federal contract transactions rolled to AWARDING_AGENCY x NAICS_CODE (industry) x ACTION_YEAR.

Source: `THE_LIBRARY.GOVERNMENT_SPENDING.CONTRACTS_BY_AGENCY_AND_NAICS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
