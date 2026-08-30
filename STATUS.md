# RIPPLE STATUS — 2026-08-29 (very late) — Join Handbook now carries the pass-2 connections as its own "measured, not yet in spine" tier; markdown handbook is generated, not hand-written

*One screen. Rewritten (never appended) at the end of every session.*

## 🚨 Read this first

1. **Standing rules from Chris today (in memory):** (a) answer the question asked, no build plans / costs /
   next steps unless he says "think it through"; (b) time + geography are first-class joins; the ID spine is
   deprioritized. Don't restate limits he already knows.
2. **The Join Handbook (both the markdown file and the standalone web page) now shows the pass-2 findings:**
   56 new connection pairs under a separate purple "measured 2026-08-29, not yet in the spine" heading on each
   table (never mixed with the 1,859 spine-verified ones), 1 red "suspect — do not use" edge (old HMDA lender
   id → bank cert, ~half wrong; the LEI crosswalk is the safe route), 49 new plain-English glossary rows, a
   6-item traps list, and a 4-row corrections table (TRI↔FRS is live via the registry-id column, ISIN really
   dead, nursing-home "affiliation id" = chain id, catalog wrong on 37). 21 tables appear in the handbook for
   the first time (drug prices, device registry, NDC directory, sanctions lists, contractor registry, FMCSA,
   subawards, Coast Guard vessels, ship tracking, rail accidents, GLEIF parent tree…).
3. **Yellow-lane call made:** the new edges were NOT registered in the spine. They live in a small pass-2 edge
   file that the handbook build merges in as its own tier. Reason: apply-config hasn't run (drift test is red),
   so registering families tonight would have left the handbook and spine disagreeing anyway. When the pass-2
   families are registered, delete them from the pass-2 file and they move into the spine tier automatically.
4. **9 of the 66 pass-2 edges were already in the spine at the same rates** (clinic NPI, xref LEI, venue LEI,
   both exclusion-list NPI edges, OSHA EIN→BMF, ICE facility, bill sponsor, committee→candidate) — a free
   confirmation that the pass-2 numbers agree with the spine. They were skipped, not duplicated.
5. **Unchanged:** apply-config not yet run (drift test red until it is); 8 spatial join errors (TRI + NTSB
   coords); DOCKET ~40% wrong; Snowflake MCP token rejected (direct python connection works — use it);
   overnight loads (MAUDE, subawards, LDA) unchecked; SAM public extract has no DUNS; IDV file and Fed
   holding-company file still not held.
6. **Git:** working tree holds the pass-2 report + scripts + JSON (from the earlier session) and tonight's
   handbook rebuild (5 new build files, 2 modified build files, both regenerated handbooks, this file).
   Nothing committed.

## BROKE

Nothing broke. Seven follow-up overlap counts that the earlier session ran by hand (and never logged) were
re-run tonight so the handbook carries real matched counts, not estimates — every one reproduced exactly.
The page's script passes a syntax check; it was not opened in a browser this session.

## YOUR MOVE (Chris)

Nothing blocking.

## NEXT (only when asked)

- Value scan of the 2,244 place columns (~$1–2).
- Parse the OpenSanctions / CSL identifier blobs into typed keys.
- Check the overnight MAUDE load — the partner the 5.2M device IDs are waiting for.
- Land the IDV file and the Fed holding-company file (both free bulk).
- Split the old HMDA lender id by agency code and re-test; if it holds, promote it out of "suspect".

**Cost note:** ~7 small read-only warehouse queries (well under $1). No storage added.
