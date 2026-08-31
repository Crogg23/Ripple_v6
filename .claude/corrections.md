# Chris's corrections — one line each, newest at the bottom.
# Injected into every prompt by .claude/hooks/chris-words.sh (last 40). Add with /correction <text>.
# This is the only place rules grow. If it gets long, that's the signal something belongs in a hook.

2026-08-30 — label + description paragraphs read as "dumb paragraphs"; comparable things go in a table, everything else short spaced lines.
2026-08-30 — same font same size same color with no spacing is unreadable; blank lines between ideas, bold headers for altitude.
2026-08-30 — "the warehouse is down" was wrong: two doors (Python scripts / chat plug-in), they fail separately, name which.
2026-08-30 — don't say something "exists" at its last-known status; say what state it's in now (the spine is retired, not live).
2026-08-30 — riff mode does not suspend the output shape: paragraphs over three lines are still banned. Short spaced lines, bold scan-words, blank lines between ideas — even when arguing.
2026-08-31 — when he asks for real job postings as market data, give the postings flat: company, role, requirements. Don't filter by open/filled status or hedge with "not applying anyway" — that's not the point, it's noise on top of the answer he asked for.
2026-08-31 — output shape keeps reverting mid-session: sentences grow clauses, parentheticals stack, lines run past three. Every message, not just the first. One idea per line, blank line between, cut the parentheticals.
2026-08-31 — FINAL on format, hard countable rules: max 12 words per line outside tables. No parentheses. One dash per line max. Table cells are fragments, never sentences. Receipts and file paths go in the report file, not the chat. If a line needs a second clause, it's two lines.
2026-08-31 — visual variety required: headers, bullets, emojis. Not all same size and color. Every update message.
2026-08-31 — BAR SPEAK, the master register: explain everything like telling a sharp friend at a bar. Plain words, short lines, every fact survives. Compress by word choice, never by leaving things out.
2026-08-31 — methodology: "through simplicity, comes complexity." Every finding walks its chain — what was checked, what a hit means, what a miss means. A label ("vintage drift") is not a chain. "It's complicated" is where work starts, never where it ends.
2026-08-30 — the spine is dead, full stop. Calling any new thing a spine is wrong.
2026-08-31 — the double output was the two blocking Stop hooks; a Stop hook fires after the message is already on screen, so blocking can only force a second copy. Never make a Stop hook block. Carry violations forward into the next turn instead.
2026-08-31 — answer in chat, receipts in the file. The answer, the numbers and the call go in chat; long tables and paths go in the report file. Being sent into the repo to read something and come back is a recurring complaint since 2026-08-06.
2026-08-31 — the A+ shape, from 1,414 of his own messages: headline as a fact, then a fenced monospace numbers block, then 3-5 capped bullets, then one bold arrow line. One screen, never scroll. Stacked short prose lines still read as a paragraph — bullets and indentation must carry the structure.
2026-08-31 — cap the count before he asks. He requests "5 bullets" / "3-4 per option" constantly. Promise a number and hit it.
2026-08-31 — auto mode runs a safety classifier on every shell command; it reads the command text only, not the conversation, so it cannot see that Chris authorised something. It denies immediate irreversible deletes. Do not try to edit its own config to get past it. Say what is blocked, in one line, and ask him to shift-tab out of auto mode.
2026-08-31 — measure before naming a cause. The 6.95 GB pack was blamed on .venv in history; it was actually three recent unreachable blobs, and the real fix was gc with the window set to now, not a history rewrite. Reachable bytes versus pack size is the check that separates the two.
