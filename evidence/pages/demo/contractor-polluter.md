---
title: "Federal Contractors × EPA Violators"
---

```sql contractors
select
    COMPANY_NAME as company,
    VIOLATING_FACILITIES as facilities,
    ANY_SNC as significant_noncompliance,
    TOTAL_EPA_PENALTIES as epa_penalties,
    TOTAL_FORMAL_ACTIONS as formal_actions,
    FEDERAL_DOLLARS_OBLIGATED as fed_dollars,
    N_AWARDS as awards,
    N_AGENCIES as agencies,
    MATCH_CONFIDENCE as confidence
from LIBRARY_MARTS.FINDINGS.FEDERAL_CONTRACTOR_EPA_VIOLATOR
order by FEDERAL_DOLLARS_OBLIGATED desc
```

```sql totals
select
    count(*) as companies,
    sum(fed_dollars) as total_fed_dollars,
    sum(epa_penalties) as total_penalties,
    sum(facilities) as total_facilities
from ${contractors}
```

# Your tax dollars, their violations

21 companies that simultaneously receive billions in federal contracts AND operate facilities with EPA violations. The government funds the very companies it penalizes for environmental harm.

<BigValue data={totals} value=companies title="Companies" />
<BigValue data={totals} value=total_fed_dollars title="Federal $ obligated" fmt="$#,##0" />
<BigValue data={totals} value=total_penalties title="EPA penalties" fmt="$#,##0" />
<BigValue data={totals} value=total_facilities title="Violating facilities" fmt="#,##0" />

## Federal money vs EPA penalties

<BarChart
    data={contractors}
    x=company
    y=fed_dollars
    fmt="$#,##0"
    swapXY=true
    title="Federal contract dollars by company"
/>

## Full detail

<DataTable data={contractors} rows=21 search=true>
    <Column id=company />
    <Column id=fed_dollars fmt="$#,##0" title="Fed $" />
    <Column id=epa_penalties fmt="$#,##0" title="EPA penalties" />
    <Column id=facilities fmt="#,##0" title="Violating sites" />
    <Column id=formal_actions fmt="#,##0" title="Formal actions" />
    <Column id=agencies title="Fed agencies paying" />
    <Column id=significant_noncompliance title="SNC?" />
    <Column id=confidence fmt="0.00" title="Match conf." />
</DataTable>

---

*Coverage note: This finding is limited by the EPA→USASpending crosswalk. Only 6,886 of 500K+ EPA records carry a parent UEI that links to federal contracts. The real universe is much larger — this is the high-confidence floor, not the ceiling.*
