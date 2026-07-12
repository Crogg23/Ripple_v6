---
title: Injury Violence Death Rates
---

```sql n
select 132000 as row_count
```

County-level death rates from injury, overdose, and violence (including guns), by intent.

Source: `THE_LIBRARY.HEALTH.INJURY_VIOLENCE_DEATH_RATES` (raw, 132,000 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />
