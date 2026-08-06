# Absence Sweep — Findings List (2026-08-05)

**Worker:** Fable, per mission packet "Absence Sweep."
**Inputs read in full:** `hunch_absence_verdicts.json` (236 verdicts), `hunch_lattice.json`
(key membership, rollups, blind spots), `library.json` / `atlas.json` (2,694 verified
edges — the ground truth used for every "connected" claim below), no fresh warehouse
queries (SERVE_MON quota exhausted; nothing here touched Snowflake).

**Status of every claim:** "verified join" always means an edge in `library.json`/`atlas.json`
on the named key. No record-level gap has been SQL-measured yet — that's the follow-up
work once the warehouse is back. This list ranks *where to point that SQL first.*

---

## Global caveats (apply to everything below)

1. **Row counts of exactly 500,000 are loader caps, not true sizes** (known trap:
   round-count caps). Any absence *rate* computed against a capped table understates the
   denominator. Affected below: SDWA tables, NPDES inspections, EPA air emissions,
   CDC NNDSS, IRS auto-revocations.
2. **The 236 verdicts score histogram-bucket overlap only.** "Credible" means the two
   key populations occupy the same value space — it says nothing about whether the two
   populations *should* match. Population semantics were applied by this sweep, not by
   the scorer.
3. **Time alignment is unchecked everywhere.** OSHA ITA is 2023–2025 slices; SEC DERA is
   quarterly slices; IRS revocation dates span decades. Every finding below needs a
   date-window filter in the confirm SQL or reporting-lag artifacts will flood it.
4. **Packet discrepancy:** the packet says `blind_spots.zero_key_tables` holds the full
   895. It holds **102** (fingerprinted tables with zero identified keys). The 895 is
   `unfingerprinted_landing` — a count only; no list of those tables exists in the
   lattice file. Section C ranks the 102 that are enumerable.

---

## A. The 236 existing verdicts — read, classified, ranked

Verdict distribution: 222 "credible", 14 "unverifiable" (sparse histograms).
Keys: CCN ×186, EIN ×50. Classification by population semantics:

| Class | Count | Meaning |
|---|---|---|
| Cross-type CCN pairs (e.g. dialysis × nursing home) | 157 (145 credible) | **Namespace artifact — discard.** CCN is one numbering system shared by all facility types; different types are genuinely different populations (artifact test b). |
| All-type registry × type registry (HCRIS / POS / affiliation) | 28 (26 credible) | Meaningful — see A-4. |
| Cross-domain EIN | 50 (all credible) | Mixed — the good ones are A-2, A-3, A-5. |
| Same-population | 1 | FQHC × RHC enrollments — low value (dual enrollment is routine). |

**A-1 (meta-finding): 65% of the "credible" verdict pile is namespace artifact.**
The scorer passed 145 cross-type CCN pairs because their CCN histograms overlap — which
they always will, since CCN buckets by state prefix. Any future absence run on CCN needs
a facility-type gate before scoring. *Nothing in that 145 is a lead.*

**A-2. Revoked nonprofits still operating employee benefit plans.**
- Tables/key: `FED_DOL_FORM5500` × `FED_IRS_AUTO_REVOCATIONS`, EIN (STEEL). Join verified (EIN edge).
- Should/shouldn't: an org whose exemption was auto-revoked (3 years of non-filing —
  i.e., likely defunct or non-compliant) should not be actively filing pension/benefit
  plan reports. Overlap = still-operating employers with revoked status.
- Verdict from data: credible — "shared occupied buckets."
- Harm: employees paying into benefit plans run by orgs that lost tax-exempt standing for non-compliance.
- Artifact risk: **medium** — revocation-then-reinstatement is common; confirm SQL must
  exclude EINs later reinstated (BMF/Pub78 presence) and align plan-year vs revocation date. Not yet ruled out.

