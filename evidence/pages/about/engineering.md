---
title: The Engineering
---

# What "making it work at scale" actually means

You can't just dump 500 million rows of government data into a spreadsheet and ctrl+F your way through it. There's real engineering between "interesting question" and "actual answer."

---

## The data arrives messy

Every federal dataset is its own universe. Different formats, different schemas, different quirks. Here's what the source registry looks like by domain:

```sql sources_by_domain
SELECT
    COALESCE(DOMAIN_PRIMARY, 'unclassified') as domain,
    COUNT(*) as sources
FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY
WHERE DOMAIN_PRIMARY IS NOT NULL
GROUP BY DOMAIN_PRIMARY
ORDER BY sources DESC
LIMIT 15
```

<BarChart
    data={sources_by_domain}
    x=domain
    y=sources
    title="Registered sources by domain"
    fmt="#,##0"
    swapXY=true
/>

```sql source_count
SELECT COUNT(*) as registered_sources FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY
```

<BigValue data={source_count} value=registered_sources title="Sources in the registry" fmt="#,##0" />

Each source needs its own transformation model — handling deduplication, type casting, normalization, grain definition. I have 969 of those. Not glamorous. Very necessary.

---

## The same entity has different IDs in different systems

This is the key insight. The government assigns unique IDs — NPI for doctors, UEI for contractors, IMO for vessels, EIN for nonprofits, CIK for public companies. These show up across multiple databases.

```sql entity_spine
SELECT COUNT(*) as match_pairs FROM LIBRARY_META."CONNECT".MATCH_PAIRS
```

<BigValue data={entity_spine} value=match_pairs title="Entity match-pairs in the connection graph" fmt="#,##0" />

If I see the same NPI in the exclusion list *and* the payments file — that's the same human being. No probability involved. The government assigned the number. I'm just checking it across their own databases.

But here's the catch: some sources left-pad the NPI and some don't. Some include the "IMO" prefix and some just have the digits. EINs have hyphens in some places and not others. Every key type needs normalization before matching.

---

## The leads break down by key type

```sql leads_by_key
SELECT
    LEFT_KEY_TYPE as key_type,
    COUNT(*) as matches
FROM LIBRARY_META."CONNECT".LEADS
GROUP BY LEFT_KEY_TYPE
ORDER BY matches DESC
```

<BarChart
    data={leads_by_key}
    x=key_type
    y=matches
    title="Leads by identifier type"
    fmt="#,##0"
/>

Most leads are NPI-keyed (healthcare). That's partly because healthcare has the cleanest government IDs, and partly because I've focused more effort there. The other domains are thinner — honestly reflecting incomplete crosswalk data more than a lack of real problems.

---

## Counting things correctly is harder than it sounds

USASpending publishes contracts at the *transaction* level — every modification is its own row. Count naively and you get 174x inflation. I wrote an intermediate model to roll transactions up to award grain.

One early finding looked great: 243 excluded providers still in the prescriber file. Then I checked dates. 242 were excluded *after* the prescriber file's reference year. They prescribed, then got banned later. The finding was backwards. I killed it and rebuilt with temporal logic.

That kind of thing happens constantly. The "interesting question" takes five minutes. Making sure the answer is correct takes days.

---

## The tech stack

| Layer | What it does |
|-------|-------------|
| **Snowflake** | Cloud warehouse. 555M+ rows, 1,942 tables, four databases |
| **dbt** | 1,032 transformation models in a dependency graph (staging → intermediate → marts) |
| **Custom Python loaders** | Downloading, checksumming, deduplication, atomic loads, recovery |
| **Portal indexer** | Crawled 338,520 open-data datasets. Tagged each with detected join keys |
| **Entity resolution** | Profiles tables for ID patterns, normalizes, builds the connection graph |
| **Detection layer** | Six rule-based cross-domain intersection queries |
| **Evidence.dev** | This site — live queries against the warehouse |

About 10,500 SQL files, 300 Python files, 2,800 YAML configs. One person.

---

## Why this isn't "just AI"

- **AI didn't clean 969 sources.** Each one has its own grain, its own quirks, its own deduplication logic.
- **AI didn't catch the temporal bug.** The backwards-finding was killed by checking dates by hand.
- **AI didn't design the connection engine.** Normalization logic per key type, authority-ranked survivorship, minimum-match gating.
- **AI didn't decide what counts as a finding.** The "who gets hurt" requirement, the libel-trap exclusions, the caveating methodology — those are human editorial decisions.

I use AI to help write code (like a power tool). But the system runs on plain SQL, deterministic joins, and hard government ID numbers. No model decides who's "guilty." No algorithm picks targets.

---

[Back to overview](/about) | [The Findings →](/about/findings)
