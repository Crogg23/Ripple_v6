# Next Session Plan — Quick Wins Sweep

*Built from `the_fix_list_2026-08-22.md`. Deliberately excludes the two XL items
(contracts re-pull, the 160-source no-loader backlog) — those need their own priced
decision, not a slot in a quick-wins session. Everything below is S or M effort,
sequenced so cheap/free wins go first and momentum carries into the judgment-heavy ones.*

**Target: one session, ~$15–25 total compute, mostly S/M items.**

---

## Phase 1 — free wins, zero risk (do these first, no thinking required)

1. **Drop the duplicate table** from 2026-08-22
   (`FED_NCHS_DRUG_POISONING_MORTALITY_COUNTY`) — one DROP statement.
2. **Run the dbt test suite and check the results are real** — confirms or kills the
   "505 uniqueness tests may not actually run" question in one shot.
3. **Mark the 104 dead ID columns as untrustworthy** in the column catalog/metadata —
   no rebuild, just labeling so nobody joins on them by accident.

**Phase 1 cost: $0. Time: under an hour.**

---

## Phase 2 — dedupe pass (cheap, high-impact correctness fixes)

Same shape of bug in five places — a runaway/paginated loader wrote the same rows
repeatedly. Dedupe query + rebuild, no re-download needed for any of these:

4. FHFA mortgage database (19M rows → real 7,204)
5. ForeignAssistance.gov (3.97M rows → real ~95,658)
6. NHTSA recall records (dedupe by recall ID + latest revision)
7. EPA ICIS Title V certificates (81% duplicate)
8. Google political-ad creative mapping (80% duplicate)

**Phase 2 cost: pennies. Time: ~2–3 hours** (five tables, same pattern, gets faster
after the first one).

---

## Phase 3 — reuse the existing epoch-date fix (already-built macro)

9. FAA aircraft registry — apply the guarded date macro to all four corrupted date
   columns; separately investigate why the tail-number key is 100% blank (one query).
10. CFTC futures + financial positions — same macro on the corrupted date column
    (the second date column is already fine, so this is a clean fix).

**Phase 3 cost: pennies. Time: ~1 hour** (the macro exists — this is applying it, not
building it).

---

## Phase 4 — the investigation-then-fix items (medium effort, real answers needed)

These need a "why" answered before a fix makes sense — but each is a single focused
investigation, not a project:

11. **Mine death counts reading zero** — find the code-mapping mismatch, fix it.
12. **SEC 13F unit mixing** — build the per-filer whole-dollars-vs-thousands detection
    rule (likely a magnitude heuristic against known large filers).
13. **NCUA wrong file loaded** — identify the correct source file, replace it.
14. **EPA penalty stamping** — redesign the case→facility join to allocate rather than
    copy the settlement total.

**Phase 4 cost: ~$4–6 compute. Time: ~4–6 hours** (each is its own small investigation).

---

## Phase 5 — the batch cleanup (breadth, not depth)

15. **openFDA: re-download the 8 wiped raw source tables** so they can be audited
    against their marts again.
16. **The remaining 20–80%-duplicate tables** not already covered in Phase 2 (FAERS
    outcomes, DHS immigration stats, EPA/NPDES informal enforcement, UK sanctions
    list, court financial disclosures, FEC committees/candidates, PBGC) — same dedupe
    pattern as Phase 2, just more of them.
17. **Re-run the scan on the 16 tables that errored out** last time (ICIJ nodes/edges,
    OpenSanctions, ICE detainers, SEC fund tables, EIA) — find out if they're broken
    or just choked the scanner.

**Phase 5 cost: ~$5–10 compute. Time: ~3–4 hours.**

---

## Deliberately NOT in this plan

- **Federal debarment list reload** — folded out of quick-wins; needs the same
  "identify the real current source" work as NCUA (Phase 4 item 13) but the debarment
  list's publisher access has historically been flaky — treat as its own follow-up if
  Phase 4's NCUA item goes smoothly.
- **FAERS column-shift full reload** — 62M rows, real money (L not M), and the parsing
  bug needs root-causing before a reload is worth doing. Own session.
- **30-sources-short-of-publisher batch** — too heterogeneous for a quick-wins pass;
  some are one-liners, some need real investigation. Worth its own triage session that
  sorts them into "cheap" vs "not cheap" first.
- **275 auto-guessed freshness cadences** — clerical, not urgent, and doesn't corrupt
  any actual analysis (it only mis-labels the *monitor*, not the data). Background task
  for whenever, not a session.
- **Contracts re-pull, no-loader backlog** — the two XL items; need their own priced
  go-ahead from Chris, not a slot here.

---

## Session totals

| | Time | Compute |
|---|---|---|
| Phase 1 | <1 hr | $0 |
| Phase 2 | 2–3 hrs | pennies |
| Phase 3 | ~1 hr | pennies |
| Phase 4 | 4–6 hrs | $4–6 |
| Phase 5 | 3–4 hrs | $5–10 |
| **Total** | **~11–15 hrs** | **~$10–20** |

That's **18 fix-list items closed** (out of 29) for under $20 — everything except the
two XL items and the three deliberately-deferred ones above. Phases are independent;
this can run as one long session or be split across several without losing anything.
