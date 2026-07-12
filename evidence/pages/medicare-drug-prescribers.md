---
title: Medicare Drug Prescribers
---

```sql n
select 1416883 as row_count
```

What every Medicare Part D prescriber wrote -- 1.4M providers, including opioid prescribing rates.

Source: `THE_LIBRARY.HEALTH.MEDICARE_DRUG_PRESCRIBERS` (raw, 1,416,883 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />
