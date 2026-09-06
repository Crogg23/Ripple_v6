# Brief for every hunch worker

You own ONE hunch. Deliver a folder `reports/tier1_deep_dive_2026-09-05/<id>_<slug>/` with:
- `queries.py` — every query you ran, using `_shared/q.py`'s `run(sql, label)`; log to `queries.log`
- `story.html` — built with `_shared/viz.py` (`base_fig`, `write_story`); 2 to 4 charts, prose beside each
- `findings.md` — the chain, in BAR SPEAK: what was checked, the number, what a hit means, what a miss means,
  what a skeptic would attack, the answer. End with one line: `STATUS: confirmed as written | confirmed but reframed | dead`
  and a one-line `HEADLINE:` with the number in it.

Rules:
- Read `.claude/traps.md` first. Assume every trap applies until you rule it out.
- Python door only: `from _shared.q import run` (run scripts from the repo root with `PYTHONPATH=reports/tier1_deep_dive_2026-09-05`).
  The chat plug-in door is 401 today; do not use it.
- SELECT only. Never CREATE, DROP, INSERT, MERGE, DELETE, ALTER. ACCOUNTADMIN, no net.
- LANDING columns are TEXT: try_to_number / try_to_date before comparing. USAspending landing columns are lowercase, quote them.
- A column that looks like an ID is not one until you count distinct and eyeball a sample.
- Rebuild the first-pass number a DIFFERENT way before writing it as fact. If it does not reproduce, say so and why.
- Prose for a reader with zero context: define CCN, NPI, HOLC, etc. once in one sentence, then never again.
- Never use the word "spine" for anything.
- Charts: no dual axes, no rainbows, fixed palette order from viz.py, one bold takeaway per chart title,
  legend for 2+ series, direct labels on the few marks that matter, hover on everything.
- Keep the warehouse cheap: aggregate in SQL, pull small result sets, no SELECT * on big tables.
- Do not write outside your folder. Do not commit.
- Final message to the orchestrator: HEADLINE line, STATUS line, 3 bullets of what changed vs the first pass, any trap you found.
