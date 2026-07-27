---
title: What is Ripple?
---

# I had a dumb question that turned out not to be dumb.

The U.S. government bans doctors every year. Fraud, patient harm, whatever — they get formally excluded from federal healthcare programs. There's a public list.

Separately, pharmaceutical companies report every dollar they pay to doctors. Also public. Different website, different agency, different file format.

My question was: **has anyone ever just... put those two lists next to each other?**

Like, is anyone checking whether the doctors on the banned list are still getting paid?

Turns out: not really. Or at least not systematically. Because those two datasets come from two different agencies that don't share infrastructure. And it's not just those two — the federal government publishes *thousands* of datasets, from dozens of agencies, and almost none of them are designed to talk to each other.

So I started building something to make them talk.

---

## The idea

What if you took every public federal dataset you could get your hands on, put them all in one place, and just... looked for contradictions?

Person on the "banned" list who's also on the "still getting paid" list. Company on the "debarred" list that still has an active federal contract. Ship on the sanctions list whose transponder is still pinging off the U.S. coast.

Not sophisticated analysis. Not AI making predictions. Just: is this entity on List A *and also* on List B, when being on both is a problem?

That's the core idea. The rest is just making it work at scale.

---

## What's actually in the warehouse right now

```sql warehouse_scale
SELECT
    COUNT(*) as tables,
    SUM(ROW_COUNT) as total_rows
FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'LANDING'
```

<BigValue data={warehouse_scale} value=total_rows title="Total rows loaded" fmt="#,##0" />
<BigValue data={warehouse_scale} value=tables title="Source tables" fmt="#,##0" />

```sql largest_sources
SELECT
    REPLACE(REPLACE(TABLE_NAME, 'FED_', ''), '_', ' ') as source,
    ROW_COUNT as rows
FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'LANDING' AND ROW_COUNT > 0
ORDER BY ROW_COUNT DESC
LIMIT 15
```

<BarChart
    data={largest_sources}
    x=source
    y=rows
    title="Largest source tables (rows)"
    fmt="#,##0"
    swapXY=true
/>

These are all public federal datasets — campaign contributions, court dockets, vessel transponders, SEC filings, Medicare prescriptions, federal contracts, consumer complaints, and more.

---

## How it connects things

Every doctor has an NPI. Every contractor has a UEI. Every vessel has an IMO. These government-issued IDs appear across multiple databases. When the same ID shows up on two lists that contradict each other — that's a lead.

```sql leads_by_detector
SELECT
    REPLACE(RULE_NAME, '_', ' ') as detector,
    COUNT(*) as leads
FROM LIBRARY_META."CONNECT".LEADS
GROUP BY RULE_NAME
ORDER BY leads DESC
```

<BarChart
    data={leads_by_detector}
    x=detector
    y=leads
    title="Leads found per detector"
    fmt="#,##0"
    swapXY=true
/>

<BigValue data={{total_leads: [{total: 1041}]}} value=total title="Total leads (all detectors)" />

Every single lead gets reviewed by a human before anything happens with it. The system finds contradictions. A person decides what they mean.

---

## Continue reading

- [The Engineering](/about/engineering) — How the system is built (the "this isn't AI slop" page)
- [The Findings](/about/findings) — What the system has found so far, with live data
- [Honest Status](/about/status) — What exists, what doesn't, what's next

---

*Built by one person. No funding. No proprietary data. Just public records and a question that wouldn't leave me alone.*
