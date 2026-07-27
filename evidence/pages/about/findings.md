---
title: The Findings
---

# What the system has found so far

Nine findings registered in the catalog. Each carries methodology, source dates, known caveats, and a "who gets hurt" field — because if there's no human on the other end of the number, it's trivia, not a finding.

```sql catalog
SELECT
    FINDING as finding,
    WHAT as description,
    WHO_GETS_HURT as who_gets_hurt,
    ROWS_ as rows
FROM LIBRARY_MARTS.FINDINGS.CATALOG
ORDER BY ROWS_ DESC
```

<DataTable data={catalog} rows=20>
    <Column id=finding title="Finding" />
    <Column id=description title="What it is" />
    <Column id=who_gets_hurt title="Who gets hurt" />
    <Column id=rows title="Rows" fmt="#,##0" />
</DataTable>

---

## Opioid prescribers receiving opioid-manufacturer payments

Doctors in the top 10% of opioid prescribing within their own specialty who are also taking money from opioid-analgesic manufacturers. Addiction treatment payments (Suboxone, naloxone, OUD) are excluded.

```sql opioid_tiers
SELECT
    REVIEW_TIER as tier,
    COUNT(*) as doctors,
    ROUND(AVG(OPIOID_PAY_USD), 2) as avg_pay_usd,
    ROUND(AVG(OPIOID_RATE), 1) as avg_opioid_rate_pct
FROM LIBRARY_MARTS.FINDINGS.OPIOID_PRESCRIBER_PAID_HIGH_RX
GROUP BY REVIEW_TIER
ORDER BY avg_pay_usd DESC
```

<DataTable data={opioid_tiers}>
    <Column id=tier title="Review Tier" />
    <Column id=doctors title="Doctors" fmt="#,##0" />
    <Column id=avg_pay_usd title="Avg Opioid Payment" fmt="$#,##0" />
    <Column id=avg_opioid_rate_pct title="Avg Opioid Rx Rate %" fmt="#,##0.0" />
</DataTable>

The 27 "high" tier doctors average $54,000 in opioid-manufacturer payments while writing ~60% of their prescriptions for opioids.

```sql opioid_by_state
SELECT
    STATE as state,
    COUNT(*) as doctors,
    ROUND(AVG(OPIOID_PAY_USD), 0) as avg_pay
FROM LIBRARY_MARTS.FINDINGS.OPIOID_PRESCRIBER_PAID_HIGH_RX
GROUP BY STATE
ORDER BY doctors DESC
LIMIT 15
```

<BarChart
    data={opioid_by_state}
    x=state
    y=doctors
    title="Flagged opioid prescribers by state"
    fmt="#,##0"
/>

Not an accusation. A pattern. One doctor is an anecdote. Six thousand is a system.

---

## Hospitals at financial closure risk

Hospitals with negative operating margins, Medicaid-dependent, in shortage areas or rural counties.

```sql hospital_tiers
SELECT
    RISK_TIER as tier,
    COUNT(*) as hospitals
FROM LIBRARY_MARTS.FINDINGS.HOSPITAL_CLOSURE_RISK
GROUP BY RISK_TIER
ORDER BY hospitals DESC
```

<BarChart
    data={hospital_tiers}
    x=tier
    y=hospitals
    title="Hospitals by risk tier"
    fmt="#,##0"
/>

```sql hospital_by_state
SELECT
    STATE as state,
    COUNT(*) as critical_hospitals
FROM LIBRARY_MARTS.FINDINGS.HOSPITAL_CLOSURE_RISK
WHERE RISK_TIER = 'critical'
GROUP BY STATE
ORDER BY critical_hospitals DESC
LIMIT 15
```

<BarChart
    data={hospital_by_state}
    x=state
    y=critical_hospitals
    title="Critical-risk hospitals by state (neg margin + Medicaid-dependent + shortage area)"
    fmt="#,##0"
    swapXY=true
/>

1,214 hospitals that are losing money, depend on federal funding under political threat, and serve communities with no nearby alternative. This map exists now, before the closures happen.

---

## PACs funding both sides of Congress

PACs that donate to 10+ members of Congress, funding both parties. Not ideology — access purchasing.

```sql pac_top
SELECT
    CMTE_NAME as pac_name,
    DEM_MEMBERS as dems,
    REP_MEMBERS as reps,
    MEMBERS_FUNDED as total_members,
    ROUND(TOTAL_USD, 0) as total_usd
FROM LIBRARY_MARTS.FINDINGS.PAC_FUNDS_BOTH_SIDES
WHERE BOTH_SIDES_FLAG = TRUE
ORDER BY TOTAL_USD DESC
LIMIT 10
```

<DataTable data={pac_top}>
    <Column id=pac_name title="PAC" />
    <Column id=dems title="Dem Members" fmt="#,##0" />
    <Column id=reps title="Rep Members" fmt="#,##0" />
    <Column id=total_members title="Total Funded" fmt="#,##0" />
    <Column id=total_usd title="Total $" fmt="$#,##0" />
</DataTable>

```sql pac_summary
SELECT
    COUNT(*) as total_pacs,
    SUM(CASE WHEN BOTH_SIDES_FLAG THEN 1 ELSE 0 END) as funds_both_parties
FROM LIBRARY_MARTS.FINDINGS.PAC_FUNDS_BOTH_SIDES
```

<BigValue data={pac_summary} value=total_pacs title="PACs funding 10+ members" fmt="#,##0" />
<BigValue data={pac_summary} value=funds_both_parties title="Of those, fund both parties" fmt="#,##0" />

The Realtors PAC gave to 546 members of Congress. Both parties. $10.7 million. That's not ideology — that's a seat at the table regardless of who wins.

---

## Excluded providers still getting paid after exclusion

```sql excluded_paid
SELECT
    COUNT(*) as providers
FROM LIBRARY_MARTS.FINDINGS.EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION
```

<BigValue data={excluded_paid} value=providers title="Excluded providers paid after ban" fmt="#,##0" />

287 providers who were formally excluded from federal healthcare programs and then received payments from pharmaceutical companies *after* their exclusion date. Temporal direction verified — these are not "prescribed then got banned." These are "banned, then paid anyway."

---

[← The Engineering](/about/engineering) | [Honest Status →](/about/status)
