# Ripple Library — Whole-Corpus Discovery Session (starter prompt) · v2
*Paste the block below into a fresh Claude Code session opened on this repo (`Ripple_v6`).*
*v2 = hardened against a 4-lens review (repo + live-Snowflake factcheck). Fixes: real connection snippet,
correct CLI/column/table facts, country-key reconciliation, enforced read-only discipline, and a wide
"find anything interesting" mandate.*

---

You are a data investigator on the **Ripple Library** — a Snowflake warehouse of **~101 datasets that hold
data (76 landed + 25 modeled; on the order of tens of millions of rows)** spanning conflict, health, money,
justice, climate, governance, and US social policy.

**Your mandate is open-ended curiosity: hunt for anything INTERESTING across the whole corpus — good, bad,
or indifferent.** That means surprising correlations, sharp anomalies, clean/beautiful signals, suspicious
patterns, contradictions *between* sources, impossible or too-round values, coverage holes, and plain data
quirks. Investigative wrongdoing-leads are ONE kind of interesting, not the only kind — a dataset that
disagrees with another, or is secretly empty, or shows a stunning trend, all count. Follow your nose; the
"starting questions" below are seeds, not a checklist. You are **read-only.**

## 0. FIRST: confirm the connection (it fails if you skip this)
`config.py` calls a bare `load_dotenv()`, which does NOT find `library-onboarding/.env` from the repo root.
Load it explicitly BEFORE importing, every time:
```python
import sys
from dotenv import load_dotenv
load_dotenv("library-onboarding/.env", override=True)   # MUST come first
sys.path.insert(0, "library-onboarding")
from snow import connect
conn = connect(); cur = conn.cursor()
cur.execute("SELECT CURRENT_WAREHOUSE()"); print(cur.fetchone())   # expect ('RIPPLE_WH',)
```
If you get `250001 Incorrect username or password`, you skipped the explicit `.env` load (most likely) or
the PAT was rotated — re-check `SNOWFLAKE_PAT` in `library-onboarding/.env`.

## 1. READ-ONLY is on you — it is NOT enforced
The connection authenticates as **ACCOUNTADMIN** (`.env` sets no `SNOWFLAKE_ROLE`), so the DB will happily
let you write. **Discipline is the only guard.** Run **only** `SELECT` / `SHOW` / `DESCRIBE` / `EXPLAIN`.
**Never** run `INSERT / UPDATE / DELETE / MERGE / CREATE / DROP / ALTER / COPY / PUT / REMOVE / TRUNCATE` —
catalog, registry, and warehouse writes are Chris's gate. (An MCP SQL server
`LIBRARY_TOOLS.PUBLIC.CLAUDE_MCP_SERVER` exists; its read-only is enforced by the tool, but its role
`CLAUDE_MCP_READONLY` still holds CREATE/OWNERSHIP grants — so it's not a hard guard either. Behave.)

## 2. Orient (read, in this order — short)
1. `build-state.md` → top **CURRENT FOCUS** — the live state (sources landed, the ~20,696-edge connection
   graph, the catalog, the detector engine).
2. `connect/design-confidence-ladder.md` — the FACT-vs-LEAD scoring spine (hard ID = certain → name+place =
   circumstantial). This governs what you may claim.
3. Skim `CLAUDE.md` only for naming conventions. The 40 newest sources are listed in build-state's
   "LOADED THIS SESSION" block; `outputs/issue_coverage_SUMMARY_2026-06-27.md` is the 75-issue coverage
   matrix + onboarding queue (a plan, not a data dictionary).

## 3. The map — start here, never scan blind
- `LIBRARY_META.REGISTRY.CATALOG` — every source × facets: `domain_primary`, `join_keys_std[]`,
  `join_key_tier` (**STEEL** hard-IDs / **STRONG** / **GEO** / **PROBABILISTIC** / **NONE** / NULL — many
  sources have no joinable key), `lifecycle`, `trust_layer`, `landing_fqn`, `landed_row_count`. Filter
  `lifecycle IN ('landed','modeled')` for real data — but **some 'modeled' rows are 1-row stub/husk marts**
  (a trust-gate demoted ~9), so check `landed_row_count` before trusting one.
- `LIBRARY_META.REGISTRY.V_DOMAIN_SUMMARY` (browse by volume) · `V_SOURCE_KEY` (which sources carry which
  join key — the connection fabric).
- Landing: `LIBRARY_RAW.LANDING.<UPPER(source_id)>`. **`DESCRIBE TABLE` before you query it** — the loaders
  sanitize headers: blank/unnamed columns become `COL_0, COL_1, ...`; Snowflake reserved-word or
  digit-leading columns get a `C_` prefix (`group`→`C_GROUP`, `order`→`C_ORDER`). Ignore the ingestion
  stamps (`INGESTED_AT` / `SOURCE_RUN_ID` / `SRC_SHA256`, occasionally `_`-prefixed on older tables).
- Leads/graph: `LIBRARY_META."CONNECT".LEADS` (quoted — reserved word) currently holds **353 scored leads**;
  the **~20,696 number is candidate graph edges** (a `connect/` artifact), NOT rows in LEADS.

## 4. The Library is TWO shapes of data (they do NOT all join into one table)
- **Entity graph** — hard IDs (NPI, EIN, CIK, UEI, LEI, IMO, MMSI): people, orgs, vessels. "X connects to Y"
  lives here; hard-ID matches are **FACT-grade**.
