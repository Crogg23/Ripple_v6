---
title: The National Debt, Daily
---

```sql debt
select * from library.national_debt
```

```sql latest
select
    record_date,
    total_debt_tn,
    public_debt_tn,
    intragov_debt_tn
from library.national_debt
order by record_date desc
limit 1
```

Treasury's **Debt to the Penny** — the total public debt outstanding, every business
day. Source: `fed_treasury_debt_to_penny`, a typed curated mart.

<BigValue data={latest} value=total_debt_tn title="Total debt, $ trillions (latest)" fmt="#,##0.00" />
<BigValue data={latest} value=public_debt_tn title="Held by the public, $ trillions" fmt="#,##0.00" />
<BigValue data={latest} value=record_date title="As of" />

<LineChart
    data={debt}
    x=record_date
    y={["total_debt_tn", "public_debt_tn", "intragov_debt_tn"]}
    title="US federal debt, daily ($ trillions)"
    yAxisTitle="$ trillions"
    yFmt="$#,##0.0"
/>
