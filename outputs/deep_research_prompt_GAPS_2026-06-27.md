# Deep-Research Prompt — Ripple Library GAP sources (29 issues)
*Paste into claude.ai with Research / extended thinking ON. Self-contained — assumes no prior context.*

---

You are a senior data sourcing researcher helping me build **"the Library"** — a Snowflake data
warehouse that ingests public datasets across any domain for accountability journalism and data-driven
investigation. I onboard each source with a Python pipeline: fetch → land raw in Snowflake (every column
as TEXT) → transform in dbt. **I do not need analysis or commentary on the issues themselves — I need
the best *datasets*.**

## What "onboardable" means (rank by this)
Strongly prefer sources that are:
- **Open + structured** — bulk CSV/ZIP download, or a clean REST/JSON or SDMX API
- **Keyless or free-API-key** (a free registration key is fine; paywalls/subscriptions are not)
- **Permissively licensed** (public domain, CC-BY, or clearly redistributable)

Avoid / flag as last-resort: scrape-only sites, login-walled or paid data, PDF-only reports with no
underlying data file, and aggregator mega-portals (don't tell me "data.gov" — name the *specific dataset*).

## The task
For **each of the 29 issues below**, find the **single best onboardable dataset** (plus up to 2 backups).
**If no clean structured dataset exists** for an issue — common for live foreign-conflict casualties —
say so plainly and name the best **proxy** (e.g. an event database, an index, a survey, displacement data).

Do not recommend any source that is already obviously core US infrastructure I'd already have (see
"already covered — skip" list at the bottom). Focus on **net-new, canonical, specific** datasets.

## For every dataset you recommend, give me exactly these fields
1. **Dataset name** + **publisher/keeper**
2. **Canonical URL** — the actual data/download/API page (not a homepage)
3. **Access method** — bulk download | REST API | SDMX API | free-API-key REST | scrape | scrape (JS)
4. **Format** — CSV / JSON / XML / XLSX / ZIP / GeoJSON / SDMX / Parquet
5. **Auth & cost** — none / free key / paid
6. **Update cadence** — how often it refreshes
7. **Approx volume** — rows or file size, ballpark
8. **License** — exact terms if you can find them
9. **Join keys / identifiers it carries** — ISO country code, FIPS, lat/lon, EIN, CIK, date, etc. (what it
   can be linked to other data on)
10. **Unit of observation** — one row = one *what*?
11. **Onboardability** — EASY / MEDIUM / HARD, one-line why
12. **Known quirks/gotchas** — schema instability, rate limits, registration friction, coverage gaps
13. **Relevance** — one line: how it actually measures this issue

Cite your sources. Output as a per-issue block or a wide table — your call, but keep all 13 fields.

---

## The 29 issues (with the angle that matters)

**Foreign conflict & security** (expect proxies, not casualty feeds)
1. **Sudan's civil war** — Darfur atrocities, displacement, famine
2. **Russia–NATO hybrid war** — sabotage / cyber / infrastructure incidents across Europe
3. **Iran & nuclear proliferation** — enrichment levels, IAEA stockpile/inspection data, facilities
4. **North Korea** — missile/nuclear test events, sanctions activity
5. **Myanmar civil war** — conflict events + displacement
6. **West Africa / Sahel instability** — jihadist violence, coups (Mali/Burkina/Niger)
7. **Pakistan's instability** — economic crisis + political violence
8. **Ethiopia & Horn of Africa** — conflict + GERD/Nile water tension
9. **Venezuela's collapse** — migration outflows, economic/oil data
10. **Lebanon's collapse** — currency/economy, Syrian refugee load

**Global structural**
11. **Wealth & income inequality** — distribution by percentile (World Inequality Database, etc.)
12. **AI economic bubble** — data-center capex, AI infrastructure investment, chip/compute buildout
13. **Antimicrobial resistance (AMR)** — resistance rates, surveillance (WHO GLASS, CDC, ECDC)
14. **AI governance gap** — AI incidents, autonomous-weapons use, national AI policy/regulation trackers
15. **Disinformation & AI propaganda** — documented influence operations, platform takedown datasets
16. **Cybersecurity attacks on critical infrastructure** — known-exploited vulns, breach disclosures, ransomware incidents
17. **Tech monopoly / digital power concentration** — antitrust actions, market-share/concentration, platform dominance
18. **Rise of extremism / terrorism** — terror/political-violence events, hate-crime data
19. **Human trafficking & modern slavery** — prevalence estimates, trafficking cases/victims
20. **Child welfare in conflict zones** — grave violations against children, child malnutrition/mortality in crises

**US social & culture-war**
21. **Abortion access** — abortion counts/rates by state post-Dobbs, travel for care, clinic counts
22. **LGBTQ+ rights rollback** — state legislation targeting LGBTQ+ people (bill trackers, policy tallies)
23. **Trans rights** — anti-trans / gender-affirming-care legislation; trans health/outcomes
24. **Childcare desert & paid leave** — childcare cost/supply/deserts; paid-leave coverage
25. **Veteran care & military suicide** — veteran suicide rates, VA healthcare access/quality
26. **Military recruitment crisis** — service-by-service recruiting vs. goals, youth eligibility/propensity
27. **First Amendment / book bans** — school/library book challenges & bans; campus speech incidents
28. **Federal vs. state power friction** — interstate legal conflict, state-law divergence (cannabis, abortion, guns)
29. **(spare slot — if you find a clearly better dataset for any above, surface it as an alternate)**

---

## Already covered — skip (don't re-recommend these or close substitutes)
US healthcare providers (CMS/NPPES/HCRIS), Medicare Part D, SEC EDGAR, FEC campaign finance, FARA,
USAspending federal contracts, OFAC/OpenSanctions, Federal Register, Supreme Court (SCDB/Oyez),
NOAA AIS, EPA ECHO, IRS nonprofit revocations, redlining (Mapping Inequality), Treasury debt, FDIC.

For these themes I **already have or have queued** the canonical source, so only mention them if you've
found something materially better: ATF firearms, DEA ARCOS, BOP, BJS, FBI crime data, CBP/ICE/EOIR
immigration, EAC/MIT election returns, HMDA, EEOC, NCES education, HUD housing, EIA energy, USDA ag,
SSA/PBGC, USGS water, V-Dem/Freedom House, UN Comtrade/IMF/Eurostat, UNHCR, FAOSTAT, GBIF, IPC.

**Goal: net-new, specific, onboardable datasets for the 29 gaps above — or an honest "no clean dataset, here's the proxy."**