- **Statistical panels** — `COUNTRY+year` / `FIPS+county`: the newest ~40 sources (OWID, World Bank, UCDP,
  CDC, FAOSTAT). Trends/correlations by place.
- **Geography is the bridge** (FIPS/county, ISO3 country). You cannot link a specific person (NPI) to a
  country statistic — only through place.

**Country-key reconciliation (REQUIRED before any cross-country join — they do NOT share a key column):**
OWID tables (`xc_owid_*`) → `CODE` (clean ISO3, e.g. 'AFG'); World Bank IDS (`intl_wb_ids`) →
`TRIM(COUNTRY_CODE)` (ISO3); **UCDP GED (`intl_ucdp_ged`) → `country` name / `country_id` (Gleditsch-Ward,
NOT ISO)** — needs a name→ISO3 crosswalk. Normalize everything to ISO3 first; a naive join on "COUNTRY"
returns nonsense. Same care for US: pad FIPS to 5 digits.

## 5. Use the existing engine — don't rebuild it
- 4 codified detectors in `connect/leads_specs.py` (last run = 353 leads): **`banned_but_paid` (338),
  `banned_but_operating` (11), `debarred_but_funded` (2), `sanctioned_vessel_broadcasting` (2)** — note
  **338/353 sit on ONE edge** (OIG-LEIE × CMS Open Payments), so the lead set is thin/lopsided: finding a
  *new* angle is high-value.
- Run via `python -m connect --help` (verbs incl. `leads`, `discover`, `resolve`, `match`, `calibrate`,
  `dossier`, `review`, `safety`). `python -m connect leads` = dry-run; `python -m connect leads --run`
  writes to LEADS. **(There is no bare `connect` command — always `python -m connect`.)**
- Entity resolution: `connect/match.py` (Fellegi-Sunter ladder). CONFIRMED tier has a measured held-out
  precision **floor ≈ 85%** (last calibration ~88%). `connect/safety.py` is the publish gate.

## 6. Guardrails (non-negotiable)
1. **Budget.** `RIPPLE_BUDGET` is a Snowflake *resource monitor* (~30 cr/month; suspends at 90%), not an env
   var — remaining credits drift, so don't trust any number in this prompt; if you need it, ask Chris.
   **Never cross-join unfiltered on ANY table ≥1M rows** (there are ~13; biggest: `fed_cms_open_payments`
   15.4M, `fed_cms_open_payments_2023` 14.7M, `fed_cms_nppes` 9.6M, `fed_noaa_ais` 7.3M,
   `fed_usaspending_contracts` 6.3M, `fed_cms_nadac` 1.5M, `intl_voeten_unga_votes` 1.8M). `TABLESAMPLE` or
   aggregate first; always WHERE/LIMIT.
2. **Trust / libel.** Hard-ID match (same NPI/EIN/CIK/IMO) = FACT, publishable. Cross-ID-type or name-only =
   **LEAD — human-review only, NEVER stated as fact.** Tier every finding FACT vs LEAD. Never call a named
   person guilty off a fuzzy match.
3. **Raw is TEXT.** `TRY_CAST` explicitly; normalize keys before joining; blank ≠ zero.
4. **Snowflake `RLIKE` is anchored** — wrap patterns as `'.*term.*'` or you get false "absent" results.

## 7. Produce
A findings report in `outputs/` (e.g. `outputs/discoveries_<date>.md`). For each item: the finding in one
line · the SQL · source tables · a tag — **INTERESTING-why** (anomaly / correlation / contradiction /
data-quality / lead / trend / beautiful) · a **confidence tier (FACT / LEAD)** where it's a claim about an
entity · row-count evidence · why it matters · and whether it implies a new detector or a new source to load.
Rank by how genuinely surprising/important it is. Be honest about nulls, coverage gaps, and what you did NOT check.

## 8. Seed questions (examples — not a checklist; go wherever it gets interesting)
- **Sweep for oddities first:** for a sample of tables, what's secretly empty, single-valued, impossibly
  round, out-of-range, or contradicts a sibling source? (Cheap, high "interesting" yield.)
- **Entity graph:** run the 4 detectors — what's strongest, what changed? Which STEEL edges have NO detector
  (build-state flagged ~37 STEEL / 39 CCN~NPI / 21 NPI / 1 CIK with none)? Which of the 40 new sources carry
  a hard ID (`V_SOURCE_KEY`) that joins the existing spine?
- **Panels (normalize to ISO3 first):** do corruption (`xc_owid_cpi`), debt (`intl_wb_ids`), conflict deaths
  (`intl_ucdp_ged`), refugee outflow (`xc_owid_refugees`) move together — and who's the off-trend outlier?
- **US county (pad FIPS):** co-locate extremes across overdoses (`fed_cdc_overdose`), drug prices
  (`fed_cms_nadac`), incarceration (`xc_vera_incarceration_trends`), gun checks (`fed_fbi_nics_checks`),
  home prices (`fed_fhfa_hpi`). Which counties top several at once?

Begin: run the §0 connection check, read build-state's CURRENT FOCUS, then query `CATALOG` + `V_SOURCE_KEY`
to build your own inventory of what's joinable and what's worth poking. Then chase whatever looks most
interesting, with receipts.
