# Ripple

---

# I had a dumb question that turned out not to be dumb.

The U.S. government bans doctors every year. Fraud, patient harm, whatever — they get formally excluded from federal healthcare programs. There's a public list.

Separately, pharmaceutical companies report every dollar they pay to doctors. Also public. Different website, different agency, different file format.

My question was: **has anyone ever just... put those two lists next to each other?**

Like, is anyone checking whether the doctors on the banned list are still getting paid?

Turns out: not really. Or at least not systematically. Because those two datasets come from two different agencies that don't share infrastructure. And it's not just those two — the federal government publishes *thousands* of datasets, from dozens of agencies, and almost none of them are designed to talk to each other.

So I started building something to make them talk.

---

# The idea

What if you took every public federal dataset you could get your hands on, put them all in one place, and just... looked for contradictions?

Person on the "banned" list who's also on the "still getting paid" list. Company on the "debarred" list that still has an active federal contract. Ship on the sanctions list whose transponder is still pinging off the U.S. coast.

Not sophisticated analysis. Not AI making predictions. Just: is this entity on List A *and also* on List B, when being on both is a problem?

That's the core idea. The rest is just making it work at scale.

---

# What "making it work at scale" actually means

Here's where the idea meets reality. You can't just dump 875 million rows of government data into a spreadsheet and ctrl+F your way through it. There's real engineering in between "interesting question" and "actual answer."

**Problem 1: The data arrives messy.**

Every federal dataset is its own universe. The NPI provider registry has 330 columns and 9.6 million rows. The AIS vessel tracking archive has 58 million rows from an 8-day window. USASpending has 6.3 million contract transaction records. They're all formatted differently, typed differently, published on different schedules.

Here's what the 10 largest source tables look like:

```
┌──────────────────────────────────────────────────────┬────────────────┐
│ Source Table                                         │ Rows           │
├──────────────────────────────────────────────────────┼────────────────┤
│ DEA ARCOS (controlled-substance transactions)        │ 178,598,026    │
│ SEC 13F Holdings                                     │ 101,261,252    │
│ FEC Individual Contributions                         │ 84,172,112     │
│ CourtListener Dockets                                │ 71,677,647     │
│ NOAA AIS (vessel transponders)                       │ 58,106,517     │
│ CMS Part D Prescriber-Drug                           │ 25,869,521     │
│ FDA FAERS (adverse-event drugs)                      │ 20,914,284     │
│ FDA FAERS (adverse-event reactions)                  │ 20,621,386     │
│ USASpending Contracts                                │ 20,000,000     │
│ USASpending Assistance                               │ 19,902,879     │
└──────────────────────────────────────────────────────┴────────────────┘
Total across all 1,937 landing tables: 875,575,558 rows
```

So the first job is just: pour everything into one warehouse, then write a cleaning model for each source. I have 975 of those cleaning models now. Each one handles one source's specific quirks — deduplication, type casting, normalization, grain definition. Not glamorous. Very necessary.

**Problem 2: The same entity has different IDs in different systems.**

