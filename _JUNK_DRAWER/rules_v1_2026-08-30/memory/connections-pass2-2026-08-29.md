---
name: connections-pass2-2026-08-29
description: "2026-08-29 pass 2 of the master connections list — GLEIF L2 parent tree held+unused, TRI↔FRS live via EPA_REGISTRY_ID, HMDA respondent id is two namespaces, NADAC↔NDC needs 5-4 padding, IDV file + Fed holding-company file are the top missing joins; pass-1 name-matching was sloppy"
metadata: 
  node_type: memory
  type: project
  originSessionId: c98fb74d-28a1-45d1-8873-b6203398bc98
  modified: 2026-08-30T05:54:57.529Z
---

Pass 2 (`reports/recon/master_connections_pass2_2026-08-29.md`, script
`scripts/pass2_connections_check_2026_08_29.py`) value-checked 200 columns + ~105 overlap joins in 5 min / ~$1.

**Non-obvious findings to carry forward:**
- GLEIF Level-2 relationships (485K rows) = a 301K-child → 77K-parent corporate tree that resolves 99%+
  into GLEIF; nobody had wired it. Also GLEIF carries 3.0M national company numbers (132,901 Delaware).
- TRI facility: `FRS_ID` is dead but `EPA_REGISTRY_ID` resolves 99.9% into FRS — pass 1 declared the
  wrong column dead. Always check sibling columns before calling a link dead.
- HMDA historic `RESPONDENT_ID` is two namespaces keyed by `AGENCY_CODE`: agencies 1-3 = FDIC cert
  (70% resolve), agency 7 (HUD) = EIN-shaped for-profit lenders. Register with agency in the key.
- NADAC NDC (11-digit) ↔ NDC directory PRODUCTNDC ('LLLL-PPP' with dash) only joins after zero-padding to
  5-4 (82%); raw join = 0%.
- FDIC NEWCERT/ULTCERT/PARCERT resolve ~100% into CERT (bank lineage); RSSDHCR resolves 0% because
  holding companies are not banks — the Fed NIC file is not held.
- SAM exclusions NPI → NPPES 99.7% / LEIE 96.3%; exclusions UEI → SAM entity 0.3% is EXPECTED (excluded
  parties aren't registrants), not a load failure.
- Contracts `parent_award_id_piid` is an IDV id; the IDV file is a separate USAspending download and is
  not held (387K parents point nowhere).
- The 08-05 catalog's 493 "not held" rows were wrong on 37 (GUDID, NPDB, FAERS, USCG, UK PSC,
  Retraction Watch, FAC single audits, EIA ids, MC numbers…). Catalog verdicts are web guesses.
- Pass-1 name matching produced junk hits (FARA reg # as "FDA FEI", court dates as "BIS denied"):
  name-scan hits must be table-aware before value checks.

- Level-3 precision (60 sampled pairs/edge, names+states compared) ran the same night: 40/41 edges hold. The
  agency-stripped legacy-HMDA-id → FDIC-cert edge is ~50% wrong — never use it; route old HMDA through the
  official ARID→LEI crosswalk. Name-agreement is a floor: lineage edges (successor bank, predecessor CCN),
  site-vs-org keys (clinic NPI), and renamed firms (sanctioned ships, post-merger DUNS) score low on names
  with a correct key — read the mismatch examples before downgrading. Reusable script:
  scripts/pass2_precision_check_2026_08_29.py.

**How to apply:** when asked about corporate parents, start from GLEIF L2 + FDIC cert pointers + TRI
parent DUNS — those are measured. See [[official-id-inventory-2026-08-29]] and
[[nobrainer-acquisitions-2026-08-29]].


**Update 2026-08-29 (late):** folded into the Join Handbook as a separate "measured, not yet in spine" tier (57 pairs + 1 suspect) via `reports/viz/_build/pass2_edges_source_2026-08-29.py` -> `build_join_handbook.py` -> `build_join_handbook_md.py` (markdown is now generated, not hand-written). 9 pass-2 edges were already in the spine at the same rates. Not registered as spine specs yet.
