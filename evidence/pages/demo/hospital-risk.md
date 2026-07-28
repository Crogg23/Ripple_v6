---
title: "Hospital Closure Risk"
---

```sql by_state
select
    STATE as state,
    AT_RISK_HOSPITALS as at_risk,
    CRITICAL as critical,
    HIGH as high,
    RURAL as rural,
    IN_SHORTAGE_COUNTY as in_shortage
from LIBRARY_MARTS.FINDINGS.HOSPITAL_CLOSURE_RISK_BY_STATE
where STATE is not null
order by at_risk desc
```

```sql totals
select
    sum(at_risk) as total_at_risk,
    sum(critical) as total_critical,
    sum(rural) as total_rural,
    sum(in_shortage) as total_shortage
from ${by_state}
```

```sql risk_breakdown
select
    RISK_TIER,
    count(*) as hospitals,
    avg(OPERATING_MARGIN_PCT) as avg_margin,
    avg(MEDICAID_DEPENDENCE_PCT) as avg_medicaid_pct,
    sum(case when IS_RURAL then 1 else 0 end) as rural_count
from LIBRARY_MARTS.FINDINGS.HOSPITAL_CLOSURE_RISK
group by RISK_TIER
order by hospitals desc
```

# Which hospitals are one budget cut from closing?

4,435 hospitals with negative operating margins AND Medicaid dependence. 1,214 are critical — rural, in shortage areas, or both. Timely given current Medicaid cut proposals.

<BigValue data={totals} value=total_at_risk title="At-risk hospitals" fmt="#,##0" />
<BigValue data={totals} value=total_critical title="Critical tier" fmt="#,##0" />
<BigValue data={totals} value=total_rural title="Rural" fmt="#,##0" />
<BigValue data={totals} value=total_shortage title="In shortage county" fmt="#,##0" />

## Map: at-risk hospitals by state

<USMap
    data={by_state}
    state=state
    value=at_risk
    colorPalette={['#fff5f0','#67000d']}
    title="Hospitals at closure risk"
    fmt="#,##0"
/>

## Risk tier breakdown

<BarChart
    data={risk_breakdown}
    x=RISK_TIER
    y=hospitals
    title="Hospitals by risk tier"
    fmt="#,##0"
/>

<DataTable data={risk_breakdown} rows=5>
    <Column id=RISK_TIER title="Tier" />
    <Column id=hospitals fmt="#,##0" />
    <Column id=avg_margin fmt="0.1%" title="Avg margin" />
    <Column id=avg_medicaid_pct fmt="0.1%" title="Avg Medicaid %" />
    <Column id=rural_count fmt="#,##0" title="Rural" />
</DataTable>

## State detail

<DataTable data={by_state} rows=15 search=true>
    <Column id=state />
    <Column id=at_risk fmt="#,##0" title="At risk" />
    <Column id=critical fmt="#,##0" />
    <Column id=high fmt="#,##0" />
    <Column id=rural fmt="#,##0" />
    <Column id=in_shortage fmt="#,##0" title="In shortage" />
</DataTable>
