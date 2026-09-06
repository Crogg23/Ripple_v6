# Probe brief: politics and markets hunches, first number only

Goal: one real number per hunch, tonight, cheap. No charts, no story. Decide lit / dim / dead.

Per hunch, a folder `reports/politics_probe_2026-09-05/<id>_<slug>/` with:
- `probe.py` — every query, via `from _shared.q import run` (run from repo root, `PYTHONPATH=reports/politics_probe_2026-09-05`), logged to `probe.log`
- `probe.md` — 10 lines max: what was checked, the first number, what a hit means, what a miss means, the trap you hit, then
  `STATUS: lit | dim | dead` (lit = a real number worth a deep dive; dim = runs but thin or one-vintage; dead = the leg does not exist)
  and `HEADLINE: <one line with the number>`.

Rules:
- Read `.claude/traps.md` first; the FEC, House disbursements, FD PTR, USAspending, and name-match traps all bite here.
- Python door only, SELECT only, ACCOUNTADMIN with no net. Never CREATE/DROP/INSERT/MERGE/DELETE/ALTER.
- Discover before you join: `information_schema.columns` for every table, `count(*)` plus `count(distinct)` on any column you treat as a key, `LIMIT 5` sample. Check LANDING vs mart row counts; they can be different files.
- Name matches: multi-word names only, verify 3 hits by eye, report the false-positive rate you saw. A single-word or surname match is noise.
- Budget: aim under 15 queries per hunch, aggregate in SQL, no row-level pulls from big tables (FEC indiv is large, dockets is 71.7M).
- If a table the chain needs is not landed, say so, name the nearest substitute, mark dead or dim, and stop. Do not build the missing leg.
- Never use the word "spine".
- Final message: HEADLINE, STATUS, one line on the trap, one line on cost (query count, longest query seconds).
