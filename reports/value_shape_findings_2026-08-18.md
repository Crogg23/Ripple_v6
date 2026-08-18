# Value-Shape Key Sniffer — Findings (2026-08-18)

Mission packet: `reports/FABLE_PACKET_value_shape_sniffer_2026-08-18.md`.
Read-only run. Nothing was registered, nothing was wired. Every number below was
measured live this session.

---

## Plain-English summary

- **Scanned:** 11,547 columns across all 302 non-portal landing tables (the full
  non-portal universe; 913 provenance columns, 150 already name-detected
  STEEL/STRONG columns, and 124 already spine-wired columns excluded first).
- **Candidates:** 59 from the name-synonym sweep (Stage 0, free) + 359 from the
  value-shape sniff (Stage 1) → 198 distinct columns went to live overlap
  testing (Stage 2).
- **Confirmed:** 18 (table, column, key) pairs pass live value overlap, the
  existing confidence gate, AND mechanism review. 1 more is borderline
  (real content, too little cross-coverage to prove today). 9 passed the
  machine gate but fail mechanism review — documented below so nobody re-tries.
- **The headline:** the four multi-cycle FEC history tables
  (`FED_FEC_COMMITTEES`, `FED_FEC_CANDIDATES`, `FED_FEC_CAND_CMTE_LINKAGE`,
  `FED_FEC_PAC_SUMMARY`) load with **positional headers (C1, C4, C10, C15)**
  and have therefore been invisible to every name-based mechanism since they
  landed. They are the *bigger* copies of the wired single-cycle twins
  (78,039 committees vs 20,007; 33,506 candidates vs 17,900).
- **The important negative:** the 9-digit sweep found **zero hidden EIN
  columns**. Every real EIN in the landing zone is already name-detectable.
  Same for LEI, UEI, DEA, IMO, COMPANY_NO: no confirmed hidden carriers.
- **Spend:** ≈ $2–4 warehouse time (~55 min of busy X-Small serving warehouse
  across all stages) vs the packet's $5–11 estimate.

## What the confirmed finds unlock

**1. Multi-cycle campaign-finance history joins the graph (6 columns).**
The positional-header FEC tables hold committee and candidate IDs in columns
named C1/C4/C10/C15. Overlap with the live spine runs 52–58% — exactly what
multi-cycle data against a current-cycle spine should look like. Wiring them
turns "money → politics" from a single-cycle view into the full history:
which PACs existed across cycles, which candidates they funded, and how the
linkage changed. Humans on the other end: every donor and every candidate.

**2. The candidate ↔ committee crosswalk becomes hard-ID (5 columns on
already-wired tables).** `CAND_PCC` (a candidate's principal campaign
committee), the leadership-PAC table's `FEC_CANDIDATE_ID`, the independent-
expenditure table's `spe_id` (the spending committee), and
`OTHER_ID`/`C15`/`C10` cross-references. These are the edges that answer
"which committee is this candidate's own, and who spends independently for
whom" — previously dark because the tagger's vocabulary is only `cmte_id` /
`cand_id` tokens.

**3. Legislators get FEC identity without waiting for the flatten build.**
`FED_CONGRESS_LEGISLATORS.FEC_IDS` is the known JSON-list column (the parked
flatten build). Single-ID rows normalize clean: 830 sitting/former members
hard-match live FEC candidate IDs today. The flatten build is still the right
fix for multi-ID members; this confirms the values are real.

**4. EPA enforcement cases pin to the facility registry (100.0%, 105,080
facilities).** `FED_EPA_ICIS_FEC_CASE_ENFORCEMENT_CONCLUSION_FACILITIES.FACILITY_UIN`
is a full-population FRS ID under a name the tagger can't see. Wiring it joins
formal enforcement-case conclusions to the 3.28M-facility registry spine:
"which operators' facilities keep concluding enforcement cases."

**5. ECHO joins the drinking-water world (99.3% of it).** `FED_EPA_ECHO.SDWA_IDS`
holds water-system IDs: 430,991 of the live spine's 434,040 distinct PWSIDs
appear in it. ECHO was already wired by facility ID; this adds the
drinking-water leg — enforcement posture joined to the systems people drink
from. (Column is plural-named; rows carrying multiple IDs normalize to NULL
and drop out — safe direction.)

**6. Medicare facility parent/chain edges (4 columns, 97.7–100%).**
`FED_CMS_POS_OTHER` carries parent, related, cross-reference, and
FQHC-approved provider numbers — all live CCNs. These are facility-to-facility
edges *inside* Medicare certification: chains of facilities under one parent.

## The confirmed table (ranked best-first)