This is the key insight that makes the whole thing work (or doesn't).

Every doctor has a 10-digit NPI. Every federal contractor has a UEI. Every sanctioned vessel has an IMO number. These are government-issued, globally unique identifiers that appear across multiple databases.

If I see the same NPI in the exclusion list *and* the payments file — that's the same human being. No probability involved. The government assigned the number. I'm just checking it across their own databases.

But here's the catch: some sources left-pad the NPI and some don't. Some include the "IMO" prefix and some just have the digits. EINs have hyphens in some places and not others. So every key type needs normalization logic before you can match it. And some domains (healthcare, politics, maritime) have clean hard IDs. Other domains (environment, corporate ownership) mostly... don't. That's where the system hits its current ceiling.

**Problem 3: Counting things correctly is harder than it sounds.**

USASpending publishes contracts at the *transaction* level — every modification to every contract is its own row. If you count rows naively, you get 174x inflation. I had to write an intermediate model that rolls transactions up to the award level.

One of my early findings looked great: 243 excluded providers still in the prescriber file. Then I checked dates. 242 of them were excluded *after* the prescriber file's reference year. They prescribed, then got banned later. My finding was backwards. I killed it and started over with proper temporal logic.

That kind of thing happens constantly. The "interesting question" takes five minutes. Making sure the answer is actually correct takes days.

---

# What I built to do this

The short version of the tech:

- **Snowflake warehouse** — where the data lives. 875 million rows across 1,937 landing tables. Four databases, organized by function (raw landing, metadata/registry, staging, marts).
- **dbt pipeline** — 1,378 transformation models in a dependency graph (975 staging, 399 marts, 4 intermediate). Staging layer (clean the source), intermediate layer (fix grain, union years), mart layer (query-ready domain tables).
- **Custom loading framework** — Python. Handles downloading, checksumming, deduplication, atomic loads, and recovery if something fails mid-load.
- **Portal indexer** — crawled open-data portals and cataloged 338,520 datasets. Tagged each one with which government ID types it carries. That's the map of "what's out there to load next."
- **Entity resolution engine** — profiles every table for known ID patterns, normalizes them, and builds a graph of where each entity appears. 22.6 million entities and 31.1 million match-pairs across datasets right now.
- **Detection layer** — eight rules that run cross-table intersection queries. Gated by thresholds so random noise doesn't create false leads.

About 1,400 hand-authored SQL files (1,378 of them dbt models), 309 Python files,
and 1,400 YAML configs. One person, about 40 days so far in this version.

(That SQL number counts files I wrote. dbt also *compiles* every model into
`target/`, which balloons the on-disk `.sql` count past 20,000 — but those are
machine-generated copies, not work, and it would be dishonest to claim them.)

The source registry organizes everything by domain:

```
┌─────────────────────────────┬─────────┐
│ Domain                      │ Sources │
├─────────────────────────────┼─────────┤
│ Open Data Portal (misc)     │ 1,404   │
│ Health & Medicine           │   135   │
│ Economy, Labor & Trade      │   108   │
│ Housing & Social            │   101   │
│ Transport & Movement        │    91   │
│ Corporate Entities          │    89   │
│ Education                   │    86   │
│ Science & Research          │    73   │
│ Justice & Courts            │    68   │
│ Government & Power          │    67   │
│ Energy & Environment        │    60   │
│ Money in Politics           │    58   │
│ Spending & Budget           │    50   │
│ History & Culture           │    37   │
│ Crime & Security            │    33   │
├─────────────────────────────┼─────────┤
│ Subtotal (15 domains above) │ 2,460   │
│ Seven smaller domains       │   114   │
│ Not yet classified          │   418   │
├─────────────────────────────┼─────────┤
│ Total registered            │ 2,992   │
└─────────────────────────────┴─────────┘
```

---

# What it's found so far

The eight detectors have produced 17,256 leads. Here's the actual query that backs this up:

```sql
-- "Show me every lead, grouped by which detector found it"
SELECT RULE_NAME, COUNT(*) as leads
FROM LIBRARY_META.CONNECT.LEADS
GROUP BY RULE_NAME
ORDER BY leads DESC;
```

```
┌─────────────────────────────────────────┬────────┐
│ Detector                                │  Leads │
├─────────────────────────────────────────┼────────┤
│ osha_cohort_outlier_2024                │ 16,215 │
│ banned_but_paid                         │    773 │
│ excluded_but_billing                    │    236 │
│ sanctioned_vessel_broadcasting_v2       │     12 │
│ banned_but_operating                    │     11 │
│ sanctioned_vessel_broadcasting (v1)     │      4 │
│ sec_filer_in_irs_bmf                    │      3 │
│ debarred_but_funded                     │      2 │
├─────────────────────────────────────────┼────────┤
│ Total                                   │ 17,256 │
└─────────────────────────────────────────┴────────┘
```

Those are two different kinds of finding, and the split matters more than the total.

`osha_cohort_outlier_2024` is a **statistical sweep**: it scores every OSHA
establishment against its own NAICS-and-size peer cohort and flags the ones whose
injury rate runs at least 2x the pooled rate on 5+ cases. 16,215 of those is not a
surprise — that's what a population-wide outlier scan returns. Each one is a
neutral, peer-relative observation with frozen SQL behind it, not an accusation.

The other seven are **intersection rules**: the same hard ID (NPI / IMO / UEI)
appearing on a flag list and an activity list at the same time. Those are rarer by
construction, which is why the counts are small.

Most of the intersection leads are healthcare-related (NPI-keyed). That's partly
because healthcare has the cleanest IDs, and partly because I've focused more
effort there. The other domains are thinner — honestly, some of those single-digit
counts reflect incomplete crosswalk data more than a lack of real problems.

Nothing in this table has been reviewed or published. Every one is a lead pending
human sign-off; auto-publish is structurally blocked.

---

# The deeper maps (beyond binary yes/no detectors)

## Opioid prescribers receiving opioid-manufacturer payments

```sql
-- The core logic (simplified):
-- 1. Find doctors in the top 10% of opioid prescribing WITHIN their specialty
-- 2. Join to Open Payments on NPI
-- 3. Filter to payments linked to opioid-analgesic drugs
-- 4. Exclude addiction-treatment payments (Suboxone, naloxone, OUD)

SELECT REVIEW_TIER, COUNT(*) as doctors,
       ROUND(AVG(OPIOID_PAY_USD), 2) as avg_pay_usd,
       ROUND(AVG(OPIOID_RATE), 1) as avg_opioid_rx_pct
FROM LIBRARY_MARTS.FINDINGS.OPIOID_PRESCRIBER_PAID_HIGH_RX
GROUP BY REVIEW_TIER ORDER BY doctors DESC;
```

```
┌─────────────┬─────────┬─────────────────┬─────────────────────┐
│ Review Tier │ Doctors │ Avg Payment ($) │ Avg Opioid Rx Rate  │
├─────────────┼─────────┼─────────────────┼─────────────────────┤
│ low         │   5,485 │         $188.90 │ 47.3% of their Rx   │
│ medium      │     508 │       $2,039.88 │ 64.1% of their Rx   │
│ high        │      27 │      $54,248.21 │ 59.8% of their Rx   │
├─────────────┼─────────┼─────────────────┼─────────────────────┤
│ Total       │   6,020 │                 │                     │
└─────────────┴─────────┴─────────────────┴─────────────────────┘
```

The 27 "high" tier doctors are averaging $54,000 in opioid-manufacturer payments while writing 60% of their prescriptions for opioids. Again — not an accusation. But a pattern worth looking at.

Top 10 states:

```
┌───────┬─────────┬──────────────────┐
│ State │ Doctors │ Avg Opioid Pay   │
├───────┼─────────┼──────────────────┤
│ FL    │     455 │           $799   │
│ CA    │     414 │           $491   │
│ TX    │     343 │           $702   │
│ NC    │     300 │           $530   │
│ MI    │     250 │           $250   │
│ TN    │     247 │           $384   │
│ AZ    │     242 │           $780   │
│ OH    │     234 │           $562   │
│ GA    │     203 │           $996   │
│ IN    │     200 │           $225   │
└───────┴─────────┴──────────────────┘
```

---

## Hospitals at financial closure risk

```sql
-- Combines Medicare Cost Reports (margins) + HRSA shortage areas
-- + Medicaid dependency + rural classification

SELECT RISK_TIER, COUNT(*) as hospitals
FROM LIBRARY_MARTS.FINDINGS.HOSPITAL_CLOSURE_RISK
GROUP BY RISK_TIER ORDER BY hospitals DESC;
```

```
┌──────────┬───────────┐
│ Tier     │ Hospitals │
├──────────┼───────────┤
│ elevated │     3,134 │
│ critical │     1,214 │
│ high     │        87 │
├──────────┼───────────┤
│ Total    │     4,435 │
└──────────┴───────────┘
```

"Critical" means: negative operating margin AND Medicaid-dependent AND in a shortage area or rural county. These are hospitals that are losing money, depend on federal funding that's under political threat, and serve communities with no nearby alternative.

Top 10 states by critical hospitals:

```
┌───────┬──────────────────────┐
│ State │ Critical Hospitals   │
├───────┼──────────────────────┤
│ CA    │                  137 │
│ TX    │                  107 │
│ LA    │                   79 │
│ NY    │                   58 │
│ IL    │                   49 │
│ OH    │                   42 │
│ FL    │                   39 │
│ PA    │                   34 │
│ OK    │                   33 │
│ AZ    │                   32 │
└───────┴──────────────────────┘
```

---

## PACs funding both parties

```sql
-- PACs that fund 10+ members of Congress, sorted by total spend

SELECT CMTE_NAME, DEM_MEMBERS, REP_MEMBERS, MEMBERS_FUNDED,
       ROUND(TOTAL_USD, 0) as total_usd
FROM LIBRARY_MARTS.FINDINGS.PAC_FUNDS_BOTH_SIDES
WHERE BOTH_SIDES_FLAG = TRUE
ORDER BY TOTAL_USD DESC LIMIT 5;
```

```
┌──────────────────────────────────────┬──────┬──────┬───────┬──────────────┐
│ PAC Name                             │ Dems │ Reps │ Total │ Total $      │
├──────────────────────────────────────┼──────┼──────┼───────┼──────────────┤
│ FAIRSHAKE (crypto)                   │   13 │   12 │    25 │ $24,855,548  │
│ National Assoc. of Realtors          │  268 │  278 │   550 │ $10,706,096  │
│ AIPAC                                │  157 │  251 │   412 │  $8,392,834  │
│ America's Credit Unions              │  239 │  242 │   484 │  $6,438,914  │
│ American Hospital Association        │  219 │  219 │   440 │  $4,930,487  │
└──────────────────────────────────────┴──────┴──────┴───────┴──────────────┘
2,680 PACs total funding 10+ members. 1,359 fund both parties.
```

The Realtors PAC gave to 546 members of Congress. Both parties. $10.7 million. That's not ideology — that's access purchasing.

---

# The full findings catalog

Everything that's been built and registered:

```sql
SELECT * FROM LIBRARY_MARTS.FINDINGS.CATALOG;
```

```
┌─────────────────────────────────────────────────────┬────────┬─────────────────────────────────┐
│ Finding                                             │ Rows   │ Who gets hurt                   │
├─────────────────────────────────────────────────────┼────────┼─────────────────────────────────┤
│ Revoked nonprofits still flagged tax-deductible     │ 22,512 │ Donors giving to dead orgs      │
│ Opioid prescribers paid by opioid manufacturers     │  6,020 │ Patients                        │
│ Hospitals at financial closure risk                  │  4,435 │ Communities losing healthcare   │
│ PACs funding both sides of Congress                  │  2,680 │ Public (access-buying)          │
│ Members of Congress: money vs. output               │    635 │ Voters                          │
│ Excluded providers paid after exclusion (shortage)  │    287 │ Patients in underserved areas   │
│ Excluded providers paid after exclusion             │    287 │ Patients / taxpayers            │
│ Excluded providers still at facilities              │     28 │ Patients at those facilities    │
│ Federal contractors with EPA violations             │     21 │ Taxpayers / environment         │
└─────────────────────────────────────────────────────┼────────┼─────────────────────────────────┘
                                                  9 findings registered
```

Each one carries: the SQL that produced it, the source dates, known caveats, methodology description, and a "who gets hurt" field — because if there's no human on the other end of the number, it's trivia, not a finding.

---

# What I don't know yet

**Is this a product?** Maybe. I don't know what the business model is. Could be a tool for journalists, a service for oversight bodies, a dataset product, or just a portfolio piece that demonstrates what's possible. Haven't decided.

**Is this complete?** No. I've loaded ~2,000 of the 338,000 datasets I've indexed. The entity resolution works cleanly within single domains (all healthcare, all politics) but breaks down across domains. Following one company from EPA violations to federal contracts to campaign donations requires crosswalk tables I haven't fully built.

**Am I sure the findings are right?** The ones in the catalog — yes. I've been burned enough times by temporal bugs, grain traps, and false positives that I now validate obsessively. Every finding carries its methodology, source dates, known caveats, and the actual SQL that produced it. But I'm one person doing QA on my own work, so I hold everything loosely.

**Has anyone done this before?** Pieces of it, yes. OIGs do cross-reference within their jurisdiction. The GAO occasionally does cross-agency work. ProPublica built individual datasets (Dollars for Docs). But I haven't found anything that does it *systematically across everything at once* with a generalized connection engine. Which either means I'm onto something, or I'm missing a reason why nobody does this. I'm not sure which yet.

---

# Why I think it might matter

The federal government publishes all this data. Taxpayers paid for it. Oversight agencies exist to find waste and fraud. But each agency only looks at its own silo.

The data to find cross-agency patterns already exists. It's already public. The joins are just... sitting there.

My hypothesis is that a single generalized system that looks across *all of it at once* will find things that no single-silo investigation ever would. So far, that seems to be true. Whether it's useful at scale, sustainable for one person, or interesting to anyone else — those are open questions.

But 773 banned doctors still getting pharma checks seems like it shouldn't be a thing. And 1,214 hospitals about to close seems like something someone should know about before it happens. And if the data's already public and the IDs already match... I'm not sure what the argument is for *not* looking.

---

# If you're reading this as a hiring manager

This is one person's work. The engineering skills it demonstrates:

- Designing and operating an 875M-row cloud data warehouse (Snowflake)
- Building a 1,378-model dbt pipeline across 24 domains
- Writing ETL frameworks with integrity checking, atomic loads, and recovery
- Entity resolution with graph-based matching across heterogeneous sources
- SQL at depth — window functions, temporal logic, grain management, anti-joins
- Python for infrastructure — loaders, indexers, connection engine
- Data quality practices — false-positive gating, audit trails, methodology caveats
- System design — the whole platform is one coherent system, not a bag of scripts

I'm not claiming it's finished. I'm claiming the engineering is real, the data is real, the methodology is honest, and the question is interesting.

---

*No funding. No team. No proprietary data. Just public records and a question that wouldn't leave me alone.*
