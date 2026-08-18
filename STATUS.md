# RIPPLE STATUS — 2026-08-18 — Sniffer batch wired + tested; rebuild command blocked at the classifier, on Chris's desk

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing new.** Standing: roll-call vote mart still disagrees with its
Python-built twin. Suite after the wiring: 3,096 passed, 2 skipped, that one
standing failure deselected. **BLOCKED: the spine rebuild command — the
permission classifier refuses warehouse-writing commands from sessions (the
known DROP-TABLE pattern). Chris runs one line, or grants the permission.**

---

## WHERE THE REBUILD STANDS (Chris said "go" — everything but the run is done)

Chris approved wiring the 2026-08-18 value-shape sniffer findings and running
the full rebuild (~$12–20, ~4.5h). This session:

- **Wired the graph:** 17 table-scoped column→key entries in the connection
  key map (the four positional-header FEC history tables' C-columns, the FEC
  crosswalk columns, the EPA case-facilities ID, ECHO's water-system column,
  the four CMS facility-chain columns).
- **Wired the spine:** 5 new spec tables (FEC committees / candidates /
  linkage / PAC summary multi-cycle histories + EPA enforcement-conclusion
  facilities) and 3 extra-key additions on wired tables (leadership-PAC →
  candidate, committee-to-candidate counterpart, ECHO → water system).
  Column meanings for the positional tables verified against live sample rows
  (they are the raw FEC bulk layouts). Name-mislabeling audit done per column:
  cross-entity references (candidate-on-committee-row etc.) are graph-only,
  never extra_keys — the buyer-DEA precedent.
- **Deliberately excluded:** legislators' FEC-IDs JSON-list column (would mint
  concatenated-ID phantom entities; the flatten build is the fix), the CMS
  chain columns as spine keys (different-entity mislabeling), the TRI
  Dun&Bradstreet column (unprovable until the DUNS world grows).
- **Tests:** full suite green after the wiring (3,096 passed / 2 skipped /
  standing failure only). Committed.

**TO RUN (Chris, in the repo, in order):**
1. `python -m connect spine`         (~4.5h, ~$12–20 — the rebuild)
2. `python -m connect seed`          (re-pins incremental; prints ONE line at
   the very END — hours of silence is normal, do not kill it)
3. Next session then refreshes the graph (re-fingerprint the ~10 affected
   tables + discover) and re-measures — no money decision there.

Alternative: add a permission rule allowing `python -m connect ...` and a
session babysits all three steps.

## THIS SESSION ALSO: the sniffer run itself (done, reported)

`reports/value_shape_findings_2026-08-18.md` — scanned all 11,547 non-portal
landing columns, 18 confirmed hidden-ID columns, rejects documented (zero
hidden EINs anywhere; lobbying registrant IDs ≠ SEC CIKs; sequence-ID
impostors killed by the NPI check digit). ~$2–4 spend vs $5–11 estimate.
Also: 182 columns still hold literal 'nan' text (inventory in reports/).

## Live/open items

- FEC-IDs flatten build (parked; this session proved the values are live).
- FEC positional-header tables: header repair at the load layer parked as the
  cleaner long-term fix (needs table-alter rights; wiring-as-is is in and
  documented per column).
- Data-trap repairs ranked by the fill + the 182 'nan' columns.
- Source-registry reconciliation (onboarding-log leg open).
- Roll-call mart rebuild via Python builder (standing).
- CourtListener citation-network load retry (standing).
- Table-count discrepancy (2,216 claimed vs 1,871 live) unchased; non-portal
  landing = exactly 302 base tables (measured this session).

**YOUR MOVE:** run the two commands above (price shown), or grant the
permission and say "go" again — a session runs and babysits all three steps.

**NEXT SESSION:**
1. Boot trust check vs this file and git log.
2. If the rebuild ran: graph refresh (re-fingerprint affected tables +
   discover), re-measure, update the graph JSON, brief with new numbers.
3. Otherwise: FEC-IDs flatten build or top data-trap repairs.

**Tests:** 3,096 passed / 2 skipped / 1 standing failure (deselected), run
after the wiring edits, before commit.

**COST:** session ~$2–4 warehouse (sniffer stages ~55 min busy X-Small) +
Fable tokens. The rebuild's $12–20 is approved but UNSPENT (blocked command).
