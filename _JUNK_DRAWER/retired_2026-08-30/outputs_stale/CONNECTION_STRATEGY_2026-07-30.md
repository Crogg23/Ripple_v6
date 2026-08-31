# Closing the 112 → 346 Gap: Four Kinds of Connection

Written 2026-07-30. Every number below was verified live this session unless marked
ESTIMATE or NOT YET CHECKED.

---

## The reframe

The gap isn't "we need more ID types." Ripple currently supports exactly **one kind
of connection**: two rows share the same hard ID value. That's `IDENTITY`.

There are four kinds, and three are unbuilt:

| Kind | What it asserts | Built? | Where it belongs |
|------|-----------------|--------|------------------|
| **IDENTITY** | Same ID value = same thing | YES (77 tables) | `ENTITY_INDEX` (the spine) |
| **BRIDGE** | ID system A maps to ID system B | NO | new `ENTITY_XREF` table |
| **HIERARCHY** | This entity is owned/controlled by that one | NO | new `ENTITY_EDGES` table |
| **CO-LOCATION** | Same physical place = probably related | NO | gated, `ENTITY_LINKS` |

Identity is the only one that's zero-false-merge. The other three are *relationships*,
not identities, and must never be merged into the spine's entity clustering — the
existing `spine.py` docstring already makes this argument for NPI↔CCN. They get their
own tables so a query can traverse them explicitly and a reader can see the hop.

---

## TIER 1 — Bridges we already own and have never used

These are the highest-leverage moves in the whole backlog. A bridge is not one more
dataset; it wires two whole *clusters* together in one shot.

### 1.1 `INT_GLEIF_RR` — the global corporate ownership tree (VERIFIED)

963,866 rows. Both endpoints are LEIs, and **LEI is already a spine key with 3.38M
entities**, so this needs zero new key types. Verified relationship counts:

| Relationship | Rows | Distinct children | Distinct parents |
|---|---|---|---|
| IS_ULTIMATELY_CONSOLIDATED_BY | 131,964 | 131,964 | 38,659 |
| IS_DIRECTLY_CONSOLIDATED_BY | 125,781 | 125,781 | 51,663 |
| IS_FUND-MANAGED_BY | 148,280 | 148,280 | 13,295 |
| IS_SUBFUND_OF | 72,583 | 72,583 | 9,204 |
| IS_INTERNATIONAL_BRANCH_OF | 1,940 | 1,940 | 1,434 |
| IS_FEEDER_TO | 1,385 | 1,385 | 991 |

**What it unlocks:** roll any subsidiary up to its ultimate parent. Today a query
about "Acme Chemical LLC" stops at Acme. With this, it continues to whoever
consolidates Acme's financials. This is the corporate veil, and GLEIF is the
*company's own regulatory filing* about who owns it — not an inference.

**Caveat:** GLEIF only covers entities that bothered to get an LEI (financial
counterparties, mostly). It will not cover a small US LLC. Coverage is the limit,
accuracy is not.

### 1.2 `XC_EPA_CORPORATE_CROSSWALK` — polluter to public company (VERIFIED)

5,300,149 rows, one per EPA facility (FRS_ID — already a spine key as of today).
Verified match coverage:

- 73,948 rows carry a `MATCHED_LEI` (1.4% of facilities)
- 22,736 distinct LEIs, 704 distinct `PARENT_CIK`, 31,685 distinct `PARENT_UEI`
- 1,174 distinct `ULTIMATE_PARENT_LEI`
- mean `MATCH_CONFIDENCE` 0.96; `MATCH_METHOD` is `exact` or `fuzzy`
- carries a `REVIEW_FLAG` boolean already

**What it unlocks:** "which publicly traded companies own the facilities with the
most Clean Water Act violations" becomes a join, not a research project. Sample rows
resolve to Phillips 66, Marathon Oil, United Oil — real matches.

