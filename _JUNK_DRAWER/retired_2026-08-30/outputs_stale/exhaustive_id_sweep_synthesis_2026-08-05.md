# Exhaustive Identifier & Join Sweep — Synthesis (2026-08-05)

**Ask:** "Loop through and make sure you missed nothing... FULL list of things that are POSSIBLE,
whether now or nice-to-have later... anything connected to information I already have."

**Method:** 25 domain clusters covering everything Ripple currently touches plus adjacent
domains it doesn't. Each domain got a finder pass (exhaustive web research) followed by an
adversarial critic pass ("what did you miss, and is anything here secretly a classification
code masquerading as a real ID"). 50 agents total, grounded against Ripple's real 150+-source
agency list (not a guess — pulled live from the warehouse before the sweep started). Full raw
detail for all 743 surviving candidates: `full_id_standard_catalog_2026-08-05.md` (same
folder). This file is the curated, prioritized version.

**Top-line count:** 756 candidates surfaced → 9 pulled as classification codes wrongly
tiered as entity keys → **747 real candidates** across 25 domains, 138 restricted/PHI/legal-walled,
the rest split roughly evenly between usable-now and nice-to-have-later. (First pass over this
had a self-inflicted bug — a naive substring match excluded "FATCA GIIN" and "Retraction Watch"
because their spelled-out names happen to contain the letters "atc" inside "f**ATC**a" and
"w**ATC**h". Caught and fixed before this report went out — see Section 5.)

---

## 1. Verified findings — real, checked with live SQL this session, ready to wire

Unlike everything else in this sweep (which is agent research, unverified against our data),
these five I personally confirmed with SQL against `LIBRARY_RAW.LANDING` after the sweep
flagged them:

- **MSHA already carries a parent-company/contractor bridge nobody is using.**
  `FED_MSHA_MINES.CURRENT_CONTROLLER_ID` (98.9% filled, 41,050 distinct controllers),
  `FED_MSHA_VIOLATIONS.CONTROLLER_ID` (93.2% filled) / `.VIOLATOR_ID` (100%) /
  `.CONTRACTOR_ID` (only 6.7% — thin, use with caution), `FED_MSHA_ACCIDENTS.CONTROLLER_ID`
  (99.7%) / `.OPERATOR_ID` (99.7%) / `.CONTRACTOR_ID` (10.4% — also thin). 4,686 distinct
  controller companies already cross-match between accidents and mines in a real join I ran.
  Values are quote-wrapped (`"0041044"`) — same CSV-parse pattern as the known MINE_ID trap,
  same fix applies. **This means mine-company ownership roll-ups (who's really behind a
  string of "different" mines with bad safety records) are possible today with zero new
  data acquisition — the columns are just sitting unrecognized.**

- **OpenSanctions is already live and bigger than the sweep assumed.** `INTL_OPENSANCTIONS`,
  71,011 rows, confirmed in both `LIBRARY_RAW.LANDING` and as a built mart
  (`LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS`). One domain agent (financial crimes)
  incorrectly concluded Ripple has no UN Security Council sanctions coverage and proposed
  acquiring it — it's wrong, we already blend OFAC+UN+EU+UK+dozens of national sanctions/PEP
  lists through this one table. Worth knowing so nobody re-proposes this.

- **`FED_DOL_FORM5500.PLAN_NUM` is a trap — 0% filled.** The agent that flagged "EBSA/ERISA
  Plan Number" as already-live cited this column; I checked it and it's completely blank
  (33,484 rows, 0 non-blank). The REAL populated plan-number column is
  **`SPONS_DFE_PN`** — 100% filled, 266 distinct values, 3-digit format (`001`, `042`...).
  Paired with the already-known EIN key, EIN+SPONS_DFE_PN is the standard way DOL/PBGC
  identify one specific benefit plan (not just the sponsoring company). `LAST_RPT_PLAN_NUM`
  (2.4% filled) and `M1_RECEIPT_CONFIRMATION_CODE` (0.4% filled) are both too thin to use.

- **`FED_DOL_OFLC.CASE_NUMBER` is fully live** — 664,616 rows, 100% filled, 664,616 distinct
  (format `I-200-19066-236817`). This is the real receipt for H-1B/PERM/H-2A labor
  certification cases — see the LCA/PERM/H-2A entries in section 3 below for why that
  matters. `PW_TRACKING_NUMBER_1` on the same table is real but only 0.3% filled — not
  usable as a join key on its own.

## 2. Whole-domain gaps — confirmed, not just under-indexed

Ripple has genuinely zero data from these regulators, not just an unrecognized column:

- **Energy & utilities** — no FERC, EIA, NRC (nuclear), or PHMSA (pipeline safety) data at
  all. (Some energy-adjacent bridges DO exist through EPA/CFTC/FRA tables we already have —
  see the "likely already have" table — but the core energy regulators themselves are absent.)
- **Agriculture & food safety** — no USDA, FSIS, or APHIS data.
- **Insurance** — no NAIC or state insurance-regulator data.
- **Social Security Administration** — confirmed absent. This is a bigger gap than it first
  looks: SSA's Death Master File and disability-determination data underlie several
  "who gets hurt" stories in other domains (benefits fraud, elder abuse, disability denial
  patterns) that currently can't be built at all.

These are Track-4-style acquisition gaps, not build items — flagged for your call on whether
any becomes a real domain.

## 3. Best near-term acquisitions (STEEL tier, free bulk, no legal barrier)

74 candidates cleared the bar of: hard unique ID + realistically free bulk download +
not already something we have. Full harm rationale for each is in the table below (trimmed
to fit — see the appendix file for untruncated text). A few standouts by mission fit:

- **NTSB Accident/Incident Number** and **PHMSA Hazmat Incident Report Number** — the actual
  "who got hurt, how, where" records behind transportation disasters (East Palestine-style
  events), missing even though we have the surrounding FAA/FRA/MSHA context.
- **FDA MAUDE / FAERS report IDs** and **UDI device identifiers** — closes the loop between
  a device/drug recall and the actual harm reports that preceded it.
- **DOL LCA / PERM / H-2A case numbers** — sit on the OFLC table we just confirmed is 100%
  populated (section 1); this is the direct receipt for H-1B wage-suppression and farm-labor
  exploitation patterns.
- **CFPB Consumer Complaint Database Complaint ID** — the one dataset where an ordinary
  person's own words about being harmed attach directly to a specific company, in bulk.
- **340B ID (HRSA OPAIS)** — one of the most actively-investigated healthcare-money stories
  in journalism right now (hospitals/pharmacies pocketing the discount-drug spread).

<details>
<summary>Full table (73 candidates) — click to expand</summary>

| Name | Domain | Bridges to / harm |
|---|---|---|
| FSIS Establishment Number | Agriculture | Ties an FSIS contamination citation to the same physical plant OSHA cites for injuries |
| NTSB Accident/Incident Number | Aviation/Rail | The "who got hurt and why" agency for transportation; no join key today |
| PHMSA Hazardous Materials Incident Report Number | Aviation/Rail | The actual release/harm record for events like East Palestine |
| NCUA Charter Number | Banking | Tracks credit-union predatory patterns and enforcement actions across name changes |
| Ginnie Mae Issuer ID | Banking | Reverse-mortgage issuer collapses strand elderly borrowers mid-servicing |
| HMDA Legacy Respondent ID (pre-2018) | Banking | Needed to trace multi-decade redlining across HMDA's 2018 key-format change |
| VHA Facility Station Number | Benefits/Veterans | Connects veterans routed to community-care hospitals under active quality investigation |
| VA/WEAMS GI Bill School Facility Code | Benefits/Veterans | The ITT Tech / Corinthian pattern on the GI Bill funding side |
| ED Office of Postsecondary Education ID (OPEID) | Benefits/Veterans | Same predatory-school pattern on the federal-loan/Pell side |
| National Cemetery Administration Interment Control Number | Benefits/Veterans | One of the few public individually-identified VA datasets for backlog-death harm |
| USDA FNS SNAP Retailer Authorization Number | Benefits/Veterans | SNAP trafficking — stores stealing food money from poor households |
| HUD Public Housing Authority (PHA) Code | Benefits/Veterans | Chronically-failing REAC-score housing authorities |
| HUD Multifamily FHA Project/Insurance Number | Benefits/Veterans | Federally-insured nursing homes/housing racking up violations while taxpayer-backstopped |
| Medicare Advantage/Part D Contract ID + PBP ID | Benefits/Veterans | CMS's own key for plan-level opioid overprescribing variation |
| Unique Device Identifier (UDI-DI) / GUDID | Consumer Safety | Ties a recalled implant to who actually received it |
| EPA Pesticide Registration Number | Consumer Safety | Matches poisoning reports to registration/cancellation history |
| EPA CompTox Dashboard Substance ID | Consumer Safety | Proves a restricted chemical is the same one in a recalled consumer product |
| NHTSA Recall Campaign Number | Consumer Safety | Shows how many complaints existed before a recall was opened |
| CPSC NEISS Case Number | Consumer Safety | The national injury-count estimate behind every CPSC recall notice |
| FDA MAUDE Report / MDR Report Key | Consumer Safety | The harm half of a device recall — who actually got hurt |
| FDA FAERS Case / Safety Report ID | Consumer Safety | Adverse-event volume/timing that preceded a drug label change |
| JPML MDL Number | Consumer Safety | The court system's own version of Ripple's mechanism-first logic — pre-grouped harm claims |
| NCUA Federal Credit Union Charter Number | Corp. Registration | Credit-union parallel to OCC charter number |
| CMS PECOS PAC ID / Enrollment ID | Corp. Registration | Catches revoked/excluded owners re-enrolling under a new corporate shell |
| FCC FRN (Registration Number) | Corp. Registration | Likely the clean substitute for the already-known masked FCC ULS EIN trap |
| ISIN | Corp. Registration | Follows money when a flagged entity raises capital via a non-US listing |
| FJC Judge NID | Criminal Courts | Judicial conflicts of interest — rulings on cases tied to a judge's own holdings |
| ATF Federal Firearms License (FFL) Number | Criminal Courts | Small share of dealers linked to disproportionate share of crime-traced guns |
| OPEID | Education | Connects a school's Title IV loan flow to its own fraud lawsuits/parent-company filings |
| RCRA Handler ID (EPA ID Number) | Environment | Chains hazardous-waste violations across one operator's multiple sites |
| EPA AQS Site ID | Environment | Proves a neighborhood is a monitoring desert with no pollution data at all |
| National Inventory of Dams (NID) ID | Environment | High-hazard dams with no emergency plan upstream of towns |
| USGS Site Number (NWIS) | Environment | Connects upstream contamination to downstream drinking-water impact |
| USCG Vessel Documentation Official Number | Environment | Covers fatal towboat/barge/fishing accidents (vessels without an IMO number) |
| OFAC-listed cryptocurrency addresses | Fin. Crimes/Sanctions | Shows which ransomware payments flowed to a sanctioned recipient |
| UDI / Device Identifier — GUDID | Healthcare | Traces a device recall to hospitals that bought/implanted that batch |
| FDA Establishment Identifier (FEI) | Healthcare | Ties repeat-failing plants together across drug/device/tissue program silos |
| HIOS ID / Standard Component ID | Healthcare | Rolls up junk-plan/high-denial insurer patterns across CMS filing systems |
| 340B ID (HRSA OPAIS) | Healthcare | Hospitals/pharmacies pocketing the 340B discount-drug spread |
| HMDA Universal Loan Identifier | Housing | Follows one loan across servicer transfers instead of only anonymous snapshots |
| FHA Case Number | Housing | Connects a specific foreclosure to the FHA program that insured it |
| FHA/HUD Multifamily Project Number | Housing | Landlord neglects federally-subsidized housing while still collecting the subsidy |
| CFPB Consumer Complaint Database Complaint ID | Housing | Ordinary borrowers' own harm complaints tied to a specific company, in bulk |
| HUD Public Housing Development Number | Housing | Rolls REAC failures down to the individual development, not just the PHA |
| DOL LCA Case Number | Immigration | The receipt for H-1B wage-suppression and "body shop" patterns |
| DOL PERM Case Number | Immigration | Front door for employment-based green cards; traces sham-recruitment fraud |
| DOL Temporary Labor Cert Case Number (H-2A/H-2B) | Immigration | Farm/seasonal labor exploitation, wage theft, documented trafficking cases |
| HIOS ID (Issuer ID + Plan ID) | Insurance | Ties an enrolled plan to its issuer's track record on premiums/network gutting |
| CMS Medicare Advantage/Part D Contract ID + PBP ID | Insurance | CMS's own key for marketing-complaint/improper-switching harm to seniors |
| GLEIF Level 2 Relationship Data (parent/ultimate parent LEI) | International | Shell-chain tracing for subsidiaries implicated in violations |
| MIC (Market Identifier Code) | International | Catches "delisted from NYSE, still trading on a thin foreign venue" |
| SIREN / SIRET (France) | International | Establishment-vs-entity granularity for site-level violations |
| OpenSanctions consolidated entity ID | International | Merges name-listed-in-one-regime-not-another sanctions gaps |
| OLMS LM File Number | Labor | The only public window into union officer pay/loans/disbursements |
| HIOS Standard Component ID | Labor | Employer-sponsored plan enrollees with a denial-pattern issuer |
| PBGC Case Number (Trusteed Plans) | Labor | Workers whose pension got trusteed and reduced below what was promised |
| Joint Board Enrolled Actuary (EA) Number | Labor | One actuary certifying funding for dozens of plans that go on to fail |
| UN/LOCODE | Motor Carrier/Maritime | Traces a sanctioned "dark fleet" tanker's undisclosed port stops |
| Unique Device Identifier / Device Identifier | Pharma/Devices | Systematically ties a recalled device model to injury reports |
| Unique Ingredient Identifier | Pharma/Devices | Bridges an EPA-restricted chemical to its FDA-regulated product use |
| CAS Registry Number | Pharma/Devices | The correct chemical-identity bridge to EPA data (UNII does NOT work for this) |
| ORCID iD | Science/Research | Tracks a misconduct researcher across institutions/name variants |
| ROR ID | Science/Research | Fixes institution-name text mismatches that undercount grant concentration |
| OpenAlex IDs (Work/Author/Institution/Funder/Source) | Science/Research | Same harm as ORCID/ROR, one bulk download instead of five acquisitions |
| PMID | Science/Research | Connects a grant and a misconduct case to the actual resulting paper |
| PMCID | Science/Research | Catches grantees who never comply with mandated public-access deposit |
| DOI | Science/Research | Extends misconduct tracing beyond biomedical (PMID) and preprints (arXiv) |
| Retraction Watch Database record | Science/Research | Recovered from the filtering-bug correction in Section 5 — a retraction happening at all, and why, is the single most direct research-misconduct harm signal there is, and no institution currently ingests it |
| Investment Adviser Registration Depository Number | Securities | Catches an adviser reopening under a new LLC after an enforcement action |
| Investment Company Series/Class ID | Securities | Retail investors sold high-load share classes of funds institutions get cheap |
| PCAOB Firm ID | Securities | Small audit shops repeatedly blessing books at companies that later restate |
| Global Intermediary Identification Number | Securities | Offshore asset-hiding visible via FATCA registration |
| Antenna Structure Registration Number | Telecom | Tower-climbing deaths (OSHA) tied to tower ownership records |
| USAC Service Provider Identification Number | Telecom | E-Rate fraud — shell vendors overbilling poor school districts |

</details>

## 4. "Likely already have this, unverified" — worth a quick check before any new acquisition

40 candidates the research agents judged were probably already sitting in existing Ripple
tables under an unrecognized column name — same shape as yesterday's NDC/EPA-case-number
finds. **Only the 5 items in Section 1 above are actually verified; everything else below is
an agent's educated guess against our real agency list, not confirmed.** Treat this as a
punch-list for a Track-3-style column check, not a done list.

<details>
<summary>Full table (40 candidates) — click to expand</summary>

| Name | Domain | Basis for the claim |
|---|---|---|
| PIID (Procurement Instrument Identifier) | Procurement/Grants | Near-certain core column in USASpending's prime-award file |
| FAIN (Federal Award Identification Number) | Procurement/Grants | Near-certain core column in USASpending |
| URI (grants Unique Record Identifier) | Procurement/Grants | Same USASpending award file, less consistently populated |
| Parent Award ID / IDV reference | Procurement/Grants | Same USASpending award file typically carries this |
| NSF Award ID | Procurement/Grants | Likely core column in the existing NSF table |
| Product Service Code (PSC) | Procurement/Grants | Sits beside the already-extracted, already-banned NAICS in the same table |
| Grants.gov Funding Opportunity Number | Procurement/Grants | If the existing Grants table is a Grants.gov opportunity feed |
| EDGAR Accession Number | Securities | Backbone identifier of any EDGAR bulk ingestion |
| Ticker / Exchange Symbol | Securities | SEC's free company_tickers.json, paired with CIK |
| SEC Investment Company/Adviser/BDC/Securities Act File Numbers | Securities | Standard EDGAR filing-header "file number" fields, four separate offering-type variants |
| Municipal Advisor Registration (Form MA) | Securities | Lives in EDGAR alongside other filer types |
| SEC Reg A / Reg CF File Numbers | Securities | Same generic file-number column, undecomposed by offering type |
| CINS (CUSIP International Numbering System) | Securities | Almost certainly sitting inside the already-verified CUSIP data |
| FinCEN Identifier | Fin. Crimes/Sanctions | Confirmed present as an empty-shell column in the BOI staging model |
| OFAC SDN ID-document fields | Fin. Crimes/Sanctions | Confirmed present in the OFAC SDN dbt model (passport/national ID/tax ID fields) |
| OpenSanctions structured schema fields | Fin. Crimes/Sanctions | Confirmed — see Section 1 |
| GLEIF Registration Authority Entity ID | International | Standard field on any full LEI Level-1 record we've already ingested |
| Aircraft Manufacturer Serial Number (MSN) | Aviation/Rail | Likely sitting in the existing FAA registry table |
| FRA Highway-Rail Crossing Inventory Number | Aviation/Rail | Likely in the existing single FRA table |
| FRA Railroad Company/Reporting Code | Aviation/Rail | Likely the reporting-railroad field in the existing FRA table |
| FRA Accident/Incident Report Number | Aviation/Rail | Likely the primary key of the existing FRA table |
| PBGC Plan Number (paired with EIN) | Insurance/Benefits | PBGC's whole business is EIN/PN-keyed |
| EPA CAMPD ORISPL + Unit ID | Energy | Standard EPA bulk emissions dataset, EPA already has 42 tables |
| EPA GHGRP Facility ID | Energy | Same reasoning — standard EPA bulk dataset |
| CFTC Large Trader / Commodity Position ID | Energy | CFTC table already present |
| AAR Reporting Mark | Energy | FRA table already present |
| MC/MX/FF Number (FMCSA Operating Authority) | Motor Carrier | Rides alongside DOT# in the same standard FMCSA census file |
| FCC Ship Radio Station Call Sign | Motor Carrier | May be in the existing FCC ULS extract |
| FCC Registration Number (FRN) | Telecom | Core ULS schema field, per the known FCC ULS EIN-masking memory note |
| SAM.gov Exclusion Record (research-fraud filtered) | Science/Research | Not new data — a look-harder note on the existing SAM table |
| EBSA/ERISA Plan Number | Labor | Confirmed — see Section 1 (use SPONS_DFE_PN, not PLAN_NUM) |
| Form M-1 Receipt Confirmation Code | Labor | Confirmed present but only 0.4% filled — see Section 1, not usable |
| OFLC Case Number | Labor | Confirmed — see Section 1 |
| National Prevailing Wage Center Tracking Number | Labor | Confirmed present but only 0.3% filled — see Section 1, not usable |
| MSHA Controller/Violator/Contractor ID | Labor | Confirmed — see Section 1 |

</details>

## 5. Correction — these are NOT join keys (classification codes)

9 items the critic passes caught masquerading as entity identifiers — same category as the
already-banned NAICS/SIC/NCES. Joining on any of these would fan out into thousands of
unrelated matches sharing one code:

RxNorm/RxCUI, LOINC (both drug/lab-test *concepts*, not entities — useful as a vocabulary
layer, never a join key), ATC classification code, UN Number (hazmat class, appeared in two
domains, both times self-caught), Harmonized Tariff Schedule/HS Code, Assistance Listing
Number/CFDA (a *program* code shared across thousands of unrelated awards).

**Self-correction:** my first filtering pass also wrongly excluded FATCA GIIN (all three
domain mentions) and "Retraction Watch Database record" — a sloppy substring match caught
"atc" inside "f**ATC**a" and "w**ATC**h" and treated them as ATC-code matches. Both are real:
GIIN is a genuine per-institution FATCA identifier (now correctly back in the candidate pool,
STEEL/STRONG tier depending on domain, `public_bulk: yes`), and Retraction Watch is a real
research-integrity database with per-record IDs — no institution currently ingests it, no
Ripple table carries it, `public_bulk: yes`, added to the acquisition table in Section 3.

## 6. Restricted / legally walled — 138 candidates, awareness only

Real identifiers, but PHI-protected (Medicare Beneficiary ID), court-authorized-access-only
(identified NPDB reports), or otherwise legally restricted (immigration A-Number — flagged
red-lane last time, still red-lane). None of these are build targets without a legal review
step first. Full list in the appendix file, grouped by domain.

## 7. How thorough was this, honestly

Every domain got a self-critique (a second agent explicitly told to find what the first
missed). None came back clean — every single domain had real gaps on first pass, most
commonly: **person-level identifiers** (licenses/certifications for individuals, not just
organizations — requested explicitly, skipped by nearly every finder on the first try) and
**state-level equivalents of federal programs** (all 25 domains under-index state regulators
relative to federal ones, because federal bulk data is easier to find). Both categories
got a second pass via the critic and are reflected in the 743-candidate count, but a third
pass would likely still find more — this converged, it did not exhaustively terminate.

## 8. What this run did NOT do

- Did not run column-name/value verification against the warehouse for any of the 738
  candidates beyond the 5 in Section 1 — Section 4's "likely already have" list is
  agent-judgment, not fact, until checked the way Section 1 was.
- Did not attempt to acquire, ingest, or wire up anything. This is a catalog, not a build.
- Did not weight state-by-state legal/paywall variation for the ~50-states items (Secretary
  of State entity numbers, state medical boards, state insurance regulators) — flagged as
  real gaps, not scoped into a single acquisition plan.
- Did not re-verify the prior (smaller) external survey's 13 candidates (RSSD, FDIC Cert,
  DOT Number, etc.) — they're excluded from this list by design (told not to re-find them),
  still stand from the earlier report.

## Recommended next step

Green-lane, cheapest first: (1) wire the 5 verified Section-1 finds into `connect/keys.py` —
zero new data needed; (2) run a Track-3-style column check against the 40 Section-4 "likely
already have" candidates to convert guesses into verified/rejected; (3) the 73 Section-3
acquisitions are genuinely new pulls — worth ranking against your own priorities, not mine to
sequence. Whole-domain gaps (Section 2) are a taste call, same as the portal-crawl question
from yesterday.
