---
title: Medicare Provider Billing
---

```sql n
select 1296739 as row_count
```

What every Medicare provider billed and got paid, 1.3M rows -- follow the money by NPI.

Source: `THE_LIBRARY.HEALTH.MEDICARE_PROVIDER_BILLING` (raw, 1,296,739 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />
