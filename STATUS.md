# RIPPLE STATUS — 2026-08-17 (session 3) — Court IDs registered (staged); grid filled

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing new.** Standing: the roll-call vote mart still disagrees with
its Python-built twin (113,512 vs 3,364 rows). Full offline suite re-run this
session: 3,034 passed, 2 skipped, that one pre-existing failure only.

---

## THE HEADLINE: the court world is measured and wired — it goes live at the rebuild

Chris said "just go" on court-ID registration. Done, with one deliberate catch:

- **19 of 20 court join surfaces verified at 99.2–100% referential match.**
  Court → docket is 100% on all 71.7M dockets; judge → assigned docket 100% on
  32.4M; judge → financial disclosure 99.8%; the disclosure money chain (1.9M
  investment lines) 99.4–99.6%. Evidence file + measuring script committed.
- **One defect found and excluded:** the "appointing judge" column on
  judgeships matches the judge table only 47% — it references a different
  record type. Wiring it would have manufactured false person entities.
- **Two new key axes are wired but DARK:** judge (person) and court
  (organization) specs, normalization, entity typing and collision math are
  all in the codebase behind one flag (`connect/keys.py:
  ENABLE_COURTLISTENER_SPINE`, default False), verified both ways.
- **Why dark:** flipping the flag changes the spine's config fingerprint,
  which by design freezes incremental spine updates until a FULL spine
  rebuild re-pins it. The full rebuild is the parked ~$10–15 / ~4.5h decision.
  **Flip the flag in the same session that runs the rebuild — never before.**
  The rebuild now buys more than before: judge dossiers, court caseload
  ledgers, and the judges-money-cases lane, all on hard IDs.

## Earlier today (sessions 1–2, all committed and pushed)

- Ladder corrections patched into the ladder doc + rankings digest.
- **Census grid FILLED for ~$2:** all 589 mart models measured (1.23B rows;
  306 fresh into 2026; 12 stale). Pension tax-ID check PASSED (100% filled;
  join zero-padded — leading zeros stripped). Staging→raw crosswalk built
  (1,170/1,172; 2 broken staging views found). Ranked data-trap census in the
  fill summary (FAERS 76% dup rows, contracts epoch-1970 on all 20M rows,
  SEC year-0095 dates, foreign-assistance single-value tax-ID, etc.).

**Where:** `reports/census_grid_2026-08-12/fill/` (FILL_SUMMARY.md front page,
now incl. the court registration section). Tree clean except this file.

## Live/open items

- **Identity-map FULL rebuild (~$10–15, ~4.5h) — parked with Chris, now the
  gate for lighting up the court keys** (flip the flag in that session).
- Data-trap repairs, ranked by the fill (FAERS dup, contracts epoch dates,
  NEISS future dates, SEC year-zero, foreign-assistance tax-ID, 2 broken
  staging views).
- Source-registry reconciliation: staging→raw leg done; onboarding-log leg
  (774 vs 1,141 vs 1,329) still unjoined.
- Court→outside-world bridge: 200 courts carry a Federal Judicial Center
  bridge ID — a future crosswalk out of the court namespace.
- Roll-call mart rebuild via Python builder (standing).
- CourtListener citation-network load retry still pending.

**YOUR MOVE:**
1. Rule on the full spine rebuild (~$10–15, ~4.5h): it now also lights up the
   court keys. Say "go" and next session runs it with the flag flipped.

**NEXT SESSION:**
1. Boot trust check against this file and git log.
2. On rebuild go: flip the court-keys flag, run the full spine rebuild,
   re-seed incremental, re-measure the graph (expect 2 new key families).
3. Otherwise: top data-trap repairs (FAERS dup + broken staging views first).

**Tests:** full offline suite run this session — 3,034 passed, 2 skipped,
1 pre-existing failure (roll-call mart twin). Nothing new broken.

**COST:** session 3 ~$1 — court join measurements over 71.7M-row tables
(~5 min warehouse) + a 16-min local test run. Whole day all-in: ~$3-4.