**Caveat:** 1.4% coverage. This is a proof the method works, not a finished bridge.
It should be wired as `ENTITY_XREF` rows carrying `MATCH_METHOD` and
`MATCH_CONFIDENCE` so every downstream claim can filter to `exact` only.

### 1.3 Bridges already in the spine but only used as identity

- `FED_CMS_FACILITY_AFFILIATION` (940,350 keyed rows) — NPI↔CCN. Currently both keys
  are indexed separately; the *pairing* between them on the same row is discarded.
  That pairing is the works-at edge.
- `FED_FEC_COMMITTEE_TO_CANDIDATE` — committee↔candidate. Wired today as
  FEC_CMTE_ID identity only; the candidate on the same row is deliberately rejected
  as an extra_key (correctly — different entity type). That rejection is exactly the
  signal that it's an EDGE.
- `FED_SEC_EDGAR_COMPANY_TICKERS` — CIK↔ticker symbol.
- `INTL_GLEIF_RELATIONSHIPS` (481,900 rows) — NOT YET INSPECTED, likely overlaps 1.1.

---

## TIER 2 — New identity axes that are clean and verified

| Key | Tables waiting | Verified? | Notes |
|---|---|---|---|
| **NPDES_ID** | 7 | YES — 44,867 distinct, 9-char, **0 blanks** in PS_VIOLATIONS | EPA water discharge permits. `FED_EPA_NPDES_ICIS_FACILITIES` is 500K rows, **100% unique**, with full address + lat/long |
| **CompanyNumber** (UK) | 1 | YES — 5,734,779 distinct / 5,734,780 rows | UK Companies House. Near-perfect key |
| **COMPANY_NUM** (IE) | 1 | YES — 818,929 distinct, 0 blanks | Irish CRO |
| **CU_NUMBER** | 1 | YES — 6,366 distinct, 0 blanks | Credit union charters. NOTE: this table's `EIN` column is DEAD (1 distinct) |
| **FRN** + `CALL_SIGN` | 1 | YES — 1.2M FRN / 1.6M call signs (254K FRN blank) | FCC licensees. `EIN` here is also DEAD |
| **MODE_S_CODE_HEX** | 1 | YES — 314K distinct, 100% unique | FAA aircraft registry. **`N_NUMBER` is 100% blank** — do not key on it |
| **OpenSanctions `ID`** | 1 | YES — 71K, 100% unique | Has an `IDENTIFIERS` field that may carry passport/tax IDs — worth parsing |
| **NDC** | 3 | NOT YET VERIFIED | Appears in CMS_OPEN_PAYMENTS (×3 years), DEA_ARCOS_FULL (`NDC_NO`), CMS_NADAC |
| **ACTIVITY_ID** | 8 | NOT YET VERIFIED | EPA ICIS. Likely an event ID not an entity ID — check before wiring |
| **CUSIP / FIGI** | 4 | n/a | Securities. Per the 2026-07-30 call these are NOT entities; wire as edges off CIK |

### Why NDC is more interesting than its row count suggests
NDC is a *drug* identifier that appears in three otherwise-unconnected places: who a
manufacturer paid (Open Payments), what physically shipped and where (ARCOS), and what
it cost (NADAC). Wiring it makes one query out of "which company paid which doctors
about drug X, and where did drug X actually ship." That is the opioid accountability
question. A drug is not a person, so it's a `product` entity type or an edge — a taste
call for Chris, flagged not decided.

---

## TIER 3 — The two genuinely novel structural ideas

### 3.1 Address as a node, with mandatory fan-out suppression

**745 landing tables have an address column. 412 have lat/long.** That's the single
largest untapped connector in the warehouse, and it's currently worth nothing because
address isn't a node type.

The idea: normalize address → canonical form (or geocode → snap to a grid cell), and
treat the result as a `place` node. Two facilities at one address are related.