| table | column | suspected key | shape hit % | distinct (normalized) | live overlap % | matched distinct | confidence | beats-chance | 5 sample values |
|---|---|---|---|---|---|---|---|---|---|
| FED_EPA_ECHO | SDWA_IDS | PWSID | 98% | 430,993 | 100.0% | 430,991 | 1.0 | 15,575x | MI0927777, FL6280042, MI2064903, FL1664099, FL4434515 |
| FED_EPA_ICIS_FEC_CASE_ENFORCEMENT_CONCLUSION_FACILITIES | FACILITY_UIN | FRS_ID | 100% | 105,113 | 100.0% | 105,080 | 1.0 | 184,990x | 110045689938, 110071206791, 110071299998, 110070247516, 110056255234 |
| FED_CMS_POS_OTHER | FQHC_APPROVED_RHC_PROVIDER_NUM | CCN | 100% | 207 | 100.0% | 207 | 1.0 | 12.2x | 053861, 103821, 363804, 233896, 053919 |
| FED_CMS_POS_OTHER | CROSS_REF_PROVIDER_NUMBER | CCN | 98% | 5,419 | 99.8% | 5,406 | 0.999 | 12.2x | 040135, 042005, 050730, 133978, 203992 |
| FED_CMS_POS_OTHER | PARENT_PROVIDER_NUMBER | CCN | 100% | 2,333 | 99.0% | 2,309 | 0.994 | 12.1x | 440083, 450053, 040090, 230106, 450239 |
| FED_FEC_BULK_CANDIDATES | CAND_PCC | FEC_CMTE_ID | 100% | 10,630 | 98.6% | 10,485 | 0.992 | ~2.7e9x | C00413179, C00696641, C00699272, C00786277, C00716548 |
| FED_FEC_LEADERSHIP_PAC | FEC_CANDIDATE_ID | FEC_CAND_ID | 80% | 8,076 | 98.4% | 7,944 | 0.990 | ~5.2e9x | P00014910, P40013005, P40017543, S2KS00097, H2AZ06304 |
| FED_CMS_POS_OTHER | RELATED_PROVIDER_NUMBER | CCN | 100% | 474 | 97.7% | 463 | 0.986 | 11.9x | 211807, 141866, 361827, 391833, 513802 |
| FED_FEC_INDEPENDENT_EXPENDITURES | spe_id | FEC_CMTE_ID | 100% | 2,410 | 80.8% | 1,947 | 0.885 | ~2.2e9x | C00825539, C00798363, C00514224, C00740845, C00674218 |
| FED_FEC_COMMITTEES | C1 | FEC_CMTE_ID | 100% | 38,693 | 54.1% | 20,952 | 0.868 | ~1.5e9x | C00076836, C00392795, C00165233, C00620120, C00661801 |
| FED_FEC_CANDIDATES | C1 | FEC_CAND_ID | 82% | 19,142 | 54.2% | 10,367 | 0.849 | ~2.9e9x | H0TX05117, H2OK05151, H6FL01291, P40012379, P40016404 |
| FED_FEC_COMMITTEE_TO_CANDIDATE | OTHER_ID | FEC_CMTE_ID | 97% | 3,796 | 63.3% | 2,401 | 0.780 | ~1.7e9x | C00799106, C00301838, C00872671, C00718155, C00636670 |
| FED_FEC_CAND_CMTE_LINKAGE | C1 | FEC_CAND_ID | 84% | 15,153 | 57.2% | 8,665 | 0.775 | ~3.0e9x | H0PA12199, H0MI06152, H0FL16094, S0NM00124, H8NV03218 |
| FED_FEC_COMMITTEES | C15 | FEC_CAND_ID | 87% | 14,591 | 58.1% | 8,482 | 0.767 | ~3.1e9x | H0MI10279, H8VA05171, H0RI02287, H0MA04184, H8CA39166 |
| FED_CONGRESS_LEGISLATORS | FEC_IDS | FEC_CAND_ID | 89% | 1,531 | 54.2% | 830 | 0.725 | ~2.9e9x | H4TX24094, H2MI11133, H8GA06286, H2VA09010, H6NY11174 |
| FED_FEC_PAC_SUMMARY | C1 | FEC_CMTE_ID | 100% | 22,899 | 53.7% | 12,290 | 0.722 | ~1.5e9x | C00764498, C00167007, C00722223, C00815233, C00823104 |
| FED_FEC_CANDIDATES | C10 | FEC_CMTE_ID | 100% | 14,777 | 52.2% | 7,712 | 0.713 | ~1.4e9x | C00289140, C00666891, C00647990, C00698506, C00777177 |
| FED_FEC_CAND_CMTE_LINKAGE | C4 | FEC_CMTE_ID | 100% | 16,251 | 51.6% | 8,381 | 0.709 | ~1.4e9x | C00576645, C00660605, C00734988, C00741405, C00784751 |

Notes on the table:
- "beats-chance" = matched ÷ expected random collisions over the key's honest
  value space (`connect/discover.py::KEY_DOMAIN`, unchanged). The scorer is
  `discover.confidence()`, unchanged.
- The 52–58% FEC overlaps are multi-cycle IDs measured against a spine that
  currently holds a subset of cycles — the *unmatched* IDs are the new
  entities those tables would add.
- The 80% shape rate on FEC candidate columns is my regex undercounting
  presidential IDs (`P00014910` has digits where House/Senate IDs carry a
  state code). The overlap join uses the real normalizer and is unaffected.

## Borderline (1)

