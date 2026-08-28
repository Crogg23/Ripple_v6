# Big-Win Pull Sweep — 2026-08-27

One last "what should we still pull before the connections phase" sweep, run on
Chris's ask. Two agents: (1) internal — every gap ledger, ranking doc, audit CSV,
and key registry in the repo; (2) external — live web verification of bulk
public datasets not yet held. Warehouse was unreachable this session (PAT
rejected), so internal row counts come from `reports/the_audit_2026-08-26/`
CSVs, not live queries.

## Headline correction

"Depth is basically solved" (this morning's brief) was WRONG in one specific
way: the depth triage only ranked tables whose row counts ended on suspiciously
round numbers. Truncations that stopped on non-round numbers were invisible to
it. The two biggest misses:

- **DOL Form 5500**: `FED_DOL_FORM5500` = 33,484 rows vs ~1M filings/yr
  published (2009–2024 → 2–3M+). A 70–90× truncation on EIN — the single
  most-connected key in the warehouse (73 landing tables). `SPONS_DFE_PN`
  verified 100% filled (EIN+PN plan key); `FED_PBGC_TRUSTEED_PLANS` (5,176)
  already waits for this join.
- **FDA MAUDE**: `FED_FDA_MAUDE` = 1,386 rows vs ~20M device adverse-event
  reports. FAERS sibling loaded fine (20.9M) — loader pattern exists.
  Pull with **GUDID** (`FED_FDA_GUDID` = 2,542 vs ~5M devices) or injuries
  can't resolve to manufacturers.

Also: `FED_USASPENDING_CONTRACTS_FULL_R2` loader is **stalled at 75.7%**
(dead since 2026-08-23, per `reports/gap_audit_2026-08-25.md`) — resuming is
nearly free and wasn't on any triage list.

## Zero-cost item (no pull at all) — highest value-per-hour

Five key finds live-verified on 2026-08-05 were never wired into
`connect/keys.py` (grep-confirmed absent): MSHA `CURRENT_CONTROLLER_ID` /
`CONTROLLER_ID` (98.9%/93.2% filled, 41,050 distinct controllers —
mine-ownership roll-ups; quote-wrap trap applies), `FED_DOL_OFLC.CASE_NUMBER`,
`SPONS_DFE_PN`, the NDC family, the EPA_CASE_NO family. CUSIP also absent.
Wiring these is registry work, not acquisition.

## Ranked pull list (internal + external merged)

### Tier A — do before/alongside the connections dig (cheap, direct graph fuel)
1. **HHS OIG LEIE exclusions** (external) — ~80k rows, joins NPI, ~1 hr, $0.
   The literal "banned but still operating" table. oig.hhs.gov, verified live.
2. **Form 5500 full history** (internal #1 above) — EIN graph fuel, ~2–3M
   filings + schedules.
3. **MAUDE + GUDID + the FDA device/recall stub cluster** —
   `FED_FDA_ESTABLISHMENT_REG` 166, `510K` 88, `PMA` 29, `DEVICE_ENFORCEMENT`
   20, `DRUG_ENFORCEMENT` 1, `CAERS` 1. One openFDA loader family, Phase 3 of
   the 08-05 master plan, never finished.
4. **FDA NDC Directory** (tiny) + wire NDC into keys — legalizes the verified
   ARCOS (178.6M) ↔ NADAC (1.5M) ↔ Open Payments (15.4M) drug chain.
5. **CUSIP↔issuer bridge** (SEC fails-to-deliver or N-PORT, one free file) —
   unlocks 101.3M rows of 13F holdings to CIK/ticker.
6. **Resume the stalled contracts R2 loader** (75.7% → done).
7. **USAspending subawards** — already priced ($5–15), needs a year-range call.

### Tier B — big new harm layers (days each, $5–40)
8. **CMS Medicare utilization + Part D prescribers** (external) — NPI-keyed,
   ~10M + ~25M rows/yr × ~10 yrs; the "what providers actually DO" layer;
   triangulates Open Payments/FAERS/LEIE.
9. **IRS 990 full e-file XML** — EIN-keyed return content incl. Schedule I
   grants = new EIN→EIN money edge. ~100+ GB XML, parsers exist.
10. **EOIR immigration court FOIA dump** — ~30 GB / up to 169M rows; judge-level
    asylum-denial disparities; dirty formats are the known cost.
11. **FMCSA carrier census + inspections + crashes** — new USDOT key; fatal-
    crash carriers still operating; chameleon carriers.
12. **FFIEC bank call reports** — RSSD/FDIC-cert keyed, quarterly to 2001.
13. **NHTSA complaints/recalls/investigations + FARS** — ~2M complaints,
    defect-death timelines; few GB.
14. **SBA PPP full loan file** — 11.5M rows, name@zip tier, half a day.
15. **PatentsView (USPTO)** — PATENT is a declared STEEL family with zero
    authoritative side (only portal scrapes carry it); ~9M patents/8M
    assignees, free bulk.

### Tier C — scope calls / flagged, not loads
- **DEA registrant file** (would name all 148,588 ARCOS buyers) — NTIS **paid**
  product; collides with clean-public-source policy. Chris call. Fallback:
  Part D prescribers + state licence rosters.
- **WaPo ARCOS raw** (if ever wanted beyond held ARCOS_FULL) — journalism-terms
  release, ends 2014.
- **HMDA year-range**, **EDGAR full**, **GDELT scope**, **HIFLD layer pick**,
  **Envirofacts program pick** — all still open scope statements.
- **Whole-domain zeros confirmed live**: FERC (0), NRC nuclear (0), PHMSA
  (2,039-row stub vs ~800k hazmat incidents — cheap, East-Palestine-class),
  FSIS/APHIS (0 — FSIS establishment number ties plant contamination to OSHA's
  5.6M rows), NAIC/HIOS insurance (0), SSA / Death Master File (0 — restricted
  access, scope call). NOTE: energy-is-absent from the 08-05 sweep is stale —
  EIA is well-landed (89 tables).
- **Never-built A/B-tier list** (zero rows, previously ranked): NLRB cases,
  USSC sentencing datafiles, Superfund SEMS (only boundaries held), 340B
  OPAIS, FCC Political File, CAMPD, ASC appraiser registry, BJS PREA audits,
  Ginnie Mae issuers, USGS NWIS. VAERS still CAPTCHA-blocked — needs a mirror.
- **Federal Audit Clearinghouse**: `FED_FAC_SINGLE_AUDIT` (411,638) may already
  cover the external find — verify before pulling.

### Stub family (≤3-row tables, logged as an open defect since 07-12, now named)
`FED_FINCEN_BOI` 1, `FED_FRA_SAFETY` 1, `FED_CMS_HPT_MRF` 1,
`FED_DOJ_CRT_CASES` 1, `FED_ED_FSA_DATACENTER` 1, `FED_FDA_CAERS` 1,
`FED_CBP_ENCOUNTERS` 9, `FED_FDIC_ENFORCEMENT` 14, `FED_FARA` 30 (verified
FARA registration key), `FED_HUD_DATA` 77, `FED_GRANTS_GOV` 100,
`FED_IRS_990` 200, `FED_COURTLISTENER_CITATION_MAP` 0.

### Verify-then-retire
- `fed_atf_ffl_locations` "gap" is stale — `FED_ATF_FFL` already holds 77,514.
- CMS Open Payments re-pull remains queued (STATUS "your move").

## External also-considered (weaker): CPSC NEISS (no company key), Eviction Lab
(aggregates only), EEOC (no case-level bulk), EIA/FERC bulk (future domain),
FAA registry, 50-state corporate registries (a project, not a load), state
Medicaid exclusions (LEIE gets 80% for 1% effort), PACER alternatives (already
have CourtListener/RECAP), USDA subsidies (raw FOIA patchy).

All external items live-verified for bulk access 2026-08-27. Internal row
counts are from the 08-26 audit CSVs (post-fix), not re-queried live.

---

# CERTIFICATION SWEEP RESULTS (2026-08-27, all 221 sub-5k non-portal landing tables, live counts + publisher web verification)

Method: live row counts pulled 2026-08-27 via the guarded read lane; 4 agents
verified each table against its publisher's actual dataset size (web-checked,
sourced). Full per-table verdict lines with URLs are in the four agent
transcripts; headline ledger below.

**Totals: ~110 COMPLETE · ~88 SLICE · ~24 UNKNOWN** (a few duplicates counted
per copy — 3× UN sanctions, 3× Prop 65, 3× FHFA suspended counterparties,
2× JPML, 2× EIA balancing authority, 2× CourtListener courts).

## NEW confirmed slices worth pulling (beyond the earlier ledger)

| table | held | publisher real | ratio |
|---|---|---|---|
| FED_COURTLISTENER_CITATION_MAP | 0 | ~18.1M citations | ∞ — empty table, free bulk |
| FED_IRS_SOI_CHARITIES | 2,450 | ~300k/yr full SOI extract | ~120x |
| FED_VOTEVIEW_ROLLCALL_META | 3,364 | ~111k rollcalls 1789– | ~33x |
| INTL_HUDOC | 2,000 (cap) | ~28k ECHR judgments | ~14x |
| FED_CFTC_COT_FINANCIAL_HIST | 4,615 | ~40k+ weekly rows since 2006 | ~9x |
| FED_FAA_ADIP_PRIVATE_AIRPORTS | 3,589 | 14,336 private-use | ~4x |
| FED_FRA_SAFETY | 1 | hundreds of thousands since 1975 | stub |
| FED_HHS_TAGGS | 45 | 500k+ HHS grant awards 1995– | stub |
| FED_USITC_DATAWEB | 7 | tens of millions of trade rows | stub |
| FED_FDA_DRUG_ENFORCEMENT | 1 | ~26k+ drug recalls | stub |
| FED_FDA_DEVICE_CLASSIFICATION | 1 | 7,075 product codes | stub |
| FED_FDA_CAERS | 1 | ~90k+ food/supplement AEs | stub |
| FED_CBP_ENCOUNTERS | 9 | ~60k+ published rows | stub |
| FED_FDIC_ENFORCEMENT | 14 | thousands of orders | stub |
| FED_NCUA_CHARTER_MERGER_EVENTS | 27 | thousands historic | stub |
| FED_OCC_NATIONAL_BANKS_BY_NAME | 62 | ~750–1,000 | ~14x |
| FED_DOJ_FCA_SETTLEMENTS | 19 | hundreds/yr | stub |
| INTL_CH_ZEFIX | 18 | ~700k Swiss entities | huge |
| INTL_GR_GEMI | 40 | ~1M Greek entities | huge |
| INTL_ES_BORME | 25 | ~18.6M Spanish corporate acts | huge |
| INTL_AUSTLII | 1 | ~1.5M cases | huge |
| CA_LOBBY_* family | 170–1,730 | thousands per session (Cal-Access) | ~2–20x |
| FED_GLOBAL_WITNESS defenders | 232 | ~2,253 killings 2012–24 | ~10x |
| FED_WPA_SLAVE_NARRATIVES / DOCSOUTH | 100/144 | 2,300 / 344 | small culture |
| FED_DOJ_EPSTEIN_LIBRARY | 777 | now 3.5M pages | ≥15x |

Confirmed dupes-of-already-held-bulk (retire the stub, no pull needed):
FED_ATF_FFL_LOCATIONS (2,000; FED_ATF_FFL holds 77,514), FED_SEC_EDGAR (200),
FED_FEC_API (500), FED_US_USASPENDING_API (300), FED_USASPENDING_BULK — all
single API pages of corpora already landed in bulk elsewhere.

Certified genuinely complete highlights: UN sanctions (1,011, exact), CISA KEV
(days-stale), MSRB registrants (exact 925), FHFA suspended counterparties
(exact 241), OFCCP CSAL (exactly 2,000 by design), FDIC failed banks (~4,100,
full history), FJC judges (~4,000), Freedom House, census boundary files,
HRSA health centers (1,356 vs 1,359), NCUA CU list, EIA-861 single-year
sheets (multi-year history optional), MEDSL election returns, Purple Book,
Superfund boundaries, CIP codes, WBD HUC8, ISO MIC.

Notable UNKNOWNs to resolve cheaply: TX lobby family (4 tables), CA_LOBBY_
EMPLOYER, FED_USCIS_DATA, FED_CMS_MAIN, ENSEMBL, cannabis bundles, FTC
datasets, OWID CPI, HIFLD, BOP stats, EU SOCTA, VA suicide appendix,
Revolving Door, EG CAPMAS, ICE statistics, Google polads stats.

Portal-catalog stubs (in scope only if portals ruled in): BR/GH/GE/BD/ES/CL/
CA/FR/AR data portals, NASA/FAA/DOT-BTS/CDC catalogs, Eurostat, FAOSTAT,
EUR-Lex, ADB.