**A-3. Revoked nonprofits still logging workplace injuries (still operating, with staff).**
- Tables/key: `FED_IRS_AUTO_REVOCATIONS` × `FED_OSHA_ITA_CASE_DETAIL_2023/2024/2025`, EIN (STEEL). Joins verified (EIN + NAME@ZIP edges).
- Should/shouldn't: OSHA injury logs in 2023–25 from EINs revoked years earlier = orgs
  operating with employees while outside the exempt system.
- Verdict from data: credible ×3 (one per year slice).
- Harm: workers injured at employers that are off the IRS books — the same orgs likely skip other compliance too.
- Artifact risk: **low-medium** — reinstatement filter needed (same as A-2); OSHA ITA EIN is 89–91% populated, so the join side is solid.

**A-4. Facilities operating with no Medicare cost report (HCRIS gap).**
- Tables/key: `FED_CMS_HCRIS` × {`NURSING_HOME`, `HOSPICE`, `HOME_HEALTH`, and their enrollment tables}, CCN (STEEL). 26 credible verdicts.
- Should/shouldn't: every Medicare-certified institutional provider must file an annual
  cost report. A certified facility in the registry with no HCRIS row is either shielding
  finances or newly certified.
- Verdict from data: credible — "24–32 shared occupied buckets" per pair.
- Harm: cost reports are the only public window into facility finances (staffing spend, related-party transactions); a facility that skips them is financially opaque while housing patients.
- Artifact risk: **medium, flagged** — the verified edge between HCRIS and these
  registries is **NAME@ZIP only, not CCN**, despite both carrying CCN. That smells like a
  CCN format mismatch (HCRIS `PROVIDER_CCN` padding/type). Confirm SQL must normalize CCN
  before calling anything absent — otherwise the whole "gap" could be a join-format artifact. Also: new-facility lag (first report due ~5 months after fiscal year end).

**A-5 (flip lead). Revoked charities appearing as SEC registrants.**
- Tables/key: `FED_IRS_REVOCATION` / `FED_IRS_AUTO_REVOCATIONS` / `FED_IRS_BMF` / `FED_IRS_PUB78` × `FED_SEC_DERA_SUB_*` / `FED_SEC_EDGAR_FINANCIALS`, EIN (STEEL). 34 of the 50 EIN verdicts. BMF × EDGAR_FINANCIALS has a verified CIK~EIN edge.
- Should/shouldn't: inverted — nonprofits mostly *shouldn't* be SEC filers, so this is an
  **unexpected-presence** check, not absence: which revoked-exemption EINs show up filing
  with the SEC (shell reuse, EIN recycling, conversion to for-profit without cleanup)?
- Verdict from data: credible (bucket overlap exists — meaning the presence is real enough to enumerate).
- Harm: donors and investors both relying on a status (charity / registrant) the other regulator says is dead.
- Artifact risk: **high, not ruled out** — SEC DERA EIN is 73–79% populated and EINs get
  recycled; expect a small, noisy overlap. Worth one enumeration query, not more, until
  the hit list is eyeballed.

The 14 "unverifiable" verdicts are all sparse-histogram CCN pairs — correctly dropped, nothing lost.

---

## B. Untested pairs — verified join, no absence check yet (the step-2 sweep)

Universe swept: all gated member pairs on CCN, NPI, EIN, FRS_ID, MINE_ID, CIK, PWSID,
DOCKET from `key_membership`. Result: **~750 pairs have a verified edge but no absence
verdict**; 285 more share a key with no verified edge yet. Ranked picks below; the full
machine-readable pair list is in the scratchpad run (`sweep_raw.json`) and reproducible
from `absence_sweep.py`.

