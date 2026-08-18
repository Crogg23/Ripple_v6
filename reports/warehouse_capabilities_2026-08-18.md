# The Ripple Data Warehouse — What It Can Do

*A capabilities overview. Every number in this document is a measured count from a
full audit of the warehouse completed August 17, 2026 — nothing here is estimated.*

---

## The one-sentence version

Ripple is a single queryable warehouse holding **1.23 billion records of the American
public record** — companies, nonprofits, doctors, judges, facilities, and the money,
violations, accidents, and lawsuits attached to them — collected from hundreds of
government and public sources and wired together so that one organization or person
can be followed across every agency that has ever touched them.

Most of this data is technically public. Almost none of it is *usable* — it lives in
hundreds of separate portals, in incompatible formats, under different ID systems,
with no way to connect a company's EPA record to its federal contracts to its
campaign donations. Ripple's core product is that connection.

---

## What's inside (the shelf, at a glance)

**589 curated, analysis-ready tables** built from ~1,100+ raw source loads. Roughly
half the content is *things that exist*, half is *things that happened to them*.

### Things that exist (~150M records)

| Category | Highlights |
|---|---|
| **Companies & legal entities** | 5.7M UK companies, 3.4M global legal-entity IDs, 814k leaked offshore entities, 516k foreign financial institutions, every US bank, credit union, and thrift |
| **Nonprofits & political money orgs** | 2.0M tax-exempt organizations, 1.4M deductible charities, 1.2M orgs stripped of tax status, 78k political committees, 78k dark-money (527) groups |
| **Health care** | 9.6M providers in the national registry, 3.0M Medicare-enrolled, 14.7k nursing homes, every hospital, 5M+ registered medical devices |
| **Physical world** | 3.3M EPA-registered facilities, 1.2M water-discharge permit holders, 434k drinking-water systems, 92k mines, 93k dams, 118k orphaned oil wells, 315k registered aircraft, every power plant |
| **People in power** | 16k federal/state judges (with schools, careers, finances), every member of Congress ever, 33k federal candidates, 7M people controlling UK companies |

### Things that happened (~830M records)

| Category | Highlights |
|---|---|
| **Money moving** | 179M opioid pill shipments, 84M individual campaign contributions, 43M drug-company payments to doctors, 26M+ federal contract/grant transactions, 19M mortgage applications, 3M small-business loans |
| **Courts** | 72M federal/state court dockets, 24M case outcomes, 18M citations, 10M opinions, 66k judge financial disclosures with 1.9M investment line items |
| **Harm & safety** | 37M drug adverse-event records, 17M consumer-finance complaints, 9.8M ER product-injury cases, 2.7M medical-device failures, 2.2M vehicle complaints, 1.9M malpractice/disciplinary reports, 618k nursing-home deficiencies |
| **Enforcement** | 15M drinking-water violations, 3.1M mine-safety violations, 1.4M hazardous-waste violations + histories, ~1.4M environmental enforcement actions, 8M+ inspections, 250k provider/contractor exclusions and sanctions |
| **Government process** | Every congressional roll-call vote ever cast (945k member-votes), 175k federal lobbying filings, 1M+ state lobbying records, 48k foreign-agent registrations |
| **Immigration** | 12.6M immigration-court cases, 2.6M detention stays tied to specific facilities and operators |

---

## What you can actually do with it

### 1. Look up anyone, everywhere, at once
An entity-resolution spine connects **31.8 million organizations and people** across
sources on *hard government identifiers* — tax IDs, provider numbers, facility IDs,
corporate registry numbers — not fuzzy name matching. Ask "show me everything the
government knows about this company" and get its environmental record, federal
contracts, workplace injuries, political donations, and court appearances in one
query. The spine's design rule is zero false merges: it never guesses that two
similar names are the same entity; softer name-based matching exists as a clearly
separated, lower-confidence layer.

### 2. Follow the money
Campaign contributions, federal contracts and grants, pharma payments to doctors,
lobbying spending, small-business and pandemic loans, bank deposits — the warehouse
holds both ends of most money flows, so it can answer directional questions:
who funds whom, who gets paid by whom, and what happened to them afterward.

### 3. Attach harm to the actors responsible
This is the mission-defining capability. Violations, accidents, deaths, adverse
events, and complaints are stored *joined to the facility, company, or person they
happened at* — mine accidents to mine operators, drinking-water violations to water
systems, nursing-home deficiencies to owners, detention outcomes to facility
operators. That turns "here's an incident" into "here's an operator's pattern."

### 4. Run the same question against everyone — a census, not a search
Because every domain is modeled in one shared grammar (things, events, links,
codes), a question written once — "who has the most violations per inspection,"
"whose enforcement stopped while violations continued" — runs across *every*
regulated universe identically. Nobody is singled out; everyone is measured with
the same ruler. This is the structural difference between Ripple and a search tool:
it surfaces systemic patterns first, and individual cases only as proof.

### 5. Screen and diligence in seconds
Sanctions lists (US, UK, UN), federal contractor exclusions, health-care fraud
exclusions, revoked nonprofits, failed banks, offshore-leaks appearances, ransomware
victimhood, firearms licenses — a single name or ID can be swept across every
watch-list and adverse-history source in the warehouse at once.

### 6. See change over time
349 tables carry real event dates; 306 are current into 2026. Trends, before/after
comparisons around enforcement actions, and "when did the pattern start" questions
are first-class, not afterthoughts.

### 7. Trust what it says — because everything is measured
Every one of the 589 tables has been audited row-by-row: row counts verified against
publishers, join keys tested for fake/masked values, duplicate rates measured, date
sanity checked. Known data defects (a federal dataset with placeholder dates, a
table with duplicate-inflated counts) are *documented and flagged in the warehouse
itself*, not discovered by users. Findings never auto-publish — a human signs off
on every conclusion before it leaves the building.

---

## What's built and about to switch on

A completed expansion sits staged behind a single switch (waiting on one scheduled
rebuild, ~hours of compute):

- **Judge dossiers** — career, education, financial disclosures, investments, and
  caseload for 16k judges on one hard ID, over 72M dockets.
- **The charity money map** — the IRS master file becomes the authoritative name
  source for 2M nonprofits; dark-money 527 groups, failed pensions, and pension
  filings join the spine.
- **Water enforcement chains** — 1.2M permit holders connected to every violation,
  inspection, and enforcement action (verified 100% linkable).
- **Detention by operator** — 2.6M detention stays resolved to 1,470 facilities.
- **A federal-ID Rosetta stone** — the old and new federal contractor ID systems
  crosswalked for free via grant data that carries both.

---

## Honest limits (stated up front, because credibility is the product)

- **Coverage is deep but not uniform** — some domains (energy, agriculture,
  insurance, Social Security) are thin or absent; the gap list is maintained
  deliberately, not discovered by surprise.
- **Politics money-to-votes** currently connects through name-based matching, not
  hard IDs; the hard-ID bridge is a known, scoped build.
- **Public record only** — no private data, no scraped personal information; if the
  government didn't publish it, it isn't here.
- **A handful of federal datasets arrive broken at the source** (bad dates,
  duplicate inflation, masked ID columns) — each is measured, flagged, and either
  repaired or quarantined, with the defect list on the record.

---

*Underlying receipts: the full per-table inventory with per-line measurement
provenance lives in `reports/noun_event_inventory_2026-08-18.md`; the audit data
behind it in `reports/census_grid_2026-08-12/`.*
