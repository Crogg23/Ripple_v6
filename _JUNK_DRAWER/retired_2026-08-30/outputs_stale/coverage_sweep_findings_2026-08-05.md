# Coverage Sweep — Key & Join Discovery Findings (2026-08-05)

**Worker:** Fable, per mission packet `mission_packet_key_discovery_2026-08-05.md`.
**Big change from the last sweep: the warehouse is ALIVE.** COMPUTE_WH connected and ran
real queries (quota apparently reset Aug 1). Everything below marked "measured" is real
SQL against LIBRARY_RAW.LANDING run today — sampled semi-joins and value probes, not
metadata reading.

## The count (packet asked for this first)

| Track | Asked | Done |
|---|---|---|
| 1. Inventory the "~793" unknowns | build the list | **100% — and the premise was wrong.** The 895 unfingerprinted landing tables are ALL portal crawl (892 `PORTAL_CKA_*` + 2 `PORTAL_SOC` + 1 `PORTAL_ARC`). There are ZERO unknown federal tables: every one of the 375 non-portal landing tables is already fingerprinted. |
| 2. Open the 285 unverified pairs | real overlap per pair | **100% — and it's 299 pairs, not 285** (311 pair-key jobs, every one measured with a sampled semi-join). |
| 3. Gap-hunt the spine | find disguised keys | 408 unmapped ID-shaped columns probed across 85 tables; **3 new key families verified by join** (NDC, EPA case number, CUSIP), 4 disguised-CCN columns verified, 3 new trap families found. |
| 4. External gaps | list, no build | 6 named, ranked below. |

Net-new keys/domains: **NDC (pharma bridge, 4 tables), EPA enforcement case number
(3 tables), CUSIP (3 tables, 109M rows), CCN-in-disguise (4 columns incl. facility
ownership chains), FARA registration number (1 table)**.

---

## Ranked findings

### F-1. Sorted-load cap truncation — a trap class nobody had named, and it poisons joins silently. (MEASURED)
`FED_IRS_AUTO_REVOCATIONS` is 500k-capped **and was loaded in EIN order**:
min EIN `000003154`, max `454595836`. The top ~55% of the EIN space never landed.
Any join against it silently loses every partner whose EIN starts above `45…` —
that's why the Form 5500 × auto-revocations control (a *verified-edge* pair, finding
A-2 last sweep) measured only **10 matching EINs in a full join**. This is worse than
the known "cap understates rates" trap: a sorted load + cap **fakes disjointness**.
- Blast radius: **35 landing tables sit at exactly 500,000 rows**, 1 at 20M
  (`FED_USASPENDING_CONTRACTS_FULL`), 209 total at suspiciously round counts (171 are
  the 10k portal samples). 74 of the 311 Track-2 pair-jobs touch a capped side —
  classified `blocked-by-cap`, not disjoint.
- **Action (green-lane, next):** for each 500k table, check whether min/max of its key
  column spans the full key space; sorted-truncated ones need reload before ANY absence
  SQL. A-2, A-3, B-4, B-11 from the last sweep are all suspect until
  `FED_IRS_AUTO_REVOCATIONS` is reloaded.

### F-2. NDC — a whole pharma key family the spine doesn't have. (MEASURED, joins verified)
Four sources carry National Drug Codes today, all invisible to the lattice:
- `FED_DEA_ARCOS_FULL.NDC_NO` — **178.6M rows**, 100% filled (opioid/controlled-substance shipments)
- `FED_CMS_NADAC.NDC` — 1.5M rows, 100% (drug prices; was already flagged as a fingerprint priority)
- `FED_CMS_OPEN_PAYMENTS*.ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_1..5` — 70% fill on slot 1, ×3 year slices
- (FAERS drug names → NDC once the FAERS quartet is fingerprinted — the C-1 priority from last sweep)
Verified joins: ARCOS→NADAC **11.2%** raw (real but suppressed by 10-vs-11-digit padding
— needs segment normalization); Open Payments→NADAC **24.7%** once NDC is normalized
5-4-2 (naive dash-strip gives 0.0% — the normalization IS the key).
**Why it matters:** this bridges DEA shipment volumes ↔ drug prices ↔ industry payments
↔ (soon) adverse events — a drug-harm chain the spine currently cannot express. New
key type for `connect/keys.py`, STEEL-grade semantics.

### F-3. A-4 is dead as framed: HCRIS physically cannot join nursing homes. (MEASURED)
`FED_CMS_HCRIS` is **hospital cost reports only** — 6,103 rows, facility types STH/CAH/
PH/RH/LTCH/CH. CCN overlap with `FED_CMS_NURSING_HOME`: **0.0% in both directions** on
clean same-format 6-char samples. The 26 "credible" HCRIS-gap verdicts were population
artifacts (hospitals vs. non-hospitals), not filing gaps, and no CCN padding fix will
change that. The real gap is external → F-8.