**B-1. Excluded providers still receiving industry money.**
- `FED_HHS_OIG_LEIE` (83,464 excluded individuals/entities) × `FED_CMS_OPEN_PAYMENTS` (15.4M payments), NPI (STEEL). Join verified.
- What shouldn't exist: pharma/device payments to providers *after* their exclusion date.
- Harm: excluded-for-fraud providers still being courted and paid by industry are almost certainly still practicing somewhere.
- Artifact risk: **flagged, manageable** — LEIE NPI is only **10.4% populated** and the
  table carries `trap_leie_npi_and_dates`. A non-match proves nothing (missing NPI ≠ not
  excluded); a *match with payment date > exclusion date* is the finding. Direction of
  the check matters: enumerate matches, don't score absences. Open Payments is also
  trap-flagged (`trap_open_payments_split`) — use all three year slices.

**B-2. Excluded providers still on the Medicare order-and-refer list.**
- `FED_HHS_OIG_LEIE` × `FED_CMS_ORDER_AND_REFERRING` (500k cap), NPI (STEEL). Join verified.
- What shouldn't exist: an NPI on both lists simultaneously — excluded from federal
  programs yet currently eligible to order/refer Medicare services.
- Harm: every order written is a claim the government pays to someone barred from the program.
- Artifact risk: **low for matches** (same LEIE NPI caveat as B-1; also check LEIE
  reinstatement/waiver dates before calling any hit live). This is the cleanest
  "banned but still operating" instance in the whole sweep — same shape as the
  already-confirmed LEIE × Part D lead, but against the *authorization* list rather than billing.

**B-3. Excluded providers affiliated with Medicare facilities / applying to re-enroll.**
- `FED_HHS_OIG_LEIE` × `FED_CMS_FACILITY_AFFILIATION` (2.26M affiliations), NPI (STEEL), verified; and × `FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS`/`_NON_PHYSICIANS` (pending enrollment applications), NPI, verified.
- What shouldn't exist: excluded NPIs listed as current facility affiliates; excluded NPIs with pending Medicare enrollment applications.
- Harm: facilities employing excluded providers face 42 CFR liability — and their patients are being treated by them; the pending-enrollment overlap is CMS about to re-admit the excluded.
- Artifact risk: same LEIE NPI/date caveats; affiliation data has its own staleness lag — check affiliation snapshot date vs exclusion date.

**B-4. Revoked nonprofits still spending large federal awards.**
- `FED_IRS_REVOCATION` (1.2M) / `FED_IRS_AUTO_REVOCATIONS` × `FED_FAC_SINGLE_AUDIT` (411k audits of orgs spending ≥$750k federal money), EIN (STEEL). Joins verified (EIN + NAME@ZIP).
- What shouldn't exist: single-audit filings dated after the EIN's revocation with no reinstatement.
- Harm: federal grant dollars flowing through orgs the IRS already declared non-compliant — grantees' clients (housing, health, education programs) are downstream.
- Artifact risk: **medium** — reinstatement filter mandatory; also single-audit EINs can be fiscal sponsors, so a hit needs an entity-name sanity check. Neither yet ruled out — that's the confirm SQL.

**B-5. Water systems with no lead/copper sampling on record.**
- `FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS` (434k systems) × `FED_EPA_SDWA_SDWA_LCR_SAMPLES` (500k cap), PWSID (STEEL). Join verified.
- What should exist and may not: every active community water system owes Lead & Copper Rule sampling; a system with zero LCR sample rows is either exempt, tiny, or unmonitored.
- Harm: this is the Flint shape — the *absence of testing* is itself the exposure; residents of never-sampled systems have no lead data at all.
- Artifact risk: **high until the cap is fixed** — LCR_SAMPLES is truncated at 500k, so
  "no sample rows" may mean "rows not loaded." This finding is *blocked on a full LCR
  reload*, then becomes one of the strongest in the sweep. Also filter to active
  community systems (schedule exemptions are legitimate).