**Why this is defensible and not junk:** shell-company networks are *found* this way.
A registered-agent address hosting 4,000 LLCs, a single suite number that is the
"headquarters" of 60 nursing homes — that pattern IS the finding.

**Why it needs a hard guard:** that same property makes it dangerous. CT Corporation's
address would fuse thousands of unrelated companies into one blob. The rule must be:
compute fan-out per normalized address, and **discard any address above a threshold**.
`discover.py` already has exactly this concept (`--fanout-max`, default 40) for
crosswalk values — the same logic, same argument, new domain. High fan-out isn't
noise to be tolerated; it's a *different* finding (a registered-agent hub) and should
be recorded separately, not merged.

**Where it lives:** never the spine. Co-location is not identity. It's a gated link.

### 3.2 County (FIPS) as a jurisdiction entity — the harm map layer

A large block of datasets have *no* entity ID and never will, because they're
aggregate statistics: BLS QCEW employment (4,429 FIPS), VERA incarceration (3,075
counties), CDC overdose, CDC drug poisoning, CDC injury/violence, IRS SOI income by
ZIP, FHFA house prices, NOAA storm events.

Today these are dead weight. But a county is a legitimate entity — it's a
*jurisdiction*, and the constitution's question is "who gets hurt." Counties are
where the answer lives.

Wiring FIPS as a `jurisdiction` node turns that dead block into a denominator layer:
opioid shipments per capita per county (ARCOS already in spine + QCEW population),
incarceration rate vs. income (VERA + IRS SOI), overdose deaths vs. treatment
facility density (CDC + the CMS/NPI facility cluster).

**This is the layer that makes harm measurable rather than anecdotal.** A finding
that says "this county has 3x the opioid shipments per resident of its neighbors" is
a mechanism claim with a population attached.

**Caveat:** FIPS joins are geographic, not identity. County boundaries change (rarely)
and there are FIPS-vs-GEOID format inconsistencies across agencies (`GEOID`,
`ST_GEOID`, `COUNTY_FIPS`, `AREA_FIPS`, `STATE_FIPS`+`CZ_FIPS` all appeared in the
audit). Needs one normalizer, same discipline as `keys.py`.

---

## TIER 4 — External data you do NOT have that would bridge what you DO have

Ranked by leverage. All are free and public unless noted. **None of these were checked
for existence in your warehouse this session — treat as "go get it," not "you have it."**

### Highest leverage

1. **SEC EDGAR Exhibit 21 (Subsidiaries of the Registrant).** Every 10-K filing
   includes an EX-21 listing every subsidiary by name and state. This is the US
   corporate family tree in the companies' own words. You already have CIK as a spine
   key and already have EDGAR financials. This is the single best fix for GLEIF's
   coverage gap: GLEIF covers financial entities, EX-21 covers *operating*
   subsidiaries — the LLCs that actually own the factories and the nursing homes.
   Free, bulk-downloadable.

2. **CMS ownership files — nursing home, hospice, home health, hospital.** CMS
   publishes actual ownership: owner name, owner type (individual vs. organization),
   ownership percentage, role, and association date, keyed to **CCN** which is already
   a spine key. This is the private-equity-in-healthcare mechanism, and it is handed
   to you pre-joined. If you take one thing from this list, take this one.

3. **IRS Form 990 Schedule R (Related Organizations).** You already have 990s. Schedule
   R is the nonprofit family tree — which nonprofits control which other nonprofits and
   which taxable subsidiaries. Keyed on EIN, already a spine key. Turns 4.16M EIN
   entities into a hierarchy.

4. **IRS Form 990 Part VII / Schedule J (officers and compensation).** Named humans
   with titles and dollar amounts, keyed to the org's EIN. This is your best source of
   *person* nodes attached to organizations. Person-name matching is fuzzy, so it goes
   through the gated resolver — but the name↔EIN pairing itself is a hard fact from a
   filing.

