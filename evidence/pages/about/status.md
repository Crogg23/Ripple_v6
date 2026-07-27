---
title: Honest Status
---

# Where this actually is

No spin. Here's what exists and what doesn't.

---

## What exists right now

```sql scale_numbers
SELECT
    (SELECT COUNT(*) FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'LANDING') as source_tables,
    (SELECT SUM(ROW_COUNT) FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'LANDING') as total_rows,
    (SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY) as registered_sources,
    (SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX) as indexed_portal_datasets,
    (SELECT COUNT(*) FROM LIBRARY_META."CONNECT".MATCH_PAIRS) as connection_pairs,
    (SELECT COUNT(*) FROM LIBRARY_META."CONNECT".LEADS) as total_leads
```

<BigValue data={scale_numbers} value=total_rows title="Rows in the warehouse" fmt="#,##0" />
<BigValue data={scale_numbers} value=source_tables title="Source tables loaded" fmt="#,##0" />
<BigValue data={scale_numbers} value=registered_sources title="Sources registered" fmt="#,##0" />
<BigValue data={scale_numbers} value=indexed_portal_datasets title="Portal datasets indexed" fmt="#,##0" />
<BigValue data={scale_numbers} value=connection_pairs title="Entity match-pairs" fmt="#,##0" />
<BigValue data={scale_numbers} value=total_leads title="Leads generated" fmt="#,##0" />

```sql coverage
SELECT
    ROUND(1942.0 / 338520 * 100, 2) as pct_loaded
```

<BigValue data={coverage} value=pct_loaded title="% of indexed sources loaded" fmt="#,##0.00" suffix="%" />

---

## What doesn't exist yet

**No front-end product.** No website anyone can use (other than this). No app. No published reports. It's all warehouse + build system + this Evidence site.

**No revenue model.** This is pre-product. The engineering is real; the business isn't built yet. Could be a tool for journalists, a service for oversight bodies, a dataset product, or a portfolio piece. Haven't decided.

**Cross-domain entity resolution is partial.** Following one company from EPA violations → federal contracts → campaign donations → SEC filings requires connecting databases that don't share an ID number. Within a domain (healthcare, politics, maritime), the connections are clean. Across domains, I need crosswalk tables that are partially built.

**Coverage is thin.** 338,520 datasets indexed. ~1,942 loaded. That's 0.57%. The long tail is enormous.

---

## The current ceiling

The biggest technical gap is entity resolution across domains.

- **Within healthcare** (NPI key) — works cleanly. 1,020 leads from NPI matches alone.
- **Within politics** (BIOGUIDE/FEC IDs) — works cleanly. Exact IDs.
- **Within maritime** (IMO) — works. 16 leads.
- **Across domains** (is this contractor also this polluter also this donor?) — partially solved. Some crosswalks exist. Most don't. That's the next big unlock.

---

## Has anyone done this before?

Pieces of it, yes:
- OIGs cross-reference within their jurisdiction
- The GAO occasionally does cross-agency work
- ProPublica built individual datasets (Dollars for Docs)

But I haven't found anything that does it *systematically across everything at once* with a generalized connection engine. Which either means I'm onto something, or I'm missing a reason why nobody does this. I'm not sure which yet.

---

## If you're reading this as a hiring manager

This is one person's work. The engineering skills it demonstrates:

- Designing and operating a 555M-row cloud data warehouse (Snowflake)
- Building a 1,032-model dbt pipeline across 24 domains
- Writing ETL frameworks with integrity checking, atomic loads, and recovery
- Entity resolution with graph-based matching across heterogeneous sources
- SQL at depth — window functions, temporal logic, grain management, anti-joins
- Python for infrastructure — loaders, indexers, connection engine
- Data quality practices — false-positive gating, audit trails, methodology caveats
- System design — the whole platform is one coherent system, not a bag of scripts

I'm not claiming it's finished. I'm claiming the engineering is real, the data is real, the methodology is honest, and the question is interesting.

---

[← The Findings](/about/findings) | [Back to overview](/about)

---

*No funding. No team. No proprietary data. Just public records and a question that wouldn't leave me alone.*