| table | column | suspected key | shape hit % | distinct | overlap % | matched | note |
|---|---|---|---|---|---|---|---|
| FED_EPA_TRI_BASIC_2023 | C_16_PARENT_CO_DB_NUM | DUNS | 100% | 3,791 | 0.4% | 16 | The name says Dun & Bradstreet and the shape agrees, but the live DUNS world is only ~30k values (NIH grants tables), so overlap can't prove it today. Re-test when the DUNS world grows. |

## Rejected on evidence — do not re-try these

**Passed the machine gate, fail mechanism review** (the confidence scorer's
STEEL fast-path skips the collision gate once 25 values match; for
name-sniffed columns that assumption doesn't hold — no name evidence exists):

- `FED_USGS_MINERALS.MRDS_ID` as BIOGUIDE (1.6% overlap): mineral-deposit IDs
  colliding with the 1-letter+6-digit shape. Not members of Congress.
- `XC_MAPPING_POLICE_VIOLENCE.ORI_AGENCY_IDENTIFIER_IF_AVAILABLE` as
  PWSID (3.3%) / NPDES (0.2%): FBI ORI agency IDs share the
  2-letter-state+7-digit shape with EPA water IDs. Prefix-structure collision,
  no mechanism.
- `FED_EPA_ECHO.SDWA_IDS` as NPDES (0.2%): residue — the same column is
  PWSID at 100%.
- Five ~0%-coverage DUNS "keeps": a follow-up sequence number (FAERS), two
  longitude columns (EPA), drug lot numbers (FDA), SEC file numbers. All
  STEEL-floor artifacts.

**Killed by the machinery, worth remembering:**

- **No hidden EINs exist.** All 161 nine-digit candidates (and their DUNS
  twins) failed overlap. The name tagger's `ein` token already catches every
  real EIN carrier in the landing zone.
- **The three giant sequence-ID impostors** — Open Payments record IDs, FAERS
  report IDs and drug sequence numbers — matched 45k–136k NPIs by brute
  cardinality but only ~11% of their values pass the NPI check digit (a real
  NPI column passes ~100%). The check-digit test is the definitive kill for
  10-digit sequence columns.
- **Senate lobbying registrant IDs are NOT SEC CIKs**: 27 matched vs ~96
  expected by chance. The lobbying registrant namespace stays unlinked to the
  SEC filer world.
- **FARA registration numbers are not UK company numbers** (0 matched; the
  synonym rule was a reach and is disproven).
- HRSA shortage-area IDs are not NPIs (below chance).

## Also found in passing

- **182 columns still carry the literal text 'nan'** (the known pandas loader
  corruption). List in the scratchpad inventory; overlaps the known 4.2M-cell
  repair but includes columns outside the earlier repair scope. Candidate for
  the standing data-trap repair list.
- **Zero Stage 1 query errors** across all 302 tables.

## Discrepancies vs the mission packet

- The packet points Stage 2 at an entity table that **does not exist** under
  that name in the entity schema. The live reference is the spine keyset table
  (`SPINE_KEYSET_LIVE`, 83.7M rows, 22 key families, post-rebuild) — used for
  all overlap measurements. Same semantics (normalized live spine values).
- The 2,216-vs-1,871 table-count discrepancy was not chased (per packet).
  One measured fact that narrows it: the non-portal landing universe is
  exactly 302 base tables.

## Method + spend

- Stage 0 (metadata only, $0): 12,741 non-portal columns fetched; 59 synonym
  hits.
- Stage 1 (~35 min busy warehouse, 6 lanes): per-table batched aggregates over
  50k-row subsamples; non-null / distinct / sentinel / 14 shape counters per
  column; checkpointed per table. First implementation re-computed the
  normalizer inside every aggregate (~12s/query); rewritten to normalize once
  per column (~2s/query, 6x).
- Stage 2 (~18 min, 6 lanes): full-column DISTINCT overlap against the spine
  keyset per suspected key, normalized by `connect.keys.normalize_sql`
  (imported), scored by `discover.confidence()` (unchanged, MIN_MATCH=3,
  COLLISION_MULT=5.0). Columns with several suspected keys tested in one query.
- Stage 2.5: NPI candidates got a Luhn check-digit rate over a 1,000-value
  sample (80840-prefixed). This is *additional stricter* evidence, not a
  loosened threshold.
- Total spend ≈ $2–4 (≈55 min busy X-Small serving warehouse + one metadata
  query). Packet estimate was $5–11.

## What happens next (human decisions — not taken here)

1. Wiring any of the 18 confirmed columns means editing the display specs and
   riding the **next** full spine rebuild (~$12–20). The 2026-08 batch rebuild
   already ran; these would be the start of the next batch.
2. The four positional-header FEC tables may deserve a **header repair at the
   load layer** (real column names) instead of wiring C1/C4 into specs —
   wiring cryptic names into the merge path bakes the confusion in. Build
   decision, not taken here.
3. The FEC_IDS flatten build (already parked) remains the right fix for
   multi-ID legislators; this run confirms the values are live FEC IDs.