5. **EPA ECHO program-ID crosswalk files.** EPA publishes the mapping between FRS_ID
   and every program ID (NPDES_ID, RCRA handler ID, TRI facility ID, air permit ID).
   You have FRS_ID in the spine as of today and NPDES_ID waiting in 7 tables. This
   crosswalk is the bridge between them, published by the agency, no fuzzy matching
   required.

### High leverage

6. **State business registries (or OpenCorporates as an aggregator).** The LLC layer.
   Most polluting facilities and most healthcare operators are LLCs with no LEI and no
   CIK. This is the biggest structural hole in your entity coverage. Individual state
   registries are free but 50 different formats; OpenCorporates aggregates them but
   bulk access is **paid** — that's a spending decision, RED lane.

7. **CourtListener docket *parties* and *attorneys* endpoints.** You already have
   71.7M CourtListener dockets — but the audit shows your table has `CASE_NAME` and
   `DOCKET_NUMBER` and no party rows. The parties are a separate endpoint. Docket
   parties name defendants, which lets litigation attach to entities. Right now your
   biggest table by row count is nearly inert for connection purposes.

8. **FDA FEI (Facility Establishment Identifier) / Drug Establishment Registration.**
   The physical plant that manufactured a drug. Bridges NDC → a facility → an address
   → (via 3.1) a corporate owner. Completes the drug supply chain from plant to
   prescriber.

9. **NPPES authorized-official fields.** You already have NPPES (9.6M providers, your
   biggest spine table). Its authorized-official name/title fields are *person* data
   attached to organizational NPIs — a free person layer you're likely already storing
   and not using. NOT CHECKED this session; verify before believing it.

10. **HUD multifamily / LIHTC property and owner files.** Federally subsidized housing
    with owner and management-agent names. The housing-harm equivalent of the CMS
    ownership files.

### Worth knowing about

11. **USPTO patent assignment data** — who actually owns which IP after transfers.
    Reveals corporate relationships that don't appear in ownership filings.
12. **Medicare cost reports (HCRIS)** — you already have this in the spine. It contains
    home-office / chain-affiliation fields that are effectively ownership data. NOT
    VERIFIED; worth a look before buying anything external.
13. **Registered-agent datasets** — needed to *suppress* the false positives in idea
    3.1 rather than to create links.
14. **FEC candidate-committee linkage file** — you have FEC committees and candidates
    as separate entity types now; FEC publishes the official linkage.

---

## What I'd do first, and why

1. **`INT_GLEIF_RR`** — highest leverage per unit of work in the entire backlog. Zero
   new key types, both ends already in the spine, 963K rows of companies' own
   statements about who owns them. This is a new *table*, not a new axis.
2. **CMS ownership files** (external, free) — keyed on CCN which is already wired.
   Directly serves the mission question with almost no engineering.
3. **NPDES_ID + the EPA crosswalk** — one verified axis (44,867 clean IDs) plus the
   agency-published bridge to FRS_ID, which turns the water-permit cluster and the
   facility cluster into one graph.
4. **FIPS as jurisdiction** — cheapest way to make ~20 currently-dead aggregate
   datasets useful, and it's the layer that turns findings into rates.
5. **990 Schedule R** (external, free) — hierarchy for the 4.16M EIN entities.

Address-as-a-node (3.1) is the most powerful idea here and the most dangerous. It
should come *after* there's a registered-agent suppression list, not before.

---

## Decisions that are Chris's, not mine

- Whether a **drug (NDC)** is an entity type or only an edge.
- Whether a **county (FIPS)** becomes a spine-native `jurisdiction` entity — that
  changes what the spine *is* from "things that can be held accountable" to "things
  plus places."
- Whether to **pay for OpenCorporates** or grind 50 state registries.
- Whether **fuzzy corporate name matching** (the `MATCH_METHOD='fuzzy'` rows in the EPA
  crosswalk, and any name-based bridge) may ever back a published finding, or only
  ever route to human review.
