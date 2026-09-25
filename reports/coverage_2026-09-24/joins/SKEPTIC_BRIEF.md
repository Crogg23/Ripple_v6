# Dossier skeptic brief, 2026-09-24

You are a fresh-context skeptic. Break the dossier; don't polish it.

## Chris's words, verbatim
"3 strong leads is pitiful - do better"
"make sure you completely understand what is completed vs whats not and then continue on - I need things that I can put in a portfolio. Go"

His pitch: "I can join public datasets." A dossier is portfolio-grade only if a hostile data editor can't break any join or number in it.

## What you get
`reports/coverage_2026-09-24/joins/<id>.md` is the claim. `<id>.sql` holds every statement the builder ran. `<id>/` holds raw results.

## Attack, in order
1. **Every join:** right key? A name join needs a second field agreeing. Re-run the match count and eyeball 5 rows.
2. **The headline number:** re-derive it yourself. Check the denominator and the peer group.
3. **The chart rows:** re-run the query behind them. Does the chart say what the headline says?
4. **Misses cited as evidence:** is the table even complete enough for a miss to mean something?
5. **The boring explanation:** name it, test it if one query can.

## Rules
- Python door only, repo root: `from connect import db; c = db.connect()`. First: `ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300`, then `ALTER SESSION SET QUERY_TAG = 'joins-skeptic-2026-09-24'`.
- Read-only: SELECT and WITH only. The login is the all-powers admin role.
- At most 20 statements. Aggregate before joining.
- Read `C:\Users\wroge\.claude\projects\c--Code-Ripple-v6\memory\MEMORY.md` and trap files touching your tables.
- Scratch files only under `reports/coverage_2026-09-24/joins/<id>/skeptic/`. Never the shared scratchpad.
- Write `reports/coverage_2026-09-24/joins/<id>_skeptic.md`. If your tools cannot write files, put the full report in your final reply instead.

## Output
Per claim in the dossier: CONFIRMED / NARROWED / BROKEN, what you ran, the number you got.
Then: the corrected one-line story, the corrected chart rows if they changed, and a final grade A/B/C.
End with one line: AGREE or DISAGREE with the builder's grade, and why.
