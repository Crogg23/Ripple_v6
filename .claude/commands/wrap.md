---
description: Close the session — skeptic pass over everything claimed, then the wrap.
---
Session close, in this order:

1. Run the `skeptic` subagent (Agent tool, subagent_type "skeptic") over every claim of done / works / fixed made this session. Give it Chris's requests verbatim, what was built (git diff + files), and each claim.
2. If the skeptic disagrees with anything, that goes first in the wrap, with both verdicts. Chris decides.
3. Any correction Chris made this session that is not yet in `.claude/corrections.md` — append it (one line, dated).
4. Any data trap found this session (a column that looks real but isn't, a count that lies) — one line in `.claude/traps.md`, dated.
5. Write the wrap: short, free-form, scannable — done, not done, waiting on Chris, rough cost (tokens + warehouse). Nothing else.

Do not commit or push unless Chris said to.