**B-6. Systems with violations but no site visits (and the reverse).**
- `FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT` × `FED_EPA_SDWA_SDWA_SITE_VISITS`, PWSID (STEEL). Verified. Complements the already-found public-notice chain — do not re-surface that one; this is the *inspection* leg.
- What should exist: repeat-violator systems should show state site visits; chronic violators with zero visit rows = enforcement absence.
- Harm: communities drinking from systems regulators cite on paper but never physically inspect.
- Artifact risk: both tables 500k-capped (same reload caveat as B-5); states also log visits in state systems SDWIS may not mirror — say "no federal record of a visit," not "never visited."

**B-7. Toxic-release facilities with no inspection trail.**
- `FED_EPA_TRI_BASIC_2023` (78,647 release reports) × `FED_EPA_NPDES_NPDES_INSPECTIONS` / `FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS`, FRS_ID (STEEL). Joins verified. The whole FRS_ID family — **91 verified pairs, zero absence verdicts** — is the largest untouched high-harm block in the lattice.
- What should exist: facilities self-reporting toxic releases should appear somewhere in the inspection/enforcement record; TRI filers invisible to ECHO/ICIS inspections are self-reporting into a void.
- Harm: neighbors of facilities that report emitting toxics and have never had a recorded federal inspection.
- Artifact risk: **medium** — TRI is self-reported (presence there is the *good* actors);
  state-delegated inspections may not federate; NPDES inspections capped at 500k. Rule
  out by restricting to high-quantity releasers and multi-year TRI presence.

**B-8. Mines with accidents but no violations on record.**
- `FED_MSHA_ACCIDENTS` (273k) × `FED_MSHA_VIOLATIONS` (3.1M) × `FED_MSHA_MINES` (91,906), MINE_ID (STEEL). All three joins verified. No verdicts.
- What should exist: a mine with serious/fatal accidents and zero violation history means MSHA never wrote anything up before or after people got hurt.
- Harm: miners at operations where injury and enforcement records don't meet.
- Artifact risk: **low** — closed universe, uncapped tables, one agency, one clean key. Best power-to-effort ratio in the list; filter to accident severity and active-mine status via the MINES registry.

**B-9. Nursing homes not submitting resident assessments.**
- `FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY` × `FED_CMS_NURSING_HOME` (14,700 homes), CCN (STEEL). Join verified (CCN + NAME@ZIP).
- What should exist: every certified nursing home must submit MDS resident assessments; a certified home missing from the MDS frequency file isn't reporting resident condition data.
- Harm: residents of facilities whose care data never reaches the oversight system — the same facilities most likely to hide understaffing and decline.
- Artifact risk: **low-medium** — new certifications lag; MDS file is 500k-capped but it's facility-level frequency, so the cap likely doesn't bite. Adjacent to (not duplicating) the known deficiencies↔penalties lead.

**B-10. Hospices operating vs. hospices enrolled.**
- `FED_CMS_HOSPICE` (6,852) × `FED_CMS_HOSPICE_ENROLLMENTS` (6,066), CCN (STEEL). Verified (CCN, NAME@ZIP, ZIP). The ~800-row gap is visible in the row counts alone.
- What should exist: 1:1-ish correspondence between the quality registry and enrollment file; either side's orphans are hospices in one CMS system and not the other.
- Harm: hospice is the current fraud epicenter (shell hospices, license flipping); registry/enrollment mismatches are exactly where shells live.
- Artifact risk: **medium** — snapshot dates differ between files; CCN population is 75–79% on both sides, so name-based fallback matching is needed before quantifying.

**B-11. Revoked orgs still filing 990s.**
- `FED_IRS_REVOCATION` × `FED_IRS_990_EFILE_INDEX` (5.5M filings), EIN (STEEL). Verified.
- What shouldn't exist: 990 e-filings dated after revocation without reinstatement — orgs presenting as exempt to donors while revoked.
- Harm: donors misled by current-looking filings from revoked orgs.
- Artifact risk: **medium-high** — filing *is* the path back to reinstatement, so post-revocation filings are partly the remediation process itself; must split "filing to reinstate" from "filing as if nothing happened" by checking Pub78 status.

