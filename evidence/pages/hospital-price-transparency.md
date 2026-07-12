---
title: Hospital Price Transparency
---

```sql rows
select * from library.hospital_price_transparency
```

```sql n
select count(*) as row_count from library.hospital_price_transparency
```

Hospital standard-charge (price transparency) file schema (1-row stub).

Source: `THE_LIBRARY.HEALTH.HOSPITAL_PRICE_TRANSPARENCY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