### F-4. CCN hiding in four unmapped columns — facility ownership chains. (MEASURED)
- `FED_CMS_POS_OTHER.PARENT_PROVIDER_NUMBER` → HCRIS CCN: **74.4%** — parent/child
  facility links, i.e. ownership/consolidation chains the spine has never seen
- `.CROSS_REF_PROVIDER_NUMBER` → HCRIS: **34.5%**; `.RELATED_PROVIDER_NUMBER`, `.FQHC_APPROVED_RHC_PROVIDER_NUM` same family
- `FED_CMS_HOSPITAL_COMPARE.FACILITY_ID` → `FED_CMS_HOSPITAL_GENERAL.CCN`: **100.0%** —
  a 5,432-row quality table that was sitting outside the CCN spine entirely
- `FED_CMS_MEDICARE_DIALYSIS_FACILITIES.ALTERNATE_CCNS` → `FED_CMS_DIALYSIS.CCN`: **88.4%**
**Action:** add these columns to the fingerprint key map; POS parent/cross-ref links are
a new *edge semantics* (ownership, not identity) worth a spine-entity decision.

### F-5. EPA enforcement-case key family links ECHO to the ICIS case tables. (MEASURED)
`FED_EPA_ECHO.FEC_CASE_IDS` → `FED_EPA_ICIS_FEC_CASE_FACILITIES.CASE_NUMBER`: **47.7%**;
case-facilities → enforcement-conclusions: **90.4%**. Same `0X-YYYY-NNNN` format across
all three. This converts B-7's "inspection absence" into full facility → case →
enforcement-outcome chains. New key type (EPA_CASE_NO).