**B-12 (lower confidence, STRONG tier). Contested mine violations with no docket trail.**
- `FED_MSHA_VIOLATIONS` (DOCKET_NO, only 6.2% populated) × `FED_COURTLISTENER_DOCKETS`, DOCKET (STRONG tier). 9 pairs in the DOCKET group are untested; only one verified edge exists in the group.
- What should exist: contested violations should trace to review-commission/court dockets.
- Harm: operators who contest their way out of penalties invisibly.
- Artifact risk: **high** — 6.2% population plus docket-format mismatch (FMSHRC dockets aren't federal-court dockets, so CourtListener coverage is partial by design). Park unless Chris wants the enforcement-evaporation angle specifically.

Also swept, deliberately not surfaced: CIK family (94 verified pairs — pure finance,
weakest human-harm link; EDGAR insiders × financials is the only one worth a later look),
BIOGUIDE (5 tables, verified, senate-trades journalism-use constraints), the remaining
NPI billing-slice pairs (year-slice permutations of already-known leads).

---

## C. Fingerprinting priorities (the step-3 flag list)

From the 102 enumerable zero-key tables (see caveat 4 — the other ~793 unfingerprinted
landing tables aren't listed anywhere in the lattice and need an inventory diff first).
Ranked by domain cluster richness × size:

1. **FDA FAERS quartet** (`_DRUG`, `_REAC`, `_INDI`, `_OUTC` — 56M rows, HEALTH, richest cluster: 49 keyed tables). Adverse-event reports; case-ID internal spine plus drug names → NDC/NADAC. Unlocks drug-harm ↔ prescriber ↔ payment chains against Part D and Open Payments.
2. **CMS NADAC** (1.5M rows, HEALTH) — has NDC in the description; cheap fingerprint, bridges FAERS ↔ Part D drug names to prices.
3. **SEC raw insider + 13F sextet** (`FED_SEC_13F_HOLDINGS` 101M, `_POSITIONS`, `_SUBMISSION`, `FED_SEC_INSIDER_*` — FINANCE, 28-keyed cluster). Almost certainly carry CIK/accession numbers; plugs the biggest raw tables in the warehouse into the existing CIK spine.
4. **EPA ICIS-AIR sub-tables + `NPDES_QNCR_HISTORY`** (ENVIRONMENT, 500k caps) — the violations-side tables the packet already flagged as zero-key; fingerprinting these is what converts findings B-6/B-7 from "inspection absence" into full violation→enforcement chains. Likely carry NPDES_ID/registry IDs mappable to FRS.
5. **`FED_SENATE_STOCK_WATCHER`** (8,350 rows, UNFILED) — name-only trap domain (per senate-trades memory), but tiny; cheap to fingerprint, journalism-use-only constraint noted.
6. **`FED_CDC_WONDER` / `FED_FDA_DRUG_ENFORCEMENT`** — 1-row stubs, not fingerprint candidates; they need re-ingestion, listed so nobody mistakes them for data.

---

## What this run did NOT do (honesty section)

- No record-level absence was measured — warehouse is down; everything above is
  join-topology + verdict-file reading + population semantics.
- Did not re-surface the four already-confirmed leads (nursing home def↔pen, SDWA
  public-notice chain, Pub78 revoked-donee, LEIE×Part D billing) except where a genuinely
  different leg exists (B-2 vs billing; B-6 vs public notice).
- The 285 share-a-key-but-no-verified-edge pairs were enumerated but not individually
  read; none outranked the verified-edge pool on harm, and per the packet's own rule the
  right output for unverified joins is "verify the join first," not an absence claim.

## Recommended next step (when Chris picks)

For each picked finding: one record-level SQL per pair (anti-join with date alignment +
reinstatement/cap filters as flagged), runnable the moment SERVE_WH resumes. B-8 (MSHA)
is the cheapest full test of the method end-to-end; B-2 (LEIE × order/refer) is the
highest harm-per-query.
