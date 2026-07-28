---
title: "Opioid Prescribers × Industry Money"
---

```sql by_state
select
    STATE as state,
    FLAGGED_PRESCRIBERS as prescribers,
    HIGH_TIER as high_tier,
    TOTAL_OPIOID_PAY_USD as opioid_pay_usd,
    AVG_OPIOID_RATE as avg_opioid_rate,
    IN_HIGH_OVERDOSE_COUNTY_2015 as in_overdose_county
from LIBRARY_MARTS.FINDINGS.OPIOID_PRESCRIBER_PAID_HIGH_RX_BY_STATE
where STATE is not null
order by prescribers desc
```

```sql totals
select
    sum(prescribers) as total_prescribers,
    sum(high_tier) as high_tier_total,
    sum(opioid_pay_usd) as total_pay
from ${by_state}
```

```sql top_prescribers
select
    NPI,
    FIRST_NAME || ' ' || LAST_NAME as name,
    SPECIALTY,
    STATE as state,
    OPIOID_RATE,
    OPIOID_CLAIMS,
    OPIOID_PAY_USD,
    REVIEW_TIER
from LIBRARY_MARTS.FINDINGS.OPIOID_PRESCRIBER_PAID_HIGH_RX
where REVIEW_TIER = 'high'
order by OPIOID_PAY_USD desc
limit 25
```

# Who prescribes the most opioids — and takes money from opioid makers?

6,020 prescribers in the top decile of opioid prescribing *within their own specialty* who also took payments from opioid-analgesic manufacturers (2022–2024). Addiction-treatment payments excluded.

<BigValue data={totals} value=total_prescribers title="Flagged prescribers" fmt="#,##0" />
<BigValue data={totals} value=high_tier_total title="High-tier (review priority)" fmt="#,##0" />
<BigValue data={totals} value=total_pay title="Industry $ to these prescribers" fmt="$#,##0" />

## By state

<USMap
    data={by_state}
    state=state
    value=prescribers
    colorPalette={['#f7fbff','#08306b']}
    title="Flagged opioid prescribers by state"
    fmt="#,##0"
/>

## State detail

<DataTable data={by_state} rows=15 search=true>
    <Column id=state />
    <Column id=prescribers fmt="#,##0" />
    <Column id=high_tier fmt="#,##0" />
    <Column id=opioid_pay_usd fmt="$#,##0" title="Opioid $ paid" />
    <Column id=avg_opioid_rate fmt="0.0%" title="Avg opioid rate" />
    <Column id=in_overdose_county title="In high-OD county (2015)" />
</DataTable>

## Highest-priority leads (review tier = high)

<DataTable data={top_prescribers} rows=15 search=true>
    <Column id=name />
    <Column id=SPECIALTY />
    <Column id=state />
    <Column id=OPIOID_RATE fmt="0.0%" title="Opioid %" />
    <Column id=OPIOID_CLAIMS fmt="#,##0" />
    <Column id=OPIOID_PAY_USD fmt="$#,##0" title="Opioid $" />
</DataTable>
