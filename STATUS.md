# RIPPLE STATUS — 2026-08-26 (late) — Merged a stranded Mac session; entity graph is now KNOWN STALE; one real scope contradiction found, not resolved

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

## 🚨 Read this part first — three things need a decision before more work happens

1. **The live entity graph is stale again, on purpose — do NOT just re-run the
   rebuild.** Merging in a second machine's stranded work (below) added 88 more
   sources to the wiring list, ~79 of them low-trust scraped city/county open-data
   portals. Those portal sources were wired in on 2026-08-24, on a different
   machine, **before** today's separate ruling that portal data is out of scope
   for the entity graph. That's a live contradiction between two sessions'
   decisions, not something to silently pick a side on.
2. **A viz options menu from yesterday is still waiting on a pick.** Nothing
   since has picked from it. Real, finished deliverable, zero Chris input yet:
   `reports/VIZ_OPTIONS_MAP_2026-08-25.md` (60 picture ideas, 30 tools compared)
   + a browsable, filterable version at `reports/viz/options_board_2026-08-25.html`.
3. **The 385-hard-cap reload task from earlier tonight is still undecided.**
   99% of that bucket (381 of 385) turned out to be the same low-trust portal
   data — Chris was asked how to proceed and said "something else" with no
   detail before moving to this handoff. Only 4 sources in that bucket are
   real: USGS 3DEP, ATF firearm-dealer locations, DOL/OFCCP compliance list,
   Bangladesh's national open-data portal.

## What actually happened tonight (long session, several real turns)

**Round A — the planned work:** fixed the tool that builds analytics tables on
top of raw data pulls (it was silently copying raw data instead of building on
a cleaner, already-deduped version, whenever one existed — the same bug class
behind 8 known bad-mart incidents this month). Ran it against the one backlog
that was genuinely ready (real, complete data, just no finished table yet):
**43 new finished tables**, tested clean. Also corrected a wrong headline
number from earlier tonight: the real count of sources stuck at "only a
preview pulled, not the real data" is **1,567**, not 414 as first claimed.

**Round B — six real bugs found and fixed in the entity-graph wiring file,**
caught because a crash on a dead/typo'd table reference was hiding them:
a leftover duplicate reference to already-superseded data, three tables a
prior review had explicitly ruled out getting silently re-added by a
generator tool, and two cases where a table reference used lowercase column
names that are a hard database error under how this system actually reads
them (meaning those two data sources were contributing **zero** rows to the
entity graph despite looking "wired," including the single biggest one —
93 million federal contract records).

**Round C — ran the full entity-graph rebuild** (with sign-off; real cost,
real time) to make Round B's fixes actually reach the live data instead of
sitting in source files. Result, checked live: **35,951,018 entities**, 20
million of them linked across more than one data source, built from 90
million raw rows. Confirmed live that removed sources dropped to zero rows
and previously-broken sources now genuinely contribute (528,670 rows from
the once-broken 93M-row USASpending table alone).

**Round D — while starting the next task, discovered this machine's copy of
the code had fallen behind a second machine's work that never got pulled in.**
A routine sync (not run by this session — likely triggered from the editor)
surfaced a merge with 2 hours of real work from a Mac session on 2026-08-24/25
that had been sitting on the shared remote, unmerged, the whole time this
session ran. Reconciling it found:
- The Mac session had **already independently found and fixed 2 of the same 6
  bugs from Round B** (the dead/typo'd reference, one of the lowercase-column
  cases) two days earlier — same bugs, found twice, because the two machines
  hadn't synced.
- It also fixed **2 more real bugs** this session hadn't touched: another
  lowercase-column mismatch, and a real data-quality gap where a missing name
  on some scraped-portal rows was landing as the literal text "nan" instead of
  a true blank (a known trap, documented before — see memory — now fixed in a
  second place it was hiding).
- It added **92 new candidate sources** to the wiring file (draft packets
  written for human review by a new tool, `scripts/spine_wiring_prep.py`) —
  11 real federal ones plus ~79 scraped-portal ones, the portal-scope
  contradiction flagged above.
- Merging created **2 accidental duplicate entries** (two sessions had each
  added a fix for the same table under the same name, in different spots in
  the file) — found and cleaned up; confirmed via the live code which version
  was actually taking effect before touching anything, both times the more
  complete version was already winning.
- **Also surfaced, not fixed:** 2 *pre-existing* duplicate entries (predate
  both sessions) for two EPA water-discharge tables, each defined twice under
  two genuinely different key types (one measured/verified, one not) — a real
  data-quality question, needs someone to check which key is actually better
  populated on live data before picking one. Not touched tonight; flagged only.

**After reconciling:** full test suite re-run clean — 304 checks passed, 0
failures (up from 215 before the merge, since the merge added real coverage).
The merge is otherwise complete and safe to build on. **The rebuild from
Round C has NOT been re-run since this merge** — see item 1 at the top.

## BROKE

Nothing from this session's own work — every fix was checked against a live
test before being trusted, twice over (once for tonight's own changes, again
after reconciling the second machine's work). The Senate LDA lobbying loader
is still running in the background, still healthy, last confirmed on year
2008.

## YOUR MOVE (Chris)

1. **The portal-scope contradiction (item 1 above)** — should those ~79
   already-wired scraped-portal sources come OUT of the entity-graph wiring
   file to match today's ruling, or does today's ruling only apply going
   forward? Real decision, not a technical one.
2. **Pick from the visualization options menu** (item 2 above) — still
   nobody's chosen anything from it.
3. **The 385-bucket reload decision (item 3 above)** — still open.
4. **Drop the old truncated USASpending contracts table** — still open,
   fully superseded now twice over.
   `DROP TABLE LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL;`
5. **GFI trade data** — still needs a dedicated Tableau-scraping session.
6. **The stale politics timeline table** — view instead of table, or
   something else? Still undecided, not urgent.
7. **Push local commits to origin** whenever wanted — not automatic.

## NEXT

The very next session's stated focus (per Chris) is a **full, comprehensive
numeric audit of the whole warehouse** — turn everything measurable into a
number. That's a distinct, large piece of work; see the handoff document
(path given to that session directly) for how it's scoped. Before or
alongside that: the portal-scope contradiction (YOUR MOVE #1) should get
resolved before anyone spends real money re-running the entity-graph rebuild
again, since the answer changes what that rebuild should even include.

**Cost note:** tonight's spend beyond the day's earlier ~$10-14: the full
entity-graph rebuild (real warehouse compute, approved before running, came
in noticeably faster than the ~4.5-hour estimate) plus several quick test
runs and small table builds. Not separately meter-verified this instant.

## Not committed

Working tree has an in-progress merge being finalized as this file is
written — commit follows immediately after. Once committed: local commits
sit ahead of origin, not pushed (no standing approval to push automatically).
