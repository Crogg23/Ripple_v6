---
title: Open Payments By Manufacturer And Nature
---

```sql rows
select * from library.open_payments_by_manufacturer_and_nature
```

```sql n
select count(*) as row_count from library.open_payments_by_manufacturer_and_nature
```

CMS Open Payments (industry payments to physicians/hospitals), 2022-2024 combined, rolled to paying MANUFACTURER/GPO x PROGRAM_YEAR x nature of payment.

Source: `THE_LIBRARY.HEALTH.OPEN_PAYMENTS_BY_MANUFACTURER_AND_NATURE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
