# Handoff: the verification sweep survey

Paste everything below into a fresh session.

---

Chris here. Before any analysis or publishing happens on Ripple, I want to re-walk the project on checked ground. Weeks of building outran verifying — the drift audit showed ~a third of past "done" claims had no verification near them. Today's job is NOT to fix anything. It is to build me the ranked list of what's worth reviewing.

**Your task, one deliverable:**
A single ranked table of every reviewable area in this project, from "biggest impact if it's wrong" down to "trivial, can leave as is." I pick from it; you don't start any review until I do.

**How to build it (survey, don't dive):**
- Surface pass only. For each area: one row — what it is, what "wrong" would cost me, how it would be checked, rough effort (minutes / hours / a day), and a 0–10 impact score. Park everything deeper with one line.
- Draw candidates from the whole width, not just recent work. At minimum walk: the warehouse loads (row counts vs publisher reality — truncation has bitten before), the load registry vs what's actually landed, the join handbook's claimed edges (measured verdicts vs name-checked), the place columns and clock columns claims, the entity/key checks (a column isn't an ID until COUNT(DISTINCT) + sample says so), the overnight loaders that were never checked, the retired spine's leftovers still imported by live code, the dbt models and tests, the reports/ folder's standing claims, and anything a `git log` walk or the transcripts flag as "done" without a check. That list is a floor, not the ceiling — add what I've forgotten.
- Sources: git history, the repo, `reports/`, `data/` checkpoints and logs, past transcripts (in `~/.claude/projects/c--Code-Ripple-v6/` — look things up there, don't ask me to re-explain), and read-only warehouse queries through the Python-scripts door. Cheap queries fine; anything that smells of real cost, price it first (/price).
- `_JUNK_DRAWER/` is reference-only for "did we already try this" — never a review target.
- Where a claim already has a verification receipt (a test, a spot-check file, a skeptic pass), say so and rank it low. Don't re-earn what's earned.

**Ranking means:** impact on the credibility of what I'd eventually analyze or publish. A wrong row count in a table I'll cite = top. A stale HTML page nobody links = bottom.

**Output shape:** one table, ranked, scannable. Under it: the top 3 you'd do first and why, in three lines. Then stop and let me pick.