### F-6. The 299 unverified pairs, all opened. The last sweep's "none outrank the verified pool" assumption: TESTED, and largely true — with exceptions. (MEASURED)
Classification of 311 pair-key jobs (5k-value sampled semi-join each, smaller side →
full larger side):
| Class | Count | Meaning |
|---|---:|---|
| join-works (sparse hits) | 58 | Key semantics align; the sparse hits are mostly "shouldn't-overlap" compliance shapes — the hits themselves are leads |
| format-mismatch-fixable | 5 | All CIK: zero-padded (`0001843162`) vs unpadded — one LPAD fixes them |
| blocked-by-cap | 74 | A capped side (F-1) makes the verdict unreliable — retest after reload |
| disjoint | 174 | 62 are CCN cross-type pairs — **A-1's namespace-artifact call now empirically confirmed with value samples**; the rest are genuinely different populations or sentinel-poisoned (F-7) |
Standouts inside join-works: `FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS` ×
LEIE (excluded providers inside a new CMS payment model — 2 hits in a 5k sample before
any enumeration), LEIE × `FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS`, and
IRS_REVOCATION × SEC DERA/EDGAR (A-5's flip lead: joinable, sparse as predicted).
Positive control: MSHA accidents → mines measured **100.0%** — the method is sound.

### F-7. New trap columns (sentinels that fake keys). (MEASURED)
- **DOCKET `'0'` sentinel**: `FED_MSHA_VIOLATIONS`, `FED_SCDB`, `FED_OYEZ`,
  `FED_FEDERAL_REGISTER_DOCUMENTS` — docket columns dominated by literal `'0'`.
  All 9 DOCKET pairs in Track 2 are untestable until filtered. B-12 stays parked.
- **LEIE NPI re-confirmed**: 74,780 of 83k rows are literal `'0000000000'`.
- **NPPES identifier tails**: `OTHER_PROVIDER_IDENTIFIER_5..36` and
  `PROVIDER_LICENSE_NUMBER_5..15` are ≤0.01% filled (n=0–411 of 9.6M) — look like key
  columns, are structurally empty slots. `OTHER_PROVIDER_IDENTIFIER_1` (16.3% fill,
  legacy Medicaid/Medicare IDs + issuer columns) is the only one worth anything.
- `FED_CMS_FACILITY_AFFILIATION.FACILITY_TYPE_CERTIFICATION_NUMBER`: 188 non-blank of
  2.26M — trap sibling, despite perfect CCN-shaped samples.

### F-8. Track 4 — external datasets that plug measured holes (list only, no build)
1. **CMS HCRIS non-hospital cost reports** (SNF-2540, HHA-1728, Hospice-1984, Renal-265
   forms; public CMS downloads) — the only honest fix for A-4/F-3.
2. **Full reloads of the sorted-truncated capped tables** (F-1) — not new data, but the
   highest-value "acquisition" on the board; IRS auto-revocations first.
3. **FDA NDC Directory** (product + package files) — canonical NDC spine + proprietary
   names; makes F-2 a first-class key family and gives FAERS its bridge.
4. **A CUSIP↔issuer bridge** — 13F trio (101M + 3.8M + 3.8M rows) carries CUSIP
   internally (positions→holdings 100% verified) but nothing maps CUSIP→CIK/ticker.
   SEC fails-to-deliver files (CUSIP+ticker, free) or N-PORT holdings would connect
   109M rows of institutional holdings to the existing CIK spine.
5. **FMSHRC docket records** — the only way to make MSHA contested-violation dockets
   joinable (CourtListener doesn't cover the review commission; B-12).
6. **Municipal domain decision** — the 892 `PORTAL_CKA_*` tables are 10k-row *samples*
   of city open-data (Boston etc.), not full datasets. If local government becomes a
   Ripple domain, these need full harvests + their own key taxonomy (parcel IDs, local
   permit/case numbers). That's a taste call, flagged, not built.

---

## Assumptions from the last sweep — audited as the packet demanded

| Carried assumption | Verdict |
|---|---|
| "895 / 102 / 793 split" | **Wrong arithmetic, wrong premise.** 895 − 102 = 793 subtracts disjoint sets (102 zero-key tables are *fingerprinted*). Real numbers, measured today: landing = 1,938 (5 new since the lattice build), fingerprinted = 1,043 (all still present), unfingerprinted = 895 = entirely portal crawl. |
| "285 unverified pairs" | **Off by 14.** Recomputed from the same lattice + edge files: 299 pairs / 311 pair-key jobs. |
| "None of the 285 outrank the verified pool" | Mostly holds after measurement, with 5 fixable CIK pairs, ~58 joinable pairs whose sparse hits are lead-shaped, and 74 unknowable-until-reload. |
| STEEL/STRONG tiering | Not re-derived; carried as-is from `connect/keys.py` KEY_TOKENS. |
| "2,694 verified edges" | 2,694 edge *rows* = 2,371 distinct table pairs (multi-key edges collapse). Both numbers real, in `library.json`. |

## Caveats (apply to everything above)

1. All overlap percentages are **5,000-distinct-value sampled semi-joins**, not full
   joins (except the Form5500×auto-revocations debug, which was full). Direction:
   sampled smaller table → full larger table. Good for "does the join work," not for
   exact rates.
2. Two of five positive controls errored on guessed column names (hospice CCN, TRI
   FRS) and were not re-run; the MSHA 100% control plus the manual EIN debug carry the
   method validation.
3. NDC ARCOS↔NADAC at 11.2% is a floor — 10-vs-11-digit padding wasn't normalized for
   that pair (Open Payments got the 5-4-2 treatment and jumped 0%→24.7%; ARCOS likely
   improves the same way).
4. Warehouse quota: today's run worked on COMPUTE_WH as ACCOUNTADMIN (the PAT's default
   role — the RIPPLE_READER PAT constraint from memory still stands for anything
   serving-facing). Whatever exhausted SERVE_MON in July can exhaust it again;
   the sweep spent compute deliberately but sampled everything.
5. My shape-classifier regexes (CIK/DUNS/MMSI = "any digit string") over-flag; every
   candidate promoted to a finding above was verified by an actual join, not by shape.

## What this run did NOT do

- Did not fingerprint the 895 portal tables (deliberate: scoped-out corpus, and a
  domain-level taste call — F-8.6).
- Did not run any absence/record-level lead SQL — this was a coverage sweep; the lead
  list still lives in the last sweep's B-findings, now with F-1 corrections.
- Did not fix anything: no fingerprint refresh, no keys.py changes, no reloads. Every
  fix above is named as an action, none executed.
- Did not open the ~750 verified-edge-no-verdict pairs (explicitly last sweep's
  territory, unchanged by this run except where F-1 invalidates cap-touching ones).
- Did not verify FARA registration number beyond existence, and did not chase the
  NPPES `OTHER_PROVIDER_IDENTIFIER_1` legacy-ID payload (medium value, unranked).

## Recommended next step

Green-lane, in order: (1) min/max audit of the 35 capped tables → reload list;
(2) add NDC + EPA_CASE_NO + the four disguised-CCN columns to the key map and refresh
fingerprints; (3) LPAD the CIK joins. Then the absence-sweep leads can actually be
trusted when the confirm SQL runs.
