---
title: Fcc Licenses By State And Service
---

```sql rows
select * from library.fcc_licenses_by_state_and_service
```

```sql n
select count(*) as row_count from library.fcc_licenses_by_state_and_service
```

FCC ULS license records rolled to STATE x RADIO_SERVICE_CODE x LICENSE_STATUS x GRANT_YEAR.

Source: `THE_LIBRARY.GOVERNMENT.FCC_LICENSES_BY_STATE_AND_SERVICE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
